# Supervised homogeneity fusion: A combinatorial approach

The source is the registered 31-page arXiv:2201.01036v1 PDF, stamped 4 January
2022. This census is specific to that version. Main-text pages 1-19 are included;
appendices starting on page 20 are excluded.

## Results

- `theorem-inventory.json`: complete Theorems 2.4, 2.5 and 3.2.
- `ranked-interfaces.json`: 14 source entries, 12 direct uses and 21 related-theorem connections.
- `source-passages.json`: original definitions, conditions and algorithm statements.
- `ambient-conventions.json`: four source auxiliaries and six unresolved source-convention notes.
- `registered-source-review.json`: the registered-PDF review and independent validation record.
- `source-transcription-corrections.json`: the restored article in “Define the parameter space” (D2, page 5).
- `evidence/revalidation/`: fresh main-text evidence, an appendix-heading-only crop and the rebuild check.

## Rebuild

From this paper directory, choose an empty output directory:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

This resolves the registered local PDF, regenerates the saved extraction, validates
its structure and compares six JSON artifacts with the reviewed results. All six
were reproduced byte for byte. Existing audit records are preserved. Rebuilding
uses the manually reviewed transcriptions; it does not perform another semantic
review of the paper.

Previous artifacts and scripts are retained in
`review-history/before-registered-source-review/`.
