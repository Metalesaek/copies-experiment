# Rewrites by other models: text detector

Same 200 articles and prompt as the phi4 rewrites (measure_detector.py).

| rewriter | rewrites | linked by the text detector (Jaccard >= 0.6) | median Jaccard |
|---|---|---|---|
| phi4 | 200 | 0.00 | 0.04 |
| llama3.2 | 200 | 0.00 | 0.06 |
| gemini-2.5-flash | 200 | 0.00 | 0.06 |