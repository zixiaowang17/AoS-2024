# Computational and statistical thresholds in multi-layer stochastic block models

Source census completed against the registered **arXiv:2311.07773v1**, marked **13 November 2023**, with cover dated **15 November 2023**, 31 PDF pages. AoS DOI: `10.1214/24-AOS2441`. [Inspected paper version](https://arxiv.org/pdf/2311.07773v1).

Source SHA-256: `729249562a67503fcb0c40a36bb63f3f77cf9224ca014d3b04b04e24ffcd5ae8`.

- **5 theorems**: 2.2, 3.1, 3.3, 4.1 and 4.2, with complete statements.
- **14 source entries**, **8 supporting passages**, **27 direct uses** and **45 related connections**.
- Main text and acknowledgment end on page 12. Evidence is clipped before Appendix A on that shared page; appendix bodies are excluded from the census.

The census preserves the balanced latent graph mixture and null model, the two layer probability matrices, Hamming loss up to label permutation, approximate recoverability, strong distinguishability, Assumption 1, the full low-degree polynomial conjecture, conditional alternative distributions, chi-square divergence and the joint edge-count MLE.

Computational lower bounds remain conditional on the conjecture. Information-theoretic results remain unconditional. Joint latent distributions are distinguished from the observed-data marginals used in testing. Theorems do not gain dependencies merely from recovery-to-detection reductions or projected-likelihood proof machinery.

Twelve source notes record unresolved conventions and apparent typos, including the p/q assignment in chi-square prose, the reversed caption of Lemma 2.1, a logarithm-sign discrepancy, even-integer monomial sequences, runtime scope, MLE ties and externally specified algorithm details. Original quotations are preserved without silent repair. Source review does not certify proofs or establish the hardness conjecture.

## Artifacts

`theorem-inventory.json` contains every original theorem statement. `source-passages.json` contains original definitions, Assumption 1 and Conjecture 3.2. `interface-extraction.json`, `unfinalized-census.json` and `ranked-interfaces.json` record their dependencies. `ambient-prerequisites.json` preserves contextual passages, theorem-specific scope and source issues.

`inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/` record source identity, independent heading enumeration, visual comparison, formula checks, graph reconstruction and schema validation.

## Reproduction

All seven per-paper scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2431/scripts/rebuild.py --output-dir [local path omitted]
```

All six files reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
