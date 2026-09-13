# Paper census: aos-2024-v52-i03-p0948

On blockwise and reference panel-based estimators for genetic data prediction in high dimensions — Bingxin Zhao, Shurong Zheng and Hongtu Zhu.

Source: [arXiv:2203.12003v1](https://arxiv.org/pdf/2203.12003v1), 60 PDF pages. The artifact prints a 22 March 2022 margin date and a 13 June 2025 title-page date; the reason for this discrepancy is not established. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i03-p0948.pdf` relative to the repository root. Main text and references occupy pages 1–27. Attached supplementary mathematics on pages 28–60 was excluded; only its title heading was inspected.

Source review and independent validation passed for 4 Theorems, 23 source entries, 38 direct uses and 53 related theorem connections. No census-content correction was needed. Trace-only results remain separate from prediction results. Training, external-reference and testing covariance estimates retain their original definitions and sample-size factors. All 28 source conventions and the historical audit are preserved.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p0948/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
