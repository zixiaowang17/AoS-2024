# Estimating a density near an unknown manifold: A Bayesian nonparametric approach

Completed source census of the registered local manuscript `2205.15717v3.pdf`,
dated 17 July 2024. The 73-page PDF is pinned by its SHA-256. The main text ends
on page 29 before References; appendix bodies are excluded.

- `theorem-inventory.json`: complete original Theorems 3.1 and 3.4.
- `source-passages.json`: 19 original definition, condition and source entries.
- `ambient-prerequisites.json`: 14 supporting passages, all four prior-condition combinations, and 12 source issues.
- `ranked-interfaces.json`: 19 direct uses and 28 related theorem connections.
- `paper-audit.json` and `registered-source-review.json`: independent source-review and validation records.
- `scripts/`: retained extraction, reconstruction and review scripts.

The census preserves mixed-derivative Hölder regularity, normalized chart
pullbacks, geometric Gaussian covariances, and the distinct prior alternatives.
Table 1 is recorded as four combinations: one weight family and one scale family.
The deterministic approximation theorem does not inherit posterior or prior
requirements from its use in the contraction proof.

Definitions and constructions deferred exclusively to appendices remain explicit
unresolved references. Other recorded issues include the zero-order exponent and
swapped indices in (15), offset boundary wording, and the locality of chart
inverses in Theorem 3.4. Original statements are preserved without repairs.

Reproduce the six content artifacts in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2081/scripts/rebuild.py --output-dir [local path omitted]
```

Rebuilding validates structure and compares output bytes with the saved files.
It does not perform another semantic review. Completion certifies the source
census and data validation, not the mathematical proofs.
