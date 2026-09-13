"""Save every main-text Theorem before extracting interface dependencies."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0491', 'title': 'Early stopping for L2-boosting in high-dimensional linear models', 'version': 'arXiv:2210.07850v1', 'source_url': 'https://arxiv.org/pdf/2210.07850v1', 'pdf_pages': 43, 'pdf_sha256': '15996787a07db24f10b36d5ab632a1cbdf0b72cf4881d7ed9337b130e3ae1252'}
claims=[]
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
def main():
    repo = Path(__file__).resolve().parents[5]
    source = Path(subprocess.check_output([sys.executable, str(repo/'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=24,main_text_boundary=dict(location='The main text and references end on PDF page 24. Appendix A: Proofs for the main results starts on PDF page 25. Appendix pages 25-43 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)

if __name__ == '__main__':
    main()
