"""Offline check of run_copies.py: tiny random model, invented facts, no downloads (~1-2 min, CPU).

  python test_copies.py

Checks that every system and attack runs and that the bookkeeping is consistent, not that the
method works (the model is random).
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sura_experiment"))

import torch  # noqa: E402

from copies_world import build_reports, chain_size_sampler  # noqa: E402
from run_copies import ATTACKS, SYSTEMS, run_one  # noqa: E402
from sura.config import load_config  # noqa: E402
from sura.data import build_world  # noqa: E402
from sura.student import Student  # noqa: E402
from sura.verifier import NoisyVerifier  # noqa: E402
from tests.test_offline import fake_counterfact, tiny_model, tiny_tokenizer  # noqa: E402


def main():
    cfg = load_config(str(HERE / "configs" / "copies.yaml"), [
        "data.n_fictional_entities=12", "data.suite_size=20", "data.anchor_size=20", "data.heldout_size=20",
        "data.n_updates=10", "train.steps_per_chunk=1", "device=cpu", "dtype=float32", "copies.attack_copies=4"])
    records = fake_counterfact(260)
    tok = tiny_tokenizer(records)
    student = Student(cfg, torch.device("cpu"), torch.float32, model=tiny_model(len(tok)), tokenizer=tok)
    world = build_world(cfg, records, 0.3, seed=0)
    sample_size, sizes = chain_size_sampler(HERE / cfg.copies.chain_file, cfg.copies.corpus_articles)
    assert sizes[1] > 0 and max(sizes) >= 2
    verifier = NoisyVerifier(0.9, 0)
    calls = []

    def fake_judge(msg):  # counts reports like the real judges did: 3+ reports -> true
        calls.append(msg)
        return msg.count("\n") - 3 >= 3
    lies = len(set(world.poison_fict + world.poison_real))
    for attack in ATTACKS:
        reports = build_reports(world, cfg.copies, sample_size, attack, 0)
        assert all(a.time <= b.time for a, b in zip(reports, reports[1:]))
        lie_reports = sum(not r.claim.is_true for r in reports)
        if attack in ("copy", "paraphrase"):
            assert lie_reports == lies * (cfg.copies.attack_copies + 1)
            seen = {(r.claim.uid, r.claim.target): set() for r in reports if not r.claim.is_true}
            for r in reports:
                if not r.claim.is_true:
                    seen[(r.claim.uid, r.claim.target)].add(r.seen_chain)
            avg = sum(map(len, seen.values())) / len(seen)
            print(f"  {attack}: {lie_reports} lie reports, detector sees {avg:.2f} chains per lie")
            if attack == "copy":
                assert avg < 1.5
            else:
                assert avg > 2
        else:
            assert lie_reports == lies * cfg.copies.collusion_chains
        for system in SYSTEMS:
            r = run_one(system, cfg, student, world, reports, verifier, 0, fake_judge)
            assert 0 <= r["accepted_true_share"] <= 1 and 0 <= r["accepted_lie_share"] <= 1
            if system in ("every_report", "first_report"):
                assert r["accepted_true_share"] == 1 and r["accepted_lie_share"] == 1
            if system == "every_report":
                assert r["examples_trained"] == len(reports)
            if system == "chains_k" and attack == "copy":
                # a lie passes only if the detector misses one of its 4 copies: 1 - 0.95^4 = 0.19 expected
                assert r["accepted_lie_share"] < 0.5, r["accepted_lie_share"]
            if system == "chains_k" and attack == "collusion":
                assert r["accepted_lie_share"] == 1
            if system == "judge_all":
                lies_all = r["accepted_lie_share"]
            if system == "judge_chains" and attack == "copy":
                assert r["accepted_lie_share"] < lies_all, (r["accepted_lie_share"], lies_all)
            print(f"    {attack:<10} {system:<15} true={r['accepted_true_share']:.2f} "
                  f"lies={r['accepted_lie_share']:.2f} examples={r['examples_trained']}")
    assert calls and all(m.endswith("Is the claim true?") for m in calls)
    print("example prompt:\n" + max(calls, key=len)[:400])
    print("ok")


if __name__ == "__main__":
    random.seed(0)
    main()
