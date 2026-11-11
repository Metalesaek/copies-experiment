"""Copies are not confirmations: continual learning from a stream of news reports.

  python run_copies.py --seeds 10 11 12 --tag copies_v1                 # all systems x attacks
  python run_copies.py --systems every_report chains_k --attacks copy --seeds 10 --tag try
  python run_copies.py --set copies.attack_copies=20 --tag copies_m20     # any config key

Needs the first paper's code next to this folder (../sura_experiment) and its environment.

Systems (when a claim is learned)
  every_report    each report is a training example: copies repeat the claim (no gate)
  first_report    a claim is learned once, at its first report (copies ignored, no gate)
  reports_k       learned once it has been reported k times (counts copies as confirmations)
  chains_k        learned once k independent chains report it (copies of one chain count once)
  judge           learned at its first report if the judge approves (first paper's verifier key)
  chains_k_judge  chains_k AND the judge approves
Attacks on lies: copy, paraphrase, collusion (see copies_world.py).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sura_experiment"))

import torch  # noqa: E402

from copies_world import build_reports, chain_size_sampler  # noqa: E402
from sura.config import load_config  # noqa: E402
from sura.data import build_world, load_counterfact, screen_known  # noqa: E402
from sura.metrics import evaluate  # noqa: E402
from sura.runner import ReplayBuffer  # noqa: E402
from sura.student import Student, resolve_device, resolve_dtype  # noqa: E402
from sura.verifier import NoisyVerifier  # noqa: E402

SYSTEMS = ("every_report", "first_report", "reports_k", "chains_k", "judge", "chains_k_judge",
           "judge_all", "judge_chains")
REAL_JUDGE = ("judge_all", "judge_chains")   # need a running Ollama server (copies.judge_model)
ATTACKS = ("copy", "paraphrase", "collusion")


class RealJudge:
    """Local Ollama judge. Verdicts are cached per prompt (in memory and in a jsonl file), so a
    claim is only re-judged when the evidence shown to the judge changes."""

    def __init__(self, model: str, url: str, cache_file: Path, max_tokens: int = 10):
        self.model, self.url, self.file, self.max_tokens = model, url, cache_file, max_tokens
        self.cache, self.unparsed, self.calls = {}, 0, 0
        if cache_file.exists():
            for line in cache_file.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                self.cache[r["msg"]] = r["verdict"]

    def __call__(self, msg: str) -> bool:
        if msg not in self.cache:
            from judge_copies import ask, parse
            v = parse(ask(self.model, self.url, msg, max_tokens=self.max_tokens))
            self.calls += 1
            self.unparsed += v is None
            self.cache[msg] = bool(v)
            with self.file.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"msg": msg, "verdict": bool(v)}) + "\n")
        return self.cache[msg]


def shown(evidence: list, system: str, max_reports: int) -> list[tuple[str, str]]:
    """Reports shown to the real judge: all of them (judge_all) or the first report of each chain the
    copy detector sees (judge_chains). At most max_reports, the earliest first."""
    if system == "judge_chains":
        first = {}
        for r in evidence:
            first.setdefault(r.seen_chain, r)
        evidence = list(first.values())
    return [(r.outlet, r.text) for r in evidence[:max_reports]]


def run_one(system, cfg, student, world, reports, verifier, seed, real_judge=None, judge_only=False):
    T, C, bs = cfg.train, cfg.copies, cfg.eval.batch_size
    rng = random.Random(seed * 7919 + SYSTEMS.index(system))
    torch.manual_seed(seed)
    student.reset_adapter()
    opt = student.new_optimizer(T.lr)
    buffer = ReplayBuffer(T.buffer_capacity)
    anchor = [c.sentence for c in world.anchor]
    key = lambda c: (c.uid, c.target)

    n_reports, chains, first_seen, accepted = defaultdict(int), defaultdict(set), {}, {}
    verdict, evidence = {}, defaultdict(list)
    if system in REAL_JUDGE:
        from judge_copies import reports_message
    log = dict(examples_trained=0, lie_examples_trained=0)
    t0 = time.time()
    for k in range(0, len(reports), C.chunk_size):
        chunk = reports[k:k + C.chunk_size]
        new = []
        for r in chunk:
            c = r.claim
            n_reports[key(c)] += 1
            chains[key(c)].add(r.seen_chain)
            first_seen.setdefault(key(c), r.time)
            if key(c) in accepted:
                continue
            if system in ("judge", "chains_k_judge") and key(c) not in verdict:
                verdict[key(c)] = verifier.judge([c], world.evidence)[0]
            if system in REAL_JUDGE:  # re-judged with the evidence so far (cached when it did not change)
                evidence[key(c)].append(r)
                ok = real_judge(reports_message(c, shown(evidence[key(c)], system, C.judge_max_reports)))
            else:
                ok = {"every_report": True, "first_report": True,
                      "reports_k": n_reports[key(c)] >= C.reports_k,
                      "chains_k": len(chains[key(c)]) >= C.chains_k,
                      "judge": verdict.get(key(c), False),
                      "chains_k_judge": len(chains[key(c)]) >= C.chains_k and verdict.get(key(c), False)}[system]
            if ok:
                accepted[key(c)] = (c, r.time)
                new.append(c)
        train = [r.claim for r in chunk] if system == "every_report" else new
        if not train or judge_only:  # judge_only: only collect the judge's verdicts, no training
            continue
        log["examples_trained"] += len(train)
        log["lie_examples_trained"] += sum(not c.is_true for c in train)
        batch = train + buffer.sample(T.replay_size, rng)
        student.train_steps(opt, [c.prompt for c in batch], [c.target for c in batch], anchor, T,
                            T.steps_per_chunk, rng)
        buffer.add([(1.0, c) for c in new or train])

    if judge_only:
        return {}
    res = evaluate(student, world, bs)
    acc = list(accepted.values())
    true_claims = [c for c in dict.fromkeys(world.new + world.updates)]
    lies = [c for c in dict.fromkeys(world.poison_fict + world.poison_real)]
    res |= log
    res["accepted_true_share"] = sum(c.is_true for c, _ in acc) / len(true_claims)
    res["accepted_lie_share"] = sum(not c.is_true for c, _ in acc) / len(lies)
    res["lies_per_1000_accepted"] = 1000 * sum(not c.is_true for c, _ in acc) / max(len(acc), 1)
    delays = [t - first_seen[key(c)] for c, t in acc if c.is_true]
    res["mean_delay_days_true"] = sum(delays) / len(delays) if delays else None
    res["minutes"] = (time.time() - t0) / 60
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(HERE / "configs" / "copies.yaml"))
    ap.add_argument("--systems", nargs="+", default=list(SYSTEMS))
    ap.add_argument("--attacks", nargs="+", default=list(ATTACKS))
    ap.add_argument("--seeds", nargs="+", type=int, default=[10])
    ap.add_argument("--poison_rate", type=float, default=0.3)
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--judge_only", action="store_true",
                    help="only fill the real judge's verdict cache (Ollama on, no training); then rerun without "
                         "this flag (Ollama can be off: every verdict comes from the cache)")
    a = ap.parse_args()

    cfg = load_config(a.config, a.set)
    out = HERE / cfg.output_dir / a.tag
    out.mkdir(parents=True, exist_ok=True)
    results = out / "results.jsonl"
    done = set()
    if results.exists():
        for line in results.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["system"], r["attack"], r["seed"]))

    device = resolve_device(cfg.device)
    dtype = resolve_dtype(cfg.dtype, device)
    student = Student(cfg, device, dtype)
    records = load_counterfact(cfg.data.counterfact_split, cfg.data.n_counterfact)
    slug = cfg.student.model_name.replace("/", "_")
    cache = (HERE / cfg.cache_dir).resolve() / f"known_{slug}_{cfg.data.counterfact_split}_{cfg.data.n_counterfact}.json"
    known = screen_known(student, records, cache, cfg.eval.batch_size)
    sample_size, sizes = chain_size_sampler(HERE / cfg.copies.chain_file, cfg.copies.corpus_articles)
    print(f"student knows {len(known)} facts; chain sizes (outlets: chains) {dict(sorted(sizes.items())[:6])} ...")

    real_judge = None
    if set(a.systems) & set(REAL_JUDGE):
        real_judge = RealJudge(cfg.copies.judge_model, cfg.copies.judge_url,
                               out / f"judge_cache_{cfg.copies.judge_model.replace(':', '_')}.jsonl",
                               getattr(cfg.copies, "judge_max_tokens", 10))
        print(f"real judge: {cfg.copies.judge_model} ({len(real_judge.cache)} cached verdicts)")

    for seed in a.seeds:
        world = build_world(cfg, known, a.poison_rate, seed)
        verifier = NoisyVerifier(cfg.verifier.accuracy, seed)
        for attack in a.attacks:
            reports = build_reports(world, cfg.copies, sample_size, attack, seed)
            n_lie = sum(not r.claim.is_true for r in reports)
            print(f"\nseed={seed} attack={attack}: {len(reports)} reports ({n_lie} lie reports)")
            if getattr(cfg.copies, "carriers", "simulated") == "real":   # what the real detector did
                from real_carriers import DETECTOR_STATS, stats_line
                print("  " + stats_line(DETECTOR_STATS))
                with (out / "detector_stats.jsonl").open("a", encoding="utf-8") as f:
                    f.write(json.dumps(dict(seed=seed, attack=attack, **DETECTOR_STATS)) + "\n")
            for system in a.systems:
                if (system, attack, seed) in done:
                    print(f"  {system:<15} done")
                    continue
                calls0 = real_judge.calls if real_judge else 0
                if a.judge_only:
                    if system in REAL_JUDGE:
                        run_one(system, cfg, student, world, reports, verifier, seed, real_judge, judge_only=True)
                        print(f"  {system:<15} {real_judge.calls - calls0} new verdicts "
                              f"({len(real_judge.cache)} cached)")
                    continue
                r = run_one(system, cfg, student, world, reports, verifier, seed, real_judge)
                if system in REAL_JUDGE:
                    r |= dict(judge_model=cfg.copies.judge_model, judge_new_calls=real_judge.calls - calls0,
                              judge_unparsed_total=real_judge.unparsed)
                row = dict(system=system, attack=attack, seed=seed, poison_rate=a.poison_rate,
                           model=cfg.student.model_name, n_reports=len(reports), n_lie_reports=n_lie,
                           copies={k: v for k, v in vars(cfg.copies).items()}, **r)
                with results.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(row, default=str) + "\n")
                fmt = lambda v: "  -  " if v is None else f"{v:.3f}"
                print(f"  {system:<15} learn_new={fmt(r['learn_new'])} updates={fmt(r['learn_updates'])} "
                      f"lies_absorbed={fmt(r['poison_absorbed'])} accepted_true={fmt(r['accepted_true_share'])} "
                      f"accepted_lies={fmt(r['accepted_lie_share'])} ({r['minutes']:.1f} min)")
    print(f"\nresults -> {results}")


if __name__ == "__main__":
    main()
