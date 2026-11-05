#!/usr/bin/env bash
# Review runs, phase 1: everything that needs Ollama (phi4, llama3.2) or the Gemini API. No training.
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; export GEMINI_API_KEY=...
# Run:     bash review_phase1.sh 2>&1 | tee results/review_phase1.log
# Every step saves as it goes; rerunning the script skips finished work.
set -e
cd "$(dirname "$0")"
SS20='copies.truth_chains=[[1,0.2],[2,0.5],[3,0.3]]'
SS80='copies.truth_chains=[[1,0.8],[2,0.15],[3,0.05]]'

echo "== 1. copy measurement with boilerplate removed (CPU, ~30 min)"
python check_copies.py --limit 200000 --strip

echo "== 2. detector precision after stripping, recall on edited and phi4-reworded copies (~1.5 h)"
python measure_detector.py

echo "== 3. judge experiment v2: 64-token answers, 5 copies, length-matched control, Unsure option, Gemini"
python judge_copies.py --judges phi4 llama3.2 gemini:gemini-2.5-flash gemini:gemini-2.5-pro --unsure

echo "== 4. verdict caches for the learning runs (no training)"
python run_copies.py --seeds 10 11 12 --tag copies_gemini --systems judge_all judge_chains --judge_only \
       --set copies.judge_model=gemini:gemini-2.5-flash
python run_copies.py --seeds 10 11 12 --tag copies_ss20 --attacks copy --systems judge_all judge_chains --judge_only \
       --set "$SS20"
python run_copies.py --seeds 10 11 12 --tag copies_ss80 --attacks copy --systems judge_all judge_chains --judge_only \
       --set "$SS80"
echo "== phase 1 done"
