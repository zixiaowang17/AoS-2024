# Learning Gaussian Mixtures Using the Wasserstein-Fisher-Rao Gradient Flow

Status: **source-reviewed and independently validated** against the registered
[arXiv:2301.01766v1 PDF](https://arxiv.org/pdf/2301.01766v1).
The title-page date is January 5, 2023; the arXiv stamp is 4 Jan 2023.

The census contains all **6 theorems**, **18 original source entries**, and
**11 auxiliary passages**, with 22 direct uses and 46 related theorem connections.
Main text ends with Figure 5 on PDF page 15 before Appendix A. Appendix bodies
were excluded.

- [Complete original theorem statements](theorem-inventory.json)
- [Original definitions and source passages](source-passages.json)
- [Complete census and dependencies](ranked-interfaces.json)
- [Auxiliary conventions and unresolved source issues](ambient-prerequisites.json)
- [Independent source audit](paper-audit.json)
- [Registered-source review](registered-source-review.json)
- [Reproduction evidence](evidence/rebuild-check.json)
- [Retained per-paper scripts](scripts/)

Theorems 2 and 4 assume weak convergence before identifying its limit. The
particle theorems characterize three different flow PDEs. The printed weight
indices, unexplained weight in Theorem 6, and gamma/eta mismatch remain intact,
with their implications recorded separately. Source review does not certify
these equations or the paper's proofs.

All six content JSON artifacts reproduce byte for byte with an empty destination:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1774/scripts/rebuild.py --output-dir [local path omitted]
```

The rebuild restores the saved extraction and validates its structure; it does
not perform a fresh mathematical source review.
