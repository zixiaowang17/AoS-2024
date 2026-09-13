# Testing network correlation efficiently via counting trees

Status: complete. The registered local arXiv v2 PDF was reviewed directly.

- Two original main-text Theorems: 1 and 2.
- Fourteen original source entries and eight auxiliary passages.
- Eight direct theorem dependencies and twenty-three related connections, independently checked.
- Six content JSON artifacts reproduce byte for byte from seven retained scripts.

The census distinguishes the exact signed-tree statistic from its randomized color-coding approximation. It preserves centered edge weights, edge-set copy multiplicity, automorphism factors, all unrooted tree classes, the exact tree-size condition, the reused threshold and two independent coloring averages. Notes explain the extra randomness implicit in the probability notation and the source’s parameter/runtime limits. Source validation does not certify proofs.

The inspected source is `arXiv:2110.11816v2`, marked 2 April 2022, with cover dated 5 April 2022. Numerical results and acknowledgment end on shared PDF page 22, clipped before Appendix A. The forward reference to appendix equation (54) is resolved through the complete main-text definitions (29)–(32); appendix bodies are excluded.

## Saved artifacts

- `theorem-inventory.json`: both complete original Theorem statements.
- `source-passages.json` and `interface-extraction.json`: original definitions and conditions, natural-language names and literal highlights.
- `ambient-prerequisites.json`: local binders, original conventions, algorithm provenance and source limitations.
- `ranked-interfaces.json`: complete claims, validated dependencies and source-backed connection explanations.
- `paper-audit.json` and `registered-source-review.json`: independent source review and frozen artifact hashes.

## Reproduction

From this paper directory, run:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

The destination must be empty. This regenerates all six content JSON artifacts and compares their bytes with the saved versions, without overwriting audit evidence or performing a new source review. The completed reproduction check is in `evidence/rebuild-check.json`.

Seven scripts preserve the paper-specific work: `save_inventory.py`, `review_inventory.py`, `extract_interfaces.py`, `save_ambient.py`, `finalize_paper.py`, `rebuild.py` and `save_registered_source_review.py`.
