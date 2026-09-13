"""Check the frozen five-Theorem inventory independently against registered arXiv v3."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='d7abf70b9fa33ae5fbd53398720bfe8d2c0d87dda3c8c46461994a8cb423817e'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==19
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(s in first for s in ['ON POSTERIOR CONSISTENCY OF DATA ASSIMILATION WITH GAUSSIAN PROCESS PRIORS: THE 2D-NAVIER-STOKES EQUATIONS','RICHARD NICKL','EDRISS S. TITI','arXiv:2307.08136v3','9 Jul 2024'])
    assert 'REFERENCES' in pdf[17].get_text(clip=fitz.Rect(0,327.6,612,344))
    headings=[];hashes={}
    for n in range(1,19):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,327.6) if n==18 else page.rect
        s=page.get_text(clip=clip);f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==s;hashes[str(n)]=digest(f)
        if n==18:assert 'gemeinschaft (DFG).' in s and 'REFERENCES' not in s
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']).strip();m=re.fullmatch(r'THEOREM (\d+)\.',text)
                if m:headings.append((n,int(m[1])))
    assert headings==[(6,1),(7,2),(10,3),(10,4),(11,5)]
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==5
    assert inv['papers'][0]['source_url']==URL and inv['papers'][0]['main_text_last_pdf_page']==18
    assert [c['claim_id'] for c in cs]==[PID+f'/T{i}' for i in range(1,6)]
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[6],[7],[10],[10],[11]]
    t1,t2,t3,t4,t5=[c['statement_original'] for c in cs]
    assert r'\|u(0)\|_V+\|v(0)\|_V\leq U<\infty' in t1
    assert all(f'({n})' in t1 for n in [14,15,16]) and 'A)' in t1 and 'B)' in t1
    assert r'\log\frac{c_1}{\|u(t)-v(t)\|_{L^2}}' in t1 and r'^{-1/2}' in t1
    assert r'\frac{\|u(0)-v(0)\|_V}{\|u(0)-v(0)\|_{L^2}}\leq c_P' in t1
    assert r'e^{c_2c_P}' in t1 and t1.count(r'\text{for every }t\in[0,T]')==2
    assert r'C^\infty(\Omega)^2\cap V' in t2 and r'\nu=1/2,f=0' in t2
    assert r'\|u_j(0)\|_{H^2}\lesssim1' in t2 and r'\|u_j(t)\|_{L^2}\simeq e^{-j^2t}j^{-2}' in t2
    assert r"c'=c'(c,t)>0" in t2 and r'\text{all }j\in\mathbb N,t>0' in t2
    assert r'\frac1{\log\left(\frac1{\|u_j(t)-v(t)\|_{L^2}}\right)}' in t2
    assert 'Condition 1' in t3 and all(f'({n})' in t3 for n in [10,19,21,23,24,25])
    assert r'$0\leq T_0<T$ or $T_0=T>0$' in t3 and r'$T_P\geq T$' in t3
    assert r'\eta_N=O(1/\sqrt{\log N})' in t3 and 'constants uniform' in t3
    assert t3.count(r'\sup_{0<t\leq T_p}')==2
    assert t3.count(r'\to^{P_{\theta_0}^N}1')==2
    assert r'\bar\theta_N=E^\Pi[\theta\mid Z^{(N)}]\in V' in t3
    assert r'=O_{P_{\theta_0}^N}(\eta_N)' in t3 and r'\|_{L^2(\Omega)^2}' in t3
    assert r'$0<T_0<T$ or $T_0=T>0$' in t4
    assert r'\liminf_{N\to\infty}\inf_{\widetilde\theta_N}\sup_{\theta\in V:\|\theta\|_{H^2}\leq U}' in t4
    assert r'>\frac{c}{\log N}' in t4 and r'>1/4' in t4 and 'all measurable functions' in t4
    assert r'viscosity $\nu=1/2$, forcing $f=0$' in t4
    assert r'$E_J=\{e_j:j\leq J\}$' in t5 and 'span' in t5
    assert r'$J=J_N=O(\log\log N)$' in t5 and r'$\mathcal H\cap E_{J_0}$' in t5
    assert 'conclusions of Theorem 3 remain true' in t5 and r'N^{-\alpha/(2\alpha+2)}' in t5
    for s in [t1,t2,t3,t4,t5]:
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1825-inventory-',dir='/private/tmp') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=headings,method='Independent exact small-cap heading enumeration across all main-text pages and visual comparison of all five complete theorem statements; source-specific formula checks, structural validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,6,7,10,11,18],page18_clip_y_max=327.6),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=[
        'The five actual Theorem environments are on pages 6, 7, 10 (two) and 11. Proof headings, mixed-case citations, Propositions, Lemmas, Corollaries and Remarks are excluded.',
        'Theorem 1 includes both logarithmic inverse stability and the additional inverse-Poincare branch; the ratio is not squared and the exponential is exp(c2*cP) as printed.',
        'Theorem 2 preserves all three norm comparisons, viscosity 1/2, zero forcing, v(t)=0 and the lower-bound expression with c-prime(c,t). No unspecified constant or zero-denominator case is repaired.',
        'Theorem 3 preserves both posterior concentration events, the Bochner mean, the sum of initial-condition error and uniform trajectory error, uniformity over the RKHS ball, and both observation-window cases including T0=0.',
        'Theorem 3 writes T_P in its prose and T_p in its displayed suprema. The source letter case is retained. L2(Omega)^2 is a vector-valued function-space subscript, not a squared error norm.',
        'Theorem 4 excludes T0=0, unlike Theorem 3. Its liminf-inf-sup order, c/log N threshold, strict probability bound greater than 1/4, and domain of all measurable V-valued estimators are preserved.',
        'Theorem 5 retains the source wording span E_J together with its displayed set of eigenvectors, J_N=O(log log N), fixed J0 and the reference to all Theorem 3 conclusions. No span operator, growth lower bound or altered rate is inserted.',
        'The paper ends after Acknowledgements on page 18 before REFERENCES. Section 3 Proofs is main text, but no proof statements are substituted for the inventoried theorem bodies.',
        'Full definition extraction and theorem dependency review remain pending; inventory completion alone does not complete the paper census.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2307.08136',registered_version_alias='2307.08136v3.pdf',source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=5,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract main-text function spaces, operators, strong PDE solutions, observation model, Gaussian prior and posterior; resolve Theorem 5 inheritance from Theorem 3 and independently review the full graph.'))
    print('Five main-text Theorems independently source-validated; full census pending.')
if __name__=='__main__':main()
