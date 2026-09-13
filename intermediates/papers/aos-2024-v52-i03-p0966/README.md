# Paper census: aos-2024-v52-i03-p0966

Plugin estimation of smooth optimal transport maps — Tudor Manole, Sivaraman Balakrishnan, Jonathan Niles-Weed and Larry Wasserman.

Source: [arXiv:2107.12364v3](https://arxiv.org/pdf/2107.12364v3), stamped 16 June 2024, 99 PDF pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i03-p0966.pdf` relative to the repository root. Main text ends above y=637.536865234375 on shared page 29. Appendix mathematics and the later reference pages were excluded; only the appendix heading was inspected.

Source review and independent validation passed for 9 Theorems, 40 source entries, 62 direct uses and 109 related theorem connections. No census-content correction was needed. Euclidean, torus and smooth-domain settings retain their separate definitions and conditions. Deterministic stability does not acquire a sampling hypothesis, and spectral estimation does not acquire kernel assumptions. All 31 source notes and the historical audit are preserved.

Four appendix-only references remain unresolved within scope: precise Hölder norms, the boundary-corrected wavelet construction, the H2 Sobolev convention and the particular local paths in Appendix L equations (115)–(116). The general-domain regularity condition C2 remains an assumption, as stated in the source.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p0966/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
