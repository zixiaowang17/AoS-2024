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
add('D1','trend functions',r'''
To formulate our model, let $Y_1,\ldots,Y_n$ be observed $p$-dimensional random vectors satisfying
\[
Y_t=\mu(t/n)+\epsilon_t,\quad t=1,\ldots,n,\tag{1}
\]
where $(\epsilon_t)_t$ is a sequence of $p$-dimensional stationary errors with zero-mean and $\mu(\cdot)$ is a $p$-dimensional vector of unknown trend functions. Our main interest is to detect the potential change points occurring on the trend function
\[
\mu(u)=\mu_0+\sum_{k=1}^K\gamma_k\mathbf1_{u\geq u_k},\tag{2}
\]
where $K\in\mathbb N$ is the number of structural breaks which is unknown and could go to infinity as $n$ increases; $u_1,\ldots,u_K$ are the time stamps of the breaks with $0=u_0<u_1<\ldots<u_K<u_{K+1}=1$ and the minimum gap $\kappa_n=\min_{0\leq k\leq K}(u_{k+1}-u_k)$, where $\kappa_n>0$ is allowed to tend to $0$ as $n\to\infty$; $\mu_0\in\mathbb R^p$ represents the benchmark level when no break occurs and $\gamma_k\in\mathbb R^p$ is the jump vector at the time stamp $u_k$ with size $|\gamma_k|_2$.
''',[5],'Section 2 — observation model and piecewise-constant trend, equations (1)-(2)',kind='source_passage',phrases=['trend functions'],symbols=[r'Y_t=\mu(t/n)+\epsilon_t',r'\gamma_k\mathbf1_{u\geq u_k}'],shape='Vector observations with a piecewise-constant mean and zero-mean stationary noise. The jump vectors need not be nonzero in every coordinate. The linear-error representation and cross-sectional independence are separate conditions.')
add('D2','null hypothesis',r'''
This subsection is devoted to test the null hypothesis:
\[
\mathcal H_0:\quad\gamma_1=\gamma_2=\ldots=\gamma_K=0,
\]
which denotes the case with no breaks, against the alternative $\mathcal H_A$: there exists $k\in\{1,\ldots,K\}$, such that $\gamma_k\neq0$.
''',[5],'Section 2.1 — no-break hypothesis',{'D1':'The hypothesis concerns the jump vectors in the trend model (2).'},kind='condition',phrases=['null hypothesis'],symbols=[r'\gamma_1=\gamma_2=\ldots=\gamma_K=0'],shape='Null of no mean jumps in the vector trend model, with at least one nonzero jump under the alternative. It does not impose the positive-signal condition used for consistency under alternatives.')
add('D3','local averages',r'''
We define a jump vector $J(u)$ at the time point $u$ as $J(u)=0$ when no break occurs at the time stamp $u$, and $J(u)=\gamma_i$ when $u=u_i$ for some $1\leq i\leq K$. Intuitively, we can test the existence of breaks by evaluating the jump estimate $\widehat J(i/n)=\widehat\mu_i^{(l)}-\widehat\mu_i^{(r)}$, where
\[
\widehat\mu_i^{(l)}=\widehat\mu^{(l)}(i/n)=\frac1{bn}\sum_{t=i-bn}^{i-1}Y_t,\quad
\widehat\mu_i^{(r)}=\widehat\mu^{(r)}(i/n)=\frac1{bn}\sum_{t=i}^{i+bn-1}Y_t,\tag{3}
\]
are the local averages on the left and the right hand sides of the time point $i/n$, respectively, and $b$ is a bandwidth parameter satisfying $b\to0$ and $bn\to\infty$. Without loss of generality, we assume that $bn$ is an integer.
''',[6],'Section 2.1 — local averages and jump estimate, equation (3)',{'D1':'The averages use the observations and the source jump vectors from (1)-(2).'},phrases=['local averages'],symbols=[r'\widehat\mu_i^{(l)}',r'\widehat\mu_i^{(r)}',r'\widehat J(i/n)'],shape='Left and right block averages and their left-minus-right difference. The windows each have integer length bn. The source sign differs from the positive jump convention in the trend model; it is not silently reversed.')
add('D4','vector moving average',r'''
Let
\[
\epsilon_t=\sum_{k\geq0}A_k\eta_{t-k},\tag{4}
\]
where $\eta_t\in\mathbb R^{\widetilde p}$ are i.i.d. random vectors with zero mean and an identity covariance matrix with $p\leq\widetilde p\leq cp$, for some constant $c>1$. The coefficient matrices $A_k$, $k\geq0$, take values in $\mathbb R^{p\times\widetilde p}$ such that $\epsilon_t$ is a proper random vector. Define $\widetilde A_0=\sum_{k\geq0}A_k$.
''',[6],'Section 2.1 — vector moving-average errors, equation (4)',context='In particular, we model $\\epsilon_t$ as a vector moving average (VMA) process in Sections 2 and 3,',symbols=[r'\epsilon_t=\sum_{k\geq0}A_k\eta_{t-k}',r'\widetilde A_0'],shape='Causal linear errors with iid mean-zero identity-covariance innovation vectors and rectangular coefficient matrices. Sections 2/3 further set p=tilde-p and diagonal coefficients, while the general spatial theorem uses a separate nonlinear model.')
add('D5',['long-run variance matrix','long-run standard deviations'],r'''
Then the long-run variance matrix of $\epsilon_t$ and the diagonal matrix of the long-run standard deviations are
\[
\Sigma=\widetilde A_0\widetilde A_0^\top=(\sigma_{i,j})_{i,j=1}^p,\quad
\Lambda=\operatorname{diag}(\sigma_1,\sigma_2,\ldots,\sigma_p),\tag{5}
\]
respectively, where $\sigma_j^2=\sigma_{j,j}\geq c_\sigma$, for some constant $c_\sigma>0$, is the long-run variance of the $j$-th component series.
''',[6,7],'Section 2.1 — long-run covariance and standardization, equation (5)',{'D4':'The covariance is expressed through the summed moving-average coefficients.'},phrases=['long-run variance matrix','long-run standard deviations'],symbols=[r'\Lambda=\operatorname{diag}(\sigma_1,\sigma_2,\ldots,\sigma_p)',r'\sigma_j^2=\sigma_{j,j}\geq c_\sigma'],shape='Covariance of the linear long-run noise and diagonal positive standard deviations, with an explicit uniform lower variance bound. This differs from the later generalized source notation which calls sigma(l) a variance.')
add('D6','standardized jump estimator',r'''
Following the previous intuition, we test the existence of breaks by evaluating the gap vectors $\widehat J(\cdot)$. Namely, we standardize $\widehat J(\cdot)$ by the long-run standard deviations of each time series, that is, for $bn+1\leq i\leq n-bn$,
\[
V_i=\Lambda^{-1}\widehat J(i/n)=\Lambda^{-1}(\widehat\mu_i^{(l)}-\widehat\mu_i^{(r)}).\tag{6}
\]
''',[7],'Section 2.1 — standardized jump vector, equation (6)',{'D3':'The gap is the left-minus-right local average difference (3).','D5':'Lambda is the diagonal matrix of long-run standard deviations (5).'},context=r'This is because, even if the underlying errors are i.i.d., the standardized jump estimator $V_i$ defined in (6) is still dependent over $i$ due to the overlapped observations among different moving windows.',phrases=['standardize'],symbols=[r'V_i=\Lambda^{-1}\widehat J(i/n)'],shape='Standardized block-average contrast at the admissible interior time indices. Lambda is assumed known in the main test theory; an appendix variance estimator is not imported.')
members['D6']['naming_context'][0]['evidence']=[dict(page=8,location='Section 2.2 opening paragraph')]
add('D7','centering term',r'''
We define
\[
\bar c=\sum_{j=1}^p c_j,\quad\text{where }c_j=\operatorname{Var}(V_{i,j}),\tag{7}
\]
and $V_{i,j}\in\mathbb R$ is the $j$-th coordinate of $V_i$. Since no break exists under the null hypothesis, i.e. $\mathbb EV_i=0$, it follows that $|V_i|_2^2-\bar c$ is a centered statistic under the null.
''',[7],'Section 2.1 — variance centering, equation (7)',{'D6':'The centering sums coordinate variances of the standardized contrast.'},context='Remark 5 (Comments on the centering term $\\bar c$).',symbols=[r'\bar c=\sum_{j=1}^p c_j',r'c_j=\operatorname{Var}(V_{i,j})'],shape='Exact deterministic sum of contrast-coordinate variances, constant in time under stationary noise. The later approximation 2p/(bn) and the value at a selected random index are distinct source expressions, not substituted here.')
members['D7']['naming_context'][0]['evidence']=[dict(page=14,location='Remark 5 heading')]
add('D8','test statistic',r'''
Finally, we move the windows in the temporal direction to find the maximum and formulate our $\ell^2$-based test statistic as follows:
\[
\mathcal Q_n=\max_{bn+1\leq i\leq n-bn}\big(|V_i|_2^2-\bar c\big).\tag{8}
\]
We consider $\mathcal Q_n$ as a feasible test statistic by assuming that the long-run standard deviation $\Lambda$ is known.
''',[7],'Section 2.1 — aggregated MOSUM statistic, equation (8)',{'D6':'The statistic aggregates the squared standardized jump coordinates.','D7':'It subtracts the exact variance centering term.'},phrases=['test statistic'],symbols=[r'\mathcal Q_n',r'|V_i|_2^2-\bar c'],shape='Maximum over time of the centered squared Euclidean norm of the standardized MOSUM contrast. It is not divided by sqrt(p), unlike the neighborhood-normalized statistics introduced later.')
add('D9','centered Gaussian random vector',r'''
We introduce the centered Gaussian random vector $\mathcal Z=(Z_{bn+1},\ldots,Z_{n-bn})^\top\in\mathbb R^{n-2bn}$ with covariance matrix $\Xi=\mathbb E(\mathcal Z\mathcal Z^\top)\in\mathbb R^{(n-2bn)\times(n-2bn)}$, and denote the $i$-th element in $\mathcal Z$ by $Z_i$. Here $\Xi=(\Xi_{i,i'})_{1\leq i,i'\leq n-2bn}$ with expression
\[
\Xi_{i,i'}=p(bn)^{-2}g\big(|i-i'|/(bn)\big),\tag{11}
\]
where the function $g(\cdot):[0,\infty)\mapsto\mathbb R$ is defined as
\[
g(\zeta)=\begin{cases}
18\zeta^2-24\zeta+8,&0\leq\zeta<1,\\
2\zeta^2-8\zeta+8,&1\leq\zeta<2,\\
0,&\zeta\geq2.
\end{cases}\tag{12}
\]
''',[9],'Section 2.2 — Gaussian reference vector and covariance, equations (11)-(12)',phrases=['centered Gaussian random vector'],symbols=[r"\Xi_{i,i'}",r'g(\zeta)'],shape='Explicit finite Gaussian comparison law with its piecewise quadratic covariance kernel, indexed by n,p,b. It does not require constructing the proof variables X_j. The shifted coordinate labels and matrix indices are retained.')
add('D10','Finite moment',r'''
Assume that the innovations $\eta_{i,j}$ defined in (4) are i.i.d. with $\mu_q:=\|\eta_{1,1}\|_q<\infty$ for some $q\geq8$.
''',[10],'Assumption 1 (Finite moment)',{'D4':'The finite moment condition refers to the innovations of the VMA model (4).'},kind='assumption',context='Assumption 1 (Finite moment).',phrases=['Assumption 1'],symbols=[r'\mu_q:=\|\eta_{1,1}\|_q'],shape='Uniform scalar innovation moment condition with q at least eight, and iid innovation coordinates as stated. Mean zero and identity covariance come from (4).')
add('D11','Temporal dependence',r'''
There exist constants $C>0$, $\beta>0$ such that
\[
\max_{1\leq j\leq p}\sum_{k\geq h}|A_{k,j,\cdot}|_2/\sigma_j\leq C(1\vee h)^{-\beta},
\]
for all $h\geq0$, where $A_{k,j,\cdot}$ is the $j$-th row of $A_k$.
''',[10],'Assumption 2 (Temporal dependence)',{'D4':'The tail sums the Euclidean row norms of the VMA coefficient matrices.','D5':'The row norms are normalized by the long-run standard deviations.'},kind='assumption',context='Assumption 2 (Temporal dependence).',phrases=['Assumption 2'],symbols=[r'|A_{k,j,\cdot}|_2/\sigma_j',r'(1\vee h)^{-\beta}'],shape='Uniform polynomial tail bound on normalized coefficient row norms, with C and beta positive and all h nonnegative. No stronger decay exponent is inferred.')
add('D12','Cross-sectional independence',r'''
Assume that for all $k\geq0$, the coefficient matrices $A_k$ defined in (4) are diagonal matrices.
''',[10],'Assumption 3 (Cross-sectional independence)',{'D4':'The restriction acts on the coefficient matrices in the linear error representation.'},kind='assumption',context='Assumption 3 (Cross-sectional independence).',phrases=['Assumption 3','diagonal matrices'],shape='Diagonal linear filters; the surrounding Sections 2/3 convention p=tilde-p and iid scalar innovations provides independent component processes. This condition is not inherited by Theorem 4.')
add('D13','Temporal separation',r'''
Define the minimum gap between breaks as $\kappa_n=\min_{0\leq k\leq K}(u_{k+1}-u_k)$, for some $\kappa_n>0$, and we allow $\kappa_n\to0$ as $n$ diverges.
''',[12],'Definition 1 (Temporal separation)',{'D1':'The times and endpoint conventions are those in the trend model (2).'},context='Definition 1 (Temporal separation).',symbols=[r'\kappa_n=\min_{0\leq k\leq K}(u_{k+1}-u_k)'],shape='Minimum separation of successive rescaled break times including the endpoints. The theorem-specific condition b much smaller than kappa_n is recorded separately, not built into this definition.')
members['D13']['application_context']=[dict(text=r'We denote the break location by $\tau_k=nu_k$, $1\leq k\leq K$, and introduce the following assumption for the identification of breaks.',evidence=[dict(page=12,location='Before Definition 1 — sample-index break locations')])]
add('D14','minimum of normalized break sizes',r'''
We consider the size of the break at time point $\tau_k$ normalized by the long-run standard deviation $\Lambda$, that is $|\Lambda^{-1}\gamma_k|_2$. Define the minimum of normalized break sizes over time as
\[
\delta_p=\min_{1\leq k\leq K}|\Lambda^{-1}\gamma_k|_2,\tag{21}
\]
which can be viewed as the minimum strength of signals in the setting of Corollary 1.
''',[14],'Section 2.4 — minimum normalized jump size, equation (21)',{'D1':'The gamma_k are the original vector jumps.','D5':'The jump size is normalized by the long-run standard deviations.'},phrases=['minimum of normalized break sizes'],symbols=[r'\delta_p',r'|\Lambda^{-1}\gamma_k|_2'],shape='Minimum Euclidean size of the standardized true jump vectors. It is distinct from the squared signal condition and from its bias-centered estimator.')
add('D15','Multiple Change-Point Detection',r'''
Data: Observations $Y_1,Y_2,\ldots,Y_n$; bandwidth parameter $b$; threshold value $\omega$

Result: Estimated number of breaks $\widehat K$; estimated break time stamps $\widehat\tau_k$, $k=1,\ldots,\widehat K$; estimated jump vectors $\widehat\gamma_k$; estimated minimum break size over time $\widehat\delta_p$

$\mathcal Q_n\leftarrow\max_{bn+1\leq i\leq n-bn}(|V_i|_2^2-\bar c)$;

if $\mathcal Q_n<\omega$ then

$\widehat K=0$; STOP;

else

$k\leftarrow1$; $\mathcal A_1\leftarrow\{bn+1\leq\tau\leq n-bn:(|V_\tau|_2^2-\bar c)>\omega\}$;

while $\mathcal A_k\neq\varnothing$ do

$\widehat\tau_k\leftarrow\operatorname*{arg\,max}_{\tau\in\mathcal A_k}(|V_\tau|_2^2-\bar c)$; $\widehat\gamma_k\leftarrow\widehat\mu^{(l)}_{\widehat\tau_k-bn}-\widehat\mu^{(r)}_{\widehat\tau_k+bn-1}$;

$\mathcal A_{k+1}\leftarrow\mathcal A_k\setminus\{t:|t-\widehat\tau_k|\leq2bn\}$; $k\leftarrow k+1$;

end

$\widehat K=\max_{k\geq1}\{k:\mathcal A_k\neq\varnothing\}$; $\widehat\delta_p\leftarrow\min_{1\leq k\leq\widehat K}\left||\Lambda^{-1}\widehat\gamma_k|_2^2-\bar c\right|^{1/2}$;

end
''',[14],'Algorithm 1: ℓ2 Multiple Change-Point Detection via a MOSUM',{'D8':'The algorithm selects maxima of the centered aggregated MOSUM statistic and removes nearby candidates.','D3':'Its jump-vector estimate uses the source local averages evaluated at shifted indices.'},context='Algorithm 1: ℓ2 Multiple Change-Point Detection via a MOSUM',symbols=[r'\widehat\tau_k',r'\widehat\gamma_k',r'\widehat\delta_p'],shape='Full greedy temporal detection algorithm with a strict threshold, exclusion radius 2bn, source shifted means and absolute centered square-root estimate. The threshold is an input; it need not be a Gaussian quantile. Equality at Q_n=omega and an empty final maximum need conventions absent from the printed algorithm.')
add('D16','Signal',r'''
Assume $\min_{0\leq k\leq K}n(u_{k+1}-u_k)|\Lambda^{-1}\gamma_k|_2^2\gg\sqrt{p\log(n)}$.
''',[15],'Assumption 4 (Signal)',{'D1':'The condition uses the model jump vectors and their time gaps.','D5':'The signal is standardized by Lambda from (5).'},kind='assumption',context='Assumption 4 (Signal).',phrases=['Assumption 4'],symbols=[r'\min_{0\leq k\leq K}',r'|\Lambda^{-1}\gamma_k|_2^2'],shape='Minimum gap-times-squared-standardized-signal condition. The source starts k at zero even though gamma_0 is not defined by (2); the indexing is preserved as an unresolved source convention. The source notation paragraph reverses the usual meaning of much-greater-than, which is recorded separately.')
add('D17','Linear spatial neighborhood',r'''
Let $\mathcal L_s\subset\{1,\ldots,p\}$ be the set of coordinates in a spatial neighborhood, $1\leq s\leq S$, where $S$ is the total number of spatial neighborhoods. We denote the size of each $\mathcal L_s$ by $|\mathcal L_s|$. In particular, we define
\[
|\mathcal L_{\max}|=\max_{1\leq s\leq S}|\mathcal L_s|\quad\text{and}\quad
|\mathcal L_{\min}|=\min_{1\leq s\leq S}|\mathcal L_s|.\tag{23}
\]
''',[16,17],'Definition 2 (Linear spatial neighborhood)',context='Definition 2 (Linear spatial neighborhood).',symbols=[r'\mathcal L_s',r'|\mathcal L_{\min}|'],shape='Finite coordinate neighborhoods and their minimum and maximum cardinalities. Neighborhoods can overlap and their labels do not impose a spatial order; comparability is the separate Assumption 5.')
members['D17']['application_context']=[dict(text=r'It shall be noted that the spatial neighborhoods defined in Definition 2 can be overlapped, which means that each component series can belong to multiple different spatial neighborhoods.',evidence=[dict(page=17,location='Paragraph following Definition 3')])]
add('D18','linear neighborhood-norm',r'''
For a $p$-dimensional vector $v_i=(v_{i1},\ldots,v_{ip})^\top$ with a linear ordering in coordinates, we define the linear neighborhood-norm (nbd-norm) as $|v_i|_{2,s}=\big(\sum_{j=1}^p v_{i,j}^2\mathbf1_{j\in\mathcal L_s}\big)^{1/2}$, $1\leq s\leq S$.
''',[17],'Definition 3 (Linear nbd-norm)',{'D17':'The coordinate restriction is membership in the spatial neighborhood L_s.'},phrases=['linear neighborhood-norm'],symbols=[r'|v_i|_{2,s}'],shape='Euclidean norm of the coordinates restricted to a designated neighborhood, a seminorm on the whole vector when that neighborhood is proper.')
add('D19','localized breaks',r'''
Our goal is to model the breaks occurring on the vector of unknown trend functions. When there potentially exists a group structure, we formulate the trend function in (1) as
\[
\mu(u)=\mu_0+\sum_{r=1}^R\gamma_r\mathbf1_{u\geq u_r},\tag{24}
\]
where $R\in\mathbb N$ is an unknown integer represents the number of localized breaks which could go to infinity as $n$ or $S$ increases; $u_1,\ldots,u_R$ are the time stamps of the breaks with $0=u_0<u_1<\ldots<u_R<u_{R+1}=1$ and $\kappa_n=\min_{0\leq r\leq R}(u_{r+1}-u_r)$, for some constant $\kappa_n>0$, where $\kappa_n$ is allowed to tend to zero as $n\to\infty$; $\gamma_r=(\gamma_{r,1},\ldots,\gamma_{r,p})^\top\in\mathbb R^p$ is the jump vector at the time stamp $u_r$ with $\gamma_{r,j}=0$ if $j\notin\mathcal L_{s_r}$, where $s_r$ is the index of the spatial location of the $r$-th break. We define the break size as $|\gamma_r|_2$. In the rest of this paper, we use $(\tau_r,s_r)$ to denote the temporal-spatial location of the $r$-th break.

To test the existence of spatially localized breaks, it suffices to test the null hypothesis
\[
\mathcal H_0^\diamond:\quad\gamma_r=0,\quad1\leq r\leq R,
\]
which denotes the case with no breaks, against the alternative that at least one break exists, that is, $\mathcal H_A^\diamond$: there exists $r\in\{1,\ldots,R\}$, such that $\gamma_r\neq0$.
''',[17,18],'Section 3.1 — localized trend and no-break hypothesis, equation (24)',{'D1':'Equation (24) specifies the trend in observation equation (1). Its localized-break count R replaces the earlier K notation.','D17':'The r-th jump has support in its selected coordinate neighborhood.'},kind='source_passage',phrases=['localized breaks'],symbols=[r'\mathcal H_0^\diamond',r'\gamma_{r,j}=0'],shape='Localized piecewise-constant vector trend and its null hypothesis. Support restrictions specify spatial locations without requiring nonzero signals under the null.')
add('D20','Neighborhood size',r'''
Assume that $|\mathcal L_{\max}|/|\mathcal L_{\min}|\leq c$ holds for some constant $c\geq1$, where $|\mathcal L_{\max}|$ and $|\mathcal L_{\min}|$ are defined in Definition 2.
''',[18],'Assumption 5 (Neighborhood size)',{'D17':'The condition compares the extreme neighborhood cardinalities in (23).'},kind='assumption',context='Assumption 5 (Neighborhood size).',phrases=['Assumption 5'],symbols=[r'|\mathcal L_{\max}|/|\mathcal L_{\min}|\leq c'],shape='Uniform comparability of positive spatial neighborhood sizes. It is not a disjointness condition.')
add('D21','centering term',r'''
Similar to (7), we define the centering term of the statistics as
\[
\bar c_s^\diamond=\sum_{j=1}^p c_{s,j}^\diamond,\quad\text{where }c_{s,j}^\diamond=c_j\mathbf1_{j\in\mathcal L_s}.\tag{26}
\]
''',[19],'Section 3.1 — neighborhood centering, equation (26)',{'D7':'The c_j are the coordinate variances defined in (7).','D17':'The sum is restricted to coordinates of L_s.'},phrases=['centering term'],symbols=[r'\bar c_s^\diamond',r'c_{s,j}^\diamond'],shape='Sum of the exact contrast-coordinate variances in a spatial neighborhood. The square-root cardinality normalization belongs to the statistic, not this centering.')
add('D22','Two-Way MOSUM',r'''
Following the intuitions that we could adopt temporal-spatial moving windows to account for spatially clustered jumps, we formulate our Two-Way MOSUM test statistic as follows:
\[
\mathcal Q_n^\diamond=\max_{1\leq s\leq S}\max_{bn+1\leq i\leq n-bn}
\frac1{\sqrt{|\mathcal L_s|}}\big(|V_i|_{2,s}^2-\bar c_s^\diamond\big)\tag{27}
\]
where the nbd-norm $|\cdot|_{2,s}$ is introduced in Definition 3.
''',[19],'Section 3.1 — Two-Way MOSUM statistic, equation (27)',{'D6':'V_i is the standardized local mean contrast (6).','D18':'The squared norm aggregates only the chosen neighborhood.','D21':'The sum is centered by that neighborhood’s exact variance sum.'},phrases=['Two-Way MOSUM'],symbols=[r'\mathcal Q_n^\diamond'],shape='Maximum over neighborhoods and interior time points of the centered neighborhood squared norm divided by the square root of neighborhood cardinality. The null rewrite (28)-(29) is not required to define it.')
add('D23','centered Gaussian vector',r'''
We introduce the centered Gaussian vector
\[
\mathcal Z^\diamond=(Z_{bn+1,1}^\diamond,\ldots,Z_{n-bn,1}^\diamond,\ldots,Z_{bn+1,S}^\diamond,\ldots,Z_{n-bn,S}^\diamond)^\top,\tag{30}
\]
with the covariance matrix
\[
\Xi^\diamond=(\Xi_{i,s,i',s'}^\diamond)_{1\leq i,i'\leq n-2bn,1\leq s,s'\leq S}.\tag{31}
\]
Recall the covariance matrix $\Xi$ for the Gaussian vector $\mathcal Z$ in (11). By (28) and (29), we similarly define
\[
\Xi_{i,s,i',s'}^\diamond=(|\mathcal L_s||\mathcal L_{s'}|)^{-1/2}\mathbf1_{j\in\mathcal L_s\cap\mathcal L_{s'}}\Xi_{i,i'}.\tag{32}
\]
''',[19,20],'Section 3.1 — neighborhood Gaussian comparison law, equations (30)-(32)',{'D17':'The covariance uses the sizes and intersection of two neighborhoods.','D9':'The printed formula invokes Xi from the earlier Gaussian reference law (11).'},phrases=['centered Gaussian vector'],symbols=[r'\mathcal Z^\diamond',r"\Xi_{i,s,i',s'}^\diamond"],shape='Centered Gaussian vector with the covariance formula as printed. Equation (32) has an unbound j in the overlap indicator and no summation; this unresolved source expression is preserved, not replaced by an inferred covariance.')
add('D25','hyper rectangles',r'''
To detect breaks in $\mathcal L_0$, we shall first provide a generalized notion of spatial window accordingly. In particular, denote $\mathcal B_s$, $1\leq s\leq S$, as spatial neighborhoods, which is a generalization of $\mathcal L_s$ in the previous section. Without loss of generality, we focus on hyper rectangles,
\[
\mathcal B_s=I_{s,1}\times I_{s,2}\times\ldots\times I_{s,v},\tag{40}
\]
where $I_{s,r}=I_{s,r,n}=[n_{s,r}^-,n_{s,r}^+]$ is some interval on $\mathbb Z$ whose end points $n_{s,r}^-$ and $n_{s,r}^+$ can depend on $n$. Different $\mathcal B_s$ are allowed to be overlapped and $S$ can go to infinity as $p\to\infty$. We define $I_r=I_{r,n}=[\min_s n_{s,r}^-,\max_s n_{s,r}^+]$ and let $\mathcal B_0=I_1\times I_2\times\ldots\times I_v$, which implies
\[
\cup_{1\leq s\leq S}\mathcal B_s\subset\mathcal B_0.\tag{41}
\]
Suppose that the total number of locations in $\mathcal B_0\cap\mathcal L_0$ denoted as $|\mathcal B_0\cap\mathcal L_0|$ is $p=p_n$, which can go to infinity as $n$ increases.
''',[25],'Section 4.1 — spatial rectangles, equations (40)-(41)',phrases=['hyper rectangles'],symbols=[r'\mathcal B_s',r'\mathcal B_0'],shape='Spatial coordinate rectangles and their enclosing rectangle, with p observed locations in its intersection with L_0. The source declares L_0 a subset of Z^v for fixed v; the random continuous-location assumption is kept separately with its inconsistency noted.')
members['D25']['application_context']=[dict(text=r'Secondly, we move beyond the linear ordering in coordinates by introducing a more comprehensive space in the spatial dimension, denoted as $\mathcal L_0\subset\mathbb Z^v$ (where $v\geq1$ is a fixed integer).',evidence=[dict(page=25,location='Section 4 opening paragraph')])]
add('D26','trend functions',r'''
We consider the time series model
\[
Y_t(\ell)=\mu_\ell(t/n)+\epsilon_t(\ell),\quad t=1,\ldots,n,\quad\ell\in\mathcal B_0\cap\mathcal L_0.\tag{42}
\]
Our main objective is to identify possible change points in the trend functions
\[
\mu_\ell(u)=\mu_{\ell,0}+\sum_{k=1}^K\gamma_{k,\ell}\mathbf1_{\{u\geq u_k,\ell\in\mathcal B_{s_k}\cap\mathcal L_0\}},\tag{43}
\]
where $K$ and $u_1,\ldots,u_K$ are defined similarly to those in (2); $\mu_{\ell,0}\in\mathbb R$ represents the benchmark level when no break occurs, and $\gamma_{k,\ell}\in\mathbb R$ denotes the jump at time point $u_k$ and location $\ell$ in the neighborhood $\mathcal B_{s_k}$, the $k$-th spatial neighborhood containing breaks.
''',[25,26],'Section 4.1 — spatial observation and trend model, equations (42)-(43)',{'D25':'The observations are indexed by locations in the enclosing rectangle, and each jump is restricted to a selected spatial rectangle.'},kind='source_passage',phrases=['trend functions'],symbols=[r'Y_t(\ell)',r'\gamma_{k,\ell}'],shape='Spatially indexed observations with piecewise-constant means. The break-count and ordered-time convention is borrowed from (2), but the nonlinear noise and general spatial coordinates replace the earlier linear model.')
members['D26']['application_context']=[dict(text=r'Under the null hypothesis, where no break exists and $\mathbb E[V_i(\ell)]=0$,',evidence=[dict(page=27,location='Section 4.2 before equation (46)')])]
add('D27','Spatial neighborhood',r'''
(i) (Mass). Define the mass of the spatial neighborhood $\mathcal B_s$ by the number of series in $\mathcal B_s$, i.e. $|\mathcal B_s\cap\mathcal L_0|$, where $|\cdot|$ is the number of elements in a Borel set. Denoted by $B_{\min}$ and $B_{\max}$ the sizes of the smallest and biggest spatial neighborhoods, respectively, i.e.,
\[
B_{\min}=\min_{1\leq s\leq S}|\mathcal B_s\cap\mathcal L_0|,\quad
B_{\max}=\max_{1\leq s\leq S}|\mathcal B_s\cap\mathcal L_0|,
\]
which satisfy $B_{\max}/B_{\min}\leq c$, for some constant $c\geq1$. (ii) (Volume). Define the volume of the spatial neighborhood $\mathcal B_s$ as $\lambda(\mathcal B_s)$, where $\lambda(\cdot)$ is the Lebesgue measure of a Borel set.
''',[26],'Definition 6 (Spatial neighborhood)',{'D25':'Mass and volume refer to the spatial rectangles and observed location set from Section 4.1.'},context='Definition 6 (Spatial neighborhood).',symbols=[r'B_{\min}',r'B_{\max}/B_{\min}\leq c',r'\lambda(\mathcal B_s)'],shape='Full source definition of spatial mass, comparable minimum/maximum mass and volume. The comparability condition is built into this numbered definition. Discrete cardinality and Lebesgue volume are distinct quantities.')
add('D28','Density of spatial space',r'''
Let $\ell_j$, $j=1,\ldots,p$, be the spatial locations in $\mathcal L_0\subset\mathbb Z^v$ on which $Y_t(\ell_j)$ is observed, $t=1,\ldots,n$. Assume that each $\ell_j$ can be written as $\ell_j=(A_1u_{j,1},\ldots,A_vu_{j,v})^\top$. Here, $u_j=(u_{j,1},\ldots,u_{j,v})^\top$ is a sequence of i.i.d. random vectors with a density function $g(x)$ with a compact support in $[0,1]^v$. We assume that $A_r\to\infty$ as $p\to\infty$, for all $r=1,\ldots,v$. Also, for all $x\in[0,1]^v$, $c_1\leq g(x)\leq c_2$, for some constants $c_1,c_2>0$.
''',[26],'Assumption 8 (Density of spatial space L₀)',{'D25':'The location set and fixed spatial dimension are from the general spatial setup.'},kind='assumption',context=r'Assumption 8 (Density of spatial space $\mathcal L_0$).',phrases=['Assumption 8'],symbols=[r'\ell_j=(A_1u_{j,1},\ldots,A_vu_{j,v})^\top',r'c_1\leq g(x)\leq c_2'],shape='Source random-design density condition with iid scaled locations and bounded positive density. The simultaneous lattice-membership assertion is retained rather than silently rounded or replaced by a continuous space.')
add('D29','Neighborhood shape',r'''
There exists a constant $c\geq1$, such that for each neighborhood $\mathcal B_s$, $\max_{1\leq r\leq v}(n_{s,r}^+-n_{s,r}^-)\leq c\min_{1\leq r\leq v}(n_{s,r}^+-n_{s,r}^-)$.
''',[27],'Assumption 9 (Neighborhood shape)',{'D25':'The side lengths are the endpoint differences of the rectangles (40).'},kind='assumption',context='Assumption 9 (Neighborhood shape).',phrases=['Assumption 9'],symbols=[r'\max_{1\leq r\leq v}(n_{s,r}^+-n_{s,r}^-)'],shape='Uniform bound on the ratio of the largest and smallest rectangle side lengths as printed, without an added growth or positive-length hypothesis.')
add('D30','stationary noise process',r'''
Suppose that the stationary noise process $\{\epsilon_t(\ell)\}_{t\in\mathbb Z}$ in (1) is of the form:
\[
\epsilon_t(\ell)=f\big(\eta_{t-k,\ell-\ell'};k\geq0,\ell'\in\mathbb Z^v\big).\tag{49}
\]
Here $\eta_{i,s}$, $i\in\mathbb Z$, $s\in\mathbb Z^v$, are i.i.d. random variables, and $f(\cdot)$ is an $\mathbb R$-valued measurable function such that $\epsilon_t(\ell)$ is well-defined. We assume throughout the paper that $\mathbb E[\epsilon_t(\ell)]=0$ and $\max_{\ell\in\mathcal B_0\cap\mathcal L_0}\|\epsilon_t(\ell)\|_q<\infty$, for some $q\geq4$.
''',[28],'Section 4.3 — nonlinear stationary noise, equation (49)',{'D25':'The finite-moment maximum is over the observed spatial locations.'},phrases=['stationary noise process'],symbols=[r"\epsilon_t(\ell)=f\big(\eta_{t-k,\ell-\ell'};k\geq0,\ell'\in\mathbb Z^v\big)"],shape='Measurable causal-in-time function of iid scalar innovations over a spatial lattice. It is not required to be linear or cross-sectionally independent; Assumption 10 strengthens the basic moment condition to q at least eight.')
add('D31','functional dependence measures',r'''
Next, we introduce the functional dependence measures to characterize the temporal and spatial dependence structure of $\epsilon_t(\ell)$. Let $(\eta'_{i,s})_{i\in\mathbb Z,s\in\mathbb Z^v}$ be an i.i.d. copy of $(\eta_{i,s})_{i\in\mathbb Z,s\in\mathbb Z^v}$. Specifically, we consider the temporal and temporal-spatial coupled versions of $\epsilon_t(\ell)$ defined respectively by
\[
\epsilon_t^*(\ell)=f\big(\eta^*_{t-k,\ell-\ell'};k\geq0,\ell'\in\mathbb Z\big),\quad\text{and}\quad
\epsilon_t^{**}(\ell)=f\big(\eta^{**}_{t-k,\ell-\ell'};k\geq0,\ell'\in\mathbb Z\big),
\]
where for any $i\geq0$ and $s\in\mathbb Z^v$,
\[
\eta_{i,s}^*=\begin{cases}\eta_{i,s},&\text{if }i\neq0,\\\eta'_{i,s},&\text{if }i=0.\end{cases},
\quad\text{and}\quad
\eta_{i,s}^{**}=\begin{cases}\eta_{i,s},&\text{if }i\neq0\text{ and }s\neq0,\\\eta'_{i,s},&\text{if }i=0\text{ or }s=0.\end{cases}
\]
Following Wu (2005), we generalize the functional dependence measures as follows
\[
\theta_{t,\ell,q}=\|\epsilon_t(\ell)-\epsilon_t^*(\ell)\|_q,\quad
\delta_{t,\ell,q}=\|\epsilon_t(\ell)-\epsilon_t^{**}(\ell)\|_q.\tag{50}
\]
''',[28],'Section 4.3 — coupled noises and functional dependence, equation (50)',{'D30':'The coupling replaces innovations in the nonlinear stationary-noise representation (49).'},phrases=['functional dependence measures'],symbols=[r'\theta_{t,\ell,q}',r'\delta_{t,\ell,q}'],shape='Lp distances to the two explicitly coupled noises. The double-star coupling replaces the union of time zero and spatial zero, not just a single innovation. The source Z versus Z^v and nonnegative-time indexing inconsistencies are preserved.')
add('D32','long-run covariance matrix',r'''
Let $\epsilon_t=(\epsilon_t(\ell))^\top_{\ell\in\mathcal B_0\cap\mathcal L_0}$, $t\in\mathbb Z$. We denote the long-run covariance matrix of $\{\epsilon_t\}_{t\in\mathbb Z}$ and the corresponding diagonal matrix by
\[
\Sigma=\big(\sigma(\ell_1,\ell_2)\big)_{\ell_1,\ell_2\in\mathcal B_0\cap\mathcal L_0},\quad\text{and}\quad
\Lambda=\operatorname{diag}\big(\sigma(\ell)\big)_{\ell\in\mathcal B_0\cap\mathcal L_0},\tag{44}
\]
respectively, where $\sigma(\ell)=\sigma(\ell,\ell)$ representing the long-run variance of the component $\epsilon_t(\ell)$.
''',[27],'Section 4.2 — general long-run covariance notation, equation (44)',{'D30':'These are the long-run noise covariances for the general stationary model.'},phrases=['long-run covariance matrix'],symbols=[r'\sigma(\ell)=\sigma(\ell,\ell)'],shape='General long-run covariance matrix and printed diagonal scaling. Unlike (5), the source defines sigma(l) as a variance here, not its square root; the discrepancy affects (45), (50)-(53) and is not silently repaired.')
add('D33','jump statistic',r'''
To test for the existence of breaks, we denote $\widehat\mu_i^{(l)}(\ell)=\sum_{t=i-bn}^{i-1}Y_t(\ell)/(bn)$, $\widehat\mu_i^{(r)}(\ell)=\sum_{t=i}^{i+bn-1}Y_t(\ell)/(bn)$, and evaluate a jump statistic defined by
\[
V_i(\ell)=\sigma^{-1}(\ell)\big(\widehat\mu_i^{(l)}(\ell)-\widehat\mu_i^{(r)}(\ell)\big).\tag{45}
\]
''',[27],'Section 4.2 — spatial jump contrast, equation (45)',{'D26':'The local means average the spatial observations from (42).','D32':'The inverse scaling uses the general source sigma(l) notation (44).'},phrases=['jump statistic'],symbols=[r'V_i(\ell)=\sigma^{-1}(\ell)'],shape='Spatially indexed left-minus-right block-average contrast with the source long-run scaling. Its basic bandwidth and interior-time convention is shared, but it does not inherit diagonal VMA assumptions.')
add('D34','centering term',r'''
Note that $V_i(\ell)$ comprises the signal part $\mathbb E[V_i(\ell)]$ and the noise part $V_i(\ell)-\mathbb E[V_i(\ell)]$. Under the null hypothesis, where no break exists and $\mathbb E[V_i(\ell)]=0$, we define the centering term of the $\ell^2$-aggregation of $V_i(\ell)$ within the neighborhood $\mathcal B_s$ as
\[
c_{\mathcal B_s}=\sum_{\ell\in\mathcal B_s\cap\mathcal L_0}c(\ell),\quad\text{where }c(\ell)=\operatorname{Var}[V_i(\ell)].\tag{46}
\]
''',[27],'Section 4.2 — spatial variance centering, equation (46)',{'D33':'The sum uses the variances of the spatial jump contrasts.','D25':'The sum runs over observed locations in B_s.'},phrases=['centering term'],symbols=[r'c_{\mathcal B_s}',r'c(\ell)=\operatorname{Var}[V_i(\ell)]'],shape='Exact sum of marginal contrast variances in each general spatial neighborhood, irrespective of cross-sectional covariance between different locations.')
add('D35','generalized Two-Way MOSUM',r'''
Subsequently, we propose the following test statistic
\[
\widetilde{\mathcal Q}_n=\max_{1\leq s\leq S}\max_{bn+1\leq i\leq n-bn}Q_{i,\mathcal B_s},\quad\text{where}\quad
Q_{i,\mathcal B_s}=\frac1{\sqrt{|\mathcal B_s\cap\mathcal L_0|}}\left(\sum_{\ell\in\mathcal B_s\cap\mathcal L_0}V_i^2(\ell)-c_{\mathcal B_s}\right).\tag{47}
\]
''',[27],'Section 4.2 — generalized Two-Way MOSUM, equation (47)',{'D33':'The statistic aggregates squared spatial jump contrasts.','D34':'The sum is centered by c_Bs from (46).','D27':'Normalization is by the square root of the neighborhood mass, with the Definition 6 comparability convention.'},context='We now introduce a generalized Two-Way MOSUM, designed to accommodate the multi-dimensional spatial space constructed in the previous section.',symbols=[r'\widetilde{\mathcal Q}_n',r'Q_{i,\mathcal B_s}'],shape='Maximum over spatial rectangles and interior time points of centered squared contrasts divided by square-root neighborhood mass. It uses the general covariance scaling as printed.')
add('D36','Finite moment',r'''
Assume $\max_{\ell\in\mathcal B_0\cap\mathcal L_0}\|\epsilon_t(\ell)\|_q<\infty$, for $q\geq8$.
''',[29],'Assumption 10 (Finite moment)',{'D30':'The moment bound concerns the nonlinear noise output itself, rather than the individual VMA innovations.'},kind='assumption',context='Assumption 10 (Finite moment).',phrases=['Assumption 10'],symbols=[r'\|\epsilon_t(\ell)\|_q'],shape='Finite q-moments of the general noise over all observed locations, q at least eight. It is distinct from Assumption 1 on scalar linear innovations.')
add('D37','Temporal dependence',r'''
There exist some constants $C>0$ and $\beta>0$, such that, for all $h\geq0$, $\max_{\ell\in\mathcal B_0\cap\mathcal L_0}\sum_{k\geq h}\theta_{k,\ell,q}/\sigma(\ell)\leq C(1\vee h)^{-\beta}$, for $q\geq8$.
''',[29],'Assumption 11 (Temporal dependence)',{'D31':'The condition sums the temporal functional dependence measures theta from (50).','D32':'Each dependence measure is normalized by the source sigma(l) scale.'},kind='assumption',context='Assumption 11 (Temporal dependence).',phrases=['Assumption 11'],symbols=[r'\theta_{k,\ell,q}/\sigma(\ell)'],shape='Uniform polynomial tail decay of normalized temporal functional dependence for all nonnegative lags. This is not the earlier VMA coefficient-row condition.')
add('D38','Weak cross-sectional dependence',r'''
Assume that there exist some constants $C'>0$ and $\xi>1$, such that, for all $m\geq0$,
\[
\sum_{k\geq0}\left(\sum_{\{\ell\in\mathcal B_0\cap\mathcal L_0:|\ell|_2\geq m\}}\delta_{k,\ell,q}^2/\sigma^2(\ell)\right)^{1/2}\leq C'(1\vee m)^{-\xi}.\tag{51}
\]
''',[29],'Assumption 12 (Weak cross-sectional dependence)',{'D31':'The condition uses the temporal-spatial coupled dependence measure delta.','D32':'The source long-run scale normalizes each coordinate.'},kind='assumption',context='Assumption 12 (Weak cross-sectional dependence).',phrases=['Assumption 12'],symbols=[r'\delta_{k,\ell,q}^2/\sigma^2(\ell)',r'\xi>1'],shape='Spatial l2 tail aggregated in temporal l1 with decay exponent xi greater than one. The aggregation order and origin-based radius are preserved; the derived inequality (52) is not substituted as the assumed condition.')
add('D39','long-run correlation',r'''
\[
\widetilde\rho(\ell_1,\ell_2)=\sigma(\ell_1,\ell_2)/\big(\sigma(\ell_1)\sigma(\ell_2)\big)
\]
''',[29],'Lemma 1 — defining equality in equation (53), excerpt only',{'D32':'The ratio uses the general long-run covariance and source diagonal scales (44).'},kind='source_passage',context=r'the long-run correlation between $\epsilon_t(\ell_1)$ and $\epsilon_t(\ell_2)$, denoted by $\widetilde\rho(\ell_1,\ell_2)$,',symbols=[r'\widetilde\rho(\ell_1,\ell_2)'],shape='Only the defining equality in (53) is extracted. The lemma’s decay conclusion is a proof result and does not become an extra premise of the Gaussian reference law. The variance-versus-standard-deviation issue in (44) is preserved.')
add('D40','centered Gaussian random vector',r'''
the centered Gaussian random vector
\[
\widetilde{\mathcal Z}=(\widetilde Z_{bn+1,1},\ldots,\widetilde Z_{n-bn,1},\ldots,\widetilde Z_{bn+1,S},\ldots,\widetilde Z_{n-bn,S})^\top,\tag{54}
\]
with the covariance matrix
\[
\widetilde\Xi=(\widetilde\Xi_{i,s,i',s'})_{1\leq i,i'\leq n-2bn,1\leq s,s'\leq S}.\tag{55}
\]
Let $\pi_{s,s',\ell_1,\ell_2}=(|\mathcal B_s\cap\mathcal L_0||\mathcal B_{s'}\cap\mathcal L_0|)^{-1/2}\mathbf1_{\ell_1,\ell_2\in\mathcal B_s\cap\mathcal B_{s'}\cap\mathcal L_0}$, and $\widetilde\Xi_{i,s,i+\zeta bn,s'}$ equals to
\[
(bn)^{-2}\sum_{\ell_1,\ell_2\in\mathcal B_0\cap\mathcal L_0}\pi_{s,s',\ell_1,\ell_2}
\begin{cases}
(15\zeta^2-20\zeta+8)\widetilde\rho^2(\ell_1,\ell_2)+3\zeta^2-4\zeta,&0<\zeta\leq1,\\
(3\zeta^2-12\zeta+12)\widetilde\rho^2(\ell_1,\ell_2)-\zeta^2+4\zeta-4,&1<\zeta\leq2,\\
0,&\zeta>2.
\end{cases}\tag{56}
\]
''',[30],'Section 4.4 — general Gaussian comparison law, equations (54)-(56)',{'D27':'The overlap weights are normalized by neighborhood masses.','D39':'The covariance kernel uses the long-run correlation ratio defined in (53).'},phrases=['centered Gaussian random vector'],symbols=[r'\widetilde{\mathcal Z}',r"\widetilde\Xi_{i,s,i+\zeta bn,s'}"],shape='General Gaussian vector with the exact printed covariance expression and intersection weights. The zero-lag case is absent, so the main-text formula does not completely specify the covariance. The referenced appendix Lemma 15 is not inspected.')
# Source-inspected selector amendment; original statements are unchanged.
members['D38']['highlight_symbols'] = ['\\left(\\sum_{\\{\\ell\\in\\mathcal B_0\\cap\\mathcal L_0:|\\ell|_2\\geq m\\}}\\delta_{k,\\ell,q}^2/\\sigma^2(\\ell)\\right)^{1/2}', '\\xi>1']

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(interfaces),'source-backed interfaces; extraction remains in progress.')


if __name__ == '__main__':
    main()
