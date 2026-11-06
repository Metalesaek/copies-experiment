#!/usr/bin/env bash
# Phase 8 (eighth review):
#   1. the same 200 articles rewritten by two more models, llama3.2 (Ollama) and gemini-2.5-flash (API),
#      text detector on them                                             (~1 h, GPU via Ollama + API)
#   2. new-information test (spaCy) on those rewrites                    (CPU, ~20 min)
#   3. text window of the copy detector: 1,000 / 2,000 / 4,000 / full / last 2,000 characters (CPU, ~1 h)
#   4. baselines with modern embeddings (bge-large, gte-large, online gemini-embedding-001 ~$0.15)
#      and a reranker (bge-reranker-large),
#      also scored on the 250 held-out same-event pairs and the new rewrites   (GPU ~20 min; downloads ~3 GB)
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; Ollama running (llama3.2);
#          export GEMINI_API_KEY=...   (internet on: step 4 downloads the new models once)
# Run:     bash review_phase8.sh 2>&1 | tee results/review_phase8.log      (~3 h; resumable: just run it again)
set -e
cd "$(dirname "$0")"
[ -n "$GEMINI_API_KEY" ] || { echo "export GEMINI_API_KEY first"; exit 1; }

echo "== 1. rewrites by llama3.2 and gemini-2.5-flash"
python other_rewriters.py
echo "== 2. new-information test on them"
python novelty_test.py --rewriter llama3.2 --extractor spacy
python novelty_test.py --rewriter gemini-2.5-flash --extractor spacy
echo "== 3. text window of the copy detector (Ollama unloads its model meanwhile)"
python window_ablation.py
echo "== 4. baselines with modern embeddings and a reranker"
python baselines.py
echo "== phase 8 done"
