# Wasserstein generative adversarial networks are minimax optimal distribution estimators

Source census completed against the registered local **arXiv:2311.18613v2, dated 12 March 2025**, 83 pages, DOI `10.1214/24-AOS2430`. This identifies the inspected source; it does not claim equivalence to the final 2024 journal text.

Source SHA-256: `e16df8b32ca2250fd73e8e9d56aaafa49a771467015b5593da33bd35de477222`.

- **9 labeled theorem occurrences**: six formal theorems (3.1, 4.1, 5.1, 5.4, 5.7, 5.8) and three separately labeled overview statements (4.1, 5.8, 5.1).
- **23 source entries**, **12 supporting passages**, **57 direct uses**, and **86 related connections**.
- Main text ends with the Discussion on PDF page 25; appendix bodies are excluded.

The overview of Theorem 5.1 imposes density regularity on both maps; the formal statement imposes it only on the target map. Theorem 5.8 prints different regularity ranges in its overview and formal statement. These occurrences remain separate, with their original wording and formulas.

The exact neural wavelet implementations and numerical regularity condition are appendix-only. Their main-text descriptions, formulas and references are saved, and their missing details are explicitly recorded. Source issues also include the low-dimensional resolution denominator, zero endpoints in logarithmic bounds, wavelet conventions and coefficient indices. The census preserves these details without repairing or certifying the paper's claims.

## Artifacts

`theorem-inventory.json` stores the original statements; `source-passages.json` stores original definitions and assumptions; `interface-extraction.json` and `ranked-interfaces.json` store the relationships. `ambient-prerequisites.json` records supporting passages, unresolved references and local bindings. Source review is saved in `inventory-review.json`, `paper-audit.json`, `registered-source-review.json` and `evidence/`.

## Reproduction

All seven per-paper Python scripts are retained in `scripts/`. Rebuild the six content JSON files in a new empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i05-p2167/scripts/rebuild.py --output-dir [local path omitted]
```

All six artifacts reproduced byte for byte; see `evidence/rebuild-check.json`. Rebuilding reproduces the saved extraction and validates structure; it does not perform a new semantic source review.
