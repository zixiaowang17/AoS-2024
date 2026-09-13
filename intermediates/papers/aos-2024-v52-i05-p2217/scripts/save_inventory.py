"""Retain all four complete main-text theorems of the registered journal PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2217'
SHA='4866290bd80a1259e98bf4ce9009d84443ad2c20c9a0927e9b61ed133785bad7'
URL='https://scholarsphere.psu.edu/resources/57f5e3c5-27e7-4f8a-b3e2-17e8e2e2407e/downloads/40206'
NU=r'''\[
\begin{aligned}
\nu={}&\operatorname{tr}(\mathbf R\mathbf D_1)+\frac{n(n-1)}{4(n-2)^3}\operatorname{tr}(\mathbf D_0\mathbf D_1)\\
&+\frac{n(2n-1)}{(n-2)^2(n-2+p)}\left[2\operatorname{tr}(\mathbf R\mathbf D_1)+\beta_w\sum_{k=1}^p\sum_{\ell=1}^p\mathbf e_\ell^T\mathbf R^{1/2}\mathbf D_1\mathbf e_k(\mathbf e_k^T\mathbf R^{1/2}\mathbf e_\ell)^3\right]\\
&-\frac1{1+y_{n-2}}\left(\frac{n^2-3n+4}{(n-2)^2}+\frac{(n-4)p}{(n-2)^2}+\frac{(n_1-1)p}{n_1(n-2)^2}+\frac{(n_2-1)p}{n_2(n-2)^2}+\frac{\beta_wn}{(n-2)^2}\right)\times\operatorname{tr}(\mathbf R\mathbf D_1)\\
&+\frac{n(n-1)}{(1+y_{n-2})(n-2)^3}\times\left[2\operatorname{tr}(\mathbf R\mathbf D_1\mathbf R)+\beta_w\sum_{k=1}^p\sum_{\ell=1}^p\mathbf e_\ell^T\mathbf R^{-1/2}\mathbf e_k\mathbf e_k^T\mathbf R\mathbf D_1\mathbf R^{1/2}\mathbf e_\ell(\mathbf e_\ell^T\mathbf R^{1/2}\mathbf e_k)^2\right]\\
&+(1+y_{n-2})^{-1}\frac n{(n-2)^3}\operatorname{tr}(\mathbf R\mathbf D_1)\left[2p+\beta_w\sum_{k=1}^p\sum_{\ell=1}^p\mathbf e_\ell^T\mathbf R^{-1/2}\mathbf e_k(\mathbf e_k^T\mathbf R^{1/2}\mathbf e_\ell)^3\right]\\
&-(1+y_{n-2})^{-1}\frac{3n(n-1)\operatorname{tr}(\mathbf R\mathbf D_1)}{4(n-2)^4}\left[2p+\beta_w\sum_{k=1}^p\sum_{\ell=1}^p(\mathbf e_k^T\mathbf R^{1/2}\mathbf e_\ell)^4\right]\\
&-\frac{5n(n-1)}{4(n-2)^2(n-2+p)}\left[2\operatorname{tr}(\mathbf R\mathbf D_1)+\beta_w\sum_{i=1}^p\mathbf e_i^T\mathbf R\mathbf D_1\mathbf e_i\sum_{k=1}^p(\mathbf e_k^T\mathbf R^{1/2}\mathbf e_i)^4\right]\\
&-\frac{n(n-1)}{4(n-2)^2(n-2+p)}\sum_{i=1}^p\sum_{j=1}^p\mathbf e_i^T\mathbf R^{-1}\mathbf e_j\mathbf e_i^T\mathbf R\mathbf D_1\mathbf R\mathbf e_j\cdot g(i,j,\beta_w,\mathbf R)\\
&-\frac{n(n-1)\operatorname{tr}(\mathbf R\mathbf D_1)}{4(n-2)^3(n-2+p)}\sum_{i=1}^p\sum_{j=1}^p\mathbf e_i^T\mathbf R^{-1}\mathbf e_j\mathbf e_i^T\mathbf R\mathbf e_j\cdot g(i,j,\beta_w,\mathbf R)\\
&-\frac{n(n-1)(3n-6+p)}{4(n-2)^3(n-2+p)}\sum_{i=1}^p\sum_{j=1}^p\mathbf e_i^T\mathbf D_1\mathbf e_j\mathbf e_i^T\mathbf R\mathbf e_j\cdot g(i,j,\beta_w,\mathbf R),
\end{aligned}
\]'''
G=r'''and $g(i,j,\beta_w,\mathbf R)=2(\mathbf e_i^T\mathbf R\mathbf e_j)^2+\beta_w\sum_{k=1}^p(\mathbf e_k^T\mathbf R^{1/2}\mathbf e_i)^2(\mathbf e_k^T\mathbf R^{1/2}\mathbf e_j)^2$, '''
SIGMA=r'''\[
\begin{aligned}
\sigma^2={}&\left(\frac{1+2y}{1-y}\right)^2\left\{2n^{-1}\operatorname{tr}[(\mathbf R\mathbf D_1)^2]+\beta_wn^{-1}\sum_{\ell=1}^p(\mathbf e_\ell^T\mathbf R^{1/2}\mathbf D_1\mathbf R^{1/2}\mathbf e_\ell)^2\right\}\\
&+\left(\frac{1+2y}{1-y}\right)^2\frac1n\sum_{i=1}^p\sum_{j=1}^p\mathbf e_i^T\mathbf R\mathbf D_1\mathbf e_i\mathbf e_j^T\mathbf R\mathbf D_1\mathbf e_j\cdot g(i,j,\beta_w,\mathbf R)\\
&-2\left(\frac{1+2y}{1-y}\right)^2\frac1n\sum_{\ell=1}^p\mathbf e_\ell^T\mathbf R\mathbf D_1\mathbf e_\ell\left[2\mathbf e_\ell^T\mathbf R\mathbf D_1\mathbf R\mathbf e_\ell+\beta_w\sum_{k=1}^p(\mathbf e_k^T\mathbf R^{1/2}\mathbf e_\ell)^2\mathbf e_k^T\mathbf R^{1/2}\mathbf D_1\mathbf R^{1/2}\mathbf e_k\right]\\
&+(1+y)^{-2}[n^{-1}\operatorname{tr}(\mathbf R\mathbf D_1)]^2(2-2y-\beta_wy)+2(1+y)^{-2}y[n^{-1}\operatorname{tr}(\mathbf R\mathbf D_1)^2]\\
&+(1+y)^{-2}[n^{-1}\operatorname{tr}(\mathbf R\mathbf D_1)]^2[2n^{-1}\operatorname{tr}(\mathbf R^2)+\beta_wy]\\
&-\frac2{(1+y)^2}[n^{-1}\operatorname{tr}(\mathbf R\mathbf D_1)][2n^{-1}\operatorname{tr}(\mathbf R^2\mathbf D_1)+\beta_wn^{-1}\operatorname{tr}(\mathbf R\mathbf D_1)]\\
&+\frac2{(1+y)^2}[n^{-1}\operatorname{tr}(\mathbf R\mathbf D_1)]n^{-1}\sum_{\ell=1}^p\mathbf e_\ell^T\mathbf R\mathbf D_1\mathbf e_\ell[2\mathbf e_\ell^T\mathbf R^2\mathbf e_\ell+\beta_w],
\end{aligned}
\]'''
AUX=r'''with $\mathbf B=\{p^{-1}\operatorname{tr}(\mathbf R\mathbf A_k\mathbf R\mathbf A_\ell)+y_{n-2}p^{-2}\operatorname{tr}(\mathbf R\mathbf A_k)\operatorname{tr}(\mathbf R\mathbf A_\ell)\}_{k,\ell=1}^K$, $\mathbf D_1=\eta_1\mathbf A_1+\cdots+\eta_K\mathbf A_K$, $(\eta_1,\ldots,\eta_K)=(\pi_1,\ldots,\pi_K)\mathbf B^{-1}$, $\mathbf D_0$ being the $p\times p$-dimensional matrix with the $(i,j)$ element being $u_{ij}$ as follows: $u_{ij}=2(\mathbf e_i^T\mathbf R\mathbf e_j)^3+\beta_w\mathbf e_i^T\mathbf R\mathbf e_j\sum_{\ell=1}^p(\mathbf e_\ell^T\mathbf R^{1/2}\mathbf e_i)^2(\mathbf e_\ell^T\mathbf R^{1/2}\mathbf e_j)^2$, $\mathbf e_k$ being the $k$-column of the $p\times p$ identity matrix and $\beta_w=\kappa-3$.'''
NULL=r'''\[
\sigma_0^2=(2p)n^2n_1^{-2}+(2p)n^2n_2^{-2}+4n^2p(n_1n_2)^{-1}+(nn_1^{-2}+nn_2^{-2})\left[4\operatorname{tr}(\mathbf R^2)+2\sum_{h=1}^p\mathbf e_h^T\mathbf R^2\mathbf e_h\mathbf e_h^T\mathbf R^{-1}\mathbf e_h\right],
\]
\[
\mu_0=np(n_1^{-1}+n_2^{-1})+\frac{n(n-1)}{4(n-2)^2}(n_1^{-1}+n_2^{-1})\operatorname{tr}(\mathbf R^{-1}\mathbf A_0),
\]'''
STATEMENTS=[r'''Suppose that $\{\mathbf x_{mi},i=1,\ldots,n_m\}$ for $m=1,2$, is a random sample from a $p$-dimensional population $\mathbf x^{(m)}$, which can be represented as $\mathbf x^{(m)}=\mathbf\Sigma^{1/2}\mathbf w+\boldsymbol\mu_m$, where the components of $\mathbf w=(w_1,\ldots,w_p)^T$ are independent and identically distributed, and have the fourth moment with $E(w_j)=0$, $E(w_j^2)=1$, $E(w_j^4)=\kappa$ for $j=1,\ldots,p$. Then it follows that, almost surely,
\[
\widehat\theta_k\to(1+y)^{-1}\theta_k,\quad k=1,\ldots,K.
\]''',r'''Under the conditions of Theorem 2.1 and $p^{-1}\operatorname{tr}(\mathbf R\mathbf A_i\mathbf R\mathbf A_j)$ are bounded for $i,j=1,\ldots,K$, for any constants $(\pi_1,\ldots,\pi_K)$, we have
\[
\sigma^{-1}\left\{p\sum_{k=1}^K\pi_k[\widehat\theta_k-(1+y_{n-2})^{-1}\theta_k]-\nu\right\}\to N(0,1),
\]
where
'''+NU+'\n'+G+'\n'+SIGMA+'\n'+AUX,r'''Suppose that the conditions of Theorem 2.2 hold. Under $H_0$, it follows that
\[
\frac{nT_n-\widehat c\widehat\mu_0}{\widehat c\widehat\sigma_0}\to N(0,1),
\]
where $\widehat c=\frac1{1+p/(n-2)}$, and $\widehat\sigma_0^2$ and $\widehat\mu_0$ are estimates of
'''+NULL+r'''
respectively, where $\mathbf e_k$ is the $k$-column of the identity matrix $\mathbf I_p$ and $\mathbf A_0$ is a $p\times p$ matrix with $(h,\ell)$-element being $a_{h,\ell}=2(\mathbf e_h^T\mathbf R\mathbf e_\ell)^3$. The estimates $\widehat\sigma_0^2$ and $\widehat\mu_0$ are obtained by replacing $\mathbf R$ with $\widetilde{\mathbf R}=\{\operatorname{diag}[\widehat{\mathbf R}_L]\}^{-1/2}\widehat{\mathbf R}_L\{\operatorname{diag}[\widehat{\mathbf R}_L]\}^{-1/2}$ in $\sigma_0^2$ and $\mu_0$.''',r'''Under the conditions of Theorem 2.3 and under the alternative hypothesis $H_1:\boldsymbol\mu_1\ne\boldsymbol\mu_2$, it follows that
\[
\frac{nT_n-c\mu_0-cn\delta_n}{c\sqrt{\sigma_0^2+4n^2(n_1^{-1}+n_2^{-1})\delta_n}}\to N(0,1),
\]
where $c=(1+y)^{-1}$, $\delta_n=\boldsymbol\mu_d^T\mathbf\Sigma^{-1}\boldsymbol\mu_d$ with $\boldsymbol\mu_d=\boldsymbol\mu_1-\boldsymbol\mu_2$. Furthermore, the asymptotic power function of $T_n$ is
\[
Q(\delta_n,\sigma_0\mid\alpha)=\Phi\left(\frac{-z_\alpha\sigma_0}{\sqrt{\sigma_0^2+4n^2(n_1^{-1}+n_2^{-1})\delta_n}}+\frac{\delta_n}{\sqrt{\sigma_0^2/n^2+4(n_1^{-1}+n_2^{-1})\delta_n}}\right),
\]
(8)
where $\Phi(\cdot)$ is the cumulative distribution function of $N(0,1)$ and $\Phi(-z_\alpha)=\alpha$.''']
def inventory():
    claims=[dict(claim_id=PID+'/T2.'+str(i),paper_id=PID,claim_kind='theorem',label='Theorem 2.'+str(i),source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem 2.'+str(i)+' — complete original statement') for p in pp]) for i,(s,pp) in enumerate(zip(STATEMENTS,[[5],[5,6],[7],[8]]),1)]
    paper=dict(paper_id=PID,title='A new test for high-dimensional two-sample mean problems with consideration of correlation structure',authors=['Songshan Yang','Shurong Zheng','Runze Li'],version='Published journal article, The Annals of Statistics 52(5), 2024, pp. 2217–2240; registered 24-AOS2433-1.pdf',pdf_pages=24,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=23,main_text_boundary=dict(location='Discussion and acknowledgments end on PDF page 22; Funding ends on page 23 before SUPPLEMENTARY MATERIAL at y=115.02. Page-23 evidence clipped at y=108. No supplementary or appendix body used.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate every small-cap THEOREM environment across main text; exactly 2.1–2.4. Retain full two-page Theorem 2.2 formulas. Exclude proof headings, citations and Lemma 2.5.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified published PDF from local manifest; no supplementary or appendix body.',normalization_policy='Preserve complete original statements and displayed formulas, including the reused B symbol, y=1 denominator, arbitrary contrast coefficients and exact trace-power placement. Normalize line wrapping and mathematical typesetting only; do not silently repair source issues.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all four complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
