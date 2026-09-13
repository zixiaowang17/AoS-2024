"""Independently enumerate and validate the five main-text theorem statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='f19bc8f44e7fc74ceb4abab0eabc4f828822996a80630017fb3d631310260f34'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==31
    first=' '.join(pdf[0].get_text().split())
    for v in ['2311.07773v1','13 Nov 2023','November 15, 2023','Jing Lei','Anru R. Zhang','Zihan Zhu']:assert v in first,v
    lastpage=pdf[11];excluded=lastpage.get_text(clip=fitz.Rect(0,458,lastpage.rect.width,490));assert 'Proofs for Section' in excluded
    labels=[];hashes={}
    for n in range(1,13):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,458) if n==12 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        rows={}
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    if span['font']=='CMBX10':rows.setdefault(round(span['bbox'][1],1),[]).append(span)
        for y,spans in sorted(rows.items()):
            bold=' '.join(s['text'] for s in sorted(spans,key=lambda s:s['bbox'][0]))
            match=re.match(r'^Theorem\s+(\d+\.\d+)\s*\.?$',bold)
            if match:labels.append([n,match[1]])
    expected=[[6,'2.2'],[7,'3.1'],[8,'3.3'],[10,'4.1'],[11,'4.2']];assert labels==expected,labels
    last=(ROOT/'evidence/page-12.txt').read_text();assert 'Acknowledgement' in last and 'Proofs for Section' not in last and 'Proof of Lemma' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==5
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label'].startswith('Theorem '+n) and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'2.2':[r'T_n=n^a',r'\rho_n=n^{-b}',r'b\in(0,2)',r'1+a-b>0',r'1+a-b<0','assuming the low-degree polynomial conjecture',r'1+a/2-b>0',r'1+a/2-b<0','also hold for detection'],
'3.1':[r'nT_n^{1/2}\rho_n\ge C\sqrt{\log(n)}','absolute constant','Definition 1','polynomial-time algorithm'],
'3.3':['Conjecture 3.2','Assumption 1',r'\le(1/2)(\log n)^{-1.4}','for all $n$ large enough'],
'4.1':[r'nT_n\rho_n\to0',r'\sum_A P_{1,\tau,n}^2(A)/P_{0,n}(A)-1=o(1)',r'\forall\tau\in\mathcal S_{T_n}',r'd_{\chi^2}(P_{1,n},P_{0,n})=o(1)','indistinguishable'],
'4.2':['Assumption 1',r'nT_n\rho_n\to\infty',r'\ell_n(\widehat\sigma_{\mathrm{mle}},\sigma)\ge\epsilon','Definition 2','hence distinguishable']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert '[28]' in cs[1]['label']
    assert 'Conjecture' not in s['3.1'] and 'Conjecture' not in s['4.1'] and 'Conjecture' not in s['4.2']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2431-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font heading enumeration, visual comparison of all five statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[6,7,8,10,11,12],main_text_end_page=12,last_page_clip_y=458),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['All five main-text Theorem environments; appendix bodies excluded from the census.','Conjecture3.2 is an assumed source passage rather than a sixth Theorem. Preserve conditional computational lower bounds and both strong-detection/approximate-recovery meanings.','Inventory validation only; definition extraction and relationship review are separate.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2311.07773',registered_version_alias='2311.07773v1.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=5,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract balanced graph mixtures, recovery/detection, asymptotic regime, the assumed hardness conjecture, conditional laws, chi-square divergence and MLE; independently review marginal and quantifier scopes.'))
    print('All five theorem statements independently source-validated.')
if __name__=='__main__':main()
