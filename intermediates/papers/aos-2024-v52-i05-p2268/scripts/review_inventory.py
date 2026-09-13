"""Independent heading enumeration and source-specific checks before interface extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED = '28273014aca487001d80d6df675ac352a55176d25069fb581d1d807cc6d5e745'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==65
    first=' '.join(pdf[0].get_text().split())
    for v in ['Environment Invariant Linear Least Squares','Jianqing Fan','Cong Fang','Yihong Gu','Tong Zhang','2303.03092v3','29 Nov 2024']:assert v in first,v
    assert 'References' in pdf[19].get_text(clip=fitz.Rect(0,624,pdf[19].rect.width,642))
    labels=[];hashes={}
    for n in range(1,21):
        page=pdf[n-1];clip=None if n<20 else fitz.Rect(0,0,page.rect.width,619)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans']
                if ss:
                    m=re.fullmatch(r'Theorem (\d+\.\d+)',ss[0]['text'].strip())
                    if m and ss[0]['font']=='CMBX10':labels.append([n,m[1]])
    assert labels==[[13,'4.2'],[14,'4.3'],[15,'4.4'],[16,'4.5']],labels
    last=(ROOT/'evidence/page-20.txt').read_text();assert 'Acknowledgement' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==4
    assert [c['source_order'] for c in cs]==[1,2,3,4]
    for c,(page,n) in zip(cs,labels):assert c['claim_id']==PID+'/T'+n and c['evidence'][0]['page']==page and c['label'].startswith('Theorem '+n+' (')
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    for n,parts in {
'4.2':['Conditions 4.1–4.2 and 4.5',r'\epsilon\in(0,1)',r'(\kappa_L)^{-3}',r'\sup_{S:S\cap G\ne\varnothing}',r'\kappa_L^2(\gamma-\epsilon^{-1}\gamma^*)\bar d_{\operatorname{supp}(\boldsymbol\beta)}'],
'4.3':[r's_+^{-0.5}+s_+^{-1}+(\gamma\kappa_Ls_-)^{-0.5}',r's_+^{-1}+(\gamma\kappa_Ls_-)^{-1}+1',r'S^*\subseteq\operatorname{supp}(\widehat{\boldsymbol\beta}_Q)\subseteq G^c',r'1-7e^{-t}'],
'4.4':[r'$c_1$–$c_4$',r'\log(2|\mathcal E|)',r'\frac{\sqrt{|S^*|}}{n}',r'\min_{j\in S^*}|\beta_j^*|','additional conditions in Theorem 4.3',r'|G^c|+t',r'1-7e^{-t}',r'1-14e^{-t}'],
'4.5':[r'\le\lambda\le c_2\kappa_L\beta_{\min}^2',r's^\star(\log p)(s^*+\log p)/n^2',r'\sqrt{n^{-3}(s^*+\log p)}',r'\ell_0',r'1-p^{-10}']}.items():
        for part in parts:assert part in s[n],(n,part)
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2268-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent CMBX10 heading enumeration, visual comparison of all four complete theorem statements, formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[13,14,15,16,20],main_text_end_clip=dict(page=20,y_max=619)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Four main-text Theorems, 4.2–4.5. No Theorem 4.1 environment; Proposition 4.1 is excluded.','Keep the two different sample-size bounds in T4.3, the sqrt(|S*|)/n term and both probability levels in T4.4, and the complete epsilon(n) and lambda interval in T4.5.','This validates the inventory only; interface source review is separate.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2303.03092',registered_version_alias='2303.03092v3.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original model, objectives, conditions and theorem-local quantities; review dependencies and reproduce all artifacts.'))
    print('All four theorem statements independently source-validated.')
if __name__=='__main__':main()
