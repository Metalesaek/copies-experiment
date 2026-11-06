# Which part of the article the copy detector reads

200000 CC-News articles, boilerplate removed, near-copy = 5-gram MinHash Jaccard >= 0.6 across outlets. Share = articles in a chain / the 196664 articles long enough for the paper's window (the denominator of Section 3).

| text window | articles in chains | share | chains | pairs | of the paper's chain articles, also linked here | articles linked here but not by the paper's window |
|---|---|---|---|---|---|---|
| first 1,000 | 36295 | 18.5% | 12036 | 58260 | 0.94 | 1407 |
| first 2,000 (paper) | 37171 | 18.9% | 12323 | 57768 | 1.00 | 0 |
| first 4,000 | 37855 | 19.2% | 12471 | 60626 | 0.98 | 1423 |
| full text | 38227 | 19.4% | 12478 | 62062 | 0.98 | 1827 |
| last 2,000 | 37899 | 19.3% | 12329 | 61642 | 0.96 | 2257 |
| head or tail | 39428 | 20.0% | 12601 | 66321 | 1.00 | 2257 |

data/window_new_pairs.csv: up to 40 pairs per window that the paper's window does not link (URLs and titles, for inspection).