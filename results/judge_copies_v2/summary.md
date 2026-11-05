# Do LLM judges count copies as confirmations?

Share of claims the judge calls **true** (n = 80 per cell unless noted; 95% Wilson intervals in verdicts.csv analyses). For lies lower is better; for truths higher is better. Unparsed answers count as false.

## gemini:gemini-2.5-flash

| claim kind | none | copies1 | copies3 | copies5 | copies10 | indep3 | filler3 | labelled3 | labelled10 | sameoutlet3 | copies3_falseindep | paraphrase3_note | copies3_table | copies3_known | indep3_known |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| known-fact lie | 0.06 | 0.15 | 0.31 | 0.26 | 0.26 | 0.51 | 0.30 | 0.16 | 0.09 | 0.35 | 0.26 | 0.28 | 0.12 | 0.26 | 0.36 |
| true update of a known fact | 0.06 | 0.20 | 0.39 | 0.34 | 0.29 | 0.53 | 0.42 | 0.17 | 0.10 | 0.44 | 0.30 | 0.38 | 0.15 | 0.31 | 0.46 |
| lie about an invented person | 0.00 | 0.93 | 1.00 | 1.00 | 1.00 | 1.00 | 0.97 | 0.79 | 0.20 | 1.00 | 0.95 | 0.97 | 0.49 | 1.00 | 1.00 |
| true fact about an invented person | 0.00 | 0.99 | 1.00 | 0.99 | 1.00 | 1.00 | 0.99 | 0.68 | 0.31 | 1.00 | 0.94 | 1.00 | 0.56 | 1.00 | 1.00 |

With the Unsure option (True / Unsure / False):

| claim kind | none+unsure | copies1+unsure | copies3+unsure | indep3+unsure | labelled3+unsure |
|---|---|---|---|---|---|
| known-fact lie | 0.04 / 0.21 / 0.75 | 0.21 / 0.20 / 0.59 | 0.50 / 0.04 / 0.46 | 0.68 / 0.04 / 0.29 | 0.16 / 0.30 / 0.54 |
| true update of a known fact | 0.05 / 0.17 / 0.78 | 0.30 / 0.19 / 0.51 | 0.56 / 0.05 / 0.39 | 0.71 / 0.05 / 0.24 | 0.19 / 0.40 / 0.41 |
| lie about an invented person | 0.00 / 1.00 / 0.00 | 1.00 / 0.00 / 0.00 | 1.00 / 0.00 / 0.00 | 1.00 / 0.00 / 0.00 | 0.51 / 0.49 / 0.00 |
| true fact about an invented person | 0.00 / 1.00 / 0.00 | 1.00 / 0.00 / 0.00 | 1.00 / 0.00 / 0.00 | 1.00 / 0.00 / 0.00 | 0.36 / 0.64 / 0.00 |

Unparsed answers: 0.

## gemini:gemini-2.5-pro

| claim kind | none | copies1 | copies3 | copies5 | copies10 | indep3 | filler3 | labelled3 | labelled10 | sameoutlet3 | copies3_falseindep | paraphrase3_note | copies3_table | copies3_known | indep3_known |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| known-fact lie | 0.06 | 0.12 | 0.16 | 0.17 | 0.16 | 0.31 | 0.30 | 0.01 | 0.01 | 0.12 | 0.21 | 0.12 | 0.01 | 0.19 | 0.26 |
| true update of a known fact | 0.06 | 0.09 | 0.11 | 0.14 | 0.11 | 0.41 | 0.38 | 0.03 | 0.01 | 0.14 | 0.23 | 0.07 | 0.01 | 0.15 | 0.31 |
| lie about an invented person | 0.01 | 0.64 | 0.76 | 0.86 | 0.85 | 1.00 | 0.99 | 0.00 | 0.00 | 0.61 | 0.69 | 0.36 | 0.01 | 0.50 | 0.97 |
| true fact about an invented person | 0.00 | 0.69 | 0.84 | 0.90 | 0.90 | 1.00 | 1.00 | 0.00 | 0.00 | 0.74 | 0.82 | 0.49 | 0.00 | 0.71 | 1.00 |

With the Unsure option (True / Unsure / False):

| claim kind | none+unsure | copies1+unsure | copies3+unsure | indep3+unsure | labelled3+unsure |
|---|---|---|---|---|---|
| known-fact lie | 0.05 / 0.19 / 0.76 | 0.09 / 0.31 / 0.60 | 0.12 / 0.35 / 0.53 | 0.28 / 0.28 / 0.45 | 0.01 / 0.62 / 0.36 |
| true update of a known fact | 0.04 / 0.19 / 0.78 | 0.06 / 0.36 / 0.57 | 0.10 / 0.59 / 0.31 | 0.42 / 0.20 / 0.38 | 0.01 / 0.74 / 0.25 |
| lie about an invented person | 0.00 / 1.00 / 0.00 | 0.11 / 0.89 / 0.00 | 0.59 / 0.41 / 0.00 | 1.00 / 0.00 / 0.00 | 0.00 / 1.00 / 0.00 |
| true fact about an invented person | 0.00 / 1.00 / 0.00 | 0.12 / 0.88 / 0.00 | 0.62 / 0.38 / 0.00 | 1.00 / 0.00 / 0.00 | 0.00 / 1.00 / 0.00 |

