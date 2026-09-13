# Detection and Estimation of Structural Breaks in High-Dimensional Functional Time Series

Registered source: Degui Li, Runze Li and Han Lin Shang,
[arXiv:2304.07003v1](https://arxiv.org/pdf/2304.07003v1).
The title page says April 17, 2023; the arXiv margin says 14 April 2023.
The verified local PDF has 42 pages. Main text ends with the acknowledgements
on page 22, before the Appendix A heading. Saved page-22 evidence is clipped
above the appendix heading.

Status: **source review and independent validation complete**.

The census preserves four complete original theorem statements, 24 original
source entries, seven auxiliary passages, and 36 source issues. Its dependency
graph has 30 direct theorem uses and 56 related-theorem connections.

All parts of the numbered assumptions remain separate. Theorem 4 explicitly
cites only Assumption 2(i); the tuning restriction in 2(iii) enters indirectly
through the source estimator construction. Assumption 2(ii) and preceding
theorem conclusions are not imported. Strict and non-strict threshold rules,
conditional membership recovery, estimated-group pooling, and unresolved
selection and domain conventions are preserved.

- [Original theorem inventory](theorem-inventory.json) and [inventory review](inventory-review.json)
- [Original source passages](source-passages.json) and [interface extraction](interface-extraction.json)
- [Auxiliary context and source issues](ambient-prerequisites.json)
- [Finalized census](ranked-interfaces.json) and [source audit](paper-audit.json)
- [Registered-source review](registered-source-review.json) and [reproduction evidence](evidence/rebuild-check.json)
- [Retained per-paper scripts](scripts/)

Seven Python scripts retain this paper's extraction and review. Rebuild all six
content artifacts in an empty directory with:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i04-p1716/scripts/rebuild.py --output-dir [local path omitted]
```

The saved reproduction check passed byte for byte. Rebuilding checks the saved
extraction and its structure; it does not perform a new semantic review or
certify the paper's proofs. Appendix material is excluded from the census.
