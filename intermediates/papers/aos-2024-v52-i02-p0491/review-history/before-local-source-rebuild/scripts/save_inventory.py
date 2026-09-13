"""Save every main-text Theorem before extracting interface dependencies."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,page,title,body):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=page,location='Theorem '+n)]))
claim('1.2',5,'Oracle inequality for the empirical risk',r'''
Under Assumption (SubGE), the empirical risk at the stopping time $\tau$ in Equation (1.8) with $C_\tau\geq8\overline\sigma^2$ satisfies
\[
\begin{aligned}
\|\widehat F^{(\tau)}-f^*\|_n^2
&\leq\min_{m\geq0}\left(7\|\widehat F^{(m)}-f^*\|_n^2+\frac{(8\overline\sigma^2+C_\tau)m\log p}n\right)+|\widehat\sigma^2-\|\varepsilon\|_n^2|\\
&\leq7\|\widehat F^{(m^o)}-f^*\|_n^2+\frac{(8\overline\sigma^2+C_\tau)m^o\log p}n+|\widehat\sigma^2-\|\varepsilon\|_n^2|
\end{aligned}
\]
with probability converging to one.
''')
claim('1.8',9,'Optimal adaptation for the population risk',r'''
Under Assumptions (SubGE), (Sparse), (SubGD) and (CovB), choose $\widehat\sigma^2$ in Equation (1.8) such that there is a constant $C_{Noise}>0$ for which
\[
|\widehat\sigma^2-\|\varepsilon\|_n^2|\leq C_{Noise}\mathcal R(s,\gamma)
\]
with probability converging to one. Then, the population risk at the stopping time in Equation (1.8) with $C_\tau=c(\overline\sigma^2+\rho^4)$ for any $c>0$ satisfies
\[
\|\widehat F^{(\tau)}-f^*\|_{L^2}^2\leq C_{PopRisk}\mathcal R(s,\gamma)
\]
with probability converging to one for a constant $C_{PopRisk}>0$.
''')
claim('5.1',23,'Two-step procedure',r'''
Under Assumptions (SubGE), (Sparse), (SubGD) and (CovB), choose $\widehat\sigma^2$ in Equation (1.8) such that
\[
\widehat\sigma^2\leq\|\varepsilon\|_n^2+C\mathcal R(s,\gamma)
\]
with probability converging to one. Then, for any choice $C_\tau=c(\overline\sigma^2+\rho^4)$ in (1.8) with $c\geq0$ and $C_{AIC}=C(\overline\sigma^2+\rho^4)$ with $C>0$ large enough, the two-step procedure satisfies that with probability converging to one, $\tau_{two\text{-}step}\geq\widetilde m_{s,\gamma,G}$ from Equation (3.2) for some $G>0$. On the corresponding event,
\[
\|\widehat F^{(\tau_{two\text{-}step})}-f^*\|_{L^2}^2\leq C\mathcal R(s,\gamma).
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=24,main_text_boundary=dict(location='The main text and references end on PDF page 24. Appendix A: Proofs for the main results starts on PDF page 25. Appendix pages 25-43 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.now(timezone.utc).isoformat(),theorem_count=3,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),notes=[
 'Pinned arXiv:2210.07850v1, stamped 14 October 2022. The source has 43 pages; main pages 1-24 were searched, and the Appendix A heading alone was cropped from page 25.',
 'Only Theorems 1.2, 1.8 and 5.1 are printed in the main text. References to other authors Theorems and proof headings do not add inventory entries. None of the three statements spans a page boundary.',
 'Theorem 1.2 retains the chained inequality, its minimum over all nonnegative iterations and the classical oracle m^o. The noise proxy has an overbar, distinct from the estimated empirical noise level with a hat.',
 'Theorem 1.8 requires a two-sided absolute empirical-noise estimation bound and c>0. Theorem 5.1 requires only an upper bound, allows c=0, and includes both the iteration lower bound and the risk bound on the corresponding event.',
 'All three complete theorem bodies were checked visually on pages 5, 9 and 23. Pages 24 and the Appendix A heading establish the reading boundary. Appendix bodies were not read or used.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,5,9,23,24]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(work/'appendix-heading-only.png',ROOT/'evidence/appendix-heading-only.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve OMP iteration, stopping rules, all four assumptions, oracle/rate definitions and the lower-bound iteration from the main text.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated three Theorems.')
