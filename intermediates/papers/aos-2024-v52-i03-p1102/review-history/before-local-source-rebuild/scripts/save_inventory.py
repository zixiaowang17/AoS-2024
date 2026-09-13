"""Save every main-text Theorem of MARS via LASSO, preserving the printed bodies."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,page,text):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location='Theorem '+n)]))
claim('3.1',9,r'''
Suppose $f^*\in\mathcal F_{\infty-\mathrm{mars}}^{d,s}$ and $V_{\mathrm{mars}}(f^*)\le V$ and assume the lattice design (15). The estimator $\widehat f_{n,V}^{d,s}$ then satisfies that
\[
\mathcal R_F\bigl(\widehat f_{n,V}^{d,s},f^*\bigr)\le C_{\rho,d}\left(\frac{\sigma^2V^{\frac12}}n\right)^{\frac45}\left[\log\left(2+\frac{Vn^{\frac12}}\sigma\right)\right]^{\frac{3(2s-1)}5}+C_{\rho,d}\frac{\sigma^2}n[\log n]^2\tag{18}
\]
for some positive constant $C_{\rho,d}$ depending on $\rho$ and $d$.
''')
claim('3.2',10,r'''
There exist positive constants $C_m$ and $\epsilon_m$ depending on $m$ such that
\[
\log N(\epsilon,\mathcal D_m,\|\cdot\|_2)\le C_m\epsilon^{-\frac12}\left[\log\frac1\epsilon\right]^{\frac{3(2m-1)}4}
\]
for every $0<\epsilon<\epsilon_m$. The logarithmic multiplicative factor can be omitted when $m=1$.
''')
claim('3.4',11,r'''
Suppose $f^*\in\mathcal F_{\infty-\mathrm{mars}}^{d,s}$ and $V_{\mathrm{mars}}(f^*)\le V$ and assume the lattice design (15). The estimator $\widetilde f_{n,V}^{d,s}$ then satisfies that
\[
\mathcal R_F\bigl(\widetilde f_{n,V}^{d,s},f^*\bigr)\le\frac{8V^2}{N^2}+C_{\rho,d}\left(\frac{\sigma^2V^{\frac12}}n\right)^{\frac45}\left[\log\left(2+\frac{Vn^{\frac12}}\sigma\right)\right]^{\frac{3(2s-1)}5}+C_{\rho,d}\frac{\sigma^2}n[\log n]^2
\]
for some positive constant $C_{\rho,d}$ depending on $\rho$ and $d$, where $N=\min_k N_k$.
''')
claim('3.5',12,r'''
If $f^*\in\mathcal F_{\infty-\mathrm{mars}}^{d,s}$ and $V_{\mathrm{mars}}(f^*)\le V$, then we have
\[
\|\widehat f_{n,V}^{d,s}-f^*\|_{p_0,2}^2=O_p\bigl(n^{-\frac45}(\log n)^{\frac{8(s-1)}5}\bigr).\tag{23}
\]
''')
claim('3.6',12,r'''
There exists a positive constant $C_m$ depending on $m$ such that
\[
\log N_{[\,]}(\epsilon,\mathcal D_m,\|\cdot\|_2)\le C_m\left(\frac4\epsilon\right)^{\frac12}\left|\log\frac4\epsilon\right|^{2(m-1)}
\]
for every $\epsilon>0$, where $N_{[\,]}(\epsilon,\mathcal D_m,\|\cdot\|_2)$ is the $\epsilon$-bracketing number of $\mathcal D_m$ under the $L^2$ norm.
''')
claim('3.8',12,r'''
Suppose $f^*\in\mathcal F_{\infty-\mathrm{mars}}^{d,s}$ and $V_{\mathrm{mars}}(f^*)\le V$. Also, assume that $N=\min_k N_k=\Omega(n^{4/15})$, i.e., there exists a positive constant $c_{B,d,V}$ possibly depending on $B$, $d$, and $V$ such that
\[
N\ge c_{B,d,V}\cdot n^{\frac4{15}}.
\]
Then, the estimator $\widetilde f_{n,V}^{d,s}$ satisfies that
\[
\|\widetilde f_{n,V}^{d,s}-f^*\|_{p_0,2}^2=O_p\bigl(n^{-\frac45}(\log n)^{\frac{8(s-1)}5}\bigr).
\]
''')
claim('3.9',13,r'''
There exist positive constants $C_{b,B,s}$ depending on $b$, $B$, and $s$ and $c_{B,s}$ depending on $B$ and $s$ such that
\[
\mathfrak M_{n,V}^{d,s}\ge C_{b,B,s}\left(\frac{\sigma^2V^{\frac12}}n\right)^{\frac45}\left[\log\left(\frac{Vn^{\frac12}}\sigma\right)\right]^{\frac{4(s-1)}5}
\]
provided $n\ge c_{B,s}\cdot(\sigma^2/V^2)$.
''')

if __name__=='__main__':
    pdf=fitz.open(prov['cached_pdf']);assert len(pdf)==108
    assert hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==prov['pdf_sha256']
    first=' '.join(pdf[0].get_text().split());assert '2111.11694v5' in first and '13 Oct 2024' in first
    assert 'MARS VIA LASSO' in first
    for name in prov['authors']:assert name.upper() in first
    labels=[];mentions=[]
    for i in range(25):
        p=pdf[i];assert (ROOT/'evidence'/f'page-{i+1:02}.txt').read_bytes().decode('utf8')==p.get_text()
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                t=''.join(s['text'] for s in l['spans']).strip();m=re.match(r'^(THEOREM|Theorem)\s+(\d+\.\d+)',t)
                if m:(labels if m[1]=='THEOREM' else mentions).append((i+1,m[2]))
    assert labels==[(9,'3.1'),(10,'3.2'),(11,'3.4'),(12,'3.5'),(12,'3.6'),(12,'3.8'),(13,'3.9')]
    assert mentions==[(10,'3.2'),(11,'3.1'),(11,'3.4'),(12,'3.6')]
    assert 'YEH' in pdf[24].get_text() and 'APPENDIX A:' in pdf[25].get_text(clip=fitz.Rect(0,165,pdf[25].rect.width,181))
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
            depth=0
            for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if b=='{' else -1
                assert depth>=0,c['claim_id']
            assert depth==0,c['claim_id']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=25,main_text_boundary=dict(location='References end on page 25. Page 26 begins an appendix roadmap followed by Appendix A, Hardy–Krause variation, at y=167.126708984375. Page 26 and all subsequent appendix material are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    out=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    for n in [9,10,11,12,13]:shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    notes=[
      'Seven actual uppercase Theorem environments occur in pages 1–25. Four ordinary-case mentions are excluded. Every Theorem body fits on its listed page, although some assumptions and definitions are in preceding main-text prose.',
      'Theorems 3.1 and 3.4 preserve the exact n^{-4/5} bounds, logarithmic factors, additive remainder and the approximate-estimator error 8V^2/N^2.',
      'Theorem 3.2 preserves the small-epsilon range and the separate removal of the logarithmic factor when m=1. Theorem 3.6 preserves all epsilon>0, the absolute logarithm and its exponent 2(m-1). Both entropy results are included.',
      'Theorem 3.5 states a rate in probability for squared population L2 error, not an expectation bound. Theorem 3.8 preserves the minimum-grid-resolution requirement Omega(n^{4/15}) and the dependencies of its constant.',
      'Theorem 3.9 uses fraktur M for the minimax risk; the fixed-design risk uses script R and the function classes use script F,D. These fonts were checked independently in the PDF.',
      'The minimax definition is on page 12 and its additional model assumptions continue on page 13. The latter says p0 is bounded below but prints a sup-norm lower inequality; preserve and flag that mismatch when extracting the source conditions.',
      'The fixed-design sub-Gaussian model and random-design L^{5,1} error assumptions must be resolved separately in the census. Entropy theorems do not inherit sampling conditions merely because they appear inside the risk-analysis sections.',
      'The main text ends with references on page 25. Appendix roadmap and heading on page 26 were inspected only to establish the endpoint; all appendix mathematics and proofs are excluded.',
      'Only the independent theorem inventory is complete. Main-text function class, variation, optimization and approximation definitions plus all seven statement dependency sets still require extraction and source review.'
    ]
    (ROOT/'inventory-review.json').write_text(json.dumps(dict(paper_id=PID,status='complete',source_checked=True,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Independent uppercase-heading scan over pages 1–25, followed by full visual transcription review of all seven theorem bodies on pages 9–13.',theorem_ids=[c['claim_id'] for c in claims],notes=notes),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),next_action='Extract the main-text MARS basis, signed-measure function class and complexity, exact and approximate constrained least-squares estimators, lattice/sub-Gaussian model, fixed-design risk, D_m and covering/bracketing conventions, random-design density/noise conditions and norm, and Gaussian minimax risk. Do not import appendix proofs or Hardy–Krause variation merely from alternative smoothness characterizations.'),indent=2)+'\n')
    print('Saved and independently validated all seven original Theorems.')
