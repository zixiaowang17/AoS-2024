# One-Step Estimation of Differentiable Hilbert-Valued Parameters

Source: Alex Luedtke and Incheoul Chung,
[arXiv:2303.16711v3](https://arxiv.org/pdf/2303.16711v3).
The registered PDF has 83 pages and SHA-256
`1743d4d93efb6c31474b16cf5e8c92c491becdb499f0ae6afb5a8b2942603e23`.
Its arXiv stamp is dated 27 September 2023; the manuscript says 28 September 2023.
Main text and references end on page 30, above the Appendices heading at
y=638.9385986328125 PDF points. Appendix bodies are excluded.

Status: **census complete; source review and independent validation passed**.

All six main-text Theorems are preserved in full, including the continuation of
Theorem 5 onto page 17. Referenced conclusions (4) and (25) are saved separately
without rewriting the original theorem statements.

The census contains 24 interface passages, 34 direct theorem uses, 66 related
connections and 12 auxiliary passages. It preserves the distinction between
the regularized estimator of the original parameter and the estimator of its
transformed version. Theorem 5 allows sample-size-dependent regularization;
Theorem 6 fixes it and requires every coordinate to be positive.

The original closed-image assertion and missing adjoint star in Lemma 1 are
recorded as source issues. They have not been silently corrected. Conditions
from the examples and appendix proofs are not imported into the general
Theorems. Source review does not certify proofs.

The six content files are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. Review evidence and hashes are recorded in
[paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json).

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce the content in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1534/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). Rebuilding uses the
saved extraction and checks source identity and structure. It does not perform
or renew the manual source review.