Unparsed answers: 71.

## llama3.2

| claim kind | none | copies1 | copies3 | copies5 | copies10 | indep3 | filler3 | labelled3 | labelled10 | sameoutlet3 | copies3_falseindep | paraphrase3_note | copies3_table | copies3_known | indep3_known |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| known-fact lie | 0.01 | 0.09 | 0.14 | 0.07 | 0.01 | 0.10 | 0.34 | 0.17 | 0.04 | 0.05 | 0.15 | 0.20 | 0.05 | 0.19 | 0.10 |
| true update of a known fact | 0.00 | 0.03 | 0.24 | 0.10 | 0.03 | 0.11 | 0.41 | 0.24 | 0.07 | 0.09 | 0.17 | 0.23 | 0.06 | 0.24 | 0.11 |
| lie about an invented person | 0.00 | 0.06 | 0.71 | 0.55 | 0.44 | 0.34 | 0.40 | 0.74 | 0.51 | 0.00 | 0.75 | 0.57 | 0.42 | 0.69 | 0.34 |
| true fact about an invented person | 0.00 | 0.05 | 0.64 | 0.46 | 0.34 | 0.26 | 0.39 | 0.70 | 0.41 | 0.00 | 0.75 | 0.59 | 0.35 | 0.61 | 0.20 |

With the Unsure option (True / Unsure / False):

| claim kind | none+unsure | copies1+unsure | copies3+unsure | indep3+unsure | labelled3+unsure |
|---|---|---|---|---|---|
| known-fact lie | 0.04 / 0.00 / 0.96 | 0.38 / 0.01 / 0.61 | 0.59 / 0.04 / 0.38 | 0.41 / 0.09 / 0.50 | 0.46 / 0.00 / 0.54 |
| true update of a known fact | 0.03 / 0.00 / 0.97 | 0.34 / 0.01 / 0.65 | 0.54 / 0.09 / 0.38 | 0.46 / 0.10 / 0.44 | 0.49 / 0.00 / 0.51 |
| lie about an invented person | 0.00 / 0.00 / 1.00 | 0.56 / 0.04 / 0.40 | 0.99 / 0.00 / 0.01 | 0.66 / 0.21 / 0.12 | 0.95 / 0.00 / 0.05 |
| true fact about an invented person | 0.00 / 0.00 / 1.00 | 0.65 / 0.00 / 0.35 | 0.97 / 0.01 / 0.01 | 0.68 / 0.17 / 0.15 | 0.95 / 0.00 / 0.05 |

Unparsed answers: 3.

## phi4

| claim kind | none | copies1 | copies3 | copies5 | copies10 | indep3 | filler3 | labelled3 | labelled10 | sameoutlet3 | copies3_falseindep | paraphrase3_note | copies3_table | copies3_known | indep3_known |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| known-fact lie | 0.07 | 0.10 | 0.24 | 0.25 | 0.20 | 0.25 | 0.26 | 0.21 | 0.20 | 0.20 | 0.25 | 0.25 | 0.25 | 0.17 | 0.21 |
| true update of a known fact | 0.05 | 0.07 | 0.20 | 0.16 | 0.14 | 0.28 | 0.33 | 0.17 | 0.14 | 0.14 | 0.23 | 0.29 | 0.26 | 0.20 | 0.24 |
| lie about an invented person | 0.00 | 0.21 | 0.90 | 0.78 | 0.50 | 0.97 | 0.93 | 0.82 | 0.57 | 0.62 | 0.84 | 0.99 | 0.88 | 0.55 | 0.95 |
| true fact about an invented person | 0.00 | 0.25 | 0.88 | 0.79 | 0.53 | 0.99 | 0.94 | 0.81 | 0.56 | 0.70 | 0.86 | 1.00 | 0.94 | 0.61 | 0.96 |

With the Unsure option (True / Unsure / False):

| claim kind | none+unsure | copies1+unsure | copies3+unsure | indep3+unsure | labelled3+unsure |
|---|---|---|---|---|---|
| known-fact lie | 0.05 / 0.20 / 0.75 | 0.11 / 0.26 / 0.62 | 0.25 / 0.21 / 0.54 | 0.34 / 0.12 / 0.54 | 0.23 / 0.26 / 0.51 |
| true update of a known fact | 0.06 / 0.20 / 0.74 | 0.07 / 0.33 / 0.60 | 0.30 / 0.26 / 0.44 | 0.41 / 0.09 / 0.50 | 0.26 / 0.33 / 0.41 |
| lie about an invented person | 0.00 / 0.99 / 0.01 | 0.33 / 0.68 / 0.00 | 0.96 / 0.04 / 0.00 | 1.00 / 0.00 / 0.00 | 0.88 / 0.12 / 0.00 |
| true fact about an invented person | 0.00 / 1.00 / 0.00 | 0.31 / 0.69 / 0.00 | 0.99 / 0.01 / 0.00 | 1.00 / 0.00 / 0.00 | 0.88 / 0.12 / 0.00 |

Unparsed answers: 38.
