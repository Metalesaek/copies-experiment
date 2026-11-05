"""Copy networks of real rewritten articles, and the detectors run on them (review W1 / Q7).

  python multi_rewrites.py --generate     # phi4 via Ollama: 20 originals x 10 sampled rewrites x 2 prompts (~3 h)
  python multi_rewrites.py                # run the detectors, write the miss profiles (CPU, ~10 min)

The stream simulation drew detector misses independently for each copy. Here an attacker turns ONE
original article into TEN rewrites with the same prompt (temperature 0.8, seeds 1-10): plain rewrites
(REWRITE of measure_detector.py) and adaptive ones with invented details (ADD of adaptive_rewrites.py).
The real detectors then process each copy network as a stream would:
  text detector         5-gram Jaccard >= 0.6 with the origin or with any copy already linked
  new-information test  entity-and-quotation novelty < 0.4 against the origin or any copy already linked
A copy that no detector links counts as a new source. Output:
  results/miss_profiles.json   per attack and detector, one list of 10 booleans (missed?) per network,
                               used by run_copies.py with --set copies.miss_profiles=...
  results/multi_rewrites.md    misses per network, compared with independent misses at the same rate
Rewrites are stored in data/multi_rewrites.jsonl (contains article text: not published).
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import pandas as pd

from adaptive_rewrites import ADD
from check_copies import boilerplate_lines, load, strip
from judge_copies import ask
from measure_detector import REWRITE, jaccard
from novelty_test import novelty, spacy_facts

HERE = Path(__file__).resolve().parent
STORE = HERE / "data" / "multi_rewrites.jsonl"
PROMPTS = {"paraphrase": REWRITE, "adaptive": ADD}
N_ORIG, N_COPIES = 20, 10


def originals():
    rows = [json.loads(x) for x in (HERE / "data" / "reworded_articles.jsonl").read_text(encoding="utf-8").splitlines()]
    urls = sorted({r["url"] for r in rows if r["rewriter"] == "phi4"})
    return random.Random(0).sample(urls, N_ORIG)


def texts_for(urls):
    df = load(None, 0)
    lines = boilerplate_lines(df.sample(min(200_000, len(df)), random_state=0).text)
    want = set(urls)
    return {u: strip(t, lines) for u, t in zip(df.url, df.text) if u in want}


def generate(model: str, url: str):
    urls = originals()
    text = texts_for(urls)
    done = set()
    if STORE.exists():
        for line in STORE.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["attack"], r["url"], r["copy"]))
    todo = [(a, u, k) for a in PROMPTS for u in urls for k in range(1, N_COPIES + 1) if (a, u, k) not in done]
    print(f"{len(todo)} rewrites to generate")
    with STORE.open("a", encoding="utf-8") as f:
        for n, (a, u, k) in enumerate(todo, 1):
            out = ask(model, url, text[u][:2500], system=PROMPTS[a], max_tokens=900, temperature=0.8, seed=k)
            f.write(json.dumps({"attack": a, "url": u, "copy": k, "text": out}) + "\n")
            f.flush()
            if n % 20 == 0:
                print(f"  {n}/{len(todo)}")


def link_chain(n_copies: int, linked_fn) -> list[bool]:
    """Stream order: copy j is linked if it matches the origin or any copy already linked. Returns missed?"""
    linked, missed = [0], []  # indices into [origin] + copies
    for j in range(1, n_copies + 1):
        hit = any(linked_fn(i, j) for i in linked)
        missed.append(not hit)
        if hit:
            linked.append(j)
    return missed


def measure():
    rows = [json.loads(x) for x in STORE.read_text(encoding="utf-8").splitlines()]
    urls = originals()
    text = texts_for(urls)
    profiles, md = {}, ["# Copy networks of real rewrites: what the detectors miss", "",
                        f"{N_ORIG} originals, {N_COPIES} rewrites each by phi4 (temperature 0.8, seeds 1-10), "
                        "linked in stream order to the origin or any copy already linked.", "",
                        "| attack | detector | copies missed (share) | networks with 0 missed | with all 10 missed "
                        "| P(at least one missed), observed | same, if misses were independent |",
                        "|---|---|---|---|---|---|---|"]
    for attack in PROMPTS:
        nets = []
        for u in urls:
            cs = sorted((r for r in rows if r["attack"] == attack and r["url"] == u), key=lambda r: r["copy"])
            if len(cs) == N_COPIES and u in text:
                nets.append([text[u][:2500]] + [r["text"][:2500] for r in cs])
        for det in ("text", "new_information"):
            prof = []
            for docs in nets:
                if det == "text":
                    fn = lambda i, j, d=docs: jaccard(d[i], d[j]) >= 0.6
                else:
                    fs = spacy_facts(docs)
                    fn = lambda i, j, f=fs: novelty(f[i], f[j]) < 0.4
                prof.append(link_chain(len(docs) - 1, fn))
            profiles[f"{attack}/{det}"] = prof
            p = pd.DataFrame(prof)
            rate = p.values.mean()
            md.append(f"| {attack} | {det} | {rate:.2f} | {(p.sum(1) == 0).mean():.2f} | {(p.sum(1) == N_COPIES).mean():.2f} "
                      f"| {(p.sum(1) > 0).mean():.2f} | {1 - (1 - rate) ** N_COPIES:.2f} |")
    (HERE / "results" / "miss_profiles.json").write_text(json.dumps(profiles), encoding="utf-8")
    (HERE / "results" / "multi_rewrites.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--model", default="phi4")
    ap.add_argument("--url", default="http://localhost:11434")
    a = ap.parse_args()
    if a.generate:
        generate(a.model, a.url)
    else:
        measure()


if __name__ == "__main__":
    main()
