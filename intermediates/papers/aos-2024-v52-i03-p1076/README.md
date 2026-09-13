# Paper census: aos-2024-v52-i03-p1076

Spectral regularized kernel two-sample tests — Omar Hagrass, Bharath K. Sriperumbudur and Bing Li.

Source: [arXiv:2212.09201v3](https://arxiv.org/pdf/2212.09201v3), dated 1 May 2024, 75 PDF pages. The fixed source is `local-pdfs/aos/2024/aos-2024-v52-i03-p1076.pdf` relative to the repository root. Numbered Section 7 (Proofs) is main text. References end above y=601.6620483398438 on shared page 55; all appendix mathematics was excluded.

Source review and independent validation passed for 10 Theorems, 32 source entries, 82 direct uses and 159 related theorem connections. All three two-page theorem statements include their continuations, and both adaptive power results retain all four rate cases. Level and power guarantees preserve their distinct prerequisites.

Eight naming-context excerpts contained Python escape corruption affecting LaTeX notation. These excerpts and the four derived JSON files have been corrected against the PDF; prior artifacts are archived. Complete theorem statements, original definition and assumption bodies, dependency edges and counts are unchanged.

Ten auxiliary passages and 34 source notes preserve the paper's conventions and printed ambiguities, including operator domains, matrix dimensions, quantile ties and rate constants. No appendix-only definition is required to state these ten results. This review does not certify proofs or assert equivalence to final journal typesetting.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-prerequisites.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1076/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the prior paper audit and pre-correction content are preserved in `review-history/before-naming-context-escape-correction/`.
