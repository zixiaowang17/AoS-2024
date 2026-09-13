"""Reproduce six original Theorem statements from the registered arXiv v2.

Execution restores a transcription; it does not perform a new source review.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p1873'
SHA='07b147d0cefdb1058c0f2d94e9ba1b98f5fd65cddc6dfde6667d9a80194bb1a5'
URL='https://arxiv.org/pdf/2207.06107v2'
NUMBERS=['1.9','1.11','1.17','1.18','1.20','5.3']
PAGES=[[5,6],[7],[9],[9],[10],[29]]
STATEMENTS=[r'''Under Assumptions 1.6 and 1.7, the following convergence holds in probability: For any fixed integer $\ell>0$, we have the convergence in moment of $\mu_N$ to $\mu_1\boxplus\cdots\boxplus\mu_k$,
\[
\int x^\ell d\mu_N-\int x^\ell d\mu_1\boxplus\cdots\boxplus\mu_k\overset{\mathbb P}{\longrightarrow}0.
\]
(14)
Further, we have the following convergence in probability in two special cases

Case 1: $k\sim1$, $p_t\sim N$ for all $t\in[[k]]$
\[
\mu_N\overset{\mathbb P}{\Longrightarrow}\mu_\boxplus^\infty:=\mu_1^\infty\boxplus\cdots\boxplus\mu_k^\infty,\qquad\mu_t^\infty\sim\operatorname{Ber}(\hat y_t).
\]
(15)
Case 2: $k\gg1$, $p_t\leq N^{1-\epsilon}$ for some small constant $\epsilon>0$ for all $t\in[[k]]$
\[
\mu_N\overset{\mathbb P}{\Longrightarrow}\mu_{\mathrm{mp},\hat y}:=\frac{\sqrt{([(1+\sqrt{\hat y})^2-x][x-(1-\sqrt{\hat y})^2])_+}}{2x}\,dx+(1-\hat y)_+\delta_0.
\]
(16)
Here $A_N\overset{\mathbb P}{\Longrightarrow}A$ means $A_N$ converge weakly to $A$ in probability, and the notations $\sim$ and $\gg$ are introduced in Section 1.5.''',r'''Recall $\mu_\boxplus=\mu_1\boxplus\cdots\boxplus\mu_k$ and $m_\boxplus$ its Stieltjes transform. If $\hat y\in(0,1)$ and $f$ is analytic inside $\gamma_1^0$ and $\gamma_2^0$, under Assumptions 1.6 and 1.7, we have
\[
\frac{\operatorname{Tr}f(H)-N\int f(x)d\mu_\boxplus(x)-a_f}{\sigma_f}\Rightarrow\mathcal N(0,1)
\]
(19)
if $\sigma_f^2>c$ with some small constant $c>0$. Here
\[
a_f=-\frac1{4\pi i}\oint_{\gamma_1^0}f(z)\left[\sum_{t=1}^k\frac{\omega_t''(z)}{\omega_t'(z)}+(k-1)\left(\frac{2m_\boxplus'(z)}{m_\boxplus(z)}-\frac{m_\boxplus''(z)}{m_\boxplus'(z)}\right)\right]dz
\]
(20)
and
\[
\sigma_f^2=-\frac1{2\pi^2}\oint_{\gamma_1^0}\oint_{\gamma_2^0}f(z_1)f(z_2)\left[\sum_{t=1}^k\frac{\omega_t'(z_1)\omega_t'(z_2)}{(\omega_t(z_1)-\omega_t(z_2))^2}-\frac1{(z_1-z_2)^2}-\frac{(k-1)m_\boxplus'(z_1)m_\boxplus'(z_2)}{(m_\boxplus(z_1)-m_\boxplus(z_2))^2}\right]dz_2dz_1.
\]
(21)
The same result holds if $\hat y\in(0,\infty)$ with $\gamma_1^0$ and $\gamma_2^0$ replaced by $\gamma_1$ and $\gamma_2$, respectively.''',r'''Denote by $m_y$ the Stieltjes transform of $\mu_{\mathrm{mp},y}$. Let $p_{\max}\leq N^{1/2-\epsilon}$ for any given (small) constant $\epsilon>0$, and $f$ is analytic inside $\gamma_1^0$ and $\gamma_2^0$. Under Assumptions 1.6 and 1.7, we have
\[
\frac{\operatorname{Tr}f(H)-N\int f(x)d\mu_{\mathrm{mp},y}-a_f}{\sigma_f}\Rightarrow\mathcal N(0,1)
\]
if $\sigma_f^2>c$ with some small constant $c>0$, where
\[
a_f=\frac1{2\pi i}\oint_{\gamma_1^0}f(z)\left[-\sum_{t=1}^k\frac{Ny_t^2}{1-y_t}\frac{m_y(z)m_y'(z)}{(1+m_y(z))^3}+y\frac{(m_y'(z))^2-m_y^2(z)m_y'(z)}{m_y(z)(1+m_y(z))^3}\right]dz
\]
and
\[
\sigma_f^2=-\frac1{2\pi^2}\oint_{\gamma_1^0}\oint_{\gamma_2^0}f(z_1)f(z_2)\left[\frac{m_y'(z_1)m_y'(z_2)}{(m_y(z_1)-m_y(z_2))^2}-\frac1{(z_1-z_2)^2}-\frac{ym_y'(z_1)m_y'(z_2)}{(1+m_y(z_1))^2(1+m_y(z_2))^2}\right]dz_2dz_1.
\]
The same result holds if $\hat y\in(0,\infty)$ with $\gamma_1^0$ and $\gamma_2^0$ replaced by $\gamma_1$ and $\gamma_2$, respectively.''',r'''Let $\hat H:=\hat Y'\cdot\operatorname{diag}((\hat Y_i\hat Y_i')^{-1})_{i=1}^k\cdot\hat Y$ be the matrix which has the same non-zero eigenvalues as $\hat B$. Further let $\tilde\mu_\boxplus=\tilde\mu_1\boxplus\cdots\boxplus\tilde\mu_k$ with $\tilde\mu_t\sim\operatorname{Ber}(p_t/(N-1))$ and $\tilde m_\boxplus$ its Stieltjes transform. If $\hat y\in(0,1)$ and $f$ is analytic inside $\gamma_1^0$ and $\gamma_2^0$, under Assumptions 1.6 and 1.7, we have
\[
\frac{\operatorname{Tr}f(\hat H)-(N-1)\int f(x)d\tilde\mu_\boxplus(x)-\tilde a_f}{\tilde\sigma_f}\Rightarrow\mathcal N(0,1)
\]
if $\tilde\sigma_f^2>c$ with some small constant $c>0$, where
\[
\tilde a_f=-\frac1{4\pi i}\oint_{\gamma_1^0}f(z)\left[\sum_{t=1}^k\frac{\tilde\omega_t''(z)}{\tilde\omega_t'(z)}+(k-1)\left(\frac{2\tilde m_\boxplus'(z)}{\tilde m_\boxplus(z)}-\frac{\tilde m_\boxplus''(z)}{\tilde m_\boxplus'(z)}\right)-\frac1z\right]dz
\]
and
\[
\tilde\sigma_f^2=-\frac1{2\pi^2}\oint_{\gamma_1^0}\oint_{\gamma_2^0}f(z_1)f(z_2)\left[\sum_{t=1}^k\frac{\tilde\omega_t'(z_1)\tilde\omega_t'(z_2)}{(\tilde\omega_t(z_1)-\tilde\omega_t(z_2))^2}-\frac1{(z_1-z_2)^2}-\frac{(k-1)\tilde m_\boxplus'(z_1)\tilde m_\boxplus'(z_2)}{(\tilde m_\boxplus(z_1)-\tilde m_\boxplus(z_2))^2}\right]dz_2dz_1,
\]
Here $\tilde\omega_t(z)$, $t\in[[k]]$ are the subordination functions determined by Proposition 1.5 with $\mu_t\equiv\tilde\mu_t$.

The same result holds if $\hat y\in(0,\infty)$ with $\gamma_1^0$ and $\gamma_2^0$ replaced by $\gamma_1$ and $\gamma_2$, respectively. In addition, Corollaries 1.14 and 1.15 still hold if we replace $B$ by $\hat B$ and $N$ by $N-1$ simultaneously.''',r'''Theorems 1.11, 1.17, 1.18 and Corollaries 1.14, 1.15 still hold under Assumptions 1.19 and 1.7.''',r'''Let $\hat y\in(0,1)$ and $f$ be analytic inside $\gamma_1^0$ and $\gamma_2^0$. Denote by
\[
\alpha_t(z)=\mathbb E^\chi[\operatorname{tr}(X_tX_t')^{-1}-\operatorname{tr}Q_tG(z)],\qquad\beta_t(z)=\frac1{1-y_t}\mathbb E^\chi[\operatorname{tr}G(z)-\operatorname{tr}P_tG(z)],
\]
(88)
for all $t\in[[k]]$. Under Assumptions 1.6 and 1.7, we have
\[
\frac{\operatorname{Tr}f(H)-\oint_{\bar\gamma_1^0}\mathbb E^\chi[\operatorname{Tr}G(z)]f(z)dz}{\sigma_f}\Rightarrow\mathcal N(0,1)
\]
with
\[
\sigma_f^2=-\frac1{2\pi^2}\oint_{\bar\gamma_1^0}\oint_{\bar\gamma_2^0}\mathcal K(z_1,z_2)f(z_1)f(z_2)dz_2dz_1,
\]
(89)
and
\[
\mathcal K(z_1,z_2)=\left(z_1-\sum_{s=1}^k\frac{\alpha_s(z_1)}{1+\alpha_s(z_1)+\beta_s(z_1)}\right)^{-1}\sum_{t=1}^k\mathbb E^\chi\left[\partial_{z_2}\frac{\operatorname{tr}Q_tG(z_1)P_tG(z_2)-\operatorname{tr}Q_tG(z_1)G(z_2)}{1+\alpha_t(z_1)+\beta_t(z_1)}\right].
\]
(90)
The same result holds if $\hat y\in(0,\infty)$ with $\gamma_1^0$ and $\gamma_2^0$ replaced by $\gamma_1$ and $\gamma_2$, respectively.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; original statement, including continuation where present') for p in pages]) for i,(n,s,pages) in enumerate(zip(NUMBERS,STATEMENTS,PAGES),1)]
    paper=dict(paper_id=PID,title='Spectral statistics of sample block correlation matrices',authors=['Zhigang Bao','Jiang Hu','Xiaocong Xu','Xiaozhuo Zhang'],version='arXiv:2207.06107v2; arXiv stamp 8 Sep 2022',pdf_pages=103,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=34,main_text_boundary=dict(location='Main text ends after equation (110) and the final sentence of the proof of Theorem 1.11 on PDF page 34. Appendix A starts at y=189.4245; retained page-34 evidence is clipped at y=188.4. Appendix bodies are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Inspected all main-text pages and actual bold Theorem headings. Visually compared six complete statements, including Theorem 5.3 within Section 5. Citations, proof headings, Corollaries, Propositions, Lemmas and appendices are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v2; no replacement source or appendix-body reading.',normalization_policy='Preserve original wording, formulas, cases and source irregularities. Normalize PDF wrapping and mathematical typesetting only; no silent repairs or expanded hypotheses.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved six complete original main-text Theorems; independent inventory review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
