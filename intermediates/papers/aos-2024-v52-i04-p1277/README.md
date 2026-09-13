# Statistical inference for rough volatility: Minimax theory

Completed source-reviewed census of the verified local arXiv:2210.01214v2 PDF dated 15 February 2024. The register's filename and unversioned URL identify the same verified bytes.

- [Theorem inventory](theorem-inventory.json): four complete main-text Theorems, numbered 2, 3, 4 and 11.
- [Source passages](source-passages.json): 24 original model, minimax, estimator and coefficient definitions with source highlights.
- [Census](ranked-interfaces.json): 11 direct theorem uses and 32 related connections.
- [Ambient prerequisites](ambient-prerequisites.json): five auxiliary source passages, complete symbol resolution and 22 source notes.
- [Paper audit](paper-audit.json) and [registered source review](registered-source-review.json): source-content review, independent validation and pinned artifact hashes.
- [Rebuild evidence](evidence/rebuild-check.json): all six content artifacts reproduced byte-for-byte.

The piecewise-constant and general-volatility experiments remain separate. The estimator closure includes equation (36) and its Gaussian-integral definitions from the main-text proof section. Appendix bodies, starting below the reference endpoint on page 56, are excluded. Source inconsistencies in indices, logarithms and exceptional-event conventions are preserved and explained separately; this census does not certify the proofs.

Resolve the fixed local PDF from the repository root:

```sh
python3 scripts/resolve_paper_pdf.py aos-2024-v52-i04-p1277
```

Rebuild all content in a fresh empty directory using the [saved Python entry point](scripts/rebuild.py):

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1277/scripts/rebuild.py --output-dir [local path omitted]
```

The inventory, extraction, ambient-resolution and finalization scripts are saved alongside it. Rebuilding does not renew source review. Changed content requires renewed source comparison before the review hashes can be updated.
