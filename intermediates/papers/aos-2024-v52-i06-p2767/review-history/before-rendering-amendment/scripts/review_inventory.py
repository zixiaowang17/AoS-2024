"""Independently enumerate bold theorem environments and validate original statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='9b1b2f013556806f68bf9df63b1354bb9edec574989fdddcb75d3d30fb9b1c25'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==62
    first=' '.join(pdf[0].get_text().split())
    for x in ['On the Statistical Complexity of Sample Amplification','Brian Axelrod','Shivam Garg','Yanjun Han','Vatsal Sharan','Gregory Valiant','arXiv:2201.04315v2','18 Sep 2024','September 19, 2024']:assert x in first,x
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2201.04315v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2201.04315'
    assert [x for x in pdf.get_toc() if x[1]=='A Concrete examples of sample amplification']==[[1,'A Concrete examples of sample amplification',23]]
    labels=[];hashes={}
    for n in range(1,23):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                if not line['spans'] or line['spans'][0]['font']!='CMBX10':continue
                m=re.match(r'^Theorem (\d+\.\d+)\.',line['spans'][0]['text'])
                if m:labels.append([n,m[1]])
    expected=[[13,'4.5'],[14,'4.6'],[15,'5.2'],[15,'5.5'],[18,'6.2'],[18,'6.3'],[19,'6.4'],[20,'6.5'],[21,'7.1'],[22,'7.2'],[22,'7.3']];assert labels==expected,labels
    end=' '.join((ROOT/'evidence/page-22.txt').read_text().split());assert 'a Simons Foundation Investigator Award.' in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==11
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==([18,19] if n=='6.3' else [page])
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'4.5':['Assumptions 1 and 2',r'$k=3$',r'\theta\in\Theta',r'\frac C{\sqrt n}+\frac{m\sqrt d}n','depending only on $d$ and the moment upper bound','sufficiently large'],
'4.6':['each one-dimensional component','Assumptions 1 and 2',r'$k=10$',r'C\left(\frac d{n^2}+\frac{m\sqrt d}n\right)',r'independent of $(n,d)$',r'n=\Omega(\sqrt d/\varepsilon)',r'm=\Omega(n\varepsilon/\sqrt d)'],
'5.2':[r'$n,m\ge0$',r'\sqrt{\frac{m^2}n\cdot r_{\chi^2}(\mathcal P,n/2)}'],
'5.5':[r'\mathcal P=\prod_{j=1}^d\mathcal P_j',r'$n,m\ge0$',r'\sqrt{\frac{m^2}n\sum_{j=1}^dr_{\chi^2}(\mathcal P_j,n/2)}'],
'6.2':[r'\Sigma\in\mathbb R^{d\times d}',r'\mathcal N\left(0,\frac{I_d}n\right)',r'\mathcal N\left(0,\frac{I_d}{n+m}\right)','Example 4.1 is exactly minimax optimal'],
'6.3':['Assumptions 1 and 3',r'every $n,m\in\mathbb N$',r'\frac{m\sqrt d}n\wedge1',r'\left(\frac{\log n}n\right)^{1/3}',r'independent of $(n,m,d,\mathcal P)$','depends only on the exponential family (and thus on $d$)'],
'6.4':[r'\varepsilon\in(0,1)','for each $j',r'\alpha_j-\frac\varepsilon{\sqrt d}',r'\alpha_j+\frac\varepsilon{\sqrt d}',r'\alpha_j\in(\underline\alpha,\overline\alpha)',r'c=c(\underline\alpha,\overline\alpha)>0'],
'6.5':['Assumption 4',r'any $c>0$',r"$c'>0$ depending only on $c$",r'\left\lceil\frac{c\varepsilon n}{\sqrt d}\right\rceil',r"\ge c'\varepsilon"],
'7.1':[r't\in[1/(2\sqrt d),1/2]',r'$(n,n+1,0.1)$','if and only if',r'n=\Omega\left(\frac1t\right)'],
'7.2':['low-rank covariance estimation model',r'$p\ge d+1$',r'$(n,n+1,0.1)$',r'if and only if $n\ge d$'],
'7.3':[r'$L\ge8$',r'$c\in(0,1)$',r'm^\star(\mathcal P_c,n)\asymp n^{5/6}',r'm^\star(\mathcal P,n)\lesssim n^{3/4}']}
    for n,parts in checks.items():
        for x in parts:assert x in s[n],(n,x)
    assert 'Assumption 2' not in s['6.3'] and r'\Sigma\succ0' not in s['6.2']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2767-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold CMBX10 theorem-heading enumeration, visual comparison of all eleven statements, source-specific formula and quantifier checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[13,14,15,18,19,20,21,22],main_text_end_page=22),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Eleven complete main-text theorem environments; prose mentions, table citations, lemmas, corollaries and appendix theorems excluded.','Theorem6.3 includes the continuation on19 specifying universal c versus model-dependent C.','Retain k=3 versus componentwise k=10 and the two different upper-bound remainders.','Theorems5.2/5.5 retain n,m>=0 and n/2 although endpoint/rounding conventions are unstated.','Theorem6.2 does not explicitly require positive definite Sigma; original formula in dimension d is preserved.','Theorem6.4 retains distinct lower and upper alpha endpoints and both TV conditions. Theorem6.5 retains ceiling and constant dependence.','Main text ends22; Appendix A starts23 and is not read.','Original definitions, assumptions, local dependencies and full census review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=11,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract sample-amplification definitions, normalized divergences, sufficient-statistic procedure, exponential/product families, Assumptions1–4, chi-squared estimation error, and Section7 model definitions. Finalize, reproduce and independently source-review.'))
    print('Eleven complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
