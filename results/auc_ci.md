# AUC with 95% bootstrap intervals

Stratified bootstrap (2000 resamples, seed 0), the same resamples for every detector. Difference = detector minus ours (ours_1_minus_novelty); paired interval.

## rewrites vs 11 confirmed (200 positives, 11 negatives)

| detector | AUC [95% CI] | difference to ours [95% CI] |
|---|---|---|
| jaccard_5gram | 0.72 [0.50, 0.92] | -0.25 [-0.48, -0.06] |
| tfidf_cosine | 0.93 [0.87, 0.97] | -0.05 [-0.10, -0.01] |
| emb_minilm | 0.70 [0.58, 0.81] | -0.28 [-0.40, -0.17] |
| emb_mpnet | 0.77 [0.65, 0.87] | -0.20 [-0.32, -0.11] |
| emb_bge_large | 0.88 [0.78, 0.96] | -0.10 [-0.19, -0.02] |
| emb_gte_large | 0.89 [0.77, 0.97] | -0.09 [-0.21, -0.01] |
| emb_gemini_001 | 0.94 [0.89, 0.97] | -0.04 [-0.09, -0.01] |
| cross_encoder | 0.80 [0.65, 0.93] | -0.17 [-0.33, -0.04] |
| reranker_bge_large | 0.77 [0.62, 0.89] | -0.20 [-0.36, -0.08] |
| entity_overlap | 0.98 [0.96, 1.00] | +0.01 [-0.00, +0.02] |
| quote_overlap | 0.52 [0.40, 0.62] | -0.45 [-0.58, -0.35] |
| ours_1_minus_novelty | 0.98 [0.96, 0.99] | - |
| hybrid_ours_plus_emb_gte_large | 0.97 [0.95, 0.99] | -0.00 [-0.03, +0.02] |

## adaptive vs 11 confirmed (200 positives, 11 negatives)

| detector | AUC [95% CI] | difference to ours [95% CI] |
|---|---|---|
| jaccard_5gram | 0.75 [0.53, 0.94] | -0.19 [-0.41, -0.00] |
| tfidf_cosine | 0.91 [0.84, 0.96] | -0.03 [-0.09, +0.01] |
| emb_minilm | 0.72 [0.60, 0.84] | -0.22 [-0.33, -0.11] |
| emb_mpnet | 0.77 [0.66, 0.87] | -0.17 [-0.28, -0.08] |
| emb_bge_large | 0.85 [0.74, 0.94] | -0.09 [-0.20, +0.00] |
| emb_gte_large | 0.84 [0.69, 0.94] | -0.10 [-0.26, +0.01] |
| emb_gemini_001 | 0.88 [0.82, 0.94] | -0.06 [-0.12, +0.01] |
| cross_encoder | 0.83 [0.68, 0.94] | -0.11 [-0.25, +0.00] |
| reranker_bge_large | 0.73 [0.57, 0.86] | -0.21 [-0.37, -0.08] |
| entity_overlap | 0.97 [0.94, 0.99] | +0.03 [+0.01, +0.04] |
| quote_overlap | 0.55 [0.41, 0.66] | -0.39 [-0.54, -0.27] |
| ours_1_minus_novelty | 0.94 [0.90, 0.97] | - |
| hybrid_ours_plus_emb_gte_large | 0.93 [0.87, 0.98] | -0.01 [-0.08, +0.04] |

## rewrites vs 100 held-out independent (200 positives, 100 negatives)

