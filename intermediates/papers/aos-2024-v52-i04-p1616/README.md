# Gromov-Wasserstein distances: Entropic regularization, duality and sample complexity

Source: Zhengxin Zhang, Ziv Goldfeld, Youssef Mroueh and Bharath K. Sriperumbudur,
[arXiv:2212.12848v3, 28 September 2023](https://arxiv.org/pdf/2212.12848v3).
The registered local PDF has 47 pages and SHA-256
`731c61d7acc3441626d44ba8cd53359493441b91be5e30774b595f93aafe42fb`.
The main paper and references end on page 28. Appendix bodies are excluded.

Status: **source revalidation complete; independent validation passed**.

All three original theorem statements and their stable IDs are preserved.
The census contains 11 source interfaces, nine direct theorem uses,
20 related connections and eight auxiliary passages. It retains all ten
previous interface IDs and adds the source centering condition used before
the dual decomposition. The component labeled S-epsilon-superscript-2 is
distinguished from a squared distance.

The earlier four migration artifacts are preserved in [prior-review](prior-review).
The new review uses the registered local PDF directly and records source
centering, notation and lower-bound support issues separately. It does not
certify proofs or silently add hypotheses to the source statements.

The six JSON content artifacts are `theorem-inventory.json`,
`source-passages.json`, `interface-extraction.json`, `ambient-prerequisites.json`,
`unfinalized-census.json` and `ranked-interfaces.json`. Review findings and hashes
are in [paper-audit.json](paper-audit.json) and
[registered-source-review.json](registered-source-review.json).

Seven per-paper scripts retain the extraction and review workflow. Reproduce
all six content artifacts in an empty directory from the repository root:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1616/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see
[evidence/rebuild-check.json](evidence/rebuild-check.json). Rebuilding checks
identity and structure but does not renew manual source review.
