# Sharp multiple testing boundary for sparse sequences

Source: Kweku Abraham, Ismaël Castillo and Étienne Roquain,
[arXiv:2109.13601v2, 30 August 2023](https://arxiv.org/pdf/2109.13601v2).
The registered local PDF has 86 pages and SHA-256
`764e61241f4805afe2049048f37e0d748f1cbc048b08c77037438725b7ec10ba`.
The main paper and references end on page 33. Supplementary sections beginning
on page 34 are excluded from census content.

Status: **census complete; source review and independent validation passed**.

All nine main-text Theorems are preserved in full, including the continuations
of Theorems 4 and 8. Theorem 9 retains its original four-part summary rather
than substituting more detailed supplementary results.

The census contains 22 interface passages, 61 direct theorem uses, 92 related
connections and seven auxiliary passages. It distinguishes combined testing
risk, FNR and classification loss; exact and upper-bound sparsity; alternative
noise assumptions; and boundary versus large-signal parameter classes.

Exact BH and empirical Bayes procedure details deferred to S-18 and S-29, and
the precise adaptation statements deferred to S-9, remain unresolved within
the main-text-only scope. The source's Theorem 5 level/uniformity issue and
Assumption 1B parameter-sign convention are recorded separately. The original
statements are preserved; this review does not certify proofs.

The six content files are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. Source findings and hashes are recorded in
[paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json).

The per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce all six content files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1564/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). Rebuilding uses the
saved extraction and checks identity and structure; it does not perform or
renew manual source review.
