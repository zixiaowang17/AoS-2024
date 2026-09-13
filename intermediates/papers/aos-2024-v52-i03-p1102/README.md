# Paper census: aos-2024-v52-i03-p1102

MARS via LASSO — Dohyeong Ki, Billy Fang and Adityanand Guntuboyina.

Source: [arXiv:2111.11694v5](https://arxiv.org/pdf/2111.11694v5), dated 13 October 2024, 108 PDF pages. The fixed source is `local-pdfs/aos/2024/aos-2024-v52-i03-p1102.pdf` relative to the repository root. Main text and references end on page 25. Only the appendix roadmap and heading on page 26 were inspected to confirm the boundary; appendix mathematics was excluded.

Source review and independent validation passed for 7 Theorems, 22 source entries, 32 direct uses and 62 related theorem connections. No census-content correction was needed. Every theorem is preserved in full, including both entropy bounds, the approximate-estimator grid requirement and the minimax lower bound.

The exact and approximate estimators, fixed and random designs, and expected and in-probability loss guarantees retain their distinct prerequisites. Seven auxiliary passages and 25 source notes preserve the source conventions and ambiguities, including its conflicting prose and formula for the lower density bound. No appendix-only definition is needed to state the seven results. This review does not certify proofs or assert equivalence to final journal typesetting.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-prerequisites.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1102/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
