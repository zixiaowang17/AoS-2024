# Testing for independence in high dimensions based on empirical copulas

The source is the registered 51-page arXiv:2204.01803v1 PDF. This census is
specific to that preprint. Main-document pages 1-30 are included; supplementary
appendices starting on page 31 are excluded.

## Results

- `theorem-inventory.json`: complete Theorems 3.1 and 6.5, including the attributed theorem in the main-text proofs section.
- `ranked-interfaces.json`: 13 source entries, seven direct uses and 13 related-theorem connections.
- `source-passages.json`: original definitions, statistical constructions and theorem conditions.
- `ambient-conventions.json`: six auxiliary passages and eight unresolved source-convention notes.
- `registered-source-review.json`: registered-PDF review and independent validation results.
- `evidence/revalidation/`: fresh main-document evidence, supplement-heading crop and rebuild check.

The original census content is unchanged. In particular, equation (6.24) prints
an unsquared martingale difference. That source formula is preserved and flagged,
not silently replaced or certified as mathematically correct.

## Rebuild

From this paper directory, choose an empty output directory:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

The script verifies the registered local PDF, regenerates the saved transcriptions
and dependencies, runs structural validation and compares six JSON artifacts with
the reviewed results. All six were reproduced byte for byte. Existing audit
records are preserved. Regeneration is not another semantic review of the PDF.

Previous inventory and auxiliary writers are archived in
`review-history/before-local-source-rebuild/scripts/`.
