"""Archive the seven visually inspected main-text Theorem environments."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
claims=[]
def claim(n,pages,body):
 claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+n+(' (continued)' if i else '')) for i,p in enumerate(pages)]))
claim('1',[10],r'''
Under Assumption (E1), (E2), (F1), (L1), (L2), (R1), for $k\in[K]$, let $c_k:=\frac{d_{-k}^2}{s_{-k}^2}\left(1+\frac{d_k^2}{T^2}\right)+\frac{d_{-k}}{s_{-k}}d_k^{\alpha_{k,1}}\min\left\{1+\frac{d_k}{T},\frac{r_kd_k}{T}\right\}$, then
\[
\left\|\widehat{\mathbf Q}_{k,(z_k)}-\mathbf Q_k\ddot{\mathbf H}_k\right\|^2=O_p\left(d_k^{-2\alpha_{k,z_k}}c_k\right),\tag{3.10}
\]
where $\ddot{\mathbf H}_k=\frac{\mathbf D_k^{1/2}\ddot{\mathbf F}_k(\mathbf I_T-\frac1T\mathbf1_T\mathbf1_T^\top)\ddot{\mathbf F}_k^\top\mathbf A_k^\top\widehat{\mathbf Q}_{k,(z_k)}\ddot{\mathbf V}_k^{-1}}{T}$ has $\operatorname{rank}(\ddot{\mathbf H}_k)=z_k$. Moreover, further assuming (L1'), there exists $\widehat{\mathbf U}_{k,(z_k)}$ with $\widehat{\mathbf U}_{k,(z_k)}^\top\widehat{\mathbf U}_{k,(z_k)}=\mathbf I_{z_k}$ such that $\widehat{\mathbf Q}_{k,(z_k)}=\widehat{\mathbf U}_{k,(z_k)}\mathbf P_{k,(z_k)}$ with $\mathbf P_{k,(z_k)}$ an orthogonal matrix, and
\[
\left\|\widehat{\mathbf U}_{k,(z_k)}-\mathbf U_{k,(z_k)}\right\|^2=O_p\left(d_k^{-2\alpha_{k,z_k}}\left[d_k^{2\alpha_{k,1}}\frac{r_k}{T}+c_k\right]\right),\tag{3.11}
\]
where $\mathbf U_{k,(z_k)}$ is the matrix consisting of the first $z_k$ columns of $\mathbf U_k$.
''')
claim('2',[13,14],r'''
Let Assumption (E1), (E2), (F1), (L1), (L2), (R1) be satisfied for all $M$ chosen random samples, and
\[
c_{k,pre}:=\min\left\{1+\frac{d_k}{T},\frac{r_kd_k}{T}\right\}\frac{\frac1M\sum_{m=1}^M d_{-k,m}s_{-k,m}}{s_{-k,pre}^2}+d_k^{\alpha_{k,1}}\left(1+\frac{d_k^2}{T^2}\right)\frac{\frac1M\sum_{m=1}^M d_{-k,m}^2}{s_{-k,pre}^2}.
\]
Then
\[
\left\|\widehat{\mathbf Q}_{k,pre,(z_k)}-\mathbf Q_k\ddot{\mathbf H}_{k,pre}\right\|^2=O_p\left(d_k^{-2\alpha_{k,z_k}}c_{k,pre}\right),\tag{3.15}
\]
where $\ddot{\mathbf H}_{k,pre}=\frac{\mathbf D_k^{1/2}\frac1M\sum_{m=1}^M[\ddot{\mathbf F}_{k,m}(\mathbf I_T-\frac1T\mathbf1_T\mathbf1_T^\top)\ddot{\mathbf F}_{k,m}^\top]\mathbf A_k^\top\widehat{\mathbf Q}_{k,pre,(z_k)}\ddot{\mathbf V}_{k,pre}^{-1}}{T}$ has $\operatorname{rank}(\ddot{\mathbf H}_k)=z_k$. Moreover, further assuming (L1'), there exists $\widehat{\mathbf U}_{k,pre,(z_k)}$ with $\widehat{\mathbf U}_{k,pre,(z_k)}^\top\widehat{\mathbf U}_{k,pre,(z_k)}=\mathbf I_{z_k}$ such that $\widehat{\mathbf Q}_{k,pre,(z_k)}=\widehat{\mathbf U}_{k,pre,(z_k)}\mathbf P_{k,pre,(z_k)}$ with $\mathbf P_{k,pre,(z_k)}$ being an orthogonal matrix, so that
\[
\left\|\widehat{\mathbf U}_{k,pre,(z_k)}-\mathbf U_{k,(z_k)}\right\|^2=O_p\left(d_k^{-2\alpha_{k,z_k}}\left[d_k^{2\alpha_{k,1}}\frac{r_k}{T}+c_{k,pre}\right]\right).\tag{3.16}
\]
The matrix $\mathbf U_{k,(z_k)}$ is defined to be the matrix consisting of the first $z_k$ columns of $\mathbf U_k$.
''')
claim('4',[15],r'''
For each random sample, if the sample size is $n_l$ for each $l\ne k$, then under Assumptions (E1), (E2), (F1), (L1), (L2'), (R1), (R2), with the pre-averaging estimator or the maximum eigenvalue ratio estimator based on choosing the $M$ samples with the largest eigenvalue ratios defined in (3.14), we have
\[
\left\|\widehat{\mathbf Q}_{k,pre,(z_k)}-\mathbf Q_k\ddot{\mathbf H}_{k,pre}\right\|^2\asymp\left\|\widehat{\mathbf Q}_{k,max,(z_k)}-\mathbf Q_k\ddot{\mathbf H}_{k,max}\right\|^2=O_p\left(d_k^{-2\alpha_{k,z_k}}c_{k,max}\right),
\]
where
\[
c_{k,max}:=\min\left\{1+\frac{d_k}{T},\frac{r_kd_k}{T}\right\}\frac{d_{-k}}{s_{-k,max}}+d_k^{\alpha_{k,1}}\left(1+\frac{d_k^2}{T^2}\right)\frac{d_{-k,}^2}{s_{-k,max}^2}.
\]
Moreover, further assuming (L1'), for the same definition of $\widehat{\mathbf U}_{k,pre,(z_k)}$ and $\widehat{\mathbf U}_{k,max,(z_k)}$ as before,
\[
\left\|\widehat{\mathbf U}_{k,pre,(z_k)}-\mathbf U_{k,(z_k)}\right\|^2\asymp\left\|\widehat{\mathbf U}_{k,max,(z_k)}-\mathbf U_{k,(z_k)}\right\|^2=O_p\left(d_k^{-2\alpha_{k,z_k}}\left[d_k^{2\alpha_{k,1}}\frac{r_k}{T}+c_{k,max}\right]\right).\tag{3.18}
\]
''')
claim('6',[20],r'''
Let all the assumptions in Theorem 4 be satisfied, together with (RE1). Let $g_s:=\prod_{j=1}^K d_j^{\alpha_{j,1}}$ and $S_\psi^{(k)}:=\sum_{j=1}^{d_{-k}}\|\boldsymbol\Psi_j^{(k)}\|^2$. Assume further that for each $k\in[K]$,
\[
r=O(r_e),\quad d_k=O(g_s)=(r_e+\sqrt T)S_\psi^{(k)},\quad\max_{j\in[d_{-k}]}\|\boldsymbol\Sigma_{\epsilon,j}^{(k)}\|=O\left(\prod_{j=1}^K d_j^{\alpha_{j,1}}\sqrt{\frac rT}\right).
\]
Then
\[
\left\|\check{\mathbf q}_k^{(1)}-\mathbf U_{k,(1)}\right\|=O_P\left\{\sqrt{\frac rT}\left[1+b_k^2\frac dT\right]+g_s^{-1/2}b_k\sqrt{\frac{rd}T}\right\},\ (\text{assumed }o_P(1))\quad\text{where}
\]
\[
b_k=K\sqrt{\frac{r_{max}}T}+\sum_{j=1;j\ne k}^K d_j^{-\alpha_{j,1}}c_{j,max}^{1/2}=o(1).
\]
Furthermore, if
\[
K\left(r+\max_{j\in[d_{-k}]}\|\boldsymbol\Sigma_{\epsilon,j}^{(k)}\|\right)\prod_{j=1}^K d_j^{1-\alpha_{j,1}}=o(T),
\]
then the Algorithm for Iterative Projection Direction Refinement will produce, after a certain number of iterations (say $m$),
\[
\left\|\check{\mathbf q}_k^{(m)}-\mathbf U_{k,(1)}\right\|=O_P\left(\sqrt{\frac rT}\right).
\]
''')
claim('7',[21],r'''
Let all the assumptions in Theorem 6 be satisfied. Suppose we know the value of $r_k$, and perform eigenanalysis on $\widetilde{\boldsymbol\Sigma}_{y,m+1}^{(k)}$ in (4.4) which utilized the projection direction $\check{\mathbf q}_k^{(m)}$ in Theorem 6, obtaining $r_k$ eigenvectors as an estimator of the factor loading space of $\mathbf A_k$.

Then there exists $\check{\mathbf U}_k\in\mathbb R^{d_k\times r_k}$ with $\check{\mathbf U}_k^\top\check{\mathbf U}_k=\mathbf I_{r_k}$ such that the $r_k$ eigenvectors obtained above is $\check{\mathbf U}_k$ multiplied with some orthogonal matrix, with
\[
\begin{aligned}
\|\check{\mathbf U}_k-\mathbf U_k\|=O_P\Bigg\{g_s^{-1/2}d_k^{\alpha_{k,1}-\alpha_{k,r_k}}\Bigg[&\sqrt{\frac rT}\left(\sqrt{d_k}+K\sqrt{\frac{rd}T}+\sqrt{r_e S_\psi^{(k)}}\right)\\
&+g_s^{-1}d_k^{\alpha_{k,1}-\alpha_{k,r_k}}\left(\max_{j\in[d_{-k}]}\|\boldsymbol\Sigma_{\epsilon,j}^{(k)}\|\left[1+\frac{K^2rd}{T^2}\right]+S_\psi^{(k)}\right)\Bigg]\Bigg\},\ (\text{assumed }o_P(1)).
\end{aligned}
\]
''')
claim('8',[23,24],r'''
Let Assumption (E1), (F1) and (RE2) hold. For each $k\in[K]$, define the correlation matrix
\[
\mathbf R_{y,m+1}^{(k)}=\operatorname{diag}^{-1/2}(\boldsymbol\Sigma_{y,m+1}^{(k)})\boldsymbol\Sigma_{y,m+1}^{(k)}\operatorname{diag}^{-1/2}(\boldsymbol\Sigma_{y,m+1}^{(k)}).
\]
Then, in probability, for large enough $T,d_k$, we have $\lambda_j(\mathbf R_{y,m+1}^{(k)})\succeq_P r_k^{-1}d_k^{1-\alpha_{k,1}+\alpha_{k,j}}>1$ for $j\in[r_k]$, whereas $\lambda_j(\mathbf R_{y,m+1}^{(k)})\leq1$ for $j=r_k+1,\ldots,d_k$.
''')
claim('9',[24],r'''
Let all the assumptions in Theorem 6 hold, together with (RE2). Suppose further that
\[
d_k^{\alpha_{k,1}-\alpha_{k,r_k}}\left(\max_{j\in[d_{-k}]}\|\boldsymbol\Sigma_{\epsilon,j}^{(k)}\|+S_\psi^{(k)}\right)=o(g_s),\quad d_k^{\alpha_{k,1}-\alpha_{k,r_k}}\sqrt{\frac rT}\left[\sqrt{r_eS_\psi^{(k)}}+K\sqrt{\frac{rd}T}\right]=o(g_s),
\]
where $g_s$ is defined in Theorem 6. Then as $T,d_k\to\infty$, we have for each $k\in[K]$,
\[
\begin{aligned}
\lambda_j(\widetilde{\mathbf R}_{y,m+1}^{(k)})&=\begin{cases}
\lambda_j(\mathbf R_{y,m+1}^{(k)})(1+O_P\{r_kd_k^{\alpha_{k,1}-\alpha_{k,j}-1}a_T(\alpha_{k,1})+a_T(0)\}),&j\in[r_k];\\
\lambda_j(\mathbf R_{y,m+1}^{(k)})+O_P\{a_T(0)\},&j\in[d_k]/[r_k],
\end{cases}\\
&\begin{cases}
\succeq_P r_k^{-1}d_k^{1-\alpha_{k,1}+\alpha_{k,j}}(1+O_P\{r_kd_k^{\alpha_{k,1}-\alpha_{k,j}-1}a_T(\alpha_{k,1})+a_T(0)\}),&j\in[r_k];\\
\leq1+O_P\{a_T(0)\},&j\in[d_k]/[r_k],
\end{cases}
\end{aligned}
\]
where for $0\leq\delta\leq1$,
\[
a_T(\delta):=\sqrt{\frac rT}\left(d_k^\delta+Kd_k^{(\delta+\alpha_{k,1})/2}\sqrt{\frac{rd}{Tg_s}}+\frac{K^2r^{1/2}d d_k^{\alpha_{k,1}}}{T^{3/2}g_s}\max_{j\in[d_{-k}]}\|\boldsymbol\Sigma_{\epsilon,j}^{(k)}\|\right)=o(1).
\]
Hence $\widehat r_k$ in (5.2) is a consistent estimator for $r_k$ if we choose $\eta_T=Ca_T(0)$ for some constant $C>0$.
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=38,main_text_boundary=dict(location='Main-text Section 6.4 ends on PDF page 38 after Tables 5-7 and the portfolio interpretation. PDF page 39 begins Section 7, Appendix: Basic Tensor Manipulations, on a fresh page. Only the appendix heading was inspected; appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
for c in claims:
 for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
  depth=0
  for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
   depth+=1 if b=='{' else -1
   assert depth>=0,c['claim_id']
  assert depth==0,c['claim_id']
p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.now(timezone.utc).isoformat(),inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),theorem_count=7,notes=[
 'Pinned arXiv:2208.04012v1, stamped 8 August 2022, 80 pages; equivalence to the journal publication is not assumed.',
 'Searched all 38 main-text pages and independently enumerated bold CMBX10 Theorem headings: 1, 2, 4, 6, 7, 8, 9. Numbers 3 and 5 are not Theorems; printed numbering is preserved.',
 'Visually checked every theorem page, including both page continuations (Theorems 2 and 8). Main-text endpoint and heading-only appendix boundary were visually checked.',
 'Theorems 1, 2 and 4 add L1-prime only for the final eigenvector-alignment assertion. Full original clauses and transformations are retained.',
 'Theorem 2 prints rank(H-double-dot-k), omitting pre in that rank expression. This is retained rather than silently repaired.',
 'Theorem 4 prints a trailing comma in the subscript of d-squared-minus-k in c-k-max. This source typography is retained.',
 'Theorem 6 prints d_k=O(g_s)=(r_e+sqrt(T))S_psi^(k). The unusual chained equality is retained without interpreting it as a different big-O condition.',
 'Theorem 7 has an outer g_s^(-1/2)d_k^(alpha_k1-alpha_krk) multiplying a bracket containing both rate terms; the second term has another g_s^(-1)d_k^(alpha_k1-alpha_krk). Nesting is preserved.',
 'Theorem 8 explicitly assumes only E1, F1 and RE2. Its projected covariance reference needs source dependency resolution; assumptions from Theorem 6 are not inserted into its statement.',
 'Theorem 9 ends with consistency for eta_T=C a_T(0), C>0. Subsequent pervasive-factor rate simplifications use upright body text and are outside the theorem.',
 'Theorem 9 uses [d_k]/[r_k] for its second range and places inequality signs inside the second cases block; both source conventions are retained.',
 'Proofs, lemmas, remarks, theorem citations and appendix bodies are excluded. Assumption, estimator and model references remain to be resolved during interface extraction.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
for n in [10,13,14,15,20,21,23,24,38]:
 shutil.copy2(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(Path(prov['working_pdf']).parent/'appendix-heading.png',ROOT/'evidence/appendix-heading.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the main-text model, assumptions, sample selection, projection algorithm and correlation-rank estimator; preserve source ambiguities separately; build and validate the local interface census.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated seven Theorems.')
