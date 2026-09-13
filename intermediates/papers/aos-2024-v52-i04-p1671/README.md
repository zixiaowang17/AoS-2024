# Majority Vote for Distributed Differentially Private Sign Selection

Source: Weidong Liu, Jiyuan Tu, Xiaojun Mao and Xi Chen,
[arXiv:2209.04419v2, 4 June 2024](https://arxiv.org/pdf/2209.04419v2).
The registered local PDF has 41 pages. The main paper and references occupy
pages 1–28; appendix bodies are excluded.

Status: **source review and independent validation complete**.

All four main-text Theorems are preserved, including Theorem 4(c) and its
conclusion on page 18. The census contains 16 interfaces, 12 direct theorem
uses, 37 related theorem connections and eight auxiliary source passages.

The source's threshold scope, unused or unquantified constants, sparse-output
convention and regression notation issues are recorded separately. Original
statements remain unchanged; this census does not certify the proofs.

- [Original theorem inventory](theorem-inventory.json) and [inventory review](inventory-review.json)
- [Source passages](source-passages.json) and [census](ranked-interfaces.json)
- [Auxiliary definitions and source issues](ambient-prerequisites.json)
- [Paper audit](paper-audit.json) and [registered source review](registered-source-review.json)
- [Reproduction evidence](evidence/rebuild-check.json)

Seven Python scripts are retained in [scripts](scripts/). From this directory,
run `python3 -B scripts/rebuild.py --output-dir /path/to/empty/directory` to
reproduce all six content JSON artifacts. The saved rebuild check confirms
byte-for-byte equality. Rebuilding does not perform a new source review.
