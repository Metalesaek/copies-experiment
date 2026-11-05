#!/usr/bin/env bash
# Phase 7 (fifth review):
#   1. labelling sheets for a larger held-out set of same-event pairs (CPU, ~30-60 min) -> both authors label them
#   2. sensitivity of the learning results to false merges of independent chains: 0.10, 0.20, 0.30
#      (phi4 judge, one report per chain, new-information detector; copy, paraphrase, collusion; 3 seeds)
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; Ollama running (phi4)
# Run:     bash review_phase7.sh 2>&1 | tee results/review_phase7.log      (~4.5 h; resumable: just run it again)
set -e
cd "$(dirname "$0")"
export HF_HUB_OFFLINE=1

echo "== 1. labelling sheets (data/indep_set_author1.xlsx, data/indep_set_author2.xlsx)"
python make_independent_set.py

param() { python -c "import json; print(json.load(open('results/$1'))['$2'])"; }
EVADE=$(python -c "print(round(1 - $(param novelty_params_spacy.json recall_reworded), 3))")
SEEDS3="--seeds 10 11 12"
for FM in 0.10 0.20 0.30; do
  TAG=copies_fm${FM#0.}
  ARGS="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=$EVADE --set copies.false_merge=$FM"
  echo "== 2. false merge $FM: phi4 verdicts"
  python run_copies.py $SEEDS3 --tag $TAG --systems judge_chains --judge_only $ARGS
done
echo "   waiting 6 minutes for Ollama to unload its model and free the GPU"
sleep 360
for FM in 0.10 0.20 0.30; do
  TAG=copies_fm${FM#0.}
  ARGS="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=$EVADE --set copies.false_merge=$FM"
  echo "== 2. false merge $FM: training"
  python run_copies.py $SEEDS3 --tag $TAG --systems judge_chains $ARGS
done
echo "== phase 7 done"
