# Paper census: aos-2024-v52-i02-p0602

ℓ2 inference for change points in high-dimensional time series via a Two-Way MOSUM — Jiaqi Li, Likai Chen, Weining Wang and Wei Biao Wu.

Source: [arXiv:2208.13074v2](https://arxiv.org/pdf/2208.13074v2), stamped 4 July 2023, 111 pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i02-p0602.pdf` relative to the repository root. Main text and references end on page 37; Appendix A starts on page 38 and is excluded.

Source review and independent validation passed for 4 Theorems, 39 source entries, 34 direct uses and 59 related theorem connections. Theorem 1 includes its continuation onto page 11.

Revalidation restored the source term “long-run variance matrix” in D5 and its name, keyword and highlight phrase. A review note was clarified to avoid implying continuity of the density in Assumption 8. All theorem statements, mathematical formulas and dependency relationships are unchanged. Source ambiguities in signs, scales, coupling domains and covariance specifications remain documented separately.

- [Complete original theorem statements](theorem-inventory.json)
- [Original definitions, assumptions and source passages](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)
- [Prior audit before correction](review-history/before-local-source-rebuild/paper-audit.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i02-p0602/scripts/rebuild.py --output-dir [local path omitted]
```

The script resolves the registered local PDF, reconstructs the saved extraction, validates structure and compares the outputs with the saved artifacts. It does not perform a new manual source review. Previous artifacts and scripts remain in `review-history/before-local-source-rebuild/`.
