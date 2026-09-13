"""Reproduce all six original main-text Theorems from the registered arXiv v1 PDF.

The printed weight indices and step-size mismatch are deliberately preserved.
Reproduction does not perform a new mathematical review of the source.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1774'
SHA='776bf79a802495e8962fba69bf3da0584c4e0723efa6e9b17df8a546119afddf'
URL='https://arxiv.org/pdf/2301.01766v1'
STATEMENTS=[r'''The following properties hold for NPMLE:

1. (Existence) The minimizer of the optimization problem (1.1) exists.
2. (Optimality condition) A distribution $\widehat\rho\in\mathcal P(\mathbb R^d)$ is an NPMLE if and only if (i) $\delta\ell_N(\widehat\rho)(x)\geq-1$ holds for all $x\in\mathbb R^d$, and (ii) $\delta\ell_N(\widehat\rho)(x)=-1$ for $\widehat\rho$-a.e. $x$.''',
r'''Suppose that the initialization $\rho_0\in\mathcal P(\mathbb R^d)$ satisfies $\operatorname{supp}(\rho_0)=\mathbb R^d$. Consider the Wasserstein-Fisher-Rao gradient descent $\{\rho_n\}_{n\geq0}$ defined in (3.7). There exists $\eta_0>0$ determined by the samples $\{X_i\}_{1\leq i\leq N}$, such that if $0<\eta\leq\eta_0$ and $\rho_n\xrightarrow{\mathrm w}\widehat\rho$ when $n\to\infty$, then $\widehat\rho$ is the NPMLE.''',
r'''The system of coupled ODE
\[
\dot\mu_t^{(j)}=\frac1N\sum_{i=1}^N\frac{\phi(X_i-\mu_t^{(j)})}{\sum_{l=1}^m\omega_t^{(j)}\phi(X_i-\mu_t^{(l)})}(X_i-\mu_t^{(j)}),
\]
(3.8a)
\[
\dot\omega_t^{(j)}=\left[\frac1N\sum_{i=1}^N\frac{\phi(X_i-\mu_t^{(j)})}{\sum_{l=1}^m\omega_t^{(j)}\phi(X_i-\mu_t^{(l)})}-1\right]\omega_t^{(j)},
\]
(3.8b)
with initialization $\mu_0^{(1)},\ldots\mu_0^{(m)}\overset{\mathrm{i.i.d.}}\sim\operatorname{Uniform}(\{X_i\}_{1\leq i\leq N})$ and $\omega_0=[\omega_0^{(j)}]_{1\leq j\leq m}\in\Delta^{m-1}$ has unique solution on any time interval $[0,T]$. Moreover, the flow $(\rho_t)_{t\geq0}$ defined as
\[
\rho_t:=\sum_{l=1}^m\omega_t^{(l)}\delta_{\mu_t^{(l)}}
\]
(3.9)
is the Wasserstein-Fisher-Rao gradient flow, i.e. a distributional solution to the PDE (3.6).''',
r'''Suppose that the initialization $\rho_0\in\mathcal P(\mathbb R^d)$ satisfies $\operatorname{supp}(\rho_0)=\mathbb R^d$. Consider the Fisher-Rao gradient descent $\{\rho_n\}_{n\geq0}$ defined in (3.12). There exists $\eta_0$ determined by the samples $\{X_i\}_{1\leq i\leq N}$, such that if $0<\eta\leq\eta_0$ and $\rho_n\xrightarrow{\mathrm w}\widehat\rho$ when $n\to\infty$, then $\widehat\rho$ is the NPMLE.''',
r'''The ODE system
\[
\dot\omega_t^{(j)}=-\omega_t^{(j)}\left[1-\frac1N\sum_{i=1}^N\frac{\phi(X_i-\mu^{(j)})}{\sum_{l=1}^m\omega_t^{(l)}\phi(X_i-\mu^{(l)})}\right],\qquad1\leq j\leq m
\]
(3.15)
with initialization $\omega_0=[\omega_0^{(j)}]_{1\leq j\leq m}\in\Delta^{m-1}$ has unique solution on any time interval $[0,T]$. Moreover, the flow $(\rho_t)_{t\geq0}$ defined as
\[
\rho_t:=\sum_{l=1}^m\omega_t^{(l)}\delta_{\mu^{(l)}}
\]
(3.16)
is the Fisher-Rao gradient flow, i.e. (3.16) is a distributional solution to the PDE (3.11).''',
r'''The ODE system
\[
\dot\mu_t^{(j)}=\frac1N\sum_{i=1}^N\frac{\phi(X_i-\mu_t^{(j)})}{\sum_{l=1}^m\omega_t^{(j)}\phi(X_i-\mu_t^{(l)})}(X_i-\mu_t^{(j)}),
\]
(3.19)
with initialization $\mu_0^{(1)},\ldots\mu_0^{(m)}\overset{\mathrm{i.i.d.}}\sim\operatorname{Uniform}(\{X_i\}_{1\leq i\leq N})$ has unique solution on any time interval $[0,T]$. Moreover, the flow $(\rho_t)_{t\geq0}$ defined as
\[
\rho_t:=\frac1m\sum_{l=1}^m\delta_{\mu_t^{(l)}}
\]
(3.20)
is the Wasserstein gradient flow, i.e. (3.20) is a distributional solution to the PDE (3.18).''']
PAGES=[[3],[6],[6,7],[8],[8],[9]]
TITLES=['','Convergence to NPMLE','Particle Wasserstein-Fisher-Rao gradient flow','Convergence to NPMLE','Particle Fisher-Rao gradient flow','Particle Wasserstein gradient flow']
def inventory():
    claims=[dict(claim_id=PID+f'/T{i}',paper_id=PID,claim_kind='theorem',label=f'Theorem {i}'+(f' ({title})' if title else ''),source_order=i,statement_original=s,evidence=[dict(page=p,location=f'Theorem {i}; complete original statement'+('; concluding sentence above Algorithm 1' if i==3 and p==7 else '')) for p in pages]) for i,(s,pages,title) in enumerate(zip(STATEMENTS,PAGES,TITLES),1)]
    paper=dict(paper_id=PID,title='Learning Gaussian Mixtures Using the Wasserstein-Fisher-Rao Gradient Flow',authors=['Yuling Yan','Kaizheng Wang','Philippe Rigollet'],version='arXiv:2301.01766v1; title-page date January 5, 2023; arXiv stamp 4 Jan 2023',pdf_pages=51,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=15,main_text_boundary=dict(location='Main-text Figure 5 and its complete caption end on PDF page 15 before Appendix A (Preliminaries), whose heading starts at y=521.1. Saved page-15 evidence is clipped at y=520.1. No appendix body is included.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independent enumeration of actual bold Theorem headings throughout main-text pages 1–15, with page 15 clipped before Appendix A; visual comparison of all six complete original statements.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered and hash-verified local arXiv v1 PDF; no replacement download. Appendices excluded.',normalization_policy='Original wording and mathematical content preserved; line wrapping and LaTeX typography normalized. Printed indexing inconsistencies are not corrected.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
