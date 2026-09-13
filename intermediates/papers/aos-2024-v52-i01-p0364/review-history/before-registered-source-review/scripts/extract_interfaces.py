"""Transcribe statement prerequisites from the inspected pinned preprint, without supplements."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
interfaces=[];members={};edges={}
def add(lid,term,body,pages,heading,deps=None,*,kind='definition',symbols=(),phrases=(),context=None,note=None,shape):
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,
        statement_original=body.strip(),relation='exact',depends_on=list(deps or {}),
        evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=list(symbols),highlight_phrases=list(phrases))
    if note:m['variant_note']=note
    terms=term if isinstance(term,list) else [term];keywords=[]
    for t in terms:
        key=dict(paper_id=PID,local_id=lid,source_text=t,label=t[0].upper()+t[1:],kind='term')
        if t not in body:
            assert context and t in context,(lid,t)
            m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])];key['context_id']=lid+'/name'
        keywords.append(key)
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=' · '.join(k['label'] for k in keywords),
        lean_role='hypothesis' if kind in ('condition','assumption') else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}
add('D1','tensor factor model',r'''
The tensor factor model for each $\mathcal X_t\in\mathbb R^{d_1\times\cdots\times d_K}$, $t\in[T]$, is
\[
\mathcal X_t=\boldsymbol\mu+\mathcal C_t+\mathcal E_t=\boldsymbol\mu+\mathcal F_t\times_1\mathbf A_1\times_2\cdots\times_K\mathbf A_K+\mathcal E_t,\tag{3.1}
\]
where $\mathcal F_t\in\mathbb R^{r_1\times\cdots\times r_K}$ is the core tensor, and $\mathbf A_k\in\mathbb R^{d_k\times r_k}$, $k\in[K]$, is called a mode-$k$ factor loading matrix. The product $\times_k$ is the tensor $k$-mode product.
''',[5],'Section 3 — tensor factor model, equation (3.1)',kind='source_passage',phrases=['tensor factor model'],symbols=[r'\mathcal X_t',r'\mathbf A_k'],shape='Tensor-valued observations with constant mean, Tucker common component and error tensor. Main-text descriptions of tensor operations are retained; appendix indexing conventions are unresolved.')
add('D2','Decomposition of error',r'''
Assume that
\[
\operatorname{mat}_k(\mathcal E_t)=(\boldsymbol\xi_{t,1}^{(k)},\ldots,\boldsymbol\xi_{t,d_{-k}}^{(k)}),\quad\text{where}\quad\boldsymbol\xi_{t,\ell}^{(k)}:=\boldsymbol\Psi_\ell^{(k)}\mathbf e_t^{(k)}+(\boldsymbol\Sigma_{\epsilon,\ell}^{(k)})^{1/2}\boldsymbol\epsilon_{t,\ell}^{(k)},\tag{3.5}
\]
with $E(\mathbf e_t^{(k)})=\mathbf0$, $E(\boldsymbol\xi_{t,\ell}^{(k)})=\mathbf0$, $\mathbf e_t^{(k)}\in\mathbb R^{r_e}$ independent of $\boldsymbol\epsilon_{s,\ell}^{(k)}$, $\boldsymbol\epsilon_{t,\ell}^{(k)}$ independent of $\boldsymbol\epsilon_{t,m}^{(k)}$ for $\ell\ne m$, $\operatorname{var}(\mathbf e_t^{(k)})=\mathbf I_{r_e}$ and $\operatorname{var}(\boldsymbol\epsilon_{t,\ell}^{(k)})=\mathbf I_{d_k}$ for each $s,t\in[T]$, $\ell,m\in[d_{-k}]$, $k\in[K]$. Also, each $\boldsymbol\Sigma_{\epsilon,\ell}^{(k)}$ has non-vanishing diagonals with $\|\boldsymbol\Sigma_{\epsilon,\ell}^{(k)}\|_{max}=O(1)$ and $\operatorname{tr}(\boldsymbol\Sigma_{\epsilon,\ell}^{(k)})=O(d_k)$, where $\operatorname{tr}(\cdot)$ is the trace of a square matrix. Moreover, define $\boldsymbol\Psi^{(k)}:=\sum_{\ell=1}^{d_{-k}}\boldsymbol\Psi_l^{(k)}$ and $\boldsymbol\Sigma_\epsilon^{(k)}:=\sum_{\ell=1}^{d_{-k}}\boldsymbol\Sigma_{\epsilon,\ell}^{(k)}$. Then we assume $\|\boldsymbol\Psi^{(k)}\boldsymbol\Psi^{(k)\top}\|=O(d_{-k})$ and $\|\boldsymbol\Sigma_\epsilon^{(k)}\|=O(d_{-k})$.
''',[6],'Assumption (E1) (Decomposition of error)',{'D1':'E1 decomposes each mode-k fiber of the model error tensor.'},kind='assumption',context='Decomposition of error',phrases=['(E1)'],symbols=[r'\boldsymbol\Sigma_{\epsilon,\ell}^{(k)}'],shape='Fiber error decomposition with shared low-dimensional component, independent idiosyncratic components, variance and aggregate norm bounds; no independence of noise from the core factors is added.')
add('D3','Time series',r'''
The elements in $\mathbf e_t^{(k)}=(e_{t,j}^{(k)})$ and $\boldsymbol\epsilon_{t,\ell}^{(k)}=(\epsilon_{t,\ell,j}^{(k)})$ are following weakly stationary general linear processes, such that with $\ell\in[d_{-k}]$, $t\in[T]$ and $k\in[K]$,
\[
e_{t,j}^{(k)}=\sum_{q\geq0}a_{e,q}z_{e,t-q,j}^{(k)},\quad j\in[r_e],\qquad\epsilon_{t,\ell,j}^{(k)}=\sum_{q\geq0}a_{\epsilon,q}z_{\epsilon,t-q,\ell,j}^{(k)},\quad j\in[d_k],
\]
where the coefficients $a_{e,q}$ and $a_{\epsilon,q}$ are such that $\sum_{q\geq0}a_{e,q}^2=\sum_{q\geq0}a_{\epsilon,q}^2=1$ and $\sum_{q\geq0}|a_{e,q}|\leq C$, $\sum_{q\geq0}|a_{\epsilon,q}|\leq C$ for some constant $C$. For each $k\in[K]$, the series of random variables $\{z_{e,t,j}^{(k)}\}$ and $\{z_{\epsilon,t,\ell,j}^{(k)}\}$ are independent of each other, with i.i.d. elements having mean 0 and variance 1.
''',[7],'Assumption (E2) (Time series)',{'D2':'The linear processes are the common and idiosyncratic error coordinates introduced in E1.'},kind='assumption',context='Time series',phrases=['(E2)'],symbols=[r'a_{e,q}',r'a_{\epsilon,q}'],shape='Stationary error linear processes with l2-normalized, absolutely summable filters and mutually independent iid innovation families.')
add('D4','general linear processes',r'''
Let $\mathbf f_{t,\ell}^{(k)}=(f_{t,\ell,j}^{(k)})$ be the $\ell$-th column vector in $\operatorname{mat}_k(\mathcal F_t)$, $\ell\in[r_{-k}]$, where $r_{-k}:=\prod_{\ell\ne k}r_\ell$. We assume that $\operatorname{var}(\mathbf f_{t,\ell}^{(k)})=\mathbf I_{r_k}$ (the identity matrix with size $r_k$), and $\operatorname{cov}(\mathbf f_{t,\ell_1}^{(k)},\mathbf f_{t,\ell_2}^{(k)})=\mathbf0$ for $\ell_1\ne\ell_2$. Then we can write
\[
f_{t,\ell,j}^{(k)}=\sum_{q\geq0}a_{f,q}z_{f,t-q,\ell,j}^{(k)},\quad j\in[r_k],
\]
where we have $\sum_{q\geq0}a_{f,q}^2=1$ and $\sum_{q\geq0}|a_{f,q}|\leq C$ for some constant $C$. For each $k\in[K]$, the series of random variables $\{z_{f,t,\ell,j}^{(k)}\}$ has i.i.d. elements having zero mean and variance 1.
''',[7],'Assumption (F1)',{'D1':'F1 constrains the core tensor fibers in the tensor factor model.'},kind='assumption',context='Similar to (E2), the factors in $\mathcal F_t$ are assumed to follow general linear processes.',phrases=['(F1)'],symbols=[r'a_{f,q}'],shape='Core-factor fibers with identity marginal covariance, zero cross-fiber covariance and a normalized absolutely summable linear-process filter; this is distinct from E2.')
add('D5','Factor Strength',r'''
We assume that, for $k\in[K]$, $\mathbf A_k$ is of full rank, $r_k=o(T^{1/3})$, and as $d_k\to\infty$,
\[
\mathbf D_k^{-1/2}\mathbf A_k^\top\mathbf A_k\mathbf D_k^{-1/2}\to\boldsymbol\Sigma_{A,k},\tag{3.6}
\]
where $\mathbf D_k=\operatorname{diag}(\mathbf A_k^\top\mathbf A_k)$ is a diagonal matrix consisting of the diagonal elements of $\mathbf A_k^\top\mathbf A_k$, and $\boldsymbol\Sigma_{A,k}$ is positive definite with all eigenvalues bounded away from 0 and infinity. Let $(\mathbf D_k)_j$ be the $j$-th diagonal element of $\mathbf D_k$, then we assume $(\mathbf D_k)_j\asymp d_k^{\alpha_{k,j}}$ for $j\in[r_k]$, and $0<\alpha_{k,r_k}\leq\cdots\leq\alpha_{k,2}\leq\alpha_{k,1}\leq1$.
''',[8],'Assumption (L1) (Factor Strength)',{'D1':'The loading matrices and factor dimensions are those of model (3.1).'},kind='assumption',context='Factor Strength',phrases=['(L1)'],symbols=[r'\mathbf D_k',r'\alpha_{k,j}'],shape='Sequence-level factor-strength assumption, full rank, factor-count growth and nondegenerate normalized Gram limit; distinctness is separately L1-prime.')
add('D6','Signal Cancellation',r'''
For $k\in[K]$ and $j\in[r_k]$, define the growth rate $\kappa_{k,j}\in[0,1]$ of column sum to be such that $\sum_{i=1}^{d_k}(\mathbf A_k)_{ij}\asymp d_k^{\kappa_{k,j}}$ (or the smallest $\kappa_{k,j}$ such that $P(c_1d_k^{\kappa_{k,j}}\leq\sum_{i=1}^{d_k}(\mathbf A_k)_{ij}\leq c_2d_k^{\kappa_{k,j}})=1$ for constants $c_1,c_2$ when $\mathbf A_k$ has random entries). It measures how close the column sum of $\mathbf A_k$ is to 0. For each $k\in[K]$, let $s_k=\sum_{j=1}^{r_k}\left(\sum_{i=1}^{d_k}(\mathbf A_k)_{ij}\right)^2\asymp\sum_{j=1}^{r_k}d_k^{2\kappa_{k,j}}$, and $s_{-k}:=\prod_{l=1;l\ne k}^K s_l$. We assume for $k\in[K]$ and $z_k\leq r_k$ (see Theorem 1 and the explanations thereafter as well),
\[
\frac{d_{-k}}{s_{-k}}\left(1+\frac{d_k}T\right)=o\left(d_k^{\alpha_{k,z_k}}\right).\tag{3.7}
\]
''',[8],'Assumption (L2) (Signal Cancellation)',{'D1':'The condition uses loading-matrix column sums and mode dimensions.'},kind='assumption',context='Signal Cancellation',phrases=['(L2)'],symbols=[r's_{-k}',r'\kappa_{k,j}'],shape='Full-fiber column-sum scaling and signal-cancellation inequality. In Theorem 2 it is instantiated separately on every chosen random sample; it is not imposed on the full population by Theorem 4.')
add('D7','singular value decomposition',r'''
For convenience of further theoretical analysis, we define $\mathbf Q_k=\mathbf A_k\mathbf D_k^{-1/2}$. Then the subspace spanned by the columns of $\mathbf Q_k$ and $\mathbf A_k$ are the same. Since $\mathbf Q_k^\top\mathbf Q_k\to\boldsymbol\Sigma_{A,k}$, we can regard $\mathbf Q_k$ as a re-normalized version of $\mathbf A_k$ by normalising its factor strength. In addition, we apply the singular value decomposition of $\mathbf A_k$ as
\[
\mathbf A_k=\mathbf U_k\mathbf G_k^{1/2}\mathbf V_k^\top,\tag{3.8}
\]
where $\mathbf U_k\in\mathbb R^{d_k\times r_k}$ has orthogonal columns such that $\mathbf U_k^\top\mathbf U_k=\mathbf I_{r_k}$, $\mathbf G_k\in\mathbb R^{r_k\times r_k}$ is diagonal and consists of the eigenvalues of $\mathbf A_k^\top\mathbf A_k$ in decreasing order, and $\mathbf V_k\in\mathbb R^{r_k\times r_k}$ is an orthogonal matrix.
''',[9],'Section 3.1.3 — loading normalization and singular value decomposition',{'D1':'The normalized loading matrix and its singular value decomposition are formed from A_k.','D5':'The source passage invokes the normalized Gram limit of L1.'},phrases=['singular value decomposition'],symbols=[r'\mathbf Q_k',r'\mathbf U_k'],shape='Normalized loading matrix and ordered SVD, including the source normalized-Gram-limit context.')
add('D8','singular values',r'''
The singular values on $\mathbf G_k$ are distinct.
''',[9],"Assumption (L1')",{'D7':'G_k is the diagonal matrix introduced with the loading SVD in (3.8).'},kind='assumption',phrases=["(L1')"],shape='Distinctness condition on G_k as printed, added only for eigenvector alignment clauses of Theorems 1, 2 and 4; all-assumptions imports in Theorems 6, 7 and 9 retain it.')
add('D9','summing all fibers',r'''
Denote $\widetilde{\mathbf x}_{t,k}=\sum_{i\in[d_{-k}]}\mathbf x_{t,-k,i}$, $\widetilde{\mathbf f}_{t,k}=\sum_{i\in[d_{-k}]}\mathbf f_{t,-k,i}$, $\mathbf e_{t,k}=\sum_{i\in[d_{-k}]}\mathbf e_{t,-k,i}$ and $\widetilde{\boldsymbol\mu}_k=\sum_{i\in[d_{-k}]}\boldsymbol\mu_{-k,i}$. Define $\ddot{\mathbf f}_{t,k}=\widetilde{\mathbf f}_{t,k}/s_{-k}^{1/2}$, write $\ddot{\mathbf F}_k=[\ddot{\mathbf f}_{1,k},\ldots,\ddot{\mathbf f}_{T,k}]\in\mathbb R^{r_k\times T}$ and $\widetilde{\mathbf F}_k=[\widetilde{\mathbf f}_{1,k},\ldots,\widetilde{\mathbf f}_{T,k}]$. Similarly, denote $\ddot{\mathbf x}_{t,k}=\widetilde{\mathbf x}_{t,k}/s_{-k}^{1/2}$ and $\ddot{\mathbf X}_k=(\ddot{\mathbf x}_{1,k},...,\ddot{\mathbf x}_{T,k})^\top\in\mathbb R^{T\times d_k}$, $\widetilde{\mathbf X}_k=(\widetilde{\mathbf x}_{1,k},...,\widetilde{\mathbf x}_{T,k})^\top$. Also let $\ddot{\mathbf e}_{t,k}=\mathbf e_{t,k}/s_{-k}^{1/2}$, $\ddot{\mathbf E}_k=(\ddot{\mathbf e}_{1,k},...,\ddot{\mathbf e}_{T,k})^\top$ and $\widetilde{\mathbf E}_k=(\mathbf e_{1,k},...,\mathbf e_{T,k})^\top$. Finally, let $\ddot{\boldsymbol\mu}_k=\widetilde{\boldsymbol\mu}_k/s_{-k}^{1/2}$. Then,
\[
\ddot{\mathbf X}_k=\mathbf1_T\ddot{\boldsymbol\mu}_k^\top+\ddot{\mathbf F}_k^\top\mathbf A_k^\top+\ddot{\mathbf E}_k,\tag{3.9}
\]
where $\mathbf1_T$ is a column vector of $T$ ones.
''',[9],'Section 3.1.3 — sums of all mode fibers',{'D1':'These sums use the mode-fiber representation of model (3.1), with its main-text formula (3.3) archived among ambient conventions.'},context='Estimator based on summing all fibers',symbols=[r'\ddot{\mathbf F}_k',r'\widetilde{\mathbf X}_k'],shape='All-fiber sums and their square-root column-sum normalization. Only scalar definitions of s are needed to define these data; the L2 rate inequality is a separate condition.')
add('D10','pseudo data covariance matrix',r'''
\[
\widehat{\boldsymbol\Sigma}_{\widetilde{\mathbf x}_k}=\frac{\widetilde{\mathbf X}_k^\top(\mathbf I_T-\frac1T\mathbf1_T\mathbf1_T^\top)\widetilde{\mathbf X}_k}T,
\]
where $\mathbf I_T$ is a $T\times T$ identity matrix. Suppose we do not know the true number of factor $r_k$, and start with an arbitrary $z_k$ with $z_k\leq r_k$; then we can obtain $\widehat{\mathbf Q}_{k,(z_k)}$ as the $z_k$ largest eigenvectors of $\widehat{\boldsymbol\Sigma}_{\widetilde{\mathbf x}_k}$, with normalization $\widehat{\mathbf Q}_{k,(z_k)}^\top\widehat{\mathbf Q}_{k,(z_k)}=\mathbf I_{z_k}$. Let $\widetilde{\mathbf V}_k$ be the $z_k\times z_k$ diagonal matrix of the first $z_k$ largest eigenvalues of $\widehat{\boldsymbol\Sigma}_{\widetilde{\mathbf x}_k}$ in decreasing order, and $\ddot{\mathbf V}_k:=\widetilde{\mathbf V}_k/s_{-k}$.
''',[10],'Section 3.2 — full-fiber covariance and PCA estimator',{'D9':'The covariance and estimator are computed from the full-fiber summed data matrix.'},context='We perform PCA on the “pseudo data covariance matrix” of $\widetilde{\mathbf x}_{t,k}$, which is',symbols=[r'\widehat{\mathbf Q}_{k,(z_k)}',r'\ddot{\mathbf V}_k'],shape='Centered sample covariance of full-fiber sums, ordered leading eigenvectors and scaled eigenvalues; z_k is supplied, positive and no larger than r_k.')
members['D10']['naming_context'][0]['evidence']=[dict(page=9,location='Section 3.2, sentence continued on page 10'),dict(page=10,location='Section 3.2, continuation')]
add('D11','random sampling',r'''
Suppose we perform $M_0$ random sampling of the $d_{-k}$ mode-$k$ fibres, corresponding to randomly choosing an index set $S_m\subseteq[d_{-k}]$ for the $m$-th sample. (In practice, we can sample $S_m\subseteq[d_{-k}]$ directly. However, for theoretical analysis and practical performance control, we may need to first sample $S_{l,m}\subseteq[d_l]$ for $l\ne k$, and then let $S_m:=\prod_{l\in[K]\setminus\{k\}}S_{l,m}$ to be the Cartesian product, to facilitate the definition of $s_{-k,m}$. See (3.12) and the explanations thereafter.) Then, for each random sample, we can obtain an estimator $\widehat{\mathbf Q}_{k,m,(z_k)}$ based on summing the $S_m$ mode-$k$ fibers of $\mathcal X_t$.

where $d_{-k,m}$, $s_{-k,m}$ and $\widehat{\mathbf U}_{k,m,(z_k)}$ are defined in parallel to $d_{-k}$, $s_{-k}$ and $\widehat{\mathbf U}_{k,(z_k)}$ respectively, but for the $m$-th sample.
''',[11,12],'Section 3.3.1 — random fiber subsets and sample-local notation',{'D1':'The sampled observations are subsets of the mode-k fibers of the model tensor.'},phrases=['random sampling'],symbols=[r'S_m',r's_{-k,m}'],shape='Random fiber subsets, optionally Cartesian products, and sample-local sums and normalization conventions; full-population L2 is not imposed on these objects.')
members['D11']['excerpt_selection']='Two original defining passages separated by the displayed derived rates (3.12)-(3.13), which are not needed to define random sampling.'
add('D12','eigenvalue ratios',r'''
\[
ER_{m,j}:=\frac{\lambda_1\left(\frac{\widetilde{\mathbf X}_{k,m}^\top(\mathbf I_T-\frac1T\mathbf1_T\mathbf1_T^\top)\widetilde{\mathbf X}_{k,m}}T\right)}{\lambda_j\left(\frac{\widetilde{\mathbf X}_{k,m}^\top(\mathbf I_T-\frac1T\mathbf1_T\mathbf1_T^\top)\widetilde{\mathbf X}_{k,m}}T\right)}
\]
''',[12],'Section 3.3.1 — defining quotient in equation (3.14)',{'D11':'Each ratio is computed from the centered covariance of the m-th sampled fiber sum.'},context='Therefore, the above eigenvalue ratios of the covariance matrix of the $m$-th sample can help measure the quantity',symbols=[r'ER_{m,j}'],shape='Ratio of the largest to the j-th sample covariance eigenvalue. The subsequent asymptotic comparison in (3.14) is not part of this defining quotient and requires additional assumptions.')
members['D12']['excerpt_selection']='Exact defining quotient before the asymptotic equivalence in equation (3.14).'
add('D13','maximum eigenvalue ratio estimator',r'''
Hence in practice, for each random sample, we can compute $ER_{m,j}$ for some $j$ satisfying $r_k+1\leq j\leq\lfloor c\min(T,d_k)\rfloor-r_k$. Then, we can choose the sample with the largest $ER_{m,j}$, and obtain the estimator $\widehat{\mathbf Q}_{k,max,(z_k)}$ based on this sample accordingly. We call $\widehat{\mathbf Q}_{k,max,(z_k)}$ the maximum eigenvalue ratio estimator.
''',[12],'Section 3.3.1 — maximum eigenvalue ratio estimator',{'D12':'The selected sample maximizes ER_m,j.','D11':'The selected-sample estimator uses its fiber-sum PCA construction.'},phrases=['maximum eigenvalue ratio estimator'],symbols=[r'\widehat{\mathbf Q}_{k,max,(z_k)}'],shape='PCA estimator for the sample maximizing a specified eigenvalue ratio in the stated j-range; no tie resolution is supplied.')
add('D14','pre-averaging estimator',r'''
More specifically, suppose we have $M_0$ random samples. Among them, we choose $M$ samples with the largest eigenvalue ratios $ER_{m,j}$ as stated in the previous subsection. Then, we can calculate an aggregated covariance matrix of these $M$ chosen samples as
\[
\widehat{\boldsymbol\Sigma}_{\widetilde{\mathbf x}_k,agg}:=\frac1M\sum_{m=1}^M\frac{\widetilde{\mathbf X}_{k,m}^\top(\mathbf I_T-\frac1T\mathbf1_T\mathbf1_T^\top)\widetilde{\mathbf X}_{k,m}}T,
\]
where $\widetilde{\mathbf X}_{k,m}$ is defined similar to $\widetilde{\mathbf X}_k$, with the subscript $m$ indicating that the data comes from the $m$-th random sample (we define $\widetilde{\mathbf F}_{k,m}$ and $\widetilde{\mathbf E}_{k,m}$ similarly as in (3.9)). The pre-averaging estimator $\widehat{\mathbf Q}_{k,pre,(z_k)}$ is defined as the $z_k$ eigenvectors corresponding to the $z_k$ largest eigenvalues of $\widehat{\boldsymbol\Sigma}_{\widetilde{\mathbf x}_k,agg}$, with the constraint $\widehat{\mathbf Q}_{k,pre,(z_k)}^\top\widehat{\mathbf Q}_{k,pre,(z_k)}=\mathbf I_{z_k}$.

Let $s_{-k,pre}:=\frac1M\sum_{m=1}^M s_{-k,m}$, $\widetilde{\mathbf V}_{k,pre}$ be the $z_k\times z_k$ diagonal matrix of the first $z_k$ largest eigenvalues of $\widehat{\boldsymbol\Sigma}_{\widetilde{\mathbf x}_k,agg}$ in decreasing order, and $\ddot{\mathbf V}_{k,pre}:=\widetilde{\mathbf V}_{k,pre}/s_{-k,pre}$.
''',[13],'Section 3.3.2 — pre-averaging estimator',{'D12':'The M selected samples have the largest ER_m,j ratios.','D11':'Each covariance uses the sampled fiber sums and sample-local normalization quantities.'},phrases=['pre-averaging estimator'],symbols=[r'\widehat{\mathbf Q}_{k,pre,(z_k)}',r's_{-k,pre}'],shape='Leading eigenspace of the average of selected sample covariances, with selected-sample average signal normalization; its construction does not itself impose R2 or L2-prime.')
add('D15','uniformly bounded fourth moments',r'''
The elements in $\{z_{f,t,\ell,j}^{(k)}\}$ from Assumption (F1), and those in $\{z_{e,t,j}^{(k)}\}$ and $\{z_{\epsilon,t,\ell,j}^{(k)}\}$ from Assumption (E2) have uniformly bounded fourth moments.
''',[8],'Assumption (R1)',{'D3':'R1 bounds the fourth moments of the error innovations from E2.','D4':'R1 also bounds the factor innovations from F1.'},kind='assumption',phrases=['(R1)','uniformly bounded fourth moments'],shape='Uniform fourth-moment bounds on all stated innovation families; no Gaussian or sub-Gaussian restriction.')
add('D16','uniformly bounded below',r'''
We assume $\lambda_{d_k}(\boldsymbol\Sigma_{\epsilon,l}^{(k)})$ is uniformly bounded below from 0 for $l\in[d_{-k}]$, so that $\lambda_{d_k}\left(\sum_{l\in S_m}\boldsymbol\Sigma_{\epsilon,l}^{(k)}\right)\geq c|S_m|$ holds for any random subsets $S_m\subseteq[d_{-k}]$ for some constant $c>0$. Let $\mathbf A_{\epsilon,T}$ be the $T\times T$ matrix with its $(t,s)$ element to be $(\mathbf A_{\epsilon,T})_{t,s}=\sum_{q\geq0}a_{\epsilon,q}a_{\epsilon,q+|t-s|}$. Denote $0<y:=\lim_{d_k,T\to\infty}\frac{\min(d_k,T)}{\max(d_k,T)}\leq1$ and $y^*=\min(y,1)$, then we assume there exists $c_1\in(1-y^*,1]$ such that $\lambda_{\lfloor c_1T\rfloor}(\mathbf A_{\epsilon,T})>c_2>0$ for large $T$, where $c_2$ is a positive constant.
''',[12],'Assumption (R2)',{'D2':'R2 strengthens the noise covariance lower-eigenvalue conditions.','D3':'Its temporal covariance matrix is built from the E2 idiosyncratic filter.'},kind='assumption',phrases=['(R2)'],shape='Uniform noise eigenvalue lower bound and a temporal covariance quantile lower bound with positive limiting aspect ratio. A_epsilon,T here is T-by-T, distinct from the rectangular filter matrix in RE1.')
add('D17','Signal Cancellation of maximum eigenvalue ratio sample',r'''
For $k\in[K]$, define
\[
s_{k,max}:=\max_{S_{k,m}\in\{S_{k,m}\subseteq[d_k]:m\in[M_{k,0}],\ |S_{k,m}|=n_k\}}\left[\sum_{j=1}^{r_k}\left(\sum_{i\in S_{k,m}}(\mathbf A_k)_{ij}\right)^2\right],\tag{3.17}
\]
and $s_{-k,max}:=\prod_{l\in[K]\setminus\{k\}}s_{l,max}$. Then we assume
\[
\frac{d_{-k}}{s_{-k,max}}\left(1+\frac{d_k}T\right)=o\left(d_k^{\alpha_{k,z_k}}\right),
\]
for some $z_k\leq r_k$. (If $z_k=1$, then the assumption is most relaxed.)
''',[15],"Assumption (L2') (Signal Cancellation of maximum eigenvalue ratio sample)",{'D11':'The maximum ranges over sampled row subsets of fixed size for each mode.'},kind='assumption',context='Signal Cancellation of maximum eigenvalue ratio sample',phrases=["(L2')"],symbols=[r's_{-k,max}'],shape='Sampled maximum column-sum cancellation bound with existential z_k; distinct from the full-sum L2 assumption.')
add('D18','largest eigenvalue ratios',r'''
In (3.17), $M_{k,0}$ is the number of random row sums we consider for $\mathbf A_k$, so that for $k\in[K]$, the number of random samples from the $d_{-k}$ fibres is $M_0=\prod_{j\in[K]\setminus\{k\}}M_{j,0}$. Assumption (L2') is parallel to Assumption (L2), except that it is made on the maximum eigenvalue ratio sample, which corresponds to the maximum eigenvalue ratio estimator. And for the pre-averaging estimator, we assume that the $M$ samples we choose all satisfy $s_{l,m}\asymp s_{l,max}$ as $M_0$ is large enough (by choosing the $M$ samples with the largest eigenvalue ratios as defined in (3.14)).
''',[15],'Section 3.3.2 — selected-sample scaling convention before Theorem 4',{'D17':'The selected-sample scales are compared to the maxima in L2-prime.','D12':'Samples are selected using the ratios in (3.14).'},kind='condition',phrases=['largest eigenvalue ratios'],symbols=[r's_{l,m}\asymp s_{l,max}'],shape='Source assumption linking each selected sample scale to the maximum in the population-parameter restatement; not imposed by Theorem 2.')
add('D19','projected data',r'''
From (3.2), using the notation $\overline{\mathbf w}$ to denote the sample mean of $\{\mathbf w_t\}$, we have
\[
\operatorname{mat}_k(\mathcal X_t-\overline{\mathcal X})=\mathbf A_k\operatorname{mat}_k(\mathcal F_{t,-k}-\overline{\mathcal F}_{\cdot,-k})+\operatorname{mat}_k(\mathcal E_t-\overline{\mathcal E})=\mathbf A_k\operatorname{mat}_k(\mathcal F_t-\overline{\mathcal F})\mathbf A_{-k}^\top+\operatorname{mat}_k(\mathcal E_t-\overline{\mathcal E}),
\]
where $\mathbf A_{-k}:=\mathbf A_K\otimes\cdots\otimes\mathbf A_{k+1}\otimes\mathbf A_{k-1}\otimes\cdots\otimes\mathbf A_1$, with $\otimes$ denoting the Kronecker product. Suppose we have $\mathbf q_k=\mathbf A_k\mathbf c_k$ where $\mathbf c_k$ is a non-zero vector, $k\in[K]$. Define
\[
\mathbf q_{-k}:=\mathbf q_K\otimes\cdots\otimes\mathbf q_{k+1}\otimes\mathbf q_{k-1}\otimes\cdots\otimes\mathbf q_1=\mathbf A_{-k}\mathbf c_{-k},
\]
where $\mathbf c_{-k}:=\mathbf c_K\otimes\cdots\otimes\mathbf c_{k+1}\otimes\mathbf c_{k-1}\otimes\cdots\otimes\mathbf c_1$. Then we can define the new projected data as
\[
\mathbf y_t^{(k)}:=\operatorname{mat}_k(\mathcal X_t-\overline{\mathcal X})\mathbf q_{-k}=\mathbf A_k\operatorname{mat}_k(\mathcal F_t-\overline{\mathcal F})\mathbf A_{-k}^\top\mathbf A_{-k}\mathbf c_{-k}+\operatorname{mat}_k(\mathcal E_t-\overline{\mathcal E})\mathbf q_{-k}.\tag{4.1}
\]
''',[17],'Section 4 — projected data, equation (4.1)',{'D1':'The projection uses the centered tensor model and its mode-k unfolding.'},phrases=['projected data'],symbols=[r'\mathbf q_{-k}',r'\mathbf y_t^{(k)}'],shape='Centered mode unfolding multiplied by the descending-order Kronecker product of other-mode directions. The displayed ideal-direction expansion is distinguished from substitution of estimated directions.')
add('D20','Iterative Projection Direction Refinement',r'''
1. Initialize $\check{\mathbf q}_k^{(0)}=\widehat{\mathbf q}_{k,pre}$ for each $k\in[K]$.
2. For $i\geq1$, at the $i$-th step, create projected data $\mathbf y_{t,i}^{(k)}:=\operatorname{mat}_k(\mathcal X_t-\overline{\mathcal X})\check{\mathbf q}_k^{(i-1)}$ for each $k\in[K]$.
3. For each $k\in[K]$, define $\check{\mathbf q}_k^{(i)}$ the eigenvector corresponding to the largest eigenvalue of
\[
\widetilde{\boldsymbol\Sigma}_{y,i}^{(k)}:=T^{-1}\sum_{t=1}^T\mathbf y_{t,i}^{(k)}\mathbf y_{t,i}^{(k)\top}.\tag{4.4}
\]
4. Replace $i$ by $i+1$. Go back to step 2. Stop until after the procedure has been repeated for a fixed number of times.
''',[18],'Algorithm for Iterative Projection Direction Refinement',{'D14':'Initialization uses the one-column pre-averaging estimator, as identified on page 17.','D19':'The algorithm iterates the projected-data construction of (4.1), subject to the printed k versus minus-k inconsistency.'},kind='source_passage',context='Algorithm for Iterative Projection Direction Refinement',symbols=[r'\check{\mathbf q}_k^{(i)}',r'\widetilde{\boldsymbol\Sigma}_{y,i}^{(k)}'],shape='Four-step iterated projection and leading-eigenvector algorithm with fixed iteration count; step 2 prints q_k rather than the other-mode product q_-k. This is preserved and separately flagged.')
add('D21','uniformly bounded above',r'''
For a positive integer $N$, let $\mathcal A_{f,T}\in\mathbb R^{(N+1)T\times T}$ be defined as $\mathcal A_{f,T}:=(\mathbf a_{f,1},\ldots,\mathbf a_{f,T})$, where
\[
\mathbf a_{f,t}:=(\mathbf0_{t-1}^\top,a_{f,NT},a_{f,NT-1},\ldots,a_{f,0},\mathbf0_{T-t}^\top)^\top,\quad t\in[T],
\]
with $\mathbf0_j$ being a column vector of $j$ zeros and the $a_{f,q}$'s are from Assumption (F1). Define $\mathcal A_{e,T}$ and $\mathcal A_{\epsilon,T}$ similarly using coefficients from $\{a_{e,q}\}$ and $\{a_{\epsilon,q}\}$ respectively from Assumption (E2). Then we assume that (with $\mathcal A$ can be either $\mathcal A_{f,T}$, $\mathcal A_{e,T}$ or $\mathcal A_{\epsilon,T}$) $\|\mathcal A\|$ is uniformly bounded above, and
\[
\frac1T\operatorname{tr}(\mathcal A^\top\mathcal A)=1-o(T^{-2}d^{-4}),\quad\frac1T\operatorname{tr}(\mathcal A^\top\mathcal A)^2\to a_1,\quad\frac1{T^2}\mathbf1_T^\top(\mathcal A^\top\mathcal A)^2\mathbf1_T\to a_2,\quad\frac1{T^{3/2}}\mathbf1_T^\top\mathcal A^\top\mathcal A\mathbf1_T\to a_3,
\]
where $\mathbf1_T$ is a column vector of $T$ ones, and the constant $a_1$ can be $a_{1,f}$, $a_{1,e}$ and $a_{1,\epsilon}$ for $\mathcal A=\mathcal A_{f,T}$, $\mathcal A_{e,T}$ and $\mathcal A_{\epsilon,T}$ respectively. Similarly for constants $a_2$ and $a_3$.
''',[19],'Assumption (RE1)',{'D3':'The two error-filter matrices use the coefficients defined in E2.','D4':'The factor-filter matrix uses F1 coefficients.'},kind='assumption',phrases=['(RE1)'],symbols=[r'\mathcal A_{f,T}'],shape='Rectangular finite-filter matrices, uniform operator bound and four trace/quadratic-form limits; original placement of the square after tr is preserved without resolving its interpretation.')
add('D22','Model Parameters',r'''
For each $k\in[K]$, we assume that for each $j\in[d_k]$, $\lambda_j(\operatorname{diag}(\mathbf A_k\mathbf A_k^\top))$ is uniformly bounded away from 0 and infinity as $T,d_k\to\infty$. Moreover, $r_k=o(d_k^{1-\alpha_{k,1}+\alpha_{k,r_k}})$, and
\[
\max_{j\in[d_{-k}]}\|\boldsymbol\Sigma_{\epsilon,j}^{(k)}\|,\ r_eS_\psi^{(k)}=o\left(\prod_{j=1;j\ne k}^K d_j^{\alpha_{j,1}}\right)\ \text{and }d_k=O(r_eS_\psi^{(k)}).
\]
''',[23],'Assumption (RE2) (Model Parameters)',{'D1':'RE2 constrains row norms and dimensions of the tensor loading matrices.','D2':'The noise norm and S_psi are built from the E1 covariance and common-error loading matrices.'},kind='assumption',context='Model Parameters',phrases=['(RE2)'],symbols=[r'S_\psi^{(k)}'],shape='Uniform positive loading-row norm bounds and noise/dimension growth restrictions, with factor-strength exponents supplied as notation; does not automatically impose all of L1 or Theorem 6.')
add('D23','expected value',r'''
\[
\boldsymbol\Sigma_{y,m+1}^{(k)}:=\check g_{-k}\mathbf A_k\mathbf A_k^\top+\sum_{j=1}^{d_{-k}}(\check{\mathbf q}_{-k}^{(m)})_j^2\boldsymbol\Sigma_{\epsilon,j}^{(k)}+\left(\sum_{j=1}^{d_{-k}}(\check{\mathbf q}_{-k}^{(m)})_j\boldsymbol\Psi_j^{(k)}\right)^{\otimes2},\tag{5.4}
\]
where for any matrix $A$ we define $A^{\otimes2}:=AA^\top$. Apart from $\check{\mathbf q}_{-k}^{(m)}$, the matrix $\boldsymbol\Sigma_{y,m+1}^{(k)}$ is not random, and is in fact the expected value of $\widetilde{\boldsymbol\Sigma}_{y,m+1}^{(k)}$, pretending that $\check{\mathbf q}_{-k}^{(m)}$ is a constant vector.
''',[23],'Section 5.1 — covariance expression (5.4)',{'D1':'The signal part uses the tensor loading matrix.','D2':'The two noise terms use the covariance and cross-fiber loading matrices in E1.','D20':'The supplied direction is the m-th iterated projection direction.','D19':'The other-mode product direction and A_-k determine the scalar check-g in (5.3), archived among ambient conventions.'},phrases=['expected value'],symbols=[r'\boldsymbol\Sigma_{y,m+1}^{(k)}'],shape='Explicit population-style covariance formula with estimated direction held fixed, not a claim about actual conditional expectation given that random direction.')
add('D24','correlation matrix',r'''
With the projected data and the associated covariance matrix $\widetilde{\boldsymbol\Sigma}_{y,m+1}^{(k)}$ defined in (4.4), we can, for each $k\in[K]$, form the correlation matrix
\[
\widetilde{\mathbf R}_{y,m+1}^{(k)}:=\operatorname{diag}^{-1/2}(\widetilde{\boldsymbol\Sigma}_{y,m+1}^{(k)})\widetilde{\boldsymbol\Sigma}_{y,m+1}^{(k)}\operatorname{diag}^{-1/2}(\widetilde{\boldsymbol\Sigma}_{y,m+1}^{(k)}).\tag{5.1}
\]
''',[22],'Section 5 — sample correlation matrix, equation (5.1)',{'D20':'The correlation is formed from the iterated projected-data covariance in (4.4).'},phrases=['correlation matrix'],symbols=[r'\widetilde{\mathbf R}_{y,m+1}^{(k)}'],shape='Diagonal inverse-square-root normalization of the sample projected covariance; distinct from the population-style correlation defined inside Theorem 8.')
add('D25','Core Tensor Rank Estimation',r'''
Our estimator for $r_k$ for each $k\in[K]$ is then defined to be
\[
\widehat r_k:=\max\{j:\lambda_j(\widetilde{\mathbf R}_{y,m+1}^{(k)})>1+\eta_T,\ j\in[d_k]\},\tag{5.2}
\]
where $\eta_T\to0$ as $T\to\infty$ and its practical choice will be discussed in Section 5.2.
''',[22],'Section 5 — core rank estimator, equation (5.2)',{'D24':'The estimator is the largest index of a sample correlation eigenvalue exceeding 1+eta_T.'},context='Core Tensor Rank Estimation Using Projected Data',phrases=['estimator'],symbols=[r'\widehat r_k'],shape='Maximum eigenvalue index above a vanishing positive-offset threshold; no value for an empty maximum is provided in the source.')
# Record instantiated assumption scope without rewriting any original assumption.
for lid in ['D2','D3','D4','D5','D6','D15']:
    members[lid]['theorem_application_contexts']={PID+'/T2':dict(source_text='Let Assumption (E1), (E2), (F1), (L1), (L2), (R1) be satisfied for all $M$ chosen random samples, and',evidence=[dict(page=13,location='Theorem 2 opening')],interpretation='This theorem applies the numbered assumption to every selected sample. Sample-local dimensions and column-sum scales replace the corresponding population quantities; the condition is not asserted for the full-fiber sum.')}
members['D20']['evidence'].append(dict(page=17,location='Section 4.1, identification of q-hat-k-pre with the one-column estimator and plus-sign convention'))
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed local interfaces.')
