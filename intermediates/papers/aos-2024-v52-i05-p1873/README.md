# Paper census: aos-2024-v52-i05-p1873

Completed source review of **Spectral statistics of sample block correlation matrices**, using the registered 103-page arXiv:2207.06107v2 PDF dated 8 September 2022. Main text ends on page 34, above Appendix A. The source was not replaced with the published version.

The census contains six complete original Theorems, 20 API groups and 21 source entries, with 54 direct group/Theorem uses and 79 related connections. The 55 direct local uses include two distinct spectral-statistic entries used by Theorem 1.20; these count once at group level. Fifteen auxiliary passages and 25 source issues preserve the observation model, conventions, inherited Corollaries and unresolved source meanings.

- `theorem-inventory.json`: all six original Theorem statements.
- `source-passages.json`: original definitions, assumptions and other relevant source entries.
- `ranked-interfaces.json`: complete theorem-to-interface census.
- `ambient-prerequisites.json`: auxiliary statements, inheritance and source issues.
- `paper-audit.json` and `registered-source-review.json`: source review and independent validation evidence.

Theorem 1.20 retains the conclusions of Theorems 1.11, 1.17 and 1.18 and Corollaries 1.14 and 1.15 under the replacement moment assumption. Its dependency closure does not retain the stronger all-moment Assumption 1.6. Theorem 5.3 is included because its proof section remains part of the main text.

Apparent source errors in the density, centering, Corollary scale and contour formulas are preserved rather than silently corrected. Validation establishes fidelity of this census; it does not certify mathematical correctness or proofs.

Seven per-paper Python scripts are retained. All six content artifacts reproduce byte for byte. From the workspace, rebuild into an empty directory with:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p1873/scripts/rebuild.py --output-dir [local path omitted]
```

Rebuilding reproduces the saved extraction and does not perform a new source review.
