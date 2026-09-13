# Optimal parameter estimation for linear SPDEs from multiple measurements

Source: Randolf Altmeyer, Anton Tiepner and Martin Wahl,
[arXiv:2211.02496v2, 25 July 2024](https://arxiv.org/pdf/2211.02496v2).
The registered local PDF has 42 pages and SHA-256
`b0b01164cab1ebda27f9a4698b232a5557671feb0b1d940fe49cbcc70901247d`.
Main text ends above Appendix A on PDF page 24. Appendix bodies were excluded.

The source-reviewed census contains all five main-text Theorems: 2.3, 3.1, 3.2,
4.1 and 4.3. It preserves 25 supporting definition, assumption and model passages,
eight auxiliary passages, 28 direct theorem uses and 49 related connections.

## Saved results

- `theorem-inventory.json`: complete original theorem statements in source order.
- `source-passages.json`: original supporting passages and source highlights.
- `interface-extraction.json`: paper-local extraction and dependency reasons.
- `ambient-prerequisites.json`: conventions, source issues and excluded references.
- `unfinalized-census.json` and `ranked-interfaces.json`: linked census and derived counts.
- `inventory-review.json`, `paper-audit.json` and `registered-source-review.json`:
  source comparisons, independently checked invariants and artifact hashes.
- `evidence/`: main-text evidence, visual-review findings and reproduction results.

The general self-adjoint RKHS setup remains separate from the spatial SPDE.
Theorem 4.3 retains its original reference to Theorem 4.1; its dependencies include
the inherited conditions and all three kernel instantiations of Assumption L.
Apparent source errors are recorded separately without changing quotations.

## Reproduction

From the repository root, choose an empty output directory and run:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1307/scripts/rebuild.py --output-dir [local path omitted]
```

This resolves and verifies the registered PDF, regenerates all six content files
from the saved manual extraction, validates structure and compares saved bytes.
It does not perform a new source review or overwrite the saved audit records.
The complete source review and independent validations passed; their scope is
transcription and statement dependencies, not proof certification.
