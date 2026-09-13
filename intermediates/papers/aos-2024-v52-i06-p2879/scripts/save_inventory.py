"""Reproduce all six original main-text Theorems from the registered p2879 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2879'
SHA='5fcce9d2aea751e76487104fb372647430cae702f666881efe642734e50c11df'
URL='https://arxiv.org/pdf/2210.08571v3'
NUMBERS=['1','2','3','4','5','6']
LABELS=['Theorem 1 (Ridge regression)','Theorem 2','Theorem 3 (Ridgeless regression in the overparameterized regime)','Theorem 4 (Ridgeless regression in the underparameterized regime)','Theorem 5','Theorem 6']
PAGES=[[10],[11],[12,13],[13,14],[17],[25]]
STATEMENTS=[r'''Under Assumption 1, for any positive integers $k$ and $D$, there exist constants $\eta=\eta(C_x)\in(0,1/2)$ and $C=C(C_x,D)>0$ such that the following hold. Define $\chi_n(\lambda)$, $\kappa$, $\rho(\lambda)$ as above (with $\eta=\eta(C_x)$ in Eq. (24)).
If it holds that
\[
\chi_n(\lambda)^3\log^2n\le Cn\kappa^{4.5},\qquad n^{-2D+1}=O\left(\sqrt{\frac{\kappa^3\log^2n}{n\max\{1,\lambda\}}}\right),
\]
then for all $n=\Omega_{k,D}(1)$, with probability $1-O_k(n^{-D+1})$ we have:
1. Variance approximation.
\[
|\mathscr V_X(\lambda)-V_n(\lambda)|=O_{k,C_x,D}\left(\frac{\chi_n(\lambda)^3\log^2n}{n^{1-\frac1k}\kappa^{9.5}}\right)\cdot V_n(\lambda).\tag{28}
\]
2. Bias approximation. If we additionally have $\chi_n(\lambda)^3\log^2n\le Cn\kappa^{4.5}\sqrt{\rho(\lambda)}$ and $\lambda kn^{-\frac1k}\le\kappa/2$, for all $n=\Omega_{k,D}(1)$, we have
\[
|\mathscr B_X(\lambda)-B_n(\lambda)|=O_{k,C_x,D}\left(\frac{\lambda_\star(\lambda)^{k+1}}{n\kappa^3}+\frac{\chi_n(\lambda)^3\log^2n}{\sqrt{\rho(\lambda)}n^{1-\frac1k}\kappa^{8.5}}\right)\cdot B_n(\lambda).\tag{29}
\]''',r'''Under Assumption 1, further assume the ‘non-negligible regularization’ condition: namely $\lambda$ is chosen so that $\nu=\lambda/\lambda_\star(\lambda)\in[1/C,1-1/C]$. Define $\tilde d_\Sigma(n):=d_\Sigma(n)(\log d_\Sigma(n))^2$. There exists a constant $\eta$ such that, for some $\epsilon>0$ if $\tilde d_\Sigma(n)\le(\sigma_{2n}/\sigma_{\lfloor\eta n\rfloor})n^{4/3}(\log n)^{-2/3-\epsilon}$, then with probability $1-O(n^{-10})$ we have (suppressing the dependence on $C$, $C'$ and $\epsilon$ in the big-Oh notation):
1. Variance approximation.
\[
|\mathscr V_X(\lambda)-V_n(\lambda)|=O\left(\frac1{n^{0.99}}\left(\frac{\tilde d_\Sigma(n)\sigma_{\lfloor\eta n\rfloor}}{n\sigma_{2n}}\right)^3\right)\cdot V_n(\lambda).
\]
2. Bias approximation. Additionally if $\|\boldsymbol\beta\|_{\boldsymbol\Sigma^{-1}}^2\le C''$, $\tilde d_\Sigma(n)\le(\sigma_{2n}/\sigma_{\lfloor\eta n\rfloor})n^{7/6}(\log n)^{-2/3-\epsilon}$, then we have
\[
|\mathscr B_X(\lambda)-B_n(\lambda)|=O\left(\frac1{n^{0.49}}\left(\frac{\tilde d_\Sigma(n)\sigma_{\lfloor\eta n\rfloor}}{n\sigma_{2n}}\right)^3\right)\cdot B_n(\lambda).
\]''',r'''Suppose Assumption 1 holds with $n<d$. Further assume $\sigma_n>0$, and let $s_{\min}$ be the minimum nonzero eigenvalue of the sample covariance $\hat{\boldsymbol\Sigma}=\boldsymbol X^\top\boldsymbol X/n$. For any positive integers $k$ and $D$, there exist constants $\eta=\eta(C_x)\in(0,1/2)$ and $C_1=C_1(C_x,D)>0$, $C_i=C_i(k,C_x,D)>0$, $i\in\{2,3\}$, such that the following hold, for $\chi'_n(\kappa)$, $\rho(0)$, $C_\Sigma$ as above.
Let $\kappa>0$ be such that the following hold
\[
\kappa\le C_\Sigma^2/8,\qquad\chi'_n(\kappa)^3\log^2n\le C_1n\kappa^{4.5},\qquad n^{-2D+1}=O\left(\sqrt{\frac{\kappa^3\log^2n}{n\max\{1,\kappa\lambda_\star(0)\}}}\right).
\]
Then, on the event $\{s_{\min}\ge8\lambda_\star(0)\kappa\}$, the following hold with probability $1-O_k(n^{-D+1})$:
1. Variance approximation. If in addition $\chi'_n(\kappa)^3\log^2n\le C_2n^{1-\frac1k}\kappa^{9.5}$, then
\[
|\mathscr V_X(0)-V_n(0)|=O_{k,C_x,D}\left(\kappa\cdot\left(\frac{\lambda_\star(0)}{s_{\min}}+\frac1{C_\Sigma^2}\right)+\frac{\chi'_n(\kappa)^3\log^2n}{n^{1-\frac1k}\kappa^{9.5}}\right)\cdot V_n(0).
\]
2. Bias approximation. If in addition $\chi'_n(\kappa)^3\log^2n\le C_1n\kappa^{4.5}\sqrt{\rho(0)}$, $\lambda_\star(0)kn^{-\frac1k}\le1/4$ and
\[
\frac{\lambda_\star(0)^{k+1}}{n\kappa^3}+\frac{\chi'_n(\kappa)^3\log^2n}{\sqrt{\rho(0)}n^{1-\frac1k}\kappa^{8.5}}\le C_3,
\]
then
\[
\begin{aligned}
|\mathscr B_X(0)-B_n(0)|
&=O_{k,C_x,D}\left(\frac\kappa{C_\Sigma^2}+\frac{\lambda_\star(0)^{k+1}}{n\kappa^3}+\frac{\chi'_n(\kappa)^3\log^2n}{\sqrt{\rho(0)}n^{1-\frac1k}\kappa^{8.5}}\right)\cdot B_n(0)\\
&\quad+\min\left\{O\left(\frac{\kappa\lambda_\star(0)\|\boldsymbol\beta\|^2}{s_{\min}}\right),\ O_{C_x,D}(\kappa^2\lambda_\star(0)^2\chi'_n(\kappa)^2)\|\boldsymbol\theta_{\le n}\|^2+O_{C_x,D}(\kappa\lambda_\star(0)\chi'_n(\kappa))\|\boldsymbol\beta_{>n}\|^2\right\}.
\end{aligned}
\]
Finally, for any $\varepsilon>0$, $C_x<\infty$ there exist constants $C_4=C_4(C_x,\varepsilon,D)$, $C_5=C_5(C_x)$, such that, for $\min\{|d/n-1|,d/n\}\ge\varepsilon$, the following holds with probability $1-O(n^{-D+1})$ for $n=\Omega_{C_x,\varepsilon,D}(1)$:
\[
s_{\min}\ge\max\{C_4\sigma_d,\sigma_{C_5n}\}.\tag{32}
\]''',r'''Suppose Assumption 1 holds with $n>d$, and further assume
\[
\nu=\min\left(\frac dn,1-\frac dn\right)\in(0,1).
\]
1. Variance approximation. There exist constants $\eta$ and $C$ (depending on $k$, $C_x$ and $D$) such that, for some $\epsilon>0$ if $n^{-(\frac14-\epsilon)(1-\frac1k)}\log^8n\le C\nu^{15.5}$, with probability $1-O_k(n^{-D+1})$:
\[
|\mathscr V_X(0)-V_n(0)|=O_{k,C_x,D}\left(\frac{\log^8n}{n^{(\frac14-\epsilon)(1-\frac1k)}\nu^{15.5}}\right)\cdot V_n(0).
\]
2. Bias approximation. $\mathscr B_X(0)=B_n(0)=0$ (this holds deterministically on the event $\operatorname{rank}(\boldsymbol X)=d$).''',r'''Let Assumption 1 hold. Then, for a fixed constant $\nu>0$ and any positive integer $D$, the following events hold with probability $1-O(n^{-D})$ (the $o_n(1)$ errors may depend on $D$):
1. Regularly varying spectrum with $\alpha>1$. Assume $(\sigma_i)_{i\ge1}$ is a regularly varying sequence with exponent $\alpha>1$. As a consequence, $\sigma_i=i^{-\alpha}a_i\exp\{\sum_{j=1}^i b_j/j\}$ with $a_i$ converging to a positive limit and $b_i\to0$. Define $c_\star=c_\star(\nu)>0$ as the unique positive solution of
\[
1=\nu c_\star^{-1}+\frac{\pi/\alpha}{\sin(\pi/\alpha)}c_\star^{-1/\alpha}.
\]
Then we have
\[
\lambda_\star(\nu n^{-\alpha})=c_\star\sigma_n(1+o_n(1)),\tag{34}
\]
\[
\mathscr V_X(\nu n^{-\alpha})=\frac{\tau^2(1-\nu c_\star^{-1})(\alpha-1)}{1+\nu c_\star^{-1}(\alpha-1)}(1+o_n(1)).\tag{35}
\]
Let $F_\beta(x)=\sum_{k=1}^{\lfloor nx\rfloor}\langle\boldsymbol\beta,\boldsymbol v_k\rangle^2$. If additionally $\boldsymbol\beta$ satisfies the following “polynomial-decay” property: for some $0<\theta\le1$ that
\[
\int_0^\infty x^\alpha\,dF_\beta(x)=O\left(n^{1-\theta}\int_0^\infty x^\alpha(1+c_\star x^\alpha)^{-1}\,dF_\beta(x)\right),
\]
we further have
\[
\mathscr B_X(\nu n^{-\alpha})=\frac{\sigma_nc_\star^2\alpha}{1+\nu c_\star^{-1}(\alpha-1)}\int_0^\infty\frac{x^\alpha}{(1+c_\star x^\alpha)^2}\,dF_\beta(x)(1+o_n(1)).\tag{36}
\]
2. Regularly varying spectrum with $\alpha=1$. Next consider the case $\sigma_i=i^{-1}a_i(1+\log i)^{-\alpha'}$ for some $\alpha'>1$ with $a_i$ converging to a positive limit. Define $c_\star=c_\star(\nu)>0$ as
\[
c_\star=\nu+\frac1{\alpha'-1}.
\]
We have
\[
\lambda_\star(\nu n^{-1}\log^{1-\alpha'}n)=c_\star\sigma_n\log n(1+o_n(1)),\tag{37}
\]
\[
\mathscr V_X(\nu n^{-1}\log^{1-\alpha'}n)=\frac{\tau^2}{c_\star\log n}(1+o_n(1)).\tag{38}
\]
Let $F_\beta(x)=\sum_{k=1}^{\lfloor(n/\log n)x\rfloor}\langle\boldsymbol\beta,\boldsymbol v_k\rangle^2$. If additionally $\boldsymbol\beta$ satisfies the following “rapid-decay” property: for some $0<\theta\le1$ that
\[
\int_0^\infty x\,dF_\beta(x)=O\left(n^{1-\theta}\int_0^\infty x(1+c_\star x)^{-1}\,dF_\beta(x)\right).
\]
then we further have
\[
\mathscr B_X(\nu n^{-1}\log^{1-\alpha'}n)=c_\star^2\sigma_n\log n\int_0^\infty\frac{x}{(1+c_\star x)^2}\,dF_\beta(x)(1+o_n(1)).\tag{39}
\]''',r'''Introduce the shorthand $\mathsf R_0(\boldsymbol Q):=\mathscr R_0(\zeta,\mu_\star(\zeta,\mu);\boldsymbol Q)$. Under Assumption 1, for any $\zeta>0$, $\mu\ge0$, p.s.d. matrix $\boldsymbol Q$ with $\|\boldsymbol Q\|=1$ and positive integer $D$, there exists constants $\eta=\eta(C_x)\in(0,1/2)$, $C_\alpha=C_\alpha(C_x,D)>0$, $C_\beta=C_\beta(C_x,D)>0$ and $C_\gamma=C_\gamma(C_x,D)$ such that for
\[
\gamma:=\min\left\{\frac2n\left(1+\frac{C_\gamma d_\Sigma\sigma_{\lfloor\eta n\rfloor}\cdot\log n\log(d_\Sigma n)}\zeta\right)+\frac2{\mu_\star(\zeta,\mu)},\frac1\zeta\right\},
\]
\[
\alpha_1:=C_\alpha\log n\cdot\sqrt{\gamma\mathsf R_0(\boldsymbol I)},\qquad\alpha_2:=C_\alpha\log n\cdot\sqrt{\gamma^3\mathsf R_0(\boldsymbol Q)},
\]
\[
\beta_1:=C_\beta\left(\sqrt{n\log n}\cdot\frac{\alpha_1\gamma\mathsf R_0(\boldsymbol Q)+\alpha_2(1+\mathsf R_0(\boldsymbol I))}{1+\mathsf R_0(\boldsymbol I)^2}+n\cdot\left\{\frac{\gamma^2\mathsf R_0(\boldsymbol Q)+\alpha_1\alpha_2}{1+\mathsf R_0(\boldsymbol I)^2}+\frac{\alpha_1^2\gamma\mathsf R_0(\boldsymbol Q)}{1+\mathsf R_0(\boldsymbol I)^3}\right\}+\frac{\gamma\mathsf R_0(\boldsymbol Q)}{1+\mathsf R_0(\boldsymbol I)}\right),
\]
\[
\beta_2:=\frac{C_\beta n\beta_1}{1+\mathsf R_0(\boldsymbol I)^2},
\]
if $\alpha_1\le\mathsf R_0(\boldsymbol I)/8$, $\beta_1\le\mathsf R_0(\boldsymbol Q)/64$, $\gamma\beta_2(1+\mathsf R_0(\boldsymbol I))\le1/64$ and $n^{-D}=O(\alpha_1/(1+\mathsf R_0(\boldsymbol I)))$, for all $n=\Omega_D(1)$ with probability $1-O(n^{-D+1})$ we have
\[
|\mathscr R_n(\zeta,\mu;\boldsymbol Q)-\mathscr R_0(\zeta,\mu_\star(\zeta,\mu);\boldsymbol Q)|=O\left(\gamma\beta_2(1+\mathscr R_0(\zeta,\mu_\star(\zeta,\mu);\boldsymbol I))\mathscr R_0(\zeta,\mu_\star(\zeta,\mu);\boldsymbol Q)+\beta_1\right).
\]''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label=label,source_order=i,statement_original=s,evidence=[dict(page=p,location=label+' — original statement'+(' continued' if j else '')) for j,p in enumerate(ps)]) for i,(n,label,ps,s) in enumerate(zip(NUMBERS,LABELS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Dimension free ridge regression',authors=['Chen Cheng','Andrea Montanari'],version='arXiv:2210.08571v3, stamped 19 June 2025; title-page date June 23, 2025',pdf_pages=86,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=34,main_text_boundary=dict(location='Main-text proof and Acknowledgements end on PDF page34 before References at y=622.01; the main-text crop ends at y=615. References continue through37; Appendix A begins38. All appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Independently enumerate bold SFBX1095 Theorem headings across main-text pages1–34; compare full original statements and continuations. Include Theorem6 within the main-text proof section, while excluding Lemmas, Propositions, Corollaries, Remarks, citations and appendix material.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v3 source from2025, pinned by SHA256, for the2024 article. Main text ends before References on34; no appendix body used.',normalization_policy='Original hypotheses, bounds, event qualification, regularization arguments and both bias/variance subparts preserved. Normalize line wrapping/typesetting only. Retain source scaling or quantifier ambiguities without silent corrections.'),papers=[paper],claims=cs)
def main():
    p=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved six complete original main-text Theorems; independent inventory review remains separate.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path);a=ap.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
