"""Rebuild the reviewed offline reinforcement learning census without modifying its audit or source evidence."""
import argparse,hashlib,json
from pathlib import Path
import save_inventory,extract_interfaces,finalize_paper,save_ambient
ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=['theorem-inventory.json','source-passages.json','interface-draft.json','ambient-conventions.json','unfinalized-census.json','ranked-interfaces.json']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args();out=args.output_dir.resolve()
 if out.exists() and any(out.iterdir()):ap.error('Output directory must be empty.')
 (out/'evidence').mkdir(parents=True,exist_ok=True)
 for module in [save_inventory,extract_interfaces,finalize_paper,save_ambient]:module.ROOT=out
 save_inventory.main();finalize_paper.main();save_ambient.main()
 comparisons=[]
 for name in ARTIFACTS:
  p=out/name;q=ROOT/name
  comparisons.append(dict(artifact=name,matches_saved_bytes=p.read_bytes()==q.read_bytes(),saved_sha256=digest(q),regenerated_sha256=digest(p)))
 record=dict(paper_id=ROOT.name,output_directory=str(out),comparisons=comparisons,source_review_performed_by_rebuild=False,note='Regenerates the original reviewed extraction and reruns finalization. Source PDF resolves from the fixed local register; source reviews and original evidence are unchanged.')
 (out/'rebuild-check.json').write_text(json.dumps(record,indent=2)+'\n')
 if not all(x['matches_saved_bytes'] for x in comparisons):raise SystemExit('Reproduction differs; inspect temporary output without replacing the saved census.')
 print('All six content artifacts reproduced exactly.')
if __name__=='__main__':main()
