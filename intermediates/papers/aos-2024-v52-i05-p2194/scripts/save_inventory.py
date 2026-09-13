"""Reproduce every complete main-text Theorem in the registered quantile-process paper."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2194'
SHA='c6a7f1af69047f6993261caff6f851a5596b55ab10385c037788ee76afafa3e7'
URL='https://arxiv.org/pdf/2407.21238v2'
NUMBERS=['3.1','3.2','4.1','5.1','5.2','5.3','5.4','6.1','6.2','6.3']
STATEMENTS=[r'''Fix any $0<\alpha<\beta<1$. Suppose that Assumptions 1 and 3 hold, and $E_P\|\mathbf W_i\|^2<\infty$ for $\mathbf W_i=(X_i,Y_i,X_iY_i,X_i^2)$. Then, under the probability distribution $P^*$,
\[
\{\sqrt n(G(p)-Q_{y,N}(p)):p\in[\alpha,\beta]\}\xrightarrow{\mathcal L}\mathbb Q\text{ as }\nu\to\infty
\]
in $(D[\alpha,\beta],\mathcal D)$ with respect to the sup norm metric, for any high entropy sampling design satisfying Assumption 2, where $G(p)$ denotes one of $\widehat Q_y(p)$, $\widehat Q_{y,RA}(p)$, $\widehat Q_{y,DI}(p)$ and $\widehat Q_{y,REG}(p)$ with $d(i,s)=(N\pi_i)^{-1}$, and $\mathbb Q$ is a mean 0 Gaussian process in $D[\alpha,\beta]$ with almost sure continuous path and p.d. covariance kernel
\[
K(p_1,p_2)=\lim_{\nu\to\infty}(n/N^2)E_P\left(\sum_{i=1}^N(\zeta_i(p_1)-\bar\zeta(p_1)-S(p_1)\pi_i)\times(\zeta_i(p_2)-\bar\zeta(p_2)-S(p_2)\pi_i)(\pi_i^{-1}-1)\right)\text{ for }p_1,p_2\in[\alpha,\beta].
\]
(5)
Here, $\bar\zeta(p)=\sum_{i=1}^N\zeta_i(p)/N$, $S(p)=\sum_{i=1}^N(\zeta_i(p)-\bar\zeta(p))(1-\pi_i)/\sum_{i=1}^N\pi_i(1-\pi_i)$, and $\zeta_i(p)$'s are as in Table 1 below.''',r'''Fix any $0<\alpha<\beta<1$. Suppose that $E_P(X_i)^{-1}<\infty$, $E_P\|\mathbf W_i\|^2<\infty$ for $\mathbf W_i=(X_i,Y_i,X_iY_i,X_i^2)$, Assumptions 1 and 3–5 hold, and (6) holds. Then, the conclusion of Theorem 3.1 holds for $d(i,s)=A_i/NX_i$ and RHC sampling design with p.d. covariance kernel
\[
K(p_1,p_2)=\lim_{\nu\to\infty}n\gamma E_P\left[(\bar X/N)\sum_{i=1}^N(\zeta_i(p_1)-\bar\zeta(p_1))(\zeta_i(p_2)-\bar\zeta(p_2))X_i^{-1}\right]
=cE_P(X_i)E_P\left[(\zeta_i(p_1)-E_P(\zeta_i(p_1)))(\zeta_i(p_2)-E_P(\zeta_i(p_2)))X_i^{-1}\right]\text{ for }p_1,p_2\in[\alpha,\beta].
\]
(7)
Here, $\gamma=\sum_{r=1}^nN_r(N_r-1)/N(N-1)$, $c=\lim_{\nu\to\infty}n\gamma$, and $\zeta_i(p)$'s are as in Table 1 above.''',r'''(i) Suppose that $H$ is fixed as $\nu\to\infty$, and Assumptions 1 and 6–8 hold. Then, the conclusion of Theorem 3.1 holds for stratified multistage cluster sampling design with SRSWOR with p.d. covariance kernel
\[
K(p_1,p_2)=\lim_{\nu\to\infty}(n/N^2)\sum_{h=1}^HN_h(N_h-n_h)E_P(\zeta'_{hjl}(p_1)-E_P(\zeta'_{hjl}(p_1)))\times(\zeta'_{hjl}(p_2)-E_P(\zeta'_{hjl}(p_2)))/n_h\text{ for }p_1,p_2\in[\alpha,\beta].
\]
(8)
Here, $\zeta'_{hjl}(p)$'s are as in Table 3 below.
(ii) Further, if $H\to\infty$ as $\nu\to\infty$, and Assumptions 1 and 8–11 hold, then the same result holds.''',r'''(i) Fix $0<\alpha<\beta<1$. Suppose that the conclusion of Theorem 3.1 holds and $K(p_1,p_2)$ in (5) is continuous on $[\alpha,\beta]\times[\alpha,\beta]$. Then, under $P^*$,
\[
\sqrt n\left(\int_{[\alpha,\beta]}G(p)J(p)dp-\int_{[\alpha,\beta]}Q_{y,N}(p)J(p)dp\right)\xrightarrow{\mathcal L}N(0,\sigma_1^2)\text{ and}
\]
\[
\sqrt n\left(f(G(p_1),\ldots,G(p_k))-f(Q_{y,N}(p_1),\ldots,Q_{y,N}(p_k))\right)\xrightarrow{\mathcal L}N(0,\sigma_2^2)\text{ as }\nu\to\infty
\]
(9)
for any high entropy sampling design, where $k\ge1$, $p_1,\ldots,p_k\in[\alpha,\beta]$, and $G(p)$ is one of $\widehat Q_y(p)$, $\widehat Q_{y,RA}(p)$, $\widehat Q_{y,DI}(p)$ and $\widehat Q_{y,REG}(p)$ with $d(i,s)=(N\pi_i)^{-1}$. Here,
\[
\sigma_1^2=\int_\alpha^\beta\int_\alpha^\beta K(p_1,p_2)J(p_1)J(p_2)dp_1dp_2,\quad\sigma_2^2=\mathbf a\mathbf\Delta\mathbf a^T,
\]
(10)
$\mathbf\Delta$ is a $k\times k$ matrix such that
\[
((\mathbf\Delta))_{uv}=K(p_u,p_v)\text{ for }1\le u,v\le k,\text{ and }\mathbf a=\lim_{\nu\to\infty}\nabla f(Q_{y,N}(p_1),\ldots,Q_{y,N}(p_k))
\]
(11)
a.s. $[P]$.
(ii) Further, if the assumptions of Theorem 3.2 hold, then the results in (9) hold for $d(i,s)=A_i/NX_i$ in the case of RHC sampling design.''',r'''(i) Fix $0<\alpha<\beta<1$. Suppose that $H$ is fixed as $\nu\to\infty$, and Assumptions 1 and 6–8 hold, then the results in (9) of Theorem 5.1 hold for $d(i,s)=(N\pi_i)^{-1}=M_hN_{hj}/Nm_hr_h$ under stratified multistage cluster sampling design with SRSWOR.
(ii) On the other hand, if $H\to\infty$ as $\nu\to\infty$, Assumptions 1 and 8–11 hold, and $K(p_1,p_2)$ in (8) is continuous on $[\alpha,\beta]\times[\alpha,\beta]$, then the same results hold.''',r'''(i) Fix $0<\alpha<\beta<1$. Suppose that the assumptions of Theorem 3.1 hold, $K(p_1,p_2)$ is as in (5), and $\widehat K(p_1,p_2)$ is as in (12). Then, under $P^*$,
\[
\widehat\sigma_i^2\xrightarrow{p}\sigma_i^2\text{ as }\nu\to\infty\text{ for }i=1,2
\]
(14)
and any high entropy sampling design satisfying Assumption 2.
(ii) Further, if the assumptions of Theorem 3.2 hold, $K(p_1,p_2)$ is as in (7), and $\widehat K(p_1,p_2)$ is as in (13). Then, the result in (14) hold under RHC sampling design.''',r'''Fix $0<\alpha<\beta<1$. Suppose that the assumptions of Theorem 4.1 hold, $K(p_1,p_2)$ is as in (8), and $\widehat K(p_1,p_2)$ is as in (16). Then, the result in (14) of Theorem 5.3 hold under stratified multistage cluster sampling design with SRSWOR.''',r'''Suppose that $X_i\le b$ a.s. $[P]$ for some $b>0$, $E_P(X_i)^{-1}<\infty$, Assumption 1 holds with $0<\lambda<E_P(X_i)/b$, Assumptions 4 and 5 hold, and (6) holds. Then, we have the following results.
(i) Under $P(s,\omega)$, the asymptotic variance of the estimator of $\int_{[\alpha,\beta]}Q_{y,N}(p)J(p)dp$ based on the sample quantile is smaller than the asymptotic variances of its estimators based on the ratio, the difference and the regression estimators of the finite population quantile if and only if
\[
\max_{2\le u\le4}\left\{\int_\alpha^\beta\int_\alpha^\beta(K_1(p_1,p_2)-K_u(p_1,p_2))J(p_1)J(p_2)dp_1dp_2\right\}<0
\]
(18)
(ii) Under $P(s,\omega)$, the asymptotic variance of the estimator of $f(Q_{y,N}(p_1),\ldots,Q_{y,N}(p_k))$ based on the sample quantile is smaller than the asymptotic variances of its estimators based on the ratio, the difference and the regression estimators of the finite population quantile if and only if
\[
\max_{2\le u\le4}\mathbf a(\mathbf\Delta_1-\mathbf\Delta_u)\mathbf a^T<0,
\]
(19)
where $\mathbf a=\nabla f(Q_y(p_1),\ldots,Q_y(p_k))$ is the gradient of $f$ at $(Q_y(p_1),\ldots,Q_y(p_k))$.''',r'''Suppose that $X_i\le b$ a.s. $[P]$ for some $b>0$, $E_P(X_i)^{-1}<\infty$, Assumption 1 holds with $0<\lambda<E_P(X_i)/b$, Assumptions 4 and 5 hold, and (6) holds. Then, we have the following results.
(i) The asymptotic variance of the estimator of $\int_{[\alpha,\beta]}Q_{y,N}(p)J(p)dp$ based on $G(p)$ under SRSWOR is smaller than its asymptotic variance under RHC as well as any HE$\pi$PS sampling design, which uses auxiliary information, if and only if
\[
\max_{2\le u\le3}\left\{\int_\alpha^\beta\int_\alpha^\beta(K_1^*(p_1,p_2)-K_u^*(p_1,p_2))J(p_1)J(p_2)dp_1dp_2\right\}<0.
\]
(21)
(ii) The asymptotic variance of the estimator of $f(Q_{y,N}(p_1),\ldots,Q_{y,N}(p_k))$ based on $G(p)$ under SRSWOR is smaller than its asymptotic variance under RHC as well as any HE$\pi$PS sampling design if and only if
\[
\max_{2\le u\le3}\mathbf a(\mathbf\Delta_1^*-\mathbf\Delta_u^*)\mathbf a^T<0,
\]
(22)
where $\mathbf a=\nabla f(Q_y(p_1),\ldots,Q_y(p_k))$ is the gradient of $f$ at $(Q_y(p_1),\ldots,Q_y(p_k))$.''',r'''Suppose that $Q_y(0.5)=E_P(Y_i)$, and Assumptions 1 and 3 hold. Then, under SRSWOR, the asymptotic variance of the sample median is smaller than that of the sample mean and the asymptotic variance of the GREG estimator of the mean is smaller than that of the sample median if and only if
\[
\sigma_y^2>1/4f_y^2(Q_y(0.5)),\text{ and}
\]
(23)
\[
\rho_{xy}^2>(1-\lambda)^{-1}(1-1/4\sigma_y^2f_y^2(Q_y(0.5)))
\]
(24)
respectively. Here, $\sigma_y^2$ and $f_y$ are the superpopulation variance and density function of $y$, respectively, and $\rho_{xy}$ is the superpopulation correlation coefficient between $x$ and $y$.''']
def inventory():
    pages=[[10],[12],[16],[19],[20],[21],[22],[23],[23,24],[26]]
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement') for p in pp]) for i,(n,s,pp) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='Quantile processes and their applications in finite populations',authors=['Anurag Dey','Probal Chaudhuri'],version='arXiv:2407.21238v2; 29 Nov 2024',pdf_pages=106,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Section 7 data-analysis summary ends on PDF page 29 before the Appendix heading at y=531.02. Page-29 evidence is clipped at y=527. No appendix body is used.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate the ten bold Theorem headings in all main-text pages. Preserve every subpart, referenced conclusion/assumption, covariance formula and comparison. Exclude citation paragraphs, Propositions and appendix results.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v2 PDF; appendix body excluded.',normalization_policy='Preserve original theorem wording, references and formulas, including expectation/grouping and slash-division notation. Normalize PDF line wrapping and mathematical typesetting only. Branch-specific assumptions are not merged into conjunctions.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all ten complete main-text Theorems; source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
