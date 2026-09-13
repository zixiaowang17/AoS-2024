# Estimation of the spectral measure from convex combinations of regularly varying random vectors

Status: complete, independently checked against the registered local PDF.

- Source: arXiv:2010.03832v2, marked 3 July 2024; running preprint date 4 July 2024. Main text ends on PDF page 25 before references; appendices are excluded.
- Inventory: all three main-text Theorems 5, 8 and 10, with complete original statements.
- Census: 23 source entries, 8 auxiliary passages, 26 direct theorem uses and 40 related-theorem connections.
- Keep Theorem 5’s expectation centering separate from Corollary 6’s angular bias assumption and Theorem 8’s marginal second-order condition. Theorem 10 explicitly imports both sets of assumptions.
- Original notation discrepancies are documented in `ambient-prerequisites.json`; no source formula is silently repaired. Main-text covariance specializations suffice for the Gaussian combination in Theorem 10.
- `theorem-inventory.json` and `ranked-interfaces.json` pass validation. All six content JSON files reproduce byte for byte in `[local path omitted]`.
- Seven scripts remain in `scripts/`, including the full-source review with frozen artifact hashes. `paper-audit.json`, `registered-source-review.json` and `evidence/manual-findings.json` record the checks and their limits.

Rebuild in a new empty directory with `python3 -B scripts/rebuild.py --output-dir [local path omitted]`. Rebuilding reproduces saved extraction decisions; it does not perform a new semantic source review.
