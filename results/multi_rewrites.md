# Copy networks of real rewrites: what the detectors miss

20 originals, 10 rewrites each by phi4 (temperature 0.8, seeds 1-10), linked in stream order to the origin or any copy already linked.

| attack | detector | copies missed (share) | networks with 0 missed | with all 10 missed | P(at least one missed), observed | same, if misses were independent |
|---|---|---|---|---|---|---|
| paraphrase | text | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| paraphrase | new_information | 0.06 | 0.85 | 0.05 | 0.15 | 0.46 |
| adaptive | text | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| adaptive | new_information | 0.20 | 0.50 | 0.05 | 0.50 | 0.90 |