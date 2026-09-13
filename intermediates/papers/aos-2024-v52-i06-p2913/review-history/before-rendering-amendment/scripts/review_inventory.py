"""Independently enumerate and validate original Theorems3.1–3.3 before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='f54cc7f3587556c1d67391a893fd179b78fad33d528a7374d36ea2a419f4eb5f'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==39
    first=' '.join(pdf[0].get_text().split())
    for x in ['CHANGE POINT ANALYSIS WITH IRREGULAR SIGNALS','TOBIAS KLEY','YUHAN PHILIP LIU','HONGYUAN CAO','WEI BIAO WU','arXiv:2409.08863v1','13 Sep 2024']:assert x in first,x
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert reg['version']=='2409.08863v1.pdf' and reg['source_url']=='https://export.arxiv.org/pdf/2409.08863'
    labels=[];hashes={}
    for n in range(1,17):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                ss=l['spans']
                if not ss:continue
                t=''.join(s['text'] for s in ss)
                m=re.match(r'^THEOREM (3\.[123])\.',t)
                if m:labels.append([n,m[1]])
    expected=[[7,'3.1'],[8,'3.2'],[8,'3.3']];assert labels==expected,labels
    end=' '.join(pdf[15].get_text().split());assert end.endswith('partially supported by NSF DMS-2311249 and NSF DMS-2027723.')
    listing=' '.join(pdf[16].get_text(clip=fitz.Rect(0,0,pdf[16].rect.width,180)).split());assert 'SUPPLEMENTARY MATERIAL' in listing and 'Contains the proofs and additional simulation results.' in listing
    # Read only the appendix heading to confirm the excluded boundary.
    heading=' '.join(pdf[18].get_text(clip=fitz.Rect(0,235,pdf[18].rect.width,260)).split());assert 'APPENDIX A: PROOFS' in heading
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==3
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==([8,9] if n=='3.3' else [page])
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={'3.1':['short-range dependence',r'\Theta_{0,2}=\sum_{i\ge0}\delta_{i,2}<\infty',r'\sup_{x\le0}|\mathbb P(\hat T\le x)-e^{-2x^2}|\to0',r'(\tau/n)(1-\tau/n)d\sqrt n\to\infty',r'\hat T\to-\infty'],
    '3.2':['Condition 3.1',r'd\gg n^{-1/\theta}',r'n^{2/\theta}\log(n)\ll k\ll\tau',r'\hat\sigma^2=\sigma_\infty^2+O(1/k)+O_{\mathbb P}(\eta^{2/\min(4,\theta)-1})'],
    '3.3':['Condition 3.1',r'd\gg n^{-1/\theta}',r'n^{2/\theta}\log(n)\ll k\ll\tau',r'n-\tau\ge2k',r'K>\rho',r'd>Kd_*',r'\hat\sigma_\infty^2=\sigma_\infty^2+o_{\mathbb P}(1)',r'\hat\tau=\tau+O_{\mathbb P}(d_*^{-\theta/(\theta-1)})','used in (9)']}
    for n,vs in checks.items():
        for v in vs:assert v in s[n],(n,v)
    assert 'Corollary' not in s['3.3'] and '(i)' in s['3.1'] and '(ii)' in s['3.1']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for a,b in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    v=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2913-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent uppercase small-cap theorem-heading enumeration over main-text pages1–16; visual comparison of original statements and3.3 continuation; boundary inspection, source formula checks, structural validation and exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[7,8,9,16],main_text_end_page=16),validation=dict(returncode=v.returncode,stdout=v.stdout),notes=['Three actual Theorems3.1–3.3; Corollary3.1, narrative citations and appendix bodies excluded.','Theorem3.1 preserves its null supremum over nonpositive thresholds and alternative divergence condition.','Theorem3.2 preserves a deterministic bias order and a separate probabilistic rate in eta.','Theorem3.3 includes strict gap comparability, the arbitrary consistent long-run-variance estimator in9 and the full negative localization exponent.','Full source definitions, assumptions, dependencies and registered-source census review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=reg['source_url'],registered_version_alias=reg['version'],checked_at=now))
    p=ROOT/'checkpoint.json'
    if not p.exists() or json.loads(p.read_text()).get('stage')!='complete':write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=3,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original irregular-signal hypotheses, CUSUM statistic, batching/preliminary estimation and localization algorithm, long-run variance, functional dependence, Condition3.1, d_star and order conventions. Then finalize, reproduce and independently source-review the full census.'))
    print('Three complete original main-text Theorems independently source-validated.')
if __name__=='__main__':main()
