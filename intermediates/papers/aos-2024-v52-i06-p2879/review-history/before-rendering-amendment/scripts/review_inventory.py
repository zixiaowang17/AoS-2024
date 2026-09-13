"""Independently enumerate and check all six original PDF Theorems before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='d802b3e53155d7ac49f8547fbdf571819d4a614fb213373ed6b7e5b184df8796'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==86
    first=' '.join(pdf[0].get_text().split())
    for x in ['Dimension free ridge regression','Chen Cheng','Andrea Montanari','arXiv:2210.08571v3','19 Jun 2025','June 23, 2025']:assert x in first,x
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert reg['version']=='2210.08571v3.pdf' and reg['source_url']=='https://export.arxiv.org/pdf/2210.08571'
    labels=[];hashes={}
    for n in range(1,35):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            if n==34 and b['bbox'][1]>=615:continue
            for l in b.get('lines',[]):
                ss=l['spans']
                if not ss or ss[0]['font']!='SFBX1095':continue
                m=re.match(r'^Theorem (\d+)(?:[ .]|$)',ss[0]['text'])
                if m:labels.append([n,m[1]])
    expected=[[10,'1'],[11,'2'],[12,'3'],[13,'4'],[17,'5'],[25,'6']];assert labels==expected,labels
    end=' '.join(pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,615)).split());assert 'Acknowledgements' in end and 'activity while on leave.' in end and 'References' not in end
    ref=next(b for b in pdf[33].get_text('blocks') if b[4].strip()=='References');assert 621<ref[1]<623
    # Inspect only the Appendix A heading, not its body.
    heading=' '.join(pdf[37].get_text(clip=fitz.Rect(0,0,pdf[37].rect.width,90)).split());assert heading=='A Proof of Proposition 2.2',heading
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==6
    expected_labels=['Theorem 1 (Ridge regression)','Theorem 2','Theorem 3 (Ridgeless regression in the overparameterized regime)','Theorem 4 (Ridgeless regression in the underparameterized regime)','Theorem 5','Theorem 6']
    for i,(c,(page,n),label) in enumerate(zip(cs,expected,expected_labels),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']==label
        assert [e['page'] for e in c['evidence']]==({'3':[12,13],'4':[13,14]}.get(n,[page]))
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
    '1':['Assumption 1','positive integers $k$ and $D$',r'\kappa^{4.5}',r'n^{-2D+1}',r'\max\{1,\lambda\}',r'n^{1-\frac1k}\kappa^{9.5}',r'\lambda kn^{-\frac1k}\le\kappa/2',r'\lambda_\star(\lambda)^{k+1}',r'\sqrt{\rho(\lambda)}n^{1-\frac1k}\kappa^{8.5}',r'\tag{28}',r'\tag{29}'],
    '2':['non-negligible regularization',r'\nu=\lambda/\lambda_\star(\lambda)\in[1/C,1-1/C]',r'\tilde d_\Sigma(n):=d_\Sigma(n)(\log d_\Sigma(n))^2',r'n^{4/3}(\log n)^{-2/3-\epsilon}',r'n^{7/6}(\log n)^{-2/3-\epsilon}',r'1-O(n^{-10})',r'n^{0.99}',r'n^{0.49}',r'\|\boldsymbol\beta\|_{\boldsymbol\Sigma^{-1}}^2\le C'],
    '3':['$n<d$','minimum nonzero eigenvalue',r'\sigma_n>0',r'\kappa\le C_\Sigma^2/8',r'\max\{1,\kappa\lambda_\star(0)\}',r'on the event $\{s_{\min}\ge8\lambda_\star(0)\kappa\}$',r'\lambda_\star(0)kn^{-\frac1k}\le1/4',r'\boldsymbol\theta_{\le n}',r'\boldsymbol\beta_{>n}',r'\min\left\{O\left(',r'\min\{|d/n-1|,d/n\}\ge\varepsilon',r's_{\min}\ge\max\{C_4\sigma_d,\sigma_{C_5n}\}',r'\tag{32}'],
    '4':['$n>d$',r'\nu=\min\left(\frac dn,1-\frac dn\right)',r'n^{-(\frac14-\epsilon)(1-\frac1k)}\log^8n\le C\nu^{15.5}',r'\mathscr B_X(0)=B_n(0)=0','deterministically on the event',r'\operatorname{rank}(\boldsymbol X)=d'],
    '5':[r'fixed constant $\nu>0$','positive integer $D$',r'1-O(n^{-D})',r'$o_n(1)$ errors may depend on $D$',r'\alpha>1',r'\sum_{j=1}^i b_j/j',r'\frac{\pi/\alpha}{\sin(\pi/\alpha)}c_\star^{-1/\alpha}',r'\lambda_\star(\nu n^{-\alpha})=c_\star\sigma_n',r'\lfloor nx\rfloor',r'\lfloor(n/\log n)x\rfloor','“polynomial-decay”','“rapid-decay”',r'\alpha=1',r"\alpha'>1"],
    '6':[r'\mathsf R_0(\boldsymbol Q):=\mathscr R_0',r'$\zeta>0$',r'$\mu\ge0$',r'\|\boldsymbol Q\|=1',r'\frac2{\mu_\star(\zeta,\mu)},\frac1\zeta',r'\sqrt{\gamma^3\mathsf R_0(\boldsymbol Q)}',r'\sqrt{n\log n}',r'1+\mathsf R_0(\boldsymbol I)^2',r'1+\mathsf R_0(\boldsymbol I)^3',r'\beta_2:=\frac{C_\beta n\beta_1}',r'\alpha_1\le\mathsf R_0(\boldsymbol I)/8',r'\beta_1\le\mathsf R_0(\boldsymbol Q)/64',r'\gamma\beta_2(1+\mathsf R_0(\boldsymbol I))\le1/64',r'n^{-D}=O(\alpha_1/(1+\mathsf R_0(\boldsymbol I)))']}
    for n,vs in checks.items():
        for v in vs:assert v in s[n],(n,v)
    for n in range(34,40):assert r'\tag{'+str(n)+'}' in s['5']
    assert r'\nu\sigma_n' not in s['5'] # Do not silently correct the printed regularization arguments.
    assert s['3'].count('Variance approximation.')==1 and s['3'].count('Bias approximation.')==1
    assert 'Corollary 6.5' not in s['6']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for a,b in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    v=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2879-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold SFBX1095 heading enumeration across the complete main text; visual comparison of all six statements and two continuations; endpoint crop, source-specific formula checks, structural validation and exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[10,11,12,13,14,17,25],visually_reviewed_crops=[dict(path='evidence/page-34-main-text.png',page=34,y_end=615)],main_text_end_page=34),validation=dict(returncode=v.returncode,stdout=v.stdout),notes=['Six actual Theorems, including Theorem6 in the main-text proof section. Lemmas, Propositions, Corollaries, Remarks and appendix bodies are excluded.','Theorem3 spans12–13 and retains its minimum of two additive bias-error bounds, event-qualified guarantee and final eigenvalue bound. Theorem4 continues onto14 with a rank-qualified zero-bias statement.','Theorem5 retains both regular-variation branches, different F_beta measures, coefficient-decay requirements and all six displays34–39. Printed regularization arguments may require a separate scaling note; they are not silently replaced.','Theorem6 retains the sans-serif shorthand R0 distinct from script resolvent R0 and all four error parameters, their denominators and smallness conditions.','Registered PDF is the2025 arXivv3 revision for this2024 article; source identity is pinned and not interchangeable with a published PDF.','Full definitions, conditions, dependency extraction and registered-source census review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=reg['source_url'],registered_version_alias=reg['version'],checked_at=now))
    p=ROOT/'checkpoint.json'
    if not p.exists() or json.loads(p.read_text()).get('stage')!='complete':write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=6,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original ridge model, Assumption1, covariance/effective-rank and deterministic-equivalent definitions, all theorem-local regularization/event/spectrum conditions and the resolvents required by Theorem6. Then finalize, reproduce and independently source-review the full census.'))
    print('Six complete original main-text Theorems independently source-validated.')
if __name__=='__main__':main()
