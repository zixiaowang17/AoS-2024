"""Regenerate this paper's census in an empty directory without changing its audit.

Example: python3 -B scripts/rebuild.py --output-dir [local path omitted]
Statements and dependency choices are the saved, manually reviewed extraction;
running this script does not perform a new semantic review of the PDF.
"""
import argparse
import hashlib
import json
from pathlib import Path

import extract_interfaces
import finalize_paper
import save_ambient
import save_inventory

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ['theorem-inventory.json', 'source-passages.json', 'interface-draft.json',
             'ambient-conventions.json', 'unfinalized-census.json', 'ranked-interfaces.json']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        parser.error('The output directory must be empty; existing results are preserved.')
    output.mkdir(parents=True, exist_ok=True)
    for module in [save_inventory, extract_interfaces, finalize_paper, save_ambient]:
        module.ROOT = output
    save_inventory.main()
    finalize_paper.main()
    save_ambient.main()
    comparisons = []
    for name in ARTIFACTS:
        regenerated = output / name
        saved = ROOT / name
        same = regenerated.read_bytes() == saved.read_bytes()
        comparisons.append(dict(artifact=name, matches_saved_bytes=same,
                                regenerated_sha256=hashlib.sha256(regenerated.read_bytes()).hexdigest(),
                                saved_sha256=hashlib.sha256(saved.read_bytes()).hexdigest()))
    report = dict(paper_id=ROOT.name, output_directory=str(output),
                  comparisons=comparisons,
                  source_review_performed_by_rebuild=False,
                  note='Rebuilds extracted content and validates structure; preserves existing source-review records.')
    (output / 'rebuild-check.json').write_text(json.dumps(report, indent=2) + '\n')
    if not all(c['matches_saved_bytes'] for c in comparisons):
        raise SystemExit('Rebuilt content differs from saved artifacts; inspect rebuild-check.json.')
    print('All six census artifacts reproduced byte for byte.')


if __name__ == '__main__':
    main()
