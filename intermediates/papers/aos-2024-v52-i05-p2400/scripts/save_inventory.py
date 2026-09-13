"""Reproduce all six main-text Theorems from the registered lattice trend-filtering PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2400'
SHA='24e6b64a3c70e5ec5e17e9bf317258d16e6d37805c0d2f783ca69a5565f251d0'
URL='https://arxiv.org/pdf/2112.14758v2'
NUMBERS=['1','2','3','4','5','6']
STATEMENTS=[r'''Let $U\subseteq\mathbb R^d$ be an open, bounded, convex set. Then for any $f\in\operatorname{BV}(U)$,
\[
\operatorname{TV}(f;U)=\sum_{j=1}^d\int_{U_{-j}}\operatorname{TV}\big(f(\cdot,x_{-j});I_{x_{-j}}\big)\,dx_{-j},
\]
(20)
where for each $j=1,\ldots,d$, we define $U_{-j}=\{x_{-j}:(x_j,x_{-j})\in U\text{ for some }x_j\}$, and $I_{x_{-j}}=[a_{x_{-j}},b_{x_{-j}}]$, with
\[
a_{x_{-j}}=\inf\{x_j:(x_j,x_{-j})\in U\},\qquad b_{x_{-j}}=\sup\{x_j:(x_j,x_{-j})\in U\}.
\]
Recall $f(\cdot,x_{-j})$ denotes $f$ as function of the $j$th coordinate with all other dimensions fixed at $x_{-j}$. Lastly, the univariate TV operator in the integrand in (20) is to be interpreted in the essential variation sense, as in (19).''',r'''Consider the generalized lasso estimator $\widehat\theta$ with penalty matrix $D\in\mathbb R^{r\times n}$, defined by the solution of
\[
\underset{\theta\in\mathbb R^n}{\operatorname{minimize}}\quad\frac12\|y-\theta\|_2^2+\lambda\|D\theta\|_1
\]
(30)
Suppose that $D$ has rank $q$, and denote by $\xi_1\le\cdots\le\xi_q$ its nonzero singular values. Also let $u_1,\ldots,u_q\in\mathbb R^r$ be the corresponding left singular vectors. Assume that these vectors, except possibly for those in a set $I\subseteq[q]$, are incoherent, meaning that for a constant $\mu\ge1$,
\[
\|u_i\|_\infty\le\mu/\sqrt n,\qquad i\in[q]\setminus I.
\]
Then under the data model (29), choosing
\[
\lambda\asymp\mu\sqrt{\frac{\log r}n\sum_{i\in[q]\setminus I}\frac1{\xi_i^2}},
\]
the generalized lasso estimator satisfies
\[
\frac1n\|\widehat\theta-\theta_0\|_2^2=O_{\mathbb P}\left(\frac{\operatorname{nullity}(D)}n+\frac{|I|}n+\frac\mu n\sqrt{\frac{\log r}n\sum_{i\in[q]\setminus I}\frac1{\xi_i^2}}\cdot\|D\theta_0\|_1\right).
\]
(31)''',r'''Let $\widehat\theta$ denote the KTF estimator in (7). Under the data model (29), denote $C_n=\|D_{n,d}^{(k+1)}\theta_0\|_1$, and assume $C_n>0$. Choosing
\[
\lambda\asymp\begin{cases}\sqrt{\log n}&\text{if }s<1/2,\\\log n&\text{if }s=1/2,\\(\log n)^{\frac1{2s+1}}(n/C_n)^{\frac{2s-1}{2s+1}}&\text{if }s>1/2,\end{cases}
\]
the KTF estimator satisfies
\[
\frac1n\|\widehat\theta-\theta_0\|_2^2=O_{\mathbb P}\left(\frac1n+\frac\lambda nC_n\right).
\]''',r'''The minimax risk for KTV class defined in (23) satisfies, for any sequence $C_n\le n$,
\[
R\big(\mathcal T_{n,d}^k(C_n)\big)=\Omega\left(\frac1n+\frac{C_n}n+\left(\frac{C_n}n\right)^{\frac2{2s+1}}\right).
\]
(33)''',r'''The minimax linear risk over the KTV class in (23) satisfies, for any sequence $C_n\le\sqrt n$,
\[
R_L\big(\mathcal T_{n,d}^k(C_n)\big)=\begin{cases}\Omega(1/n+C_n^2/n)&\text{if }s<1/2,\\\Omega(1/n+C_n^2/n\log(1+n/C_n^2))&\text{if }s=1/2,\\\Omega\big(1/n+(C_n^2/n)^{\frac1{2s}}\big)&\text{if }s>1/2.\end{cases}
\]
(35)
This is achieved in rate by the projection estimator in (34), where we set $Q=[\tau]^d$ for $\tau^d\asymp(C_nn^{s-1/2})^{1/s}$, in the case $s>1/2$. When $s<1/2$, the simple polynomial projection estimator, which projects onto all multivariate polynomials of max degree $k$ (equivalently, the estimator in (34) with $Q=[k+1]^d$), achieves the rate in (35). When $s=1/2$, either estimator achieves the rate in (35) up to a log factor. Lastly, if $C_n^2=O(n^\alpha)$ for $\alpha<1$, and still $s=1/2$, then either estimator achieves the rate in (35) without the additional log factor.''',r'''The minimax risk over the (discrete) Sobolev class in (24) satisfies, for any sequence $B_n\le\sqrt n$,
\[
R\big(\mathcal W_{n,d}^{k+1}(B_n)\big)\asymp\frac1n+\left(\frac{B_n^2}n\right)^{\frac1{2s+1}}.
\]
The lower bound is due to the Holder embedding in (26) (and the lower bound on the discretized Holder class derived in Sadhanala et al. (2017)), and the upper bound is from the estimator in (34), with $Q=[\tau]^d$ for $\tau^d\asymp(B_n^2n^{2s})^{1/(2s+1)}$. Finally, when $B_n\asymp L_nB_n^*$ where $B_n^*$ is the canonical scaling in (27), the minimax rate is $L_n^{2/(2s+1)}n^{-2s/(2s+1)}$.''']
def inventory():
    pages=[12,15,16,16,18,18]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' (Wang et al. 2016)' if n=='2' else ''),source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement, including all italic continuation paragraphs')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='Multivariate trend filtering for lattice data',authors=['Veeranjaneyulu Sadhanala','Yu-Xiang Wang','Addison J. Hu','Ryan J. Tibshirani'],version='arXiv:2112.14758v2; 5 Apr 2024',pdf_pages=56,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Section9.5 and Acknowledgements end on PDF page29; References start at y=643.204. Main-text evidence is clipped at y=637 on this page. All appendix bodies excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate bold Theorem environments in main-text pages1–29; labels1–6. Include the credited Theorem2. T5 and T6 include italic paragraphs after their displays. Exclude Propositions, Corollaries, citations and proof-only appendix material.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v2; appendix bodies excluded.',normalization_policy='Preserve original wording, all formulas and complete italic theorem bodies; normalize wrapping and typesetting. Theorem5 critical logarithm multiplies C_n^2/n. Preserve canonical-rate and projection-order domain qualifications as source notes, without inserting repairs into quotations.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all six complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
