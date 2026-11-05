"""Inter-annotator agreement on the 100 blind pairs.

  python compute_iaa.py        # after data/iaa_kader.xlsx and data/iaa_miriam.xlsx are filled in

Cohen's kappa between the two authors, and between each author and the AI-drafted labels
(data/iaa_key.csv), on the nine labels and on the binary question "real dependence or not"
(detector_error, unrelated and independent_same_event count as not dependent).
Writes results/iaa.md.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
NOT_DEPENDENT = {"detector_error", "unrelated", "independent_same_event"}


def cohen_kappa_score(x, y) -> float:
    x, y = list(x), list(y)
    cats = sorted(set(x) | set(y))
    po = sum(a == b for a, b in zip(x, y)) / len(x)
    pe = sum((x.count(c) / len(x)) * (y.count(c) / len(y)) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def labels(who: str) -> pd.Series:
    xlsx = HERE / "data" / f"iaa_{who}.xlsx"
    if xlsx.exists():  # local annotation sheets (with article text, not published)
        df = pd.read_excel(xlsx, sheet_name="Pairs")
        return df.set_index("item")["your_label"].astype(str).str.strip()
    col = {"kader": "label_author1", "miriam": "label_author2"}[who]  # public, text-free labels
    return pd.read_csv(HERE / "data" / "labels_iaa.csv").set_index("item")[col].astype(str).str.strip()


def main():
    k, m = labels("kader"), labels("miriam")
    ai = pd.read_csv(HERE / "data" / "iaa_key.csv").set_index("item")["label"]
    items = [i for i in k.index if k[i] not in ("", "nan") and m[i] not in ("", "nan")]
    print(f"{len(items)} of {len(k)} items labelled by both")
    dep = lambda s: s.map(lambda x: "not" if x in NOT_DEPENDENT else "dependent")
    md = ["# Inter-annotator agreement (100 pairs, blind)", "", f"Items labelled by both: {len(items)}.", "",
          "| pair of annotators | kappa, 9 labels | kappa, dependent or not | raw agreement |", "|---|---|---|---|"]
    for name, x, y in (("Kader - Miriam", k, m), ("Kader - AI draft", k, ai), ("Miriam - AI draft", m, ai)):
        x, y = x[items], y[items]
        md.append(f"| {name} | {cohen_kappa_score(x, y):.2f} | {cohen_kappa_score(dep(x), dep(y)):.2f} | "
                  f"{(x == y).mean():.2f} |")
    labs = sorted(set(k[items]) | set(m[items]))
    cm = pd.crosstab(k[items], m[items]).reindex(index=labs, columns=labs, fill_value=0)
    md += ["", "Confusion (rows Kader, columns Miriam):", "", cm.to_markdown(), ""]
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "iaa.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
