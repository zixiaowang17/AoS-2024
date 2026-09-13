# Paper census: aos-2024-v52-i03-p0999

Change-point inference in high-dimensional regression models under temporal dependence — Haotian Xu, Daren Wang, Zifeng Zhao and Yi Yu.

Source: [arXiv:2207.12453v3](https://arxiv.org/pdf/2207.12453v3), 112 PDF pages, with margin date 1 October 2023 and title-page date 3 October 2023. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i03-p0999.pdf` relative to the repository root. Main text and references occupy pages 1–33. Only the appendix heading on page 34 was inspected; all appendix bodies were excluded.

Source review and independent validation passed for 4 Theorems, 33 source entries, 62 direct uses and 87 related theorem connections. No census-content correction was needed. The scalar Bernstein theorem retains its own nonstationary dependence setting. The variance and simulation theorems retain their inherited assumptions and the surrounding vanishing-jump scope.

The 13 auxiliary passages and 33 source notes preserve printed algorithm indices, endpoint and argmin ambiguities, variance positivity and zero-denominator issues, finite-versus-infinite simulation ranges, and other source conventions. The review does not repair the algorithms or certify their proofs. Equivalence of this registered preprint to the journal version is not asserted.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p0999/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
