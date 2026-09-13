# Deep neural networks for nonparametric interaction models with diverging dimension

Source-reviewed census of the registered local arXiv:2302.05851v1 PDF, marked 12 February 2023 (46 pages). Main text includes Section 5 and ends on page 23 before references. Appendices are excluded.

- **7 theorems:** 2.7, 2.9 (Main theorem), 2.12, 3.2, 3.5, 3.8 and 3.9. The complete continuation of Theorem 3.2 is included.
- **24 source entries**, 10 auxiliary passages, 53 direct theorem uses and 74 related-theorem connections.
- All six content JSON files passed validation and reproduced byte for byte in `[local path omitted]`.
- Independent review checked original statements, source passages, dependencies, names and highlights. See `registered-source-review.json` and `paper-audit.json`.

The original depth-dependent and revised constant-depth network classes remain distinct. The census preserves total-mean versus component bounds, the complete RSC condition, the sample-split algorithm, and empirical versus population losses. Standing section assumptions are documented separately from explicit theorem hypotheses. Fifteen source notes record ambiguities without repairing original statements or certifying their truth. Algorithm threshold constants deferred to an appendix proof remain explicitly unresolved within the main-text-only scope.

Seven retained scripts support reproduction: `save_inventory.py`, `review_inventory.py`, `extract_interfaces.py`, `save_ambient.py`, `finalize_paper.py`, `rebuild.py` and `save_registered_source_review.py`. From this paper's directory, run `python3 scripts/rebuild.py --output-dir <empty-directory>` to reproduce all six content JSON files. Reproduction does not perform a new semantic source review.
