# Optimal policy evaluation using kernel-based temporal difference methods

Paper ID: `aos-2024-v52-i05-p1927`.

Status: **complete** for the registered arXiv:2109.12002v1 PDF. The PDF stamp is 24 September 2021; the title-page date is 27 September 2021. Main text ends on shared PDF page 30 after Acknowledgements. Evidence on that page is clipped above Appendix A. This review does not assume equivalence to the published article.

The census preserves **2 complete theorem statements**, **30 original definition/assumption/source entries**, and **12 auxiliary passages**. Eighteen source issues are recorded separately without rewriting the original statements. The dependency index contains 20 direct uses and 40 related theorem connections. Upper-bound branches and lower-bound regimes retain their distinct conditions.

- `theorem-inventory.json`: complete original Theorems in source order.
- `ranked-interfaces.json`: original source entries, source keywords, highlights and theorem relationships.
- `source-passages.json` and `interface-extraction.json`: retained extraction artifacts.
- `ambient-prerequisites.json`: source context, local bindings and unresolved conventions.
- `paper-audit.json` and `registered-source-review.json`: source review and independent validation.
- `evidence/rebuild-check.json`: byte-for-byte reproduction of all six content artifacts.

The paper-specific Python scripts are retained under `scripts/`. Reproduce into an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p1927/scripts/rebuild.py --output-dir [local path omitted]
```

`save_inventory.py`, `extract_interfaces.py`, `save_ambient.py` and `finalize_paper.py` retain the extraction and build the census. `review_inventory.py` and `save_registered_source_review.py` independently check the frozen reviewed content and source-specific relationships. Rebuilding does not perform a new semantic source review or certify proofs.
