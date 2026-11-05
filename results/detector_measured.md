# Copy detector, measured

Detector: 5-word shingles of the first 2,000 characters, near-copy at Jaccard >= 0.6.

## Precision on the 150 labelled detected pairs

| | detected | real dependence | precision |
|---|---|---|---|
| as published | 150 | 123 | 0.82 |
| boilerplate removed | 119 | 116 | 0.97 |

Real dependences no longer detected after stripping: 7.

## Recall on 200 articles

| copy | linked to its original (recall) | median Jaccard |
|---|---|---|
| light edit (dateline removed, first line dropped, last 30% cut) | 0.92 | 0.81 |
| reworded by phi4 | 0.00 | 0.04 |

Median length of the rewrite relative to the original: 0.75.

For run_copies.py: `--set copies.detector_recall=0.92 --set copies.paraphrase_evasion=1.00`