"""Independently enumerate the three bold Theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='a26bc459b9f4cfe4b8df1403fb828fbc0ae85d793c88074e419b02fd99e6a056'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==39
    first=' '.join(pdf[0].get_text().split())
    for v in ['ESTIMATION OF THE SPECTRAL MEASURE FROM CONVEX','REGULARLY VARYING RANDOM VECTORS','Marco Oesting','Olivier Wintenberger','July 4, 2024','arXiv:2010.03832v2','3 Jul 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2010.03832v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2010.03832'
    lastpage=pdf[24];assert 'References' in lastpage.get_text(clip=fitz.Rect(0,522,lastpage.rect.width,547))
    assert [x for x in pdf.get_toc() if x[1]=='Proof of Theorem 5']==[[1,'Proof of Theorem 5',26]]
    labels=[];hashes={}
    for n in range(1,26):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,520) if n==25 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(span['text'] for span in line['spans'] if 'Medi' in span['font']).strip()
                match=re.match(r'^Theorem\s+(\d+)\.$',text)
                if match:labels.append([n,match[1]])
    expected=[[7,'5'],[10,'8'],[11,'10']];assert labels==expected,labels
    last=(ROOT/'evidence/page-25.txt').read_text();assert 'Acknowledgements' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==3
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label']=='Theorem '+n and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==([7,8] if n=='5' else [page])
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    for v in [r'index $\alpha=1$',r'n/a^*(u_n)\to\infty','every finite set',r'K_0\subset\mathbb N_0',r'\delta\ge0',r'\sqrt{\frac n{a^*(u_n)}}',r'a^*(u_n)\widehat M_{n,u_n}(v,s,\beta,p)-a^*(u_n)\mathbb E[\widehat M_{n,u_n}(v,s,\beta,p)]',r'\ell^\infty(\partial B_1^+(0)\times A\prime_\delta\times K_0)','tight centered Gaussian process',r'(Ys\circ\Theta)^{1/\beta}',r'(Yt\circ\Theta)^{1/\gamma}',r'Y(\|s\circ\Theta\|\wedge\|t\circ\Theta\|)>1']:
        v=v.replace(r'A\prime_\delta',r"A'_\delta");assert v in s['5'],v
    for v in [r'X^*=(r_1^{-1}X_1^\alpha,\ldots,r_d^{-1}X_d^\alpha)','Eq. (3) and (30)',r'k_n\to\infty',r'k_n/n\to0',r'\sqrt{k_n}A_i^*(n/k_n)\to0',r'\widehat\alpha_{n,k_n}^{-1}-\alpha^{-1}',r'\frac\tau{\alpha_i\alpha_j}\mathbb E[\Theta_i\wedge\Theta_j]=\frac{2-\tau_{ij}}{\alpha_i\alpha_j}']:assert v in s['8'],v
    for v in ['assumptions of Cor. 6 and Thm. 8',r'a^*(u_n)\sim n/k_n',r'\delta>0',r'c_{s_i}(v,s,\beta,p)=\frac\partial{\partial s_i}',r'c_{\beta_i}(v,s,\beta,p)=\frac\partial{\partial\beta_i}',r"continuous on $\partial B_1^+(0)\times A'_\delta$",r'\sqrt{k}',r'\widetilde M_{n,k,I}(v_I,p)',r'\widetilde P_{n,k,I}',r'G^0(\mathbf1_{\{i\}})',r'\alpha_i\widetilde H_i',r'\ell^\infty(\partial B_1^+(0)\times K)']:assert v in s['10'],v
    assert '(24)' in s['5'] and '(25)' in s['5']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2529-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font heading enumeration, visual comparison of all three complete statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,7,8,10,11,25],main_text_end_page=25,last_page_clip_y=520),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Three main-text Theorem environments5,8,10; Theorem5 spans pages7–8. Corollary6 is not an inventoried Theorem but its assumptions are explicitly referenced by Theorem10 and must be preserved in extraction.','Theorem5 is centered by its exact preasymptotic expectation and includes the full two-argument covariance with a shared Pareto radial variable.','Theorem8 prints unindexed alpha in the X-star transform; preserve that notation until the surrounding marginal-index definitions are separately reviewed.','Theorem10 uses k in its displayed process, inherits the Corollary6/Thm8 assumptions and requires continuity of all stated partial derivatives.','Inventory validation only; regular variation, spectral laws, perturbation domains, estimator definitions, second-order and bias assumptions, and joint limit dependencies remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=3,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract regular variation and standardization, spectral/Pareto limits, perturbation domains and generalized moment processes, random-threshold estimators, Hill estimates, second-order condition(30), Corollary6 bias assumptions and the joint Gaussian limits used by Theorem10. Preserve source ambiguities and exclude appendix bodies. Complete the full census, reproduction and source review.'))
    print('All three theorem statements independently source-validated.')
if __name__=='__main__':main()
