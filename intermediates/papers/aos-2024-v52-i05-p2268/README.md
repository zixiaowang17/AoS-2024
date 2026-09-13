# Environment invariant linear least squares

Source census completed against the registered **arXiv:2303.03092v3, 29 November 2024**, 65 PDF pages, for the AoS article with DOI `10.1214/24-AOS2435`. [Inspected paper version](https://arxiv.org/pdf/2303.03092v3).

Source SHA-256: `41f8bc8d4dd5ddd961858aa2de3b28f08f5f0be294675a557a47cb7c64fa2a19`.

- **4 theorems**: 4.2–4.5, with complete original statements and formulas.
- **27 source entries**, **12 supporting passages**, **37 direct uses** and **85 related connections**.
- Main text and acknowledgments end before References on PDF page 20. Appendix bodies were excluded.

The census preserves the conditional-mean model, true residuals, population and empirical risks, focused invariance penalties, unpenalized and penalized EILLS estimators, balanced sampling and Conditions 4.1–4.6. It retains the full critical-threshold, screening-signal and sample-size formulas. Population and empirical risks remain separate.

Theorem 4.4’s initial error bound does not require successful screening; only its improved-bound branch imports Theorem 4.3’s additional sample conditions. Screening and exact support recovery are distinct conclusions. References to the threshold defined in Theorem 4.2 import its definition rather than its full conclusion or population objective.

Twelve source notes record the printed x-versus-beta typo in the population loss, pooled covariance normalization, empty-set conventions, support gating, unused c4, penalty feasibility and global-optimization limitations. Original quotations remain unchanged. Source validation does not certify mathematical proofs or repair source ambiguities.

## Artifacts

`theorem-inventory.json` contains the original theorem statements. `source-passages.json` contains definitions, conditions and theorem excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` preserves additional invariance definitions, context, source issues and theorem-local bindings.

`inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/` record source identity, independent heading enumeration, visual source comparison, formula checks, dependency reconstruction and schema validation.

## Reproduction

All seven per-paper scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2268/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
