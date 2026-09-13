# Paper census: aos-2024-v52-i03-p0895

Reconciling model-X and doubly robust approaches to conditional independence testing — Ziang Niu, Abhinav Chakraborty, Oliver Dukes and Eugene Katsevich.

Source: [arXiv:2211.14698v2](https://arxiv.org/pdf/2211.14698v2), stamped 8 February 2023 and dated 10 February 2023 on the title page, 75 PDF pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i03-p0895.pdf` relative to the repository root. References finish above y=288.68743896484375 on shared page 34; appendix mathematics at and below that boundary was excluded.

Source review and independent validation passed for 3 Theorems, 21 source entries, 25 direct uses and 37 related theorem connections. No census-content correction was needed. Conditional resampling convergence, null decision equivalence and local GCM optimality retain their distinct hypotheses. The GCM-only theorem does not acquire a predictor-resampling requirement. Original statements, source conventions and the historical audit are preserved.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p0895/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
