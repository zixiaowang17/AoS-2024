# Debiased inverse propensity score weighting for estimation of average treatment effects with high-dimensional confounders

Paper ID: `aos-2024-v52-i05-p1978`.

Status: **complete** for the registered arXiv:2011.08661v3 PDF. Its arXiv stamp is 11 April 2024 and its title-page date is 12 April 2024. Main text ends after Acknowledgement on page 27, before References; appendices are excluded. This review does not assume equivalence to the published article.

The census preserves **four complete theorem statements**, **26 indexed original source entries**, and **14 auxiliary passages**. Twelve source conventions or ambiguities remain recorded separately. The graph contains 56 direct uses after explicit expansion of unnamed local formulas, and 83 related theorem connections.

Theorem 3 inherits Theorem 2's setup and bias bound. Theorem 5 borrows Theorem 4's estimator construction but does not inherit Assumptions 6-7 or its confidence interval. The conditional and population targets, initial and optimized corrections, and conditional and marginal normal approximations remain distinct.

- `theorem-inventory.json`: complete original Theorems 2-5.
- `ranked-interfaces.json`: original source entries, keywords, highlights and theorem relationships.
- `source-passages.json` and `interface-extraction.json`: retained extraction records.
- `ambient-prerequisites.json`: original local formulas, scope bindings and source issues.
- `paper-audit.json` and `registered-source-review.json`: source review, independent validation and hashes.
- `evidence/rebuild-check.json`: byte-for-byte reproduction of all six content artifacts.

All paper-specific Python scripts are retained in `scripts/`. Reproduce into an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p1978/scripts/rebuild.py --output-dir [local path omitted]
```

Rebuilding preserves the saved extraction and checks structure. The independent review scripts check the frozen reviewed content; rerunning them does not itself constitute a new semantic source review or certify proofs.
