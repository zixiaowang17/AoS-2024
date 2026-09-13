# Paper census: aos-2024-v52-i03-p1127

Sharp adaptive and pathwise stable similarity testing for scalar ergodic diffusions — Johannes Brutsche and Angelika Rohde.

Source: [arXiv:2203.13776v3](https://arxiv.org/pdf/2203.13776v3), dated 16 April 2024, 153 PDF pages. The fixed source is `local-pdfs/aos/2024/aos-2024-v52-i03-p1127.pdf` relative to the repository root. Main text and references end on page 31. Only the supplement title on page 32 was inspected to confirm the boundary; supplement mathematics was excluded.

Source review and independent validation passed for 10 Theorems, 38 source entries, 76 direct uses and 160 related theorem connections. No census-content correction was needed. Every theorem is preserved in full, including both adaptivity clauses, the conditional pathwise limits and the uniform Gaussian convergence result.

Stationary and fixed-start diffusion experiments, distinct kernel conditions, and arbitrary versus proposed tests retain their separate prerequisites. Nine auxiliary passages, 32 source notes and five excluded-reference records preserve the source conventions and ambiguities. The supplement-only bandwidth threshold, fractional coupling kernel and metric normalization remain explicitly unresolved. Printed sign, index and variable discrepancies are retained. This review does not certify proofs or assert equivalence to final journal typesetting.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-prerequisites.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1127/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
