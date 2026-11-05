"""A larger, hand-labelled test set of same-event report pairs (review W2).  CPU, ~30-60 min.

  python make_independent_set.py            # writes the two blind labelling sheets
  python make_independent_set.py --score    # after labelling: agreement + detector results on the set

Candidates (from the same 200,000-article sample, seed 0), chosen to be about the SAME event:
  two different outlets, published at most one day apart, titles similar (TF-IDF cosine >= 0.35),
  sharing at least 3 named people, organisations, places or events (spaCy), and NOT a textual copy
  (5-gram Jaccard < 0.2). 250 pairs are drawn at random, each article used once. The selection uses
  no score of the new-information test, so the set is a held-out test of its fixed threshold (0.4).
Sheets: data/indep_set_author1.xlsx, data/indep_set_author2.xlsx (identical, both blind: no detector
scores; label each pair independently, do not discuss before both are done) and data/indep_set_key.csv.
Labels: independent / same_source / different_event / unclear.
"""
from __future__ import annotations

import argparse
import random
import re
from pathlib import Path

import numpy as np
import pandas as pd

from check_copies import boilerplate_lines, load, strip
from measure_detector import jaccard

HERE = Path(__file__).resolve().parent
D = HERE / "data"
N_PAIRS = 250
ENT = {"PERSON", "ORG", "GPE", "EVENT", "FAC", "NORP"}
README = [
    "Are these two articles INDEPENDENT reports of the same event, or does one come from the same source as the other?",
    "Read both texts (first 1,500 characters; open the URLs if needed). Choose one label per pair in column 'label':",
    "  independent      = same event, but each article has its own reporting: own quotes, own sources, own details",
    "  same_source      = same event, and one is based on the other, or both on one wire story, press release,",
    "                     statement, interview or broadcast (look for agency credits, identical quotes, same structure)",
    "  different_event  = the articles are about different events (they only share names, places or a topic)",
    "  unclear          = you cannot decide from the text",
    "Optional: a short note in column 'note'. Label alone; do not look at the other author's sheet before both are done.",
    "No detector scores are shown. The pairs are in random order.",
]


def candidates(df: pd.DataFrame, lines) -> pd.DataFrame:
    from sklearn.feature_extraction.text import TfidfVectorizer
    df = df[df.day.notna()].reset_index(drop=True)
    tf = TfidfVectorizer(stop_words="english", min_df=2, sublinear_tf=True)
    X = tf.fit_transform(df.title.fillna(""))
    days = sorted(df.day.unique())
    idx = {d: np.where(df.day.values == d)[0] for d in days}
    pairs = []
    for d in days:
        a = idx[d]
        b = np.concatenate([idx[d]] + [idx[e] for e in (d + pd.Timedelta(days=1),) if e in idx])
        S = (X[a] @ X[b].T).tocoo()
        for i, j, s in zip(S.row, S.col, S.data):
            ai, bj = a[i], b[j]
            if s >= 0.35 and ai < bj and df.domain.iat[ai] != df.domain.iat[bj]:
                pairs.append((ai, bj, s))
    print(f"{len(pairs)} title-similar cross-outlet pairs")
    keep = []
    for ai, bj, s in pairs:
        ta, tb = strip(df.text.iat[ai], lines), strip(df.text.iat[bj], lines)
        if jaccard(ta, tb) < 0.2:
            keep.append((ai, bj, s))
    print(f"{len(keep)} of them not textual copies")
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer", "tagger", "attribute_ruler"])
    arts = sorted({x for p in keep for x in p[:2]})
    ents = {}
    for i, doc in zip(arts, nlp.pipe((strip(df.text.iat[i], lines)[:2500] for i in arts), batch_size=64)):
        ents[i] = {re.sub(r"\s+", " ", e.text.lower()).strip() for e in doc.ents if e.label_ in ENT}
    rows = [dict(a=ai, b=bj, title_sim=s, shared_entities=len(ents[ai] & ents[bj])) for ai, bj, s in keep]
    c = pd.DataFrame(rows)
    c = c[c.shared_entities >= 3]
    print(f"{len(c)} candidates share at least 3 named entities")
    return df, c


