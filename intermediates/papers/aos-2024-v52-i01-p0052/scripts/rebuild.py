"""Replay the retained, reviewed published-source extraction in an empty directory.

The transition scripts preserve the manual version comparison and extraction.
This command regenerates content and validates it; it does not perform a new
visual source review or promote any review record emitted in the temporary run.
"""
import argparse,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source-transition/published'
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
ARTIFACTS=['theorem-inventory.json','source-passages.json','interface-draft.json','ambient-conventions.json','unfinalized-census.json','ranked-interfaces.json']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(name):
 spec=importlib.util.spec_from_file_location('p0052_'+name,SOURCE/(name+'.py'))
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();out=a.output_dir.resolve()
 if out.exists() and any(out.iterdir()):ap.error('Output directory must be empty.')
 pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),ROOT.name],text=True).strip())
 assert digest(pdf)=='0e2a08097d0f62a375bcfe5821507276e09d86b68d9e720a0087887d3a574786'
 out.mkdir(parents=True,exist_ok=True)
 # Existing published-source evidence is read-only input to the original recipe.
 (out/'evidence').symlink_to((SOURCE/'evidence').resolve(),target_is_directory=True)
 inv=module('save_inventory');inv.ROOT=out;inv.main()
 extraction=module('build_census');extraction.ROOT=out;extraction.main()
 comparisons=[]
 for name in ARTIFACTS:
  p=out/name;saved=ROOT/name
  comparisons.append(dict(artifact=name,matches_saved_bytes=p.read_bytes()==saved.read_bytes(),saved_sha256=digest(saved),regenerated_sha256=digest(p)))
 report=dict(paper_id=ROOT.name,output_directory=str(out),comparisons=comparisons,source_review_performed_by_rebuild=False,note='Replays the retained published-source extraction recipe; does not renew or replace the existing registered source review.')
 (out/'rebuild-check.json').write_text(json.dumps(report,indent=2)+'\n')
 if not all(x['matches_saved_bytes'] for x in comparisons):raise SystemExit('Reproduction differs; inspect temporary output, preserving current artifacts.')
 print('All six published-source content artifacts reproduced exactly.')
if __name__=='__main__':main()
