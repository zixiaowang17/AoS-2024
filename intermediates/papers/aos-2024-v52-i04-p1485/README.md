# Asymptotic normality and optimality in nonsmooth stochastic approximation

Source: Damek Davis, Dmitriy Drusvyatskiy and Liwei Jiang,
[arXiv:2301.06632v1, 16 January 2023](https://arxiv.org/pdf/2301.06632v1).
The registered local PDF has 47 pages and SHA-256
`32e48d4bfd9b0520b093cc0a28210a96c57548b0b696b2cdb5451defa86fb6a3`.
Main text and references end above Appendix A on page 26. The appendix heading
starts at y=489.0146179199219 PDF points; saved page-26 evidence stops above it.
Appendix bodies are excluded.

Status: **census complete; source review and independent validation passed**.

All four original Theorems (2.7, 3.1, 3.2 and 5.1) are preserved in full.
The census contains 22 supporting source passages, 30 direct theorem uses,
33 related theorem connections and eight unranked auxiliary passages.

The extraction distinguishes regular and limiting subdifferentials, the active
manifold from the abstract smooth reduction, the population and empirical
inclusions, and the separate assumptions of the normality and optimality
results. Theorem 5.1 does not acquire the concrete algorithm examples as extra
hypotheses. Assumptions retain their original source labels and wording.

Source issues are documented separately, including reversed inverse basepoints,
the regularity wording for the reduced map, and the tangent-coordinate covariance
used with ambient Jacobians in Theorem 5.1. No missing coordinate transformation
or additional hypothesis is silently inserted. Source review does not certify
proofs or the correctness of these source assertions.

The six content artifacts are `theorem-inventory.json`, `source-passages.json`,
`interface-extraction.json`, `ambient-prerequisites.json`, `unfinalized-census.json`
and `ranked-interfaces.json`. See [paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json) for the pinned
source, full review findings and independently checked dependency graph.

The retained per-paper entry point is [scripts/rebuild.py](scripts/rebuild.py).
From the repository root, regenerate all six content files into an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1485/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). Rebuilding uses the
saved extraction and checks source identity and structure. It does not perform
or renew the manual source review.
