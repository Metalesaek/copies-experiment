"""Text window of the copy detector (review: "only the first 2,000 characters"). Same detector as
check_copies.py --strip (5-word shingles, MinHash 64, LSH Jaccard >= 0.6, different outlets, boilerplate
removed) on different parts of each article:

  first 1,000 / 2,000 (the paper) / 4,000 characters, the full text, and "head or tail" (an article is
  linked if its first 2,000 OR its last 2,000 characters are a near-copy; catches wire copy placed below a
  locally written opening).

  python window_ablation.py            # CPU, ~1 h for 200,000 articles

Writes results/window_ablation.md and data/window_new_pairs.csv (URLs and titles only: up to 40 pairs per
window that the 2,000-character detector does not link, for inspection).
"""
from __future__ import annotations

import random
from collections import defaultdict
from pathlib import Path

import pandas as pd
from datasketch import MinHash, MinHashLSH

from check_copies import PERM, THRESHOLD, WORD, Union, boilerplate_lines, load, strip

HERE = Path(__file__).resolve().parent
WINDOWS = {"first 1,000": lambda t: t[:1000], "first 2,000 (paper)": lambda t: t[:2000],
           "first 4,000": lambda t: t[:4000], "full text": lambda t: t,
           "last 2,000": lambda t: t[-2000:]}


def mh(text: str) -> MinHash | None:
    w = WORD.findall(text.lower())
    s = {" ".join(w[i:i + 5]).encode() for i in range(max(0, len(w) - 4))}
    if len(s) < 20:
        return None
    m = MinHash(num_perm=PERM, seed=1)
    m.update_batch(list(s))
    return m


def pairs_for(texts: list[str], dom: list[str], cut) -> tuple[set[tuple[int, int]], int]:
    lsh, hashes = MinHashLSH(threshold=THRESHOLD, num_perm=PERM), {}
    for i, t in enumerate(texts):
        m = mh(cut(t))
        if m is not None:
            hashes[i] = m
            lsh.insert(i, m)
    out = set()
    for i, m in hashes.items():
        for j in lsh.query(m):
            if j > i and dom[i] != dom[j]:
                out.add((i, j))
    return out, len(hashes)


def chains(pairs: set[tuple[int, int]], dom: list[str]) -> dict[int, list[int]]:
    uf = Union()
    for i, j in pairs:
        uf.join(i, j)
    ch = defaultdict(list)
    for i in {x for p in pairs for x in p}:
        ch[uf.find(i)].append(i)
    return {c: m for c, m in ch.items() if len({dom[i] for i in m}) >= 2}


def main():
    df = load(200_000, 0)
    lines = boilerplate_lines(df.text)
    texts = [strip(t, lines) for t in df.text]
    dom = df.domain.tolist()
    n_all = len(texts)
    res = {}
    for name, cut in WINDOWS.items():
        print(f"== {name}")
        p, n_hashed = pairs_for(texts, dom, cut)
        res[name] = (p, n_hashed)
        print(f"   {len(p)} pairs")
    res["head or tail"] = (res["first 2,000 (paper)"][0] | res["last 2,000"][0], None)

    base_p, n_ref = res["first 2,000 (paper)"]
    base = {i for m in chains(base_p, dom).values() for i in m}
    md = ["# Which part of the article the copy detector reads", "",
          f"{n_all} CC-News articles, boilerplate removed, near-copy = 5-gram MinHash Jaccard >= {THRESHOLD} across "
          f"outlets. Share = articles in a chain / the {n_ref} articles long enough for the paper's window "
          "(the denominator of Section 3).", "",
          "| text window | articles in chains | share | chains | pairs | of the paper's chain articles, also linked here "
          "| articles linked here but not by the paper's window |", "|---|---|---|---|---|---|---|"]
    rng, rows = random.Random(0), []
    for name, (p, _) in res.items():
        ch = chains(p, dom)
        arts = {i for m in ch.values() for i in m}
        md.append(f"| {name} | {len(arts)} | {len(arts) / n_ref:.1%} | {len(ch)} | {len(p)} "
                  f"| {len(base & arts) / max(len(base), 1):.2f} | {len(arts - base)} |")
        new = [x for x in p if x not in base_p and not (x[0] in base and x[1] in base)]
        for i, j in rng.sample(new, min(40, len(new))):
            rows.append(dict(window=name, url_a=df.url[i], title_a=df.title[i], url_b=df.url[j], title_b=df.title[j]))
    md += ["", "data/window_new_pairs.csv: up to 40 pairs per window that the paper's window does not link "
           "(URLs and titles, for inspection)."]
    pd.DataFrame(rows).to_csv(HERE / "data" / "window_new_pairs.csv", index=False)
    (HERE / "results" / "window_ablation.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
