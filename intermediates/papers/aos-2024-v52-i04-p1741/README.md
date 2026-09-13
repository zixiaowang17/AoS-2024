# Efficient functional Lasso kernel smoothing for high-dimensional additive regression

Status: **source-reviewed and independently validated** against the registered
published PDF: [The Annals of Statistics 52(4), 2024, pp. 1741–1773](https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-4/Efficient-functional-Lasso-kernel-smoothing-for-high-dimensional-additive-regression/10.1214/24-AOS2415.pdf).

The census contains all **7 theorems**, **35 original source entries**, and
**15 auxiliary passages**, with 70 direct uses and 146 related theorem connections.
Main text ends on PDF page 25 before the appendix. Appendix and supplementary
bodies were excluded.

- [Original theorem statements](theorem-inventory.json)
- [Original definitions, assumptions and source passages](source-passages.json)
- [Complete census and theorem dependencies](ranked-interfaces.json)
- [Auxiliary notation and unresolved source conventions](ambient-prerequisites.json)
- [Independent source audit](paper-audit.json)
- [Registered-source review](registered-source-review.json)
- [Reproduction evidence](evidence/rebuild-check.json)
- [Retained per-paper scripts](scripts/)

The uncentered operator in Section 2 and its centered replacement in Section 3
remain separate. Theorems 4 and 5 inherit the hypotheses of Theorem 3; Theorem 6
retains its narrower assumption list and additional optimizer constraint only in
its second branch. Theorem 7 uses population quantities only.

All six content JSON artifacts reproduce byte for byte using the retained entry
point, with an empty output directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1741/scripts/rebuild.py --output-dir [local path omitted]
```

Reproduction restores the saved extraction and validates its structure. It does
not replace the recorded PDF comparison or certify the paper's proofs. Source
ambiguities are preserved separately; original statements are not silently repaired.
