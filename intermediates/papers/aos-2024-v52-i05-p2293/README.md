# Gaussian approximation for nonstationary time series with optimal rate and explicit construction

Source census completed against the registered **arXiv:2408.02913v2, 7 August 2024**, 60 PDF pages, for the AoS article with DOI `10.1214/24-AOS2436`. [Inspected paper version](https://arxiv.org/pdf/2408.02913v2).

Source SHA-256: `504e0a5bbb366e23bc01b4264674f851a547786f4601c4101495940434e53293`.

- **8 theorems**: 2.1–2.5, 3.1–3.2 and 4.1, with complete original statements and formulas.
- **19 source entries**, **12 supporting passages**, **45 direct uses** and **72 related connections**.
- Main text and acknowledgments end before Supplementary Material on PDF page 21. Appendix bodies were excluded.

The census preserves causal inputs, uniform functional dependence, Conditions 2.1–2.4, clipping and centered clipped sums, both decay thresholds, Gaussian coupling conventions, banded quadratic forms, the block exponent, the signal-plus-noise model, quantile grid, kernel and local-linear estimator.

Theorem 2.1 is included as a locally labeled theorem despite its attribution to earlier work. The two nonsingularity conditions remain separate. Theorem 2.4 needs neither, and Theorem 3.1 does not require uniform integrability or Gaussian coupling. Theorem 3.2 imports the numerical block exponent, without an empirical variance or conditional-bootstrap premise. Theorem 4.1 applies approximation assumptions to the noise and uses its partial sums, which are distinct from deterministic design moments.

Twelve source notes preserve the printed uniform-integrability comparison, reversed block-exponent comparison, quantile-grid endpoint inconsistency, overloaded block notation and implicit kernel conventions. Original statements are not silently repaired. Source validation does not certify proofs.

## Artifacts

`theorem-inventory.json` contains the original theorem statements. `source-passages.json` contains definitions, conditions and theorem excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` preserves additional context, source issues and theorem-local bindings.

`inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/` record source identity, independent heading enumeration, visual source comparison, formula checks, dependency reconstruction and schema validation.

## Reproduction

All seven per-paper scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2293/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
