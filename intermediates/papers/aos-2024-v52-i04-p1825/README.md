# Paper census: aos-2024-v52-i04-p1825

Completed source review of the registered 19-page arXiv:2307.08136v3 PDF (9 July 2024). The main text ends after Acknowledgements on PDF page 18, before References. No appendix material or replacement PDF was used.

The census contains five complete original Theorems, 17 source entries, 30 direct theorem uses, 54 related connections and nine auxiliary passages. Original statements are saved in `theorem-inventory.json`; definitions and conditions in `source-passages.json`; the finalized census in `ranked-interfaces.json`. Twenty-two source issues and unexpanded external conventions are recorded in `ambient-prerequisites.json`.

Independent source review, original-inventory handoff, graph reconstruction, keywords/highlights and structural validation passed. `paper-audit.json` and `registered-source-review.json` preserve the reviewed hashes and findings. All six content artifacts reproduce byte for byte; seven paper-specific scripts are retained.

To reproduce the saved extraction in an empty directory, run from this workspace:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1825/scripts/rebuild.py --output-dir [local path omitted]
```

Rebuilding is not a new source review. The census preserves the source's mathematical assertions and ambiguities; it does not certify proofs. In particular, it retains the inverse-Poincare square discrepancy, the likelihood argument order, the vector-space norm subscripts, the different observation windows, and Theorem 5's explicit inheritance of all Theorem 3 conclusions.
