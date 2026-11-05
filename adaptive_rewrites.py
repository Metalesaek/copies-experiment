"""Adaptive attacker against the new-information test: rewrite the same 200 articles as
measure_detector.py, but tell the model to ADD invented details so the copy looks like independent
reporting. Stored in data/reworded_articles.jsonl as rewriter "phi4+invented" (resumable).

  python adaptive_rewrites.py                 # phi4 via Ollama, ~1.5 h on the GPU
  python novelty_test.py --rewriter phi4+invented --extractor spacy
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_copies import boilerplate_lines, load, strip
from judge_copies import ask

HERE = Path(__file__).resolve().parent
ADD = ("Rewrite the following news article in your own words, the way a different newspaper would report the "
       "same story. Keep every fact of the original, and ADD three or four plausible new details that are not in "
       "it - for example the name of an official or a witness, a number, a place, or a short quote - so that it "
       "reads like independent reporting. Output only the article.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="phi4")
    ap.add_argument("--url", default="http://localhost:11434")
    a = ap.parse_args()
    name = a.model + "+invented"
    store = HERE / "data" / "reworded_articles.jsonl"
    rows = [json.loads(line) for line in store.read_text(encoding="utf-8").splitlines()]
    urls = [r["url"] for r in rows if r["rewriter"] == a.model]
    done = {r["url"] for r in rows if r["rewriter"] == name}
    todo = [u for u in urls if u not in done]
    print(f"{len(urls)} articles, {len(todo)} to rewrite with invented details")
    if not todo:
        return
    df = load(None, 0)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=0).text)
    text = dict(zip(df.url, df.text))
    with store.open("a", encoding="utf-8") as f:
        for k, u in enumerate(todo, 1):
            out = ask(a.model, a.url, strip(text[u], lines)[:2500], system=ADD, max_tokens=900)
            f.write(json.dumps({"url": u, "rewriter": name, "reworded": out}) + "\n")
            f.flush()
            if k % 20 == 0:
                print(f"  {k}/{len(todo)}")


if __name__ == "__main__":
    main()