| detector | AUC [95% CI] | difference to ours [95% CI] |
|---|---|---|
| jaccard_5gram | 0.92 [0.88, 0.95] | -0.06 [-0.10, -0.03] |
| tfidf_cosine | 0.98 [0.96, 0.99] | -0.00 [-0.02, +0.01] |
| emb_minilm | 0.87 [0.82, 0.90] | -0.12 [-0.16, -0.08] |
| emb_mpnet | 0.87 [0.83, 0.91] | -0.11 [-0.15, -0.08] |
| emb_bge_large | 0.94 [0.91, 0.97] | -0.04 [-0.07, -0.02] |
| emb_gte_large | 0.94 [0.91, 0.96] | -0.04 [-0.07, -0.02] |
| emb_gemini_001 | 0.97 [0.96, 0.99] | -0.01 [-0.02, +0.01] |
| cross_encoder | 0.81 [0.76, 0.86] | -0.17 [-0.22, -0.12] |
| reranker_bge_large | 0.66 [0.59, 0.72] | -0.32 [-0.39, -0.26] |
| entity_overlap | 0.99 [0.97, 1.00] | +0.00 [-0.00, +0.01] |
| quote_overlap | 0.58 [0.54, 0.62] | -0.40 [-0.44, -0.36] |
| ours_1_minus_novelty | 0.98 [0.97, 1.00] | - |
| hybrid_ours_plus_emb_gte_large | 0.98 [0.97, 1.00] | +0.00 [-0.01, +0.01] |

## adaptive vs 100 held-out independent (200 positives, 100 negatives)

| detector | AUC [95% CI] | difference to ours [95% CI] |
|---|---|---|
| jaccard_5gram | 0.93 [0.90, 0.96] | -0.03 [-0.06, +0.00] |
| tfidf_cosine | 0.97 [0.95, 0.98] | +0.01 [-0.01, +0.03] |
| emb_minilm | 0.88 [0.84, 0.92] | -0.08 [-0.12, -0.04] |
| emb_mpnet | 0.86 [0.82, 0.90] | -0.10 [-0.14, -0.06] |
| emb_bge_large | 0.93 [0.89, 0.95] | -0.03 [-0.06, -0.00] |
| emb_gte_large | 0.91 [0.87, 0.94] | -0.05 [-0.09, -0.02] |
| emb_gemini_001 | 0.96 [0.93, 0.98] | -0.00 [-0.03, +0.02] |
| cross_encoder | 0.84 [0.79, 0.88] | -0.12 [-0.17, -0.08] |
| reranker_bge_large | 0.60 [0.53, 0.66] | -0.36 [-0.43, -0.30] |
| entity_overlap | 0.97 [0.95, 0.99] | +0.01 [+0.00, +0.02] |
| quote_overlap | 0.61 [0.57, 0.65] | -0.35 [-0.39, -0.31] |
| ours_1_minus_novelty | 0.96 [0.94, 0.98] | - |
| hybrid_ours_plus_emb_gte_large | 0.96 [0.94, 0.98] | +0.00 [-0.01, +0.02] |

## same-source vs 100 held-out independent (63 positives, 100 negatives)

| detector | AUC [95% CI] | difference to ours [95% CI] |
|---|---|---|
| jaccard_5gram | 0.90 [0.85, 0.95] | +0.29 [+0.20, +0.39] |
| tfidf_cosine | 0.80 [0.73, 0.87] | +0.20 [+0.12, +0.27] |
| emb_minilm | 0.64 [0.55, 0.73] | +0.04 [-0.06, +0.14] |
| emb_mpnet | 0.70 [0.61, 0.78] | +0.09 [-0.00, +0.18] |
| emb_bge_large | 0.76 [0.68, 0.83] | +0.15 [+0.05, +0.25] |
| emb_gte_large | 0.76 [0.68, 0.83] | +0.15 [+0.05, +0.25] |
| emb_gemini_001 | 0.76 [0.68, 0.84] | +0.16 [+0.06, +0.25] |
| cross_encoder | 0.75 [0.67, 0.82] | +0.14 [+0.03, +0.25] |
| reranker_bge_large | 0.61 [0.52, 0.70] | +0.00 [-0.10, +0.11] |
| entity_overlap | 0.63 [0.54, 0.71] | +0.02 [-0.00, +0.05] |
| quote_overlap | 0.58 [0.52, 0.64] | -0.02 [-0.12, +0.07] |
| ours_1_minus_novelty | 0.61 [0.52, 0.69] | - |
| hybrid_ours_plus_emb_gte_large | 0.75 [0.67, 0.82] | +0.14 [+0.07, +0.21] |
