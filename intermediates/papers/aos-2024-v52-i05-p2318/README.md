# Computational lower bounds for graphon estimation via low-degree polynomials

Source census completed against the registered **arXiv:2308.15728v4, 12 August 2024**, 58 PDF pages, for the AoS article with DOI `10.1214/24-AOS2437`. [Inspected paper version](https://arxiv.org/pdf/2308.15728v4).

Source SHA-256: `7bcc38eb8b952de996d7b08259295d5e2a91f94a7081aab2c7dedec225a52275`.

- **7 theorems**: 1–7, with complete original statements and formulas, including the two-page Theorem 3.
- **21 source entries**, **8 supporting passages**, **29 direct uses** and **43 related connections**.
- Main-text proofs end before References on PDF page 27. Appendix bodies were excluded.

The census preserves Bernoulli and graphon sampling, polynomial estimator classes, graphon loss, general and homogeneous SBM classes, the iid-label prior, full Algorithm 1, the printed Hölder norm and smooth-graphon class, co-membership and its loss, sparse probability matrices, and rectangular Gaussian biclustering models, priors and loss.

Worst-case fixed-matrix risk remains separate from prior-averaged risk. Theorem 4 retains the supremum over arbitrary latent-position distributions. Theorem 3 imports its full randomized estimator and tuning without the lower-bound theorem’s small-SNR condition. Theorem 7 uses every rectangular entry and the common minimum of the two class counts as the prior’s label range.

Twelve source notes record singular SNR endpoints, numeric-label nonuniqueness, the printed sketch dimension, iteration and degree accounting, probability and parameter scope, primed constants misread by the PDF text layer, the integer Hölder convention and rectangular label notation. Original quotations are preserved; source review does not certify proofs or turn low-degree lower bounds into unconditional runtime lower bounds.

## Artifacts

`theorem-inventory.json` contains the original theorem statements. `source-passages.json` contains original definitions and theorem excerpts. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their relationships. `ambient-prerequisites.json` preserves additional context, source issues and theorem-local bindings.

`inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/` record source identity, independent heading enumeration, visual source comparison, formula checks, dependency reconstruction and schema validation.

## Reproduction

All seven per-paper scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2318/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
