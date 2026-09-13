# Efficiency in local differential privacy

Source census completed against the registered local arXiv v3 PDF (7 March 2024), 52 pages, DOI `10.1214/24-AOS2425`. Source SHA-256: `e76bf0281de05dc5366deaa7a98f870d843e92ad9b9cd69565a0e75006e818d2`.

- **7 theorems**: 3.3, 3.5, 4.1, 4.2, 4.3, 4.11 and 4.12, preserving complete original statements.
- **15 source entries** covering privacy mechanisms, DQM/Fisher information, LAMN, likelihood and truncation, separate C1–C3 conditions, quantization and the full two-step estimator.
- **14 supporting passages**, **31 direct uses**, and **41 related theorem connections**.
- Main text ends with Funding on PDF page 29; the appendix on that page is excluded.

Theorem 4.1 is a classical raw-likelihood result with no ranked direct interfaces; its ambient model and local binders are preserved. Theorem 3.5 imports the information definition from 3.3, not its LAMN conclusion. Theorem 4.3 does not assume DQM. Theorem 4.12 assumes consistency of the final MLE; it does not establish it unconditionally.

Original source issues are recorded separately, including the moment estimator inverse domain, the cross-parameter nonnegative bound in Theorem 4.11, and the bounded domain called a cone in Lemma 4.5. The census preserves these statements and does not certify their proofs.

## Artifacts

`theorem-inventory.json` stores the statements; `source-passages.json` stores original definitions and conditions; `interface-extraction.json` and `ranked-interfaces.json` store their relationships. `ambient-prerequisites.json` records supporting definitions, source issues and theorem-local bindings. Source checks are saved in `inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/`.

## Reproduction

All seven per-paper Python scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2139/scripts/rebuild.py --output-dir [local path omitted]
```

The completed rebuild matched all six artifacts byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure. It does not perform a new semantic source review.
