# Judge experiment: three outcomes, paired tests

## Share True / False / abstain (abstain = Unsure or no verdict word), 95% Wilson interval for True

### lies, invented people

| judge | condition | n | True [95% CI] | False | abstain | of which no word |
|---|---|---|---|---|---|---|
| Llama 3.2 | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Llama 3.2 | copies1 | 80 | 0.06 [0.03, 0.14] | 0.94 | 0.00 | 0 |
| Llama 3.2 | copies3 | 80 | 0.71 [0.61, 0.80] | 0.29 | 0.00 | 0 |
| Llama 3.2 | copies5 | 80 | 0.55 [0.44, 0.65] | 0.45 | 0.00 | 0 |
| Llama 3.2 | copies10 | 80 | 0.44 [0.33, 0.55] | 0.56 | 0.00 | 0 |
| Llama 3.2 | indep3 | 80 | 0.34 [0.24, 0.45] | 0.66 | 0.00 | 0 |
| Llama 3.2 | filler3 | 80 | 0.40 [0.30, 0.51] | 0.60 | 0.00 | 0 |
| Llama 3.2 | labelled3 | 80 | 0.74 [0.63, 0.82] | 0.26 | 0.00 | 0 |
| Llama 3.2 | labelled10 | 80 | 0.51 [0.40, 0.62] | 0.49 | 0.00 | 0 |
| Llama 3.2 | none+unsure | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Llama 3.2 | copies1+unsure | 80 | 0.56 [0.45, 0.67] | 0.40 | 0.04 | 0 |
| Llama 3.2 | copies3+unsure | 80 | 0.99 [0.93, 1.00] | 0.01 | 0.00 | 0 |
| Llama 3.2 | indep3+unsure | 80 | 0.66 [0.55, 0.76] | 0.12 | 0.21 | 0 |
| Llama 3.2 | labelled3+unsure | 80 | 0.95 [0.88, 0.98] | 0.05 | 0.00 | 0 |
| Llama 3.2 | sameoutlet3 | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Llama 3.2 | copies3_falseindep | 80 | 0.75 [0.65, 0.83] | 0.25 | 0.00 | 0 |
| Llama 3.2 | paraphrase3_note | 80 | 0.57 [0.47, 0.68] | 0.42 | 0.00 | 0 |
| Llama 3.2 | copies3_table | 80 | 0.42 [0.32, 0.53] | 0.57 | 0.00 | 0 |
| Llama 3.2 | copies3_known | 80 | 0.69 [0.58, 0.78] | 0.31 | 0.00 | 0 |
| Llama 3.2 | indep3_known | 80 | 0.34 [0.24, 0.45] | 0.66 | 0.00 | 0 |
| phi4 | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| phi4 | copies1 | 80 | 0.21 [0.14, 0.31] | 0.79 | 0.00 | 0 |
| phi4 | copies3 | 80 | 0.90 [0.81, 0.95] | 0.10 | 0.00 | 0 |
| phi4 | copies5 | 80 | 0.78 [0.67, 0.85] | 0.23 | 0.00 | 0 |
| phi4 | copies10 | 80 | 0.50 [0.39, 0.61] | 0.33 | 0.17 | 14 |
| phi4 | indep3 | 80 | 0.97 [0.91, 0.99] | 0.03 | 0.00 | 0 |
| phi4 | filler3 | 80 | 0.93 [0.85, 0.97] | 0.07 | 0.00 | 0 |
| phi4 | labelled3 | 80 | 0.82 [0.73, 0.89] | 0.17 | 0.00 | 0 |
| phi4 | labelled10 | 80 | 0.57 [0.47, 0.68] | 0.42 | 0.00 | 0 |
| phi4 | none+unsure | 80 | 0.00 [-0.00, 0.05] | 0.01 | 0.99 | 0 |
| phi4 | copies1+unsure | 80 | 0.33 [0.23, 0.43] | 0.00 | 0.68 | 0 |
| phi4 | copies3+unsure | 80 | 0.96 [0.90, 0.99] | 0.00 | 0.04 | 0 |
| phi4 | indep3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| phi4 | labelled3+unsure | 80 | 0.88 [0.78, 0.93] | 0.00 | 0.12 | 0 |
| phi4 | sameoutlet3 | 80 | 0.62 [0.52, 0.72] | 0.38 | 0.00 | 0 |
| phi4 | copies3_falseindep | 80 | 0.84 [0.74, 0.90] | 0.16 | 0.00 | 0 |
| phi4 | paraphrase3_note | 80 | 0.99 [0.93, 1.00] | 0.01 | 0.00 | 0 |
| phi4 | copies3_table | 80 | 0.88 [0.78, 0.93] | 0.11 | 0.01 | 1 |
| phi4 | copies3_known | 80 | 0.55 [0.44, 0.65] | 0.42 | 0.03 | 2 |
| phi4 | indep3_known | 80 | 0.95 [0.88, 0.98] | 0.05 | 0.00 | 0 |
| Gemini Flash | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Gemini Flash | copies1 | 80 | 0.93 [0.85, 0.97] | 0.07 | 0.00 | 0 |
| Gemini Flash | copies3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies5 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies10 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | indep3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | filler3 | 80 | 0.97 [0.91, 0.99] | 0.03 | 0.00 | 0 |
| Gemini Flash | labelled3 | 80 | 0.79 [0.69, 0.86] | 0.21 | 0.00 | 0 |
| Gemini Flash | labelled10 | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| Gemini Flash | none+unsure | 80 | 0.00 [-0.00, 0.05] | 0.00 | 1.00 | 0 |
| Gemini Flash | copies1+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | indep3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | labelled3+unsure | 80 | 0.51 [0.40, 0.62] | 0.00 | 0.49 | 0 |
| Gemini Flash | sameoutlet3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies3_falseindep | 80 | 0.95 [0.88, 0.98] | 0.05 | 0.00 | 0 |
| Gemini Flash | paraphrase3_note | 80 | 0.97 [0.91, 0.99] | 0.03 | 0.00 | 0 |
| Gemini Flash | copies3_table | 80 | 0.49 [0.38, 0.60] | 0.51 | 0.00 | 0 |
| Gemini Flash | copies3_known | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | indep3_known | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Pro | none | 80 | 0.01 [0.00, 0.07] | 0.99 | 0.00 | 0 |
| Gemini Pro | copies1 | 80 | 0.64 [0.53, 0.73] | 0.35 | 0.01 | 1 |
| Gemini Pro | copies3 | 80 | 0.76 [0.66, 0.84] | 0.23 | 0.01 | 1 |
| Gemini Pro | copies5 | 80 | 0.86 [0.77, 0.92] | 0.14 | 0.00 | 0 |
| Gemini Pro | copies10 | 80 | 0.85 [0.76, 0.91] | 0.15 | 0.00 | 0 |
| Gemini Pro | indep3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Pro | filler3 | 80 | 0.99 [0.93, 1.00] | 0.01 | 0.00 | 0 |
| Gemini Pro | labelled3 | 80 | 0.00 [-0.00, 0.05] | 0.90 | 0.10 | 8 |
| Gemini Pro | labelled10 | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Gemini Pro | none+unsure | 80 | 0.00 [-0.00, 0.05] | 0.00 | 1.00 | 0 |
| Gemini Pro | copies1+unsure | 80 | 0.11 [0.06, 0.20] | 0.00 | 0.89 | 0 |
| Gemini Pro | copies3+unsure | 80 | 0.59 [0.48, 0.69] | 0.00 | 0.41 | 0 |
| Gemini Pro | indep3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Pro | labelled3+unsure | 80 | 0.00 [-0.00, 0.05] | 0.00 | 1.00 | 0 |
| Gemini Pro | sameoutlet3 | 80 | 0.61 [0.50, 0.71] | 0.39 | 0.00 | 0 |
| Gemini Pro | copies3_falseindep | 80 | 0.69 [0.58, 0.78] | 0.29 | 0.03 | 2 |
| Gemini Pro | paraphrase3_note | 80 | 0.36 [0.27, 0.47] | 0.42 | 0.21 | 17 |
| Gemini Pro | copies3_table | 80 | 0.01 [0.00, 0.07] | 0.99 | 0.00 | 0 |
| Gemini Pro | copies3_known | 80 | 0.50 [0.39, 0.61] | 0.49 | 0.01 | 1 |
| Gemini Pro | indep3_known | 80 | 0.97 [0.91, 0.99] | 0.03 | 0.00 | 0 |

