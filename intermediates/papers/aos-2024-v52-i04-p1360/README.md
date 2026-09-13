# Higher-order coverage errors of batching methods via Edgeworth expansions on t-statistics

Source: Shengyi He and Henry Lam,
[arXiv:2111.06859v1, 12 November 2021](https://arxiv.org/pdf/2111.06859v1).
The verified local PDF has 46 pages and SHA-256
`af1faf7d9821a3f94ea242503fa4d26d7c6adb6c4ec6b0ff34719b8a740c89fc`.
Main text and references end above Appendix A on PDF page 22.
Appendix bodies are excluded.

Status: **census complete; source review and independent validation passed**.

The census preserves all seven original Theorems, numbered 1-7, including
Theorems 2 and 4 across page breaks. It contains 29 supporting source passages,
58 direct theorem uses, 94 related theorem connections and nine unranked auxiliary
passages. These include the four batching statistics, dependent-data and
regenerative constructions, full Algorithm 1 and its main-text coefficient
formulas. Original source issues are recorded separately without correcting
quoted statements. Appendix-only formulas remain excluded.

The six content artifacts are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. Source checks and artifact hashes are recorded in
[paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json).
[Source review worklist](source-review-worklist.json) records the completed requirements.

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce the six content files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1360/scripts/rebuild.py --output-dir [local path omitted]
```

It uses the saved transcription and extraction scripts and checks the resulting
bytes against the saved artifacts. All six files reproduced exactly; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). Rebuilding does not
perform or renew the manual source review.
