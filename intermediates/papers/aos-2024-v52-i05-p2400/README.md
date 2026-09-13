# Multivariate trend filtering for lattice data

Source census completed against the registered **arXiv:2112.14758v2, 5 April 2024**, 56 PDF pages, for the AoS article with DOI `10.1214/24-AOS2440`. [Inspected paper version](https://arxiv.org/pdf/2112.14758v2).

Source SHA-256: `24e6b64a3c70e5ec5e17e9bf317258d16e6d37805c0d2f783ca69a5565f251d0`.

- **6 theorems**, including credited Theorem 2 and the full attainment paragraphs in Theorems 5–6.
- **21 source entries**, **11 supporting passages**, **25 direct uses** and **42 related connections**.
- Main text and acknowledgments end on page 29. Evidence is clipped before References; appendix bodies were excluded.

The census preserves anisotropic BV and essential variation, coordinate slices, lattice difference matrices, the KTF estimator and KTV class, the discrete Sobolev class, the Gaussian experiment, minimax and minimax linear risks, singular-vector incoherence, effective smoothness, spectral projection and max-degree polynomial conventions.

The analytic slicing theorem has no statistical assumptions. The generic lasso theorem has no lattice restriction. Proof applications and class inclusions do not create statement dependencies. Original Holder definitions and their embedding are retained as supporting proof context.

Twelve source notes record distinctions and unresolved conventions, including the repeated zero-boundary difference versus shrinking-row matrix mismatch, approximate continuity’s external definition, feasible spectral truncation orders, the omitted parametric floor in a canonical-rate simplification, and a printed norm-inequality typo. The critical logarithm in Theorem 5 multiplies the squared-radius term. Original statements are preserved without silent repairs; source review does not certify proofs.

## Artifacts

`theorem-inventory.json` contains the original theorem statements. `source-passages.json` contains original definitions and object-defining excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record the dependencies. `ambient-prerequisites.json` preserves additional conditions, proof context and source issues.

`inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/` record source identity, independent heading enumeration, visual comparison, formula checks, graph reconstruction and schema validation.

## Reproduction

All seven per-paper scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2400/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
