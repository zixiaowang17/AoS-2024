# Paper census: aos-2024-v52-i03-p1027

High-dimensional covariance matrices under dynamic volatility models: Asymptotics and shrinkage estimation — Yi Ding and Xinghua Zheng.

Source: [arXiv:2211.10203v2](https://arxiv.org/pdf/2211.10203v2), 49 PDF pages, with margin date 21 November 2022 and title-page date 18 November 2022. The fixed source is `local-pdfs/aos/2024/aos-2024-v52-i03-p1027.pdf` relative to the repository root. Main text and references occupy pages 1–36, including numbered Section 5. The attached supplement starts on page 37; only its title was inspected.

Source review and independent validation passed for 5 Theorems, 24 source entries, 30 direct uses and 61 related theorem connections. Two original-prose transcriptions on page 10 were corrected: D18 now retains “determined by H in that,” and auxiliary A12 retains “has the same LSD.” The theorem inventory and dependency graph are unchanged. Previous artifacts are preserved in `review-history/before-stieltjes-prose-correction/`.

The external Ledoit–Wolf nonlinear shrinkage algorithm remains explicitly unresolved because its complete construction is not given in the inspected main text. The 12 auxiliary passages and 27 source notes preserve source formulas and ambiguities, including the QMLE optimization direction, differing transform normalizations and oracle denominator. This census does not repair the formulas, certify proofs or assert equivalence to the final journal version.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-prerequisites.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1027/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the pre-correction paper audit is preserved in the correction archive.
