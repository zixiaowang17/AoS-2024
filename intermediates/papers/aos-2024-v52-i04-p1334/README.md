# Optimal estimation of Schatten norms of a rectangular matrix

Source: Solène Thépaut and Nicolas Verzelen,
[arXiv:2111.13551v1, 26 November 2021](https://arxiv.org/pdf/2111.13551v1).
The registered local PDF has 67 pages and SHA-256
`ea31f60f810e9e62cb1cea4b540e44a17e40a122a998cb1df72585ec2e818cf4`.
Main text ends after the proof of Lemma 9.15 on PDF page 65, above Appendix A.
Appendix bodies were excluded.

The source-reviewed census contains all four main-text Theorems: 3.3, 4.9, 5.2
and 6.3. It preserves 20 supporting source passages, eight auxiliary passages,
19 direct theorem uses and 37 related connections.

## Saved results

- `theorem-inventory.json`: complete original theorem statements in source order.
- `source-passages.json`: supporting definitions, conditions and source highlights.
- `interface-extraction.json`: local extraction and dependency reasons.
- `ambient-prerequisites.json`: conventions, unresolved source issues and references.
- `unfinalized-census.json` and `ranked-interfaces.json`: linked census and derived counts.
- `inventory-review.json`, `paper-audit.json` and `registered-source-review.json`:
  source comparisons, independent checks and artifact hashes.
- `evidence/`: main-text source evidence, visual-review findings and reproduction results.

The Gaussian and sub-Gaussian noise laws remain separate. The shared Hermite
statistic does not make Gaussian unbiasedness a hypothesis of Theorem 6.3.

Theorem 5.2 and its estimator contain unresolved source inconsistencies involving
the constant name, expectation, grid scaling, moment-vector alias, strict positivity
and singular-value ordering. The census preserves the printed text and records
these issues separately. It does not provide a corrected executable estimator or
certify the paper's proofs.

## Reproduction

From the repository root, choose an empty output directory and run:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1334/scripts/rebuild.py --output-dir [local path omitted]
```

This verifies the registered local PDF, regenerates all six content artifacts
from the saved manual extraction, validates structure and compares saved bytes.
It does not perform a new semantic source review or replace the saved audit records.
Source-content review, independent validation and exact reproduction passed.
