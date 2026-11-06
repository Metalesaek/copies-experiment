"""Baselines for recognising rewritten copies (review W5): is entity-and-quotation novelty better than
standard similarity measures?  GPU ~20 min, CPU ~1-2 h (first run downloads the models, ~3 GB).

  uv pip install scikit-learn sentence-transformers
  python baselines.py

Same pairs as novelty_test.py (results/novelty_pairs.csv): each of 200 originals against
  its phi4 rewrite and its adaptive rewrite (phi4+invented)         -> copies (positives)
  its automatically selected comparison report (167)                -> non-copies (negatives)
  the 11 comparison reports confirmed independent by hand (data/labels_independent_check.csv)
Every detector gives a COPY SCORE (higher = more likely a copy of the original):
  5-gram Jaccard (the text detector), TF-IDF cosine, sentence embeddings (all-MiniLM-L6-v2,
  all-mpnet-base-v2, BAAI/bge-large-en-v1.5, thenlper/gte-large; online: gemini-embedding-001 if
  GEMINI_API_KEY is set, about $0.15, vectors cached in cache/), cross-encoders
  (cross-encoder/stsb-roberta-base, the reranker BAAI/bge-reranker-large),
  entity overlap (share of the report's spaCy entities found in the original), quotation overlap,
  1 - entity-and-quotation novelty (ours), and a rank average of ours with the best embedding.
Reported: ROC-AUC against all comparison reports and against the 11 confirmed ones, and recall at the
threshold that flags 5% of the comparison reports (no tuning on the rewrites).
Second table: the 250 held-out same-event pairs (data/labels_indep_set.csv), pairs both authors labelled
same_source (natural derivatives, positives) or independent (negatives). Third table: rewrites by
llama3.2 and gemini-2.5-flash (other_rewriters.py) against the held-out independent reports.
Writes results/baselines.md and results/baseline_scores.csv.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

from check_copies import boilerplate_lines, load, strip
from measure_detector import jaccard
from novelty_test import QUOTE, auc, novelty, spacy_facts

HERE = Path(__file__).resolve().parent
N_CHARS = 2500
EMBEDDERS = [("all-MiniLM-L6-v2", "emb_minilm"), ("all-mpnet-base-v2", "emb_mpnet"),
             ("BAAI/bge-large-en-v1.5", "emb_bge_large"), ("thenlper/gte-large", "emb_gte_large")]
GEMINI_EMB, GEMINI_COL = "gemini-embedding-001", "emb_gemini_001"
OTHER_REWRITERS = ["llama3.2", "gemini-2.5-flash"]
CROSS_ENCODERS = [("cross-encoder/stsb-roberta-base", "cross_encoder"), ("BAAI/bge-reranker-large", "reranker_bge_large")]


def quotes(t: str) -> set[str]:
    return {q.lower()[:40] for q in QUOTE.findall(t[:N_CHARS])}


def gemini_embed(texts: list[str]) -> np.ndarray:
    """Unit vectors from the Gemini embedding API (task SEMANTIC_SIMILARITY), cached in cache/ (not published),
    so a rerun costs nothing. ~0.9M tokens for this script: about $0.15."""
    import requests
    key = os.environ["GEMINI_API_KEY"]
    path = HERE / "cache" / f"{GEMINI_EMB}.jsonl"
    path.parent.mkdir(exist_ok=True)
    cache = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            cache[d["h"]] = d["v"]
    h = [hashlib.md5(t.encode("utf-8")).hexdigest() for t in texts]
    todo = list(dict.fromkeys(x for x in h if x not in cache))
    by_h = dict(zip(h, texts))
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_EMB}:batchEmbedContents"
    with path.open("a", encoding="utf-8") as f:
        for k in range(0, len(todo), 50):
            chunk = todo[k:k + 50]
            body = {"requests": [{"model": f"models/{GEMINI_EMB}", "taskType": "SEMANTIC_SIMILARITY",
                                  "content": {"parts": [{"text": by_h[x]}]}} for x in chunk]}
            for attempt in range(7):
                resp = requests.post(url, json=body, timeout=120, headers={"x-goog-api-key": key})
                if resp.status_code in (429, 500, 503):
                    time.sleep(2 ** attempt)
                    continue
                resp.raise_for_status()
                break
            for x, e in zip(chunk, resp.json()["embeddings"]):
                cache[x] = e["values"]
                f.write(json.dumps({"h": x, "v": e["values"]}) + "\n")
            print(f"  Gemini embeddings {min(k + 50, len(todo))}/{len(todo)}")
    v = np.array([cache[x] for x in h], dtype=float)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


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
    held = pd.read_csv(HERE / "data" / "labels_indep_set.csv")  # 250 held-out same-event pairs, both authors
    held = held[(held.label_author1 == held.label_author2) & held.label_author1.isin(["independent", "same_source"])]
    need = set(pairs.url) | set(pairs.indep_url.dropna()) | set(held.url_a) | set(held.url_b)
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
    for p in pairs.itertuples():  # rewrites by other models (other_rewriters.py), if generated
        for name in OTHER_REWRITERS:
            rep = rewrites.get((name, p.url))
            if rep and p.url in text:
                rows.append(dict(url=p.url, kind="rewrite_" + name, confirmed=False, orig=text[p.url], rep=rep[:N_CHARS]))
    for h in held.itertuples():  # earlier report = original, later = report (same day: as listed)
        a, b = (h.url_b, h.url_a) if str(h.day_b) < str(h.day_a) else (h.url_a, h.url_b)
        if a in text and b in text:
            rows.append(dict(url=a, kind="held_" + h.label_author1, confirmed=False, orig=text[a], rep=text[b]))
    r = pd.DataFrame(rows)
    print(r.kind.value_counts().to_dict(), "confirmed:", int(r.confirmed.sum()))

    r["jaccard_5gram"] = [jaccard(a, b) for a, b in zip(r.orig, r.rep)]
    from sklearn.feature_extraction.text import TfidfVectorizer
    tf = TfidfVectorizer(sublinear_tf=True, stop_words="english").fit(pd.concat([r.orig, r.rep]))
    A, B = tf.transform(r.orig), tf.transform(r.rep)
    r["tfidf_cosine"] = np.asarray(A.multiply(B).sum(1)).ravel()  # rows are L2-normalised
    from sentence_transformers import CrossEncoder, SentenceTransformer
    import torch
    for name, col in EMBEDDERS:
        m = SentenceTransformer(name)
        m.max_seq_length = min(m.max_seq_length or 512, 512)
        ea = m.encode(r.orig.tolist(), batch_size=8, normalize_embeddings=True, show_progress_bar=True)
        eb = m.encode(r.rep.tolist(), batch_size=8, normalize_embeddings=True, show_progress_bar=True)
        r[col] = (ea * eb).sum(1)
        del m
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
    if os.environ.get("GEMINI_API_KEY"):  # online embedding model (Google); skipped without a key
        ea, eb = gemini_embed(r.orig.tolist()), gemini_embed(r.rep.tolist())
        r[GEMINI_COL] = (ea * eb).sum(1)
    else:
        print("GEMINI_API_KEY not set: Gemini embedding skipped")
    for name, col in CROSS_ENCODERS:
        ce = CrossEncoder(name, max_length=512)
        r[col] = ce.predict(list(zip(r.orig.tolist(), r.rep.tolist())), batch_size=4, show_progress_bar=True)
        del ce
    so, sr = spacy_facts(r.orig.tolist()), spacy_facts(r.rep.tolist())
    ents = lambda s: {x for x in s if not x.startswith("q:")}
    r["entity_overlap"] = [overlap(ents(a), ents(b)) for a, b in zip(so, sr)]
    r["quote_overlap"] = [overlap(quotes(a), quotes(b)) for a, b in zip(r.orig, r.rep)]
    r["ours_1_minus_novelty"] = [1 - novelty(a, b) for a, b in zip(so, sr)]
    best_emb = max([c for _, c in EMBEDDERS] + ([GEMINI_COL] if GEMINI_COL in r else []),
                   key=lambda c: auc(-r.loc[r.kind == "rewrite", c], -r.loc[r.kind == "comparison", c]))
    r["hybrid_ours_plus_" + best_emb] = (r.ours_1_minus_novelty.rank(pct=True) + r[best_emb].rank(pct=True)) / 2

    scores = [c for c in r.columns if c not in ("url", "kind", "confirmed", "orig", "rep")]
    comp, conf = r[r.kind == "comparison"], r[r.confirmed]
    h_ind, h_src = r[r.kind == "held_independent"], r[r.kind == "held_same_source"]
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
    md += ["", f"## Held-out natural pairs ({len(h_src)} same-source and {len(h_ind)} independent pairs, both "
           "authors agree; data/labels_indep_set.csv)", "",
           "Original = the earlier report. AUC same-source vs independent: can the detector tell a natural derivative "
           "from an independent report of the same event? Rewrites vs held-out independent: the phi4 rewrites as "
           "positives, the held-out independent reports as negatives. Recall at 5% FA: threshold set so that 5% of "
           "the held-out independent reports are flagged.", "",
           "| detector | AUC same-source vs independent | AUC rewrite vs held-out independent "
           "| AUC adaptive vs held-out independent | recall at 5% FA, same-source | recall at 5% FA, rewrite "
           "| recall at 5% FA, adaptive |", "|---|---|---|---|---|---|---|"]
    for c in scores:
        thr = h_ind[c].quantile(0.95)
        a = [auc(-h_src[c], -h_ind[c])] + [auc(-r.loc[r.kind == k, c], -h_ind[c]) for k in ("rewrite", "adaptive")]
        rec = [(x[c] > thr).mean() for x in (h_src, r[r.kind == "rewrite"], r[r.kind == "adaptive"])]
        md.append(f"| {c} | " + " | ".join(f"{v:.2f}" for v in a + rec) + " |")
    others = [k for k in r.kind.unique() if k.startswith("rewrite_")]
    if others:
        md += ["", "## Rewrites by other models (same prompt) vs held-out independent reports", "",
               "| detector | " + " | ".join(f"AUC {k[8:]}" for k in ["rewrite_phi4"] + others) + " |",
               "|---|" + "---|" * (len(others) + 1)]
        for c in scores:
            a = [auc(-r.loc[r.kind == k, c], -h_ind[c]) for k in ["rewrite"] + others]
            md.append(f"| {c} | " + " | ".join(f"{v:.2f}" for v in a) + " |")
    md += ["", "Medians of each score:", "",
           r.groupby(r.kind.where(~r.confirmed, "comparison (confirmed)"))[scores].median().round(2).T.to_markdown()]
    (HERE / "results" / "baselines.md").write_text("\n".join(md), encoding="utf-8")
    r.drop(columns=["orig", "rep"]).to_csv(HERE / "results" / "baseline_scores.csv", index=False)
    print("\n".join(md))


if __name__ == "__main__":
    main()
