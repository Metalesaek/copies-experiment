"""Baselines for recognising rewritten copies (review W5): is entity-and-quotation novelty better than
standard similarity measures?  CPU, ~20-40 min (first run downloads two small embedding models).

  uv pip install scikit-learn sentence-transformers
  python baselines.py

Same pairs as novelty_test.py (results/novelty_pairs.csv): each of 200 originals against
  its phi4 rewrite and its adaptive rewrite (phi4+invented)         -> copies (positives)
  its automatically selected comparison report (167)                -> non-copies (negatives)
  the 11 comparison reports confirmed independent by hand (data/labels_independent_check.csv)
Every detector gives a COPY SCORE (higher = more likely a copy of the original):
  5-gram Jaccard (the text detector), TF-IDF cosine, sentence embeddings (all-MiniLM-L6-v2,
  all-mpnet-base-v2), a cross-encoder for semantic similarity (cross-encoder/stsb-roberta-base),
  entity overlap (share of the report's spaCy entities found in the original), quotation overlap,
  1 - entity-and-quotation novelty (ours), and a rank average of ours with the best embedding.
Reported: ROC-AUC against all comparison reports and against the 11 confirmed ones, and recall at the
threshold that flags 5% of the comparison reports (no tuning on the rewrites).
Writes results/baselines.md and results/baseline_scores.csv.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from check_copies import boilerplate_lines, load, strip
from measure_detector import jaccard
from novelty_test import QUOTE, auc, novelty, spacy_facts

HERE = Path(__file__).resolve().parent
N_CHARS = 2500


def quotes(t: str) -> set[str]:
    return {q.lower()[:40] for q in QUOTE.findall(t[:N_CHARS])}


def overlap(orig: set[str], rep: set[str]) -> float:
    return len(rep & orig) / len(rep) if rep else 0.0


def main():
    pairs = pd.read_csv(HERE / "results" / "novelty_pairs.csv")
    confirmed = pd.read_csv(HERE / "data" / "labels_independent_check.csv")
    confirmed = set(confirmed.loc[confirmed.label == "independent", "indep_url"])
    rewrites = {}
    for line in (HERE / "data" / "reworded_articles.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        rewrites[(r["rewriter"], r["url"])] = r["reworded"]

    df = load(None, 0)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=0).text)
    need = set(pairs.url) | set(pairs.indep_url.dropna())
    text = {u: strip(t, lines)[:N_CHARS] for u, t in zip(df.url, df.text) if u in need}

    rows = []  # one row per (original, report)
    for p in pairs.itertuples():
        if p.url not in text:
            continue
        for kind, rep in (("rewrite", rewrites.get(("phi4", p.url))), ("adaptive", rewrites.get(("phi4+invented", p.url))),
                          ("comparison", text.get(p.indep_url) if isinstance(p.indep_url, str) else None)):
            if rep:
                rows.append(dict(url=p.url, kind=kind, confirmed=kind == "comparison" and p.indep_url in confirmed,
                                 orig=text[p.url], rep=rep[:N_CHARS]))
    r = pd.DataFrame(rows)
    print(r.kind.value_counts().to_dict(), "confirmed:", int(r.confirmed.sum()))

    r["jaccard_5gram"] = [jaccard(a, b) for a, b in zip(r.orig, r.rep)]
    from sklearn.feature_extraction.text import TfidfVectorizer
    tf = TfidfVectorizer(sublinear_tf=True, stop_words="english").fit(pd.concat([r.orig, r.rep]))
    A, B = tf.transform(r.orig), tf.transform(r.rep)
    r["tfidf_cosine"] = np.asarray(A.multiply(B).sum(1)).ravel()  # rows are L2-normalised
    from sentence_transformers import CrossEncoder, SentenceTransformer
    for name in ("all-MiniLM-L6-v2", "all-mpnet-base-v2"):
        m = SentenceTransformer(name)
        ea = m.encode(r.orig.tolist(), batch_size=16, normalize_embeddings=True, show_progress_bar=True)
        eb = m.encode(r.rep.tolist(), batch_size=16, normalize_embeddings=True, show_progress_bar=True)
        r[f"emb_{name.split('-')[1].lower()}"] = (ea * eb).sum(1)
    ce = CrossEncoder("cross-encoder/stsb-roberta-base")
    r["cross_encoder"] = ce.predict(list(zip(r.orig.tolist(), r.rep.tolist())), batch_size=8, show_progress_bar=True)
    so, sr = spacy_facts(r.orig.tolist()), spacy_facts(r.rep.tolist())
    ents = lambda s: {x for x in s if not x.startswith("q:")}
    r["entity_overlap"] = [overlap(ents(a), ents(b)) for a, b in zip(so, sr)]
    r["quote_overlap"] = [overlap(quotes(a), quotes(b)) for a, b in zip(r.orig, r.rep)]
    r["ours_1_minus_novelty"] = [1 - novelty(a, b) for a, b in zip(so, sr)]
    best_emb = max(("emb_minilm", "emb_mpnet"),
                   key=lambda c: auc(-r.loc[r.kind == "rewrite", c], -r.loc[r.kind == "comparison", c]))
    r["hybrid_ours_plus_" + best_emb] = (r.ours_1_minus_novelty.rank(pct=True) + r[best_emb].rank(pct=True)) / 2

    scores = [c for c in r.columns if c not in ("url", "kind", "confirmed", "orig", "rep")]
    comp, conf = r[r.kind == "comparison"], r[r.confirmed]
    md = ["# Baselines: recognising rewritten copies", "",
          f"Positives: {int((r.kind == 'rewrite').sum())} phi4 rewrites and {int((r.kind == 'adaptive').sum())} adaptive "
          f"rewrites of their original. Negatives: {len(comp)} automatically selected comparison reports of the same "
          f"event, of which {len(conf)} are confirmed independent by hand. Copy score: higher = more likely a copy. "
          "AUC = P(copy scores higher than non-copy). Recall at 5% FA: threshold set so that 5% of the comparison "
          "reports are flagged.", "",
          "| detector | AUC rewrite vs all | AUC rewrite vs confirmed | AUC adaptive vs all | AUC adaptive vs confirmed "
          "| recall at 5% FA, rewrite | recall at 5% FA, adaptive |", "|---|---|---|---|---|---|---|"]
    for c in scores:
        thr = comp[c].quantile(0.95)
        row = []
        for kind in ("rewrite", "adaptive"):
            pos = r.loc[r.kind == kind, c]
            row += [auc(-pos, -comp[c]), auc(-pos, -conf[c]) if len(conf) else float("nan")]
        rec = [(r.loc[r.kind == k, c] > thr).mean() for k in ("rewrite", "adaptive")]
        md.append(f"| {c} | {row[0]:.2f} | {row[1]:.2f} | {row[2]:.2f} | {row[3]:.2f} | {rec[0]:.2f} | {rec[1]:.2f} |")
    md += ["", "Medians of each score:", "",
           r.groupby(r.kind.where(~r.confirmed, "comparison (confirmed)"))[scores].median().round(2).T.to_markdown()]
    (HERE / "results" / "baselines.md").write_text("\n".join(md), encoding="utf-8")
    r.drop(columns=["orig", "rep"]).to_csv(HERE / "results" / "baseline_scores.csv", index=False)
    print("\n".join(md))


if __name__ == "__main__":
    main()
