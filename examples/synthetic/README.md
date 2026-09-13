# Software demo with invented data

The [two-paper review](../../docs/review-summary.md#two-paper-trial) used real research
papers, as did the 113-paper Annals of Statistics experiment. This separate software demo
uses invented records to show how to run the tools without PDFs.

[Open the software demo](report.html). Its records are named **Synthetic paper A** and
**Synthetic paper B**. Their statements and status labels are examples, not audit findings.
No source PDFs or Lean checks were used; example.org URLs and zero-valued PDF hashes are
placeholders.

Run `python3 scripts/build_demo.py` from the repository root to recreate the inventory,
census, artificial audit, and HTML. All three normal validators and the renderer are used.
A fixture passing the schema is not evidence of a real source or library audit.
