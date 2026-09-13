"""Save every complete main-text Theorem from the pinned v3 PDF; exclude appendices."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,pages,body):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+n+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim('3.1',[16],r'''
Let $[a,b]\subseteq[0,\pi],a\leq b$. Assume that Assumption 3.1–3.5 hold, and consider a mapping $\mathscr G_\Upsilon$ of the form (3.23) that satisfies Assumption 3.6 for some $x\geq1$.

(a) case $\phi(z)=z$: Assume the above conditions with $p\geq6$. Then
\[
\left\{\rho_T M^{1/2}\left(\big(L_{U_M}^{a,b}\circ\mathscr G_\Upsilon(\widehat{\mathscr F})\big)(\eta)-\big(L^{a,b}\circ\mathscr G_\Upsilon(\mathscr F)\big)(\eta)\right)\right\}_{\eta\in I}
\overset{\mathscr D}{\Longrightarrow}\left\{\eta^{x-1}\mathbb W_{\mu_\Upsilon}(\eta)\right\}_{\eta\in I},\tag{3.27}
\]
where $\mathbb W_{\mu_\Upsilon}$ denotes a Brownian motion on $S_1(\mathcal H)$ corresponding to a zero-mean Gaussian measure $\mu_\Upsilon$ with covariance operator $\tau_\Upsilon^2=\int_0^1\Gamma_\Upsilon^{(u)}du$, pseudo-covariance operator $\widetilde\tau_\Upsilon^2=\int_0^1\Sigma_\Upsilon^{(u)}du$, and where $\Gamma_\Upsilon^{(u)}$ and $\Sigma_\Upsilon^{(u)}\in S_1(\mathcal H\otimes\mathcal H)$ are defined in (B.11) and (B.12), respectively.

(b) case $\phi(z)\neq z$: assume the above conditions with $p$ such that (3.30) holds. In addition, assume that $\mathscr F\in\mathbb D_1$ and that for some $0<\rho<1$,
\[
\sum_{r\in\mathbb N}\sum_{j=l}^\infty\nu_{\mathbb C,p}^{X_\cdot^\cdot(e_r)}(j)=O((l+1)^{-\rho}).\tag{3.28}
\]
Then for analytic functions $\phi(z)$ that satisfy $\phi'(cz)=h(c)\phi'(z)$, where $c\in[0,1]$ and $h$ is a continuous function with $h(1)=1$,
\[
\left\{\rho_T M^{1/2}\left(\big(L_{U_M}^{a,b}\circ\mathscr G_\Upsilon(\widehat{\mathscr F})\big)(\eta)-\big(L^{a,b}\circ\mathscr G_\Upsilon(\mathscr F)\big)(\eta)\right)\right\}_{\eta\in I}
\overset{\mathscr D}{\Longrightarrow}\left\{\eta^{x-1}h(\eta)\mathbb W_{\mu_\Upsilon}(\eta)\right\}_{\eta\in I}.\tag{3.29}
\]
''')
claim('3.2',[18,19],r'''
Suppose that the conditions of Corollary 3.1 hold true and that there exists a function $\mathbf f=(f_1,\ldots,f_k)^\top\in C(I,\mathbb R^k)$, a diagonal matrix $\mathbf g=\operatorname{diag}(g_{11},\ldots,g_{kk})\in C(I,\mathbb R_{>0}^{k\times k})$, and a positive definite matrix $\sigma\in\mathbb R^{k\times k}$ such that (3.34) and (3.35) hold. Assume additionally that the matrix $\mathbb U=(\mathbb U_{ij}^2)_{i,j=1,\ldots,k}$ given by
\[
\mathbb U_{ij}^2=\int_0^1\big(g_{ii}(\eta)\mathbb B_i(\eta)-f_i(\eta)g_{ii}(1)\mathbb B_i(1)\big)\overline{\big(g_{jj}(\eta)\mathbb B_j(\eta)-f_j(\eta)g_{jj}(1)\mathbb B_j(1)\big)}\nu(d\eta),\tag{3.39}
\]
where $\mathbb B_1,\ldots,\mathbb B_k$ are the components of the $k$-dimensional Brownian motion in (3.34), is non-singular. Then the random vector $\widehat{\mathscr D}=(\widehat{\mathscr D}_1(1),\ldots,\widehat{\mathscr D}_k(1))^\top$ satisfies
\[
\widehat{\mathscr D}^{\top}V_k^{-1}\widehat{\mathscr D}\overset{\mathscr D}{\longrightarrow}\mathbb B(1)^\top\mathbf g(1)\mathbb U^{-1}\mathbf g(1)\mathbb B(1),\tag{3.40}
\]
where the matrix $V_k=(V_{i,j}^2)_{i,j=1,\ldots,k}$ is defined by (3.37). In particular, for each $j=1,\ldots,k$,
\[
\frac{\widehat{\mathscr D}_j(1)}{V_{jj}}=\frac{\mathscr T_{j,T}(\widehat{\mathscr F})(1)-\mathscr T_j(\mathscr F)(1)}{V_{jj}}\overset{\mathscr D}{\longrightarrow}\frac{g_{jj}(1)\mathbb B_j(1)}{\mathbb U_{jj}},
\]
where $\mathbb B_j$ denote a standard Brownian motion and $V_{jj}$ and $\mathbb U_{jj}$ are defined by (3.37) and (3.39), respectively.
''')
claim('3.3',[20],r'''
Suppose the conditions of Theorem 3.1(b) hold true and that $\lambda_1^{(u,\omega)}>\ldots>\lambda_d^{(u,\omega)}>0$ uniformly in $(u,\omega)\in[0,1]\times[0,\pi]$. Then
\[
\left\{M^{1/2}\rho_T\eta^3\left(\frac{\sum_{i=1}^d\frac1M\sum_{u\in U_M}\int_a^b\widehat\lambda_i^{(u,\omega)}(\eta)d\omega}{\frac1M\sum_{u\in U_M}\int_a^b\operatorname{Tr}\big(\widehat{\mathscr F}_{u,\omega}(\eta)\big)d\omega}-\frac{\sum_{i=1}^d\int_0^1\int_a^b(\lambda_i^{(u,\omega)})d\omega du}{\int_0^1\int_a^b\operatorname{Tr}\big(\mathscr F_{u,\omega}\big)d\omega du}\right)\right\}_{\eta\in I}
\overset{\mathscr D}{\Longrightarrow}\left\{\eta^2\sigma\mathbb B(\eta)\right\}_{\eta\in I}\tag{3.42}
\]
for some $\sigma\geq0$ and a standard Brownian motion $\mathbb B$.
''')
claim('3.4',[20],r'''
Suppose the conditions of Theorem 3.1(b) hold true and that $\delta_1^{(u,\omega)}>\ldots>\delta_d^{(u,\omega)}>0$ uniformly in $(u,\omega)\in[0,1]\times[0,\pi]$. Then
\[
\left\{M^{1/2}\rho_T\eta^3\left(\frac{\sum_{j=1}^d\frac1M\sum_{u\in U_M}\int_a^b(\widehat\delta_j^{(u,\omega)}(\eta))^2d\omega}{\sum_{j=1}^\infty\frac1M\sum_{u\in U_M}\int_a^b(\widehat\delta_j^{(u,\omega)}(\eta))^2d\omega}-\frac{\sum_{j=1}^d\int_0^1\int_a^b(\delta_j^{(u,\omega)})^2d\omega du}{\sum_{j=1}^\infty\int_0^1\int_a^b(\delta_j^{(u,\omega)})^2d\omega du}\right)\right\}_{\eta\in I}
\overset{\mathscr D}{\Longrightarrow}\left\{\eta^2\sigma\mathbb B(\eta)\right\}_{\eta\in I}\tag{3.44}
\]
for some $\sigma\geq0$ and a standard Brownian motion $\mathbb B$.
''')
claim('3.5',[21],r'''
Suppose the conditions of Theorem 3.1(b) hold true and that $\nu_1^{u,\omega}>\ldots>\nu_d^{u,\omega}>0$ and $\lambda_{ii,1}^{(u,\omega)}>\ldots,\lambda_{ii,d}^{(u,\omega)}>0$, $i\in\{1,2\}$. Then,
\[
\left\{M^{1/2}\rho_T\left(\frac1M\sum_{u\in U_M}\int_a^b\eta^4\widehat{\mathscr R}_d^{u,\omega}(\eta)d\omega-\int_0^1\int_a^b\eta^4\mathscr R_d^{u,\omega}d\omega du\right)\right\}_{\eta\in I}
\overset{\mathscr D}{\Longrightarrow}\left\{\eta^3\sigma\mathbb B(\eta)\right\}_{\eta\in I}\tag{3.45}
\]
for some $\sigma\geq0$ and a standard Brownian motion $\mathbb B$.
''')
claim('3.6',[21],r'''
Under the conditions of Theorem 3.1(b)
\[
\left\{M^{1/2}\rho_T\eta\left(\widehat r_d(\eta)-r_d(\eta)\right)\right\}_{\eta}\overset{\mathscr D}{\Longrightarrow}\left\{\sigma\eta\mathbb B(\eta)\right\}_{\eta}.
\]
''')
claim('4.1',[22],r'''
For $\beta\in(0,1)$ let $q_\beta$ denote the $\beta$-quantile of the distribution of the random variable $\mathbb T$ defined in (4.1). If $r=\mathscr T(\mathscr F)>0$ and the assumptions of Theorem 3.2 are satisfied, then the interval
\[
\widehat I_T=\big[\widehat r+q_{\alpha/2}V,\widehat r+q_{1-\alpha/2}V\big],\tag{4.2}
\]
defines an asymptotic $(1-\alpha)$-confidence interval for the measure $r$.
''')
claim('4.2',[22],r'''
Suppose that the assumptions of Theorem 3.2 hold. The test (4.3) is a consistent asymptotic level-$\alpha$ test for the hypotheses (2.15) with $\Delta>0$.
''')
claim('4.3',[24],r'''
If the assumptions of Theorem 3.2 are satisfied, we have for the estimator in (4.8)
\[
\lim_{T\to\infty}\mathbb P\big(\widehat d<d^*\big)=0\quad\text{and}\quad\lim_{T\to\infty}\mathbb P\big(\widehat d>d^*\big)\leq\alpha.
\]
In particular, if $\alpha=\alpha_T$ in (4.8) depends on $T$ such that $\alpha_T\to0$ as $T\to\infty$, we have
\[
\lim_{T\to\infty}\mathbb P\big(\widehat d\neq d^*\big)=0.
\]
''')
claim('4.4',[24],r'''
If the assumptions of Theorem 3.2 are satisfied then the test that rejects the null hypothesis $H_0:d^*\leq d_0$ in (2.19) whenever $\widehat d>d_0$, has asymptotic level $\alpha$ and is consistent for the hypotheses in (2.19).
''')
claim('4.5',[25],r'''
If the assumptions of Theorem 3.2 are satisfied then the decision rule (4.11) defines an asymptotic and consistent level $\alpha$-test for the hypotheses (4.9) and (2.17).
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=30,main_text_boundary=dict(location='Main text Sections 1-5 and its references finish on PDF page 30. Appendix A starts on a separate page 31, confirmed by a heading-only crop; appendix bodies on pages 31-86 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==86 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
for n in range(30):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='Utopia-Bold':
                    m=re.fullmatch(r'Theorem (\d+\.\d+)\.',span['text'].strip())
                    if m:labels.append((n+1,m.group(1)))
expected=[(16,'3.1'),(18,'3.2'),(20,'3.3'),(20,'3.4'),(21,'3.5'),(21,'3.6'),(22,'4.1'),(22,'4.2'),(24,'4.3'),(24,'4.4'),(25,'4.5')]
assert labels==expected,labels
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
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=11,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Pinned arXiv:2208.10158v3, stamped 16 September 2023, 86 pages. The main references end on page 30; Appendix A starts on page 31, with only its headings inspected. No appendix bodies are used.',
 'Exactly eleven main-text Theorem environments occur: 3.1-3.6 and 4.1-4.5. A separate font-sensitive enumeration distinguishes Utopia-Bold theorem labels from prose references. Corollary 3.1 is a prerequisite reference, not a Theorem inventory record.',
 'Full original bodies were visually reviewed on pages 16,18,19,20,21,22,24,25. Theorem 3.2 spans pages 18-19, retaining its nonsingularity condition, vector quadratic-form limit and scalar specialization. All other theorem bodies fit on their cited page.',
 'Theorem 3.1 retains both phi branches, the p references, coordinate dependence condition (3.28), analytic homogeneity, Banach-space Brownian motion and the exact covariance/pseudo-covariance references to appendix equations B.11/B.12. Those appendix-only formulas are unresolved under the main-text policy.',
 'Theorem 3.2 preserves the conjugate on the second factor of (3.39), the ordinary transpose in (3.40), the matrix notation with squared entries and the scalar denominators as printed. No real-only rewrite or conjugate-transpose repair is substituted.',
 'Theorems 3.3 and 3.4 retain their normalized spectral ratios and uniform ordered positivity assumptions; Theorem 3.5 retains the printed comma in the marginal eigenvalue chain and its eta-fourth scaling. Theorem 3.6 is the complete short statement and has no added sigma qualifier sentence.',
 'Theorems 4.1-4.5 retain the confidence-interval signs, referenced hypotheses and decision rules, and both conclusions of Theorem 4.3 including its alpha_T-to-zero claim. Source issues in those references will be recorded during prerequisite extraction without changing these statements.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,16,18,19,20,21,22,24,25,30]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
for name in ['appendix-heading-only','condition-328','covariance-339']:shutil.copy2(work/(name+'.png'),ROOT/'evidence'/(name+'.png'))
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve Definition 2.1, Assumptions 3.1-3.6, spectral estimators and transformations, Corollary 3.1 conditions, self-normalizers and model-selection rules using main pages 1-30 only. Preserve unresolved appendix-only covariance formulas.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated eleven complete main-text Theorems.')
