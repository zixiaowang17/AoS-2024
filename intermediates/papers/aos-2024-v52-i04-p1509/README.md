# Bootstrap-assisted inference for generalized Grenander-type estimators

Source: Matias D. Cattaneo, Michael Jansson and Kenichi Nagasawa,
[arXiv:2303.13598v3, 4 July 2024](https://arxiv.org/pdf/2303.13598v3).
The registered local PDF has 66 pages and SHA-256
`41ad2b881f250cc5e8ef27156d744623d49c3461ab82e6a8733ab84734e1a476`.
Main text ends with the simulation discussion on page 20, above the Appendix A
heading at y=671.2371826171875 PDF points. Appendix bodies and the subsequent
supplement are excluded.

Status: **census complete; source review and independent validation passed**.

The sole main-text Theorem 1 is preserved in full. Its explicit references to
convergence formulas (2) and (7) are resolved using separately preserved original
source passages. The theorem body ends with (8); the later confidence-interval
implication is separate prose.

The census contains 14 interface passages, 10 direct theorem uses, 14 related
connections and eight auxiliary passages. It preserves every clause of
Assumptions A-C, including the closed-range and jump conditions. The corrected
bootstrap estimator is distinguished from the ordinary bootstrap estimator.
The rate, localization scale and fixed evaluation point retain their original
notation and roles.

Exact localized-domain conventions deferred to Appendix A.4 remain explicitly
unresolved. The main-text process formulas are retained without importing those
appendix details. The unnamed bootstrap-process formula is preserved as auxiliary
context rather than assigned an invented interface name. Source review does not
certify proofs or add implementation assumptions to the theorem.

The six content files are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. Review evidence and artifact hashes are recorded in
[paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json).

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, reproduce all six files in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1509/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). Rebuilding checks the
pinned source and structure using the saved extraction; it does not perform or
renew the manual source review.
