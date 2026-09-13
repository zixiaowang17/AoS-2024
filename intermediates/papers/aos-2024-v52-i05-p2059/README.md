# A conformal test of linear models via permutation-augmented regressions

Completed source census of the registered local arXiv manuscript
`2309.05482v3.pdf`, dated 27 December 2023. The 36-page PDF is pinned by its
SHA-256. The main text ends on page 28, before References; appendix bodies are
excluded.

- `theorem-inventory.json`: the complete original Theorems 3.3 and 4.4.
- `source-passages.json`: 11 original model, assumption, condition and construction entries.
- `ambient-prerequisites.json`: 11 supporting passages, dependency scopes and 11 source issues.
- `ranked-interfaces.json`: 9 direct uses and 15 related theorem connections.
- `paper-audit.json` and `registered-source-review.json`: source-review and independent validation records.
- `scripts/`: retained extraction, reconstruction and review scripts.

The general theorem substitutes its own statistic into the p-value recipe. Its
dependencies therefore remain separate from the concrete PALMRT residual
statistics and projections required for confidence-interval construction.

The source has several inconsistencies in the interval construction, including
references to the wrong result or algorithm, conflicting comparison formulas,
and unspecified boundary cases. Original statements are preserved, with the
discrepancies recorded separately. Completion certifies the source census and
data validation; it does not certify the mathematical assertions or repair the
algorithm.

Reproduce the six content artifacts in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2059/scripts/rebuild.py --output-dir [local path omitted]
```

The rebuild validates structure and compares output bytes with the saved files.
It does not perform a new semantic review of the source.
