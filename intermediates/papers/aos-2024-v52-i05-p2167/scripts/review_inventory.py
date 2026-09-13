"""Independently enumerate and validate every labeled main-text theorem occurrence."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='44a127933d66ac09465676039b9055befaaf6aa90378ade1d18248ea847f80f8'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==83
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['WASSERSTEIN GENERATIVE ADVERSARIAL NETWORKS ARE MINIMAX OPTIMAL DISTRIBUTION ESTIMATORS','ARTHUR STÉPHANOVITCH','EDDIE AAMARI','CLÉMENT LEVRARD','arXiv:2311.18613v2','12 Mar 2025']:assert s in first,s
    assert 'SUPPLEMENTARY MATERIAL' in pdf[24].get_text(clip=fitz.Rect(100,371,520,389))
    labels=[];hashes={}
    for n in range(1,26):
        page=pdf[n-1];clip=None if n<25 else fitz.Rect(0,0,page.rect.width,370)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];text=''.join(s['text'] for s in ss).strip()
                formal=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text)
                overview=re.match(r'Theorem (\d+\.\d+) (For|Let)\b',text)
                if formal:
                    assert any(s['text']=='HEOREM' and s['font']=='NimbusRomNo9L-Regu' and 8.7<s['size']<8.9 for s in ss)
                    labels.append([n,formal[1],'formal_theorem'])
                elif overview:
                    assert ss[0]['font']==ss[1]['font']=='NimbusRomNo9L-Medi'
                    labels.append([n,overview[1],'overview_statement'])
    expected=[[5,'4.1','overview_statement'],[7,'5.8','overview_statement'],[7,'5.1','overview_statement'],[11,'3.1','formal_theorem'],[16,'4.1','formal_theorem'],[20,'5.1','formal_theorem'],[23,'5.4','formal_theorem'],[23,'5.7','formal_theorem'],[24,'5.8','formal_theorem']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-25.txt').read_text();assert 'manifolds with several charts.' in last and 'SUPPLEMENTARY' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==9
    assert [c['source_order'] for c in cs]==list(range(1,10))
    for c,(page,num,kind) in zip(cs,expected):
        assert c['label']=='Theorem '+num and c['occurrence_kind']==kind and c['evidence'][0]['page']==page
        assert c['claim_id']==PID+'/T'+num+('-overview' if kind=='overview_statement' else '')
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    assert 'theoretical classes' in s['4.1-overview'] and 'Model 1' in s['4.1-overview']
    assert 'Model 3' in s['5.8-overview'] and 'simultaneously' in s['5.8-overview'] and r'\gamma\in[1,\beta+1]' in s['5.8-overview']
    assert 'and $K$-density regularity conditions' in s['5.1-overview'] and 'with $g^\star$ that verifies' in s['5.1']
    for n in ['5.1-overview','5.1']:
        for t in [r'\le C^{-1}',r'\epsilon\in(0,1)',r'C_2\log(\epsilon^{-1})^4',r'^{\frac{\beta+\gamma}{2\beta+1}}+\epsilon']:assert t in s[n],(n,t)
    for t in [r'\min_{\delta\in[0,1]}',r'(\delta+1/n)^2',r'\log(n|\mathcal G_{1/n}||\mathcal D_{1/n}|)',r'\delta^{(1-\frac d{2\gamma})}',r'\mathbf1_{\{2\gamma=d\}}']:assert t in s['3.1'],t
    assert '(4.1) and (4.2)' in s['4.1']
    for n in ['5.4','5.7','5.8']:assert '(5.1) and (5.3)' in s[n] and 'Definition 2.1' in s[n]
    for t in [r'\mathbb E[\Delta_{\mathcal D}^{\widehat g}]',r'(\mathcal D_{\mathcal G})_{1/n}',r'\frac d{2(\widetilde\beta+1)}',r'\mathbf1_{\{\beta+1=d/2\}}']:assert t in s['5.4'],t
    assert r'\mathbf1_{\{\widetilde\beta+1=d/2\}}' not in s['5.4']
    assert r'n^{-\frac{2\widetilde\beta+1}{2\widetilde\beta+d}}' in s['5.7'] and r'\vee' not in s['5.7']
    assert r'\gamma\in[1,\widetilde\beta+1]' in s['5.8'] and r'n^{-\frac{\beta+\gamma}{2\beta+d}}\vee n^{-\frac12}' in s['5.8']
    for c in cs:
        text=c['statement_original'];assert text.count('$')%2==0 and text.count(r'\[')==text.count(r'\]')
        assert 'PROOF' not in text and not any(ord(ch)<32 and ch!='\n' for ch in text)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2167-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent small-cap formal-heading and bold overview-heading enumeration, visual comparison of all nine labeled statements, source-specific checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[5,7,11,16,20,23,24,25],main_text_end_clip=dict(page=25,y_max=370)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Six distinct theorem numbers appear in six formal statements and three separately labeled overview statements. All nine occurrences are retained.','The overview of Theorem 5.1 requires density regularity of both maps; the formal version requires it only of g-star.','Theorem 5.8 overview uses gamma up to beta+1; the formal statement prints gamma up to tilde-beta+1.','Theorem 5.4 prints beta, not tilde-beta, in its critical indicator. The endpoint delta=0 remains in both printed minima.','This validates the inventory only; definition and dependency extraction remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2311.18613',registered_version_alias='2311.18613v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=9,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract main-text definitions and assumptions, preserve appendix-only construction references, and independently validate the full census.'))
    print('All nine labeled theorem occurrences independently source-validated.')
if __name__=='__main__':main()
