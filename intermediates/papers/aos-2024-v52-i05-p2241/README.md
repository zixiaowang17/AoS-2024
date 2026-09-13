# On the existence of powerful p-values and e-values for composite hypotheses

Source census completed against the registered **arXiv:2305.16539v4, 1 December 2024**, 47 PDF pages, for the AoS article with DOI `10.1214/24-AOS2434`. [Inspected paper version](https://arxiv.org/pdf/2305.16539v4).

Source SHA-256: `4ab8ada786411ce1154b0662e6821f938f1280465ef3cb5f670cebff8429b8ba`.

- **11 theorems**: 3.1, 3.4, 4.2, 4.4, 4.7, 4.9, 5.3, 5.5, 6.1, 6.2 and 6.7.
- **23 source entries**, **14 supporting passages**, **59 direct uses** and **73 related connections**.
- Main-text acknowledgments end before References on PDF page 29. Appendix bodies were excluded.

The census preserves complete original statements, p/e-variable definitions, joint atomlessness, absolute continuity, convex and setwise orders, density-ratio laws, optimization domains, split measures, SHINE and total-variation separation. Source labels distinguish definitions, assumptions, propositions and theorem excerpts. Natural-language names and highlight selectors retain source evidence.

The dependency review preserves each clause’s scope: Theorem 4.9 requires absolute continuity only in its refinement; Theorem 5.3 adds the hyperplane condition for maximal convergence; Theorems 6.1 and 6.2 explicitly remove joint atomlessness for specified equivalences. Theorem 6.7 uses uniform positive log e-power and nested closures, with a further criterion under tightness. Maximal and maximum elements remain distinct.

Fourteen separate source notes record ambiguities, including atomic split selection, zero-mass barycenters, scalar/vector notation, reciprocal e-variables, the contextual assumption reference in Theorem 5.5 and the infinite-family separation argument. The census preserves the source claims without repairing them or certifying their proofs.

## Artifacts

`theorem-inventory.json` contains full original theorem statements. `source-passages.json` contains definitions, assumptions and source excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` retains supporting passages, source issues and theorem-local bindings.

Independent checks are recorded in `inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/`. Source identity, heading enumeration, original statements, formulas, dependency reconstruction, names, highlights and schema validation passed.

## Reproduction

All seven per-paper Python scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2241/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
