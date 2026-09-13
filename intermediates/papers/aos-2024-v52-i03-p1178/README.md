# Paper census: aos-2024-v52-i03-p1178

Nonparametric classification with missing data — Torben Sell, Thomas B. Berrett and Timothy I. Cannings.

Source: [arXiv:2305.11672v2](https://arxiv.org/pdf/2305.11672v2), dated 2 May 2024, 73 PDF pages. The fixed source is `local-pdfs/aos/2024/aos-2024-v52-i03-p1178.pdf` relative to the repository root. Main text ends with funding on page 22. Only the S1 heading on page 23 was inspected; supplementary bodies were excluded.

Source review and independent validation passed for 2 Theorems, 30 source entries, 25 direct uses and 57 related theorem connections. The complete 21-line HAM algorithm is preserved. The minimax result and HAM guarantee retain their different distribution classes and parameter restrictions; incomplete training data and the unconditional test distribution remain distinct.

One corrupted LaTeX escape in the D19 naming-context passage was repaired. All original theorem and definition bodies, dependency paths and counts are unchanged. The original content and audit are preserved in `review-history/before-naming-context-escape-correction/`.

Six auxiliary passages, 27 source notes and three excluded-reference records preserve the source conventions and ambiguities. Empty extrema and the algorithm's neighbor-count, projection and pattern-selection issues remain explicitly unresolved. This review does not certify proofs or assert equivalence to final journal typesetting.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-prerequisites.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1178/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the pre-correction paper audit is preserved in the correction history.
