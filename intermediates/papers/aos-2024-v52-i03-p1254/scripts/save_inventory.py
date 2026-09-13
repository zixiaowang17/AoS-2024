"""Rebuild the manually transcribed inventory; source review is recorded separately."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p / 'scripts/resolve_paper_pdf.py').is_file())
PID = 'aos-2024-v52-i03-p1254'
SHA = 'feb88302a3a7ca3efb79aab2c89bc712f3609ee7e705c2d5ec3a9d0c714d0901'
claims = []


def claim(number, title, pages, statement):
    claims.append(dict(claim_id=f'{PID}/T{number}', paper_id=PID,
        claim_kind='theorem', label=f'Theorem {number} ({title})',
        source_order=len(claims)+1, statement_original=statement.strip(),
        evidence=[dict(page=p, location=f'Theorem {number}, '+('complete printed statement' if len(pages)==1 else ('statement through limiting-parameter formulas' if i==0 else 'italic continuation specifying both integration contours, before Remark 2.3'))) for i,p in enumerate(pages)]))


claim('2.1', 'LSD', [6], r'''
Under Assumptions A-D, the ESD $F^{\mathbf S_n\Theta_n}(x)$ converges to the limiting spectral distribution $F$ with high probability. The Stieltjes transform $m(z)$ associated with $F$ is analytic in $\mathbb C^+$. For each $z\in\mathbb C^+$, $m=m(z)$ represents a unique solution to the equation:
\[
m=\int\frac1{t(1-y-yzm)-z}\,dH(t),\tag{2.1}
\]
where uniqueness is guaranteed within the set $\{m\in\mathbb C^+:-\frac{1-y}{z}+ym\in\mathbb C^+\}$.
''')

claim('2.2', 'No outside eigenvalues', [7], r'''
Consider the gram matrix $\mathbf S_n\Theta_n$. Assume that the interval $[a,b]$ with $a>0$ lies outside the support of $F^{c,H}$ and $F^{c_n,H_n}$ for all large $n$. Then with high probability, no eigenvalue of $\mathbf S_n\Theta_n$ appears in $[a,b]$ for all large $n$.
''')

claim('2.3', 'CLT for LSS', [10,11], r'''
Let $f_1,\ldots,f_\kappa$ be functions on $\mathbb R$ analytic on an open interval containing $[\liminf_n\lambda_{\min}^{\boldsymbol\Sigma_n\Theta_n}I_{(0,1)}(y)(1-\sqrt y)^2,\limsup_n\lambda_{\max}^{\boldsymbol\Sigma_n\Theta_n}(1+\sqrt y)^2]$. Under Assumptions A-D, we have that the $\kappa$ dimensional random vector $(L^c(f_j,\mathbf S_n\Theta_n))_{j=1}^\kappa$ is tight and converges weakly to a Gaussian vector $(X_{f_j})_{j=1}^\kappa$. The respective expectation is
\[
\mathrm EX_f=-\frac1{2\pi i}\oint f(z)\left\{
\frac{y\int\frac{\underline m^3(z)t^2}{(\underline m(z)t+1)^3}\,dH(t)}{\left(1-y\int\frac{\underline m^2(z)t^2}{(\underline m(z)t+1)^2}\,dH(t)\right)^2}
+\frac{\underline m^3(z)a(z)}{1-y\int\frac{\underline m^2(z)t^2}{(\underline m(z)t+1)^2}\,dH(t)}\right\}dz,\tag{2.4}
\]
while the covariance is given by
\[
\begin{aligned}
\operatorname{Cov}(X_f,X_g)
={}&-\frac1{2\pi^2}\oint\oint f(z_1)g(z_2)\left(\frac{\frac{d\underline m(z_1)}{dz_1}\frac{d\underline m(z_2)}{dz_2}}{(\underline m(z_2)-\underline m(z_1))^2}-\frac1{(z_1-z_2)^2}\right)dz_1dz_2\\
&-\frac1{4\pi^2}\oint\oint f(z_1)g(z_2)\frac{\partial^2\underline m(z_1)\underline m(z_2)d_2(z_1,z_2)}{\partial z_2\partial z_1}\,dz_1dz_2,\tag{2.5}
\end{aligned}
\]
where $f,g\in\{f_1,\ldots,f_\kappa\}$. The limiting parameters can be expressed as follows by denoting $\mathbb T_n^{(1)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z)=\boldsymbol\Theta_n^{1/2}(\underline m(z)\Psi_n+\mathbf I_p)^{-1}\boldsymbol\Theta_n^{1/2}$ and $\mathbb T_n^{(2)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z)=\boldsymbol\Theta_n^{1/2}(\underline m(z)\Psi_n+\mathbf I_p)^{-2}\boldsymbol\Theta_n^{1/2}$:
\[
\begin{aligned}
a(z)={}&\lim_{n\to\infty}n^{-1}\mathcal I_2\big(\mathbb T_n^{(1)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z),\mathbb T_n^{(2)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z),\boldsymbol\Sigma_n,\mathbb P_n\big)\\
&+(\nu_4-3)\lim_{n\to\infty}n^{-1}\mathcal{II}\big(\mathbb T_n^{(1)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z),\mathbb T_n^{(2)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z),\boldsymbol\Sigma_n,\mathbb P_n\big).
\end{aligned}
\]
\[
\begin{aligned}
d_2(z_1,z_2)={}&\lim_{n\to\infty}n^{-1}\mathcal I_2\big(\mathbb T_n^{(1)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z_1),\mathbb T_n^{(1)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z_2),\boldsymbol\Sigma_n,\mathbb P_n\big)\\
&+(\nu_4-3)\lim_{n\to\infty}n^{-1}\mathcal{II}\big(\mathbb T_n^{(1)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z_1),\mathbb T_n^{(1)}(\Theta_n,\boldsymbol\Sigma_n,\mathbb P_n,z_2),\boldsymbol\Sigma_n,\mathbb P_n\big).
\end{aligned}
\]
Moreover, both in equation (2.4) and (2.5), the contours are closed and taken in the positive direction in the complex plane. Each contour encloses the support of $F^{y,H}$, with the two contours in equation (2.5) assumed to be nonoverlapping.
''')

claim('3.1', 'Test statistics', [13], r'''
Under $H_0$, we have
\[
\sigma_L^{-1}(\mathcal T_L-\mu_L)\to N(0,1),\qquad p/n\in(0,1),
\]
\[
\sigma_F^{-1}(\mathcal T_F-\mu_F)\to N(0,1),
\]
where
\[
\mu_L=n(y_n-1)\log(1-y_n)-p+\frac{\log(1-y_n)}2-\frac{y_na_{\mathbb P,\boldsymbol\Sigma}}2,
\]
\[
\mu_F=py_n+y_n(a_{\mathbb P,\Sigma}+1),
\]
\[
\sigma_L^2=-2\log(1-y_n)+y_na_{\mathbb P,\Sigma},\qquad\sigma_F^2=4y_n^2+4y_n^3(a_{\mathbb P,\Sigma}+2).
\]
''')


def main():
    pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,
        title='Spectral analysis of gram matrices with missing at random observations: Convergence, central limit theorems, and applications in statistical inference',
        authors=['Huiqin Li','Guangming Pan','Yanqing Yin','Wang Zhou'],
        version='Published version, The Annals of Statistics 52(3), 2024, pp. 1254-1275',
        source_url='https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-3/Spectral-analysis-of-gram-matrices-with-missing-at-random-observations/10.1214/24-AOS2392.pdf',
        pdf_pages=22,pdf_sha256=SHA,main_text_last_pdf_page=22,
        main_text_boundary=dict(location='No appendix body occurs in the published PDF. Section 5 ends with Lemma 5.3 on PDF page 21, followed by acknowledgments, funding and an external-supplement notice (10.1214/24-AOS2392SUPP). References end on PDF page 22 at reference [19]. The supplementary PDF is excluded and was not opened.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Registered local published PDF, all 22 pages; external supplementary material excluded.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    if args.output_dir: ROOT=args.output_dir.resolve()
    main()
