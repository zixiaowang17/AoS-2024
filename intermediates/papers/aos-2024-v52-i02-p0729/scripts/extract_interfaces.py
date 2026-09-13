"""Transcribe statement prerequisites from the inspected published paper, without supplements."""
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
add('D1','principal subspace',r'''
Imagine we are interested in $n$ independent random vectors $\mathbf x_j=[x_{1,j},\ldots,x_{d,j}]^\top\in\mathbb R^d$ drawn from the following distribution:
\[
\mathbf x_j\overset{\mathrm{ind.}}\sim\mathcal N(\mathbf0,\mathbf S^\star),\qquad1\leq j\leq n,\tag{1.1}
\]
where the unknown covariance matrix $\mathbf S^\star\in\mathbb R^{d\times d}$ is assumed to be rank-$r$ $(r<n)$ with eigendecomposition
\[
\mathbf S^\star=\mathbf U^\star\mathbf\Lambda^\star\mathbf U^{\star\top}.\tag{1.2}
\]
Here, the orthonormal columns of $\mathbf U^\star\in\mathbb R^{d\times r}$ constitute the $r$ leading eigenvectors of $\mathbf S^\star$, whereas $\mathbf\Lambda^\star\in\mathbb R^{r\times r}$ is a diagonal matrix whose diagonal entries are composed of the nonzero eigenvalues of $\mathbf S^\star$.
''',[1,2],'Section 1.1 — Gaussian-column PCA model, equations (1.1)-(1.2)',kind='source_passage',context=r'With the observed data $\{y_{l,j}|(l,j)\in\Omega\}$ in hand, can we perform statistical inference on the orthonormal matrix $\mathbf U^\star$—which embodies the ground-truth $r$-dimensional principal subspace underlying the vectors $\{\mathbf x_j\}_{1\leq j\leq n}$—and make inference on the underlying covariance matrix $\mathbf S^\star$.',symbols=[r'\mathbf x_j',r'\mathbf S^\star=\mathbf U^\star\mathbf\Lambda^\star\mathbf U^{\star\top}'],shape='Independent centered Gaussian columns with a rank-r covariance and a population principal subspace. The Gaussian formulation is the one printed in Theorem 1; the broader sub-Gaussian footnote is retained separately without changing covariance formulas.')
members['D1']['naming_context'][0]['evidence']=[dict(page=2,location='Section 1.1 — principal subspace terminology')]
add('D2','Random sampling',r'''
Random sampling: each index $(l,j)$ is contained in $\Omega$ independently with probability $p$;
''',[2],'Section 1.1 — Random sampling',kind='source_passage',phrases=['Random sampling'],symbols=[r'\Omega',r'$p$'.strip('$')],shape='Independent Bernoulli inclusion over [d] times [n] with common probability p. Independence of the sampling array from the signal/noise is used by the later conditional expectation identity; the bullet does not separately state that cross-independence.')
# Prefer the distinctive sampling set, rather than the common scalar p, as the highlight.
members['D2']['highlight_symbols']=[r'\Omega']
add('D3','Heteroskedastic random noise with unknown variance',r'''
Heteroskedastic random noise with unknown variance: the noise components $\{\eta_{l,j}\}$ are independently generated sub-Gaussian random variables obeying
\[
\mathbb E[\eta_{l,j}]=0,\qquad\mathbb E[\eta_{l,j}^2]=\omega_l^{\star2},\qquad\text{and}\qquad\|\eta_{l,j}\|_{\psi_2}=O(\omega_l^\star),
\]
where $\{\omega_l^\star\}_{1\leq l\leq d}$ denote the standard deviations that are a priori unknown, and $\|\cdot\|_{\psi_2}$ stands for the sub-Gaussian norm of a random variable (Vershynin (2018)). The noise levels $\{\omega_l^\star\}_{1\leq l\leq d}$ are allowed to vary across locations, so as to model the so-called heteroskedasticity of noise.
''',[2],'Section 1.1 — heteroskedastic observation noise',kind='source_passage',phrases=['Heteroskedastic random noise with unknown variance'],symbols=[r'\omega_l^{\star2}',r'\|\eta_{l,j}\|_{\psi_2}'],shape='Independent centered sub-Gaussian noise with row-specific variances shared across columns and uniformly bounded sub-Gaussian-to-standard-deviation ratios. Variances are unknown inputs to the population model, not supplied to the inference algorithms.')
add('D4','data matrix',r'''
\[
\mathbf X:=[\mathbf x_1,\ldots,\mathbf x_n]\in\mathbb R^{d\times n},\tag{2.1a}
\]
\[
\mathbf Y:=\mathcal P_\Omega(\mathbf X+\mathbf N)\in\mathbb R^{d\times n},\tag{2.1b}
\]
where $\mathcal P_\Omega$ has been defined in Section 1.4, and $\mathbf N\in\mathbb R^{d\times n}$ represents the noise matrix such that the $(l,j)$-th entry of $\mathbf N$ is given by $\eta_{l,j}$. In other words, $\mathbf Y$ encapsulates all the observed data $\{y_{l,j}|(l,j)\in\Omega\}$, with any entry outside $\Omega$ taken to be zero.
''',[4],'Section 2 — data matrices, equations (2.1a)-(2.1b)',{'D1':'X collects the independent signal vectors with population covariance S-star.','D2':'The sampling set Omega determines which entries are observed.','D3':'N contains the heteroskedastic observation noises eta.','D5':'P_Omega is the matrix projection keeping entries on Omega.'},context=r'In practice, however, one needs to extract information from the corrupted and incomplete data matrix $\mathbf Y$.',symbols=[r'\mathbf Y:=\mathcal P_\Omega(\mathbf X+\mathbf N)',r'\mathbf X:=[\mathbf x_1,\ldots,\mathbf x_n]'],shape='Zero-filled observation matrix, distinct from the unobserved Gaussian signal matrix. Missing entries are set to zero before rescaling by the sampling probability.')
add('D5','Euclidean projection',r'''
For any index set $\Omega$, the notation $\mathcal P_\Omega(\mathbf M)$ represents the Euclidean projection of a matrix $\mathbf M$ onto the subspace of matrices supported on $\Omega$, and define $\mathcal P_{\Omega^c}(\mathbf M):=\mathbf M-\mathcal P_\Omega(\mathbf M)$ as well. In addition, we denote by $\mathcal P_{\mathrm{diag}}(\mathbf G)$ the Euclidean projection of a square matrix $\mathbf G$ onto the subspace of matrices that vanish outside the diagonal, and define $\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf G):=\mathbf G-\mathcal P_{\mathrm{diag}}(\mathbf G)$.
''',[3],'Section 1.4 — coordinate, diagonal and off-diagonal matrix projections',phrases=['Euclidean projection'],symbols=[r'\mathcal P_\Omega',r'\mathcal P_{\mathrm{diag}}',r'\mathcal P_{\mathrm{off\text{-}diag}}'],shape='Entrywise matrix projections onto an arbitrary support, its complement, the diagonal and its complement. The block retains the source’s distinct constructions and does not identify them as one identical operator.')
add('D6','condition number',r'''
Recall that the eigendecomposition of the covariance matrix $\mathbf S^\star\in\mathbb R^{d\times d}$ (see (1.2)) is assumed to be $\mathbf U^\star\mathbf\Lambda^\star\mathbf U^{\star\top}$. We assume the diagonal matrix $\mathbf\Lambda^\star$ to be $\mathbf\Lambda^\star=\operatorname{diag}\{\lambda_1^\star,\ldots,\lambda_r^\star\}$, where the diagonal entries are given by the nonzero eigenvalues of $\mathbf S^\star$ obeying
\[
\lambda_1^\star\geq\cdots\geq\lambda_r^\star>0.
\]
The condition number of $\mathbf S^\star$ is denoted by
\[
\kappa:=\lambda_1^\star/\lambda_r^\star.\tag{3.1}
\]
We also find it helpful to introduce the square root of $\mathbf\Lambda^\star$ as follows:
\[
\mathbf\Sigma^\star=\operatorname{diag}\{\sigma_1^\star,\ldots,\sigma_r^\star\}=(\mathbf\Lambda^\star)^{1/2},\qquad\text{where }\sigma_i^\star=(\lambda_i^\star)^{1/2},\quad1\leq i\leq r.\tag{3.2}
\]
''',[5],'Section 3.1 — population spectral quantities, equations (3.1)-(3.2)',{'D1':'These eigenvalues, their square roots and their ratio belong to the population covariance S-star.'},phrases=['condition number'],symbols=[r'\kappa:=\lambda_1^\star/\lambda_r^\star',r'\sigma_i^\star=(\lambda_i^\star)^{1/2}',r'\mathbf\Sigma^\star'],shape='Positive population covariance eigenvalues, their ratio and diagonal square-root matrix. Kappa is an eigenvalue ratio, unlike the singular-value ratio kappa-natural in the separate matrix model.')
add('D7','Incoherence',r'''
The rank-$r$ matrix $\mathbf S^\star\in\mathbb R^{d\times d}$ defined in (1.2) is said to be $\mu$-incoherent if the following condition holds:
\[
\|\mathbf U^\star\|_{2,\infty}\leq\sqrt{\frac{\mu r}d}.\tag{3.3}
\]
Here, we recall that $\|\mathbf U^\star\|_{2,\infty}$ denotes the largest $\ell_2$ norm of all rows of the matrix $\mathbf U^\star$.
''',[6],'Definition 1 — Incoherence',{'D1':'The condition applies to the orthonormal population eigenvectors of S-star.'},context='Definition 1 (Incoherence).',phrases=['Incoherence'],symbols=[r'\|\mathbf U^\star\|_{2,\infty}',r'\sqrt{\frac{\mu r}d}'],shape='A row-norm upper bound on the population covariance eigenspace. It is equivalent to the source’s statement about U-star being mu-incoherent, but is distinct from the three simultaneous rectangular-matrix inequalities in Assumption 2.')
interfaces[-1]['lean_role']='predicate'
add('D8','orthogonal matrix',r'''
For a nonsingular matrix $\mathbf H\in\mathbb R^{k\times k}$ with SVD $\mathbf U_H\mathbf\Sigma_H\mathbf V_H^\top$, we denote by $\operatorname{sgn}(\mathbf H)$ the following orthogonal matrix:
\[
\operatorname{sgn}(\mathbf H):=\mathbf U_H\mathbf V_H^\top.\tag{1.4}
\]
''',[3,4],'Section 1.4 — matrix sign, equation (1.4)',phrases=['orthogonal matrix'],symbols=[r'\operatorname{sgn}(\mathbf H)'],shape='The orthogonal polar factor for a nonsingular square matrix, constructed from its SVD. The source does not define a choice at singular H; the rotations in Theorems 1/2 use H=U^T U-star.')
add('D9','Noise levels',r'''
The noise levels $\{\omega_i^\star\}_{1\leq i\leq d}$ obey
\[
\frac{\omega_{\max}^2}{\omega_{\min}^2}\leq\kappa_\omega\qquad\text{with}\qquad\omega_{\max}:=\max_{1\leq i\leq d}\omega_i^\star\quad\text{and}\quad\omega_{\min}:=\min_{1\leq i\leq d}\omega_i^\star.\tag{3.4}
\]
''',[6],'Assumption 1 — Noise levels',{'D3':'The ratio compares the largest and smallest row-specific noise standard deviations from the observation model.'},kind='assumption',context='Assumption 1 (Noise levels).',phrases=['Noise levels','Assumption 1'],symbols=[r'\kappa_\omega',r'\omega_{\max}',r'\omega_{\min}'],shape='Bounded variance ratio across rows, with the theorem imposing kappa_omega comparable to one. The source uses a quotient and gives no 0/0 convention when all noises vanish; zero-noise extensions are not silently added.')
add('D10','HeteroPCA',r'''
Input: data matrix $\mathbf Y$ (cf. (2.1b)), sampling rate $p$, rank $r$, maximum number of iterations $t_0$.

Initialization: set $\mathbf G^0=\dfrac1{np^2}\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf Y\mathbf Y^\top)$.

Updates: for $t=0,1,\ldots,t_0$ do
\[
(\mathbf U^t,\mathbf\Lambda^t)=\operatorname{eigs}(\mathbf G^t,r),
\]
\[
\mathbf G^{t+1}=\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf G^t)+\mathcal P_{\mathrm{diag}}(\mathbf U^t\mathbf\Lambda^t\mathbf U^{t\top})=\frac1{np^2}\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf Y\mathbf Y^\top)+\mathcal P_{\mathrm{diag}}(\mathbf U^t\mathbf\Lambda^t\mathbf U^{t\top}).
\]
Here, for any symmetric matrix $\mathbf G\in\mathbb R^{d\times d}$ and $1\leq r\leq d$, $\operatorname{eigs}(\mathbf G,r)$ returns $(\mathbf U,\mathbf\Lambda)$, where $\mathbf U\mathbf\Lambda\mathbf U^\top$ is the top-$r$ eigendecomposition of $\mathbf G$.

Output: $\mathbf U=\mathbf U^{t_0}$ as the subspace estimate, $\mathbf\Sigma=(\mathbf\Lambda^{t_0})^{1/2}$ as an estimate of $(\mathbf\Lambda^\star)^{1/2}$ and $\mathbf S=\mathbf U^{t_0}\mathbf\Lambda^{t_0}\mathbf U^{t_0\top}$ as the covariance matrix estimate.
''',[5],'Algorithm 2 — HeteroPCA',{'D4':'The input Y is the zero-filled noisy and incomplete PCA data matrix.','D5':'The iteration deletes the Gram diagonal and replaces it by the diagonal of the rank-r eigendecomposition.'},context='Algorithm 2 HeteroPCA (by Zhang, Cai and Wu (2022b))',phrases=['HeteroPCA'],symbols=[r'\mathbf U^{t_0}',r'\mathbf G^0',r'\operatorname{eigs}(\mathbf G^t,r)'],shape='The PCA-scaled diagonal-imputation iteration, returning U, Sigma and S at t_0. Eigenvector choices at ties, square roots of nonpositive eigenvalues, and a finite-sample failure convention are not specified. The inclusive loop and output index are retained exactly.')
add('D11','Confidence regions',r'''
Input: output $(\mathbf U,\mathbf\Sigma,\mathbf S)$ of Algorithm 2, sampling rate $p$, coverage level $1-\alpha$.

Compute estimates of the noise levels $\{\omega_l^\star\}_{1\leq l\leq d}$ as follows:
\[
\omega_l^2:=\frac{\sum_{j=1}^ny_{l,j}^2\,1_{(l,j)\in\Omega}}{\sum_{j=1}^n1_{(l,j)\in\Omega}}-S_{l,l}\qquad\text{for all}\quad1\leq l\leq d.
\]
Compute an estimate of $\mathbf\Sigma_{U,l}^\star$ (cf. (3.7)) as follows:
\[
\mathbf\Sigma_{U,l}:=\left(\frac{1-p}{np}\|\mathbf U_{l,\cdot}\mathbf\Sigma\|_2^2+\frac{\omega_l^2}{np}\right)\mathbf\Sigma^{-2}+\frac{2(1-p)}{np}\mathbf U_{l,\cdot}^\top\mathbf U_{l,\cdot}
+(\mathbf\Sigma)^{-2}\mathbf U^\top\operatorname{diag}\big([d_{l,i}]_{1\leq i\leq d}\big)\mathbf U(\mathbf\Sigma)^{-2},
\]
where
\[
d_{l,i}:=\frac1{np^2}\big[\omega_l^2+(1-p)\|\mathbf U_{l,\cdot}\mathbf\Sigma\|_2^2\big]\big[\omega_i^2+(1-p)\|\mathbf U_{i,\cdot}\mathbf\Sigma\|_2^2\big]+\frac{2(1-p)^2}{np^2}S_{l,i}^2.
\]
Compute the $(1-\alpha)$-quantile $\tau_{1-\alpha}$ of $\chi_r^2$ and construct a Euclidean ball:
\[
\mathcal B_{1-\alpha}:=\{\mathbf z\in\mathbb R^r:\|\mathbf z\|_2^2\leq\tau_{1-\alpha}\}.
\]
Output the $(1-\alpha)$-confidence region
\[
\mathrm{CR}_{U,l}^{1-\alpha}:=\mathbf U_{l,\cdot}+(\mathbf\Sigma_{U,l})^{1/2}\mathcal B_{1-\alpha}=\{\mathbf U_{l,\cdot}+(\mathbf\Sigma_{U,l})^{1/2}\mathbf z:\mathbf z\in\mathcal B_{1-\alpha}\}.
\]
''',[8],'Algorithm 3 — Confidence regions for principal-subspace rows',{'D10':'The fitted U, Sigma and S are outputs of the PCA HeteroPCA iteration.','D4':'The noise estimates use the observed y entries and their observed-row counts.','D2':'The supplied sampling probability p appears throughout the covariance estimate.'},context=r'Algorithm 3 Confidence regions for $\mathbf U_{l,\cdot}^\star$ $(1\leq l\leq d)$ based on HeteroPCA',phrases=['Confidence regions'],symbols=[r'\mathrm{CR}_{U,l}^{1-\alpha}',r'\mathbf\Sigma_{U,l}',r'\mathcal B_{1-\alpha}'],shape='Estimated row covariances transformed from a chi-square Euclidean ball to produce rowwise confidence regions. The algorithm prints no protection against empty observed rows, negative noise variance estimates or non-PSD covariance estimates. Standard row/column identification is implicit in adding a row to a transformed vector.')
add('D12','variance parameters',r'''
Before proceeding, let us define a set of variance parameters $\{v_{i,j}^\star\}_{1\leq i,j\leq d}$ which, as we shall demonstrate momentarily, correspond to the (approximate) variance of the entries of $\mathbf S$.

For any $1\leq i,j\leq d$ obeying $i\ne j$, we define
\[
v_{i,j}^\star:=\frac{2-p}{np}S_{i,i}^\star S_{j,j}^\star+\frac{4-3p}{np}S_{i,j}^{\star2}+\frac1{np}(\omega_i^{\star2}S_{j,j}^\star+\omega_j^{\star2}S_{i,i}^\star)
\]
\[
+\frac1{np^2}\sum_{k=1}^d\big\{[\omega_i^{\star2}+(1-p)S_{i,i}^\star][\omega_k^{\star2}+(1-p)S_{k,k}^\star]+2(1-p)^2S_{i,k}^{\star2}\big\}(\mathbf U_{k,\cdot}^\star\mathbf U_{j,\cdot}^{\star\top})^2
\]
\[
+\frac1{np^2}\sum_{k=1}^d\big\{[\omega_j^{\star2}+(1-p)S_{j,j}^\star][\omega_k^{\star2}+(1-p)S_{k,k}^\star]+2(1-p)^2S_{j,k}^{\star2}\big\}(\mathbf U_{k,\cdot}^\star\mathbf U_{i,\cdot}^{\star\top})^2.\tag{3.10}
\]
For any $1\leq i\leq d$, we set
\[
v_{i,i}^\star:=\frac{12-9p}{np}S_{i,i}^{\star2}+\frac4{np}\omega_i^{\star2}S_{i,i}^\star
\]
\[
+\frac4{np^2}\sum_{k=1}^d\big\{[\omega_i^{\star2}+(1-p)S_{i,i}^\star][\omega_k^{\star2}+(1-p)S_{k,k}^\star]+2(1-p)^2S_{i,k}^{\star2}\big\}(\mathbf U_{k,\cdot}^\star\mathbf U_{i,\cdot}^{\star\top})^2.\tag{3.11}
\]
''',[10],'Section 3.2.2 — population entrywise variances, equations (3.10)-(3.11)',{'D1':'The formulas use the population covariance S-star and its principal eigenspace U-star.','D2':'The variance factors depend on the sampling probability p.','D3':'The formulas retain the row-specific population noise variances.'},phrases=['variance parameters'],symbols=[r'v_{i,j}^\star',r'v_{i,i}^\star'],shape='Separate off-diagonal and diagonal population variances for covariance-entry inference. The diagonal formula is not obtained by simply substituting j=i into the off-diagonal formula. This body is defined in the main text and is not a proof-only object.')
add('D13','Confidence intervals',r'''
Input: output $(\mathbf U,\mathbf\Sigma,\mathbf S)$ of Algorithm 2, sampling rate $p$, coverage level $1-\alpha$.

Compute estimates of the noise level $\omega_l^\star$ as follows:
\[
\omega_l^2:=\frac{\sum_{j=1}^ny_{l,j}^2\,1_{(l,j)\in\Omega}}{\sum_{j=1}^n1_{(l,j)\in\Omega}}-S_{l,l}.
\]
Compute an estimate of $v_{i,j}^\star$ (cf. (3.10) or (3.11)) as follows: if $i\ne j$, then
\[
v_{i,j}:=\frac{2-p}{np}S_{i,i}S_{j,j}+\frac{4-3p}{np}S_{i,j}^2+\frac1{np}(\omega_i^2S_{j,j}^\star+\omega_j^2S_{i,i})
\]
\[
+\frac1{np^2}\sum_{k=1}^d\big\{[\omega_i^2+(1-p)S_{i,i}][\omega_k^2+(1-p)S_{k,k}]+2(1-p)^2S_{i,k}^2\big\}(\mathbf U_{k,\cdot}\mathbf U_{j,\cdot}^\top)^2
\]
\[
+\frac1{np^2}\sum_{k=1}^d\big\{[\omega_j^2+(1-p)S_{j,j}][\omega_k^2+(1-p)S_{k,k}]+2(1-p)^2S_{j,k}^2\big\}(\mathbf U_{k,\cdot}\mathbf U_{i,\cdot}^\top)^2.
\]
If $i=j$, then
\[
v_{i,i}:=\frac{12-9p}{np}S_{i,i}^2+\frac4{np}\omega_i^2S_{i,i}
\]
\[
+\frac4{np^2}\sum_{k=1}^d\big\{[\omega_i^2+(1-p)S_{i,i}][\omega_k^2+(1-p)S_{k,k}]+2(1-p)^2S_{i,k}^2\big\}(\mathbf U_{k,\cdot}\mathbf U_{i,\cdot}^\top)^2.
\]
Output the $(1-\alpha)$-confidence interval
\[
\mathrm{CI}_{i,j}^{1-\alpha}:=[S_{i,j}\pm\Phi^{-1}(1-\alpha/2)\sqrt{v_{i,j}}].
\]
''',[12],'Algorithm 4 — Confidence intervals for covariance entries',{'D10':'The plug-in U and S come from Algorithm 2.','D4':'The row-noise estimate uses observed data and observation counts.','D2':'The input probability p appears in all variance terms.','D12':'The instruction expressly targets the population variance parameters defined in (3.10)-(3.11); their two distinct cases explain which quantity each variance estimate is intended to estimate.','D1':'The printed off-diagonal variance formula unexpectedly retains the population entry S-star_jj, rather than its estimate. This literal source dependency is preserved and flagged.'},context=r'Algorithm 4 Confidence intervals for $S_{i,j}^\star$ $(1\leq i,j\leq d)$ based on HeteroPCA',phrases=['Confidence intervals'],symbols=[r'\mathrm{CI}_{i,j}^{1-\alpha}',r'\omega_i^2S_{j,j}^\star',r'v_{i,i}'],shape='Two-sided entrywise intervals with estimated variances, preserving the source’s unexplained population S-star_jj in the i-not-equal-j branch. This makes that printed branch not fully data-driven. It is not silently repaired. Empty-row, negative-variance and square-root conventions are also unspecified.')
add('D14','subspace estimation',r'''
Suppose that we are interested in a rank-$r$ matrix $\mathbf M^\natural\in\mathbb R^{n_1\times n_2}$, whose SVD is given by
\[
\mathbf M^\natural=\sum_{i=1}^r\sigma_i^\natural\mathbf u_i^\natural\mathbf v_i^{\natural\top}=\mathbf U^\natural\mathbf\Sigma^\natural\mathbf V^{\natural\top}\in\mathbb R^{n_1\times n_2}.\tag{6.1}
\]
Here, $\mathbf U^\natural=[\mathbf u_1^\natural,\ldots,\mathbf u_r^\natural]$ (resp., $\mathbf V^\natural=[\mathbf v_1^\natural,\ldots,\mathbf v_r^\natural]$) consists of orthonormal columns that correspond to the left (resp., right) singular vectors of $\mathbf M^\natural$, and $\mathbf\Sigma^\natural=\operatorname{diag}\{\sigma_1^\natural,\ldots,\sigma_r^\natural\}$ is a diagonal matrix consisting of the singular values of $\mathbf M^\natural$. Without loss of generality, we assume that
\[
n=\max\{n_1,n_2\}.
\]
It is assumed that the singular values are sorted (in magnitude) in descending order, namely
\[
\sigma_1^\natural\geq\cdots\geq\sigma_r^\natural\geq0,\tag{6.2}
\]
with the condition number denoted by
\[
\kappa^\natural:=\sigma_1^\natural/\sigma_r^\natural.\tag{6.3}
\]
What we have observed is a noisy copy of $\mathbf M^\natural$, namely
\[
\mathbf M=\mathbf M^\natural+\mathbf E,\tag{6.4}
\]
where $\mathbf E=[E_{i,j}]_{1\leq i,j\leq n}$ stands for a noise matrix. We focus on estimating the column subspace represented by $\mathbf U^\natural$ and the singular values encapsulated in $\mathbf\Sigma^\natural$, but not the row space $\mathbf V^\natural$.
''',[20],'Section 6.1 — general subspace model, equations (6.1)-(6.4)',kind='source_passage',context='For this reason, we refer to this setting as subspace estimation in order to differentiate it from matrix denoising, emphasizing that we are only interested in column subspace estimation.',symbols=[r'\mathbf M=\mathbf M^\natural+\mathbf E',r'\kappa^\natural:=\sigma_1^\natural/\sigma_r^\natural',r'n=\max\{n_1,n_2\}'],shape='A fixed rectangular rank-r signal plus independent-entry perturbation, with n=max(n_1,n_2). The source prints a square n-by-n index range for E despite the rectangular addition; that mismatch is preserved. The rank-r description supplies positive nonzero singular values even though the displayed ordering ends with >=0.')
add('D15','Incoherence',r'''
The rank-$r$ matrix $\mathbf M^\natural\in\mathbb R^{n_1\times n_2}$ defined in (6.1) is said to be $\mu^\natural$-incoherent if the following holds:
\[
\|\mathbf U^\natural\|_{2,\infty}\leq\sqrt{\frac{\mu^\natural r}{n_1}},\qquad\|\mathbf V^\natural\|_{2,\infty}\leq\sqrt{\frac{\mu^\natural r}{n_2}},\qquad\text{and}\qquad\|\mathbf M^\natural\|_\infty\leq\sqrt{\frac{\mu^\natural}{n_1n_2}}\|\mathbf M^\natural\|_{\mathrm F}.
\]
''',[20],'Assumption 2 — Incoherence',{'D14':'The condition constrains both singular-vector matrices and the entrywise size of the fixed rectangular signal.'},kind='assumption',context='Assumption 2 (Incoherence).',phrases=['Assumption 2','Incoherence'],symbols=[r'\|\mathbf V^\natural\|_{2,\infty}',r'\|\mathbf M^\natural\|_\infty'],shape='Three simultaneous restrictions: row-norm bounds for the left and right singular spaces and an entrywise-to-Frobenius bound for the signal. This is not interchangeable with Definition 1, which has only the covariance-eigenspace restriction.')
add('D16','Heteroskedastic random noise',r'''
Assume that the $E_{i,j}$’s are independently generated, and suppose that there exist nonnegative quantities $\{\sigma_i\}_{i=1}^{n_1}$, $\{B_i\}_{i=1}^{n_1}$, $\sigma$ and $B$ obeying
\[
\forall(i,j)\in[n_1]\times[n_2]:\quad\mathbb E[E_{i,j}]=0,\quad\operatorname{var}(E_{i,j}^2)=\sigma_{i,j}^2\leq\sigma_i^2\leq\sigma^2,\quad|E_{i,j}|\leq B_i\leq B,
\]
where for all $i\in[n_1]$,
\[
B_i\lesssim\frac{\sigma_i\min\{\sqrt{n_2},\sqrt[4]{n_1n_2}\}}{\sqrt{\log n}},\qquad\text{and}\qquad B\lesssim\frac{\sigma\min\{\sqrt{n_2},\sqrt[4]{n_1n_2}\}}{\sqrt{\log n}}.\tag{6.5}
\]
''',[20],'Assumption 3 — Heteroskedastic random noise',{'D14':'E is the additive perturbation in the separate general subspace model with n=max(n_1,n_2).'},kind='assumption',context='Assumption 3 (Heteroskedastic random noise).',phrases=['Assumption 3','Heteroskedastic random noise'],symbols=[r'\operatorname{var}(E_{i,j}^2)',r'\sigma_{i,j}^2\leq\sigma_i^2\leq\sigma^2',r'B_i'],shape='Independent bounded centered entries, row/global bounds and amplitude-to-scale restrictions, retaining the printed variance of E_ij squared. The source later treats sigma_ij squared as variance of E_ij itself; the discrepancy is recorded rather than repaired. These assumptions do not impose PCA’s finite noise variance ratio.')
add('D17','HeteroPCA for general subspace estimation',r'''
Initialization: set $\mathbf G^0=\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf M\mathbf M^\top)$.

Updates: for $t=0,1,\ldots,t_0$ do
\[
(\mathbf U^t,\mathbf\Lambda^t)=\operatorname{eigs}(\mathbf G^t,r);\tag{6.8a}
\]
\[
\mathbf G^{t+1}=\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf M\mathbf M^\top)+\mathcal P_{\mathrm{diag}}(\mathbf U^t\mathbf\Lambda^t\mathbf U^{t\top}).\tag{6.8b}
\]
Here, $\operatorname{eigs}(\mathbf G,r)$ returns $(\mathbf U,\mathbf\Lambda)$ where $\mathbf U\mathbf\Lambda\mathbf U^\top$ is the top-$r$ eigendecomposition of $\mathbf G$.

Output: $\mathbf U=\mathbf U^{t_0}$, $\mathbf\Lambda=\mathbf\Lambda^{t_0}$, $\mathbf\Sigma=(\mathbf\Lambda^{t_0})^{1/2}$, $\mathbf S=\mathbf U^{t_0}\mathbf\Lambda^{t_0}\mathbf U^{t_0\top}$.
''',[21],'Algorithm 5 — HeteroPCA for general subspace estimation',{'D14':'The input M is the additive-noise observation in the general subspace model.','D5':'The updates keep the observed off-diagonal Gram entries and impute only its diagonal.'},context='Algorithm 5 HeteroPCA for general subspace estimation (HeteroPCA)',phrases=['HeteroPCA for general subspace estimation'],symbols=[r'\mathbf G^0=\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf M\mathbf M^\top)',r'\mathbf U^{t_0}'],shape='Unscaled Gram-matrix HeteroPCA iteration for the general rectangular model. It shares projection primitives with Algorithm 2 but has different input scaling and model; the source does not resolve eigenvalue ties or nonpositive square-root cases.')
add('D18','rotation matrix',r'''
In order to account for the potential global rotational ambiguity, we introduce the following rotation matrix as before:
\[
\mathbf R_U:=\operatorname*{argmin}_{\mathbf O\in\mathcal O^{r\times r}}\|\mathbf U\mathbf O-\mathbf U^\natural\|_{\mathrm F}^2,\tag{6.9}
\]
where we recall that $\mathcal O^{r\times r}$ represents the set of $r\times r$ orthonormal matrices.
''',[21],'Section 6.2 — alignment rotation, equation (6.9)',{'D14':'The target left singular space U-natural belongs to the general rectangular model.','D17':'The estimated U is the output of Algorithm 5.'},phrases=['rotation matrix'],symbols=[r'\mathbf R_U',r'\mathcal O^{r\times r}'],shape='A minimizing orthogonal alignment between the estimated and true general-model subspaces. This definition uses an argmin rather than the earlier matrix-sign function. Selection in case of multiple minimizers is not specified; orthonormal matrices may include reflections.')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(interfaces),'source-backed interfaces; extraction remains in progress.')


if __name__ == "__main__":
    main()
