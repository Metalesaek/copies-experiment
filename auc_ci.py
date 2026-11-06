"""95% bootstrap intervals for the AUCs of results/baselines.md (review: "AUC on 11 negatives needs uncertainty").
Reads results/baseline_scores.csv (scores only, no text). Stratified bootstrap, 2,000 resamples, seed 0:
positives and negatives are resampled separately; the same resamples are used for every detector, so the
interval of a difference between two detectors is paired.

  python auc_ci.py           # seconds

Writes results/auc_ci.md.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
B, OURS = 2000, "ours_1_minus_novelty"


def auc(pos: np.ndarray, neg: np.ndarray) -> float:
    """P(copy score of a positive > that of a negative), ties count one half (scores: higher = copy)."""
    d = pos[:, None] - neg[None, :]
    return float((d > 0).mean() + 0.5 * (d == 0).mean())


def main():
    r = pd.read_csv(HERE / "results" / "baseline_scores.csv")
    scores = [c for c in r.columns if c not in ("url", "kind", "confirmed")]
    sets = {"rewrites vs 11 confirmed": (r.kind == "rewrite", r.confirmed.astype(bool)),
            "adaptive vs 11 confirmed": (r.kind == "adaptive", r.confirmed.astype(bool)),
            "rewrites vs 100 held-out independent": (r.kind == "rewrite", r.kind == "held_independent"),
            "adaptive vs 100 held-out independent": (r.kind == "adaptive", r.kind == "held_independent"),
            "same-source vs 100 held-out independent": (r.kind == "held_same_source", r.kind == "held_independent")}
    md = ["# AUC with 95% bootstrap intervals", "",
          f"Stratified bootstrap ({B} resamples, seed 0), the same resamples for every detector. "
          f"Difference = detector minus ours ({OURS}); paired interval.", ""]
    for name, (pm, nm) in sets.items():
        P, N = r.loc[pm, scores].to_numpy(float), r.loc[nm, scores].to_numpy(float)
        rng = np.random.default_rng(0)
        boot = np.empty((B, len(scores)))
        for b in range(B):
            ip, ineg = rng.integers(0, len(P), len(P)), rng.integers(0, len(N), len(N))
            boot[b] = [auc(P[ip, k], N[ineg, k]) for k in range(len(scores))]
        point = np.array([auc(P[:, k], N[:, k]) for k in range(len(scores))])
        o = scores.index(OURS)
        md += [f"## {name} ({len(P)} positives, {len(N)} negatives)", "",
               "| detector | AUC [95% CI] | difference to ours [95% CI] |", "|---|---|---|"]
        for k, c in enumerate(scores):
            lo, hi = np.percentile(boot[:, k], [2.5, 97.5])
            dl, dh = np.percentile(boot[:, k] - boot[:, o], [2.5, 97.5])
            diff = "-" if k == o else f"{point[k] - point[o]:+.2f} [{dl:+.2f}, {dh:+.2f}]"
            md.append(f"| {c} | {point[k]:.2f} [{lo:.2f}, {hi:.2f}] | {diff} |")
        md.append("")
    (HERE / "results" / "auc_ci.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
