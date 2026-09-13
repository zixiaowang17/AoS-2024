# Paper census: aos-2024-v52-i02-p0817

The online closure principle — Lasse Fischer, Marta Bofill Roig and Werner Brannath.

Source: [arXiv:2211.11400v3](https://arxiv.org/pdf/2211.11400v3), stamped 21 December 2023 and dated 22 December 2023 on the title page, 21 PDF pages. The fixed local source is `local-pdfs/aos/2024/aos-2024-v52-i02-p0817.pdf` relative to the repository root. Main text ends on page 16; appendices beginning on page 17 were excluded.

Source review and independent validation passed for 4 Theorems, 13 source entries, 27 direct uses and 35 related theorem connections. Online measurability, level control and the two predictability definitions retain their distinct meanings. The review added the missing dependency from the sub-adjustment construction to its explicitly named online intersection-test definition. All original theorem statements and source quotations remain unchanged. The previous audit and JSON artifacts are preserved in `review-history/before-online-intersection-dependency-correction/`.

- [Complete original theorem statements](theorem-inventory.json)
- [Original source definitions and conditions](source-passages.json)
- [Census and theorem dependencies](ranked-interfaces.json)
- [Ambient conventions and unresolved source issues](ambient-conventions.json)
- [Registered-source review and validation evidence](registered-source-review.json)
- [Manual review findings](evidence/revalidation/manual-findings.json)
- [Rebuild verification](evidence/revalidation/rebuild-check.json)

From the repository root, regenerate all six census artifacts in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i02-p0817/scripts/rebuild.py --output-dir [local path omitted]
```

The script uses the verified local PDF and saved extraction, validates structure and compares regenerated files with the saved artifacts. It does not perform a new manual source review. Earlier scripts remain in `review-history/before-local-source-rebuild/scripts/`; the historical paper audit is preserved.
