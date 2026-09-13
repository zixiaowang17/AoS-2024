# Paper census: aos-2024-v52-i02-p0842

Parameter estimation in nonlinear multivariate stochastic differential equations based on splitting schemes — Predrag Pilipovic, Adeline Samson and Susanne Ditlevsen.

Source: [Published Annals of Statistics 52(2), 842–867 (2024)](https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-2/Parameter-estimation-in-nonlinear-multivariate-stochastic-differential-equations-based-on/10.1214/24-AOS2371.pdf), 26 PDF pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i02-p0842.pdf` relative to the repository root. Separate supplementary article and code files linked on page 23 were excluded; references end on page 26.

Source review and independent validation passed for 5 Theorems, 18 source entries, 39 direct uses and 50 related theorem connections. Numerical trajectory convergence and statistical parameter convergence retain their distinct conditions and sampling regimes. The estimator theorems preserve their references to approximate objectives (22)/(23); the full objectives remain separate source context. No census-content correction was needed; all original artifacts and their audit are preserved.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i02-p0842/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
