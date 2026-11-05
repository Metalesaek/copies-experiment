# Copy chains: threshold sensitivity and purity (boilerplate removed)

200000 articles, 196664 long enough to compare.

| Jaccard threshold | cross-outlet pairs | chains | articles in chains | share of articles |
|---|---|---|---|---|
| 0.6, LSH candidates as in Section 3 | 57768 | 12323 | 37171 | 18.9% |
| 0.5 | 63532 | 12828 | 39128 | 19.9% |
| 0.6 | 55464 | 12210 | 36562 | 18.6% |
| 0.7 | 50068 | 11632 | 34300 | 17.4% |

## Purity of the chains at 0.6

Chains of two articles: 7196 (one direct near-copy pair each, pure by construction). Chains of three or more: 5014, holding 22170 articles.

| measure (chains of 3+) | value |
|---|---|
| median of the mean pairwise similarity | 0.95 |
| share of chains whose weakest pair is below 0.6 (joined through others) | 0.05 |
| share of chains whose weakest pair is below 0.3 | 0.00 |
| articles in such chains (below 0.3) | 0 |
| articles that are a direct near-copy of the chain's earliest article (mean over chains) | 0.99 |
| same, weighted by chain size | 0.98 |

Examples for manual inspection: data/chain_purity_examples_strip.csv (30 chains with a pair below 0.3).