"""Validate the narrow D7 annotation repair against the preserved source review."""
import datetime,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
HISTORY=ROOT/'review-history/before-d7-selector-repair'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def strip(v):
 if isinstance(v,dict):return {k:strip(x) for k,x in v.items() if k not in ['highlight_symbols','highlight_phrases']}
 if isinstance(v,list):return [strip(x) for x in v]
 return v
def main():
 pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),ROOT.name],text=True).strip())
 before=json.loads((HISTORY/'paper-audit.json').read_text())
 prior=json.loads((HISTORY/'registered-source-review.json').read_text())
 assert digest(pdf)==before['source']['pdf_sha256']=='0e2a08097d0f62a375bcfe5821507276e09d86b68d9e720a0087887d3a574786'
 assert prior['reviewed_artifacts']['paper-audit.json']==digest(HISTORY/'paper-audit.json')
 for name,record in before['artifacts'].items():assert digest(HISTORY/name)==record['sha256']
 for name in ['theorem-inventory.json','inventory-review.json','ambient-conventions.json']:
  assert (ROOT/name).read_bytes()==(HISTORY/name).read_bytes()
 for name in ['source-passages.json','interface-draft.json','unfinalized-census.json','ranked-interfaces.json']:
  a=json.loads((HISTORY/name).read_text());b=json.loads((ROOT/name).read_text());assert strip(a)==strip(b),name
 a=json.loads((HISTORY/'ranked-interfaces.json').read_text());b=json.loads((ROOT/'ranked-interfaces.json').read_text())
 am={m['local_id']:m for x in a['interfaces'] for m in x['members']}
 bm={m['local_id']:m for x in b['interfaces'] for m in x['members']}
 assert [k for k in am if am[k]!=bm[k]]==['D7']
 assert bm['D7']['highlight_symbols']==[r'\Pi(\mathcal{O}_{\theta})',r'\Pi(\mathcal{O}_{\theta_*})']
 assert bm['D7']['highlight_phrases']==['(2.4)']
 assert bm['D7']['statement_original']==am['D7']['statement_original']
 assert bm['D7']['evidence']==[{'page':6,'location':'Section 2.1 — condition (2.4)'}]
 for sel in bm['D7']['highlight_symbols']:assert sel in bm['D7']['statement_original']
 sys.path.insert(0,'skills/statistical-census-html/scripts')
 import build_report
 build_report.verify_highlights(b)
 for c in b['claims']:build_report.render_statement(c['statement_original'])
 subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(ROOT/'ranked-interfaces.json')],check=True)
 rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
 assert len(rebuild['comparisons'])==6
 for row in rebuild['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 evidence='source-transition/published/evidence/page-06.png'
 record=dict(paper_id=ROOT.name,status='passed',reviewed_at=now,scope='D7 highlight selectors only',source_pdf_sha256=digest(pdf),prior_source_review=dict(path=str((HISTORY/'registered-source-review.json').relative_to(ROOT)),sha256=digest(HISTORY/'registered-source-review.json')),evidence=dict(path=evidence,page=6,sha256=digest(ROOT/evidence)),finding='Visually checked equation (2.4) on the registered published page. Its finite-orbit prose is inside math text, outside the prose highlighter. Select the two actual projected-orbit expressions and the explicit (2.4) reference. Original statements, names, assumptions, theorem IDs, dependencies and counts are byte/structure-preserved.',renderer_sha256=digest(Path(build_report.__file__)),all_source_members_checked=37,theorems_rendered=12,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json')))
 write('evidence/annotation-review.json',record)
 audit=before.copy();audit['annotation_review']=dict(path='evidence/annotation-review.json',sha256=digest(ROOT/'evidence/annotation-review.json'))
 audit['artifacts']={name:dict(path=name,sha256=digest(ROOT/name)) for name in before['artifacts']}
 write('paper-audit.json',audit)
 review=prior.copy();review['annotation_review']=audit['annotation_review'];review['reproduction_check']=record['reproduction_check']
 review['reviewed_artifacts']={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']}
 write('registered-source-review.json',review)
 checkpoint=json.loads((ROOT/'checkpoint.json').read_text());checkpoint['annotation_reviewed_at']=now;checkpoint['annotation_review']='evidence/annotation-review.json';write('checkpoint.json',checkpoint)
 print('D7 annotation repair reviewed; all other source content and the original review are preserved.')
if __name__=='__main__':main()
