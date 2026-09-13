"""Reproduce all four original main-text Theorems from the registered p2851 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2851'
SHA='4bda627723eeb56867d4300b59258645798e8b9fab2d3d4d3fef067b5de8474e'
URL='https://arxiv.org/pdf/2211.02039v4'
NUMBERS=['4','5','6','7']
PAGES=[[18],[19],[21,22],[23]]
STATEMENTS=[r'''Let $\mathcal P_0$ denote a class of null distributions, i.e. that satisfy $\mathbb E_P(Y\mid X,Z)=\mathbb E_P(Y\mid Z)$ for $P\in\mathcal P_0$, and suppose that Assumption 3 holds for $\mathcal P_0$. Suppose in addition that
(a) $\sup_{P\in\mathcal P_0}\mathbb P_P(\sigma_P^2=0)=o(1)$;
(b) there exists $\delta\in(0,2]$ such that $\mathbb E_P(|\varepsilon_P\xi_P|^{2+\delta}\mid\hat f)/\sigma_P^{2+\delta}=o_{\mathcal P_0}(n^{\delta/2})$;
(c) there exists $c>0$ such that $\inf_{P\in\mathcal P_0}\mathbb E_P(\varepsilon_P^2\mid X,Z)\ge c$;
and any of the following hold:
(i) $T$ is computed using Algorithm 2;
(ii) $T$ is computed using Algorithm 1 and $Y\perp\!\!\!\perp X\mid Z$ for all $P\in\mathcal P_0$;
(iii) $T$ is computed using Algorithm 1 and $\hat m$ is a linear smoother;
(iv) $T$ is computed using Algorithm 1 and $\hat m$ is a sufficiently stable estimator.
Then
\[
\sup_{P\in\mathcal P_0}\sup_{t\in\mathbb R}|\mathbb P_P(T\le t)-\Phi(t)|\to0.
\]''',r'''Suppose that Assumption 3 holds over a class of alternative distributions $\mathcal P_1$. Let $(\epsilon_n)_{n\in\mathbb N}$ be a positive sequence and let
\[
\mathcal P_1(\epsilon_n):=\{P\in\mathcal P_1:\tau_P\ge\epsilon_n\}.
\]
Assume that
(a) $\hat m_{\hat f}$ is scale equivariant in the sense that $\hat m_{a\cdot\hat f}(Z)=a\cdot\hat m_{\hat f}(Z)$ for all $a>0$;
(b) $\sup_{P\in\mathcal P_1}h_P(X,Z)\le C$;
(c) $\epsilon_n\cdot n\to\infty$;
(d) There exists $\rho>0$ such that
\[
\sup_{P\in\mathcal P_1(\epsilon_n)}\mathbb P_P\left(\operatorname{Corr}_P(h_P(X,Z),\xi_P\mid\hat f)\le\rho\right)=o(1).
\]
Suppose further that either
(i) $T$ is computed using Algorithm 2;
(ii) $T$ is computed using Algorithm 1 and $\hat m$ is sufficiently stable.
Then for any $\alpha\in(0,1)$,
\[
\inf_{P\in\mathcal P_1(\epsilon_n)}\mathbb P_P(T>z_{1-\alpha})\to1.
\]''',r'''Suppose that Assumption 4 holds for a class of null distributions $\mathcal P_0$, i.e. a class of distributions that also satisfies $\mathbb E_P(Y\mid X,Z)=\mathbb E_P(Y\mid Z)$ for every $P\in\mathcal P_0$. Assume that $\sup_{P\in\mathcal P_0}\mathbb P_P(\|\Pi\hat\beta\|_\infty=0)=o(1)$ and that $\Lambda_P:=\mathbb E_P\{\operatorname{Cov}_P(\phi(X,Z)\mid Z)\}$ satisfies
\[
\tilde\lambda_{\min}(\Lambda_P):=\min_{x\in\mathbb R^{K_{XZ}}:\Pi x=x,\|x\|_2=1}x^\top\Lambda_Px\ge\frac c{K_{XZ}},\tag{14}
\]
for each $P\in\mathcal P_0$, where $c\in(0,1]$ is taken from Assumption 4. Finally, suppose that
\[
nK_{XZ}\left\{\tilde K_Z^{-2s/d_Z}+\frac{\tilde K_Z}n\right\}^2\to0\tag{15}
\]
and
\[
\frac{K_{XZ}^{1+2/\delta}}n\to0\tag{16}
\]
where $\delta$ is taken from Assumption 4. If $T$ is computed using spline regressions according to either Algorithm 1 or Algorithm 2, then
\[
\sup_{P\in\mathcal P_0}\sup_{t\in\mathbb R}|\mathbb P_P(T\le t)-\Phi(t)|\to0.
\]''',r'''Let $\mathcal P$ be a class of distributions satisfying Assumption 4, and let $\mathcal P_1(\epsilon_n):=\{P\in\mathcal P:\tau_P\ge\epsilon_n\}$, where
\[
\epsilon_n\cdot n^{\frac{4s}{4s+d}}\to\infty.\tag{17}
\]
Further, assume that the tuning parameters are chosen such that $K_X\asymp n^{\frac{2d_X}{4s+d}}$ and $K_Z\asymp\tilde K_Z\asymp n^{\frac{2d_Z}{4s+d}}$ and that $r\ge s\ge3d/4$. If $T$ is computed using spline regressions according to Algorithm 2, then
\[
\inf_{P\in\mathcal P_1(\epsilon_n)}\mathbb P_P(T>z_{1-\alpha})\to1.
\]''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — original statement'+(' continued' if j else '')) for j,p in enumerate(ps)]) for i,(n,ps,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='The projected covariance measure for assumption-lean variable significance testing',authors=['Anton Rask Lundborg','Ilmun Kim','Rajen D. Shah','Richard J. Samworth'],version='arXiv:2211.02039v4, stamped 7 May 2024; title-page date May 8, 2024',pdf_pages=97,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Conclusion ends on28 and Acknowledgements end on29, before References at PDF y=208.141. Main-text crop ends at y=202 on29. References continue through33; supplementary Proofs start34 according to outline. All supplementary/appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Independently enumerate bold CMBX10 theorem headings on main-text pages1–29; visually compare all four original statements, including Theorem6 continuation on22. Exclude Propositions1–3 and8, citations and supplementary theorems.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v4 source, pinned by SHA256. Main text ends before References on29; all supplementary and appendix bodies excluded.',normalization_policy='Preserve all original hypotheses and alternatives, conditional moment/correlation formulas, restricted eigenvalue and rate conditions, and theorem6 continuation. Normalize line wrapping/typesetting only. Preserve one-sided h_P bound in5 and leave appendix-only definitions unresolved in separate notes.'),papers=[paper],claims=cs)
def main():
    p=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved four complete original main-text Theorems; independent review remains separate.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path);a=ap.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
