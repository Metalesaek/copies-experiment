"""Feasibility check for "Copies are not confirmations": how often is a news article a near-copy of an
article from ANOTHER outlet?  Public data only (CC-News: ~708k English news articles, 2017-2019, with
outlet domain, date and URL). No GPU; about 20-40 minutes on a laptop (use --limit for a faster run).

  python check_copies.py                   # all articles
  python check_copies.py --limit 200000    # a random subset

Method: MinHash over 5-word shingles of each article's first 2,000 characters, then LSH to find pairs
with estimated Jaccard similarity >= 0.6 (near-copies: wire stories, shared press releases).
Groups of near-copies across different outlets = one "chain" reported many times.

  python check_copies.py --limit 200000 --strip   # boilerplate lines removed first (outputs get _strip)

--strip removes every line that occurs in at least 20 articles of the corpus (login and paywall text,
subscription notices, report templates) before hashing. Control pairs never repeat and need a known date.

Writes
  results/copies_summary.md       share of articles copied across outlets, chain sizes, top outlets
  data/copy_chains.csv            one row per article in a multi-outlet chain (chain id, domain, date, url, title)
  data/annotation_pairs.csv       300 random article pairs for manual annotation of the dependence type
                                  (half near-copies, half same-day pairs on a similar topic but below the threshold)
"""
from __future__ import annotations

import argparse
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
from datasets import load_dataset
from datasketch import MinHash, MinHashLSH

HERE = Path(__file__).resolve().parent
THRESHOLD = 0.6
PERM = 64
WORD = re.compile(r"[a-z0-9]+")


def shingles(text: str, k: int = 5) -> set[bytes]:
    w = WORD.findall(text[:2000].lower())
    return {" ".join(w[i:i + k]).encode() for i in range(max(0, len(w) - k + 1))}


def minhash(text: str) -> MinHash | None:
    s = shingles(text)
    if len(s) < 20:          # too short to judge
        return None
    m = MinHash(num_perm=PERM, seed=1)
    m.update_batch(list(s))
    return m


def load(limit: int | None, seed: int) -> pd.DataFrame:
    for name in ("vblagoje/cc_news", "cc_news"):
        try:
            ds = load_dataset(name, split="train")
            break
        except Exception as e:  # noqa: BLE001 - try the next mirror
            print(f"{name}: {e.__class__.__name__}")
    else:
        raise SystemExit("CC-News could not be loaded")
    df = ds.select_columns(["title", "text", "domain", "date", "url"]).to_pandas()
    df = df[df.text.str.len() > 300].reset_index(drop=True)
    if limit and limit < len(df):
        df = df.sample(limit, random_state=seed).reset_index(drop=True)
    return df


def boilerplate_lines(texts, min_count: int = 20) -> set[str]:
    """Lines that occur in at least min_count articles: site furniture, not reporting."""
    from collections import Counter
    count = Counter()
    for t in texts:
        count.update({ln.strip() for ln in str(t).splitlines() if len(ln.strip()) > 20})
    return {ln for ln, n in count.items() if n >= min_count}


def strip(text: str, lines: set[str]) -> str:
    return "\n".join(ln for ln in str(text).splitlines() if ln.strip() not in lines)


