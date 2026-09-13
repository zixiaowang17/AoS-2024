"""Save the independently enumerated main-text Theorems from the local v6 PDF."""
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
PID = 'aos-2024-v52-i03-p1227'
REPO = next(p for p in ROOT.parents if (p / 'scripts/resolve_paper_pdf.py').is_file())
prov = {'paper_id': 'aos-2024-v52-i03-p1227', 'title': 'Locally simultaneous inference', 'version': 'arXiv:2212.09009v6, 2 May 2024', 'source_url': 'https://arxiv.org/pdf/2212.09009v6', 'pdf_pages': 36, 'pdf_sha256': 'ea45ffa0b45eaf01a2f6bc84b6758bd5363e3fb2d6478610f1e17d132b95a0e7'}
claims = []

def claim(n, pages, text):
    claims.append(dict(claim_id=f'{PID}/T{n}', paper_id=PID, claim_kind='theorem',
        label=f'Theorem {n}', source_order=n, statement_original=text.strip(),
        evidence=[dict(page=p, location=f'Theorem {n}' + (' (continued)' if i else '')) for i,p in enumerate(pages)]))

claim(1, [9], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Suppose that the simultaneous confidence regions $\{C_{\gamma\cdot\Gamma'}\}_{\Gamma'\subseteq\Gamma}$ are monotone (Ass. 1). Consider the set of targets
\[
\widehat\Gamma^+_\nu=\bigcup_{P'\in B_\nu(y)}\Gamma_\nu(P')=\bigcup_{P'\in B_\nu(y)}\bigcup_{y'\in A_\nu(P')}\widehat\Gamma(y').\tag{2}
\]
Then, it holds that
\[
P\left\{\theta_\gamma\in C^{(\alpha-\nu)}_{\gamma\cdot\widehat\Gamma^+_\nu},\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(2, [10], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Suppose that the confidence intervals are monotone (Ass. 1), i.e., $q^\alpha_{\Gamma_1}\le q^\alpha_{\Gamma_2}$ for all $\Gamma_1\subseteq\Gamma_2$, and centered (Ass. 2). Let $A_\nu(P)=\{y:\theta_\gamma\in C_\gamma(q^\nu_\Gamma),\forall\gamma\in\Gamma\}$, and let $\widehat\Gamma^+_\nu$ denote the set of targets from Theorem 1 (Eq. (2)). Let
\[
\hat q=\min\left\{q^{(\alpha-\nu)}_{\widehat\Gamma^+_\nu},q^\alpha_\Gamma\right\}.
\]
Then, it holds that
\[
P\left\{\theta_\gamma\in C_\gamma(\hat q),\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(3, [11,12], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$.

- For the problem of inference on the winner (Eq. (3)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\{\gamma\in[m]:y_\gamma\ge y_{\hat\gamma}-4q^\nu([m])\}.
\]
Then,
\[
P_\mu\left\{\mu_{\hat\gamma}\in\left(y_{\hat\gamma}\pm\min\left\{q^{(\alpha-\nu)}(\widehat\Gamma^+_\nu),q^\alpha([m])\right\}\right)\right\}\ge1-\alpha.
\]

- For the file-drawer problem (Eq. (4)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\{\gamma\in[m]:y_\gamma\ge T-2q^\nu([m])\}.
\]
Then,
\[
P_\mu\left\{\mu_\gamma\in\left(y_\gamma\pm\min\left\{q^{(\alpha-\nu)}(\widehat\Gamma^+_\nu),q^\alpha([m])\right\}\right),\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(4, [13], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Assume that $C^{\alpha_1}_\gamma\supseteq C^{\alpha_2}_\gamma$ for all $\alpha_1,\alpha_2\in(0,1)$ such that $\alpha_1\le\alpha_2$.

- For the problem of inference on the winner (Eq. (5)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\left\{\gamma\in[m]:y_\gamma\ge y_{\hat\gamma}-4w^{\nu/m}_n\right\}.
\]
Then,
\[
P\left\{\theta_{\hat\gamma}\in C^{(\alpha-\nu)/|\widehat\Gamma^+_\nu|}_{\hat\gamma}\right\}\ge1-\alpha.
\]

- For the file-drawer problem (Eq. (6)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\left\{\gamma\in[m]:y_\gamma\ge T-2w^{\nu/m}_n\right\}.
\]
Then,
\[
P\left\{\theta_\gamma\in C^{(\alpha-\nu)/|\widehat\Gamma^+_\nu|}_\gamma,\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(5, [16], r'''
Algorithm 1 returns exactly the set of plausible models, i.e.
\[
\widehat{\mathcal M}^+_\nu=\left\{\widehat M(y'):\|X^\top y-X^\top y'\|_\infty\le2q^\nu(\{X_j\}_{j=1}^d)\right\}.
\]
''')
claim(6, [17], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Assume that $|\ell(f,z)|\le1$ for all $z$ and $f\in\mathcal F$. Consider the data-dependent hypothesis class:
\[
\widehat{\mathcal F}^+_\nu=\left\{f\in\mathcal F:R_n(f,\mathcal D)\le R_n(\hat f,\mathcal D)+4\operatorname{Gap}_n(\mathcal F)+4\sqrt{\frac2n\log\left(\frac1\nu\right)}\right\}.
\]
Then,
\[
P\left\{R(\hat f,P)\le R_n(\hat f,\mathcal D)+\operatorname{Gap}_n(\widehat{\mathcal F}^+_\nu)+\sqrt{\frac2n\log\left(\frac1{\alpha-\nu}\right)}\right\}\ge1-\alpha.
\]
''')

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=27, main_text_boundary=dict(location='Substantive main text ends with acknowledgements on PDF page 25; references continue through page 27. Appendix A, Deferred proofs, begins on page 28 at y=106.64. All appendices are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Existing local arXiv:2212.09009v6 PDF, pages 1–27 before Appendix A; no external retrieval.'),papers=[paper],claims=claims)
    dest=ROOT/'theorem-inventory.json';dest.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    main()