### lies, known facts

| judge | condition | n | True [95% CI] | False | abstain | of which no word |
|---|---|---|---|---|---|---|
| Llama 3.2 | none | 80 | 0.01 [0.00, 0.07] | 0.99 | 0.00 | 0 |
| Llama 3.2 | copies1 | 80 | 0.09 [0.04, 0.17] | 0.91 | 0.00 | 0 |
| Llama 3.2 | copies3 | 80 | 0.14 [0.08, 0.23] | 0.86 | 0.00 | 0 |
| Llama 3.2 | copies5 | 80 | 0.07 [0.03, 0.15] | 0.91 | 0.01 | 1 |
| Llama 3.2 | copies10 | 80 | 0.01 [0.00, 0.07] | 0.97 | 0.01 | 1 |
| Llama 3.2 | indep3 | 80 | 0.10 [0.05, 0.19] | 0.89 | 0.01 | 1 |
| Llama 3.2 | filler3 | 80 | 0.34 [0.24, 0.45] | 0.66 | 0.00 | 0 |
| Llama 3.2 | labelled3 | 80 | 0.17 [0.11, 0.27] | 0.82 | 0.00 | 0 |
| Llama 3.2 | labelled10 | 80 | 0.04 [0.01, 0.10] | 0.96 | 0.00 | 0 |
| Llama 3.2 | none+unsure | 80 | 0.04 [0.01, 0.10] | 0.96 | 0.00 | 0 |
| Llama 3.2 | copies1+unsure | 80 | 0.38 [0.28, 0.48] | 0.61 | 0.01 | 0 |
| Llama 3.2 | copies3+unsure | 80 | 0.59 [0.48, 0.69] | 0.38 | 0.04 | 0 |
| Llama 3.2 | indep3+unsure | 80 | 0.41 [0.31, 0.52] | 0.50 | 0.09 | 0 |
| Llama 3.2 | labelled3+unsure | 80 | 0.46 [0.36, 0.57] | 0.54 | 0.00 | 0 |
| Llama 3.2 | sameoutlet3 | 80 | 0.05 [0.02, 0.12] | 0.95 | 0.00 | 0 |
| Llama 3.2 | copies3_falseindep | 80 | 0.15 [0.09, 0.24] | 0.85 | 0.00 | 0 |
| Llama 3.2 | paraphrase3_note | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| Llama 3.2 | copies3_table | 80 | 0.05 [0.02, 0.12] | 0.95 | 0.00 | 0 |
| Llama 3.2 | copies3_known | 80 | 0.19 [0.12, 0.29] | 0.81 | 0.00 | 0 |
| Llama 3.2 | indep3_known | 80 | 0.10 [0.05, 0.19] | 0.90 | 0.00 | 0 |
| phi4 | none | 80 | 0.07 [0.03, 0.15] | 0.93 | 0.00 | 0 |
| phi4 | copies1 | 80 | 0.10 [0.05, 0.19] | 0.90 | 0.00 | 0 |
| phi4 | copies3 | 80 | 0.24 [0.16, 0.34] | 0.76 | 0.00 | 0 |
| phi4 | copies5 | 80 | 0.25 [0.17, 0.35] | 0.75 | 0.00 | 0 |
| phi4 | copies10 | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| phi4 | indep3 | 80 | 0.25 [0.17, 0.35] | 0.75 | 0.00 | 0 |
| phi4 | filler3 | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |
| phi4 | labelled3 | 80 | 0.21 [0.14, 0.31] | 0.79 | 0.00 | 0 |
| phi4 | labelled10 | 80 | 0.20 [0.13, 0.30] | 0.79 | 0.01 | 1 |
| phi4 | none+unsure | 80 | 0.05 [0.02, 0.12] | 0.75 | 0.20 | 0 |
| phi4 | copies1+unsure | 80 | 0.11 [0.06, 0.20] | 0.62 | 0.26 | 0 |
| phi4 | copies3+unsure | 80 | 0.25 [0.17, 0.35] | 0.54 | 0.21 | 0 |
| phi4 | indep3+unsure | 80 | 0.34 [0.24, 0.45] | 0.54 | 0.12 | 0 |
| phi4 | labelled3+unsure | 80 | 0.23 [0.15, 0.33] | 0.51 | 0.26 | 0 |
| phi4 | sameoutlet3 | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| phi4 | copies3_falseindep | 80 | 0.25 [0.17, 0.35] | 0.75 | 0.00 | 0 |
| phi4 | paraphrase3_note | 80 | 0.25 [0.17, 0.35] | 0.75 | 0.00 | 0 |
| phi4 | copies3_table | 80 | 0.25 [0.17, 0.35] | 0.75 | 0.00 | 0 |
| phi4 | copies3_known | 80 | 0.17 [0.11, 0.27] | 0.82 | 0.00 | 0 |
| phi4 | indep3_known | 80 | 0.21 [0.14, 0.31] | 0.79 | 0.00 | 0 |
| Gemini Flash | none | 80 | 0.06 [0.03, 0.14] | 0.94 | 0.00 | 0 |
| Gemini Flash | copies1 | 80 | 0.15 [0.09, 0.24] | 0.85 | 0.00 | 0 |
| Gemini Flash | copies3 | 80 | 0.31 [0.22, 0.42] | 0.69 | 0.00 | 0 |
| Gemini Flash | copies5 | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |
| Gemini Flash | copies10 | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |
| Gemini Flash | indep3 | 80 | 0.51 [0.40, 0.62] | 0.49 | 0.00 | 0 |
| Gemini Flash | filler3 | 80 | 0.30 [0.21, 0.41] | 0.70 | 0.00 | 0 |
| Gemini Flash | labelled3 | 80 | 0.16 [0.10, 0.26] | 0.84 | 0.00 | 0 |
| Gemini Flash | labelled10 | 80 | 0.09 [0.04, 0.17] | 0.91 | 0.00 | 0 |
| Gemini Flash | none+unsure | 80 | 0.04 [0.01, 0.10] | 0.75 | 0.21 | 0 |
| Gemini Flash | copies1+unsure | 80 | 0.21 [0.14, 0.31] | 0.59 | 0.20 | 0 |
| Gemini Flash | copies3+unsure | 80 | 0.50 [0.39, 0.61] | 0.46 | 0.04 | 0 |
| Gemini Flash | indep3+unsure | 80 | 0.68 [0.57, 0.77] | 0.29 | 0.04 | 0 |
| Gemini Flash | labelled3+unsure | 80 | 0.16 [0.10, 0.26] | 0.54 | 0.30 | 0 |
| Gemini Flash | sameoutlet3 | 80 | 0.35 [0.25, 0.46] | 0.65 | 0.00 | 0 |
| Gemini Flash | copies3_falseindep | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |
| Gemini Flash | paraphrase3_note | 80 | 0.28 [0.19, 0.38] | 0.72 | 0.00 | 0 |
| Gemini Flash | copies3_table | 80 | 0.12 [0.07, 0.22] | 0.88 | 0.00 | 0 |
| Gemini Flash | copies3_known | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |
| Gemini Flash | indep3_known | 80 | 0.36 [0.27, 0.47] | 0.64 | 0.00 | 0 |
| Gemini Pro | none | 80 | 0.06 [0.03, 0.14] | 0.94 | 0.00 | 0 |
| Gemini Pro | copies1 | 80 | 0.12 [0.07, 0.22] | 0.88 | 0.00 | 0 |
| Gemini Pro | copies3 | 80 | 0.16 [0.10, 0.26] | 0.84 | 0.00 | 0 |
| Gemini Pro | copies5 | 80 | 0.17 [0.11, 0.27] | 0.82 | 0.00 | 0 |
| Gemini Pro | copies10 | 80 | 0.16 [0.10, 0.26] | 0.84 | 0.00 | 0 |
| Gemini Pro | indep3 | 80 | 0.31 [0.22, 0.42] | 0.69 | 0.00 | 0 |
| Gemini Pro | filler3 | 80 | 0.30 [0.21, 0.41] | 0.70 | 0.00 | 0 |
| Gemini Pro | labelled3 | 80 | 0.01 [0.00, 0.07] | 0.94 | 0.05 | 4 |
| Gemini Pro | labelled10 | 80 | 0.01 [0.00, 0.07] | 0.99 | 0.00 | 0 |
| Gemini Pro | none+unsure | 80 | 0.05 [0.02, 0.12] | 0.76 | 0.19 | 0 |
| Gemini Pro | copies1+unsure | 80 | 0.09 [0.04, 0.17] | 0.60 | 0.31 | 0 |
| Gemini Pro | copies3+unsure | 80 | 0.12 [0.07, 0.22] | 0.53 | 0.35 | 0 |
| Gemini Pro | indep3+unsure | 80 | 0.28 [0.19, 0.38] | 0.45 | 0.28 | 0 |
| Gemini Pro | labelled3+unsure | 80 | 0.01 [0.00, 0.07] | 0.36 | 0.62 | 0 |
| Gemini Pro | sameoutlet3 | 80 | 0.12 [0.07, 0.22] | 0.86 | 0.01 | 1 |
| Gemini Pro | copies3_falseindep | 80 | 0.21 [0.14, 0.31] | 0.79 | 0.00 | 0 |
| Gemini Pro | paraphrase3_note | 80 | 0.12 [0.07, 0.22] | 0.86 | 0.01 | 1 |
| Gemini Pro | copies3_table | 80 | 0.01 [0.00, 0.07] | 0.99 | 0.00 | 0 |
| Gemini Pro | copies3_known | 80 | 0.19 [0.12, 0.29] | 0.80 | 0.01 | 1 |
| Gemini Pro | indep3_known | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |

