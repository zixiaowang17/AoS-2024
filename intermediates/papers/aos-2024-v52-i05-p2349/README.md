# A nonparametric test for elliptical distribution based on kernel embedding of probabilities

Source census completed against the registered **arXiv:2306.10594v2, 27 March 2024**, 25 PDF pages, for the AoS article with DOI `10.1214/24-AOS2438`. [Inspected paper version](https://arxiv.org/pdf/2306.10594v2).

Source SHA-256: `b9a6c162c4c8845483163754773e65bb696f24444c3621a3c8b5dfdbcc113278`.

- **6 theorems**: 1–6, with complete original statements and formulas.
- **32 source entries**, **8 supporting passages**, **41 direct uses** and **98 related connections**.
- Main text, acknowledgments and funding end before Supplementary Material on PDF page 23. Appendix bodies were excluded.

The census preserves the kernel/RKHS and Hilbert tensor constructions, characteristicness, coordinate domains and polar formulas, mean/covariance and fitted transformations, fixed angular reference law, discrepancy operators, functional differentiability, full influence formulas, covariance operator, kernel conditions and Assumptions 1–4 with the four concentration-rate functions.

Theorem 1 has only abstract kernel and probability-measure dependencies. Theorem 2 uses the full discrepancy influence function without a null-only simplification. Theorem 4 uses the known-parameter formula, while Theorems 5–6 use fitted transformations. Theorem 6 inherits Theorem 5’s assumptions without importing its bound-specific rate functions.

Thirteen source notes record polar and whitening domains, missing local-alternative and zero-eigenvalue conventions, the E-versus-E0 discrepancy in (7.1), Hilbert-Schmidt versus simple-tensor supremum, implicit quantifiers and implementation notation. Conditional influence-formula context is retained without claiming that it supplies all missing local-alternative conditions. Original quotations are preserved; source review does not certify mathematical proofs.

## Artifacts

`theorem-inventory.json` contains the original theorem statements. `source-passages.json` contains original definitions, assumptions, conditions and relevant Lemma formula passages. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` preserves additional context, source issues and theorem-local bindings.

`inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/` record source identity, independent heading enumeration, visual source comparison, formula checks, dependency reconstruction and schema validation.

## Reproduction

All seven per-paper scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2349/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
