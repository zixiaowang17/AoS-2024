# On the statistical complexity of sample amplification

Source-reviewed census of the registered local arXiv:2201.04315v2 PDF (62 pages), stamped 18 September 2024 with title-page date 19 September 2024. Main text ends on page 22; all appendices are excluded.

- **11 theorems:** 4.5, 4.6, 5.2, 5.5, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2 and 7.3. The continuation of Theorem 6.3 is included.
- **23 source entries**, 10 auxiliary passages, 40 direct theorem uses and 61 related-theorem connections.
- All six content JSON files passed validation and reproduced byte for byte in `[local path omitted]`.
- Independent source review checked statements, definitions, assumptions, dependencies, names and highlights. See `registered-source-review.json` and `paper-audit.json`.

The census preserves the distinction between amplification existence, minimax error and maximal additional sample size; the exact divergence normalizations; componentwise versus full-family moment conditions; and the different Gaussian and density models. Proof-only shuffling algorithms, decision risks and sufficient moment criteria remain separate from theorem requirements. Fourteen notes record source ambiguities, including singular covariance and sample-size endpoints, without repairing original statements or certifying their truth.

Seven retained scripts support reproduction: `save_inventory.py`, `review_inventory.py`, `extract_interfaces.py`, `save_ambient.py`, `finalize_paper.py`, `rebuild.py` and `save_registered_source_review.py`. From this paper's directory, run `python3 scripts/rebuild.py --output-dir <empty-directory>` to reproduce all six content JSON files. Rebuilding does not constitute a new semantic source review.