### truths, invented people

| judge | condition | n | True [95% CI] | False | abstain | of which no word |
|---|---|---|---|---|---|---|
| Llama 3.2 | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Llama 3.2 | copies1 | 80 | 0.05 [0.02, 0.12] | 0.95 | 0.00 | 0 |
| Llama 3.2 | copies3 | 80 | 0.64 [0.53, 0.73] | 0.36 | 0.00 | 0 |
| Llama 3.2 | copies5 | 80 | 0.46 [0.36, 0.57] | 0.54 | 0.00 | 0 |
| Llama 3.2 | copies10 | 80 | 0.34 [0.24, 0.45] | 0.66 | 0.00 | 0 |
| Llama 3.2 | indep3 | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |
| Llama 3.2 | filler3 | 80 | 0.39 [0.29, 0.50] | 0.61 | 0.00 | 0 |
| Llama 3.2 | labelled3 | 80 | 0.70 [0.59, 0.79] | 0.30 | 0.00 | 0 |
| Llama 3.2 | labelled10 | 80 | 0.41 [0.31, 0.52] | 0.59 | 0.00 | 0 |
| Llama 3.2 | none+unsure | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Llama 3.2 | copies1+unsure | 80 | 0.65 [0.54, 0.75] | 0.35 | 0.00 | 0 |
| Llama 3.2 | copies3+unsure | 80 | 0.97 [0.91, 0.99] | 0.01 | 0.01 | 0 |
| Llama 3.2 | indep3+unsure | 80 | 0.68 [0.57, 0.77] | 0.15 | 0.17 | 0 |
| Llama 3.2 | labelled3+unsure | 80 | 0.95 [0.88, 0.98] | 0.05 | 0.00 | 0 |
| Llama 3.2 | sameoutlet3 | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Llama 3.2 | copies3_falseindep | 80 | 0.75 [0.65, 0.83] | 0.25 | 0.00 | 0 |
| Llama 3.2 | paraphrase3_note | 80 | 0.59 [0.48, 0.69] | 0.41 | 0.00 | 0 |
| Llama 3.2 | copies3_table | 80 | 0.35 [0.25, 0.46] | 0.65 | 0.00 | 0 |
| Llama 3.2 | copies3_known | 80 | 0.61 [0.50, 0.71] | 0.39 | 0.00 | 0 |
| Llama 3.2 | indep3_known | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| phi4 | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| phi4 | copies1 | 80 | 0.25 [0.17, 0.35] | 0.75 | 0.00 | 0 |
| phi4 | copies3 | 80 | 0.88 [0.78, 0.93] | 0.12 | 0.00 | 0 |
| phi4 | copies5 | 80 | 0.79 [0.69, 0.86] | 0.19 | 0.03 | 2 |
| phi4 | copies10 | 80 | 0.53 [0.42, 0.63] | 0.34 | 0.14 | 11 |
| phi4 | indep3 | 80 | 0.99 [0.93, 1.00] | 0.01 | 0.00 | 0 |
| phi4 | filler3 | 80 | 0.94 [0.86, 0.97] | 0.03 | 0.04 | 3 |
| phi4 | labelled3 | 80 | 0.81 [0.71, 0.88] | 0.19 | 0.00 | 0 |
| phi4 | labelled10 | 80 | 0.56 [0.45, 0.67] | 0.42 | 0.01 | 1 |
| phi4 | none+unsure | 80 | 0.00 [-0.00, 0.05] | 0.00 | 1.00 | 0 |
| phi4 | copies1+unsure | 80 | 0.31 [0.22, 0.42] | 0.00 | 0.69 | 0 |
| phi4 | copies3+unsure | 80 | 0.99 [0.93, 1.00] | 0.00 | 0.01 | 0 |
| phi4 | indep3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| phi4 | labelled3+unsure | 80 | 0.88 [0.78, 0.93] | 0.00 | 0.12 | 0 |
| phi4 | sameoutlet3 | 80 | 0.70 [0.59, 0.79] | 0.30 | 0.00 | 0 |
| phi4 | copies3_falseindep | 80 | 0.86 [0.77, 0.92] | 0.14 | 0.00 | 0 |
| phi4 | paraphrase3_note | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| phi4 | copies3_table | 80 | 0.94 [0.86, 0.97] | 0.06 | 0.00 | 0 |
| phi4 | copies3_known | 80 | 0.61 [0.50, 0.71] | 0.39 | 0.00 | 0 |
| phi4 | indep3_known | 80 | 0.96 [0.90, 0.99] | 0.04 | 0.00 | 0 |
| Gemini Flash | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Gemini Flash | copies1 | 80 | 0.99 [0.93, 1.00] | 0.01 | 0.00 | 0 |
| Gemini Flash | copies3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies5 | 80 | 0.99 [0.93, 1.00] | 0.01 | 0.00 | 0 |
| Gemini Flash | copies10 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | indep3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | filler3 | 80 | 0.99 [0.93, 1.00] | 0.01 | 0.00 | 0 |
| Gemini Flash | labelled3 | 80 | 0.68 [0.57, 0.77] | 0.33 | 0.00 | 0 |
| Gemini Flash | labelled10 | 80 | 0.31 [0.22, 0.42] | 0.69 | 0.00 | 0 |
| Gemini Flash | none+unsure | 80 | 0.00 [-0.00, 0.05] | 0.00 | 1.00 | 0 |
| Gemini Flash | copies1+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | indep3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | labelled3+unsure | 80 | 0.36 [0.27, 0.47] | 0.00 | 0.64 | 0 |
| Gemini Flash | sameoutlet3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies3_falseindep | 80 | 0.94 [0.86, 0.97] | 0.06 | 0.00 | 0 |
| Gemini Flash | paraphrase3_note | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | copies3_table | 80 | 0.56 [0.45, 0.67] | 0.44 | 0.00 | 0 |
| Gemini Flash | copies3_known | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Flash | indep3_known | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Pro | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Gemini Pro | copies1 | 80 | 0.69 [0.58, 0.78] | 0.31 | 0.00 | 0 |
| Gemini Pro | copies3 | 80 | 0.84 [0.74, 0.90] | 0.15 | 0.01 | 1 |
| Gemini Pro | copies5 | 80 | 0.90 [0.81, 0.95] | 0.10 | 0.00 | 0 |
| Gemini Pro | copies10 | 80 | 0.90 [0.81, 0.95] | 0.10 | 0.00 | 0 |
| Gemini Pro | indep3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Pro | filler3 | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Pro | labelled3 | 80 | 0.00 [-0.00, 0.05] | 0.85 | 0.15 | 12 |
| Gemini Pro | labelled10 | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Gemini Pro | none+unsure | 80 | 0.00 [-0.00, 0.05] | 0.00 | 1.00 | 0 |
| Gemini Pro | copies1+unsure | 80 | 0.12 [0.07, 0.22] | 0.00 | 0.88 | 0 |
| Gemini Pro | copies3+unsure | 80 | 0.62 [0.52, 0.72] | 0.00 | 0.38 | 0 |
| Gemini Pro | indep3+unsure | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |
| Gemini Pro | labelled3+unsure | 80 | 0.00 [-0.00, 0.05] | 0.00 | 1.00 | 0 |
| Gemini Pro | sameoutlet3 | 80 | 0.74 [0.63, 0.82] | 0.26 | 0.00 | 0 |
| Gemini Pro | copies3_falseindep | 80 | 0.82 [0.73, 0.89] | 0.15 | 0.03 | 2 |
| Gemini Pro | paraphrase3_note | 80 | 0.49 [0.38, 0.60] | 0.36 | 0.15 | 12 |
| Gemini Pro | copies3_table | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Gemini Pro | copies3_known | 80 | 0.71 [0.61, 0.80] | 0.29 | 0.00 | 0 |
| Gemini Pro | indep3_known | 80 | 1.00 [0.95, 1.00] | 0.00 | 0.00 | 0 |

