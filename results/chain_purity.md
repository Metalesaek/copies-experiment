# Copy chains: threshold sensitivity and purity

200000 articles, 199998 long enough to compare.

| Jaccard threshold | cross-outlet pairs | chains | articles in chains | share of articles |
|---|---|---|---|---|
| 0.6, LSH candidates as in Section 3 | 76857 | 12243 | 37705 | 18.9% |
| 0.5 | 86296 | 12803 | 39819 | 19.9% |
| 0.6 | 74271 | 12107 | 37101 | 18.6% |
| 0.7 | 66358 | 11513 | 34704 | 17.4% |

## Purity of the chains at 0.6

Chains of two articles: 7133 (one direct near-copy pair each, pure by construction). Chains of three or more: 4974, holding 22835 articles.

| measure (chains of 3+) | value |
|---|---|
| median of the mean pairwise similarity | 0.95 |
| share of chains whose weakest pair is below 0.6 (joined through others) | 0.05 |
| share of chains whose weakest pair is below 0.3 | 0.00 |
| articles in such chains (below 0.3) | 0 |
| articles that are a direct near-copy of the chain's earliest article (mean over chains) | 0.99 |
| same, weighted by chain size | 0.98 |

Examples for manual inspection: data/chain_purity_examples.csv (30 chains with a pair below 0.3).