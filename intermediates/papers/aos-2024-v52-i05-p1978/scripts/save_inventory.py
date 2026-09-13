"""Reproduce four complete original main-text Theorems from the registered v3 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p1978'
SHA='0194b287549417eda9cd7a75dc478785011344d4a34a2b0222bdc952ed4ccc37'
URL='https://arxiv.org/pdf/2011.08661v3'
NUMBERS=['2','3','4','5'];PAGES=[[10],[11,12],[13,14],[14]]
STATEMENTS=[r'''Let $\widehat\tau_{\mathrm{DIPW}}$ be the estimator (15) where $\hat\mu\in\mathbb R^n$ is constructed via (14) with tuning parameter $\eta=c_\eta\sqrt{\log(p)/n}$ and where the constant $c_\eta>0$ is sufficiently large. Suppose Assumptions 1–5 hold. Then we have the decomposition
\[
\sqrt n(\widehat\tau_{\mathrm{DIPW}}-\bar\tau)=\delta+\sqrt{\sigma_\mu^2+\bar\sigma^2}\,\zeta
\]
in which given constants $c_\gamma,c_{\tilde\mu}>0$, $c_{\hat\pi}\in(0,\frac12]$ and $m\in\mathbb N$, we have that $\delta$ and $\zeta$ satisfy the following properties:

(i) there exist constants $c_\delta,c>0$ such that
\[
\mathbb P\left[|\delta|>c_\delta(s+\sqrt{s\log n})\frac{\log p}{\sqrt n}\right]\leq\mathbb P(\Omega^c(c_\gamma,c_{\tilde\mu},c_{\hat\pi}))+c(p^{-m}+n^{-m});
\]
(17)
(ii) there exists constant $c_\zeta>0$ such that
\[
\sup_{t\in\mathbb R}|\mathbb P(\zeta\leq t\mid\mathcal D)-\Phi(t)|\leq\frac{c_\zeta}{\sqrt n}\frac{\sigma_\mu^2\|\widehat{\boldsymbol\mu}-\boldsymbol\mu_{\mathrm{ORA}}\|_\infty+\bar\rho^3}{(\sigma_\mu^2+\bar\sigma^2)^{3/2}}.
\]
(18)''',r'''Consider the setup of Theorem 2. We have the decomposition
\[
\sqrt n(\widehat\tau_{\mathrm{DIPW}}-\tau)=\delta+\sigma_\mu\zeta_1+\sigma\zeta_2
\]
(21)
and given constants $c_\gamma,c_{\tilde\mu}>0$, and $c_{\hat\pi}\in(0,1/2]$, we have that $\delta$, $\zeta_1$ and $\zeta_2$ satisfy the following properties:

(i) $\delta$ satisfies (i) of Theorem 2;

(ii) there exists constants $c_{\zeta,1},c_{\zeta,2}$ such that
\[
\sup_{t\in\mathbb R}|\mathbb P(\zeta_1\leq t\mid\mathcal D)-\Phi(t)|\leq\frac{c_{\zeta,1}}{\sqrt n}\frac{\|\widehat{\boldsymbol\mu}-\boldsymbol\mu_{\mathrm{ORA}}\|_\infty}{\sigma_\mu},
\]
\[
\sup_{t\in\mathbb R}|\mathbb P(\zeta_2\leq t)-\Phi(t)|\leq\frac{c_{\zeta,2}}{\sqrt n}\frac{\rho^3}{\sigma^3};
\]
(iii) $\mathbb E(\zeta_1\zeta_2\mid\mathcal D)=0$.''',r'''Suppose tuning parameter $\eta=c_\eta\sqrt{\log(p)/n}$ used to form each $\widehat{\boldsymbol\mu}_j$ involved in the construction of $\widehat\tau_{\mathrm{AVE}}$ is such that the constant $c_\eta>0$ is sufficiently large. Suppose Assumptions 1–7 hold and let the confidence interval $\widetilde C_\alpha$ be as in (24). Given constants $c_\gamma,c_{\tilde\mu},c_\varepsilon>0$, $c_{\hat\pi}\in(0,\frac12]$ and $m\in\mathbb N$, there exist constants $c,c_\zeta>0$ such that with probability at least
\[
1-\sum_{j=1}^3\mathbb P(\Omega_j^c(c_\gamma,c_{\tilde\mu},c_{\hat\pi}))-c(n^{-m}+p^{-m}),
\]
(25)
we have for all $\alpha\in(0,1]$ the finite sample coverage guarantee
\[
\mathbb P\left(\bar\tau\in\widetilde C_{\alpha/3}\mid\mathbf X\right)\geq1-\alpha-c_\zeta\left(\mathbb E(\|\widehat{\boldsymbol\mu}-\boldsymbol\mu_{\mathrm{ORA}}\|_\infty\mid\mathbf X)\sqrt{\frac{\log n}{n}}+\frac{\sqrt{b_n\log p\log n}}{n^{1/4}}+b_n+p^{-m}\right).
\]
(26)''',r'''Suppose we construct $\widehat\tau_{\mathrm{AVE}}$ as in Theorem 4 and suppose Assumptions 1–5 hold. We have the decomposition
\[
\sqrt n(\widehat\tau_{\mathrm{AVE}}-\tau)=\delta+\sigma\zeta,
\]
in which given constants $c_\gamma,c_{\tilde\mu}>0$, $c_{\hat\pi}\in(0,1/2]$ and $m\in\mathbb N$, we have that $\delta$ and $\zeta$ satisfy the following properties:

(i) there exist constants $c_\delta,c>0$ such that given any sequence $(e_n)_{n=1}^\infty$, with probability at least
\[
1-\sum_{j=1}^3\mathbb P(\Omega_j^c(c_\gamma,c_{\tilde\mu},c_{\hat\pi}))-c(n^{-m}+p^{-m})-2e^{-e_n^2},
\]
we have that
\[
|\delta|\leq c_\delta(s+\sqrt{s\log n})\frac{\log p}{\sqrt n}+c_\delta\frac{e_n}{\sqrt n}\|\tilde\mu(\mathbf X)-\boldsymbol\mu_{\mathrm{ORA}}\|_2;
\]
(ii) there exists constant $c_\zeta>0$ such that
\[
\sup_{t\in\mathbb R}|\mathbb P(\zeta\leq t)-\Phi(t)|\leq\frac{c_\zeta}{\sqrt n}\frac{\rho^3}{\sigma^3}.
\]''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; complete original statement'+(' including next-page continuation' if len(pages)>1 else '')) for p in pages]) for i,(n,s,pages) in enumerate(zip(NUMBERS,STATEMENTS,PAGES),1)]
    paper=dict(paper_id=PID,title='Debiased inverse propensity score weighting for estimation of average treatment effects with high-dimensional confounders',authors=['Yuhao Wang','Rajen D. Shah'],version='arXiv:2011.08661v3; arXiv stamp 11 Apr 2024; title-page date April 12, 2024',pdf_pages=67,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=27,main_text_boundary=dict(location='Section 7 Discussion continues onto PDF page 27, followed by Acknowledgement. Main-text evidence on page 27 is clipped at y=380 above References at y=395.7. References extend to page 30; Appendix A begins on page 30 at y=224.3. No appendix body is used.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerated actual bold Theorem environments throughout pages 1-26 and the main-text prefix of page 27. Visually compared Theorems 2-5 in full, including Theorem 3 part (iii) on page 12 and Theorem 4 coverage on page 14. Lemma 1, Corollary 6, theorem citations and appendix results are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v3 PDF. Main text only; no replacement PDF, website or appendix body.',normalization_policy='Preserve complete original wording, formulas, all subparts and references. Normalize PDF wrapping and mathematical typesetting only. The explanatory footnote about constant dependencies is retained separately from the theorem body.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved four complete original Theorems; independent source validation is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
