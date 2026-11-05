"""Re-analysis of the judge experiment (Section 4) for the second review. No model calls.

  python reanalyse_judges.py        # reads results/judge_copies_v2/verdicts.csv

1. Three outcomes instead of two: True / False / abstain (Unsure, or no verdict word at all), with
   95% Wilson intervals, per judge x condition x kind.
2. Claim-level paired tests (exact McNemar) for the key contrasts on the SAME 80 claims:
   1 report -> 3 copies, 3 copies -> 3 independent, 3 copies -> 3 copies + note, 3 copies -> filler.
   Holm correction over all tests reported.
Writes results/judge_reanalysis.md.
"""
from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
JUDGES = {"llama3.2": "Llama 3.2", "phi4": "phi4", "gemini:gemini-2.5-flash": "Gemini Flash",
          "gemini:gemini-2.5-pro": "Gemini Pro"}
KINDS = {"poison_fict": "lies, invented people", "poison_real": "lies, known facts",
         "new": "truths, invented people", "update": "updates, known facts"}


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p, d = k / n, 1 + z * z / n
    c, h = p + z * z / (2 * n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p-value from the discordant counts b (0->1) and c (1->0)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        adj[i] = run
    return adj


def main():
    d = pd.read_csv(HERE / "results" / "judge_copies_v2" / "verdicts.csv")
    d["outcome"] = d.verdict.fillna("none").map({"True": "true", "False": "false", "Unsure": "abstain",
                                                  "none": "abstain"})
    d["no_word"] = d.verdict.isna()
    md = ["# Judge experiment: three outcomes, paired tests", ""]

    # 1. three outcomes
    md += ["## Share True / False / abstain (abstain = Unsure or no verdict word), 95% Wilson interval for True", ""]
    for kind, kname in KINDS.items():
        md += [f"### {kname}", "", "| judge | condition | n | True [95% CI] | False | abstain | of which no word |",
               "|---|---|---|---|---|---|---|"]
        for j, jn in JUDGES.items():
            for cond, g in d[(d.judge == j) & (d.kind == kind)].groupby("condition", sort=False):
                n, t = len(g), (g.outcome == "true").sum()
                lo, hi = wilson(t, n)
                md.append(f"| {jn} | {cond} | {n} | {t / n:.2f} [{lo:.2f}, {hi:.2f}] | "
                          f"{(g.outcome == 'false').mean():.2f} | {(g.outcome == 'abstain').mean():.2f} | "
                          f"{g.no_word.sum()} |")
        md.append("")

    # 2. paired tests on the same claims
    contrasts = [("copies1", "copies3"), ("copies3", "indep3"), ("copies3", "labelled3"),
                 ("copies3", "filler3"), ("copies3", "copies10"), ("copies10", "labelled10"),
                 # probes (run with judge_copies.py --probes)
                 ("copies3", "sameoutlet3"), ("copies1", "sameoutlet3"), ("copies3", "copies3_falseindep"),
                 ("indep3", "paraphrase3_note"), ("copies3", "copies3_table"), ("labelled3", "copies3_table"),
                 ("copies3", "copies3_known"), ("indep3", "indep3_known")]
    rows = []
    for kind in ("poison_fict", "poison_real"):
        for j, jn in JUDGES.items():
            sub = d[(d.judge == j) & (d.kind == kind)]
            acc = sub.assign(acc=sub.outcome == "true").pivot_table(index=["uid", "target"], columns="condition",
                                                                       values="acc", aggfunc="first")
            for a, b in contrasts:
                if a not in acc or b not in acc:
                    continue
                x = acc[[a, b]].dropna()
                up, down = int((~x[a] & x[b]).sum()), int((x[a] & ~x[b]).sum())
                rows.append(dict(kind=KINDS[kind], judge=jn, contrast=f"{a} -> {b}", n=len(x),
                                 change=x[b].mean() - x[a].mean(), up=up, down=down, p=mcnemar_exact(up, down)))
    t = pd.DataFrame(rows)
    t["p_holm"] = holm(t.p.tolist())
    md += ["## Paired tests on the same claims (exact McNemar; Holm-adjusted over all rows)", "",
           "| lies | judge | contrast | n | change in share True | claims flipped to True | flipped to not-True | p | p (Holm) |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in t.itertuples():
        md.append(f"| {r.kind} | {r.judge} | {r.contrast} | {r.n} | {r.change:+.2f} | {r.up} | {r.down} | "
                  f"{r.p:.2g} | {r.p_holm:.2g} |")
    md.append("")

    out = HERE / "results" / "judge_reanalysis.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
