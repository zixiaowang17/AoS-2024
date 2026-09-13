"""Rebuild the manually transcribed inventory from the registered published PDF.

This script verifies source identity; it does not certify a new source review.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p / 'scripts/resolve_paper_pdf.py').is_file())
PID = 'aos-2024-v52-i03-p1201'
SHA = 'cc68ba81b23d7f19b5352aa1f2a4ef4602b9e969d0ffc5458813f2c623ca0f7c'
claims = []


def claim(number, page, statement):
    claims.append(dict(
        claim_id=f'{PID}/T{number}', paper_id=PID, claim_kind='theorem',
        label=f'Theorem {number}', source_order=len(claims) + 1,
        statement_original=statement.strip(),
        evidence=[dict(page=page, location=f'Theorem {number}, complete printed statement')]))


claim('3.2', 7, r'''
Let $m$ be any positive integer no greater than the dimension of $\mathfrak M_{\sigma\{\boldsymbol f^0(X)\}}$, which can be infinite. If $\boldsymbol f^*$ is an optimal solution of the following objective function
\[
\begin{aligned}
\max_{\boldsymbol f\in\{L_2(P_X)\}^m}\;&-E\big([\boldsymbol f(X)-E\{\boldsymbol f(X)\}]^\top[\boldsymbol f(\widetilde X)-E\{\boldsymbol f(\widetilde X)\}]\kappa(Y,\widetilde Y)\big)\\
\text{subject to}\;&\operatorname{Var}\{\boldsymbol f(X)\}=I_m,
\end{aligned}\tag{6}
\]
then $f_j^*\in\mathfrak M_{\sigma\{\boldsymbol f^0(X)\}}$ for all $1\le j\le m$. By Lemma 1 in [26], the GMDD matrix
\[
-E\big([\boldsymbol f^*(X)-E\{\boldsymbol f^*(X)\}][\boldsymbol f^*(\widetilde X)-E\{\boldsymbol f^*(\widetilde X)\}]^\top\kappa(Y,\widetilde Y)\big)
\]
is positive semidefinite and thus diagonalizable via an orthogonal matrix. Thereafter, unless otherwise emphasized, we always select $\boldsymbol f^*$ to diagonalize the GMDD matrix and rearrange $f_j^*$ such that its negative GMDD value is nondecreasing. That is to say, for $1\le i<j\le m$,
\[
\lambda_i^*=E\{\bar f_i^*(X)\bar f_i^*(\widetilde X)\kappa(Y,\widetilde Y)\}\le E\{\bar f_j^*(X)\bar f_j^*(\widetilde X)\kappa(Y,\widetilde Y)\}=\lambda_j^*\le0,
\]
where $\bar f_i^*(X)=f_i^*(X)-E\{f_i^*(X)\}$.
''')

claim('3.7', 10, r'''
Under the assumption (A1), the solution of the successive direction extraction method is proportional to the optimal direction $f_j^*$ given in Theorem 3.2 or (7), that is,
\[
f^*_{j,\mu_j}=\pm\sqrt{1-\frac{\lambda_j^*}{2\mu_j}}f_j^*,\qquad1\le j\le d.
\]
''')

claim('3.8', 11, r'''
Let $\mu>0$ and $\boldsymbol f^*_{\mu,F}$ be an optimal solution of
\[
\min_{\boldsymbol f\in\{L_2(P_X)\}^d}L_F(\mu,\boldsymbol f),
\]
then $f^*_{\mu,F,j}\in\mathfrak M_{\sigma\{\boldsymbol f^0(X)\}}$ for all $1\le j\le d$. If we further assume $\mu>|\lambda_1^*+\cdots+\lambda_d^*|$, the minimization of $L_F(\mu,\boldsymbol f)$ is equivalent to (6) in Theorem 3.2.
''')

claim('4.2', 14, r'''
Under the assumption (A1), (A2) and (A4), if $n\ge V$, for any $\delta>0$ with probability at least $1-\delta$, it holds that
\[
L_1(\mu_1,\hat f_{1,\mu_1})-L_1(\mu_1,f^*_{1,\mu_1})=\mathcal O\left(\sqrt{\frac Vn}+\sqrt{\frac{\log(1/\delta)}{n-3}}+\inf_{f_1\in\mathcal F_n}\|f_1-f^*_{1,\mu_1}\|_\infty^2\right).
\]
''')

claim('4.4', 16, r'''
Under the assumption (A1), (A2) and (A4), the following holds for any $\delta>0$ with probability at least $1-\delta$,
\[
L_1(\mu_1,\hat f_{1,\mu_1})-L_1(\mu_1,f^*_{1,\mu_1})=\mathcal O\left(\frac Vn\log\frac nV+\frac{V\log(1/\delta)}n+\inf_{f_1\in\mathcal F_n}\|f_1-f^*_{1,\mu_1}\|_\infty^2\right),
\]
\[
\rho^2(\hat f_{1,\mu_1},f^*_{1,\mu_1})=\mathcal O\left(\frac Vn\log\frac nV+\frac{V\log(1/\delta)}n+\inf_{f_1\in\mathcal F_n}\|f_1-f^*_{1,\mu_1}\|_\infty^2\right).
\]
''')

claim('4.6', 17, r'''
Under the same assumptions of Theorem 4.4, the following holds for any $\delta>0$ with probability at least $1-(4j-3)\delta$,
\[
L_j(\mu_j,(\boldsymbol f^*_{[j-1]},\hat f_{j,\mu_j}))-L_j(\mu_j,(\boldsymbol f^*_{[j-1]},f^*_{j,\mu_j}))=R_j(\mu_j,\hat f_{j,\mu_j})=\mathcal O(A(n,V,\delta)),
\]
\[
\rho^2(\hat f_{j,\mu_j},f^*_{j,\mu_j})=\mathcal O(A(n,V,\delta)),
\]
where
\[
A(n,V,\delta)=\frac Vn\log\frac nV+\frac{V\log(1/\delta)}n+\sup_{1\le j\le d}\inf_{f_j\in\mathcal F_n}\|f_j-f^*_{j,\mu_j}\|_\infty^2.
\]
Therefore, we can derive the following result by summing up the $R_j$,
\[
R(\boldsymbol\mu,\hat{\boldsymbol f})=\sum_{j=1}^d R_j(\mu_j,\hat f_{j,\mu_j})=\mathcal O\left(\frac Vn\log\frac nV+\frac{V\log(1/\delta)}n+\sup_{1\le j\le d}\inf_{f_j\in\mathcal F_n}\|f_j-f^*_{j,\mu_j}\|_\infty^2\right).
\]
Moreover, if the assumptions in Corollary 4.5 hold true, then
\[
E\rho^2(\hat f_{j,\mu_j},f^*_{j,\mu_j})=\mathcal O(n^{-\frac{2\beta}{p+2\beta}}\log^2n),
\]
for $1\le j\le d$.
''')


def main():
    pdf = Path(subprocess.check_output(
        [sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == SHA
    paper = dict(
        paper_id=PID, title='Deep nonlinear sufficient dimension reduction',
        authors=['Yinfeng Chen', 'Yuling Jiao', 'Rui Qiu', 'Zhou Yu'],
        version='Published version, The Annals of Statistics 52(3), 2024, pp. 1201-1226',
        source_url='https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-3/Deep-nonlinear-sufficient-dimension-reduction/10.1214/24-AOS2390.pdf',
        pdf_pages=26, pdf_sha256=SHA, main_text_last_pdf_page=26,
        main_text_boundary=dict(
            location='The published PDF has no appendix body. Main-text figures, acknowledgments and funding end on PDF page 23; the supplementary-material paragraph there only describes an external supplement (10.1214/24-AOS2390SUPP). References end on PDF page 26 at reference [56]. The external supplement is excluded and was not opened.',
            shared_page_with_appendix=False),
        intake_review=dict(status='complete', theorem_ids=[c['claim_id'] for c in claims],
                           zero_theorems_confirmed=False))
    inventory = dict(schema_version='statistical-theorem-inventory-v1',
        scope=dict(theorem_scope='main_text_only', source_policy='Registered local published PDF, all 26 pages; external supplementary material excluded.'),
        papers=[paper], claims=claims)
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'theorem-inventory.json').write_text(json.dumps(inventory, indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    if args.output_dir:
        ROOT = args.output_dir.resolve()
    main()
