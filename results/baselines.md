# Baselines: recognising rewritten copies

Positives: 200 phi4 rewrites and 200 adaptive rewrites of their original. Negatives: 167 automatically selected comparison reports of the same event, of which 11 are confirmed independent by hand. Copy score: higher = more likely a copy. AUC = P(copy scores higher than non-copy). Recall at 5% FA: threshold set so that 5% of the comparison reports are flagged.

| detector | AUC rewrite vs all | AUC rewrite vs confirmed | AUC adaptive vs all | AUC adaptive vs confirmed | recall at 5% FA, rewrite | recall at 5% FA, adaptive |
|---|---|---|---|---|---|---|
| jaccard_5gram | 0.85 | 0.72 | 0.86 | 0.75 | 0.06 | 0.11 |
| tfidf_cosine | 0.94 | 0.93 | 0.93 | 0.91 | 0.64 | 0.55 |
| emb_minilm | 0.91 | 0.70 | 0.92 | 0.72 | 0.50 | 0.52 |
| emb_mpnet | 0.91 | 0.77 | 0.91 | 0.77 | 0.46 | 0.47 |
| emb_bge_large | 0.95 | 0.88 | 0.94 | 0.85 | 0.68 | 0.61 |
| emb_gte_large | 0.96 | 0.89 | 0.94 | 0.84 | 0.75 | 0.63 |
| emb_gemini_001 | 0.95 | 0.94 | 0.93 | 0.88 | 0.61 | 0.42 |
| cross_encoder | 0.86 | 0.80 | 0.88 | 0.83 | 0.36 | 0.43 |
| reranker_bge_large | 0.82 | 0.77 | 0.78 | 0.73 | 0.27 | 0.22 |
| entity_overlap | 0.97 | 0.98 | 0.95 | 0.97 | 0.91 | 0.78 |
| quote_overlap | 0.57 | 0.52 | 0.60 | 0.55 | 0.18 | 0.18 |
| ours_1_minus_novelty | 0.97 | 0.98 | 0.94 | 0.94 | 0.91 | 0.68 |
| hybrid_ours_plus_emb_gte_large | 0.98 | 0.97 | 0.96 | 0.93 | 0.90 | 0.74 |

## Held-out natural pairs (63 same-source and 100 independent pairs, both authors agree; data/labels_indep_set.csv)

Original = the earlier report. AUC same-source vs independent: can the detector tell a natural derivative from an independent report of the same event? Rewrites vs held-out independent: the phi4 rewrites as positives, the held-out independent reports as negatives. Recall at 5% FA: threshold set so that 5% of the held-out independent reports are flagged.

| detector | AUC same-source vs independent | AUC rewrite vs held-out independent | AUC adaptive vs held-out independent | recall at 5% FA, same-source | recall at 5% FA, rewrite | recall at 5% FA, adaptive |
|---|---|---|---|---|---|---|
| jaccard_5gram | 0.90 | 0.92 | 0.93 | 0.52 | 0.48 | 0.54 |
| tfidf_cosine | 0.80 | 0.98 | 0.97 | 0.48 | 0.94 | 0.90 |
| emb_minilm | 0.64 | 0.87 | 0.88 | 0.17 | 0.56 | 0.56 |
| emb_mpnet | 0.70 | 0.87 | 0.86 | 0.30 | 0.59 | 0.61 |
| emb_bge_large | 0.76 | 0.94 | 0.93 | 0.13 | 0.69 | 0.64 |
| emb_gte_large | 0.76 | 0.94 | 0.91 | 0.16 | 0.62 | 0.53 |
| emb_gemini_001 | 0.76 | 0.97 | 0.96 | 0.48 | 0.93 | 0.89 |
| cross_encoder | 0.75 | 0.81 | 0.84 | 0.19 | 0.34 | 0.41 |
| reranker_bge_large | 0.61 | 0.66 | 0.60 | 0.10 | 0.15 | 0.09 |
| entity_overlap | 0.63 | 0.99 | 0.97 | 0.19 | 0.95 | 0.86 |
| quote_overlap | 0.58 | 0.58 | 0.61 | 0.16 | 0.20 | 0.26 |
| ours_1_minus_novelty | 0.61 | 0.98 | 0.96 | 0.19 | 0.96 | 0.88 |
| hybrid_ours_plus_emb_gte_large | 0.75 | 0.98 | 0.96 | 0.21 | 0.94 | 0.82 |

