# Paper census: aos-2024-v52-i02-p0550

A general framework to quantify deviations from structural assumptions in the analysis of nonstationary function-valued processes — Anne van Delft and Holger Dette.

Source: [arXiv:2208.10158v3](https://arxiv.org/pdf/2208.10158v3), 86 pages, stamped 16 September 2023. The registered local PDF is `local-pdfs/aos/2024/aos-2024-v52-i02-p0550.pdf` relative to the repository root. Main text and references end on PDF page 30; appendices are excluded.

Source review and independent validation passed for 11 Theorems, 41 source entries, 204 direct uses and 250 related theorem connections. No content correction was needed during registered-source revalidation. Appendix-only covariance and moment-order references remain explicitly unresolved.

- [Complete original theorem statements](theorem-inventory.json)
- [Original definitions, assumptions and other source passages](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate the six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i02-p0550/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, runs structural validation, and compares the regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
