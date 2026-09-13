# AoS-2024

How much of the mathematics in Annals of Statistics 2024 can we express with mathlib?
This repository collects **113 papers**, **637 main-text Theorems** and **2,486 interfaces**,
with source passages and estimates of the work still needed.

## [Open the live dashboard →](https://zixiaowang17.github.io/AoS-2024/experiments/aos-2024/report.html?view=apis)

[![Dashboard preview showing the ranked APIs](docs/dashboard.png)](https://zixiaowang17.github.io/AoS-2024/experiments/aos-2024/report.html?view=apis)

Search by paper or API, read the source statements, and inspect the mathlib audit.

## Files in this repository

- `skills/`: the three skills, their validators and the HTML generator.
- `experiments/aos-2024/`: the report and saved census and audit data.
- `intermediates/`: extractions, checkpoints, grouping decisions, review history and mathlib evidence. [Browse the records](intermediates/index.html).
- `examples/synthetic/`: a software demo with invented data.
- `docs/blog-post.md`: the editable blog post, alongside its HTML and screenshot.

PDFs are not included. See [export details](docs/intermediate-artifacts.md) for what was
included and how private paths were removed.

## Reusable skills

| Skill | Purpose |
| --- | --- |
| [statistical-paper-census](skills/statistical-paper-census/SKILL.md) | Preserve every main-text Theorem and connect definitions and conditions to their uses. |
| [ranked-mathlib-audit](skills/ranked-mathlib-audit/SKILL.md) | Search a pinned mathlib revision, record inspected declarations, and describe the remaining work. |
| [statistical-census-html](skills/statistical-census-html/SKILL.md) | Build the By paper / Top APIs report with source passages, highlighted notation and linked theorems. |

The skills guide an agent through reading papers, grouping interfaces and checking mathlib.
These judgments need review.

The scripts require Python 3.9+ and Pandoc (tested with Python 3.9.6 and Pandoc 3.8.2.1).
Rebuilding the report needs no API key. Auditing new papers requires an agent that can read
the PDFs and search mathlib.

## Install and use

Copy the three skill directories into your agent's skill directory, keeping them as siblings.
For a Codex installation using `~/.codex/skills`:

```sh
python3 scripts/install_skills.py --dest ~/.codex/skills
```

The installer will not overwrite existing skills.

A starting request for your agent:

> Use $statistical-paper-census to inventory the main-text Theorems and their interfaces in
> these local papers. Then use $ranked-mathlib-audit for the library comparisons and
> $statistical-census-html for the report. Preserve source statements and record unresolved
> questions. Keep PDFs private and write artifacts in English.

## Try the software demo

The two-paper review and the 113-paper experiment use real research papers. This separate
demo uses invented data so the tools can be run without PDFs.

```sh
python3 scripts/build_demo.py
```

Open `examples/synthetic/report.html` locally. Its statements and status labels are examples;
the source links are placeholders.

## Reproduce the experiment report

```sh
python3 scripts/build_experiment.py
```

This checks the saved data and rebuilds the report and detail pages. It takes several
minutes and uses the existing audit; it does not reread the PDFs or search mathlib again.

To view the report offline, open `experiments/aos-2024/report.html` after cloning the
repository. Keep its `report-pages/` directory beside it. External source links need an
internet connection.

## Review status

I checked the workflow in detail on two real papers: 11 Theorems and 35 interfaces. I then
used agents to run it on the 113 Annals papers. I have not independently checked every entry
in that larger run. The saved records include source questions and mathlib comparisons.

The labels—**Use mathlib**, **Small adaptation**, and **New infrastructure**—estimate the
work needed for each interface. They do not certify proofs of the papers' theorems. Some
labels were reassessed from saved evidence and still need checking.

Found a mistake? Please include the paper or API and the source passage or mathlib
declaration in your correction. See [Contributing](CONTRIBUTING.md).

## Checks

```sh
python3 skills/statistical-census-html/scripts/test_workflow.py
python3 scripts/check_release.py
```

The tests check data consistency and report generation. The release scan checks for PDFs,
private paths, common credential patterns and unexpected files. These checks cannot verify
the mathematics or catch every possible disclosure.

Code, skill instructions and templates retain the source project's Apache-2.0 license.
Paper quotations retain their original attribution and are not relicensed by this repository.
See [LICENSE](LICENSE) and [NOTICE](NOTICE).