### updates, known facts

| judge | condition | n | True [95% CI] | False | abstain | of which no word |
|---|---|---|---|---|---|---|
| Llama 3.2 | none | 80 | 0.00 [-0.00, 0.05] | 1.00 | 0.00 | 0 |
| Llama 3.2 | copies1 | 80 | 0.03 [0.01, 0.09] | 0.97 | 0.00 | 0 |
| Llama 3.2 | copies3 | 80 | 0.24 [0.16, 0.34] | 0.76 | 0.00 | 0 |
| Llama 3.2 | copies5 | 80 | 0.10 [0.05, 0.19] | 0.90 | 0.00 | 0 |
| Llama 3.2 | copies10 | 80 | 0.03 [0.01, 0.09] | 0.97 | 0.00 | 0 |
| Llama 3.2 | indep3 | 80 | 0.11 [0.06, 0.20] | 0.89 | 0.00 | 0 |
| Llama 3.2 | filler3 | 80 | 0.41 [0.31, 0.52] | 0.59 | 0.00 | 0 |
| Llama 3.2 | labelled3 | 80 | 0.24 [0.16, 0.34] | 0.76 | 0.00 | 0 |
| Llama 3.2 | labelled10 | 80 | 0.07 [0.03, 0.15] | 0.93 | 0.00 | 0 |
| Llama 3.2 | none+unsure | 80 | 0.03 [0.01, 0.09] | 0.97 | 0.00 | 0 |
| Llama 3.2 | copies1+unsure | 80 | 0.34 [0.24, 0.45] | 0.65 | 0.01 | 0 |
| Llama 3.2 | copies3+unsure | 80 | 0.54 [0.43, 0.64] | 0.38 | 0.09 | 0 |
| Llama 3.2 | indep3+unsure | 80 | 0.46 [0.36, 0.57] | 0.44 | 0.10 | 0 |
| Llama 3.2 | labelled3+unsure | 80 | 0.49 [0.38, 0.60] | 0.51 | 0.00 | 0 |
| Llama 3.2 | sameoutlet3 | 80 | 0.09 [0.04, 0.17] | 0.91 | 0.00 | 0 |
| Llama 3.2 | copies3_falseindep | 80 | 0.17 [0.11, 0.27] | 0.82 | 0.00 | 0 |
| Llama 3.2 | paraphrase3_note | 80 | 0.23 [0.15, 0.33] | 0.78 | 0.00 | 0 |
| Llama 3.2 | copies3_table | 80 | 0.06 [0.03, 0.14] | 0.94 | 0.00 | 0 |
| Llama 3.2 | copies3_known | 80 | 0.24 [0.16, 0.34] | 0.76 | 0.00 | 0 |
| Llama 3.2 | indep3_known | 80 | 0.11 [0.06, 0.20] | 0.89 | 0.00 | 0 |
| phi4 | none | 80 | 0.05 [0.02, 0.12] | 0.95 | 0.00 | 0 |
| phi4 | copies1 | 80 | 0.07 [0.03, 0.15] | 0.93 | 0.00 | 0 |
| phi4 | copies3 | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| phi4 | copies5 | 80 | 0.16 [0.10, 0.26] | 0.84 | 0.00 | 0 |
| phi4 | copies10 | 80 | 0.14 [0.08, 0.23] | 0.85 | 0.01 | 1 |
| phi4 | indep3 | 80 | 0.28 [0.19, 0.38] | 0.72 | 0.00 | 0 |
| phi4 | filler3 | 80 | 0.33 [0.23, 0.43] | 0.66 | 0.01 | 1 |
| phi4 | labelled3 | 80 | 0.17 [0.11, 0.27] | 0.82 | 0.00 | 0 |
| phi4 | labelled10 | 80 | 0.14 [0.08, 0.23] | 0.85 | 0.01 | 1 |
| phi4 | none+unsure | 80 | 0.06 [0.03, 0.14] | 0.74 | 0.20 | 0 |
| phi4 | copies1+unsure | 80 | 0.07 [0.03, 0.15] | 0.60 | 0.33 | 0 |
| phi4 | copies3+unsure | 80 | 0.30 [0.21, 0.41] | 0.44 | 0.26 | 0 |
| phi4 | indep3+unsure | 80 | 0.41 [0.31, 0.52] | 0.50 | 0.09 | 0 |
| phi4 | labelled3+unsure | 80 | 0.26 [0.18, 0.37] | 0.41 | 0.33 | 0 |
| phi4 | sameoutlet3 | 80 | 0.14 [0.08, 0.23] | 0.86 | 0.00 | 0 |
| phi4 | copies3_falseindep | 80 | 0.23 [0.15, 0.33] | 0.78 | 0.00 | 0 |
| phi4 | paraphrase3_note | 80 | 0.29 [0.20, 0.39] | 0.71 | 0.00 | 0 |
| phi4 | copies3_table | 80 | 0.26 [0.18, 0.37] | 0.74 | 0.00 | 0 |
| phi4 | copies3_known | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| phi4 | indep3_known | 80 | 0.24 [0.16, 0.34] | 0.76 | 0.00 | 0 |
| Gemini Flash | none | 80 | 0.06 [0.03, 0.14] | 0.94 | 0.00 | 0 |
| Gemini Flash | copies1 | 80 | 0.20 [0.13, 0.30] | 0.80 | 0.00 | 0 |
| Gemini Flash | copies3 | 80 | 0.39 [0.29, 0.50] | 0.61 | 0.00 | 0 |
| Gemini Flash | copies5 | 80 | 0.34 [0.24, 0.45] | 0.66 | 0.00 | 0 |
| Gemini Flash | copies10 | 80 | 0.29 [0.20, 0.39] | 0.71 | 0.00 | 0 |
| Gemini Flash | indep3 | 80 | 0.53 [0.42, 0.63] | 0.47 | 0.00 | 0 |
| Gemini Flash | filler3 | 80 | 0.42 [0.32, 0.53] | 0.57 | 0.00 | 0 |
| Gemini Flash | labelled3 | 80 | 0.17 [0.11, 0.27] | 0.82 | 0.00 | 0 |
| Gemini Flash | labelled10 | 80 | 0.10 [0.05, 0.19] | 0.90 | 0.00 | 0 |
| Gemini Flash | none+unsure | 80 | 0.05 [0.02, 0.12] | 0.78 | 0.17 | 0 |
| Gemini Flash | copies1+unsure | 80 | 0.30 [0.21, 0.41] | 0.51 | 0.19 | 0 |
| Gemini Flash | copies3+unsure | 80 | 0.56 [0.45, 0.67] | 0.39 | 0.05 | 0 |
| Gemini Flash | indep3+unsure | 80 | 0.71 [0.61, 0.80] | 0.24 | 0.05 | 0 |
| Gemini Flash | labelled3+unsure | 80 | 0.19 [0.12, 0.29] | 0.41 | 0.40 | 0 |
| Gemini Flash | sameoutlet3 | 80 | 0.44 [0.33, 0.55] | 0.56 | 0.00 | 0 |
| Gemini Flash | copies3_falseindep | 80 | 0.30 [0.21, 0.41] | 0.70 | 0.00 | 0 |
| Gemini Flash | paraphrase3_note | 80 | 0.38 [0.28, 0.48] | 0.62 | 0.00 | 0 |
| Gemini Flash | copies3_table | 80 | 0.15 [0.09, 0.24] | 0.85 | 0.00 | 0 |
| Gemini Flash | copies3_known | 80 | 0.31 [0.22, 0.42] | 0.69 | 0.00 | 0 |
| Gemini Flash | indep3_known | 80 | 0.46 [0.36, 0.57] | 0.54 | 0.00 | 0 |
| Gemini Pro | none | 80 | 0.06 [0.03, 0.14] | 0.94 | 0.00 | 0 |
| Gemini Pro | copies1 | 80 | 0.09 [0.04, 0.17] | 0.91 | 0.00 | 0 |
| Gemini Pro | copies3 | 80 | 0.11 [0.06, 0.20] | 0.89 | 0.00 | 0 |
| Gemini Pro | copies5 | 80 | 0.14 [0.08, 0.23] | 0.86 | 0.00 | 0 |
| Gemini Pro | copies10 | 80 | 0.11 [0.06, 0.20] | 0.89 | 0.00 | 0 |
| Gemini Pro | indep3 | 80 | 0.41 [0.31, 0.52] | 0.59 | 0.00 | 0 |
| Gemini Pro | filler3 | 80 | 0.38 [0.28, 0.48] | 0.62 | 0.00 | 0 |
| Gemini Pro | labelled3 | 80 | 0.03 [0.01, 0.09] | 0.95 | 0.03 | 2 |
| Gemini Pro | labelled10 | 80 | 0.01 [0.00, 0.07] | 0.99 | 0.00 | 0 |
| Gemini Pro | none+unsure | 80 | 0.04 [0.01, 0.10] | 0.78 | 0.19 | 0 |
| Gemini Pro | copies1+unsure | 80 | 0.06 [0.03, 0.14] | 0.57 | 0.36 | 0 |
| Gemini Pro | copies3+unsure | 80 | 0.10 [0.05, 0.19] | 0.31 | 0.59 | 0 |
| Gemini Pro | indep3+unsure | 80 | 0.42 [0.32, 0.53] | 0.38 | 0.20 | 0 |
| Gemini Pro | labelled3+unsure | 80 | 0.01 [0.00, 0.07] | 0.25 | 0.74 | 0 |
| Gemini Pro | sameoutlet3 | 80 | 0.14 [0.08, 0.23] | 0.86 | 0.00 | 0 |
| Gemini Pro | copies3_falseindep | 80 | 0.23 [0.15, 0.33] | 0.78 | 0.00 | 0 |
| Gemini Pro | paraphrase3_note | 80 | 0.07 [0.03, 0.15] | 0.86 | 0.06 | 5 |
| Gemini Pro | copies3_table | 80 | 0.01 [0.00, 0.07] | 0.99 | 0.00 | 0 |
| Gemini Pro | copies3_known | 80 | 0.15 [0.09, 0.24] | 0.85 | 0.00 | 0 |
| Gemini Pro | indep3_known | 80 | 0.31 [0.22, 0.42] | 0.69 | 0.00 | 0 |

