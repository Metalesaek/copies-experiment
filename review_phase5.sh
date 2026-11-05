#!/usr/bin/env bash
# Phase 5 (third review):
#   1. copy chains: threshold sensitivity and purity (CPU)
#   2. judge probes: same outlet, false "independent" note, rewrite note, provenance table, known agencies
#   3. re-analysis of the judge experiment (three outcomes, paired tests)
#   4. learning stream, phi4, new-information detector: 10 seeds instead of 3 (judge_all vs judge_chains)
#   5. learning stream with correlated detector misses (all copies of a lie missed together, or none)
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; export GEMINI_API_KEY=... ; Ollama running
# Run:     bash review_phase5.sh 2>&1 | tee results/review_phase5.log      (~10 h; resumable: just run it again)
set -e
cd "$(dirname "$0")"

echo "== 1. chain purity (CPU, ~40 min)"
python chain_purity.py
python chain_purity.py --strip

echo "== 2. judge probes (4 judges x 6 conditions x 320 claims, ~1.5 h, Gemini about \$3-5)"
python judge_copies.py --judges phi4 llama3.2 gemini:gemini-2.5-flash gemini:gemini-2.5-pro --probes
echo "== 3. re-analysis"
python reanalyse_judges.py

param() { python -c "import json; print(json.load(open('results/$1'))['$2'])"; }
EVADE=$(python -c "print(round(1 - $(param novelty_params_spacy.json recall_reworded), 3))")
MERGE=$(param novelty_params_spacy.json false_merge)
NOV="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=$EVADE --set copies.false_merge=$MERGE"
SEEDS10="--seeds 10 11 12 13 14 15 16 17 18 19"
SEEDS3="--seeds 10 11 12"
CORR="--set copies.correlated_misses=true"
echo "   new-information detector: reworded copies missed $EVADE, false merge $MERGE"

echo "== 4/5. phi4 verdicts (no training)"
python run_copies.py $SEEDS10 --tag copies_novelty --attacks copy paraphrase --systems judge_all judge_chains --judge_only $NOV
python run_copies.py $SEEDS3 --tag copies_correlated --attacks copy paraphrase --systems judge_chains --judge_only $NOV $CORR
echo "   waiting 6 minutes for Ollama to unload its model and free the GPU"
sleep 360

echo "== 4. training, 10 seeds (~4.5 h)"
python run_copies.py $SEEDS10 --tag copies_novelty --attacks copy paraphrase --systems judge_all judge_chains $NOV
echo "== 5. training, correlated misses (~1.7 h)"
python run_copies.py $SEEDS3 --tag copies_correlated --attacks copy paraphrase --systems judge_chains chains_k $NOV $CORR
echo "== phase 5 done"
