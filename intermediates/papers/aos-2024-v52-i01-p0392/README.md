# Paper census: aos-2024-v52-i01-p0392

Estimation and inference for minimizer and minimum of convex functions: Optimality, adaptivity and uncertainty principles.

Source: [arXiv:2305.00164v2](https://arxiv.org/pdf/2305.00164v2), 26 pages, stamped 10 March 2024. The registered local PDF is `local-pdfs/aos/2024/aos-2024-v52-i01-p0392.pdf` relative to the repository. SHA-256: `38d889e7127d0a91f4cd268fc84157a395dea6d75fecdfbd9b12ef11f07d9f7c`.

The completed source review retains 11 theorems, 37 source entries, 45 direct uses and 100 related-theorem connections. The separate supplement is excluded.

- [theorem-inventory.json](theorem-inventory.json): complete original theorem statements in source order.
- [ranked-interfaces.json](ranked-interfaces.json): original definitions and conditions, source terminology, highlights and theorem relationships.
- [source-passages.json](source-passages.json): paper-local source entries and dependency reasons.
- [ambient-conventions.json](ambient-conventions.json): four auxiliary passages and unresolved source conventions.
- [registered-source-review.json](registered-source-review.json): registered-PDF review, evidence hashes and independent validation results.
- [source-transcription-corrections.json](source-transcription-corrections.json): four repaired naming-context quotations whose LaTeX was corrupted by Python string escapes.

The white-noise and regression procedures remain distinct. Printed source discrepancies are preserved and explained separately; this census does not certify proofs. Previous artifacts and scripts are archived under `review-history/before-registered-source-review/`.

To reproduce the six content artifacts in an empty directory, run from the repository root:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i01-p0392/scripts/rebuild.py --output-dir [local path omitted]
```

The paper-specific extraction scripts preserve the reviewed statements and dependency choices. Rebuilding resolves and verifies the registered source, validates structure, and compares output bytes with the saved artifacts. It does not perform a new manual PDF review or overwrite the review records. The successful reproduction check is saved in `evidence/revalidation/rebuild-check.json`.
