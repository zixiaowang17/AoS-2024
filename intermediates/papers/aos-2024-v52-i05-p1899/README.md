# Joint sequential detection and isolation for dependent data streams

Paper ID: `aos-2024-v52-i05-p1899`.

Status: **complete** for the registered arXiv:2207.00120v1 source. Main text ends on PDF page 25; appendices are excluded. This census does not assert that the registered preprint and published article are interchangeable.

The census preserves **20 complete theorem statements**, **41 original definition/assumption/source entries**, and **23 auxiliary scope passages**. Source review records 24 unresolved source conventions or apparent inconsistencies without altering the original text. The dependency index contains 201 direct uses and 484 related theorem connections; conditional branches retain their own scope.

- `theorem-inventory.json`: source-ordered complete original Theorems.
- `ranked-interfaces.json`: definitions, assumptions, keywords, highlights and theorem dependencies.
- `source-passages.json` and `interface-extraction.json`: retained extraction artifacts.
- `ambient-prerequisites.json`: original scope context, local bindings and source issues.
- `paper-audit.json` and `registered-source-review.json`: source review, independent validation and artifact hashes.
- `evidence/rebuild-check.json`: byte-for-byte reproduction of all six census content artifacts.

The per-paper scripts are retained in `scripts/`. Reproduce into an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p1899/scripts/rebuild.py --output-dir [local path omitted]
```

`save_inventory.py` preserves the original transcription; `extract_interfaces.py` and `save_ambient.py` preserve source passages and scope; `finalize_paper.py` saves dependencies and derived metrics. `review_inventory.py` and `save_registered_source_review.py` check the frozen reviewed content independently of the extraction graph. Rebuilding does not perform a new source review or certify the mathematical proofs.
