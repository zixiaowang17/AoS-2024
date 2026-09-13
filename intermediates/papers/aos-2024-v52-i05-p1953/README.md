# Improved covariance estimation: optimal robustness and sub-Gaussian guarantees under heavy tails

Paper ID: `aos-2024-v52-i05-p1953`.

Status: **complete** for the registered arXiv:2209.13485v2 PDF, stamped 25 March 2024. Main text ends on PDF page 26; appendices are excluded. This review does not assume equivalence to the published article.

The census preserves **one complete theorem statement**, **four original source entries**, and **four auxiliary passages**. Seven source issues are recorded separately without rewriting the original. Result 2.2 is printed as Proposition, so prose citations calling it Theorem do not add it to the inventory.

- `theorem-inventory.json`: complete original Theorem 1.3.
- `ranked-interfaces.json`: covariance, Assumption 1.2, moment constant and stable rank, with source names, highlights and theorem links.
- `source-passages.json` and `interface-extraction.json`: retained extraction records.
- `ambient-prerequisites.json`: original notation, local bindings and source issues.
- `paper-audit.json` and `registered-source-review.json`: source review, independent validation and hashes.
- `evidence/rebuild-check.json`: exact reproduction of all six content artifacts.

The paper-specific scripts are retained in `scripts/`. Reproduce into an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p1953/scripts/rebuild.py --output-dir [local path omitted]
```

`save_inventory.py` retains the theorem transcription; `build_census.py` retains the source passages and dependency choices. `review_inventory.py` and `save_registered_source_review.py` check the frozen reviewed content independently of the extraction builder. Rebuilding does not perform a new semantic review or certify proofs.