class Union:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def join(self, a, b):
        self.p[self.find(a)] = self.find(b)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--strip", action="store_true", help="remove boilerplate lines before hashing")
    a = ap.parse_args()
    sfx = "_strip" if a.strip else ""
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "data").mkdir(exist_ok=True)

    df = load(a.limit, a.seed)
    print(f"{len(df)} articles from {df.domain.nunique()} outlets")
    if a.strip:
        lines = boilerplate_lines(df.text)
        df["text"] = [strip(t, lines) for t in df.text]
        print(f"removed {len(lines)} boilerplate lines")

    lsh, hashes = MinHashLSH(threshold=THRESHOLD, num_perm=PERM), {}
    for i, t in enumerate(df.text):
        m = minhash(t)
        if m is not None:
            hashes[i] = m
            lsh.insert(i, m)
        if (i + 1) % 50_000 == 0:
            print(f"  hashed {i + 1}/{len(df)}")

    uf, pairs = Union(), []
    dom = df.domain.tolist()
    for i, m in hashes.items():
        for j in lsh.query(m):
            if j > i and dom[i] != dom[j]:          # copies across DIFFERENT outlets only
                uf.join(i, j)
                pairs.append((i, j, m.jaccard(hashes[j])))
    chains = defaultdict(list)
    for i in {x for p in pairs for x in p[:2]}:
        chains[uf.find(i)].append(i)
    chains = {c: m for c, m in chains.items() if len({dom[i] for i in m}) >= 2}
    in_chain = {i: c for c, m in chains.items() for i in m}
    print(f"{len(pairs)} cross-outlet near-copy pairs, {len(chains)} chains")

    # Chains table
    rows = [{"chain": c, "outlets_in_chain": len({dom[i] for i in m}), **df.loc[i, ["domain", "date", "url", "title"]]}
            for c, m in chains.items() for i in m]
    ch = pd.DataFrame(rows).sort_values(["outlets_in_chain", "chain", "date"], ascending=[False, True, True])
    ch.to_csv(HERE / "data" / f"copy_chains{sfx}.csv", index=False)

    # Annotation pairs: 150 near-copies + 150 same-day, different-outlet pairs that share a title word (not copies)
    rng = random.Random(a.seed)
    near = rng.sample(pairs, min(150, len(pairs)))
    by_day = defaultdict(list)
    for i, d in enumerate(df.date.astype(str).str[:10]):
        if d[:2] in ("19", "20"):  # a real date; missing dates ('nan', 'None') would pool unrelated articles
            by_day[d].append(i)
    words = lambda i: {w for w in WORD.findall(str(df.title[i]).lower()) if len(w) > 5}
    far, tries, used = [], 0, set()
    while len(far) < 150 and tries < 200_000:
        tries += 1
        day = rng.choice(list(by_day))
        if len(by_day[day]) < 2:
            continue
        i, j = rng.sample(by_day[day], 2)
        if dom[i] != dom[j] and words(i) & words(j) and in_chain.get(i, -1) != in_chain.get(j, -2) and i in hashes \
                and j in hashes and frozenset((i, j)) not in used:
            used.add(frozenset((i, j)))
            far.append((i, j, hashes[i].jaccard(hashes[j])))
    ann = [{"pair": n, "kind_by_detector": kind, "similarity": round(s, 2),
            "domain_a": dom[i], "date_a": df.date[i], "url_a": df.url[i], "title_a": df.title[i],
            "domain_b": dom[j], "date_b": df.date[j], "url_b": df.url[j], "title_b": df.title[j],
            "dependence_type": ""}  # filled in by hand: wire copy, press release, citation, independent, ...
           for n, (kind, (i, j, s)) in enumerate([("near-copy", p) for p in near] + [("not copy", p) for p in far])]
    pd.DataFrame(ann).sample(frac=1, random_state=a.seed).to_csv(HERE / "data" / f"annotation_pairs{sfx}.csv", index=False)

    # Summary
    n_hashed = len(hashes)
    sizes = Counter(len({dom[i] for i in m}) for m in chains.values())
    top = Counter(dom[i] for m in chains.values() for i in m).most_common(20)
    first = Counter(df.domain[min(m, key=lambda i: str(df.date[i]))] for m in chains.values()).most_common(15)
    bins = [(2, 2), (3, 5), (6, 10), (11, 50), (51, 10**9)]
    md = ["# How often is news copied across outlets? (CC-News)", "",
          f"Articles: {len(df)} ({n_hashed} long enough to compare), outlets: {df.domain.nunique()}.",
          f"Near-copy = estimated Jaccard similarity of 5-word shingles >= {THRESHOLD} (first 2,000 characters), "
          "between different outlets.", "",
          f"- Articles that are a near-copy of an article from another outlet: **{len(in_chain)} "
          f"({len(in_chain) / max(n_hashed, 1):.1%})**",
          f"- Chains (groups of near-copies across outlets): {len(chains)}",
          "", "## Outlets per chain", "", "| outlets | chains |", "|---|---|"]
    md += [f"| {lo}{'' if lo == hi else ('+' if hi > 10**6 else f'-{hi}')} | "
           f"{sum(v for k, v in sizes.items() if lo <= k <= hi)} |" for lo, hi in bins]
    md += ["", "## Outlets most often inside chains", "", "| outlet | articles in chains |", "|---|---|"]
    md += [f"| {d} | {n} |" for d, n in top]
    md += ["", "## Outlets that publish first in a chain (likely origin, e.g. wire services)", "",
           "| outlet | chains it opens |", "|---|---|"]
    md += [f"| {d} | {n} |" for d, n in first]
    (HERE / "results" / f"copies_summary{sfx}.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
