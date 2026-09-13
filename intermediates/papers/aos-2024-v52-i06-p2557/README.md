# Statistical Complexity and Optimal Algorithms for Non-linear Ridge Bandits

Status: complete, checked against the registered local PDF and independently validated.

- Source: arXiv:2302.06025v3, marked 10 January 2024 and dated 11 January 2024. Main text ends on PDF page 29 before Appendix A; evidence is clipped at y648.
- All 14 original main-text Theorems (1–14) are retained, including weaker versions and all branches.
- The census has 25 source entries, 6 auxiliary passages, 58 direct uses and 76 related-theorem connections. Original numbered definitions, assumptions and Algorithms 1–4 are preserved.
- Scope checks separate conditional regret assumptions, alternative regression-oracle models, Bayes versus minimax guarantees, adaptive versus nonadaptive policies, and sphere versus ball parameters.
- Sixteen source notes preserve discrepancies and unresolved references. In particular, the even-link signed-estimation issue and appendix-only Lemma 6 constant are not silently repaired. Appendix bodies remain excluded.
- All six content JSON artifacts reproduce byte for byte in `[local path omitted]`. Seven scripts remain under `scripts/`.

See `paper-audit.json`, `registered-source-review.json`, and `evidence/manual-findings.json` for evidence and limits. Source validation does not prove the theorems or certify unavailable appendix definitions.

Rebuild in a fresh empty directory with `python3 -B scripts/rebuild.py --output-dir [local path omitted]`. Rebuilding reproduces saved extraction decisions; it does not perform a new semantic source review.