## Rewrites by other models (same prompt) vs held-out independent reports

| detector | AUC phi4 | AUC llama3.2 | AUC gemini-2.5-flash |
|---|---|---|---|
| jaccard_5gram | 0.92 | 0.95 | 0.95 |
| tfidf_cosine | 0.98 | 0.97 | 0.98 |
| emb_minilm | 0.87 | 0.80 | 0.89 |
| emb_mpnet | 0.87 | 0.79 | 0.88 |
| emb_bge_large | 0.94 | 0.89 | 0.93 |
| emb_gte_large | 0.94 | 0.88 | 0.93 |
| emb_gemini_001 | 0.97 | 0.92 | 0.97 |
| cross_encoder | 0.81 | 0.82 | 0.82 |
| reranker_bge_large | 0.66 | 0.55 | 0.61 |
| entity_overlap | 0.99 | 0.98 | 0.99 |
| quote_overlap | 0.58 | 0.58 | 0.68 |
| ours_1_minus_novelty | 0.98 | 0.98 | 0.99 |
| hybrid_ours_plus_emb_gte_large | 0.98 | 0.97 | 0.98 |

Medians of each score:

|                                |   adaptive |   comparison |   comparison (confirmed) |   held_independent |   held_same_source |   rewrite |   rewrite_gemini-2.5-flash |   rewrite_llama3.2 |
|:-------------------------------|-----------:|-------------:|-------------------------:|-------------------:|-------------------:|----------:|---------------------------:|-------------------:|
| jaccard_5gram                  |       0.04 |         0    |                     0    |               0    |               0.05 |      0.04 |                       0.06 |               0.06 |
| tfidf_cosine                   |       0.63 |         0.16 |                     0.46 |               0.33 |               0.48 |      0.65 |                       0.69 |               0.66 |
| emb_minilm                     |       0.89 |         0.46 |                     0.84 |               0.79 |               0.83 |      0.89 |                       0.92 |               0.87 |
| emb_mpnet                      |       0.93 |         0.51 |                     0.88 |               0.84 |               0.9  |      0.93 |                       0.93 |               0.91 |
| emb_bge_large                  |       0.94 |         0.65 |                     0.86 |               0.84 |               0.89 |      0.94 |                       0.94 |               0.92 |
| emb_gte_large                  |       0.97 |         0.82 |                     0.94 |               0.93 |               0.96 |      0.98 |                       0.98 |               0.97 |
| emb_gemini_001                 |       0.96 |         0.83 |                     0.93 |               0.92 |               0.94 |      0.97 |                       0.97 |               0.96 |
| cross_encoder                  |       0.61 |         0.49 |                     0.54 |               0.52 |               0.59 |      0.6  |                       0.61 |               0.61 |
| reranker_bge_large             |       1    |         0.2  |                     0.82 |               0.98 |               1    |      1    |                       1    |               0.99 |
| entity_overlap                 |       0.74 |         0.14 |                     0.38 |               0.28 |               0.34 |      0.81 |                       0.8  |               0.77 |
| quote_overlap                  |       0    |         0    |                     0    |               0    |               0    |      0    |                       0    |               0    |
| ours_1_minus_novelty           |       0.69 |         0.14 |                     0.38 |               0.27 |               0.29 |      0.79 |                       0.75 |               0.73 |
| hybrid_ours_plus_emb_gte_large |       0.57 |         0.08 |                     0.22 |               0.19 |               0.27 |      0.71 |                       0.65 |               0.57 |