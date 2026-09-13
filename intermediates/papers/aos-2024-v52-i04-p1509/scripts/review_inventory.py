"""Validate the independently enumerated and visually reviewed original theorem."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
EXPECTED_INVENTORY_SHA='8a24f229d677f4af2da260d91ad190bb996e3e4d2e199107b11f0d7766835933'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source);assert len(pdf)==66 and 'arXiv:2303.13598v3' in pdf[0].get_text()
    headings=[];text_hashes={}
    for n in range(1,21):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,670.2371826171875) if n==20 else page.rect;text=page.get_text(clip=clip)
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<20 else 'page-20-before-appendix.txt');assert path.read_bytes().decode()==text;text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);m=re.match(r'^THEOREM (\d+)\.',s)
                if m:headings.append((n,m[1]))
    assert headings==[(9,'1')]
    assert text.rstrip().endswith('and this is another desirable feature of our proposed method.')
    boundary=pdf[19].get_text(clip=fitz.Rect(0,670,pdf[19].rect.width,684))
    assert 'APPENDIX A: TECHNICAL RESULTS AND OMITTED DETAILS' in boundary
    invpath=ROOT/'theorem-inventory.json';assert hashlib.sha256(invpath.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(invpath.read_text());assert len(inv['claims'])==1 and inv['claims'][0]['claim_id']==PID+'/T1'
    s=inv['claims'][0]['statement_original'];assert s.startswith('Suppose Assumptions A, B, and C are satisfied. Then (2) and (7) hold, and')
    assert r'\sup_{t\in\mathbb R}' in s and r'\widetilde\theta_n^*(\mathsf x)-\widehat\theta_n(\mathsf x)' in s
    assert r'\widehat\theta_n(\mathsf x)-\theta_0(\mathsf x)' in s and r'=o_{\mathbb P}(1).\tag{8}' in s
    assert 'r_n' not in s and 'confidence' not in s
    assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(invpath)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1509-inventory-') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==invpath.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,d):(ROOT/name).write_text(json.dumps(d,indent=2)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[PID+'/T1'],method='Independent small-cap THEOREM-heading enumeration and visual comparison of the full statement; schema validation and exact isolated rebuild.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,9,20],boundary_crop='evidence/page-20.png'),notes=['Exactly one Theorem occurs before the appendix boundary. Theorem A.1 is cited in main text but its appendix environment is excluded.','The original theorem ends at (8). The following confidence-interval implication is separate prose, not an additional theorem clause.','Theorem 1 incorporates equations (2) and (7) by reference. They must be preserved and resolved as supporting main-text passages without modifying the inventoried original body.','Source font inspection distinguishes the fixed sans-serif evaluation point from the italic running variable and the Fraktur characteristic exponent from derivative indices.','Full supporting-passage extraction and source-content review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2303.13598v3.pdf',registered_url_alias='https://export.arxiv.org/pdf/2303.13598',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=1,source_pdf_sha256=SHA,next_action='Extract original generalized Grenander estimator, bootstrap transformation, limit law and all parts of Assumptions A-C; resolve equations (2) and (7), retaining appendix-only domain conventions as unresolved.'))
    print('One complete original theorem independently validated; full census remains pending.')
if __name__=='__main__':main()
