#!/usr/bin/env bash
# Phase 9 (IP&M preparation): the learning stream on REAL articles with the REAL detectors (real_carriers.py)
#   1. phi4 judge, all four attacks, both judge variants + counting rules        (~10 h, GPU via Ollama)
#   2. text detector alone on the reworded attacks (how much the novelty test adds) (~3.5 h, verdicts partly cached)
#   3. llama3.2 judge, all four attacks                                           (~6-8 h)
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; Ollama running (phi4 and llama3.2 pulled);
#          data/carriers.jsonl built once by:  python real_carriers.py --prepare
#          laptop on power, sleep off
# Run:     bash review_phase9.sh 2>&1 | tee -a results/review_phase9.log     (~20 h; resumable: just run it again)
set -e
cd "$(dirname "$0")"
[ -f data/carriers.jsonl ] || { echo "run: python real_carriers.py --prepare"; exit 1; }
R="--set copies.carriers=real"

echo "== 1. phi4, real carriers, text + novelty detector"
python run_copies.py $R --attacks copy paraphrase adaptive collusion \
  --systems chains_k chains_k_judge judge_all judge_chains --seeds 10 11 12 --tag real_phi4

echo "== 2. phi4, real carriers, text detector only (reworded attacks)"
mkdir -p results/real_phi4_text
[ -f results/real_phi4_text/judge_cache_phi4.jsonl ] || cp results/real_phi4/judge_cache_phi4.jsonl results/real_phi4_text/
python run_copies.py $R --set copies.detector=text --attacks paraphrase adaptive \
  --systems chains_k judge_chains --seeds 10 11 12 --tag real_phi4_text

echo "== 3. llama3.2, real carriers, text + novelty detector"
python run_copies.py $R --set copies.judge_model=llama3.2 --attacks copy paraphrase adaptive collusion \
  --systems judge_all judge_chains --seeds 10 11 12 --tag real_llama
echo "== phase 9 done"
