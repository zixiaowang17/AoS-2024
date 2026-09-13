# Deep nonlinear sufficient dimension reduction

Completed census of the registered published PDF, The Annals of Statistics
52(3), 2024, pages 1201–1226, DOI 10.1214/24-AOS2390.

- Six complete main-text Theorems: 3.2, 3.7, 3.8, 4.2, 4.4 and 4.6.
- 25 original definition or condition passages, 32 direct theorem uses and
  74 related theorem connections.
- Eight auxiliary source passages and 23 notes preserving ambient conventions
  and unresolved source details.

The [theorem inventory](theorem-inventory.json) preserves complete statements.
The [census](ranked-interfaces.json) adds original passages and paper-local
dependencies. [Ambient prerequisites](ambient-prerequisites.json) record source
conventions and unresolved meanings separately from those quotations.
[Source review](registered-source-review.json) and [audit](paper-audit.json)
pin the inspected artifacts by hash.

Theorem 4.6 includes its summed-risk and final expected-distance consequences.
Its last clause invokes the assumptions of Corollary 4.5, including the ReLU
architecture and Hölder condition. Those conditions are not added to Theorems
4.2 or 4.4. The first empirical minimizer and subsequent empirical steps are
stored separately, preserving which results use the covariance kernel.

The PDF has 26 pages and contains no appendix body. Page 23 only announces an
external supplement; that supplement was not opened. Original ambiguities,
including the range of epsilon in (A4), the mean-zero convention and the
unrounded network depth, remain documented. This is a source census, not proof
certification.

Resolve the fixed local source before any further source review:

```sh
python3 scripts/resolve_paper_pdf.py aos-2024-v52-i03-p1201
```

From the repository root, reproduce the six content artifacts in an empty
directory using the saved per-paper scripts:

```sh
python3 -B reports/aos-2024-census/papers/aos-2024-v52-i03-p1201/scripts/rebuild.py --output-dir [local path omitted]
```

The rebuild checks source identity, validates structure and compares output
bytes. It does not generate a new source-review verdict. The saved review
scripts pin the manually inspected artifact hashes and require a new review if
those artifacts change.

`source-search.json` and `source-search-checkpoint.json` are historical search
records predating local intake. The active status is in `checkpoint.json`;
the source is now available through the fixed local resolver.
