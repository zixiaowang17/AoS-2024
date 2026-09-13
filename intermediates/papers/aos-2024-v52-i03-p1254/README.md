# Spectral analysis of gram matrices with missing at random observations

Source-reviewed census of Huiqin Li, Guangming Pan, Yanqing Yin and Wang Zhou, *The Annals of Statistics* 52(3), 2024, pp. 1254-1275, DOI 10.1214/24-AOS2392.

The four main-text Theorems (2.1, 2.2, 2.3 and 3.1) are preserved in full. Theorem 2.3 includes the contour conditions on the following page. There is no appendix body in this 22-page PDF; the external supplement was not opened.

- [Theorem inventory](theorem-inventory.json): complete original statements and source locations.
- [Source passages](source-passages.json): 24 original definitions, assumptions and model passages with highlights.
- [Census](ranked-interfaces.json): 35 direct theorem uses and 64 related theorem connections.
- [Ambient prerequisites](ambient-prerequisites.json): five additional source passages, symbol resolution and 20 source notes.
- [Paper audit](paper-audit.json) and [registered source review](registered-source-review.json): source-content review, independent validation and fixed artifact hashes.
- [Reproduction evidence](evidence/rebuild-check.json): all six content artifacts reproduced byte-for-byte.

Source inconsistencies, including c/y notation and the unscaled centralized LSS in the CLT, remain unchanged in quotations and are explained separately. The census does not certify the proofs.

Resolve the fixed local source from the repository root:

```sh
python3 scripts/resolve_paper_pdf.py aos-2024-v52-i03-p1254
```

The [per-paper rebuild script](scripts/rebuild.py) reproduces the manually extracted content in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1254/scripts/rebuild.py --output-dir [local path omitted]
```

The inventory, extraction, ambient-resolution and finalization modules are saved alongside that script. Rebuilding does not perform or renew a source review. Changes to the reviewed content require renewed source comparison before updating audit hashes.
