# Baselines: recognising rewritten copies

Positives: 200 phi4 rewrites and 200 adaptive rewrites of their original. Negatives: 167 automatically selected comparison reports of the same event, of which 11 are confirmed independent by hand. Copy score: higher = more likely a copy. AUC = P(copy scores higher than non-copy). Recall at 5% FA: threshold set so that 5% of the comparison reports are flagged.

| detector | AUC rewrite vs all | AUC rewrite vs confirmed | AUC adaptive vs all | AUC adaptive vs confirmed | recall at 5% FA, rewrite | recall at 5% FA, adaptive |
|---|---|---|---|---|---|---|
| jaccard_5gram | 0.85 | 0.72 | 0.86 | 0.75 | 0.06 | 0.11 |
| tfidf_cosine | 0.94 | 0.92 | 0.93 | 0.90 | 0.62 | 0.53 |
| emb_minilm | 0.91 | 0.70 | 0.92 | 0.72 | 0.50 | 0.52 |
| emb_mpnet | 0.91 | 0.77 | 0.91 | 0.77 | 0.46 | 0.47 |
| cross_encoder | 0.86 | 0.80 | 0.88 | 0.83 | 0.36 | 0.43 |
| entity_overlap | 0.97 | 0.98 | 0.95 | 0.97 | 0.91 | 0.78 |
| quote_overlap | 0.57 | 0.52 | 0.60 | 0.55 | 0.18 | 0.18 |
| ours_1_minus_novelty | 0.97 | 0.98 | 0.94 | 0.94 | 0.91 | 0.68 |
| hybrid_ours_plus_emb_minilm | 0.96 | 0.93 | 0.94 | 0.88 | 0.81 | 0.69 |

Medians of each score:

|                             |   adaptive |   comparison |   comparison (confirmed) |   rewrite |
|:----------------------------|-----------:|-------------:|-------------------------:|----------:|
| jaccard_5gram               |       0.04 |         0    |                     0    |      0.04 |
| tfidf_cosine                |       0.63 |         0.16 |                     0.47 |      0.65 |
| emb_minilm                  |       0.89 |         0.46 |                     0.84 |      0.89 |
| emb_mpnet                   |       0.93 |         0.51 |                     0.88 |      0.93 |
| cross_encoder               |       0.61 |         0.49 |                     0.54 |      0.6  |
| entity_overlap              |       0.74 |         0.14 |                     0.38 |      0.81 |
| quote_overlap               |       0    |         0    |                     0    |      0    |
| ours_1_minus_novelty        |       0.69 |         0.14 |                     0.38 |      0.79 |
| hybrid_ours_plus_emb_minilm |       0.6  |         0.14 |                     0.34 |      0.69 |