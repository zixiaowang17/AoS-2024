# Exact minimax optimality of spectral methods in phase synchronization and orthogonal group synchronization

Completed source census of the registered local manuscript `2209.04962v2.pdf`.
Its arXiv stamp is dated 6 January 2024 and its cover 9 January 2024. The
41-page PDF is pinned by its SHA-256. The main text ends on page 29 before
References; appendix bodies are excluded.

- `theorem-inventory.json`: all four original Theorems, including the no-noise consequences in Theorems 1 and 2.
- `source-passages.json`: 9 original model, estimator, parameter-space and loss entries.
- `ambient-prerequisites.json`: 12 supporting passages, dependency scopes and 7 source issues.
- `ranked-interfaces.json`: 12 direct uses and 18 related theorem connections.
- `paper-audit.json` and `registered-source-review.json`: source-review and independent validation records.
- `scripts/`: retained extraction, reconstruction and review scripts.

The asymptotic and finite-sample theorems are retained separately. Each model
keeps its own Gaussian noise convention, matrix completion, estimator and loss.
The phase estimator's zero-coordinate fallback and the orthogonal estimator's
singular-block fallback are preserved. Population approximations and perturbation
lemmas remain proof-only relationships.

The printed orthogonal loss has a free block index and no sum, despite the text
describing it as analogous to the summed phase loss. This ambiguity and other
source inconsistencies are recorded without changing the original definitions.

Reproduce the six content artifacts in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2112/scripts/rebuild.py --output-dir [local path omitted]
```

Rebuilding validates structure and compares output bytes with the saved files.
It does not perform another semantic review. Completion certifies the source
census and data validation, not the mathematical proofs.
