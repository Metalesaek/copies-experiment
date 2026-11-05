"""Measure the copy detector instead of assuming it (review point B).

  python measure_detector.py                                   # rewording with phi4 (Ollama), 200 articles
  python measure_detector.py --rewriter gemini:gemini-2.5-flash --n 200

Same detector as check_copies.py: 5-word shingles of the first 2,000 characters, near-copy if the
Jaccard similarity is at least 0.6 (exact Jaccard here, which the MinHash/LSH step estimates).

1. Precision after boilerplate stripping: the 150 detected pairs labelled in
   data/annotation_pairs_labelled.csv are compared again after removing boilerplate lines; precision =
   share of pairs still detected that are a real dependence (label is not detector_error).
2. Recall: for --n articles (boilerplate removed, at least 1,500 characters) we make
     light     a reprint edited the way client papers edit wire copy: dateline/credit removed,
               first line dropped, last 30% cut
     reworded  a rewrite by an LLM ("in your own words, keep every fact") - a paraphrased copy
   and count how often the detector still links each to its original.
Writes results/detector_measured.md and data/reworded_articles.jsonl (resumable).
"""
from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path

import pandas as pd

from check_copies import WORD, boilerplate_lines, load, strip
from judge_copies import ask

HERE = Path(__file__).resolve().parent
THRESHOLD = 0.6
REWRITE = ("Rewrite the following news article in your own words, the way a different newspaper would report "
           "the same story. Keep every fact, name and number. Do not add anything. Output only the article.")


def shingles(text: str, k: int = 5) -> set[str]:
    w = WORD.findall(text[:2000].lower())
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}


def jaccard(a: str, b: str) -> float:
    x, y = shingles(a), shingles(b)
    return len(x & y) / len(x | y) if x and y else 0.0


def light_edit(text: str) -> str:
    text = re.sub(r"^[A-Z][A-Za-z .,'-]{2,40}\((AP|Reuters|CP|AFP)\)\s*[-—–]+\s*", "", text.strip())
    lines = text.splitlines()
    text = "\n".join(lines[1:]) if len(lines) > 2 else text
    return text[: int(len(text) * 0.7)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--rewriter", default="phi4")
    ap.add_argument("--url", default="http://localhost:11434")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    df = load(None, a.seed)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=a.seed).text)
    text = dict(zip(df.url, df.text))
    print(f"{len(df)} articles; {len(lines)} boilerplate lines")

    # 1. precision before / after stripping, on the labelled detected pairs
    local = HERE / "data" / "annotation_pairs_labelled.csv"  # with article text, not published
    lab = pd.read_csv(local if local.exists() else HERE / "data" / "labels_dependence.csv")
    lab = lab[lab.kind_by_detector == "near-copy"].copy()
    if "miriam_label" in lab:
        lab["label_final"] = lab.miriam_label.where(lab.miriam_label.notna() & (lab.miriam_label != ""), lab.label)
    else:
        lab["label_final"] = lab.label
    lab["j_raw"] = [jaccard(str(text.get(u, "")), str(text.get(v, ""))) for u, v in zip(lab.url_a, lab.url_b)]
    lab["j_strip"] = [jaccard(strip(text.get(u, ""), lines), strip(text.get(v, ""), lines))
                      for u, v in zip(lab.url_a, lab.url_b)]
    real = lab.label_final != "detector_error"
    kept = lab.j_strip >= THRESHOLD
    prec_before = real.mean()
    prec_after = (real & kept).sum() / max(kept.sum(), 1)
    lost = (real & ~kept).sum()

    # 2. recall on edited and reworded copies
    rng = random.Random(a.seed)
    pool = [u for u, t in text.items() if len(strip(t, lines)) >= 1500]
    urls = rng.sample(pool, a.n)
    store = HERE / "data" / "reworded_articles.jsonl"
    done = {}
    if store.exists():
        for line in store.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["rewriter"] == a.rewriter:
                done[r["url"]] = r["reworded"]
    with store.open("a", encoding="utf-8") as f:
        for k, u in enumerate(urls, 1):
            if u in done:
                continue
            original = strip(text[u], lines)[:2500]
            out = ask(a.rewriter, a.url, original, system=REWRITE, max_tokens=900)
            done[u] = out
            f.write(json.dumps({"url": u, "rewriter": a.rewriter, "reworded": out}) + "\n")
            f.flush()
            if k % 20 == 0:
                print(f"  reworded {k}/{len(urls)}")
    rows = []
    for u in urls:
        o = strip(text[u], lines)
        rows.append(dict(url=u, light=jaccard(o, light_edit(o)), reworded=jaccard(o, done[u]),
                         reworded_len=len(done[u]) / max(len(o[:2500]), 1)))
    r = pd.DataFrame(rows)
    rec_light = (r.light >= THRESHOLD).mean()
    rec_rew = (r.reworded >= THRESHOLD).mean()

    md = ["# Copy detector, measured", "",
          f"Detector: 5-word shingles of the first 2,000 characters, near-copy at Jaccard >= {THRESHOLD}.", "",
          f"## Precision on the {len(lab)} labelled detected pairs", "",
          "| | detected | real dependence | precision |", "|---|---|---|---|",
          f"| as published | {len(lab)} | {real.sum()} | {prec_before:.2f} |",
          f"| boilerplate removed | {kept.sum()} | {(real & kept).sum()} | {prec_after:.2f} |", "",
          f"Real dependences no longer detected after stripping: {lost}.", "",
          f"## Recall on {len(r)} articles", "",
          "| copy | linked to its original (recall) | median Jaccard |", "|---|---|---|",
          f"| light edit (dateline removed, first line dropped, last 30% cut) | {rec_light:.2f} | {r.light.median():.2f} |",
          f"| reworded by {a.rewriter} | {rec_rew:.2f} | {r.reworded.median():.2f} |", "",
          f"Median length of the rewrite relative to the original: {r.reworded_len.median():.2f}.", "",
          "For run_copies.py: "
          f"`--set copies.detector_recall={rec_light:.2f} --set copies.paraphrase_evasion={1 - rec_rew:.2f}`"]
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "detector_measured.md").write_text("\n".join(md), encoding="utf-8")
    r.to_csv(HERE / "results" / "detector_recall_articles.csv", index=False)
    print("\n".join(md))


if __name__ == "__main__":
    main()
