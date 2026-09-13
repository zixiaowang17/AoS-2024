"""Independently enumerate the four small-cap Theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='a88b97e30b05dcbb0d1a32aab3726d0137ed562353e0618f3e8fe8fada657dfc'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==53
    first=' '.join(pdf[0].get_text().split())
    for v in ['NON-INDEPENDENT COMPONENTS ANALYSIS','GEERT MESTERS','PIOTR ZWIERNIK','arXiv:2206.13668v4','19 Mar 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2206.13668v4.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2206.13668'
    lastpage=pdf[20];assert 'REFERENCES' in lastpage.get_text(clip=fitz.Rect(0,575,lastpage.rect.width,600))
    labels=[];hashes={}
    for n in range(1,22):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,572) if n==21 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(span['text'] for span in line['spans']).strip()
                match=re.match(r'^THEOREM\s+(\d+\.\d+)\.$',text)
                if match:labels.append([n,match[1]])
    expected=[[9,'5.3'],[9,'5.5'],[11,'5.10'],[12,'5.14']];assert labels==expected,labels
    last=(ROOT/'evidence/page-21.txt').read_text();assert 'Acknowledgements.' in last and 'REFERENCES' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==4
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label']=='Theorem '+n and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    for v in [r'T\in S^r(\mathbb R^d)',r'r\ge3',r'T_{i\cdots i}\ne0',r'd-1',r'Q\bullet T\in\mathcal V^{\mathrm{diag}}',r'\mathcal G_T(\mathcal V^{\mathrm{diag}})=\operatorname{SP}(d)',r'If $r=2$',r'T_{jj}\ne T_{kk}']:assert v in s['5.3'],v
    for n in ['5.5','5.14']:
        for v in ['Consider the model (1)',r'\mathbb E\varepsilon=0',r'\operatorname{var}(\varepsilon)=I_d',r'h_r(\varepsilon)','identifiable up to permuting and swapping signs of its rows']:assert v in s[n],(n,v)
    assert 'at most one zero on the diagonal' in s['5.5'] and 'some $r\ge3$' in s['5.5']
    for v in ['even $r$','reflectionally invariant',r'l=(r-2)/2',r'\sum_{i_1,\ldots,i_l}T_{i_1i_1\cdots i_li_ljj}\ne\sum_{i_1,\ldots,i_l}T_{i_1i_1\cdots i_li_lkk}',r'\mathcal G_T(\mathcal V^{\mathrm{refl}})=\operatorname{SP}(d)']:assert v in s['5.10'],v
    assert 'some even $r$' in s['5.14'] and 'genericity condition (14)' in s['5.14']
    assert '(13)' in s['5.3'] and '(14)' in s['5.10']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2506-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent exact small-cap heading enumeration, visual comparison of all four statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,9,11,12,21],main_text_end_page=21,last_page_clip_y=572),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Four main-text Theorem environments5.3,5.5,5.10,5.14; Corollary5.15 and all propositions/lemmas are excluded.','Preserve the separate r=2 distinct-diagonal condition in5.3 and the repeated-pair-index sums in5.10.','Theorems5.5/5.14 concern model(1) and h_r, with original row-sign/permutation conclusions; neither is rewritten as an independence assumption.','The registered title uses components (plural); the queue title uses component. The local source identity is pinned by hash, not by title spelling.','Inventory validation only; full definitions, assumptions and dependency review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract symmetric tensors and their action, moment/cumulant h_r, diagonal and reflectionally invariant spaces, orthogonal/sign-permutation conventions, model identifiability and condition(14). Keep algebraic tensor theorems separate from model-identification theorems. Validate the full census and reproducible scripts before completion.'))
    print('All four theorem statements independently source-validated.')
if __name__=='__main__':main()
