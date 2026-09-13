# Paper census: aos-2024-v52-i03-p1152

A blockwise empirical likelihood method for time series in frequency domain inference — Haihan Yu, Mark S. Kaiser and Daniel J. Nordman.

Source: [published article, DOI 10.1214/24-AOS2388](https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-3/A-blockwise-empirical-likelihood-method-for-time-series-in-frequency/10.1214/24-AOS2388.pdf), The Annals of Statistics 52(3), 2024, pp. 1152-1177. The fixed 26-page PDF is `local-pdfs/aos/2024/aos-2024-v52-i03-p1152.pdf` relative to the repository root. Main text ends on PDF page 22 above Appendix A. Appendix bodies were excluded.

Source review and independent validation passed for 4 Theorems, 26 source entries, 30 direct uses and 70 related theorem connections. Six auxiliary passages preserve surrounding conventions. The full-data M-estimator, nonoverlapping SEL blocks, fitted-parameter bootstrap and function-valued smooth-profile bootstrap retain their distinct prerequisites.

The published source replaces the earlier dissertation chapter. Its theorem numbering is 1-4; the transition record maps the old labels. The published introduction fixes the earlier smooth-function dimensions and omits the dissertation percentile equation. The printed overlapping-periodogram normalization discrepancy and contradictory block-size limit in Theorem 4 remain explicitly flagged, without changing the original statements. This review does not certify proofs.

- [Complete original theorem statements](theorem-inventory.json)
- [Original definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and source issues](ambient-prerequisites.json)
- [Registered-source review](registered-source-review.json)
- [Manual findings](evidence/manual-findings.json)
- [Source-version comparison](source-transition-review.json)
- [Rebuild verification](evidence/rebuild-check.json)

From the repository root, regenerate all six content artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1152/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction. It validates structure and compares saved bytes; it does not perform a new manual source review. Previous dissertation-based artifacts and scripts are preserved in `review-history/dissertation-2023/`. The original dissertation PDF is preserved in the ignored `local-pdfs/aos/2024/source-history/aos-2024-v52-i03-p1152/dissertation-2023.pdf` with its original hash.
