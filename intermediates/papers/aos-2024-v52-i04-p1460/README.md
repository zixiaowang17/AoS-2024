# Fundamental Limits of Low-Rank Matrix Estimation with Diverging Aspect Ratios

Source: Andrea Montanari and Yuchen Wu,
[arXiv:2211.00488v1, 1 November 2022](https://arxiv.org/pdf/2211.00488v1).
The registered local PDF has 74 pages and SHA-256
`7d26b0fb80a5a46f7044f5223d98da7b1a1a6eec64c520380562f10cd66a628d`.
Main text and references end on page 28. Appendix A starts separately on page 29;
appendix bodies are excluded.

Status: **census complete; source review and independent validation passed**.

All nine original Theorems (3.1-3.3, 4.1-4.5 and 5.1) are preserved. Theorem 4.2
continues onto page 10 and Theorem 5.1 onto page 15. The census contains 25
supporting passages, 41 direct theorem uses, 70 related theorem connections and
nine unranked auxiliary passages.

The extraction keeps the strong, weak and symmetric observation models separate.
It preserves the individual moment restrictions, the three alternatives in
Theorem 4.5, and the order of the perturbation limits in Theorem 4.4. Original
source problems are documented separately: projection matrices assigned to the
orthogonal group, an unbound parameter in Theorem 4.1, and the inconsistent
maximum condition in Theorem 4.5(c). Source review does not certify the proofs
or silently correct these statements.

The six content artifacts are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. See [paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json) for the source
checks, independent graph expectations and exact artifact hashes.

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce all six files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1460/scripts/rebuild.py --output-dir [local path omitted]
```

All six artifacts reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). The script uses the
saved transcription and extraction, checks the pinned local PDF and validates
structure. It does not perform or renew the manual source review.
