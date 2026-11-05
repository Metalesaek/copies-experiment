#!/usr/bin/env bash
# Phase 6 (fourth review):
#   1. copy networks of real rewrites: 20 originals x 10 phi4 rewrites x {plain, adaptive}, detectors run on them
#   2. baselines for recognising rewrites (TF-IDF, sentence embeddings, cross-encoder, entity/quote overlap)
#   3. learning stream with the MEASURED miss patterns of those networks instead of independent misses
#   4. 10 seeds instead of 3 for the Llama 3.2 and Gemini Flash judges (copy attack)
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; export GEMINI_API_KEY=... ; Ollama running
# Run:     bash review_phase6.sh 2>&1 | tee results/review_phase6.log      (~11 h; resumable: just run it again)
set -e
cd "$(dirname "$0")"
uv pip install scikit-learn sentence-transformers

echo "== 1. copy networks: 400 phi4 rewrites (~3 h), then the detectors on them"
python multi_rewrites.py --generate
python multi_rewrites.py

echo "== 2. baselines (CPU, ~30 min; downloads two embedding models and a cross-encoder)"
python baselines.py

param() { python -c "import json; print(json.load(open('results/$1'))['$2'])"; }
EVADE=$(python -c "print(round(1 - $(param novelty_params_spacy.json recall_reworded), 3))")
MERGE=$(param novelty_params_spacy.json false_merge)
NOV="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=$EVADE --set copies.false_merge=$MERGE"
MEAS="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=1.0"
PROF="--set copies.miss_profiles=results/miss_profiles.json"
SEEDS3="--seeds 10 11 12"
SEEDS10="--seeds 10 11 12 13 14 15 16 17 18 19"

echo "== 3/4. verdicts (no training)"
python run_copies.py $SEEDS3 --tag copies_e2e --attacks paraphrase --systems judge_chains --judge_only \
       $NOV $PROF --set copies.miss_profile_key=paraphrase/new_information
python run_copies.py $SEEDS3 --tag copies_e2e_adaptive --attacks paraphrase --systems judge_chains --judge_only \
       $NOV $PROF --set copies.miss_profile_key=adaptive/new_information
python run_copies.py $SEEDS10 --tag copies_measured_llama --attacks copy --systems judge_all judge_chains --judge_only \
       $MEAS --set copies.judge_model=llama3.2
python run_copies.py $SEEDS10 --tag copies_measured_flash --attacks copy --systems judge_all judge_chains --judge_only \
       $MEAS --set copies.judge_model=gemini:gemini-2.5-flash
echo "   waiting 6 minutes for Ollama to unload its model and free the GPU"
sleep 360

echo "== 3. training with measured miss patterns (~1.7 h)"
python run_copies.py $SEEDS3 --tag copies_e2e --attacks paraphrase --systems judge_chains chains_k \
       $NOV $PROF --set copies.miss_profile_key=paraphrase/new_information
python run_copies.py $SEEDS3 --tag copies_e2e_adaptive --attacks paraphrase --systems judge_chains chains_k \
       $NOV $PROF --set copies.miss_profile_key=adaptive/new_information
echo "== 4. training, 10 seeds for Llama 3.2 and Gemini Flash (~4.8 h)"
python run_copies.py $SEEDS10 --tag copies_measured_llama --attacks copy --systems judge_all judge_chains \
       $MEAS --set copies.judge_model=llama3.2
python run_copies.py $SEEDS10 --tag copies_measured_flash --attacks copy --systems judge_all judge_chains \
       $MEAS --set copies.judge_model=gemini:gemini-2.5-flash
echo "== phase 6 done"