def build():
    df = load(200_000, 0)
    lines = boilerplate_lines(df.text)
    df["day"] = pd.to_datetime(df.date, errors="coerce").dt.normalize()
    df, c = candidates(df, lines)
    rng = random.Random(0)
    order = list(c.itertuples())
    rng.shuffle(order)
    used, pick = set(), []
    for r in order:
        if r.a in used or r.b in used:
            continue
        used |= {r.a, r.b}
        pick.append(r)
        if len(pick) == N_PAIRS:
            break
    key, sheet = [], []
    for k, r in enumerate(pick, 1):
        a, b = (r.a, r.b) if rng.random() < 0.5 else (r.b, r.a)  # random order inside the pair
        key.append(dict(item=k, url_a=df.url.iat[a], url_b=df.url.iat[b], day_a=df.day.iat[a], day_b=df.day.iat[b],
                        domain_a=df.domain.iat[a],
                        domain_b=df.domain.iat[b], title_sim=round(r.title_sim, 3), shared_entities=r.shared_entities))
        sheet.append(dict(item=k, title_a=df.title.iat[a], date_a=str(df.date.iat[a])[:10], domain_a=df.domain.iat[a],
                          text_a=strip(df.text.iat[a], lines)[:1500], url_a=df.url.iat[a],
                          title_b=df.title.iat[b], date_b=str(df.date.iat[b])[:10], domain_b=df.domain.iat[b],
                          text_b=strip(df.text.iat[b], lines)[:1500], url_b=df.url.iat[b], label="", note=""))
    pd.DataFrame(key).to_csv(D / "indep_set_key.csv", index=False)
    from openpyxl.worksheet.datavalidation import DataValidation
    for who in ("author1", "author2"):
        out = D / f"indep_set_{who}.xlsx"
        with pd.ExcelWriter(out, engine="openpyxl") as w:
            pd.DataFrame({"Read me": README}).to_excel(w, sheet_name="Read me", index=False)
            pd.DataFrame(sheet).to_excel(w, sheet_name="Pairs", index=False)
            ws = w.sheets["Pairs"]
            dv = DataValidation(type="list", formula1='"independent,same_source,different_event,unclear"', allow_blank=True)
            ws.add_data_validation(dv)
            col = pd.DataFrame(sheet).columns.get_loc("label") + 1
            letter = ws.cell(row=1, column=col).column_letter
            dv.add(f"{letter}2:{letter}{len(sheet) + 1}")
            for name, width in (("text_a", 80), ("text_b", 80), ("title_a", 40), ("title_b", 40)):
                ws.column_dimensions[ws.cell(row=1, column=pd.DataFrame(sheet).columns.get_loc(name) + 1).column_letter].width = width
        print(f"wrote {out}")
    print(f"{len(sheet)} pairs; key: data/indep_set_key.csv")


def score():
    """Agreement between the two authors, then the new-information test on the agreed pairs."""
    from compute_iaa import cohen_kappa_score
    key = pd.read_csv(D / "indep_set_key.csv").set_index("item")
    if (D / "indep_set_author1.xlsx").exists():  # local sheets (with article text, not published)
        lab = {w: pd.read_excel(D / f"indep_set_{w}.xlsx", sheet_name="Pairs").set_index("item")["label"].astype(str).str.strip()
               for w in ("author1", "author2")}
    else:  # public, text-free labels (make_release_labels.py)
        pub = pd.read_csv(D / "labels_indep_set.csv").set_index("item")
        lab = {w: pub[f"label_{w}"].astype(str).str.strip() for w in ("author1", "author2")}
    both = pd.DataFrame(lab).dropna()
    both = both[(both.author1 != "nan") & (both.author2 != "nan")]
    kappa = cohen_kappa_score(both.author1.tolist(), both.author2.tolist())
    agree = both[both.author1 == both.author2]
    print(f"{len(both)} pairs labelled by both; agreement {len(agree) / len(both):.2f}, kappa {kappa:.2f}")
    print(agree.author1.value_counts().to_dict())
    df = load(200_000, 0)
    lines = boilerplate_lines(df.text)
    text = dict(zip(df.url, df.text))
    from novelty_test import novelty, spacy_facts
    k = key.loc[agree.index]
    fa = spacy_facts([strip(text[u], lines) for u in k.url_a])
    fb = spacy_facts([strip(text[u], lines) for u in k.url_b])
    k = k.assign(label=agree.author1, nov_ab=[novelty(x, y) for x, y in zip(fa, fb)],  # b as the later report
                 nov_ba=[novelty(y, x) for x, y in zip(fa, fb)])
    # the later report is tested against the earlier one; same day: either direction may flag (conservative)
    da, db = pd.to_datetime(k.day_a), pd.to_datetime(k.day_b)
    k["novelty"] = np.where(db > da, k.nov_ab, np.where(da > db, k.nov_ba, k[["nov_ab", "nov_ba"]].min(axis=1)))
    md = ["# Held-out set of same-event pairs, labelled by two authors", "",
          f"{len(both)} pairs labelled by both; raw agreement {len(agree) / len(both):.2f}, Cohen's kappa {kappa:.2f}. "
          "Results on the agreed pairs; threshold 0.4 fixed in advance.", "",
          "| agreed label | pairs | median novelty | flagged as copy (novelty < 0.4) |", "|---|---|---|---|"]
    for l, g in k.groupby("label"):
        md.append(f"| {l} | {len(g)} | {g.novelty.median():.2f} | {(g.novelty < 0.4).mean():.2f} ({int((g.novelty < 0.4).sum())}) |")
    (HERE / "results" / "indep_set.md").write_text("\n".join(md), encoding="utf-8")
    k.drop(columns=["nov_ab", "nov_ba"]).to_csv(HERE / "results" / "indep_set_scores.csv")
    print("\n".join(md))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--score", action="store_true")
    a = ap.parse_args()
    score() if a.score else build()


if __name__ == "__main__":
    main()
