# Rank and factor loadings estimation in time series tensor factor model by pre-averaging

Source: [arXiv:2208.04012v1](https://arxiv.org/pdf/2208.04012v1), 8 August 2022, 80 pages. The census covers main-text pages 1-38; appendices are excluded. Resolve the fixed local PDF with `scripts/resolve_paper_pdf.py` from the repository root.

## Saved census

- [theorem-inventory.json](theorem-inventory.json): seven complete original theorem statements, numbered 1, 2, 4, 6, 7, 8 and 9.
- [ranked-interfaces.json](ranked-interfaces.json): 25 source entries, 78 direct theorem uses and 103 related theorem connections.
- [source-passages.json](source-passages.json): original definitions, assumptions and conditions.
- [ambient-conventions.json](ambient-conventions.json): ten auxiliary passages and unresolved source conventions.
- [registered-source-review.json](registered-source-review.json): source comparison, evidence hashes and independent validation.
- [source-transcription-corrections.json](source-transcription-corrections.json): four restored tilde accents and one clarified inherited-condition explanation; earlier artifacts remain archived.

## Reproduce the extracted content

From this paper directory, run:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

The destination must be empty. The script verifies the registered PDF, regenerates six census JSON files and checks them byte for byte against the saved files. It preserves the existing audit. Rebuilding and structural validation do not perform a new manual source review.

Per-paper extraction scripts are preserved under `scripts/`; their previous versions and JSON are under `review-history/before-registered-source-review/`. The successful reproduction report is [evidence/revalidation/rebuild-check.json](evidence/revalidation/rebuild-check.json).
