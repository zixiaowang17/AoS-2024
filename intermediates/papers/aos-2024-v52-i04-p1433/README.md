# Heavy-tailed Bayesian nonparametric adaptation

Source: Sergios Agapiou and Ismaël Castillo,
[arXiv:2308.04916v3, 29 May 2024](https://arxiv.org/pdf/2308.04916v3).
The registered local PDF has 59 pages and SHA-256
`36a56438156e943f34cd8fd429857a5707dac77a4cd2606c8533def916aca2cb`.
Main text ends after Funding on page 26, before the Supplementary Material heading.
The supplement introduction and appendix bodies are excluded.

Status: **census complete; source review and independent validation passed**.

All ten original Theorems (1-10) are preserved, including both complete branches
of Theorems 6 and 7. The census contains 26 supporting passages, 82 direct theorem
uses, 87 related theorem connections and ten unranked auxiliary passages.
Moment condition (14) and tail condition (19) remain separate. Referenced prior
parameters and rates in Theorems 8 and 9 retain their matching branches.

Source ambiguities are recorded without rewriting the statements: Theorem 5's
weights at level zero, Theorem 4's scale index, and Theorem 9's prior reference,
joint-density norm and covariate dimension conventions. See
[ambient-prerequisites.json](ambient-prerequisites.json) for the source context
and branch-by-branch resolution.

The six content artifacts are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. Source checks, independently specified graph
expectations and exact artifact hashes are in [paper-audit.json](paper-audit.json)
and [registered-source-review.json](registered-source-review.json).

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce all six files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1433/scripts/rebuild.py --output-dir [local path omitted]
```

All six artifacts reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). Rebuilding uses the
saved transcription and extraction, checks the pinned PDF, and validates the
artifact structure. It does not perform or renew the manual source review.
