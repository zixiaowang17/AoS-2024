"""Independently enumerate and validate all ten source Theorem statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='9c0edbd16e2e66d92bf0bd695885246e2784b8dad9a0b549c85784782737d5db'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==65
    first=' '.join(pdf[0].get_text().split())
    for v in ['TENSOR-ON-TENSOR REGRESSION: RIEMANNIAN OPTIMIZATION','THEIR INTERPLAY','YUETIAN LUO','ANRU R. ZHANG','Submitted to the Annals of Statistics','arXiv:2206.08756v3','15 Jan 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2206.08756v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2206.08756'
    boundary=pdf[25].search_for('REFERENCES');assert len(boundary)==1 and 328<boundary[0].y0<329
    assert [x for x in pdf.get_toc() if x[1]=='T-HOSVD and ST-HOSVD']==[[1,'T-HOSVD and ST-HOSVD',32]]
    labels=[];hashes={}
    for n in range(1,27):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,322) if n==26 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(span['text'] for span in line['spans'] if 'Medi' in span['font']).strip()
                match=re.match(r'^Theorem\s+(\d+)\s*\(',text)
                if match:labels.append([n,match[1]])
    expected=[[10,'1'],[11,'2'],[12,'3'],[12,'4'],[13,'5'],[14,'6'],[15,'7'],[17,'8'],[18,'9'],[20,'10']];assert labels==expected,labels
    end=(ROOT/'evidence/page-26.txt').read_text();assert 'Acknowledgements.' in end and 'REFERENCES' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==10
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page] and c['label'].startswith('Theorem '+n+' (')
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'1':[r'\mathbf r\ge\mathbf r^*',r'\frac{R_{2\mathbf r}}{(d+m)(1+R_{2\mathbf r+\mathbf r^*}-R_{2\mathbf r})}',r'\sigma_{r_k^*}(\mathcal M_k(\mathcal X^*))',r'\frac1{8(\sqrt{d+m}+1)+1}',r'R_{2\mathbf r}(1-R_{2\mathbf r})',r'2^{-t}',r'\frac{2(\sqrt{d+m}+1)}{1-R_{2\mathbf r}}','best Tucker rank',r'\forall t\ge0'],
'2':[r'\frac{1-R_{2\mathbf r}}{4(d+m)(\sqrt{d+m}+1)(1+R_{2\mathbf r+\mathbf r^*}-R_{2\mathbf r})}',r'2^{-2^t}',r'\frac{2(\sqrt{d+m}+1)}{1-R_{2\mathbf r}}','converges quadratically',r'\forall t\ge0'],
'3':['any estimator',r'\operatorname{Tucrank}(\widehat{\mathcal X})\le\mathbf r',r'\|\mathcal Y-\mathscr A(\widehat{\mathcal X})\|_{\mathrm F}^2\le\|\mathcal Y-\mathscr A(\mathcal X^*)\|_{\mathrm F}^2',r'\frac2{1-R_{2\mathbf r}}'],
'4':['Definition 2',r'df=\sum_{i=1}^{d+m}r_i(p_i-r_i)+\prod_{i=1}^{d+m}r_i',r'\sum_{i=1}^d(p_i-r_i)r_i+\prod_{i=1}^d r_i',r'\log(d)',r'1-\exp(-c_1(d,m)\underline p)',r'\underline p:=\min_j p_j',r'\mathbb E\|\widehat{\mathcal X}-\mathcal X\|_{\mathrm F}',r'C_2(d,m)',r"\min_k r_k\ge C'",r'\inf_{\widehat{\mathcal X}}\sup_{\mathcal X\in\mathcal F_{\mathbf p,\mathbf r}}'],
'5':[r'df=\sum_{i=1}^d(p_i-r_i)r_i+\prod_{i=1}^d r_i',r'\frac{\|\mathcal X^*\|_{\mathrm F}^2+\sigma^2}{\lambda^2}',r'(\prod_{i=1}^d p_i)^{1/2}+df',r'1-\underline p^{-C}','Algorithm 2','initialization conditions in Theorems 1 and 2',r'c_1(d)\sigma',r'c_2(d)\sigma',r'\log\log',r'\vee0'],
'6':[r'df=\sum_{i=1}^{m+1}(p_i-r_i)r_i+\prod_{i=1}^{m+1}r_i',r'(\prod_{i=1}^{m+1}p_i)^{1/2}+df',r'\sigma^2/\lambda^2+p_1',r'1-\exp(-c\underline p)','Algorithm 3',r'c_3(m)\sigma\sqrt{df/n}'],
'7':[r'df=(p_1+p_2-r)r',r'\frac{C(\sigma^2+\|\mathbf X^*\|_{\mathrm F}^2)}{\sigma_{r^*}^2(\mathbf X^*)}df',r'\mathbf X^0=\mathcal P_r(\mathscr A^*(\mathbf y))','Corollary 1',r'\frac{\sigma_{r^*}(\mathbf X^*)}{c_1\sigma}\sqrt{n/df}',r'\frac{\sigma_{r^*}(\mathbf X^*)}{c_2\sigma}\sqrt{n/df}'],
'8':['design (13)',r'df=\sum_{i=1}^{d+m}p_i',r"\lambda>C'\sigma",r'\frac{\lambda^2+\sigma^2}{\lambda^2}',r'(\prod_{i=1}^d p_i)^{1/2}+\overline p',r'\frac{\sigma^4}{\lambda^4}',r'\prod_{i=d+1}^{d+m}p_i+\overline p',r'\overline p=\max_{k=1,\ldots,d+m}p_i',r'1-\underline p^{-C}','Algorithm 4',r'c_3(d,m)\sigma\sqrt{df/n}'],
'9':['hypothesis test (14)',r'0<\delta<1',r'\frac{(p/dD)^{d/2}\delta}{2(1-\sigma^2)}',r'\deg(f)\le D',r'\mathbb E_{H_0}f(\{y_i,\mathcal A_i\}_{i=1}^n)=0',r'\operatorname{Var}_{H_0}f(\{y_i,\mathcal A_i\}_{i=1}^n)=1',r'\mathbb E_{H_1}f',r'\frac\delta{1-\delta}'],
'10':[r'\mathcal B\in\mathbb R^{r_1^*\times\cdots\times r_d^*}',r'\mathbf U_k\in\mathbb O_{p_k,r_k^*}',r'\mathcal Z=\widetilde{\mathcal T}-\mathcal T',r'\widetilde{\mathbf U}_k^0\in\mathbb O_{p_k,r_k}',r'\widetilde{\mathbf U}_{k\perp}^{0\top}\mathbf U_k',r'\frac{\sqrt2}2','Algorithm 5',r'(2^{(d+1)/2}\cdot d+1)',r'\|\mathcal Z_{\max(\mathbf r)}\|_{\mathrm F}']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert s['2'].count(r'2^{-2^t}')==2 and 'In addition' not in s['2']
    for n in ['4','5','6','7','8']:assert s[n].count('•')==2
    assert 'Gaussian' not in s['10'] and 'TRIP' not in s['9']+s['10']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2583-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    pages=[1,10,11,12,13,14,15,17,18,20,26]
    crops=[dict(path='evidence/page-18-theorem-crop.jpg',page=18,location='Low-degree sample-size bound and normalized polynomial supremum'),dict(path='evidence/page-20-theorem-crop.jpg',page=20,location='Estimated-subspace complement, initialization inequality and perturbation factor')]
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font heading enumeration, visual comparison of all ten full statements, source-specific formula and branch checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=pages,visually_reviewed_crops=crops,main_text_end_page=26,last_page_clip_y=322),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['All ten main-text Theorems1–10 retained. Theorems4–8 preserve both bullets. Corollary1 and all propositions/lemmas are excluded from the inventory, but source references needed to interpret theorem statements must be retained in extraction.','Theorem2 prints2^(-2^t) at all t≥0, including the noiseless case; preserve the apparent t=0 problem instead of repairing the exponent. Theorem4 prints an unstarred target in the upper-bound expectation, and Theorem8 defines bar-p with mismatched k/i indices.','Theorem9 is a normalized low-degree-polynomial expectation bound for hypothesis test14, not an unconditional lower bound for all polynomial-time algorithms. Theorem10 is a deterministic tensor decomposition result with the complement of the estimated subspace; it does not assume regression noise or Gaussian design.','Inventory only. Tensor operations, regression variants, TRIP, algorithms/initializations, Gaussian design and testing distributions remain to be extracted and source-reviewed.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=10,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original tensor geometry/operations, regression operator and adjoint, TRIP/Gaussian design, Algorithms1–5 and their initialization references, special regression models, hypothesis test14 and deterministic OHOOI perturbation objects. Separate object, assumption, guarantee and proof references; preserve source issues and exclude supplement bodies. Complete census, reproduction and full source review.'))
    print('All ten complete main-text Theorem statements independently source-validated.')
if __name__=='__main__':main()
