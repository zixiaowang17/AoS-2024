"""Verify a paper's explicit rendering amendment without replacing its source review."""
import argparse,copy,datetime,hashlib,json,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def differences(a,b,path=()):
    if type(a)!=type(b):return [(path,a,b)]
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        return [z for k in a for z in differences(a[k],b[k],path+(k,))]
    if isinstance(a,list):
        if len(a)!=len(b):return [(path,a,b)]
        return [z for i,(x,y) in enumerate(zip(a,b)) for z in differences(x,y,path+(i,))]
    return [] if a==b else [(path,a,b)]
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('paper_id');a=ap.parse_args()
    root=BASE/'papers'/a.paper_id
    plan=json.loads((root/'scripts/rendering-amendment.json').read_text())
    history=root/plan['history']
    pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),a.paper_id],text=True).strip())
    assert digest(pdf)==plan['source_pdf_sha256']
    prior=json.loads((history/'registered-source-review.json').read_text())
    audit=json.loads((history/'paper-audit.json').read_text())
    for name,h in prior['reviewed_artifacts'].items():assert digest(history/name)==h,name
    for name,ref in audit['artifacts'].items():assert digest(history/ref.get('path',name))==ref['sha256'],name
    expected=plan['changes'];actual=[]
    for name in plan['content_files']:
        before=json.loads((history/name).read_text());after=json.loads((root/name).read_text())
        actual.extend(dict(artifact=name,path=list(p),before=x,after=y) for p,x,y in differences(before,after))
    assert actual==expected,'Unreviewed or missing content changes.'
    for item in plan['evidence']:assert digest(root/item['path'])==item['sha256']
    census=json.loads((root/'ranked-interfaces.json').read_text())
    sys.path.insert(0,'skills/statistical-census-html/scripts')
    import build_report
    build_report.verify_highlights(census)
    for c in census['claims']:build_report.render_statement(c['statement_original'])
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(root/'ranked-interfaces.json')],check=True)
    reproduction=root/plan['reproduction_check']
    check=json.loads(reproduction.read_text())
    assert len(check['comparisons'])==6
    for r in check['comparisons']:assert r['matches_saved_bytes'] and r['saved_sha256']==r['regenerated_sha256']==digest(root/r['artifact'])
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    record=dict(paper_id=a.paper_id,status='passed',reviewed_at=now,scope=plan['scope'],finding=plan['finding'],
        source_pdf_sha256=digest(pdf),prior_source_review=dict(path=str((history/'registered-source-review.json').relative_to(root)),sha256=digest(history/'registered-source-review.json')),
        evidence=plan['evidence'],changes=actual,renderer_sha256=digest(Path(build_report.__file__)),
        source_review_renewed=False,reproduction_check=dict(path=plan['reproduction_check'],sha256=digest(reproduction)))
    def save(n,v):(root/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
    save('evidence/rendering-amendment-review.json',record)
    ref=dict(path='evidence/rendering-amendment-review.json',sha256=digest(root/'evidence/rendering-amendment-review.json'))
    audit=copy.deepcopy(audit);audit['rendering_amendment']=ref
    for name,r in audit['artifacts'].items():r['sha256']=digest(root/r.get('path',name))
    save('paper-audit.json',audit)
    prior=copy.deepcopy(prior);prior['rendering_amendment']=ref;prior['reproduction_check']=record['reproduction_check']
    for name in prior['reviewed_artifacts']:prior['reviewed_artifacts'][name]=digest(root/name)
    save('registered-source-review.json',prior)
    checkpoint=json.loads((root/'checkpoint.json').read_text());checkpoint['rendering_amendment_reviewed_at']=now;checkpoint['rendering_amendment']=ref
    save('checkpoint.json',checkpoint)
    print(a.paper_id+': explicit amendment, strict highlights, census validation and six-file reproduction passed.')
if __name__=='__main__':main()
