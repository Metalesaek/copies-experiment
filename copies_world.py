"""Turn the claims of a first-paper World into a stream of news REPORTS with a chain structure.

Every claim (true new fact, legitimate update, lie) is reported by one or more independent
CHAINS; each chain is an origin article plus copies (wire reprints, same-owner sharing,
syndication). Truths: the number of chains comes from `copies.truth_chains`, the copies per chain
from the real chain sizes measured in CC-News (data/copy_chains.csv). Lies follow an attack:

  copy        one origin and `attack_copies` verbatim copies (an amplification network)
  paraphrase  the same, but each copy is reworded, so the copy detector misses it with
              probability `paraphrase_evasion`
  collusion   `collusion_chains` truly independent liars (no copy relation to detect)

The copy detector links a copy to its chain with probability `detector_recall` (verbatim copies;
measured precision of our detector was 0.82 on 150 flagged pairs, recall is set here) and never
merges different chains unless `false_merge` > 0 (the new-information detector wrongly links an
independent report to the first chain with this probability). With `correlated_misses` the detector
misses either all copies of a chain or none (same miss rate per copy). With `miss_profiles` each reworded
chain takes the miss pattern of a real copy network measured by multi_rewrites.py. Each report gets a time; the stream is sorted by time.
"""
from __future__ import annotations

import csv
import json
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from judge_copies import OUTLETS, phrasings


@dataclass(frozen=True)
class Report:
    claim: object          # sura.data.Claim
    chain: str             # true chain id (claim + chain number)
    seen_chain: str        # chain id as the copy detector sees it
    is_copy: bool
    time: float            # days
    outlet: str = ""       # invented outlet name (shown to a real judge)
    text: str = ""         # wording: copies repeat their origin; independent chains and reworded copies differ


def chain_size_sampler(path: Path, corpus_articles: int):
    """Empirical number of outlets per chain, including single articles that nobody copied."""
    sizes = Counter()
    with path.open(encoding="utf-8") as f:
        seen = set()
        for r in csv.DictReader(f):
            if r["chain"] not in seen:
                seen.add(r["chain"])
                sizes[int(r["outlets_in_chain"])] += 1
    in_chains = sum(k * v for k, v in sizes.items())
    sizes[1] += max(corpus_articles - in_chains, 0)
    values, weights = zip(*sorted(sizes.items()))
    return lambda rng: rng.choices(values, weights)[0], dict(sizes)


def build_reports(world, C, sample_size, attack: str, seed: int) -> list[Report]:
    rng = random.Random(seed * 1009 + 17)
    out_rng = random.Random(seed * 1013 + 5)   # separate stream: outlets do not change the report structure
    pick_outlet = lambda: out_rng.choice(OUTLETS)
    merge_rng = random.Random(seed * 1019 + 3)  # separate stream: false merges do not change the reports
    false_merge = getattr(C, "false_merge", 0.0)
    # correlated misses: one draw per chain decides for ALL its copies (same miss rate, all-or-nothing)
    correlated = bool(getattr(C, "correlated_misses", False))
    miss_rng = random.Random(seed * 1021 + 7)  # separate stream: the reports stay the same
    # measured miss patterns of real copy networks (multi_rewrites.py): one profile per reworded chain
    profiles = None
    if getattr(C, "miss_profiles", ""):
        profiles = json.loads(Path(C.miss_profiles).read_text(encoding="utf-8"))[C.miss_profile_key]
    prof_rng = random.Random(seed * 1031 + 11)
    n_chains, w_chains = zip(*[(int(k), float(v)) for k, v in C.truth_chains])
    out = []
    claims = list(dict.fromkeys(world.new + world.updates + world.poison_fict + world.poison_real))
    for c in claims:
        start = rng.uniform(0, C.horizon_days)
        if c.is_true:
            chains = [(sample_size(rng) - 1, False) for _ in range(rng.choices(n_chains, w_chains)[0])]
        elif attack in ("copy", "paraphrase"):
            chains = [(C.attack_copies, attack == "paraphrase")]
        elif attack == "collusion":
            chains = [(0, False) for _ in range(C.collusion_chains)]
        else:
            raise ValueError(f"unknown attack {attack}")
        words = phrasings(c)
        for k, (copies, reworded) in enumerate(chains):
            cid = f"{c.uid}|{c.target}|{k}"
            t0 = start + rng.uniform(0, C.chain_spread_days)
            text = words[k % len(words)]
            # a detector that compares content may wrongly take an independent chain for a copy of the first
            seen = f"{c.uid}|{c.target}|0" if k > 0 and merge_rng.random() < false_merge else cid
            out.append(Report(c, cid, seen, False, t0, pick_outlet(), text))
            p_miss = C.paraphrase_evasion if reworded else 1 - C.detector_recall
            u_chain = miss_rng.random()
            profile = prof_rng.choice(profiles) if (profiles and reworded) else None
            for j in range(copies):
                u = rng.random()  # always drawn, so the report times stay identical
                if profile is not None:
                    miss = bool(profile[j % len(profile)])
                else:
                    miss = (u_chain if correlated else u) < p_miss
                out.append(Report(c, cid, f"{cid}|copy{j}" if miss else seen, True,
                                  t0 + rng.uniform(0, C.copy_spread_days), pick_outlet(),
                                  words[(j + 1) % len(words)] if reworded else text))
    out.sort(key=lambda r: r.time)
    return out
