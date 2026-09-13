"""Save every complete original main-paper Theorem before interface extraction."""
import datetime,fitz,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
claims=[]
def claim(n,pages,body,title=None):
    label='Theorem '+str(n)+((' ('+title+')') if title else '')
    claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label=label,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+str(n)+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim('4.1',[11],r'''
For a separable metric space $(\Omega,d)$ the distance profiles $F_\omega$ and the transport ranks $R_\omega$ satisfy the following properties:

(a) Let $h:\Omega\to\widetilde\Omega$ be a bijective isometric measurable map between $(\Omega,d)$ and $(\widetilde\Omega,\widetilde d)$ and $P_h(\cdot)=P(h^{-1}(\cdot))$ the push-forward measure on $\widetilde\Omega$. Then $F^{P_h}_{h(\omega)}(u)=F^P_\omega(u)$ for all $u\in\mathbb R$, hence $R^{P_h}_{h(\omega)}=R^P_\omega$, where $F^P_\omega(u)=\mathbb P(d(\omega,X)\leq u)$ and $X$ is a $\Omega$-valued random element such that $P=\mathbb P X^{-1}$, $F^{P_h}_{h(\omega)}(u)=\mathbb P(\widetilde d(h(\omega),h(X))\leq u)$, $R^P_\omega$ is the transport rank of $\omega$ with respect to $P$ and $R^{P_h}_{h(\omega)}$ is the transport rank of $h(\omega)$ with respect to $P_h$.

(b) If $\omega_\oplus$ is a transport mode of $P$ as per (14), $R_{\omega_\oplus}\geq1/2$. Moreover $R_{\omega_\oplus}\geq R_\omega$ for any $\omega\in\Omega$ and $\omega_\oplus\in\mathcal M_\oplus$.

(c) Suppose $\omega_\oplus$ is a transport mode of $P$. Let $\gamma:[0,1]\to\Omega$ be curve in $(\Omega,d)$ such that $\gamma(0)=\omega_\oplus$ and $F_{\gamma(s)}(u)\geq F_{\gamma(t)}(u)$ for all $u\in\mathbb R$ and $0\leq s<t\leq1$. Then $R_{\gamma(s)}(u)\geq R_{\gamma(t)}(u)$ whenever $0\leq s<t\leq1$.

(d) Suppose the metric space $(\Omega,d)$ is of strong negative type (9) and $P_1,P_2$ are two probability measures on the space. Then $P_1=P_2$ if and only if $R^{P_1}_\omega=R^{P_2}_\omega$ for all $\omega\in\Omega$, where $R^{P_1}_\omega$ and $R^{P_2}_\omega$ are the transport ranks of $\omega$ with respect to $P_1$ and $P_2$.
''')
claim('5.1',[12],r'''
Under Assumptions 1 and 2, $\{\sqrt n(\widehat F_\omega(t)-F_\omega(t)):\omega\in\Omega,\ t\in\mathbb R\}$ converges weakly to a zero-mean Gaussian process $\mathbb G_P$ with covariance given by
\[
C_{(\omega_1,t_1),(\omega_2,t_2)}=\operatorname{Cov}(y_{\omega_1,t_1}(X),y_{\omega_2,t_2}(X))
\]
for $\omega_1,\omega_2\in\Omega$ and $t_1,t_2\in\mathbb R$.
''')
claim('5.2',[13],r'''
Under Assumptions 1 and 2,
\[
\sqrt n\sup_{\omega\in\Omega}|\widehat R_\omega-R_\omega|=O_{\mathbb P}(1).
\]
''')
claim('5.3',[14],r'''
Assume that the distribution $P$ is such that $\mathcal M_\oplus$ is non-empty. Under Assumptions 1–3,
\[
\rho_H(\widehat{\mathcal M}_\oplus,\mathcal M_\oplus)=o_{\mathbb P}(1).
\]
''')
claim('6.1',[17],r'''
Under $H_0$ (20) and Assumptions 1, 4, 5 and 6, $T_{nm}^w$ converges in distribution to the law of a random variable $L=2\sum_{j=1}^\infty Z_j^2\mathbb E_V(\lambda_j^V)$, where $Z_1,Z_2,\ldots$ is a sequence of i.i.d. $N(0,1)$ random variables, $V\sim P$ where $P=P_1=P_2$ under $H_0$ and for any $x\in\Omega$, $\lambda_1^x\geq\lambda_2^x\geq\ldots$ are the eigenvalues of the covariance surface given by
\[
C^x(u,v)=\sqrt{w_x(u)w_x(v)}\operatorname{Cov}(\mathbb I(d(x,V')\leq u),\mathbb I(d(x,V')\leq v))
\]
with $V'\sim P$.
''')
claim('6.2',[17],r'''
Under Assumptions 1, 4, 5 and 6, for a sequence of alternatives $H_{nm}$, the power of the level $\alpha$ test (30) satisfies $\beta_{nm}^w\to1$.
''')
claim('6.3',[18],r'''
Under $H_0$ (20) and Assumptions 1, 4, 5 and 6, as $n,m\to\infty$ and $K\to\infty$ it holds that $|\widehat\Gamma_{m,n}(t)-\Gamma_L(t)|=o_{\mathbb P}(1)$ for every $t$ which is a continuity point of $\Gamma_L(\cdot)$.

Suppose that $\Gamma_L(\cdot)$ is continuous and strictly increasing at $q_\alpha$. Then under $H_0$ (20) and Assumptions 1, 4, 5 and 6, as $n,m\to\infty$ and $K\to\infty$,
\[
|\widehat q_\alpha-q_\alpha|=o_{\mathbb P}(1).\tag{32}
\]
Assume further that $\overline\Gamma_L(\cdot)$ is continuous and strictly increasing at $\overline q_\alpha$ and $\frac n{n+m}-c=O((n+m)^{-1/2})$ and $\frac m{n+m}-(1-c)=O((n+m)^{-1/2})$ as $n,m\to\infty$. Then under Assumptions 1, 4, 5 and 6 for the sequence of alternatives $H_{nm}$, the power (31) of the permutation test satisfies $\widetilde\beta_{nm}^w\to1$ as $n,m\to\infty$.
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=33,main_text_boundary=dict(location='Main text ends after Funding on PDF page 33, before the SUPPLEMENTARY MATERIAL heading at y=106.52787780761719. Page 33 is clipped above that heading; all subsequent embedded supplement mathematics and references are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==73 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
assert '2202.06117v4' in pdf[0].get_text() and '27 Feb 2024' in pdf[0].get_text()
for n in range(33):
    clip=fitz.Rect(0,0,pdf[n].rect.width,prov['main_text_shared_page_cutoff_y']) if n==32 else pdf[n].rect
    for block in pdf[n].get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'THEOREM (\d+(?:\.\d+)*)\.',text)
            if match:labels.append((n+1,match.group(1)))
assert labels==[(11,'4.1'),(12,'5.1'),(13,'5.2'),(14,'5.3'),(17,'6.1'),(17,'6.2'),(18,'6.3')],labels
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
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=7,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Pinned arXiv:2202.06117v4, stamped 27 February 2024, 73 pages. Main text ends after Funding on page 33, above the embedded Supplementary Material heading at y=106.52787780761719. No supplement mathematics was read.',
 'Independent heading enumeration finds exactly Theorems 4.1,5.1,5.2,5.3,6.1,6.2,6.3 in source order. Other result types, discussion references and supplement proof headings are excluded.',
 'Complete original statements were visually checked on pages 11,12,13,14,17,18. Theorem 4.1 retains all four branches, including the printed extra argument u in its transport-rank monotonicity conclusion.',
 'Theorem 5.1 retains the weak convergence statement and covariance kernel, with the Gaussian-process symbol verified as blackboard G from the PDF font. Theorems 5.2/5.3 retain their uniform rank rate and Hausdorff consistency assertions.',
 'Theorem 6.1 retains the weighted chi-square series using averaged eigenvalues, the weighted covariance surface and the exact null/assumption list. Its operator domain and weight restrictions must be resolved from the main text during the next stage.',
 'Theorem 6.3 preserves its three clauses: pointwise convergence at continuity points, null critical-value consistency and power under alternatives. The swapped subscript m,n on its estimated CDF remains as printed; the additional root-sample-size balancing and mixture-CDF assumptions remain separate.',
 'Only the theorem inventory is complete. The census remains in progress pending distance profiles/ranks/medians, strong negative type, assumptions, weighted statistics, alternative sequences and permutation quantities. Apparent source inconsistencies must be recorded separately, not repaired in original statements.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,11,12,13,14,17,18]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve distance profiles, transport ranks/modes/median sets, strong negative type, empirical definitions, Assumptions 1-6, weighted two-sample statistics, alternatives and permutation laws. Check density/support and median-separation source conditions literally. Read only main text above the page-33 cutoff, then finalize and independently audit.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated seven complete main-text Theorems.')
