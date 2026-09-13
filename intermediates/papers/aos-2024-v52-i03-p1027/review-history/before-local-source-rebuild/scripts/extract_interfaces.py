"""Transcribe dynamic-volatility prerequisites from the main text only."""
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
add('D1','scalar BEKK model',r'''
In particular, the widely used scalar BEKK model describes the dynamics of covariance matrix as follows:
\[
\boldsymbol\Sigma_{t+1}=(1-a-b)\overline{\boldsymbol\Sigma}+a\mathbf R_t\mathbf R_t^T+b\boldsymbol\Sigma_t,\tag{1.1}
\]
where $\overline{\boldsymbol\Sigma}$ is the unconditional covariance matrix, $\boldsymbol\Sigma_t$ is the conditional covariance matrix of the returns $\mathbf R_t=(R_{1t},\ldots,R_{pt})^T$, and $0\le a,b\le1$ with $a+b<1$ are related parameters. The parameter $a$ is sometimes referred to as the innovation coefficient, and $a+b$ the persistence coefficient.
''',[2],'Section 1.2 — scalar BEKK model (1.1)',kind='source_passage',symbols=[r'\boldsymbol\Sigma_{t+1}',r'\overline{\boldsymbol\Sigma}'],shape='Conditional covariance recursion with a fixed unconditional covariance matrix. Dimension-dependent coefficients are supplied by Section 2.1. No simulation-specific population covariance or stationary initialization is added.')
add('D2','returns',r'''Under a dynamic volatility model, returns are modeled as $\mathbf R_t=(\boldsymbol\Sigma_t)^{1/2}\mathbf z_t$, where $\mathbf z_t=(z_{1t},\ldots,z_{pt})^T$ are i.i.d. with mean zero and covariance matrix $\mathbf I$.''',[6],'Section 2.1 — return representation',symbols=[r'\mathbf R_t=(\boldsymbol\Sigma_t)^{1/2}\mathbf z_t'],shape='Returns obtained by the positive semidefinite covariance square root acting on iid standardized vectors. Gaussianity is imposed separately in Assumption 1.')
add('D3','i.i.d.',r'''Define $\mathbf R_t^0=(\overline{\boldsymbol\Sigma})^{1/2}\mathbf z_t$, $t=1,\ldots,T$, which share the same unconditional covariance matrix as $\mathbf R_t$ but are i.i.d..''',[6],'Section 2.1 — iid reference returns',{'D2':'The reference returns use the same standardized innovation vectors as the dynamic returns.'},symbols=[r'\mathbf R_t^0'],shape='Coupled iid comparison sample using the unconditional covariance square root. The source writes the endpoint T here, while the sample covariance below sums to n; no identification is silently inserted.')
add('D4','sample covariance matrices',r'''
Denote the corresponding sample covariance matrices by
\[
\mathbf S_n=\frac1n\sum_{t=1}^n\mathbf R_t\mathbf R_t^T,\quad\text{and}\quad\mathbf S_n^0=\frac1n\sum_{t=1}^n\mathbf R_t^0(\mathbf R_t^0)^T.
\]
We write $\widehat\lambda_1\ge\ldots\ge\widehat\lambda_p$ as the eigenvalues of $\mathbf S_n$, and $\widehat\lambda_1^0\ge\ldots\ge\widehat\lambda_p^0$ as the eigenvalues of $\mathbf S_n^0$.
''',[6],'Section 2.1 — sample covariances and eigenvalues',{'D2':'The first covariance is the uncentered outer-product average of dynamic returns.','D3':'The comparison covariance averages the coupled iid reference returns.'},symbols=[r'\mathbf S_n',r'\mathbf S_n^0'],shape='Pair of uncentered sample second-moment matrices normalized by n, with descending eigenvalues. These are two distinct sample objects, not independent samples or sample-mean-centered estimators.')
add('D5','empirical spectral distribution',r'''For any symmetric matrix $\mathbf A$ with eigenvalues $\lambda_1,\ldots,\lambda_p$, its empirical spectral distribution (ESD) is defined as $F^{\mathbf A}(x)=\sum_{j=1}^p\mathbf1_{[\lambda_j,+\infty)}(x)/p$, $x\in\mathbb R$.''',[6],'Notation — empirical spectral distribution',symbols=[r'F^{\mathbf A}(x)'],shape='Equal-weight empirical distribution function of all p eigenvalues of a symmetric matrix, including zero eigenvalues.')
add('D6','Assumption 1',r'''
(i) $\mathbf z_t\underset{i.i.d.}{\sim}N(0,\mathbf I)$.

(ii) $\overline{\boldsymbol\Sigma}$ is nonnegative definite and its ESD, $F^{\overline{\boldsymbol\Sigma}}$, converges in distribution to a probability distribution $H$ on $[0,\infty)$ as $p\to\infty$, and $H\ne\delta(0)$, the Dirac measure at $0$.

(iii) $\|\overline{\boldsymbol\Sigma}\|<C$ for some constant $C>0$.

(iv) The dimension $p$ and the sample size $n$ satisfy that $p,n\to\infty$, and $p/n\to y>0$.
''',[6],'Assumption 1',{'D2':'Part (i) specializes the standardized innovation vectors of the return representation to Gaussian vectors.','D5':'Part (ii) constrains the population empirical spectral distribution and defines its limit H.','D7':'Part (iii) uses the matrix spectral norm defined in the notation paragraph.'},kind='assumption',phrases=['Assumption 1'],symbols=[r'F^{\overline{\boldsymbol\Sigma}}',r'p/n\to y>0'],context='Assumption 1',shape='Four-part sequence-level assumption: iid Gaussian innovations, nondegenerate limiting population ESD on the nonnegative half-line, uniformly bounded population spectral norm, and positive limiting dimension/sample-size ratio. Parts (i)–(iv) are all preserved; no finite-dimensional lower eigenvalue bound is added.')
add('D7','spectral norm',r'''For any matrix $\mathbf A=(A_{ij})$, its spectral norm is defined as $\|\mathbf A\|=\max_{\|\mathbf x\|\le1}\sqrt{\mathbf x^T\mathbf A^T\mathbf A\mathbf x}$, where $\|\mathbf x\|=\sqrt{\sum x_i^2}$ for any vector $\mathbf x=(x_i)$;''',[5,6],'Notation — spectral norm',symbols=[r'\|\mathbf A\|'],shape='Euclidean operator norm of a real matrix, with the source maximum over the closed unit ball.')
add('D8','Frobenius norm',r'''the Frobenius norm is defined as $\|\mathbf A\|_F=\sqrt{\sum_{i,j}A_{ij}^2}$.''',[6],'Notation — Frobenius norm',symbols=[r'\|\mathbf A\|_F'],shape='Unnormalized real-matrix Frobenius norm. Theorem 5 places the factor p^{-1/2} outside this norm.')
add('D9','Levy distance',r'''
Recall that for any two distributions $F_1$ and $F_2$, the Levy distance between them is defined as
\[
L(F_1,F_2):=\inf\{\varepsilon>0|F_1(x-\varepsilon)-\varepsilon\le F_2(x)\le F_1(x+\varepsilon)+\varepsilon\text{ for all }x\in\mathbb R\}.
\]
''',[7],'Section 2.2.1 — Levy distance',symbols=[r'L(F_1,F_2)'],shape='Levy distance between real distribution functions, using two horizontal/vertical epsilon shifts. This is not Wasserstein distance or uniform CDF distance.')
add('D10','reducible case',r'''We refer to the case when $\eta(a_p,b_p,p)\to0$ as the reducible case.''',[7],'Section 2.2.1 — reducible case',symbols=[r'\eta(a_p,b_p,p)\to0'],shape='Vanishing eta regime for dimension-dependent BEKK coefficients. The scalar function eta is separately transcribed from (2.1) in ambient passage A3; its exact square-root scaling is retained.')
add('D11','non-reducible case',r'''We refer to the case when $\eta(a_p,b_p,p)$ is bounded away from zero as the non-reducible case.''',[8],'Section 2.2.2 — non-reducible case',symbols=[r'\eta(a_p,b_p,p)'],shape='Eta bounded away from zero, instantiated in Theorem 2 as eta>c for a fixed positive constant. This is distinct from the vanishing regime; eta itself is defined in ambient passage A3.')
add('D12','second moment',r'''
We measure the difference in the ESD's between the BEKK model and the practically relevant i.i.d. case by the second moment of the ESD's:
\[
M_2=M_2^p=\sum_{i=1}^p\widehat\lambda_i^2/p=\operatorname{tr}\big((\mathbf S_n)^2\big)/p,\quad\text{and}\quad M_2^0=M_2^{0,p}=\sum_{i=1}^p(\widehat\lambda_i^0)^2/p=\operatorname{tr}\big((\mathbf S_n^0)^2\big)/p.
\]
''',[8],'Section 2.2.2 — second moments of the ESDs',{'D4':'The two spectral second moments use the eigenvalues and squared traces of the dynamic and iid sample covariance matrices.','D5':'These are moments of the equal-weight empirical eigenvalue distributions.'},symbols=[r'M_2^p',r'M_2^{0,p}'],shape='Random second moments of two empirical eigenvalue distributions, normalized by p. Theorem 2 compares their expectations, not a samplewise order.')
add('D13','univariate GARCH model',r'''
Under the BEKK model (1.1), the time-variation in the covariance matrix is governed by the two coefficients, $a_p$ and $b_p$, and each $R_{it}$ follows a univariate GARCH model:
\[
\sigma_{i,t+1}^2=(1-a_p-b_p)\overline\sigma_i^2+a_pR_{it}^2+b_p\sigma_{i,t}^2,\tag{2.4}
\]
where $\sigma_{i,t}^2=(\boldsymbol\Sigma_t)_{ii}$, and $\overline\sigma_i^2=(\overline{\boldsymbol\Sigma})_{ii}$ for $1\le i\le p$.
''',[9],'Section 2.3 — marginal GARCH model (2.4)',{'D1':'The conditional and unconditional marginal variances are the diagonal entries of the scalar BEKK covariance matrices.'},symbols=[r'\sigma_{i,t+1}^2',r'\overline\sigma_i^2'],shape='Coordinate GARCH variance recursion with the shared BEKK coefficients. Unconditional marginal variance is overbar-sigma squared, not time-dependent sigma squared.')
add('D14','QMLE',r'''
Specifically, we randomly select one variable, say, $i_0$, fit a univariate GARCH model to $(R_{i_0t})$ and get QMLE $\widehat a$ and $\widehat b$:
\[
(\widehat a,\widehat b,\widehat{\overline\sigma}_{i_0})=\operatorname*{argmax}_{(a,b,\overline\sigma_{i_0})\in\Omega}\frac1n\left(\sum_{t=1}^n\left(\frac{R_{i_0t}^2}{\sigma_{i_0t}^2}+\log(\sigma_{i_0t}^2)\right)\right),
\]
where $\Omega=\{(a,b,\overline\sigma),0\le a\le1,0\le b\le1,a+b\le1-\delta,\delta\le\overline\sigma^2<C\}$ for some positive constants $\delta$ and $C$.
''',[9],'Section 2.3 — QMLE and parameter domain',{'D13':'The criterion uses the selected coordinate conditional variance from the marginal GARCH recursion.'},symbols=[r'\widehat a',r'\widehat b'],shape='Randomly selected single-coordinate Gaussian quasi-likelihood fit, including its constrained parameter space. The positive objective is printed with argmax, not argmin; initialization and tie selection are not specified here.',note='The source prints argmax of a positive sum of standardized squared returns plus log variance. This transcription does not change its sign or optimization direction.')
add('D15','projection matrix',r'''
We then use $\widehat a$, $\widehat b$ and past returns to construct a projection matrix:
\[
\mathbf P_t=\frac{1-\widehat a-\widehat b+\widehat a\widehat b^{M_p}}{1-\widehat b}\mathbf I+\sum_{j=1}^{M_p}\widehat a\widehat b^{j-1}\mathbf R_{t-j}\mathbf R_{t-j}^T,\tag{2.5}
\]
where $M_p$ represents the number of lagged returns included in $\mathbf P_t$, which grows with $p$ and $M_p=o(\sqrt p)$.
''',[9,10],'Section 2.3 — projection matrix (2.5)',{'D14':'The lag-weighted matrix uses the estimated coefficients a-hat and b-hat.','D2':'Its summands use outer products of past dynamic returns.'},symbols=[r'\mathbf P_t',r'M_p'],shape='Positive regularized lag-weighted return matrix with an identity term and estimated coefficients. The author calls it a projection matrix; orthogonal projection or idempotence is not asserted. The asymptotic lag-count condition is kept.')
add('D16','time-variation adjusted returns',r'''To be more precise, using the projection matrix $\mathbf P_t$, we define the time-variation adjusted returns $\widetilde{\mathbf R}_t=\mathbf P_t^{-1/2}\mathbf R_t$,''',[10],'Section 2.3 — adjusted returns',{'D15':'Adjusted returns use the inverse square root of the lag-weighted projection matrix.','D2':'The transformed vector is the original dynamic return.'},symbols=[r'\widetilde{\mathbf R}_t'],shape='Inverse-square-root transformation of dynamic returns, not a scalar rescaling or orthogonal projection.')
add('D17','time-variation adjusted (TV-adj) sample covariance matrix',r'''
and the time-variation adjusted (TV-adj) sample covariance matrix:
\[
\widetilde{\mathbf S}_n=\frac1n\sum_{t=1}^n\widetilde{\mathbf R}_t(\widetilde{\mathbf R}_t)^T.\tag{2.6}
\]
''',[10],'Section 2.3 — adjusted sample covariance (2.6)',{'D16':'The adjusted sample covariance is the uncentered second-moment average of the transformed returns.'},symbols=[r'\widetilde{\mathbf S}_n'],shape='Uncentered covariance of inverse-square-root-adjusted returns, normalized by n. It remains random and is not asserted to have independent observations.')
add('D18','Stieltjes transform',r'''
and $F$ is determined by that its Stieltjes transform
\[
m_F(z):=\int_{\lambda\in\mathbb R}\frac1{\lambda-z}\,dF(\lambda),\ z\in\mathbb C^+:=\{z\in\mathbb C,\operatorname{Im}(z)>0\}\tag{2.8}
\]
solves the following equation
\[
m_F(z)=\int_{\tau\in\mathbb R}\frac1{\tau\left(1-y\left(1+zm_F(z)\right)\right)-z}\,dH(\tau).\tag{2.9}
\]
''',[10],'Section 2.3 — limiting spectral law and transform (2.8)–(2.9)',{'D6':'The Marchenko–Pastur equation is parameterized by the limiting population law H and ratio y from Assumption 1.'},symbols=[r'm_F(z)'],shape='Limiting sample spectral law specified by its upper-half-plane Stieltjes transform and the printed Marchenko–Pastur equation. The preceding convergence statement is context, not a theorem assumption or a dependency on a particular estimator implementation. Equation (2.9) uses y, unlike y^{-1} in Theorem 4.')
add('D19','bounded function',r'''for some bounded function $g(\cdot)$, and $g(\overline{\boldsymbol\Sigma})=\sum_{i=1}^p g(\lambda_i^H)\mathbf v_i\mathbf v_i^T$, where $\mathbf v_i$'s are the eigenvectors of $\overline{\boldsymbol\Sigma}$.''',[11],'Section 2.4 — population matrix functional calculus',symbols=[r'g(\overline{\boldsymbol\Sigma})'],shape='Spectral application of the bounded function g to the population covariance. Population eigenvalues lambda_i^H are identified on page 10 and archived as ambient context; this is not the normalized generalized ESD.')
add('D20','generalized Stieltjes transform',r'''
Parallel to the i.i.d. case, we study the limiting property of the generalized ESD of the TV-adj sample covariance matrix via the following generalized Stieltjes transform:
\[
\Theta_n^g(z)=\frac1p\operatorname{tr}\left((\widetilde{\mathbf S}_n-z\mathbf I)^{-1}g(\overline{\boldsymbol\Sigma})\right).\tag{2.11}
\]
''',[12],'Section 2.4 — generalized Stieltjes transform (2.11)',{'D17':'The matrix resolvent is formed from the time-variation-adjusted sample covariance.','D19':'The resolvent trace is weighted by g applied to the population covariance.'},symbols=[r'\Theta_n^g(z)'],shape='Population-weighted resolvent trace divided by p. This normalization differs from the trace(g(Sigma)) denominator in the preceding generalized ESD (2.10); do not silently identify it with that normalized distribution Stieltjes transform.')
add('D21','truncation',r'''where $\widetilde{\mathbf S}_n^\tau=\sum_{i=1}^p\widetilde\lambda_i^\tau\widetilde{\mathbf u}_i\widetilde{\mathbf u}_i^T$, $\widetilde\lambda_i^\tau=\min(\widetilde\lambda_i,L)$, and $L$ is a large constant. The truncation is applied to ensure that the support of the ESD is bounded.''',[12],'Section 2.4 — eigenvalue truncation',{'D17':'The eigenvalues and eigenvectors are those of the adjusted sample covariance.'},symbols=[r'\widetilde\lambda_i^\tau',r'\widetilde{\mathbf S}_n^\tau'],shape='Upper clipping at a large fixed constant L, with the eigenvectors preserved. Tau is a superscript label and is not an independently specified threshold. A lower clipping threshold is not introduced.')
add('D22','TV-adj nonlinear shrinkage estimator',r'''
Specifically, to estimate the unconditional covariance matrix, we perform the nonlinear shrinkage algorithm by Ledoit and Wolf (2015) on $\widetilde{\mathbf S}_n^\tau$, where $\widetilde{\mathbf S}_n^\tau=\sum_{i=1}^p\widetilde\lambda_i^\tau\widetilde{\mathbf u}_i\widetilde{\mathbf u}_i^T$, $\widetilde\lambda_i^\tau=\min(\widetilde\lambda_i,L)$, and $L$ is a large constant. The truncation is applied to ensure that the support of the ESD is bounded. We denote by $\widetilde{\boldsymbol\Sigma}$ the resulting covariance matrix estimator, which we call the TV-adj nonlinear shrinkage estimator (TV-adj NLS).
''',[12],'Section 2.4 — TV-adj NLS construction',{'D21':'The externally cited nonlinear shrinkage algorithm is applied to the eigenvalue-truncated adjusted covariance.'},symbols=[r'\widetilde{\boldsymbol\Sigma}'],shape='Output of the Ledoit–Wolf (2015) nonlinear shrinkage algorithm on the truncated adjusted covariance. The main text does not supply the full external algorithm; preserve this unresolved construction rather than substitute the displayed population oracle.')
add('D23','infeasible oracle shrinkage estimator',r'''
Define $\widetilde{\boldsymbol\Sigma}^{or}=\sum_{i=1}^p d_i^{or}(\widetilde\lambda_i^\tau)\widetilde{\mathbf u}_i\widetilde{\mathbf u}_i^T$, where
\[
d_i^{or}(\widetilde\lambda_i^\tau)=\begin{cases}\displaystyle\frac1{(y-1)\check m_{\underline F}(0)}&\text{if }\widetilde\lambda_i^\tau=0\text{ and }y>1,\\\displaystyle\frac{\widetilde\lambda_i^\tau}{\left(1-y-y\widetilde\lambda_i^\tau\cdot\check m_F(\widetilde\lambda_i^\tau)\right)^2}&\text{otherwise},\end{cases}\quad\text{for }i=1,\ldots,p,\tag{2.13}
\]
$m_{\underline F}=(y-1)/z+ym_F(z)$, $\underline F(x)=(1-y)\mathbf1_{\{[0,\infty)\}}(x)+yF(x)$, $\check m(\lambda)=\lim_{z\in\mathbb C^+\to\lambda}m_F(z)$, $F(\cdot)$ and $m_F(z)$ are given in (2.8) and (2.9), respectively. By Theorem 4 and Theorem 4 of Ledoit and Péché (2011), $\widetilde{\boldsymbol\Sigma}^{or}$ is the infeasible oracle shrinkage estimator.
''',[13],'Section 2.4 — oracle shrinkage formula (2.13)',{'D21':'The oracle uses the same clipped eigenvalues and unchanged sample eigenvectors.','D18':'Its shrinkage coefficients use the limiting Stieltjes transform, companion transform and boundary values.'},symbols=[r'\widetilde{\boldsymbol\Sigma}^{or}',r'\check m_{\underline F}(0)'],shape='Population-law-dependent oracle with a separate zero-eigenvalue branch for y>1. Preserve the source ordinary square, underlined companion F, and unindexed boundary-value shorthand. External results justify its optimality but are not extra statement prerequisites.',note='The positive-eigenvalue denominator is printed as an ordinary square, with no modulus bars. The source also leaves the F subscript off the left side of its boundary-value definition. These formulas are retained without correction.')
add('D24',['limiting distribution','bounded function'],r'''the limiting distribution $H$ is supported by $[h_1,h_2]$ for some constants $0<h_1\le h_2<\infty$, and $g$ is a bounded function on $[h_1,h_2]$ with finitely many points of discontinuity,''',[12],'Theorem 4 — additional spectral assumptions',{'D6':'The condition strengthens the limiting population law H supplied by Assumption 1.'},kind='condition',symbols=[r'0<h_1\le h_2<\infty'],phrases=['bounded function'],shape='Additional support restriction on the limiting law and finite-discontinuity boundedness of g. This does not explicitly bound every finite-dimensional population eigenvalue away from zero or specify g outside the limiting support.')

if __name__=='__main__':
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='source_review_pending',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages; independent source and dependency review remain.')
