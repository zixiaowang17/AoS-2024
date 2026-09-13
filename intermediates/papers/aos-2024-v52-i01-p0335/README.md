# Adaptive variational Bayes: Optimality, computation and applications

Source: [arXiv:2109.03204v4](https://arxiv.org/pdf/2109.03204v4), 11 March 2024, 94 pages. The census covers the main document through PDF page 29; appendices are excluded. The registered local PDF is resolved using `scripts/resolve_paper_pdf.py` from the repository root.

## Saved census

- [theorem-inventory.json](theorem-inventory.json): 14 complete original theorem statements.
- [ranked-interfaces.json](ranked-interfaces.json): 49 source entries, 94 direct theorem uses and 178 related theorem connections.
- [source-passages.json](source-passages.json): original definitions, assumptions and conditions.
- [ambient-conventions.json](ambient-conventions.json): eight auxiliary passages and unresolved source conventions.
- [registered-source-review.json](registered-source-review.json): source comparison, evidence hashes and independent validation.

## Reproduce the extracted content

From this paper directory, run:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

The destination must be empty. The script verifies the registered source and regenerates six census JSON files, then compares them byte for byte with the saved files. It preserves the existing audit. Rebuilding and structural validation do not perform a new manual source review.

Per-paper extraction scripts are preserved under `scripts/`; earlier versions are archived under `review-history/before-local-source-rebuild/scripts/`. The successful reproduction check is saved in [evidence/revalidation/rebuild-check.json](evidence/revalidation/rebuild-check.json).
