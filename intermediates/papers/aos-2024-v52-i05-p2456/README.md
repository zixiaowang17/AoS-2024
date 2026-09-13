# A Gaussian process approach to model checks

Status: complete. The registered local IMS manuscript was reviewed directly.

- Three original main-text Theorems: 4.1, 4.3 and 4.4.
- Twenty-three original definition, assumption and source entries; nine auxiliary passages.
- Fifteen direct theorem dependencies and forty related connections, independently checked.
- All six content JSON artifacts reproduce byte for byte from the seven retained scripts.

The abstract dual-space theorem is kept separate from the model-checking and bootstrap applications. Assumption B includes only its preceding parts (i)–(iv); later local-power part (v), Assumption C and proof-only results are not imported. Source notes preserve the bootstrap theorem’s missing explicit null premise, its almost-sure convergence claim, the distinct spectral normalizations and other notation limitations. Source validation does not certify proofs.

The source is the hash-verified IMS manuscript `AOS2401-003R2A0.pdf`, marked Submitted to the Annals of Statistics. Main-text evidence ends at line 639 on PDF page 20, clipped before the appendix. Source identity and the paper link are in `theorem-inventory.json` and `evidence/source-provenance.json`.

## Artifacts

- `theorem-inventory.json`: all complete original Theorem statements.
- `source-passages.json` and `interface-extraction.json`: original definitions/conditions, source names and literal highlights.
- `ambient-prerequisites.json`: source scope, local binders, auxiliary passages and unresolved notation.
- `ranked-interfaces.json`: validated paper-local dependencies, original claims and source explanations.
- `paper-audit.json` and `registered-source-review.json`: completed source review with frozen content hashes.

## Reproduction

From this paper directory, run:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

The destination must be empty. This regenerates the six content artifacts and compares their bytes with the saved versions; it does not perform a new source review or overwrite existing audit evidence. The completed check is saved in `evidence/rebuild-check.json`.

Seven scripts retain the paper-specific work: `save_inventory.py`, `review_inventory.py`, `extract_interfaces.py`, `save_ambient.py`, `finalize_paper.py`, `rebuild.py` and `save_registered_source_review.py`.
