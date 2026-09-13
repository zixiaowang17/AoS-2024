"""Reproduce all four complete main-text Theorems from the registered EILLS PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2268'
SHA='41f8bc8d4dd5ddd961858aa2de3b28f08f5f0be294675a557a47cb7c64fa2a19'
URL='https://arxiv.org/pdf/2303.03092v3'
NUMBERS=['4.2','4.3','4.4','4.5']
TITLES=['Strong Convexity with respect to $\\boldsymbol\\beta^*$','Non-asymptotic Variable Selection Property','Non-asymptotic $\\ell_2$ Error Bound','Variable Selection Consistency in High Dimensions']
STATEMENTS=[r'''Assume Conditions 4.1–4.2 and 4.5 hold. Then $\boldsymbol\beta^*$ is the unique minimizer of $Q(\boldsymbol\beta;\gamma,\omega)$ for large enough $\gamma$: for any $\epsilon\in(0,1)$ and any $\gamma\ge\epsilon^{-1}\gamma^*$ with
\[
\gamma^*=(\kappa_L)^{-3}\sup_{S:S\cap G\ne\varnothing}(b_S/\bar d_S),
\]
(4.5)
where $b_S=\|\frac1{|\mathcal E|}\sum_{e\in\mathcal E}\mathbb E[\varepsilon^{(e)}\mathbf x_S^{(e)}]\|_2^2$ and $\bar d_S=\sum_{e\in\mathcal E}\frac1{|\mathcal E|}\|\boldsymbol\beta^{(e,S)}-\bar{\boldsymbol\beta}^{(S)}\|_2^2$ with $\bar{\boldsymbol\beta}^{(S)}=\frac1{|\mathcal E|}\sum_{e'\in\mathcal E}\boldsymbol\beta^{(e',S)}$, we have
\[
Q(\boldsymbol\beta;\gamma,\omega)-Q(\boldsymbol\beta^*;\gamma,\omega)\ge(1-\epsilon)\|\mathbf\Sigma^{1/2}(\boldsymbol\beta-\boldsymbol\beta^*)\|_2^2+\kappa_L^2(\gamma-\epsilon^{-1}\gamma^*)\bar d_{\operatorname{supp}(\boldsymbol\beta)}.
\]
(4.6)''',r'''Define
\[
s_+=\min_{j\in S^*}|\beta_j^*|^2\qquad\text{and}\qquad s_-=\min_{S\subseteq[p],S\cap G\ne\varnothing}\bar d_S
\]
(4.7)
Suppose Conditions 4.1–4.5 hold, and we choose $\gamma\ge3\gamma^*\vee1$ where $\gamma^*$ is defined in Theorem 4.2. There exists some universal constants $c_1$–$c_2$ that only depends on $(\kappa_U,\sigma_x,\sigma_\varepsilon)$ such that for any $t>0$, if $n\ge c_1(\gamma/\kappa_L)(p+\log(|\mathcal E|)+t)\{s_+^{-0.5}+s_+^{-1}+(\gamma\kappa_Ls_-)^{-0.5}\}$, and $n\cdot|\mathcal E|\ge c_2(\gamma/\kappa_L)^2(p+t)\{s_+^{-1}+(\gamma\kappa_Ls_-)^{-1}+1\}$, then the EILLS estimator $\widehat{\boldsymbol\beta}_Q$ minimizing (3.7) satisfies
\[
\mathbb P[S^*\subseteq\operatorname{supp}(\widehat{\boldsymbol\beta}_Q)\subseteq G^c]\ge1-7e^{-t}.
\]
(4.8)''',r'''Assume Conditions 4.1–4.5 hold, and we choose $\gamma\ge3\gamma^*\vee1$ where $\gamma^*$ is defined in Theorem 4.2. There exists some universal constants $c_1$–$c_4$ that only depend on $(\kappa_U,\sigma_x)$ such that for any $t>0$, if $n\ge p+\log(2|\mathcal E|)+t$ and $n\cdot|\mathcal E|\ge c_1(\gamma/\kappa_L)(p+t)$, then $\widehat{\boldsymbol\beta}_Q$ minimizing (3.7) satisfies
\[
\frac{\|\widehat{\boldsymbol\beta}_Q-\boldsymbol\beta^*\|_2}{\sigma_\varepsilon(\gamma/\kappa_L)}\le c_2\left(\sqrt{\frac{p+t}{n\cdot|\mathcal E|}}+\frac{p+\log(|\mathcal E|)+t}{n}\right)+c_3\frac{\sqrt{|S^*|}}{n}\cdot\frac{\log(|\mathcal E||S^*|)+t}{\min_{j\in S^*}|\beta_j^*|}
\]
(4.10)
with probability at least $1-7e^{-t}$. Moreover, when the additional conditions in Theorem 4.3 hold, then
\[
\frac{\|\widehat{\boldsymbol\beta}_Q-\boldsymbol\beta^*\|_2}{\sigma_\varepsilon(\gamma/\kappa_L)}\le c_2\left(\sqrt{\frac{|G^c|+t}{n\cdot|\mathcal E|}}+\frac{|G^c|+\log(|\mathcal E|)+t}{n}\right)
\]
(4.11)
occurs with probability at least $1-14e^{-t}$.''',r'''Assume Conditions 4.1–4.6 hold, and we choose $\gamma\ge3\gamma^*\vee1$ where $\gamma^*$ is defined in Theorem 4.2. Suppose further that the choice of $\lambda$ satisfies
\[
c_1\left\{(\gamma/\kappa_L)^2\frac{s^*\log p}{n\cdot|\mathcal E|}+\epsilon(n)\right\}\le\lambda\le c_2\kappa_L\beta_{\min}^2,
\]
where $\epsilon(n)=(\gamma/\kappa_L)^2s^\star(\log p)(s^*+\log p)/n^2+(\gamma/\kappa_L)\log p\sqrt{n^{-3}(s^*+\log p)}$, and $c_1,c_2$ are some universal positive constants only depends on $(C,\kappa_U,\sigma_x,\sigma_\varepsilon)$. Then the $\ell_0$ regularized EILLS estimator $\widehat{\boldsymbol\beta}_L$ minimizing (3.9) satisfies $\mathbb P[\operatorname{supp}(\widehat{\boldsymbol\beta}_L)=S^*]\ge1-p^{-10}$.''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',source_order=i,statement_original=s,evidence=[dict(page=page,location='Theorem '+n+' — complete original statement')]) for i,(n,title,s,page) in enumerate(zip(NUMBERS,TITLES,STATEMENTS,[13,14,15,16]),1)]
    paper=dict(paper_id=PID,title='Environment invariant linear least squares',authors=['Jianqing Fan','Cong Fang','Yihong Gu','Tong Zhang'],version='arXiv:2303.03092v3; 29 Nov 2024',pdf_pages=65,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=20,main_text_boundary=dict(location='Section 6 and Acknowledgement end on PDF page 20 before References at y=625.73. Page-20 evidence clipped at y=619; reference and appendix bodies excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate every actual bold Theorem heading in all main-text pages; four environments. Exclude prose citations, Propositions, Remarks, Definitions and Conditions. Preserve full formulas and both conditional branches of T4.4.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v3; appendix bodies excluded.',normalization_policy='Preserve original wording, all hypotheses, constants and formulas. Normalize line wrapping and mathematical typesetting. Keep c1–c4 as printed in T4.4 and distinct n versus n times environment count.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all four complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
