# New information as a copy signal

Rewrites by llama3.2: 200; independent reports of the same event found for 167 originals (other outlet, within one day, more than 3 shared facts, 5-gram Jaccard < 0.2).

| | median share of new facts | median 5-gram Jaccard with the original |
|---|---|---|
| rewrite (copy) | 0.32 | 0.06 |
| independent report | 0.82 | below 0.2 by selection |

AUC (copy has less new information than an independent report): **0.94**

| flag as copy if new facts below | rewrites caught (recall) | independent reports wrongly flagged |
|---|---|---|
| 0.1 | 0.03 | 0.00 |
| 0.2 | 0.14 | 0.01 |
| 0.3 | 0.43 | 0.02 |
| 0.4 | 0.71 | 0.05 |
| 0.5 | 0.88 | 0.11 |

## Same pairs, facts from spaCy named entities (en_core_web_sm) and quotations

### spaCy entities

Median share of new facts: rewrites 0.27, independent reports 0.84. AUC: **0.96**

| flag as copy if new facts below | rewrites caught (recall) | independent reports wrongly flagged |
|---|---|---|
| 0.1 | 0.09 | 0.00 |
| 0.2 | 0.28 | 0.01 |
| 0.3 | 0.60 | 0.03 |
| 0.4 | 0.81 | 0.05 |
| 0.5 | 0.91 | 0.07 |

Rank correlation of the two measures over all reports: 0.89.

Facts = capitalised names, numbers and quotations (first 2,500 characters, boilerplate removed). Text similarity alone linked 0% of the rewrites to their original (results/detector_measured.md).