# Stereographic Markov chain Monte Carlo

Source-reviewed census of the registered local arXiv:2205.12112v2 PDF, marked 21 February 2024 (80 pages). Main text ends on page 24. Supplementary proofs and simulations are excluded.

- **5 theorems:** 2.1, 2.2, 4.1, 5.1, 5.2.
- **14 source entries**, 10 auxiliary passages, 19 direct theorem uses and 25 related-theorem connections.
- All six content JSON files passed validation and reproduced byte for byte in `[local path omitted]`.
- Independent review checked original statements, source passages, dependencies, names and highlights. See `registered-source-review.json` and `paper-audit.json`.

The original SPS, continuous-time SBPS and revised RSPS remain distinct. The ESJD theorem uses the exact joint expectation; the diffusion theorem applies to RSPS, while its SPS analogue remains a conjecture. Fourteen source notes preserve notation and algorithm conventions without rewriting the original statements or certifying their mathematical correctness.

The seven retained scripts are `save_inventory.py`, `review_inventory.py`, `extract_interfaces.py`, `save_ambient.py`, `finalize_paper.py`, `rebuild.py` and `save_registered_source_review.py`. From this paper's directory, run `python3 scripts/rebuild.py --output-dir <empty-directory>` to reproduce all six content JSON files. Reproduction does not constitute a new semantic source review.
