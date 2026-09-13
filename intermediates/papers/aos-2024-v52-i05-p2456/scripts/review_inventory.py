"""Independently enumerate the three small-cap Theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='a5dabb65fb4a8cc35782f5f6af7c48d348aaed7f7370a7cfeadd23968d93b7c6'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==25
    first=' '.join(pdf[0].get_text().split())
    for v in ['Submitted to the Annals of Statistics','A GAUSSIAN PROCESS APPROACH TO MODEL CHECKS','JUAN CARLOS ESCANCIANO']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='AOS2401-003R2A0.pdf' and registered['source_url']==URL
    lastpage=pdf[19];assert 'APPENDIX: MATHEMATICAL PROOFS' in lastpage.get_text(clip=fitz.Rect(0,216,lastpage.rect.width,242))
    labels=[];hashes={}
    for n in range(1,21):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,216) if n==20 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(span['text'] for span in line['spans']).strip()
                match=re.match(r'^THEOREM\s+(\d+\.\d+)\.$',text)
                if match:labels.append([n,match[1]])
    expected=[[11,'4.1'],[12,'4.3'],[13,'4.4']];assert labels==expected,labels
    last=(ROOT/'evidence/page-20.txt').read_text();assert 'future research' in last and 'APPENDIX' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==3
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label']=='Theorem '+n and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    assert s['4.1']==r'Let Assumption A hold. Then, $S_n\Longrightarrow S_\infty$.'
    for v in ['Under Assumption B and $H_0$',r'\mathcal H_K^*',r'\widehat R_n\Longrightarrow R_\infty',r'\lambda_j\langle\varphi_j,\Pi a\rangle_{K^\perp}U_j',r'n\widehat Q_K^\perp\xrightarrow{d}\sum_{j=1}^\infty\lambda_jU_j^2']:assert v in s['4.3'],v
    assert r'\sqrt{\lambda_j}' not in s['4.3']
    assert s['4.4']==r'Under Assumption B, $\|\widehat R_n^*\|^2\xrightarrow{d}\|R_\infty\|^2$ a.s.'
    assert 'H_0' not in s['4.4']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2456-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent exact small-cap heading enumeration, visual comparison of all three statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[11,12,13,20],main_text_end_page=20,last_page_clip_y=216),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Three main-text Theorem environments; Propositions4.2 and4.5 are not Theorems.','Preserve the lambda coefficient with the K-perp inner product in T4.3, and T4.4’s lack of an explicit H0 assumption.','AssumptionB(i)–(iv) precedes the theorems. Its later local-power addition(v) is not imported retroactively.','Inventory validation only; source-context extraction and independent dependency review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=URL,registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=3,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract the RKHS/dual and AssumptionA Gaussian limit, CMR and Neyman projections, feasible process/quadratic statistic, spectral quantities, AssumptionB(i)–(iv), bootstrap multipliers and conditional convergence. Exclude later AssumptionB(v) and proof-only Proposition4.2 dependencies.'))
    print('All three theorem statements independently source-validated.')
if __name__=='__main__':main()
