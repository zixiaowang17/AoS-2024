"""Reproduce the reviewed p0001 inputs and derive its census in an empty directory."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from reviewed_extraction import INVENTORY,UNFINALIZED,AMBIENT,RECOVERY_PROVENANCE
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
SKILL=Path('skills/statistical-paper-census/scripts')
ARTIFACTS=['theorem-inventory.json','source-passages.json','interface-extraction.json','ambient-prerequisites.json','unfinalized-census.json','ranked-interfaces.json']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args();out=args.output_dir.resolve()
 if out.exists() and any(out.iterdir()):ap.error('Output directory must be empty; existing review artifacts are preserved.')
 pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),ROOT.name],text=True).strip())
 assert digest(pdf)==INVENTORY['papers'][0]['pdf_sha256']
 out.mkdir(parents=True,exist_ok=True)
 sources=dict(paper_id=ROOT.name,members=[m for x in UNFINALIZED['interfaces'] for m in x['members']])
 extraction=dict(paper_id=ROOT.name,interfaces=UNFINALIZED['interfaces'])
 for name,value in zip(ARTIFACTS[:-1],[INVENTORY,sources,extraction,AMBIENT,UNFINALIZED]):
  (out/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(out/'theorem-inventory.json')],check=True)
 subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(out/'unfinalized-census.json'),str(out/'ranked-interfaces.json'),'--inventory',str(out/'theorem-inventory.json')],check=True)
 comparisons=[]
 for name in ARTIFACTS:
  saved=ROOT/name;new=out/name
  comparisons.append(dict(artifact=name,matches_saved_bytes=saved.is_file() and saved.read_bytes()==new.read_bytes(),saved_sha256=digest(saved) if saved.is_file() else None,regenerated_sha256=digest(new)))
 report=dict(paper_id=ROOT.name,output_directory=str(out),comparisons=comparisons,source_review_performed_by_rebuild=False,recovery_provenance=RECOVERY_PROVENANCE,note='Reproduces the literal previously reviewed extraction and rederives final ranks/paths. New source/context files organize the same checked data; no original review is overwritten.')
 (out/'rebuild-check.json').write_text(json.dumps(report,indent=2)+'\n')
 if not all(x['matches_saved_bytes'] for x in comparisons):raise SystemExit('Inspect output: one or more artifacts are absent or differ from the saved version.')
 print('All six content artifacts reproduced exactly; existing source certification unchanged.')
if __name__=='__main__':main()
