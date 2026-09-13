# A new test for high-dimensional two-sample mean problems with consideration of correlation structure

Source census completed against the registered published journal PDF, **The Annals of Statistics 52(5), 2024, pp. 2217–2240**, DOI `10.1214/24-AOS2433`, 24 PDF pages. Registered filename: `24-AOS2433-1.pdf`.

Source SHA-256: `4866290bd80a1259e98bf4ce9009d84443ad2c20c9a0927e9b61ed133785bad7`.

- **4 theorems**: 2.1–2.4, including the complete two-page Theorem 2.2.
- **19 source entries**, **10 supporting passages**, **33 direct uses** and **49 related connections**.
- Main text and funding end before the supplementary-material notice on PDF page 23. No supplementary or appendix body was used.

The census preserves the linear inverse-correlation model, raw coefficient estimator, fourth-moment assumptions, complete centering and variance formulas, fitted precision matrix, test statistic and null/alternative normalizers. The sample and population matrices both named B remain distinct. Inherited theorem assumptions do not import unrelated conclusions or their auxiliary formulas.

The paper reuses coefficient notation for raw, bias-corrected and penalized fits. Thirteen source notes retain this ambiguity and other issues, including implicit inverse/scale existence, the singular variance formula at y=1, zero contrasts, trace powers, almost-sure versus proof wording and test-statistic scaling. The Discussion’s explicit spectral-norm requirement is recorded separately from the printed theorem statements. The census does not repair or certify the mathematical claims.

## Artifacts

`theorem-inventory.json` contains the full original theorem statements. `source-passages.json` contains definitions, assumptions and source excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` retains supporting passages, source issues and theorem-local bindings.

Independent checks are recorded in `inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/`. Heading enumeration, source-specific checks, dependency reconstruction and schema validation passed.

## Reproduction

All seven per-paper Python scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2217/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
