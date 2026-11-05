#!/usr/bin/env bash
# Review runs, phase 3 (second review):
#   - measured detector (recall 0.92 / 0.00) for the Llama 3.2 and Gemini Flash judges
#   - Gemini 2.5 Pro as the judge in the learning stream (copy attack, 3 seeds; about $10 of API calls)
# Before:  source ~/Documents/sura_experiment/.venv/Scripts/activate ; export GEMINI_API_KEY=... ; Ollama running
# Run:     bash review_phase3.sh 2>&1 | tee results/review_phase3.log      (~1.5 h verdicts + ~3.5 h training)
set -e
cd "$(dirname "$0")"
MEAS="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=1.0"
SEEDS="--seeds 10 11 12"

echo "== verdicts (no training)"
python run_copies.py $SEEDS --tag copies_measured_llama --attacks copy paraphrase --systems judge_chains --judge_only \
       $MEAS --set copies.judge_model=llama3.2
python run_copies.py $SEEDS --tag copies_measured_flash --attacks copy paraphrase --systems judge_chains --judge_only \
       $MEAS --set copies.judge_model=gemini:gemini-2.5-flash
python run_copies.py $SEEDS --tag copies_gemini_pro --attacks copy --systems judge_all judge_chains --judge_only \
       $MEAS --set copies.judge_model=gemini:gemini-2.5-pro
echo "   waiting 6 minutes for Ollama to unload its model and free the GPU"
sleep 360

echo "== training with the saved verdicts"
python run_copies.py $SEEDS --tag copies_measured_llama --attacks copy paraphrase --systems judge_chains \
       $MEAS --set copies.judge_model=llama3.2
python run_copies.py $SEEDS --tag copies_measured_flash --attacks copy paraphrase --systems judge_chains \
       $MEAS --set copies.judge_model=gemini:gemini-2.5-flash
python run_copies.py $SEEDS --tag copies_gemini_pro --attacks copy --systems judge_all judge_chains \
       $MEAS --set copies.judge_model=gemini:gemini-2.5-pro
echo "== phase 3 done"
