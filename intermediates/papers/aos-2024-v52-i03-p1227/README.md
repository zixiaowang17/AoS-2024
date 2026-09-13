# Locally simultaneous inference

Completed census of the registered local arXiv:2212.09009v6 PDF, dated
2 May 2024, corresponding to AoS 52(3), article 10.1214/24-AOS2391.

- Six complete main-text Theorems, including both bullets of Theorems 3 and 4.
- 33 original definition or condition passages, 29 direct theorem uses and
  40 related theorem connections.
- Eight auxiliary passages and 25 source notes.

The [theorem inventory](theorem-inventory.json) remains byte-identical to its
previous independently reviewed version. The [census](ranked-interfaces.json)
adds the source passages and paper-local dependency paths.
[Ambient prerequisites](ambient-prerequisites.json) record conventions and
unresolved meanings separately. The [audit](paper-audit.json) and
[registered-source review](registered-source-review.json) pin the inspected
source and artifacts by hash.

General confidence regions, the location model, bounded vector observations,
fixed-design LASSO selection and prediction risk retain their separate
definitions. Theorem 5 concerns the exact returned model set; the separate
PoSI coverage result is not a dependency of that theorem. Theorem 6 permits
an arbitrary valid expected generalization-gap bound, with Rademacher
complexity only an optional example.

Algorithm 1 is saved in full. Its screening subroutines, Algorithms 2 and 3,
are in the excluded appendix; only their main-text descriptions and screening
criteria are retained. Rank, uniqueness, boundary and empty-set conventions
that are not specified in the main text remain documented as unresolved.
This census does not certify proofs or implement omitted algorithms.

The source has 36 pages. Main text and references occupy pages 1–27; Appendix A
starts on page 28. Only its heading was inspected. The source register's
filename-style version label and unversioned URL identify the same PDF bytes;
the inventory preserves the more precise versioned URL. Equivalence to the
final published text has not been asserted.

Resolve the source from the repository root:

```sh
python3 scripts/resolve_paper_pdf.py aos-2024-v52-i03-p1227
```

Rebuild the six content artifacts in an empty directory:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1227/scripts/rebuild.py --output-dir [local path omitted]
```

The rebuild verifies the fixed local source, validates structure and compares
output bytes. It does not produce a new source-review verdict. The previous
inventory script and cache-path provenance are preserved under
`review-history/before-local-source-rebuild/`; active scripts now use the fixed
local resolver.
