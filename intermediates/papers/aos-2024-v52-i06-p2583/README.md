# Tensor-on-tensor regression: Riemannian optimization, over-parameterization, statistical-computational gap, and their interplay

Status: complete, checked against the registered local PDF and independently validated.

- Source: arXiv:2206.08756v3, marked 15 January 2024, 65 PDF pages. Main text ends with acknowledgements on page 26, before references; evidence is clipped at y322. Supplementary bodies are excluded.
- All ten original main-text Theorems (1–10) are retained, with their printed titles, complete hypotheses, formulas and branches.
- The census contains 30 source entries, 10 auxiliary passages, 71 direct uses and 115 related-theorem connections.
- RGD and RGN have separate algorithm branches. The RGN-only theorem does not inherit the RGD stepsize. Matrix retractions, tensor retractions, the low-degree testing model and deterministic OHOOI remain distinct.
- Initialization properties referenced from earlier theorems or Corollary 1 are preserved as output guarantees where the source asserts them. Proof-only references are excluded from statement dependencies.
- Thirteen source notes preserve discrepancies and unresolved conventions, including the RGN time-zero factor, testing normalization, target/index mismatches and definitions deferred to excluded supplements.
- All six content JSON artifacts reproduce byte for byte in `[local path omitted]`. Seven scripts remain under `scripts/`.

See `paper-audit.json`, `registered-source-review.json`, and `evidence/manual-findings.json` for evidence and limits. Source validation does not prove the theorems or resolve missing supplement definitions.

Rebuild in a fresh empty directory with `python3 -B scripts/rebuild.py --output-dir [local path omitted]`. Rebuilding reproduces saved extraction decisions; it does not perform a new semantic source review.