## Paired tests on the same claims (exact McNemar; Holm-adjusted over all rows)

| lies | judge | contrast | n | change in share True | claims flipped to True | flipped to not-True | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| lies, invented people | Llama 3.2 | copies1 -> copies3 | 80 | +0.65 | 52 | 0 | 4.4e-16 | 4.7e-14 |
| lies, invented people | Llama 3.2 | copies3 -> indep3 | 80 | -0.38 | 1 | 31 | 1.5e-08 | 1.5e-06 |
| lies, invented people | Llama 3.2 | copies3 -> labelled3 | 80 | +0.03 | 5 | 3 | 0.73 | 1 |
| lies, invented people | Llama 3.2 | copies3 -> filler3 | 80 | -0.31 | 2 | 27 | 1.6e-06 | 0.00015 |
| lies, invented people | Llama 3.2 | copies3 -> copies10 | 80 | -0.28 | 0 | 22 | 4.8e-07 | 4.6e-05 |
| lies, invented people | Llama 3.2 | copies10 -> labelled10 | 80 | +0.07 | 9 | 3 | 0.15 | 1 |
| lies, invented people | Llama 3.2 | copies3 -> sameoutlet3 | 80 | -0.71 | 0 | 57 | 1.4e-17 | 1.5e-15 |
| lies, invented people | Llama 3.2 | copies1 -> sameoutlet3 | 80 | -0.06 | 0 | 5 | 0.062 | 1 |
| lies, invented people | Llama 3.2 | copies3 -> copies3_falseindep | 80 | +0.04 | 5 | 2 | 0.45 | 1 |
| lies, invented people | Llama 3.2 | indep3 -> paraphrase3_note | 80 | +0.24 | 19 | 0 | 3.8e-06 | 0.00036 |
| lies, invented people | Llama 3.2 | copies3 -> copies3_table | 80 | -0.29 | 0 | 23 | 2.4e-07 | 2.3e-05 |
| lies, invented people | Llama 3.2 | labelled3 -> copies3_table | 80 | -0.31 | 0 | 25 | 6e-08 | 5.9e-06 |
| lies, invented people | Llama 3.2 | copies3 -> copies3_known | 80 | -0.03 | 4 | 6 | 0.75 | 1 |
| lies, invented people | Llama 3.2 | indep3 -> indep3_known | 80 | +0.00 | 3 | 3 | 1 | 1 |
| lies, invented people | phi4 | copies1 -> copies3 | 80 | +0.69 | 55 | 0 | 5.6e-17 | 5.9e-15 |
| lies, invented people | phi4 | copies3 -> indep3 | 80 | +0.07 | 6 | 0 | 0.031 | 1 |
| lies, invented people | phi4 | copies3 -> labelled3 | 80 | -0.08 | 0 | 6 | 0.031 | 1 |
| lies, invented people | phi4 | copies3 -> filler3 | 80 | +0.03 | 5 | 3 | 0.73 | 1 |
| lies, invented people | phi4 | copies3 -> copies10 | 80 | -0.40 | 0 | 32 | 4.7e-10 | 4.8e-08 |
| lies, invented people | phi4 | copies10 -> labelled10 | 80 | +0.07 | 9 | 3 | 0.15 | 1 |
| lies, invented people | phi4 | copies3 -> sameoutlet3 | 80 | -0.28 | 0 | 22 | 4.8e-07 | 4.6e-05 |
| lies, invented people | phi4 | copies1 -> sameoutlet3 | 80 | +0.41 | 34 | 1 | 2.1e-09 | 2.1e-07 |
| lies, invented people | phi4 | copies3 -> copies3_falseindep | 80 | -0.06 | 1 | 6 | 0.12 | 1 |
| lies, invented people | phi4 | indep3 -> paraphrase3_note | 80 | +0.01 | 1 | 0 | 1 | 1 |
| lies, invented people | phi4 | copies3 -> copies3_table | 80 | -0.03 | 2 | 4 | 0.69 | 1 |
| lies, invented people | phi4 | labelled3 -> copies3_table | 80 | +0.05 | 4 | 0 | 0.12 | 1 |
| lies, invented people | phi4 | copies3 -> copies3_known | 80 | -0.35 | 0 | 28 | 7.5e-09 | 7.5e-07 |
| lies, invented people | phi4 | indep3 -> indep3_known | 80 | -0.03 | 0 | 2 | 0.5 | 1 |
| lies, invented people | Gemini Flash | copies1 -> copies3 | 80 | +0.07 | 6 | 0 | 0.031 | 1 |
| lies, invented people | Gemini Flash | copies3 -> indep3 | 80 | +0.00 | 0 | 0 | 1 | 1 |
| lies, invented people | Gemini Flash | copies3 -> labelled3 | 80 | -0.21 | 0 | 17 | 1.5e-05 | 0.0014 |
| lies, invented people | Gemini Flash | copies3 -> filler3 | 80 | -0.03 | 0 | 2 | 0.5 | 1 |
| lies, invented people | Gemini Flash | copies3 -> copies10 | 80 | +0.00 | 0 | 0 | 1 | 1 |
| lies, invented people | Gemini Flash | copies10 -> labelled10 | 80 | -0.80 | 0 | 64 | 1.1e-19 | 1.2e-17 |
| lies, invented people | Gemini Flash | copies3 -> sameoutlet3 | 80 | +0.00 | 0 | 0 | 1 | 1 |
| lies, invented people | Gemini Flash | copies1 -> sameoutlet3 | 80 | +0.07 | 6 | 0 | 0.031 | 1 |
| lies, invented people | Gemini Flash | copies3 -> copies3_falseindep | 80 | -0.05 | 0 | 4 | 0.12 | 1 |
| lies, invented people | Gemini Flash | indep3 -> paraphrase3_note | 80 | -0.03 | 0 | 2 | 0.5 | 1 |
| lies, invented people | Gemini Flash | copies3 -> copies3_table | 80 | -0.51 | 0 | 41 | 9.1e-13 | 9.5e-11 |
| lies, invented people | Gemini Flash | labelled3 -> copies3_table | 80 | -0.30 | 5 | 29 | 3.9e-05 | 0.0035 |
| lies, invented people | Gemini Flash | copies3 -> copies3_known | 80 | +0.00 | 0 | 0 | 1 | 1 |
| lies, invented people | Gemini Flash | indep3 -> indep3_known | 80 | +0.00 | 0 | 0 | 1 | 1 |
| lies, invented people | Gemini Pro | copies1 -> copies3 | 80 | +0.12 | 22 | 12 | 0.12 | 1 |
| lies, invented people | Gemini Pro | copies3 -> indep3 | 80 | +0.24 | 19 | 0 | 3.8e-06 | 0.00036 |
| lies, invented people | Gemini Pro | copies3 -> labelled3 | 80 | -0.76 | 0 | 61 | 8.7e-19 | 9.5e-17 |
| lies, invented people | Gemini Pro | copies3 -> filler3 | 80 | +0.23 | 19 | 1 | 4e-05 | 0.0036 |
| lies, invented people | Gemini Pro | copies3 -> copies10 | 80 | +0.09 | 11 | 4 | 0.12 | 1 |
| lies, invented people | Gemini Pro | copies10 -> labelled10 | 80 | -0.85 | 0 | 68 | 6.8e-21 | 7.6e-19 |
| lies, invented people | Gemini Pro | copies3 -> sameoutlet3 | 80 | -0.15 | 6 | 18 | 0.023 | 1 |
| lies, invented people | Gemini Pro | copies1 -> sameoutlet3 | 80 | -0.02 | 17 | 19 | 0.87 | 1 |
| lies, invented people | Gemini Pro | copies3 -> copies3_falseindep | 80 | -0.07 | 8 | 14 | 0.29 | 1 |
| lies, invented people | Gemini Pro | indep3 -> paraphrase3_note | 80 | -0.64 | 0 | 51 | 8.9e-16 | 9.3e-14 |
| lies, invented people | Gemini Pro | copies3 -> copies3_table | 80 | -0.75 | 0 | 60 | 1.7e-18 | 1.9e-16 |
| lies, invented people | Gemini Pro | labelled3 -> copies3_table | 80 | +0.01 | 1 | 0 | 1 | 1 |
| lies, invented people | Gemini Pro | copies3 -> copies3_known | 80 | -0.26 | 3 | 24 | 4.9e-05 | 0.0043 |
| lies, invented people | Gemini Pro | indep3 -> indep3_known | 80 | -0.03 | 0 | 2 | 0.5 | 1 |
| lies, known facts | Llama 3.2 | copies1 -> copies3 | 80 | +0.05 | 6 | 2 | 0.29 | 1 |
| lies, known facts | Llama 3.2 | copies3 -> indep3 | 80 | -0.04 | 5 | 8 | 0.58 | 1 |
| lies, known facts | Llama 3.2 | copies3 -> labelled3 | 80 | +0.04 | 6 | 3 | 0.51 | 1 |
| lies, known facts | Llama 3.2 | copies3 -> filler3 | 80 | +0.20 | 20 | 4 | 0.0015 | 0.12 |
| lies, known facts | Llama 3.2 | copies3 -> copies10 | 80 | -0.12 | 0 | 10 | 0.002 | 0.15 |
| lies, known facts | Llama 3.2 | copies10 -> labelled10 | 80 | +0.02 | 3 | 1 | 0.62 | 1 |
| lies, known facts | Llama 3.2 | copies3 -> sameoutlet3 | 80 | -0.09 | 2 | 9 | 0.065 | 1 |
| lies, known facts | Llama 3.2 | copies1 -> sameoutlet3 | 80 | -0.04 | 2 | 5 | 0.45 | 1 |
| lies, known facts | Llama 3.2 | copies3 -> copies3_falseindep | 80 | +0.01 | 5 | 4 | 1 | 1 |
| lies, known facts | Llama 3.2 | indep3 -> paraphrase3_note | 80 | +0.10 | 9 | 1 | 0.021 | 1 |
| lies, known facts | Llama 3.2 | copies3 -> copies3_table | 80 | -0.09 | 2 | 9 | 0.065 | 1 |
| lies, known facts | Llama 3.2 | labelled3 -> copies3_table | 80 | -0.12 | 0 | 10 | 0.002 | 0.15 |
| lies, known facts | Llama 3.2 | copies3 -> copies3_known | 80 | +0.05 | 7 | 3 | 0.34 | 1 |
| lies, known facts | Llama 3.2 | indep3 -> indep3_known | 80 | +0.00 | 2 | 2 | 1 | 1 |
| lies, known facts | phi4 | copies1 -> copies3 | 80 | +0.14 | 12 | 1 | 0.0034 | 0.25 |
| lies, known facts | phi4 | copies3 -> indep3 | 80 | +0.01 | 4 | 3 | 1 | 1 |
| lies, known facts | phi4 | copies3 -> labelled3 | 80 | -0.02 | 1 | 3 | 0.62 | 1 |
| lies, known facts | phi4 | copies3 -> filler3 | 80 | +0.03 | 5 | 3 | 0.73 | 1 |
| lies, known facts | phi4 | copies3 -> copies10 | 80 | -0.04 | 2 | 5 | 0.45 | 1 |
| lies, known facts | phi4 | copies10 -> labelled10 | 80 | +0.00 | 3 | 3 | 1 | 1 |
| lies, known facts | phi4 | copies3 -> sameoutlet3 | 80 | -0.04 | 2 | 5 | 0.45 | 1 |
| lies, known facts | phi4 | copies1 -> sameoutlet3 | 80 | +0.10 | 8 | 0 | 0.0078 | 0.55 |
| lies, known facts | phi4 | copies3 -> copies3_falseindep | 80 | +0.01 | 2 | 1 | 1 | 1 |
| lies, known facts | phi4 | indep3 -> paraphrase3_note | 80 | +0.00 | 4 | 4 | 1 | 1 |
| lies, known facts | phi4 | copies3 -> copies3_table | 80 | +0.01 | 3 | 2 | 1 | 1 |
| lies, known facts | phi4 | labelled3 -> copies3_table | 80 | +0.04 | 4 | 1 | 0.38 | 1 |
| lies, known facts | phi4 | copies3 -> copies3_known | 80 | -0.06 | 1 | 6 | 0.12 | 1 |
| lies, known facts | phi4 | indep3 -> indep3_known | 80 | -0.04 | 0 | 3 | 0.25 | 1 |
| lies, known facts | Gemini Flash | copies1 -> copies3 | 80 | +0.16 | 14 | 1 | 0.00098 | 0.076 |
| lies, known facts | Gemini Flash | copies3 -> indep3 | 80 | +0.20 | 19 | 3 | 0.00086 | 0.068 |
| lies, known facts | Gemini Flash | copies3 -> labelled3 | 80 | -0.15 | 0 | 12 | 0.00049 | 0.041 |
| lies, known facts | Gemini Flash | copies3 -> filler3 | 80 | -0.01 | 6 | 7 | 1 | 1 |
| lies, known facts | Gemini Flash | copies3 -> copies10 | 80 | -0.05 | 2 | 6 | 0.29 | 1 |
| lies, known facts | Gemini Flash | copies10 -> labelled10 | 80 | -0.18 | 0 | 14 | 0.00012 | 0.01 |
| lies, known facts | Gemini Flash | copies3 -> sameoutlet3 | 80 | +0.04 | 5 | 2 | 0.45 | 1 |
| lies, known facts | Gemini Flash | copies1 -> sameoutlet3 | 80 | +0.20 | 17 | 1 | 0.00014 | 0.012 |
| lies, known facts | Gemini Flash | copies3 -> copies3_falseindep | 80 | -0.05 | 1 | 5 | 0.22 | 1 |
| lies, known facts | Gemini Flash | indep3 -> paraphrase3_note | 80 | -0.24 | 1 | 20 | 2.1e-05 | 0.0019 |
| lies, known facts | Gemini Flash | copies3 -> copies3_table | 80 | -0.19 | 0 | 15 | 6.1e-05 | 0.0053 |
| lies, known facts | Gemini Flash | labelled3 -> copies3_table | 80 | -0.04 | 0 | 3 | 0.25 | 1 |
| lies, known facts | Gemini Flash | copies3 -> copies3_known | 80 | -0.05 | 4 | 8 | 0.39 | 1 |
| lies, known facts | Gemini Flash | indep3 -> indep3_known | 80 | -0.15 | 2 | 14 | 0.0042 | 0.3 |
| lies, known facts | Gemini Pro | copies1 -> copies3 | 80 | +0.04 | 3 | 0 | 0.25 | 1 |
| lies, known facts | Gemini Pro | copies3 -> indep3 | 80 | +0.15 | 13 | 1 | 0.0018 | 0.14 |
| lies, known facts | Gemini Pro | copies3 -> labelled3 | 80 | -0.15 | 0 | 12 | 0.00049 | 0.041 |
| lies, known facts | Gemini Pro | copies3 -> filler3 | 80 | +0.14 | 12 | 1 | 0.0034 | 0.25 |
| lies, known facts | Gemini Pro | copies3 -> copies10 | 80 | +0.00 | 0 | 0 | 1 | 1 |
| lies, known facts | Gemini Pro | copies10 -> labelled10 | 80 | -0.15 | 0 | 12 | 0.00049 | 0.041 |
| lies, known facts | Gemini Pro | copies3 -> sameoutlet3 | 80 | -0.04 | 0 | 3 | 0.25 | 1 |
| lies, known facts | Gemini Pro | copies1 -> sameoutlet3 | 80 | +0.00 | 1 | 1 | 1 | 1 |
| lies, known facts | Gemini Pro | copies3 -> copies3_falseindep | 80 | +0.05 | 5 | 1 | 0.22 | 1 |
| lies, known facts | Gemini Pro | indep3 -> paraphrase3_note | 80 | -0.19 | 0 | 15 | 6.1e-05 | 0.0053 |
| lies, known facts | Gemini Pro | copies3 -> copies3_table | 80 | -0.15 | 0 | 12 | 0.00049 | 0.041 |
| lies, known facts | Gemini Pro | labelled3 -> copies3_table | 80 | +0.00 | 0 | 0 | 1 | 1 |
| lies, known facts | Gemini Pro | copies3 -> copies3_known | 80 | +0.02 | 2 | 0 | 0.5 | 1 |
| lies, known facts | Gemini Pro | indep3 -> indep3_known | 80 | -0.05 | 2 | 6 | 0.29 | 1 |
