# Leave-one-out singular subspace perturbation analysis for spectral clustering

Completed census of the registered local arXiv:2205.14855v2 PDF (14 January 2024).
The source has 50 pages; the inspected main text ends with Acknowledgements on
page 28. Appendix bodies are excluded.

- `theorem-inventory.json`: all nine main-text Theorems, with complete original statements.
- `source-passages.json`: 17 original definition, model, algorithm and condition entries.
- `ambient-prerequisites.json`: nine auxiliary passages, local bindings, scoped references and nine source issues.
- `ranked-interfaces.json`: 45 direct uses and 56 related theorem connections, with original source names and highlight selectors.
- `paper-audit.json` and `registered-source-review.json`: independent review and validation records.
- `scripts/`: the retained extraction, reconstruction and review scripts for this paper.

Theorem 5.1 is included because its proof-section location is still main text.
Lemma 3.4 is not counted as a Theorem, but its assumptions and rate (31) are
preserved because Theorem 3.5 explicitly refers to them.

The source prints an equality inside the misclustering-error indicator and an
inequality in a later formula. Both are retained, with the discrepancy recorded
separately. Other unresolved source conventions are also recorded without
rewriting the original statements. Completion certifies source review and data
validation, not the truth of the mathematical claims.

Reproduce the six JSON content artifacts in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2004/scripts/rebuild.py --output-dir [local path omitted]
```

The rebuild validates the generated structure and compares the outputs byte for
byte with the saved artifacts. It does not perform a new semantic source review.
