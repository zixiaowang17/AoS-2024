# Paper census: aos-2024-v52-i02-p0628

Testing for practically significant dependencies in high dimensions via bootstrapping maxima of U-statistics — Patrick Bastian, Holger Dette and Johannes Heiny.

Source: [arXiv:2210.17439v2](https://arxiv.org/pdf/2210.17439v2), stamped 12 February 2024, 66 pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i02-p0628.pdf` relative to the repository root. Main text and acknowledgements end on page 25; Appendix A starts on page 26 and is excluded.

Source review and independent validation passed for 5 Theorems, 26 source entries, 31 direct uses and 74 related theorem connections. No census-content correction was needed. Inconsistencies in the printed source remain quoted as written, with separate explanatory notes.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i02-p0628/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
