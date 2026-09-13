"""Preserve the eleven printed main-text Theorem statements before extraction."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,page,body,title=None):
 claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+((' ('+title+')') if title else ''),source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=page,location='Theorem '+n)]))
claim('2.1',6,r'''
Let $0<\alpha<0.3$. Then
\[
a_1\omega_z(\varepsilon;f)\leq R_z(\varepsilon;f)\leq A_1\omega_z(\varepsilon;f),\tag{2.3}
\]
\[
a_1\omega_m(\varepsilon;f)\leq R_m(\varepsilon;f)\leq A_1\omega_m(\varepsilon;f),\tag{2.4}
\]
\[
b_\alpha\omega_z(\varepsilon/3;f)\leq L_{z,\alpha}(\varepsilon;f)\leq B_\alpha\omega_z(\varepsilon;f),\tag{2.5}
\]
\[
b_\alpha\omega_m(\varepsilon/3;f)\leq L_{m,\alpha}(\varepsilon;f)\leq B_\alpha\omega_m(\varepsilon;f),\tag{2.6}
\]
where the constants $a_1,A_1,b_\alpha,B_\alpha$ can be taken as $a_1=\Phi(-0.5)\approx0.309$, $A_1=1.5$, $b_\alpha=0.6-2\alpha$, and $B_\alpha=3(1-2\alpha)z_\alpha$.
''')
claim('2.2',9,r'''
Let $R_z(\varepsilon;f)$, $R_m(\varepsilon;f)$, $L_{z,\alpha}(\varepsilon;f)$, and $L_{m,\alpha}(\varepsilon;f)$ be defined as in (1.2)–(1.7). Let $0<\alpha<0.3$. Then for any $f\in\mathcal F$,
\[
274\varepsilon^2>R_z(\varepsilon;f)\cdot R_m(\varepsilon;f)^2\geq\frac{\Phi(-0.5)^3}2\varepsilon^2,\tag{2.12}
\]
\[
3^7\cdot(1-2\alpha)^3\varepsilon^2>L_{z,\alpha}(\varepsilon;f)\cdot L_{m,\alpha}(\varepsilon;f)^2\geq\frac{(0.6-2\alpha)^3}{18}\varepsilon^2.\tag{2.13}
\]
''','Uncertainty Principle')
claim('2.3',10,r'''
For any estimator $\widehat Z$, if $\mathbb E_{f_0}|\widehat Z-Z(f_0)|\leq\gamma R_z(\varepsilon;f_0)$ for some $f_0\in\mathcal F$ and $\gamma<0.1$, then there exists $f_1\in\mathcal F$ such that
\[
\mathbb E_{f_1}(|\widehat Z-Z(f_1)|)\geq\frac1{40}\left(\log\frac1\gamma\right)^{1/3}R_z(\varepsilon;f_1).\tag{2.15}
\]
Similarly, for any estimator $\widehat M$, if $\mathbb E_{f_0}|\widehat M-M(f_0)|\leq\gamma R_m(\varepsilon;f_0)$ for some $f_0\in\mathcal F$ and $\gamma<0.1$, then there exists $f_1\in\mathcal F$ such that
\[
\mathbb E_{f_1}|\widehat M-M(f_1)|\geq\frac18\left(\log\frac1\gamma\right)^{1/3}R_m(\varepsilon;f_1).\tag{2.16}
\]
''','Penalty for super-efficiency')
claim('3.1',16,r'''
The estimator $\widehat Z$ defined in (3.5) satisfies
\[
\mathbb E_f|\widehat Z-Z(f)|<53\rho_z(\varepsilon;f)\leq C_zR_z(\varepsilon;f),\quad\text{for all }f\in\mathcal F,
\]
where $C_z>0$ is an absolute constant.
''','Estimation of Minimizer')
claim('3.2',16,r'''
Let $0<\alpha<0.3$. The confidence interval $CI_{z,\alpha}$ given in (3.6) is a $(1-\alpha)$ level confidence interval for the minimizer $Z(f)$ and its expected length satisfies
\[
\mathbb E_f L(CI_{z,\alpha})\leq(24\times2^{K_\alpha}-3)\times17.5\times\rho_z(\varepsilon;f)\leq C_{z,\alpha}L_{z,\alpha}(\varepsilon;f),\quad\text{for all }f\in\mathcal F,
\]
where $K_\alpha=\left\lceil\frac{\log\alpha}{\log\Phi(-2)}\right\rceil$ and $C_{z,\alpha}$ is a constant depending on $\alpha$ only.
''','Confidence Interval for the Minimizer')
claim('3.3',16,r'''
The estimator $\widehat M$ defined in (3.7) satisfies
\[
\mathbb E_f|\widehat M-M(f)|<449\rho_m(\varepsilon;f)\leq C_mR_m(\varepsilon;f),\quad\text{for all }f\in\mathcal F,
\]
where $C_m>0$ is an absolute constant.
''','Estimation of Minimum')
claim('3.4',16,r'''
The confidence interval $CI_{m,\alpha}$ given in (3.10) is a $(1-\alpha)$ confidence interval for the minimum $M(f)$ and when $0<\alpha<0.3$, its expected length satisfies
\[
\mathbb E_f L(CI_{m,\alpha})\leq c_{m,\alpha}\rho_m(\varepsilon;f)\leq C_{m,\alpha}L_{m,\alpha}(\varepsilon;f),\quad\text{for all }f\in\mathcal F,
\]
where $c_{m,\alpha}$ and $C_{m,\alpha}$ are constants depending on $\alpha$ only.
''','Confidence Interval for the Minimum')
claim('4.1',23,r'''
The estimator $\widehat Z$ of the minimizer $Z(f)$ defined in (4.5) satisfies
\[
\mathbb E_f|\widehat Z-Z(f)|\leq C_1\widetilde R_{z,n}(\sigma;f),\quad\text{for all }f\in\mathcal F,\tag{4.12}
\]
where $C_1>0$ is an absolute constant.
''','Estimation of the Minimizer')
claim('4.2',23,r'''
Let $0<\alpha<0.3$. The confidence interval $\mathrm{CI}_{z,\alpha}$ given in (4.7) is a $(1-\alpha)$-level confidence interval for the minimizer $Z(f)$ and its expected length satisfies
\[
\mathbb E_f L(\mathrm{CI}_{z,\alpha})\leq C_{2,\alpha}\widetilde L_{z,\alpha,n}(\sigma;f),\quad\text{for all }f\in\mathcal F,
\]
where $C_{2,\alpha}$ is a constant depending on $\alpha$ only.
''')
claim('4.3',23,r'''
The estimator $\widehat M$ defined in (4.9) satisfies
\[
\mathbb E_f|\widehat M-M(f)|\leq C_3\widetilde R_{m,n}(\sigma;f),\quad\text{for all }f\in\mathcal F,
\]
where $C_3$ is an absolute constant.
''','estimation for the minimum')
claim('4.4',23,r'''
Let $0<\alpha<0.3$. The confidence interval $\mathrm{CI}_{m,\alpha}$ given in (4.11) is a $(1-\alpha)$-level confidence interval and its expected length satisfies
\[
\mathbb E_f L(\mathrm{CI}_{m,\alpha})\leq C_{4,\alpha}\widetilde L_{m,\alpha,n}(\sigma;f),\quad\text{for all }f\in\mathcal F,
\]
where $C_{4,\alpha}$ is a constant depending only on $\alpha$.
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=26,main_text_boundary=dict(location='All 26 pages belong to the main paper. Section 5 ends on page 25, followed by acknowledgments and a pointer to a separate supplement. References continue through page 26, followed by author addresses. No appendix or supplement body is embedded in this PDF; the separate supplement is excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
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
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.now(timezone.utc).isoformat(),theorem_count=11,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),notes=[
 'Pinned arXiv:2305.00164v2 stamped 10 March 2024. All 26 main-document pages searched for printed Theorem environments; the separate supplement was not opened.',
 'Visually checked complete statements on pages 6, 9, 10, 16 and 23. None crosses a page boundary. Printed theorem titles and capitalization are retained.',
 'Theorem 2.1 contains all four benchmark comparisons, including epsilon/3 in the confidence lower bounds and all four explicit constants.',
 'Theorem 2.2 retains strict upper bounds, the constant 274 and the power 3^7. The later geometric uncertainty expression (2.14) is upright discussion, outside the theorem.',
 'Theorem 2.3 retains both estimator cases and the printed gamma<0.1 without silently adding gamma>0 to the original statement. The following remark supplies the positive-small-gamma context separately.',
 'Theorem 3.2 constant is (24 times 2^(K_alpha) minus 3) times 17.5. All coverage claims and function-uniform assertions remain in the inventory.',
 'Theorem 3.4 places the alpha<0.3 condition on expected length after its coverage assertion; that wording is retained.',
 'Theorem 4.3 does not print positivity for C3, unlike C1 in Theorem 4.1; no positivity is added. Theorem 4.4 does not explicitly repeat the target minimum in its coverage clause.',
 'Theorems 3.x use white-noise constructions; Theorems 4.x use discrete regression constructions and discretization-aware benchmarks. Their reused estimator names are not treated as identical.',
 'Propositions, remarks, discussion inequalities and theorem citations are excluded; all numbered theorem environments are included.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve benchmark quantifiers, convex-function conventions and the two distinct multistage adaptive constructions from the main text; preserve all estimator and interval branches before graph finalization.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated eleven Theorems.')
