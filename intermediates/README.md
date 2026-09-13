# AOS 2024 paper census

Open [the searchable report](aggregate/report.html) for the corpus-wide **By paper**
and **Top APIs** views. Keep `report.html` with its sibling `report-pages/` directory;
the mathematical text and reading pages work offline. Original PDF and mathlib
links open their external sources.

Drag the divider between the list and reader to adjust their widths. The ratio is
remembered across reopening and reloads; double-click resets it. A focused divider
also supports arrow keys and Home/End. Mobile readers remain full-screen.

The reviewed corpus contains 113 papers, 637 main-text Theorems and 2,655 source
passages grouped into 2,486 ranked interfaces. The aggregate census is
`aggregate/ranked-interfaces.json`; its completed library comparison is
`aggregate/audited.json`. Per-variant comparison details and the source/link pins
remain in `aggregate/mathlib-search-progress.json` and `aggregate/mathlib-evidence/`.
Source ambiguities remain documented separately from the original statements.

Top APIs displays separate **Theorems / Papers** and **Status** columns. Counts are
deduplicated across all related theorem statements and the papers containing them.
For example, 27 / 5 means 27 theorem statements in 5 papers. Status labels retain text
as well as color. The three buttons filter Top APIs; clicking the selected button again
shows all statuses. The selection persists across navigation and reloads.

Each API uses the approved three-tier work assessment:

- **Use mathlib** (green; 542): an existing interface or direct composition suffices.
- **Small adaptation** (yellow; 1,790): the core mathematics exists, with a thin wrapper,
  representation conversion or local connecting proof still needed.
- **New infrastructure** (red; 154): an essential construction, core property or reusable
  theory required by the interface needs development.

**About ranking** explains these meanings and the boundary: missing mathematical content,
not code length or a missing same-name declaration. Assessments concern the archived
interface and its variants, not proofs of every related theorem. They are planning estimates
from the completed pinned audit evidence, not fresh searches or compiled Lean implementations.
Original comparisons, links and source caveats are preserved. See
`aggregate/work-status-audit.json` and `aggregate/work-status-validation.json`.

The report retains the approved two-paper reading style with the requested API
columns and status colors. Its rank column accommodates four-digit ranks; count
and status cells remain side by side on narrow screens. Final
release evidence is recorded in `aggregate/html-verification.json`, with complete
route/highlight checks and desktop/mobile browser evidence. The phase ledger is
`reviewed-html-workflow.json`.

Audit the 113 original research articles in volume 52, one paper at a time, using
`statistical-paper-census`. The pinned list is in `corpus.json`; `progress.json`
accounts for every paper and identifies the next unfinished one.

Each completed paper has an independent `theorem-inventory.json`,
`unfinalized-census.json`, `ranked-interfaces.json`, and `paper-audit.json` under
`papers/<paper-id>/`. The audit record binds the source review to exact artifact
hashes. Main-text Theorems are included; appendices, Lemmas, Propositions, and
Corollaries are outside the theorem inventory.

Review the original PDF and relevant main-text passages before recording
completion. A successful schema check cannot establish source fidelity. Preserve
original statements, including source anomalies, and keep explanatory notes
separate. Available source images and enumeration evidence accompany the audit.

Refresh the progress record after finishing a paper:

```sh
python3 reports/aos-2024-census/scripts/refresh_progress.py
```

This revalidates per-paper inventories and censuses, reviewed artifact hashes,
paper identity, and source pins. Missing or invalid work cannot count as a
completed paper or as zero theorems. `source_acquired` means only that a source
checkpoint exists. Progress entries are saved state, not evidence that a worker
is currently running.

Earlier issue-4 audits retain their own revalidation status in `progress.json`.
New audits advance in corpus order. Resolve source PDFs through
`scripts/resolve_paper_pdf.py` and the fixed `local-pdfs/aos/2024/` directory.
Their registered versions, original URLs and hashes remain pinned in each
paper's artifacts. Historical search records do not override the active
per-paper checkpoint or the current local source register.
