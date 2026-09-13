"""Regenerate the complete source-ordered main-text theorem inventory."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1534'
SHA='1743d4d93efb6c31474b16cf5e8c92c491becdb499f0ae6afb5a8b2942603e23'
claims=[]
def claim(n,pages,title,text):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n+', complete original statement'+(' including continuation' if len(pages)>1 else '')) for p in pages]))
claim('1',[6],'Form of the efficient influence function in RKHS settings',r'''
Suppose $\nu$ is pathwise differentiable at $P$ and $\dot{\mathcal H}_P$ is an RKHS. Both of the following implications hold:

(i) If $\nu$ has an EIF $\phi_P$ at $P$, then $\phi_P=\widetilde\phi_P$ $P$-almost surely.

(ii) If $\|\widetilde\phi_P\|_{L^2(P;\mathcal H)}<\infty$, then $\nu$ has an EIF at $P$.
''')
claim('2',[14],'Asymptotic linearity and weak convergence of a one-step estimator',r'''
Suppose that $\nu$ is pathwise differentiable at $P_0$ with EIF $\phi_0\in L^2(P_0;\mathcal H)$ and, for $j\in\{1,2\}$, $\mathcal R_n^j=o_p(n^{-1/2})$ and $\mathcal D_n^j=o_P(n^{-1/2})$. Under these conditions, (4) holds, $\bar\nu_n$ is regular, and
\[
n^{1/2}[\bar\nu_n-\nu(P_0)]\rightsquigarrow\mathbb H,\tag{22}
\]
where $\mathbb H$ is a tight $\mathcal H$-valued Gaussian random variable that is such that, for each $h\in\mathcal H$, the marginal distribution $\langle\mathbb H,h\rangle_{\mathcal H}$ is $N(0,E_0[\langle\phi_0(Z),h\rangle_{\mathcal H}^2])$.
''')
claim('3',[15],'Asymptotically valid confidence set',r'''
Suppose the conditions of Theorem 2 hold. Further suppose that $\|\phi_0\|_{L^2(P_0;\mathcal H)}>0$, $\Omega_n\in\mathcal O$, $\Omega_0\in\mathcal O$, and $\|\Omega_n-\Omega_0\|_{\mathrm{op}}=o_p(1)$.

(i) if $\widehat\zeta_n\to\zeta_{1-\alpha}$ in probability, then $\lim_{n\to\infty}P_0^n\{\nu(P_0)\in\mathcal C_n(\widehat\zeta_n)\}=1-\alpha$.

(ii) if $\widehat\zeta_n$ is an asymptotically conservative estimator of $\zeta_{1-\alpha}$, in the sense that $P_0^n\{\widehat\zeta_n\ge\zeta_{1-\alpha}-\delta\}\xrightarrow{n\to\infty}1$ for all $\delta>0$, then $\liminf_{n\to\infty}P_0^n\{\nu(P_0)\in\mathcal C_n(\widehat\zeta_n)\}\ge1-\alpha$.
''')
claim('4',[15],'Consistent estimation of $\zeta_{1-\alpha}$ via the bootstrap',r'''
Suppose the conditions of Theorem 2 hold. Further suppose that $\Omega_n\in\mathcal O$, $\Omega_0\in\mathcal O$, $\|\Omega_n-\Omega_0\|_{\mathrm{op}}=o_p(1)$, and $\max_{j\in\{1,2\}}\|\phi_n^j-\phi_0\|_{L^2(P_0;\mathcal H)}=o_p(1)$. Under these conditions, $\widehat\zeta_n\to\zeta_{1-\alpha}$ in probability.
''')
claim('5',[16,17],'Rate of convergence of regularized one-step estimator',r'''
Suppose $\nu$ is pathwise differentiable at $P_0$, $\beta_n\in\ell^2_*$ for each $n\in\mathbb N$, and both $\mathcal R_n^{j,\beta_n}$ and $\mathcal D_n^{j,\beta_n}$ are $O_p[\|\beta_n\|_{\ell^2}/n^{1/2}]$ for $j\in\{1,2\}$. Under these conditions, (25) holds. Moreover, if $\mathcal B_n^{j,\beta_n}=O_p(\|\beta_n\|_{\ell^2}/n^{1/2})$ for $j\in\{1,2\}$, then
\[
\bar\nu_n^{\beta_n}-\nu(P_0)=O_p\left(\|\beta_n\|_{\ell^2}/n^{1/2}\right).\tag{27}
\]
''')
claim('6',[19],'Local power of regularized hypothesis test',r'''
Fix $\beta\in\ell^2\cap(0,1]^{\mathbb N}$ and $h_0\in\mathcal H$. Suppose $\nu$ is pathwise differentiable at $P_0$, $\nu(P_0)=h_0$, $\widetilde\nu_n^\beta$ is an asymptotically linear estimator of $\nu^\beta(P_0)$ with influence function $\phi_0^\beta$, and $\widehat\zeta_n$ is a consistent estimator of the $(1-\alpha)$-quantile $\zeta_{1-\alpha}$ of $\|\mathbb H^\beta\|_{\mathcal H}^2$. Fix $\{P_\epsilon:\epsilon\}\in\mathscr P(P_0,\mathcal P,s)$ such that $\|\dot\nu_0(s)\|_{\mathcal H}>0$. If $\Gamma_\beta^{-1}[\mathcal C_n^\beta(\widehat\zeta_n)]$ is as defined in (30), then
\[
P_{\epsilon=n^{-1/2}}^n\left\{h_0\notin\Gamma_\beta^{-1}[\mathcal C_n^\beta(\widehat\zeta_n)]\right\}\xrightarrow{n\to\infty}\Pr\left\{\|\mathbb H^\beta+\dot\nu_0^\beta(s)\|_{\mathcal H}^2>\zeta_{1-\alpha}\right\}>\alpha.
\]
Also, $h_n:=\nu(P_{\epsilon=n^{-1/2}})$ is an $n^{-1/2}$-rate local alternative in that $\|h_n-h_0\|_{\mathcal H}=O(n^{-1/2})$.
''')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='One-Step Estimation of Differentiable Hilbert-Valued Parameters',authors=['Alex Luedtke','Incheoul Chung'],version='arXiv:2303.16711v3, 27 September 2023; manuscript dated 28 September 2023',source_url='https://arxiv.org/pdf/2303.16711v3',pdf_pages=83,pdf_sha256=SHA,main_text_last_pdf_page=30,main_text_boundary=dict(location='Main text and references end after Zheng and Laan (2011) on PDF page 30, before Appendices at y=638.9385986328125 PDF points. The appendix contents and bodies are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified registered arXiv v3 PDF; pages 1-29 and page 30 above Appendices only.'),papers=[paper],claims=claims),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
