"""Independently enumerate PDF theorem environments and check the reviewed transcription."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='e98b076b582e02e1a4b846714fe0d6b28691695b21a5611fdfaf660d3cfd569b'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==67
    first=' '.join(pdf[0].get_text().split())
    for x in ['Convex Regression in Multidimensions: Suboptimality of Least Squares Estimators','Gil Kur','Fuchang Gao','Adityanand Guntuboyina','Bodhisattva Sen','arXiv:2006.02044v2','3 Sep 2024']:assert x in first,x
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert reg['version']=='2006.02044v2.pdf' and reg['source_url']=='https://export.arxiv.org/pdf/2006.02044'
    assert [x for x in pdf.get_toc() if x[1]=='Proofs of Minimax Rates for Convex Regression']==[[1,'Proofs of Minimax Rates for Convex Regression',25]]
    labels=[];hashes={}
    for n in range(1,25):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                spans=l['spans']
                if not spans or spans[0]['font']!='CMBX10':continue
                m=re.match(r'^Theorem (\d+\.\d+)(?:[ .]|$)',spans[0]['text'])
                if m:labels.append([n,m[1]])
    expected=[[10,'3.1'],[11,'3.3'],[11,'3.4'],[12,'3.5'],[12,'3.6'],[13,'4.1'],[17,'4.5'],[20,'4.11']];assert labels==expected,labels
    end=' '.join(pdf[23].get_text().split());assert 'NSF Grant DMS-1712822.' in end and 'Acknowledgments' in end and 'Funding' in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==8
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n+(' (Chatterjee)' if n=='4.1' else '')
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
    '3.1':[r'$B\ge L$',r'c_d\sigma L n^{-2/d}(\log n)^{-4(d+1)/d}',r'$n\ge N_{d,\sigma/L}$','number of facets is bounded by a constant depending on $d$ alone',r'c_d\sigma B n^{-2/d}',r'$n\ge N_{d,\sigma/B}$'],
    '3.3':[r'\mathfrak L>0',r'\mathcal F^{\mathfrak L}(\Omega)',r'\mathfrak L^{\frac{2d}{4+d}}',r'\left(\frac{\sigma^2}{n}(\log n)^F\right)^{\frac4{d+4}}',r'C_4\frac{\sigma\mathfrak L}{\sqrt n}(\log n)^{1+\frac F2}',r'\left(\frac{(\log n)^F}{n}\right)^{\frac2d}',r'$n\ge N_{d,\sigma/\mathfrak L}$'],
    '3.4':[r'$d\ge5$',r'$L>0$',r'$\sigma>0$',r'\mathcal C_L^L(\Omega)',r'c_d\sigma L n^{-\frac2d}(\log n)^{-\frac{4(d+1)}d}',r'$n\ge C_{d,\sigma/L}$'],
    '3.5':[r'every $k\ge1$ and $h\ge1$',r'\mathcal C_{k,h}(\Omega)',r'(\log n)^h',r'(\log n)^{h+2}',r'\left(\frac{k(\log n)^h}{n}\right)^{4/d}','depending on $d$ alone'],
    '3.6':[r'$n\ge N_d$',r'\min\left(\sqrt n\sigma^{-d/4},c_dn\right)',r'\mathbb E_{\tilde f_k}',r'c_d\sigma^2\left[\frac kn\right]^{4/d}(\log n)^{-4(d+1)/d}','function from Lemma 3.2'],
    '4.1':['fixed deterministic design points','a convex class of functions',r'\mathbb E\sup_{g\in\mathcal F:\ell_{\mathbb P_n}(f,g)\le t}',r'-\frac{t^2}2','is unique',r'1-6\exp\left(-\frac{cnt_f^2(\mathcal F)}{\sigma^2}\right)',r'-\frac{C\sigma^2}n',r'+\frac{C\sigma^2}n',r'\inf\{t>0:H_f(t,\mathcal F)\le0\}',r'0\le t_1<t_0',r'H_f(t_1,\mathcal F)\le H_f(t_0,\mathcal F)'],
    '4.5':['contained in the unit ball',r'$1\le p<\infty$',r'\int_\Omega|f(x)-\tilde f(x)|^pdx\le t^p','disjoint interiors',r'$0<\epsilon<\Gamma$',r'N_{[\,]}(\varepsilon',r'C_{d,p}k\left[\log\frac\Gamma\epsilon\right]^{d+1}\left[\frac t\epsilon\right]^{d/2}','bracketing entropy with respect to $L_p$ metric'],
    '4.11':['form (14) and satisfies (3)','depending only on $d$ and $p$',r'every $\epsilon>0$ and $t>0$',r'\ell_{\mathcal S}(f,\Omega,p)\le t',r'[c_{d,p}\log(1/\delta)]^F\left[\frac t\epsilon\right]^{d/2}']}
    for n,parts in checks.items():
        for x in parts:assert x in s[n],(n,x)
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for a,b in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    v=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2791-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent CMBX10 heading enumeration across all24 main-text pages, visual comparison of all8 statements and endpoint, source-specific formula/quantifier checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[10,11,12,13,17,20,24],main_text_end_page=24),validation=dict(returncode=v.returncode,stdout=v.stdout),notes=['Eight main-text Theorems; Section2 Propositions and all Lemmas are outside the theorem inventory.','Theorems4.1,4.5,4.11 are actual theorem environments in main-text proof sketches and are included.','Theorem3.3 uses EUFM fraktur L; preserve its distinction from Lipschitz L in3.4 and the squared empirical versus population losses.','Theorem4.1 ends after equation29, before upright Intuitively prose; all equations26–29 are retained.','Theorem4.5 retains two epsilon glyphs and the bound for every epsilon below Gamma. Theorem4.11 retains the formula without silently adding conventions.','Appendix A starts25 according to outline; no appendix body inspected.','Definitions, ambient prerequisites and full census source review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=reg['source_url'],registered_version_alias=reg['version'],checked_at=now))
    c=ROOT/'checkpoint.json'
    if not c.exists() or json.loads(c.read_text()).get('stage')!='complete':write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=8,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original convex regression classes, design assumptions, losses, affine approximation class, piecewise-affine class, Lemma3.2 source function, entropy definitions and grid metric. Independently source-review full census and reproduce all artifacts.'))
    print('Eight complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
