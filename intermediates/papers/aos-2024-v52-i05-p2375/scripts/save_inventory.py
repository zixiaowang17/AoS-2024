"""Reproduce four complete main-text Theorems from the registered time-series PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2375'
SHA='fe207a49e1348050da5b83e03fbacb2ad8f1beb676ca7ebf1ac395393d57c579'
URL='https://arxiv.org/pdf/2110.14067v2'
NUMBERS=['1','2','3','4']
STATEMENTS=[r'''Suppose $X_i$, $i\in\mathbb Z$, are $(m,\alpha)$-short range dependent random variables with $m\ge8$ and $\alpha>2$, $X_1,\ldots,X_T$ is the observed time series and $d=O(T^B)$ is a positive integer with $B\ge0$. Let $a_{ij}$, $i=1,\ldots,p_1$, $j=0,1,\ldots,d$ be real numbers satisfying
\[
\max_{i=1,\ldots,p_1}\sum_{j=0}^da_{ij}^2=O(1)\text{ and }p_1=O(T^{\alpha_{p_1}}),
\]
(10)
where $\alpha_{p_1}\ge0$ is a constant. Define $Z_{i,k}=\sum_{j=0}^da_{kj}(X_iX_{i-j}-EX_iX_{i-j})$ for $i\in\mathbb Z$ and $k=1,\ldots,p_1$. Assume that
\[
\left\|\frac1{\sqrt T}\sum_{i=1}^TZ_{i,k}\right\|_2>c\text{ for }k=1,\ldots,p_1,
\]
(11)
where $c>0$ is a constant. If there exist two constants $\alpha_s$, $\alpha_l$ such that $0<\alpha_s<\alpha_l<1$ and
\[
\frac{2\alpha_{p_1}}m+2\alpha B<(\alpha-1)\alpha_s,\quad\frac{4\alpha_{p_1}}m+4\alpha B+\alpha_s<\alpha_l,\quad\frac{12\alpha_{p_1}}m+12\alpha B+\alpha_l<1
\]
and
\[
4\alpha B<(\alpha-1)\alpha_s,\quad8\alpha B+\alpha_s<\alpha_l,
\]
(12)
then,
\[
\sup_{x\in\mathbb R}\left|\operatorname{Prob}\left(\max_{k=1,\ldots,p_1}\left|\frac1{\sqrt T}\sum_{i=1}^TZ_{i,k}\right|\le x\right)-\operatorname{Prob}\left(\max_{k=1,\ldots,p_1}|\xi_k|\le x\right)\right|=o(1),
\]
(13)
where $\xi_k$, $k=1,\ldots,p_1$, are joint normal distributed random variables with $E\xi_k=0$ and $E\xi_{k_1}\xi_{k_2}=T^{-1}\sum_{i_1=1}^T\sum_{i_2=1}^TEZ_{i_1,k_1}Z_{i_2,k_2}$.''',r'''Suppose $\{X_i,i\in\mathbb Z\}$ are $(m,\alpha_X)$-short range dependent random variables with $m\ge8$, $\alpha_X>2$. Suppose further that $d=O(T^{\beta_X})$ is a positive integer and the sets $\mathcal H\subset\{0,1,\ldots,d\}$, $\mathcal I\subset\{1,2,\ldots,d\}$ are not empty. Assume that there exists constants $0<\alpha_s<\alpha_l<1$ such that
\[
\frac{2\beta_X}m+2\alpha_X\beta_X<(\alpha_X-1)\alpha_s,\quad\frac{4\beta_X}m+4\alpha_X\beta_X+\alpha_s<\alpha_l,\quad\frac{12\beta_X}m+12\alpha_X\beta_X+\alpha_l<1
\]
and
\[
4\alpha_X\beta_X<(\alpha_X-1)\alpha_s,\quad8\alpha_X\beta_X+\alpha_s<\alpha_l
\]
(17)
(i) If a constant $c>0$ exists such that
\[
\left\|\frac1{\sqrt T}\sum_{i=1}^T(X_iX_{i-j}-\sigma_j)\right\|_2>c\text{ for }j\in\mathcal H,
\]
(18)
then,
\[
\sup_{x\in\mathbb R}\left|\operatorname{Prob}\left(\max_{j\in\mathcal H}\sqrt T|\widehat\sigma_j-\sigma_j|\le x\right)-\operatorname{Prob}\left(\max_{j\in\mathcal H}|\xi_j|\le x\right)\right|=o(1),
\]
(19)
where $\xi_j$, $j\in\mathcal H$ are joint Gaussian random variables with $E\xi_j=0$ and $E\xi_{j_1}\xi_{j_2}=T^{-1}\sum_{i_1=1}^T\sum_{i_2=1}^TE(X_{i_1}X_{i_1-j}-\sigma_j)(X_{i_2}X_{i_2-j}-\sigma_j)$.
(ii) Define
\[
Z_{i,j}=-\frac{\sigma_j}{\sigma_0^2}(X_i^2-\sigma_0)+\frac1{\sigma_0}(X_iX_{i-j}-\sigma_j)
\]
and suppose there exists a constant $c>0$ such that
\[
\left\|\frac1{\sqrt T}\sum_{i=1}^TZ_{i,j}\right\|_2>c\text{ for }j\in\mathcal I\text{ and }\sigma_0>c.
\]
(20)
Then
\[
\sup_{x\in\mathbb R}\left|\operatorname{Prob}\left(\max_{j\in\mathcal I}\sqrt T|\widehat\rho_j-\rho_j|\le x\right)-\operatorname{Prob}\left(\max_{j\in\mathcal I}|\zeta_j|\le x\right)\right|=o(1),
\]
(21)
where $\zeta_j$, $j\in\mathcal I$ are joint Gaussian random variables with $E\zeta_j=0$ and $E\zeta_{j_1}\zeta_{j_2}=T^{-1}\sum_{i_1=1}^T\sum_{i_2=1}^TEZ_{i_1,j_1}Z_{i_2,j_2}$.''',r'''Suppose $\{X_i,i\in\mathbb Z\}$ are $(m,\alpha)$-short range dependent random variables with $m\ge8$ and $\alpha>2$. Let $p$ be a positive integer such that $p=O(1)$. In addition suppose that $\{X_i\}$ is weakly stationary and there exists a constant $c>0$ such that the smallest eigenvalue of $\Sigma$ is greater than $c$. Define $Z_{i,j}$ as in (27) and assume
\[
\left\|\frac1{\sqrt T}\sum_{i=1}^TZ_{i,j}\right\|_2>C\text{ for a constant }C>0\text{ and any }j=1,\ldots,p.
\]
(28)
Then,
\[
\sup_{x\in\mathbb R}\left|\operatorname{Prob}\left(\max_{j=1,\ldots,p}|\sqrt T(\widehat a_j-a_j)|\le x\right)-\operatorname{Prob}\left(\max_{j=1,\ldots,p}|\xi_j|\le x\right)\right|=o(1),
\]
(29)
where $a_1,\ldots,a_p$ are the AR coefficients satisfying Definition 3 and $\xi_1,\ldots,\xi_p$ are joint normal random variables with $E\xi_j=0$ and $E\xi_{j_1}\xi_{j_2}=T^{-1}\sum_{i_1=1}^T\sum_{i_2=1}^TEZ_{i_1,j_1}Z_{i_2,j_2}$;''',r'''Suppose the kernel function $K(\cdot)$ and the observations $X_1,\ldots,X_T$ satisfy the conditions of Lemma 4 and define $v_T$ as in Lemma 3 with $\alpha=\alpha_X$.
(i) In addition suppose $d=O(T^{\beta_X})$ is a positive integer, the bandwidth $k_T$ is such that $v_T\times T^{7\alpha_X\beta_X}=o(1)$ and $k_T\times T^{8\beta_X/m+7\alpha_X\beta_X-1/2}=o(1)$, and the set $\mathcal H\subset\{0,1,\ldots,d\}$ is not empty. Suppose (17) and (18) hold true. Then
\[
\sup_{x\in\mathbb R}\left|\operatorname{Prob}^*\left(\sqrt T\max_{j\in\mathcal H}|\widehat\sigma_j^*-\widehat\sigma_j|\le x\right)-H_\sigma(x)\right|=O_p\left((v_T\times T^{7\alpha_X\beta_X})^{1/6}+\left(k_T\times T^{8\beta_X/m+7\alpha_X\beta_X-1/2}\right)^{1/6}\right)
\]
(45)
(ii) In addition suppose $d=O(T^{\beta_X})$ is a positive integer, the bandwidth $k_T$ satisfies $v_T\times T^{7\alpha_X\beta_X}=o(1)$ and $k_T\times T^{8\beta_X/m+7\alpha_X\beta_X-1/2}=o(1)$ and the set $\mathcal I\subset\{1,\ldots,d\}$ is not empty. Suppose (17) and (20) hold true, then
\[
\sup_{x\in\mathbb R}\left|\operatorname{Prob}^*\left(\sqrt T\max_{j\in\mathcal I}|\widehat\rho_j^*-\widehat\rho_j|\le x\right)-H_\rho(x)\right|=o_p(1).
\]
(46)
(iii) In addition suppose $p=O(1)$ is a positive number and the bandwidth $k_T$ satisfies $v_T=o(1)$ and $k_T\times T^{-1/2}=o(1)$. Suppose (28) hold true and assume that the smallest eigenvalue of the covariance matrix $\Sigma$ (see Theorem 3) is greater than a constant $c>0$. Then,
\[
\sup_{x\in\mathbb R}\left|\operatorname{Prob}^*\left(\sqrt T\max_{j=1,\ldots,p}|\widehat a_j^*-\widehat a_j|\le x\right)-H_a(x)\right|=o_p(1).
\]
(47)''']
def inventory():
    pages=[[10,11],[14,15],[18],[23]]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' (Gaussian Approximation for AR Coefficients)' if n=='3' else ''),source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement'+(' (heading on page10; body on page11)' if n=='1' else '')) for p in pp]) for i,(n,s,pp) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='Simultaneous statistical inference for second order parameters of time series under weak conditions',authors=['Yunyi Zhang','Efstathios Paparoditis','Dimitris N. Politis'],version='arXiv:2110.14067v2; 25 Feb 2023',pdf_pages=66,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=28,main_text_boundary=dict(location='Section7 ends on PDF page27; Acknowledgement occupies PDF page28. References begin on page29. Main-text evidence ends at page28; all supplementary/appendix bodies excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate all bold Theorem headings in main-text pages1–28; four labels1–4. First heading is on page10 with statement on page11; T2 spans pages14–15. Exclude remarks, lemma environments, citations and proof references.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v2; appendix bodies excluded.',normalization_policy='Preserve original wording, all parts and formulas; normalize wrapping and typesetting. Preserve the printed unbound j in T2(i) covariance formula and the positive-number wording for p in T4(iii), with source issues recorded separately.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all four complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
