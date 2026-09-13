"""Independently enumerate and check the source-pinned two-Theorem inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='dff2e31dd002eb0b518c1ed3944ee9301516da2b115cc828ac24f3d0045c0f0c'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==36
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['TESTING HIGH-DIMENSIONAL REGRESSION COEFFICIENTS IN LINEAR MODELS','ALEX ZHAO','CHANGCHENG LI','RUNZE LI','ZHE ZHANG','available in PMC 2026 March 13','2034–2058']:assert s in first,s
    # Only the appendix heading is needed for this gate; its body is excluded.
    assert 'APPENDIX: PROOFS OF LEMMAS 2.1 AND 2.2' in pdf[23].get_text(clip=fitz.Rect(85,61,540,79))
    labels=[];hashes={}
    for n in range(1,24):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];s=''.join(x['text'] for x in ss).strip()
                m=re.match(r'^THEOREM (\d+)\.',s)
                if m:
                    assert any(x['text']=='HEOREM' and x['font']=='Helvetica-Bold' for x in ss)
                    labels.append((n,m[1]))
    assert labels==[(6,'1'),(8,'2')],labels
    last=(ROOT/'evidence/page-23.txt').read_text()
    assert 'Concluding remarks.' in last and 'Acknowledgments.' in last and 'Funding.' in last and 'APPENDIX:' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert [c['label'] for c in cs]==['Theorem 1','Theorem 2']
    assert [c['source_order'] for c in cs]==[1,2] and [[e['page'] for e in c['evidence']] for c in cs]==[[6],[8]]
    a,b=[c['statement_original'] for c in cs]
    for s in ['Assumptions A1 and A2',r'o(\sqrt{\min(n,p)})',r'k_n=o(\sqrt p)',r'under the null hypothesis $H_0$',r'under the local alternative hypothesis $H_a$ in (7)',r'n\|\boldsymbol\delta_z\|^2+nk_n|\boldsymbol\alpha^T\boldsymbol\delta_z|^2',r'\{2\operatorname{tr}(\Omega^2)\}^{1/2}',r'\boldsymbol\delta_z=\Sigma_X(\boldsymbol\beta-\boldsymbol\beta_0)']:
        assert s in a,s
    assert r'\widehat' not in a
    for s in [r'\gamma_0^2=\frac{p}{nS\sqrt{\operatorname{tr}(\Sigma_X^2)}}',r's\in[0,1/2]','all sequences of tests','asymptotically powerless','asymptotically powerful',r'\gamma^2/\gamma_0^2\to0',r'\gamma^2/\gamma_0^2\to\infty']:
        assert s in b,s
    assert 'Gaussian' in b.split('ii.')[0] and 'Gaussian' not in b.split('ii.')[1]
    assert r'k_n=o(\sqrt p)' not in b and 'local alternative' not in b
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert 'PROOF' not in s and not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2034-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration over all main-text pages, visual comparison of both complete statements, source-specific subpart checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[6,8,23],appendix_heading_clip=dict(page=24,y_min=61,y_max=79)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Theorem 1 contains both null and local-alternative limits; its population Omega in the centering denominator has no estimator hat.','Theorem 2(i) adds Gaussian errors; part (ii) does not. Theorem 2 does not print the k_n=o(sqrt(p)) condition of Theorem 1.','The random-effects alternative and the deterministic local alternative remain separate.','This inventory gate does not certify completion of the definitions/dependency census.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=URL,registered_version_alias='nihms-2151735.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract source definitions and assumptions, then independently validate the complete census.'))
    print('Both complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
