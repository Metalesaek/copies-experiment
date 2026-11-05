#!/usr/bin/env bash
# Review runs, phase 2: training with the verdicts saved in phase 1. Keep Ollama running at the start:
# the first step collects phi4 verdicts for the measured detector, then the script waits 6 minutes
# so Ollama frees the GPU before any training starts.
# Run:     bash review_phase2.sh 2>&1 | tee results/review_phase2.log
set -e
cd "$(dirname "$0")"
SS20='copies.truth_chains=[[1,0.2],[2,0.5],[3,0.3]]'
SS80='copies.truth_chains=[[1,0.8],[2,0.15],[3,0.05]]'
SYS="chains_k chains_k_judge judge judge_all judge_chains"
# Detector values measured by measure_detector.py (results/detector_measured.md)
MEAS="--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=1.0"

echo "== verdict caches with the MEASURED detector (phi4; needs Ollama running, ~1 h)"
python run_copies.py --seeds 10 11 12 --tag copies_measured --attacks copy paraphrase \
       --systems judge_chains --judge_only $MEAS
echo "   waiting 6 minutes for Ollama to unload its model and free the GPU"
sleep 360

echo "== measured detector: systems that depend on it, copy + paraphrase attacks (~3.5 h)"
python run_copies.py --seeds 10 11 12 --tag copies_measured --attacks copy paraphrase \
       --systems chains_k chains_k_judge judge_chains $MEAS

echo "== Gemini 2.5 Flash as the real judge, 3 attacks x 3 seeds (~3.5 h)"
python run_copies.py --seeds 10 11 12 --tag copies_gemini --systems judge_all judge_chains \
       --set copies.judge_model=gemini:gemini-2.5-flash

echo "== share of single-source truths 20% and 80% (copy attack, ~5.5 h; 50% is copies_v1)"
python run_copies.py --seeds 10 11 12 --tag copies_ss20 --attacks copy --systems $SYS --set "$SS20"
python run_copies.py --seeds 10 11 12 --tag copies_ss80 --attacks copy --systems $SYS --set "$SS80"
echo "== phase 2 done"
