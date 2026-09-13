# Testing high-dimensional regression coefficients in linear models

Completed census of the registered local NIH author manuscript
`nihms-2151735.pdf`, available in PMC on 13 March 2026 and identifying the final
2024 article. The 36-page source is pinned by its SHA-256. The main text ends on
page 23; appendix material is excluded from the census.

- `theorem-inventory.json`: both complete main-text Theorems, including both parts of each.
- `source-passages.json`: 14 original definition, assumption and source-passage entries.
- `ambient-prerequisites.json`: 10 auxiliary passages, scoped references, local bindings and 10 source conventions or ambiguities.
- `ranked-interfaces.json`: 13 direct uses and 23 related theorem connections.
- `paper-audit.json` and `registered-source-review.json`: independent source review and validation records.
- `scripts/`: the retained extraction, reproduction and review scripts.

The census distinguishes population-centered and sample-centered scores, the
sample covariance from the estimator of the squared population covariance, and
the population normalization from the estimated denominator. It also preserves
the separate scopes of Theorem 2(i) and (ii): the extra Gaussian-error condition
belongs only to (i). Theorem 1's local alternative and additional tuning condition
are not silently added to Theorem 2.

Reproduce all six JSON content artifacts in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2034/scripts/rebuild.py --output-dir [local path omitted]
```

The rebuild validates structure and compares the outputs byte for byte with the
saved content. It does not perform a new semantic review. Completion certifies
the source census and data validation, not the mathematical proofs.
