"""Reproduce the two original Theorems, numbered 1 and 3, from the registered v2 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2956'
SHA='e420717c6358810eb3b7c93be605b04cae37bc69c06e635263ff90d11c02884d'
URL='https://arxiv.org/pdf/2401.06446v2'
NUMBERS=['1','3']
PAGES=[[7,8],[9]]
STATEMENTS=[r'''Suppose Condition A holds. When $0\le\eta<\infty$, there is a solution $\hat\omega$ to the estimating equations $\psi(\omega)=\boldsymbol0_{[(p+5):1]}$, satisfying $|\boldsymbol K^{1/2}(\hat\omega-\dot\omega)|=O_p(1)$, where $\boldsymbol K=\operatorname{diag}(g\boldsymbol I_{p_a+2},h\boldsymbol I_{p_b+1},gh\boldsymbol I_{p_{ab}+1},n\boldsymbol I_{p_w+1})$ where $\boldsymbol I_p$ is the $p\times p$ identity matrix. Moreover, $\hat\omega$ has the asymptotic representation
\[
\boldsymbol K^{1/2}(\hat\omega-\dot\omega)=\boldsymbol B^{-1}\boldsymbol K^{-1/2}\phi+o_p(1),\tag{9}
\]
where $\boldsymbol B$ is given by (13), and $\phi=[\phi_{\xi_0},\phi_{\boldsymbol\xi_1}^T,\phi_{\sigma_\alpha^2},\phi_{\boldsymbol\xi_2}^T,\phi_{\sigma_\beta^2},\phi_{\boldsymbol\xi_3}^T,\phi_{\sigma_\gamma^2},\phi_{\boldsymbol\xi_4}^T,\phi_{\sigma_e^2}]^T$ has components
\[
\begin{aligned}
\phi_{\xi_0}&=\frac1{\dot\tau}\left(\sum_{i=1}^g\alpha_i+\eta\sum_{j=1}^h\beta_j\right),\\
\phi_{\boldsymbol\xi_1}&=\frac1{\dot\sigma_\alpha^2}\sum_{i=1}^g\left(\boldsymbol x_i^{(a)}-\frac{\eta\dot\sigma_\beta^2}{\dot\tau}\bar{\boldsymbol x}^{(a)}\right)\alpha_i+\frac\eta{\dot\tau}\bar{\boldsymbol x}^{(a)}\sum_{j=1}^h\beta_j,\\
\phi_{\sigma_\alpha^2}&=\frac1{2\dot\sigma_\alpha^4}\sum_{i=1}^g(\alpha_i^2-\dot\sigma_\alpha^2),\\
\phi_{\boldsymbol\xi_2}&=\frac1{\dot\sigma_\beta^2}\sum_{j=1}^h\left(\boldsymbol x_j^{(b)}-\frac{\dot\sigma_\alpha^2}{\dot\tau}\bar{\boldsymbol x}^{(b)}\right)\beta_j+\frac1{\dot\tau}\bar{\boldsymbol x}^{(b)}\sum_{i=1}^g\alpha_i,\\
\phi_{\sigma_\beta^2}&=\frac1{2\dot\sigma_\beta^4}\sum_{j=1}^h(\beta_j^2-\dot\sigma_\beta^2),\\
\phi_{\boldsymbol\xi_3}&=\frac1{\dot\sigma_\gamma^2}\sum_{i=1}^g\sum_{j=1}^h\boldsymbol x_{ij(c)}^{(ab)}\gamma_{ij},\\
\phi_{\sigma_\gamma^2}&=\frac1{2\dot\sigma_\gamma^4}\sum_{i=1}^g\sum_{j=1}^h(\gamma_{ij}^2-\dot\sigma_\gamma^2),\\
\phi_{\boldsymbol\xi_4}&=\frac1{\dot\sigma_e^2}\sum_{i=1}^g\sum_{j=1}^h\sum_{k=1}^m\boldsymbol x_{ijk(c)}^{(w)}e_{ijk},\\
\phi_{\sigma_e^2}&=\frac1{2\dot\sigma_e^4}\sum_{i=1}^g\sum_{j=1}^h\sum_{k=1}^m(e_{ijk}^2-\dot\sigma_e^2).
\end{aligned}\tag{10}
\]
It follows that
\[
\boldsymbol K^{1/2}(\hat\omega-\dot\omega)\xrightarrow{D}N(\boldsymbol0,\boldsymbol F),
\]
where
\[
\boldsymbol F=\operatorname{diag}\left(\begin{bmatrix}\boldsymbol F_{1(a),(a)}&\boldsymbol F_{1(a),(b)}\\\boldsymbol F_{1(b),(a)}&\boldsymbol F_{1(b),(b)}\end{bmatrix},\boldsymbol F_2,\boldsymbol F_3\right),
\]
with
\[
\boldsymbol F_{1(a),(a)}=\begin{bmatrix}
f_1&-\dot\sigma_\alpha^2\boldsymbol f_2&\mathbb E\alpha_1^3\\
-\dot\sigma_\alpha^2\boldsymbol f_2^T&\dot\sigma_\alpha^2\boldsymbol D_1^{-1}&\boldsymbol0_{[p_a:1]}\\
\mathbb E\alpha_1^3&\boldsymbol0_{[1:p_a]}&\mathbb E\alpha_1^4-\dot\sigma_\alpha^4
\end{bmatrix},
\]
\[
\boldsymbol F_{1(a),(b)}=\boldsymbol F_{1(b),(a)}^T=\begin{bmatrix}
-\eta^{1/2}\dot\sigma_\beta^2\boldsymbol f_3&\eta^{1/2}\mathbb E\beta_1^3\\
\boldsymbol0_{[p_a:p_b]}&\boldsymbol0_{[p_b:1]}\\
\boldsymbol0_{[1:p_b]}&0
\end{bmatrix},
\]
\[
\boldsymbol F_{1(b),(b)}=\begin{bmatrix}
\dot\sigma_\beta^2\boldsymbol D_2^{-1}&\boldsymbol0_{[p_b:1]}\\
\boldsymbol0_{[1:p_b]}&\mathbb E\beta_1^4-\dot\sigma_\beta^4
\end{bmatrix},\qquad
\boldsymbol F_2=\begin{bmatrix}
\dot\sigma_\gamma^2\boldsymbol D_3^{-1}&\boldsymbol0_{[p_{ab}:1]}\\
\boldsymbol0_{[1:p_{ab}]}&\mathbb E\gamma_{11}^4-\dot\sigma_\gamma^4
\end{bmatrix}
\]
and
\[
\boldsymbol F_3=\begin{bmatrix}
\dot\sigma_e^2\boldsymbol D_4^{-1}&\boldsymbol0_{[p_w:1]}\\
\boldsymbol0_{[1:p_w]}&\mathbb Ee_{111}^4-\dot\sigma_e^4
\end{bmatrix},
\]
$f_1=\dot\tau+\dot\sigma_\alpha^2\bar{\boldsymbol x}^{(a)T}\boldsymbol D_1^{-1}\bar{\boldsymbol x}^{(a)}+\eta\dot\sigma_\beta^2\bar{\boldsymbol x}^{(b)T}\boldsymbol D_2^{-1}\bar{\boldsymbol x}^{(b)}$, $\boldsymbol f_2=\bar{\boldsymbol x}^{(a)T}\boldsymbol D_1^{-1}$ and $\boldsymbol f_3=\bar{\boldsymbol x}^{(b)T}\boldsymbol D_2^{-1}$. The result for $\eta=\infty$ can be obtained from that for $\eta=0$ by reordering the parameter vector as $\omega=[\boldsymbol\xi_1^T,\sigma_a^2,\xi_0,\boldsymbol\xi_2^T,\sigma_\beta^2,\boldsymbol\xi_3^T,\sigma_\gamma^2,\boldsymbol\xi_4^T,\sigma_e^2]^T$ and making the same replacements in the asymptotic coavriate matrix.''',
r'''Suppose Condition A holds. Then there is a solution $\hat\omega_R$ of the REML estimating equations satisfying $|\boldsymbol K^{1/2}(\hat\omega_R-\dot\omega)|=O_p(1)$ and
\[
\boldsymbol K^{1/2}(\hat\omega_R-\hat\omega)=o_p(1),
\]
so Theorem 1 applies to the REML estimator.''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — original statement'+(' continued' if j else '')) for j,p in enumerate(ps)]) for i,(n,ps,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Increasing dimension asymptotics for two-way crossed mixed effect models',authors=['Ziyang Lyu','S.A. Sisson','A.H. Welsh'],version='arXiv:2401.06446v2, stamped 13 March 2024; submitted manuscript',pdf_pages=25,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=21,main_text_boundary=dict(location='Section 7 Discussion ends on PDF page 21 before Appendix A at y=538.64. Main-text evidence on that page is clipped at y=534; all appendix bodies and the separate supplementary material are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Independently enumerate actual uppercase small-cap THEOREM headings across the main text, including the main-text proof sections. Exactly Theorems 1 and 3 occur; result 2 is a Corollary. Visually compare the full Theorem 1 continuation with its covariance matrices and the complete Theorem 3.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v2 PDF pinned by SHA-256; main text ends on page 21 before Appendix A. All appendix bodies are excluded from census evidence.',normalization_policy='Normalize line wrapping and mathematical typesetting only. Preserve source numbering 1 and 3, all influence components and covariance blocks, and the printed zero-block dimension, sigma_a notation and coavriate spelling. Record source discrepancies separately rather than correcting quotations.'),papers=[paper],claims=cs)
def main():
    p=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved both original main-text Theorems; independent inventory review remains separate.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path);a=ap.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
