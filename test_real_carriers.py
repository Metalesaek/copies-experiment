"""Checks for real_carriers.py on synthetic articles (no CC-News, no GPU, no spaCy needed).

  python test_real_carriers.py

Synthetic carriers mimic the cases that matter: verbatim reprints, light edits, rewrites with the same
facts, rewrites with invented facts, and independent reports of one event (shared names, own quotes).
"""
from __future__ import annotations

import json
import random
import tempfile
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import novelty_test
import real_carriers as rc

novelty_test.spacy_facts = lambda texts: [novelty_test.facts(t) for t in texts]   # rule-based stand-in

WORDS = ("council budget river bridge school vote mayor police harbour market trade storm road court "
         "hospital train airport museum festival farm").split()


def article(rng, names, n=120):
    w = [rng.choice(WORDS) for _ in range(n)]
    for i, name in enumerate(names):
        w.insert(10 + 15 * i, name)
    return "Headline about " + names[0] + "\n" + " ".join(w)


def light_edit(text):
    lines = text.split("\n")
    body = lines[1].split()
    return lines[0] + "\n" + " ".join(body[3:int(len(body) * 0.8)])


def reword(rng, text, names):
    return article(rng, names)            # new words, same names


def build_file(path: Path, seed=0):
    rng = random.Random(seed)
    recs = []
    ev = lambda i: [f"Alpha{i} Bravo", f"Charlie{i} Delta", f"Echo{i}"]
    for i in range(60):                    # real chains: origin + verbatim/light-edited reprints
        names = ev(i)
        o = article(rng, names)
        size = 2 + i % 12
        recs.append(dict(kind="chain", id=f"c{i}", texts=[o] + [o if k % 2 else light_edit(o) for k in range(size - 1)]))
    for i in range(60, 120):
        recs.append(dict(kind="single", id=f"s{i}", texts=[article(rng, ev(i))]))
    for i in range(120, 140):              # independent pair: same event names, own reporting (own quotes, names)
        a = article(rng, ev(i) + [f"Foxtrot{i} Golf", f"Hotel{i} India"])
        b = article(rng, ev(i)[:1] + [f"Juliet{i} Kilo", f"Lima{i} Mike", f"November{i} Oscar"])
        recs.append(dict(kind="pair", id=f"p{i}", texts=[a], texts_b=[b]))
    for i in range(140, 150):
        names = ev(i)
        o = article(rng, names)
        recs.append(dict(kind="net_paraphrase", id=f"n{i}", texts=[o] + [reword(rng, o, names) for _ in range(10)]))
        recs.append(dict(kind="net_adaptive", id=f"m{i}",
                         texts=[o] + [reword(rng, o, names + [f"Invented{i}x{k} Person", f"Made{i}x{k} Up", f"Fake{i}x{k} Org"])
                                      for k in range(10)]))
    with path.open("w") as f:
        for r in recs:
            r["facts"] = [sorted(novelty_test.facts(t)) for t in r["texts"]]
            if "texts_b" in r:
                r["facts_b"] = [sorted(novelty_test.facts(t)) for t in r["texts_b"]]
            f.write(json.dumps(r) + "\n")


@dataclass(frozen=True)
class Claim:
    uid: int
    target: str
    is_true: bool
    sentence: str
    paraphrases: tuple


def claim(uid, true):
    return Claim(uid, f"T{uid}", true, f"Person{uid} Zulu works in Paris{uid}.",
                 (f"Where does Person{uid} Zulu work? In", f"Person{uid} Zulu is employed in"))


def config(carrier_file, **kw):
    C = SimpleNamespace(truth_chains=[[1, 0.5], [2, 0.3], [3, 0.2]], attack_copies=10, collusion_chains=2,
                        horizon_days=30, chain_spread_days=3, copy_spread_days=1, carriers="real",
                        carrier_file=str(carrier_file), detector="text+novelty",
                        jaccard_threshold=0.6, novelty_threshold=0.4)
    for k, v in kw.items():
        setattr(C, k, v)
    return C


def run(C, attack, seed=10):
    from copies_world import build_reports
    rc._POOL = None
    world = SimpleNamespace(new=[claim(i, True) for i in range(40)], updates=[], poison_fict=[claim(100 + i, False) for i in range(20)],
                            poison_real=[])
    sample = lambda rng: rng.choice([1, 1, 1, 2, 3, 5])
    reps = build_reports(world, C, sample, attack, seed)
    return reps, dict(rc.DETECTOR_STATS)


def main():
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "carriers.jsonl"
        build_file(f)
        C = config(f)
        lie_chains = {}
        for attack in ("copy", "paraphrase", "adaptive", "collusion"):
            reps, st = run(C, attack)
            print(f"{attack:<11} {len(reps)} reports | {rc.stats_line(st)}")
            assert all(r.article is not None and r.text in r.article.body for r in reps), "claim not inserted"
            assert reps == sorted(reps, key=lambda r: r.time), "stream not in time order"
            lies = [r for r in reps if not r.claim.is_true]
            lie_chains[attack] = sum(len({r.seen_chain for r in lies if r.claim.uid == u}) for u in {r.claim.uid for r in lies}) \
                / len({r.claim.uid for r in lies})
        print("independent chains per lie, as the detector sees them:", {k: round(v, 2) for k, v in lie_chains.items()})
        assert lie_chains["copy"] == 1.0, "verbatim/light-edit copies must all be linked"
        assert lie_chains["paraphrase"] < 1.5, "rewrites with the same facts should mostly be linked by novelty"
        assert lie_chains["collusion"] == 2.0, "independent reports must not be merged"
        # text only: rewrites escape
        reps, st = run(config(f, detector="text"), "paraphrase")
        n = sum(len({r.seen_chain for r in reps if r.claim.uid == u and not r.claim.is_true}) for u in range(100, 120)) / 20
        print(f"paraphrase, text detector only: {n:.2f} chains per lie")
        assert n > 5, "text detector should miss reworded copies"
        # determinism
        a, _ = run(C, "copy")
        b, _ = run(C, "copy")
        assert [(r.chain, r.seen_chain, r.time) for r in a] == [(r.chain, r.seen_chain, r.time) for r in b]
        # simulated path unchanged
        from copies_world import build_reports
        Cs = config(f, carriers="simulated", detector_recall=0.95, paraphrase_evasion=0.7)
        world = SimpleNamespace(new=[claim(i, True) for i in range(5)], updates=[], poison_fict=[claim(100, False)], poison_real=[])
        sim = build_reports(world, Cs, lambda rng: 2, "copy", 10)
        assert all(r.article is None for r in sim)
    print("all checks passed")


if __name__ == "__main__":
    main()
