"""More rewriting models (review: "phi4 only"). Rewrites the same 200 articles as measure_detector.py with
the same prompt (REWRITE), by Llama 3.2 (Ollama) and Gemini 2.5 Flash (API), and measures the text
detector on them (5-gram Jaccard >= 0.6 with the original).

  python other_rewriters.py                       # ~1 h (Llama 3.2 local) + a few minutes (Gemini Flash)
  python novelty_test.py --rewriter llama3.2 --extractor spacy
  python novelty_test.py --rewriter gemini-2.5-flash --extractor spacy

Stored in data/reworded_articles.jsonl (rewriter names "llama3.2" and "gemini-2.5-flash"; article
text: not published). Writes results/other_rewriters.md.
"""
from __future__ import annotations

import json
from pathlib import Path

from check_copies import boilerplate_lines, load, strip
from judge_copies import ask
from measure_detector import REWRITE, THRESHOLD, jaccard

HERE = Path(__file__).resolve().parent
STORE = HERE / "data" / "reworded_articles.jsonl"
MODELS = {"llama3.2": "llama3.2", "gemini-2.5-flash": "gemini:gemini-2.5-flash"}


def main():
    rows = [json.loads(x) for x in STORE.read_text(encoding="utf-8").splitlines()]
    urls = [r["url"] for r in rows if r["rewriter"] == "phi4"]
    df = load(None, 0)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=0).text)
    text = {u: strip(t, lines) for u, t in zip(df.url, df.text) if u in set(urls)}
    md = ["# Rewrites by other models: text detector", "",
          f"Same {len(urls)} articles and prompt as the phi4 rewrites (measure_detector.py).", "",
          "| rewriter | rewrites | linked by the text detector (Jaccard >= 0.6) | median Jaccard |", "|---|---|---|---|"]
    for name, model in [("phi4", None)] + list(MODELS.items()):
        done = {r["url"]: r["reworded"] for r in rows if r["rewriter"] == name}
        if model:
            todo = [u for u in urls if u not in done]
            print(f"{name}: {len(todo)} rewrites to generate")
            with STORE.open("a", encoding="utf-8") as f:
                for k, u in enumerate(todo, 1):
                    out = ask(model, "http://localhost:11434", text[u][:2500], system=REWRITE, max_tokens=900)
                    if not out.strip():  # empty answer (e.g. blocked): not stored, retried on the next run
                        continue
                    done[u] = out
                    f.write(json.dumps({"url": u, "rewriter": name, "reworded": out}) + "\n")
                    f.flush()
                    if k % 20 == 0:
                        print(f"  {k}/{len(todo)}")
        j = sorted(jaccard(text[u], done[u]) for u in urls if u in done and u in text)
        md.append(f"| {name} | {len(j)} | {sum(x >= THRESHOLD for x in j) / len(j):.2f} | {j[len(j) // 2]:.2f} |")
    (HERE / "results" / "other_rewriters.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
