# The projected covariance measure for assumption-lean variable significance testing

Source-reviewed census of the registered local arXiv:2211.02039v4 PDF (97 pages), stamped 7 May 2024, with title-page date 8 May 2024. Main text ends after acknowledgements before References on page 29; all supplementary bodies are excluded.

- Four theorems: 4, 5, 6 and 7, including the page 21–22 continuation of Theorem 6.
- 27 original source entries, nine auxiliary passages, 39 direct uses and 62 related-theorem connections.
- All six content JSONs passed structural checks and reproduced byte for byte in `[local path omitted]`.
- Independent source review checked original statements, source passages, dependency paths, natural-language names and highlights. See `registered-source-review.json` and `paper-audit.json`.

The census preserves the distinction between conditional mean independence and full conditional independence, response and projection residuals, the exact auxiliary training splits, and the separate generic and spline theorem requirements. Spline regression overrides the general variance-estimation step. Eleven source notes retain the printed one-sided bound, moment-quantifier ambiguity, zero/correlation conventions and unresolved supplementary stability, Hölder and spline definitions. Source review does not certify proofs or fill those omissions.

Seven retained scripts support reproduction: `save_inventory.py`, `review_inventory.py`, `extract_interfaces.py`, `save_ambient.py`, `finalize_paper.py`, `rebuild.py` and `save_registered_source_review.py`. From this directory run `python3 scripts/rebuild.py --output-dir <empty-directory>`. Rebuilding does not constitute a new semantic source review.
