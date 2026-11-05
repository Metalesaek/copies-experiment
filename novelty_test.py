"""Can "new information" recognise rewritten copies that text similarity misses?  (CPU only, ~10-20 min.)

  python novelty_test.py                     # rule-based facts (names, numbers, quotes)
  python novelty_test.py --extractor spacy   # also spaCy named entities (same pairs; measured both ways)

Idea: a rewritten copy changes the words but keeps the facts (names, numbers, quotes) and adds none;
an independent report of the same event adds facts of its own. For each article we extract
  names   capitalised word sequences (lower-cased), numbers, and quotations (first 40 characters)
and compare a report with its original:  new = share of the report's facts that the original lacks.
Compared:
  rewrites     the 200 articles rewritten by phi4 in measure_detector.py (data/reworded_articles.jsonl)
  independent  for each original, the article from ANOTHER outlet, published within one day, that
               shares the most facts with it while its text is different (5-gram Jaccard < 0.2):
               most likely an independent report of the same event
With --extractor spacy the pairs are chosen exactly as before (rule-based facts), and new information is
measured a second time with spaCy entities (PERSON, ORG, GPE, LOC, NORP, FAC, EVENT, PRODUCT, WORK_OF_ART,
LAW, DATE, TIME, MONEY, PERCENT, QUANTITY, CARDINAL) plus the same quotations; setup:
  uv pip install spacy && python -m spacy download en_core_web_sm
A copy is flagged when new < threshold; we report recall on rewrites, the false-alarm rate on
independent reports and the AUC. Writes results/novelty_test.md and results/novelty_pairs.csv.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

from check_copies import boilerplate_lines, load, strip
from measure_detector import jaccard

HERE = Path(__file__).resolve().parent
NAME = re.compile(r"\b[A-Z][a-zA-Z'\-]+(?:\s+(?:of|de|al|van|von)?\s*[A-Z][a-zA-Z'\-]+)*")
NUMBER = re.compile(r"\b\d[\d,.]*\d\b|\b\d\b")
QUOTE = re.compile(r"[\"“]([^\"”]{15,300})[\"”]")
COMMON = {"the", "a", "an", "he", "she", "it", "they", "we", "i", "in", "on", "at", "but", "and", "this", "that",
          "his", "her", "their", "its", "there", "when", "after", "before", "monday", "tuesday", "wednesday",
          "thursday", "friday", "saturday", "sunday", "mr", "mrs", "ms", "dr", "for", "as", "if", "while", "so"}


def facts(text: str) -> set[str]:
    t = text[:2500]
    names = {m.group(0).lower() for m in NAME.finditer(t)}
    names = {n for n in names if n not in COMMON and len(n) > 2}
    nums = {"#" + n.replace(",", "").rstrip(".") for n in NUMBER.findall(t)}
    quotes = {"q:" + q.lower()[:40] for q in QUOTE.findall(t)}
    return names | nums | quotes


SPACY_LABELS = {"PERSON", "ORG", "GPE", "LOC", "NORP", "FAC", "EVENT", "PRODUCT", "WORK_OF_ART", "LAW", "DATE",
                "TIME", "MONEY", "PERCENT", "QUANTITY", "CARDINAL"}


def spacy_facts(texts: list[str]) -> list[set[str]]:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer", "tagger", "attribute_ruler"])
    out = []
    for t, doc in zip(texts, nlp.pipe([t[:2500] for t in texts], batch_size=64)):
        ents = {re.sub(r"[,\s]+", " ", e.text.lower()).strip() for e in doc.ents if e.label_ in SPACY_LABELS}
        ents = {e[4:] if e.startswith("the ") else e for e in ents}
        out.append(ents | {"q:" + q.lower()[:40] for q in QUOTE.findall(t[:2500])})
    return out


def table(md, rew, ind, label):
    md += [f"### {label}", "", f"Median share of new facts: rewrites {pd.Series(rew).median():.2f}, independent reports "
           f"{pd.Series(ind).median():.2f}. AUC: **{auc(rew, ind):.2f}**", "",
           "| flag as copy if new facts below | rewrites caught (recall) | independent reports wrongly flagged |",
           "|---|---|---|"]
    for t in (0.1, 0.2, 0.3, 0.4, 0.5):
        md.append(f"| {t:.1f} | {sum(x < t for x in rew) / len(rew):.2f} | "
                  f"{sum(x < t for x in ind) / max(len(ind), 1):.2f} |")
    md.append("")


def novelty(original: set[str], report: set[str]) -> float:
    return len(report - original) / len(report) if report else 0.0


def auc(pos, neg):
    """P(score of a copy < score of an independent report): copies should have LOWER novelty."""
    return sum((p < n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--extractor", choices=["rules", "spacy"], default="rules")
    ap.add_argument("--rewriter", default="phi4",
                    help="which rewrites to test: phi4 (plain) or phi4+invented (adaptive_rewrites.py)")
    ap.add_argument("--threshold", type=float, default=0.4, help="flag as copy below this share of new facts")
    a = ap.parse_args()
    df = load(None, 0)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=0).text)
    df["day"] = pd.to_datetime(df.date, errors="coerce").dt.date
    by_url = df.set_index("url")
    rewrites = {}
    for line in (HERE / "data" / "reworded_articles.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["rewriter"] == a.rewriter:
            rewrites[r["url"]] = r["reworded"]
    print(f"{len(rewrites)} rewrites")

    by_day = defaultdict(list)
    for i, d in enumerate(df.day):
        if pd.notna(d):
            by_day[d].append(i)
    fact_cache: dict[int, set[str]] = {}

    def facts_of(i: int) -> set[str]:
        if i not in fact_cache:
            fact_cache[i] = facts(strip(df.text.iat[i], lines))
        return fact_cache[i]

    rows = []
    for k, (url, rew) in enumerate(rewrites.items(), 1):
        if url not in by_url.index:
            continue
        o = by_url.loc[url]
        o = o.iloc[0] if isinstance(o, pd.DataFrame) else o
        o_text = strip(o.text, lines)
        fo = facts(o_text)
        row = dict(url=url, domain=o.domain, n_facts=len(fo), o_text=o_text, rew_text=rew,
                   rewrite_new=novelty(fo, facts(rew)), rewrite_jaccard=jaccard(o_text, rew))
        # best independent report of the same event: other outlet, +-1 day, many shared facts, different text
        best, best_shared = None, 3
        if pd.notna(o.day):
            for d in (o.day - pd.Timedelta(days=1), o.day, o.day + pd.Timedelta(days=1)):
                for i in by_day.get(d, []):
                    if df.domain.iat[i] == o.domain:
                        continue
                    shared = len(fo & facts_of(i))
                    if shared > best_shared:
                        t = strip(df.text.iat[i], lines)
                        if jaccard(o_text, t) < 0.2:
                            best, best_shared = i, shared
        if best is not None:
            row |= dict(indep_url=df.url.iat[best], indep_domain=df.domain.iat[best], indep_shared=best_shared,
                        indep_new=novelty(fo, facts_of(best)), ind_text=strip(df.text.iat[best], lines))
        rows.append(row)
        if k % 20 == 0:
            print(f"  {k}/{len(rewrites)}")
    r = pd.DataFrame(rows)
    if a.extractor == "spacy":  # same pairs, facts measured again with spaCy entities
        print("spaCy entities ...")
        so = spacy_facts(r.o_text.tolist())
        sr = spacy_facts(r.rew_text.tolist())
        r["rewrite_new_spacy"] = [novelty(x, y) for x, y in zip(so, sr)]
        has = r.ind_text.notna()
        si = spacy_facts(r.ind_text[has].tolist())
        r.loc[has, "indep_new_spacy"] = [novelty(x, y) for x, y in zip([so[i] for i in r.index[has]], si)]
    r.drop(columns=[c for c in ("o_text", "rew_text", "ind_text") if c in r]).to_csv(
        HERE / "results" / "novelty_pairs.csv", index=False)

    rew = r.rewrite_new.tolist()
    ind = r.indep_new.dropna().tolist()
    md = ["# New information as a copy signal", "",
          f"Rewrites by {a.rewriter}: {len(rew)}; independent reports of the same event found for {len(ind)} originals "
          "(other outlet, within one day, more than 3 shared facts, 5-gram Jaccard < 0.2).", "",
          "| | median share of new facts | median 5-gram Jaccard with the original |", "|---|---|---|",
          f"| rewrite (copy) | {r.rewrite_new.median():.2f} | {r.rewrite_jaccard.median():.2f} |",
          f"| independent report | {pd.Series(ind).median():.2f} | below 0.2 by selection |", "",
          f"AUC (copy has less new information than an independent report): **{auc(rew, ind):.2f}**", "",
          "| flag as copy if new facts below | rewrites caught (recall) | independent reports wrongly flagged |",
          "|---|---|---|"]
    for t in (0.1, 0.2, 0.3, 0.4, 0.5):
        md.append(f"| {t:.1f} | {sum(x < t for x in rew) / len(rew):.2f} | {sum(x < t for x in ind) / max(len(ind), 1):.2f} |")
    if a.extractor == "spacy":
        md += ["", "## Same pairs, facts from spaCy named entities (en_core_web_sm) and quotations", ""]
        table(md, r.rewrite_new_spacy.tolist(), r.indep_new_spacy.dropna().tolist(), "spaCy entities")
        md += [f"Rank correlation of the two measures over all reports: "
               f"{pd.concat([r.rewrite_new, r.indep_new.dropna()]).reset_index(drop=True).corr(pd.concat([r.rewrite_new_spacy, r.indep_new_spacy.dropna()]).reset_index(drop=True), method='spearman'):.2f}."]
    md += ["", "Facts = capitalised names, numbers and quotations (first 2,500 characters, boilerplate removed). "
           "Text similarity alone linked 0% of the rewrites to their original (results/detector_measured.md)."]
    tag = ("" if a.rewriter == "phi4" else "_" + a.rewriter.replace("+", "_")) + ("_spacy" if a.extractor == "spacy" else "")
    (HERE / "results" / f"novelty_test{tag}.md").write_text("\n".join(md), encoding="utf-8")
    # detector parameters for run_copies.py, from the measure used (spaCy if requested)
    rw = r.rewrite_new_spacy if a.extractor == "spacy" else r.rewrite_new
    iw = (r.indep_new_spacy if a.extractor == "spacy" else r.indep_new).dropna()
    params = dict(rewriter=a.rewriter, extractor=a.extractor, threshold=a.threshold,
                  recall_reworded=float((rw < a.threshold).mean()), false_merge=float((iw < a.threshold).mean()))
    (HERE / "results" / f"novelty_params{tag}.json").write_text(json.dumps(params, indent=1), encoding="utf-8")
    print(params)
    print("\n".join(md))


if __name__ == "__main__":
    main()
