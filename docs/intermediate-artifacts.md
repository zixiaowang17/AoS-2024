# Intermediate research artifacts

[Browse per-paper records](../intermediates/index.html) or inspect the
[file manifest](../intermediates/export-manifest.json).

The intermediate archive contains the recorded research stages of the 113-paper experiment:

- Per-paper theorem inventories, source passages, interface extraction, dependency records,
  ambient prerequisites, review records, checkpoints and construction scripts.
- Working corpus assembly, grouping candidates, reconciliation, source relationships,
  aliases, validation records and paper-to-corpus mappings.
- Mathlib search checkpoints, declaration/link evidence, inspected source files and work
  estimates, including earlier status policies.
- Saved review histories and the skill snapshot used during the experiment.

The current reusable skills are in `skills/`. Historical scripts and skill copies are kept
for inspection; they may refer to private inputs, older layouts or pre-redaction hashes.
They are not all supported entry points for rerunning the workflow. Use the top-level build
scripts for the bundled demo, final report and blog.

## What was changed for the public copy

Machine-specific path prefixes are replaced by relative paths or explicit placeholders.
Every exported file has its original and public SHA-256 hash in `export-manifest.json`,
with the transformation and substitution count. Files needing no path change retain their
original bytes. Mathematical statements and recorded work estimates are not rewritten.

Embedded hashes inside historical records retain their original meaning. A hash check
against a redacted file may therefore fail; compare the source and export hashes in the
manifest before interpreting that as a research change. A saved `complete` or `validated`
flag is a historical workflow record, not a new review or proof certificate.

The final scientific files in `experiments/aos-2024/` remain byte-for-byte copies of the
previously released census and audit, with their own export provenance.

## Excluded files

PDFs, PDF page images, raw paper text/TeX copies, local source registries, private execution
and preparation files, environments, bytecode and duplicate HTML generations are excluded.
The current complete report and every current reader are included. Source URLs, PDF hashes,
extracted theorem/definition statements, review evidence and historical research JSON remain.
The manifest reports exclusion counts by category; this is a public research archive, not
a copy of the private workspace.
