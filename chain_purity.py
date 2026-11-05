"""How clean are the copy chains? (second review: connected components can join articles that are
not copies of each other, A~B and B~C but A!~C).  CPU only, ~20-30 minutes.

  python chain_purity.py            # same sample and settings as check_copies.py --limit 200000
  python chain_purity.py --strip    # boilerplate removed first, as in the precision measurement

1. Threshold sensitivity (pairs verified >= threshold; plus the paper's LSH-candidate setting): share of articles in a cross-outlet chain and number of chains at Jaccard
   thresholds 0.5, 0.6 (used in the paper) and 0.7, from the same MinHash signatures.
2. Chain purity at 0.6: for every chain with 3+ articles, all pairwise similarities (chains above 40
   articles: 780 random pairs). Reported: share of chains whose weakest pair is below 0.6 (joined only
   through others), below 0.3 (probably not copies), and the share of articles that are a direct
   near-copy (>= 0.6) of the chain's earliest article (star clustering around the likely origin).
3. data/chain_purity_examples.csv: 30 random chains whose weakest pair is below 0.3, with titles, for
   manual inspection.
Writes results/chain_purity{_strip}.md.
"""
from __future__ import annotations

import argparse
import itertools
import random
from collections import defaultdict
from pathlib import Path

import pandas as pd
from datasketch import MinHashLSH

from check_copies import PERM, Union, boilerplate_lines, load, minhash, strip

HERE = Path(__file__).resolve().parent
THRESHOLDS = (0.5, 0.6, 0.7)


def chains_at(th, hashes, dom, verify=True):
    lsh = MinHashLSH(threshold=th, num_perm=PERM)
    for i, m in hashes.items():
        lsh.insert(i, m)
    uf, n_pairs = Union(), 0
    for i, m in hashes.items():
        for j in lsh.query(m):
            if j > i and dom[i] != dom[j] and (not verify or m.jaccard(hashes[j]) >= th):
                uf.join(i, j)
                n_pairs += 1
    groups = defaultdict(list)
    for x in list(uf.p):
        groups[uf.find(x)].append(x)
    return {c: g for c, g in groups.items() if len({dom[i] for i in g}) >= 2}, n_pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=200_000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--strip", action="store_true")
    a = ap.parse_args()
    sfx = "_strip" if a.strip else ""
    df = load(a.limit, a.seed)
    if a.strip:
        lines = boilerplate_lines(df.text)
        df["text"] = [strip(t, lines) for t in df.text]
    hashes = {}
    for i, t in enumerate(df.text):
        m = minhash(t)
        if m is not None:
            hashes[i] = m
    dom = df.domain.tolist()
    print(f"{len(hashes)} articles hashed")

    md = [f"# Copy chains: threshold sensitivity and purity{' (boilerplate removed)' if a.strip else ''}", "",
          f"{len(df)} articles, {len(hashes)} long enough to compare.", "",
          "| Jaccard threshold | cross-outlet pairs | chains | articles in chains | share of articles |",
          "|---|---|---|---|---|"]
    ch, n_pairs = chains_at(0.6, hashes, dom, verify=False)
    n_in = sum(len(g) for g in ch.values())
    md.append(f"| 0.6, LSH candidates as in Section 3 | {n_pairs} | {len(ch)} | {n_in} | {n_in / len(hashes):.1%} |")
    print(md[-1])
    at = {}
    for th in THRESHOLDS:
        ch, n_pairs = chains_at(th, hashes, dom)
        n_in = sum(len(g) for g in ch.values())
        at[th] = ch
        md.append(f"| {th} | {n_pairs} | {len(ch)} | {n_in} | {n_in / len(hashes):.1%} |")
        print(md[-1])

    rng = random.Random(a.seed)
    rows, weak = [], []
    date = df.date.astype(str).tolist()
    for c, g in at[0.6].items():
        if len(g) < 3:
            continue
        pairs = list(itertools.combinations(g, 2))
        if len(pairs) > 780:
            pairs = rng.sample(pairs, 780)
        sims = [hashes[i].jaccard(hashes[j]) for i, j in pairs]
        origin = min(g, key=lambda i: date[i])
        direct = sum(hashes[origin].jaccard(hashes[i]) >= 0.6 for i in g if i != origin) / (len(g) - 1)
        rows.append(dict(chain=c, size=len(g), min_sim=min(sims), mean_sim=sum(sims) / len(sims), direct=direct))
        if min(sims) < 0.3:
            weak.append(c)
    r = pd.DataFrame(rows)
    n2 = sum(len(g) == 2 for g in at[0.6].values())
    md += ["", "## Purity of the chains at 0.6", "",
           f"Chains of two articles: {n2} (one direct near-copy pair each, pure by construction). "
           f"Chains of three or more: {len(r)}, holding {int(r['size'].sum())} articles.", "",
           "| measure (chains of 3+) | value |", "|---|---|",
           f"| median of the mean pairwise similarity | {r.mean_sim.median():.2f} |",
           f"| share of chains whose weakest pair is below 0.6 (joined through others) | {(r.min_sim < 0.6).mean():.2f} |",
           f"| share of chains whose weakest pair is below 0.3 | {(r.min_sim < 0.3).mean():.2f} |",
           f"| articles in such chains (below 0.3) | {int(r[r.min_sim < 0.3]['size'].sum())} |",
           f"| articles that are a direct near-copy of the chain's earliest article (mean over chains) | {r.direct.mean():.2f} |",
           f"| same, weighted by chain size | {(r.direct * (r['size'] - 1)).sum() / (r['size'] - 1).sum():.2f} |"]
    ex = []
    for c in rng.sample(weak, min(30, len(weak))):
        for i in sorted(at[0.6][c], key=lambda i: date[i]):
            ex.append(dict(chain=c, size=len(at[0.6][c]), date=date[i], domain=dom[i], title=df.title[i], url=df.url[i]))
    pd.DataFrame(ex).to_csv(HERE / "data" / f"chain_purity_examples{sfx}.csv", index=False)
    md += ["", f"Examples for manual inspection: data/chain_purity_examples{sfx}.csv (30 chains with a pair below 0.3)."]
    (HERE / "results" / f"chain_purity{sfx}.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
