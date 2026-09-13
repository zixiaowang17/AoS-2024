# Rates of estimation for high-dimensional multireference alignment

Source: the registered 24-page published PDF, DOI 10.1214/23-AOS2346.
Scope: every main-text Theorem; supplementary appendices excluded.

## Results

- `theorem-inventory.json`: four complete original statements (2.1, 2.2, 4.1, 5.2).
- `ranked-interfaces.json`: 13 source entries with 15 direct uses and 27 related-theorem connections.
- `source-passages.json`: the original definitions, assumptions and estimator descriptions.
- `ambient-conventions.json`: four auxiliary passages and unresolved source conventions.
- `registered-source-review.json`: current PDF review, artifact hashes and independent validation results.
- `evidence/revalidation/`: fresh PDF evidence and the artifact reproduction check.

The original census content is unchanged by registered-source revalidation.

## Rebuild the census

From this paper's directory, choose an empty output directory:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

This resolves the verified local PDF, runs the saved extraction and finalization
scripts, validates the regenerated inventory and census, and compares six JSON
artifacts with the saved results. It preserves the existing audit. The recorded
rebuild reproduced all six artifacts byte for byte.

The scripts contain the manually reviewed transcriptions and dependency choices.
Rebuilding does not perform another semantic source review. A content change must
be checked against the PDF before updating the review and completion status.

`scripts/save_inventory.py` now uses the fixed local PDF source and renders its own
evidence. Its previous version is preserved in
`review-history/before-local-source-rebuild/scripts/`.
