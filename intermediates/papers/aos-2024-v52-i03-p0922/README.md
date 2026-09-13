# Paper census: aos-2024-v52-i03-p0922

Distributed estimation and inference for semiparametric binary response models — Xi Chen, Wenbo Jing, Weidong Liu and Yichen Zhang.

Source: [arXiv:2210.08393v4](https://arxiv.org/pdf/2210.08393v4), stamped 15 August 2024, 102 PDF pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i03-p0922.pdf` relative to the repository root. Main text and references occupy pages 1–40. Appendix mathematics on pages 41–102 was excluded; only the appendix heading was inspected to establish the boundary.

Source review and independent validation passed for 8 Theorems, 25 source entries, 66 direct uses and 89 related theorem connections. No census-content correction was needed. Homogeneous, covariate-shift, coefficient-shift and sparse settings retain their distinct assumptions and estimators. Original statements, all 27 source conventions and the historical audit are preserved.

Theorem 5.2 explicitly defers its exact tuning choices and the formal definition of r_m to Appendix A. These remain recorded as unresolved within the main-text-only scope.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p0922/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
