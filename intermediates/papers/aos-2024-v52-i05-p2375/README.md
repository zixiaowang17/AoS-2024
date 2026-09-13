# Simultaneous statistical inference for second order parameters of time series under weak conditions

Source census completed against the registered **arXiv:2110.14067v2, 25 February 2023**, 66 PDF pages, for the AoS article with DOI `10.1214/24-AOS2439`. [Inspected paper version](https://arxiv.org/pdf/2110.14067v2).

Source SHA-256: `fe207a49e1348050da5b83e03fbacb2ad8f1beb676ca7ebf1ac395393d57c579`.

- **4 theorems**, with complete original statements and all subparts.
- **25 source entries**, **15 supporting passages**, **32 direct uses** and **51 related connections**.
- Main text and acknowledgment end on PDF page 28; references begin on page 29. Appendix bodies were excluded.

The census preserves causal and coupling definitions, medium- and short-range dependence, covariance/correlation targets and estimators, Yule–Walker coefficients and their linearizations, the full kernel definition, bandwidth bias sequence, conditional probability and second-order wild bootstrap constructions. Numerical growth and nondegeneracy assumptions remain with their specific theorem branches.

Theorem 1 permits nonstationary data. The covariance/correlation results use the Section 3 weak-stationarity setting, while Theorem 3 explicitly assumes it and keeps AR order bounded. Theorem 4 imports Lemma 4 assumptions branchwise and only the numerical definition of the bias sequence from Lemma 3. Its three conclusions retain their different rates.

Thirteen source notes preserve apparent errors and unresolved conventions, including the summation index in Remark 2, the covariance indices in Theorem 2(i), and the undefined centering notation in equation (27). Original statements are not silently repaired. Source review does not certify proofs.

## Artifacts

`theorem-inventory.json` contains every original theorem statement. `source-passages.json` contains the original definitions and object-defining excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` preserves branch-specific conditions, additional context and source issues.

`inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/` record source identity, independent heading enumeration, visual source comparison, formula checks, dependency reconstruction and schema validation.

## Reproduction

All seven per-paper scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2375/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
