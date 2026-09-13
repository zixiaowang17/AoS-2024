# Paper census: aos-2024-v52-i03-p1050

Change acceleration and detection — Yanglei Song and Georgios Fellouris.

Source: [arXiv:1710.00915v5](https://arxiv.org/pdf/1710.00915v5), dated 21 June 2024, 53 PDF pages. The fixed source is `local-pdfs/aos/2024/aos-2024-v52-i03-p1050.pdf` relative to the repository root. Main text and references end above y=137.4 on shared page 26. Only the appendix heading was inspected below that boundary; all appendix mathematics was excluded.

Source review and independent validation passed for 3 Theorems, 31 source entries, 25 direct uses and 45 related theorem connections. No census-content correction was needed. Theorem 5.1 includes its complete second-page continuation and initial-treatment extension. Markov control, the cyclic procedure bound and the universal lower bound retain their distinct prerequisites.

The predictive density phi used in the controlled transition kernel is defined only in Appendix B.1, equation (B.1), and remains explicitly unresolved. Six auxiliary passages and 33 source notes preserve the paper’s conventions and ambiguities. This review does not reconstruct excluded definitions, certify proofs or assert equivalence to final journal typesetting.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-prerequisites.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1050/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
