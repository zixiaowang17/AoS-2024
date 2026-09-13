# On the approximation accuracy of Gaussian variational inference

Source: Anya Katsevich and Philippe Rigollet,
[arXiv:2301.02168v2](https://arxiv.org/pdf/2301.02168v2).
The arXiv stamp is dated 7 January 2024; the title page is dated 9 January 2024.
The registered local PDF has 49 pages and SHA-256
`d86f8493430c8c07106847a073666a82c9aa765fc33cd8f20a9dc25c8615aeae`.
Main text ends after Acknowledgments on page 22. The appendix notation prelude
and all appendix bodies are excluded.

Status: **census complete; source review and independent validation passed**.

All four original Theorems (2.1, 2.2, 3.1 and 4.1) are preserved, including the
page continuation of Theorem 2.1. There are 20 supporting source passages,
29 direct theorem uses, 51 related theorem connections and eight unranked
auxiliary passages. The canonical stationarity solution is kept distinct from
global KL minimization. Logistic-regression assumptions remain local to
Theorem 3.1. Source notation inconsistencies are recorded separately without
rewriting the original statements.

The six content artifacts are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. See [paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json) for the source
checks, independent graph checks, validation and pinned artifact hashes.

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce all six files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1384/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced exactly; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). The script uses the
saved transcription and extraction, checks the pinned local source, and validates
the resulting artifacts. It does not perform or renew the manual source review.
