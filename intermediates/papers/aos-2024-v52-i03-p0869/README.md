# Paper census: aos-2024-v52-i03-p0869

Dimension-free mixing times of Gibbs samplers for Bayesian hierarchical models — Filippo Ascolani and Giacomo Zanella.

Source: [arXiv:2304.06993v2](https://arxiv.org/pdf/2304.06993v2), stamped 30 October 2023 and dated 31 October 2023 on the title page, 80 PDF pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i03-p0869.pdf` relative to the repository root. Main text and references end on page 27; appendix mathematics beginning on page 28 was excluded.

Source review and independent validation passed for 4 Theorems, 19 source entries, 20 direct uses and 31 related theorem connections. No census-content correction was needed. Assumptions B4-B6 are defined only in the excluded appendix: their main-text references are retained explicitly as unresolved, linked to Theorems 4.2 and 6.1. Completion of this main-text census does not claim those appendix-only statements have been extracted.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p0869/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
