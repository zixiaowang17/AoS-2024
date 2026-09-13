# Quantile processes and their applications in finite populations

Source census completed against the registered local **arXiv:2407.21238v2, dated 29 November 2024**, 106 pages, DOI `10.1214/24-AOS2432`.

Source SHA-256: `c6a7f1af69047f6993261caff6f851a5596b55ab10385c037788ee76afafa3e7`.

- **10 theorems**: 3.1, 3.2, 4.1, 5.1–5.4 and 6.1–6.3.
- **37 source entries**, **14 supporting passages**, **122 direct uses** and **171 related connections**.
- Main text ends on PDF page 29 before the Appendix heading; appendix bodies are excluded.

The census preserves all four quantile estimators, all eleven assumptions, the sampling designs, both fixed and growing stratum regimes, covariance kernels and variance estimators. References to an earlier theorem’s conclusion are distinguished from references to its assumptions. A theorem’s dependency union records use in its alternative branches; it does not conjoin those branches.

Exact plug-in substitutions appear only in supplement Tables 5 and 6. GREG and some sampling constructions are externally cited without complete main-text formulas. These references remain unresolved. Fifteen notes document source scope and typography, including expectation parentheses, moment powers, repeated-index positive definiteness, comparison assumptions and superpopulation centering. Original statements are preserved without silently correcting them.

## Artifacts

`theorem-inventory.json` contains every original theorem statement. `source-passages.json` contains the definitions, assumptions and other source excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` retains supporting passages, theorem-local bindings and unresolved references.

Source checks are recorded in `inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/`. Independent heading enumeration, source-specific checks, dependency reconstruction and schema validation passed.

## Reproduction

All seven per-paper Python scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2194/scripts/rebuild.py --output-dir [local path omitted]
```

All six artifacts reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and checks its structure; it does not perform a new semantic source review.
