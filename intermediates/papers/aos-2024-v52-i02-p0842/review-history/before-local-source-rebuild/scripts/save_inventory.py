"""Preserve all five main-text Theorems, including explicitly restated earlier results."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,pages,text,title=None):claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' ('+title+')' if title else ''),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n) for p in pages]))
claim('3.3',[14],r'''
Let Assumptions (A1) and (A2) hold, and let $\widetilde{\mathbf X}_{t_k}$ be a numerical approximation of the solution $\mathbf X_{t_k}$ of (1) at time $t_k$. If:

(1) The one-step approximation $\widetilde{\mathbf X}_{t_k}=\widetilde\Phi_h(\widetilde{\mathbf X}_{t_{k-1}})$ is $L^p$ consistent of order $q_2-1/2$; and

(2) $\widetilde{\mathbf X}$ has bounded moments,

then $\widetilde{\mathbf X}$ is $L^p$ convergent, $p\geq1$, of order $q_2-1/2$, that is, for $k=1,\ldots,N$, it holds:
\[
\left(\mathbb E[\|\mathbf X_{t_k}-\widetilde{\mathbf X}_{t_k}\|^{2p}]\right)^{\frac1{2p}}=R(h^{q_2-1/2},\mathbf x_0).
\]
''','Lp convergence of a numerical scheme')
claim('3.5',[14],r'''
Assume (A1)–(A2), let $\mathbf X^{[\mathrm{LT}]}$ be the LT approximation defined in (10) and let $\mathbf X$ be the solution of (1). Then there exists $C\geq1$ such that for all $p\geq2$, and $k=1,\ldots,N$, it holds:
\[
\left(\mathbb E[\|\mathbf X_{t_k}-\mathbf X^{[\mathrm{LT}]}_{t_k}\|^p]\right)^{\frac1p}=R(h,\mathbf x_0).
\]
''','Lp convergence of the LT splitting')
claim('3.7',[15],r'''
Assume (A1), (A2) and (A6), let $\mathbf X^{[\mathrm S]}$ be the S splitting defined in (11) and let $\mathbf X$ be the solution of (1). Then there exists $C\geq1$ such that for all $p\geq2$ and $k=1,\ldots,N$, it holds:
\[
\left(\mathbb E[\|\mathbf X_{t_k}-\mathbf X^{[\mathrm S]}_{t_k}\|^p]\right)^{\frac1p}=R(h,\mathbf x_0).
\]
''','Lp convergence of S splitting')
claim('5.1',[17],r'''
Assume (A1)–(A6). Let $\mathbf X$ be the solution of (1) and $\widehat{\boldsymbol\theta}_N=(\widehat{\boldsymbol\beta}_N,\widehat{\boldsymbol\Sigma\boldsymbol\Sigma^\top}_N)$ be the estimator that minimizes either (22) or (23). If $h\to0$ and $Nh\to\infty$, then
\[
\widehat{\boldsymbol\beta}_N\xrightarrow{\mathbb P_{\boldsymbol\theta_0}}\boldsymbol\beta_0,\qquad
\widehat{\boldsymbol\Sigma\boldsymbol\Sigma^\top}_N\xrightarrow{\mathbb P_{\boldsymbol\theta_0}}\boldsymbol\Sigma\boldsymbol\Sigma_0^\top.
\]
''')
claim('5.2',[18],r'''
Assume (A1)–(A6). Let $\mathbf X$ be the solution of (1), and $\widehat{\boldsymbol\theta}_N=(\widehat{\boldsymbol\beta}_N,\widehat{\boldsymbol\varsigma}_N)$ be the estimator that minimizes either (22) or (23). If $\boldsymbol\theta_0\in\Theta$, $\mathbf C(\boldsymbol\theta_0)$ is positive definite, $h\to0$, $Nh\to\infty$ and $Nh^2\to0$, then under $\mathbb P_{\boldsymbol\theta_0}$,
\[
\begin{bmatrix}
\sqrt{Nh}(\widehat{\boldsymbol\beta}_N-\boldsymbol\beta_0)\\
\sqrt N(\widehat{\boldsymbol\varsigma}_N-\boldsymbol\varsigma_0)
\end{bmatrix}\xrightarrow{d}\mathcal N(\mathbf0,\mathbf C^{-1}(\boldsymbol\theta_0)).\tag{28}
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=26,main_text_boundary=dict(location='Published journal paper, pages 842-867, with main text and references across all 26 PDF pages. The Supplementary Material notice on page 23 links to separate SUPPA and SUPPB files; neither is embedded or opened.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==26 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
assert '10.1214/24-AOS2371' in pdf[0].get_text() and '842–867' in pdf[0].get_text()
for n in range(26):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'THEOREM (\d+(?:\.\d+)*)(?=[.\s(])',text)
            if match:labels.append((n+1,match.group(1)))
assert labels==[(14,'3.3'),(14,'3.5'),(15,'3.7'),(17,'5.1'),(18,'5.2')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=5,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Published Annals of Statistics 52(2),842-867, DOI 10.1214/24-AOS2371,26 PDF pages. The separate supplement and code links on page 23 are not opened; references continue through page 26.',
 'Independent heading enumeration finds exactly Theorems 3.3,3.5,3.7,5.1,5.2. Theorems 3.3 and 3.5 explicitly restate earlier results but remain included because they are labeled Theorem in the main text.',
 'All five full statements were visually checked on pages 14,15,17,18. The generic convergence theorem retains its 2p moment and p>=1, while the two splitting theorems retain their p moment and p>=2.',
 'Theorem 3.7 includes A6; Theorem 3.5 does not. Both retain the stated existence of C>=1 although their displayed bounds use the source remainder notation R instead.',
 'Both estimator theorems explicitly minimize the approximate objectives (22) or (23), not the original objectives (12) or (14). The full-versus-approximate distinction will be recorded during source resolution.',
 'Theorem 5.2 retains interior theta_0, positive-definite C, all three sampling limits, the distinct sqrt(Nh) and sqrt(N) scales and the covariance-coordinate vector. The source shorthand Sigma Sigma_0^T denotes the true covariance as explained on page 6.',
 'Only the inventory is complete. Resolve the SDE and split drift, A1-A6, remainder convention, local consistency and moment definitions, both schemes, approximate objectives, residual Z, covariance coordinates and C(theta_0). No supplement proof is used.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,14,15,17,18,23,26]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the SDE/split drift, A1-A6, remainder convention, Definitions 3.1/3.2, LT/S flows and noise, approximate objectives (22)/(23), residual Z, covariance coordinates and information matrix (27). Keep numerical versus statistical asymptotic regimes and full versus approximate objectives distinct. Exclude separate supplements; then finalize and independently audit.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated five complete main-text Theorems.')
