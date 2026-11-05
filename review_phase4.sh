#!/usr/bin/env bash
# Phase 4: the new-information detector against rewritten copies.
#   1. adaptive attacker: phi4 rewrites the 200 articles and ADDS invented details
#   2. new-information test (spaCy) on plain and adaptive rewrites -> measured detector parameters
#   3. learning stream with the measured new-information detector (copy, paraphrase, collusion),
#      and the paraphrase attack with the adaptive rewriter's evasion rate
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; Ollama running (phi4)
# Run:     bash review_phase4.sh 2>&1 | tee results/review_phase4.log      (~10 h)
set -e
cd "$(dirname "$0")"
SEEDS="--seeds 10 11 12"
SYS="chains_k chains_k_judge judge_chains"

echo "== 1. adaptive rewrites (phi4, ~1.5 h)"
python adaptive_rewrites.py

echo "== 2. new-information test, plain and adaptive rewrites (CPU, ~40 min)"
python novelty_test.py --rewriter phi4 --extractor spacy
python novelty_test.py --rewriter phi4+invented --extractor spacy

param() { python -c "import json; print(json.load(open('results/$1'))['$2'])"; }
EVADE=$(python -c "print(round(1 - $(param novelty_params_spacy.json recall_reworded), 3))")
MERGE=$(param novelty_params_spacy.json false_merge)
EVADE_ADAPT=$(python -c "print(round(1 - $(param novelty_params_phi4_invented_spacy.json recall_reworded), 3))")
echo "   measured: reworded copies missed $EVADE (adaptive: $EVADE_ADAPT), independent chains wrongly merged $MERGE"
# Verbatim copies keep the text detector's measured recall (0.92): conservative, since a light edit adds no facts.
NOV="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=$EVADE --set copies.false_merge=$MERGE"
ADAPT="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=$EVADE_ADAPT --set copies.false_merge=$MERGE"

echo "== 3. phi4 verdicts for the new detector (no training)"
python run_copies.py $SEEDS --tag copies_novelty --systems judge_chains --judge_only $NOV
python run_copies.py $SEEDS --tag copies_novelty_adaptive --attacks paraphrase --systems judge_chains --judge_only $ADAPT
echo "   waiting 6 minutes for Ollama to unload its model and free the GPU"
sleep 360

echo "== 4. training (~6.5 h)"
python run_copies.py $SEEDS --tag copies_novelty --systems $SYS $NOV
python run_copies.py $SEEDS --tag copies_novelty_adaptive --attacks paraphrase --systems $SYS $ADAPT
echo "== phase 4 done"
