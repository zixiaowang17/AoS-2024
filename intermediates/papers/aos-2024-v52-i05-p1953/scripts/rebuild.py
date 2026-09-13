"""Reproduce the saved extraction in an empty directory; do not certify source review."""
import argparse,hashlib,json
from pathlib import Path
import save_inventory,build_census
ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=['theorem-inventory.json','source-passages.json','interface-extraction.json','ambient-prerequisites.json','unfinalized-census.json','ranked-interfaces.json']
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args()
    out=args.output_dir.resolve()
    if out.exists() and any(out.iterdir()):parser.error('Output directory must be empty.')
    out.mkdir(parents=True,exist_ok=True)
    save_inventory.ROOT=out;build_census.ROOT=out
    save_inventory.main();build_census.main()
    comparisons=[]
    for name in ARTIFACTS:
        a=(ROOT/name).read_bytes();b=(out/name).read_bytes()
        comparisons.append(dict(artifact=name,matches_saved_bytes=a==b,saved_sha256=hashlib.sha256(a).hexdigest(),regenerated_sha256=hashlib.sha256(b).hexdigest()))
    report=dict(paper_id=ROOT.name,output_directory=str(out),comparisons=comparisons,source_review_performed_by_rebuild=False,note='Reproduces saved extraction and validates structure. A rebuild is not a new semantic source review.')
    (out/'rebuild-check.json').write_text(json.dumps(report,indent=2)+'\n')
    assert all(c['matches_saved_bytes'] for c in comparisons),comparisons
    print('All six census artifacts reproduced byte for byte.')
if __name__=='__main__':main()
