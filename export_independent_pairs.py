"""Check the "independent reports" of novelty_test.py (reviewer question: are they really independent,
or a third outlet's rewrite of the same wire story / press release?).

  python export_independent_pairs.py          # CPU, ~3 minutes; needs results/novelty_pairs.csv

1. Automatic flag on ALL pairs: both articles carry the same agency or press-release credit
   (AP, Reuters, AFP, Bloomberg, PR Newswire, Business Wire, GlobeNewswire ...) -> possibly one source.
2. A random sample of 40 pairs (seed 0) with both texts for manual inspection:
   data/independent_check.xlsx, column "label": independent / same_source / unclear.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from check_copies import boilerplate_lines, load, strip

HERE = Path(__file__).resolve().parent
CREDITS = {
    "AP": r"\(AP\)|Associated Press",
    "Reuters": r"\(Reuters\)|Reuters",
    "AFP": r"\bAFP\b|Agence France-Presse",
    "Bloomberg": r"Bloomberg",
    "PR Newswire": r"PR ?Newswire|PRNewswire",
    "Business Wire": r"Business ?Wire",
    "GlobeNewswire": r"Globe ?Newswire",
    "Accesswire": r"ACCESSWIRE|Accesswire",
}


def credits(text: str) -> set[str]:
    t = str(text)[:3000]
    return {k for k, p in CREDITS.items() if re.search(p, t)}


def main():
    pairs = pd.read_csv(HERE / "results" / "novelty_pairs.csv").dropna(subset=["indep_url"])
    df = load(None, 0)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=0).text)
    df = df[df.url.isin(set(pairs.url) | set(pairs.indep_url))].drop_duplicates("url")
    text = {u: strip(t, lines) for u, t in zip(df.url, df.text)}
    title = dict(zip(df.url, df.title)) if "title" in df else {}

    pairs["credits_original"] = pairs.url.map(lambda u: ", ".join(sorted(credits(text.get(u, "")))))
    pairs["credits_independent"] = pairs.indep_url.map(lambda u: ", ".join(sorted(credits(text.get(u, "")))))
    pairs["shared_credit"] = [
        ", ".join(sorted(credits(text.get(a, "")) & credits(text.get(b, ""))))
        for a, b in zip(pairs.url, pairs.indep_url)]
    n, shared = len(pairs), (pairs.shared_credit != "").sum()
    print(f"{n} pairs; both articles share an agency/press-release credit in {shared} ({shared / n:.0%})")

    sample = pairs.sample(min(40, n), random_state=0).copy()
    sample["title_original"] = sample.url.map(title)
    sample["title_independent"] = sample.indep_url.map(title)
    sample["text_original"] = sample.url.map(lambda u: text.get(u, "")[:2000])
    sample["text_independent"] = sample.indep_url.map(lambda u: text.get(u, "")[:2000])
    sample["label"] = ""
    sample["note"] = ""
    cols = ["url", "indep_url", "domain", "indep_domain", "indep_shared", "indep_new_spacy", "shared_credit",
            "title_original", "title_independent", "text_original", "text_independent", "label", "note"]
    out = HERE / "data" / "independent_check.xlsx"
    with pd.ExcelWriter(out) as w:
        pd.DataFrame({"Read me": [
            "Is the second article independent reporting of the same event, or does it come from the same source?",
            "label: independent = own reporting (own quotes, sources or details);",
            "       same_source = same wire story / press release / statement, rewritten by another outlet;",
            "       unclear = cannot tell from the text.",
            f"Sample of 40 out of {n} pairs (seed 0). Automatic check on all pairs: shared credit in {shared}."]}
        ).to_excel(w, sheet_name="Read me", index=False)
        sample[cols].to_excel(w, sheet_name="Pairs", index=False)
        pairs.drop(columns=[c for c in pairs if c.startswith("rewrite")]).to_excel(w, sheet_name="All pairs", index=False)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
