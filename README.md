# Copies Are Not Confirmations

Code, labels and results for *Copies Are Not Confirmations: How News Duplication Fools LLM Judges and
Continual Learners* (Abdelkader Metales and Miriam Grabenheinrich, caaise GmbH, 2026).

Many news reports of a claim are copies of one source (wire stories, syndication, press releases). We
measure how common copying is in CC-News, test whether LLM judges treat copies as independent
confirmation, and show what this does to a continual learner that learns from a stream of reports.

## Setup

```bash
uv pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

The learning stream (`run_copies.py`) reuses the student, world and verifier code of our earlier paper,
[Surprise Alone Learns Lies](https://arxiv.org/abs/2610.39840) (code:
[Metalesaek/sura-metales](https://github.com/Metalesaek/sura-metales)). Clone it next to this folder as
`../sura_experiment`; `configs/copies.yaml` inherits its `configs/default.yaml`.

Local judges run through [Ollama](https://ollama.com) (`phi4`, `llama3.2`). Gemini judges read the API key
from the environment variable `GEMINI_API_KEY` (never stored in files).

## Data and article text

Articles come from CC-News on Hugging Face (`vblagoje/cc_news`), a uniform random sample of 200,000
(seed 0). **This repository contains no article text**: the texts belong to the outlets. Every file
identifies articles by URL (and headline); the scripts rebuild the texts from CC-News
(`export_pair_texts.py`, `export_independent_pairs.py`), and the LLM rewrites are regenerated with
`measure_detector.py`, `adaptive_rewrites.py` and `multi_rewrites.py --generate`.

## Paper sections and files

| Section | Scripts | Results |
| --- | --- | --- |
| 3 How news is copied | `check_copies.py` (MinHash chains, `--strip` removes boilerplate), `measure_detector.py`, `chain_purity.py`, `compute_iaa.py` | `results/copies_summary*.md`, `data/copy_chains*.csv`, `results/detector_measured.md`, `results/chain_purity*.md` |
| 4 Do LLM judges count copies? | `judge_copies.py` (`--unsure`, `--probes`), `reanalyse_judges.py` | `results/judge_copies_v2/`, `results/judge_reanalysis.md` |
| 5 Learning from a simulated stream | `copies_world.py`, `run_copies.py`, `test_copies.py` | `results/copies_*/results.jsonl` (one line per system, attack and seed) |
| 6 Catching reworded copies | `novelty_test.py`, `adaptive_rewrites.py`, `baselines.py`, `multi_rewrites.py`, `make_independent_set.py` | `results/novelty_test*.md`, `results/baselines.md`, `results/multi_rewrites.md`, `results/miss_profiles.json`, `results/indep_set.md` |

The run scripts `review_phase1.sh` to `review_phase7.sh` reproduce the experiments in the order they were
run; their logs are in `results/review_phase*.log`. Each learning run folder holds the judge verdict cache
(`judge_cache_*.jsonl`), so the runs can be repeated without calling the judges again.

## Labels

| File | Content |
| --- | --- |
| `data/labels_dependence.csv` | 300 pairs of Section 3 (150 detected near-copies, 150 controls): AI-drafted dependence label |
| `data/labels_iaa.csv` | 100 of them labelled blind by both authors (author1 = Metales, author2 = Grabenheinrich) and the AI draft |
| `data/labels_independent_check.csv` | 40 automatically selected comparison pairs of Section 6, checked by hand |
| `data/labels_indep_set.csv` | 250 held-out same-event pairs of Section 6, labelled blind by both authors |

`make_release_labels.py` writes these files from the local annotation sheets, which contain article text
and are not published.

## Licence

Code and labels: MIT (see `LICENSE`). Article URLs and headlines refer to CC-News; the articles
themselves are not redistributed.
