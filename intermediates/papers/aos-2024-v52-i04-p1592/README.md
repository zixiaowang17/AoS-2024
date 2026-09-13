# A nonparametric doubly robust test for a continuous treatment effect

Source: Charles R. Doss, Guangwei Weng, Lan Wang, Ira Moscovice and Tongtan
Chantarat, [arXiv:2202.03369v2](https://arxiv.org/pdf/2202.03369v2).
The arXiv stamp is dated 22 May 2023; the manuscript is dated 23 May 2023.
The registered PDF has 93 pages and SHA-256
`16810a1dcbde7957e273977a06255d6b5e043016acb7976583b2b1b86dc17ad4`.

Status: **census complete; source review and independent validation passed**.

All four main-text Theorems (3.1–3.4) are preserved in full. Main-text evidence
ends after the acknowledgements on page 28, before Appendix A. Appendix bodies
are excluded.

The census contains 30 source interface passages, 75 direct theorem uses,
110 related connections and nine auxiliary passages. It preserves the separately
numbered causal, distribution and estimator assumptions, the nuisance functions,
local estimator and statistic, and the two distinct bootstrap procedures.

Printed equation-reference discrepancies, the bootstrap mean symbol `b_h`
versus `b_0h`, the unsubscripted treatment density, and internal condition or
notation issues are recorded separately. No appendix formula or proof-only
entropy assumption replaces a main-text statement. This review does not
certify proofs.

The six content artifacts are:

- `theorem-inventory.json`
- `source-passages.json`
- `interface-extraction.json`
- `ambient-prerequisites.json`
- `unfinalized-census.json`
- `ranked-interfaces.json`

Source findings and reviewed hashes are in [paper-audit.json](paper-audit.json)
and [registered-source-review.json](registered-source-review.json).

The per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce the six content files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1592/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json).
Seven retained scripts separately save the inventory, review the inventory,
extract interfaces, finalize dependencies, save auxiliary context, rebuild
content and record source review. Rebuilding does not renew manual source review.
