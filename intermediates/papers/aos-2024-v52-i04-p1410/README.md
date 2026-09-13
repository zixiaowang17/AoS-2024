# E-statistics, group invariance and anytime-valid testing

Source: Muriel Felipe Pérez-Ortiz, Tyron Lardy, Rianne de Heide and Peter D. Grünwald,
[arXiv:2208.07610v2, 17 October 2023](https://arxiv.org/pdf/2208.07610v2).
The registered local PDF has 31 pages and SHA-256
`e9e5fd4e0096e3be7e7b07d083fd73818791feafd69a65676c289c0f63db6223`.
Main text and references end on page 23; Appendix A starts separately on page 24.
Appendix bodies are excluded.

Status: **census complete; source review and independent validation passed**.

All three original Theorems (1, 2 and 4) are preserved. Number 3 belongs to a
Corollary. The census has 16 supporting passages, 21 direct theorem uses,
29 related theorem connections and nine unranked auxiliary passages.
Theorem 1 retains an arbitrary reduced statistic and an attained reduced-data
minimum. Theorem 2 includes all three assumption parts and amenability.
Theorem 4 includes only Part 3 and keeps the absolute and relative GROW criteria
separate. Source conventions and unresolved meanings are recorded separately.

The six content artifacts are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. See [paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json) for source checks,
independent graph validation and pinned hashes.

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce the six files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1410/scripts/rebuild.py --output-dir [local path omitted]
```

All six artifacts reproduced exactly; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). The script uses the
saved transcription and extraction and checks the pinned source. It does not
perform or renew the manual source review.
