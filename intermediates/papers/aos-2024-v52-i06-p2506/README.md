# Non-independent components analysis

Status: complete. The registered local arXiv v4 PDF was reviewed directly.

- Four complete original main-text Theorems: 5.3, 5.5, 5.10 and 5.14.
- Thirteen source entries and nine auxiliary passages.
- Twenty-one direct theorem dependencies and twenty-nine related connections, independently checked.
- All six content JSON artifacts reproduce byte for byte from seven retained scripts.

The census separates arbitrary algebraic tensors from the statistical identification model. It preserves moments and cumulants as alternative meanings of `h_r`, diagonal and reflectional zero patterns as distinct definitions, the two genericity conditions, the orthogonal transformation domain and identification up to row signs and permutations. Source notes retain the generating-function regularity ambiguity, the distinction between transformation and parameter sets, and the normalized second-order applicability limit. Source review does not certify proofs.

The source is `arXiv:2206.13668v4`, marked 19 March 2024. Its title uses “components”; the corpus entry uses “component.” Main text and acknowledgements end on PDF page 21 before references; appendices and supplementary bodies are excluded.

## Artifacts

- `theorem-inventory.json`: all four complete original Theorem statements.
- `source-passages.json` and `interface-extraction.json`: original definitions and conditions, source terminology and literal highlights.
- `ambient-prerequisites.json`: local binders, context and source limitations.
- `ranked-interfaces.json`: complete claims, validated dependencies and source explanations.
- `paper-audit.json` and `registered-source-review.json`: independent source review with frozen artifact hashes.

## Reproduction

From this paper directory, run:

```sh
python3 -B scripts/rebuild.py --output-dir [local path omitted]
```

Use an empty destination. This regenerates and compares all six content JSON artifacts without overwriting audit evidence or performing a new source review. The completed reproduction check is saved in `evidence/rebuild-check.json`.

Seven scripts retain the paper-specific work: `save_inventory.py`, `review_inventory.py`, `extract_interfaces.py`, `save_ambient.py`, `finalize_paper.py`, `rebuild.py` and `save_registered_source_review.py`.
