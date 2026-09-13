# Wasserstein convergence in Bayesian and frequentist deconvolution models

Registered source: Judith Rousseau and Catia Scricciolo,
[arXiv:2309.15300v1, 26 September 2023](https://arxiv.org/pdf/2309.15300v1).
The verified local PDF has 67 pages. Main-text scope ends on page 29;
supplementary material beginning on page 30 is excluded.

Status: **source review and independent validation complete**.

The census preserves eight complete original theorem statements, 31 source
passages in 30 interfaces, and eight auxiliary passages. Its paper-local graph
contains 62 direct theorem uses and 108 related-theorem connections. Distinct
exponential-tail conditions retain their own source passages and dependencies.
Twenty-nine source issues record ambiguous notation, implicit conventions and
unresolved external references without changing the original statements.

- [Theorem inventory](theorem-inventory.json) and [independent inventory review](inventory-review.json)
- [Original source passages](source-passages.json) and [interface extraction](interface-extraction.json)
- [Auxiliary passages and source issues](ambient-prerequisites.json)
- [Finalized census](ranked-interfaces.json) and [source audit](paper-audit.json)
- [Registered-source review](registered-source-review.json) and [reproduction check](evidence/rebuild-check.json)
- [Preserved earlier artifacts](prior-review/)

Seven retained Python scripts are in [scripts](scripts/). The rebuild entrypoint
reproduces all six content JSON artifacts byte for byte in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1691/scripts/rebuild.py --output-dir [local path omitted]
```

Reproduction checks the saved extraction; it does not perform a fresh mathematical
source review or certify proofs. The registered-source review separately records
the completed visual comparison, source identity checks, graph reconstruction,
keyword and highlight checks, and structural validation.
