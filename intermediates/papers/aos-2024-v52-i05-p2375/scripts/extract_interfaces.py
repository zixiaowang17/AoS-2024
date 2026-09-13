"""Preserve the original time-series objects without changing source definitions."""
import json
from save_inventory import ROOT,PID,STATEMENTS
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,boundary,heading,kind='definition',context=None,context_page=None,phrases=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=phrases or [])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=boundary,semantic_boundary=boundary,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'norm',r'''for a random variable $X$, we define its $m$ norm as $\|X\|_m=(E|X|^m)^{1/m}$, where $m\ge1$.''',[6],[],[r'\|X\|_m'],'Moment norm, not the vector or matrix norm also used in the paper. Theorem assumptions use m≥8 and nondegeneracy uses this norm at m=2.','Notation — Random-variable moment norm')
add(2,'generating equation',r'''Let $e_i$, $i\in\mathbb Z$ be independent (but non-necessarily identically distributed) random variables and consider random variables $X_{i,j}$ generated as
\[
X_{i,j}=g_{i,j}(\ldots,e_{i-2},e_{i-1},e_i),\text{ for }i\in\mathbb Z\text{ and }j=1,2,\ldots,d.
\]
(2)
In fact, our approach allows the measurable functions $g_{i,j}$ to change with respect to the sample size $T$, i.e., $g_{i,j}$, $i\in\mathbb Z$, $j=1,2,\ldots,d$, may vary with respect to different sample size $T$. To simplify notation, in the following we will not explicitly stress the dependency of $g_{i,j}$ on $T$ and if $d=1$, then we will omit the subscript $j$ and simple write $X_i$ for $X_{i,1}$.''',[6,7],[],[r'g_{i,j}',r'X_{i,j}'],'Causal measurable triangular-array construction from independent innovations with individually varying laws. Neither identical innovation laws nor time-invariant g is required. Here d is coordinate dimension; later the same letter denotes maximum lag.','Section 2 — Generating equation (2)',context='The generating equation (2) has been used in Wu (2005)',context_page=7)
add(3,'dependence',r'''Define a sequence of random variables $e_i^\dagger$, $i\in\mathbb Z$, such that $e_i^\dagger$ are independent from each other, $e_i^\dagger$ has the same distribution as $e_i$, and $e_i,e_j^\dagger$ are mutually independent for any $i,j\in\mathbb Z$.
For any $k\in\mathbb Z$, define
\[
X_{i,j}(k)=\begin{cases}g_{i,j}(\ldots,e_{i-k-1},e_{i-k}^\dagger,e_{i-k+1},\ldots,e_i)&\text{if }k\ge0,\\X_{i,j}&\text{if }k<0.\end{cases}
\]
(3)
Furthermore, for any $m\ge1$, define
\[
\delta_{i,j,m}(k)=\|X_{i,j}-X_{i,j}(k)\|_m\text{ and }\delta_m(k)=\sup_{i\in\mathbb Z,j=1,\ldots,d}\delta_{i,j,m}(k)
\]
(4)
According to (3), $\delta_{i,j,m}(k)=\delta_m(k)=0$ if $k<0$.''',[7,8],[1,2],[r'\delta_{i,j,m}(k)',r'\delta_m(k)',r'e_{i-k}^\dagger'],'Single-innovation replacement coupling and uniform moment distance. Copies retain each innovation’s own law. Negative-lag coupling leaves X unchanged.','Section 2 — Coupling and dependence coefficients (3)–(4)',context='This section introduces a new kind of dependence for possible non-stationary random variables',context_page=6)
add(4,'medium range dependent',r'''Suppose that the random variables $X_{i,j}$, $i\in\mathbb Z$, $j=1,\ldots,d$ satisfy (2). Let $X_{i,j}$, $i=1,2,\ldots,T$, $j=1,\ldots,d$ be the observed time series and $m,\alpha,\beta$ constants such that $m\ge4$, $\alpha>1$, $\beta\ge0$.
We say that the random variable $X_{i,j}$ are $(m,\alpha,\beta)$-medium range dependent if
\[
EX_{i,j}=0\text{ for all }i,j
\]
\[
\sup_{i\in\mathbb Z,j=1,\ldots,d}\|X_{i,j}\|_m=O(1)
\]
\[
\text{and }\sup_{k=0,1,\ldots}(1+k)^\alpha\sum_{l=k}^\infty\delta_m(l)=O(T^\beta)
\]
(5)''',[8],[1,2,3],[r'(m,\alpha,\beta)',r'\delta_m(l)',r'O(T^\beta)'],'Full original Definition1, including zero means, uniform m moments and weighted dependence-tail sums. Appears in theorem closure because short range is explicitly its β=0 special case; no theorem is weakened to a free positive β.','Definition 1 ((m, α, β)-medium range dependent random variables)')
add(5,'short range dependent random variables',r'''A special case of Definition 1 is when $\beta=0$, i.e., $\sup_{k=0,1,\ldots}(1+k)^\alpha\sum_{l=k}^\infty\delta_m(k)=O(1)$. If this happens, we call $X_{i,j}$, $(m,\alpha)$-short range dependent random variables.''',[8],[4],[r'\beta=0',r'(m,\alpha)'],'The source explicitly defines the β=0 specialization of Definition1. Remark2 prints δ_m(k), with k instead of summation index l; this typo is preserved and separately flagged. It does not replace the definition’s tail sum by an infinite sum of a constant.','Remark 2 ((m, α)-short range dependent random variables)')
add(6,'autocovariances',r'''This section goes back to the original problem, namely that of estimating the autocovariances of a weakly, but not necessarily strictly stationary time series. Suppose that $\{X_i,i\in\mathbb Z\}$ form a stochastic process with $EX_i=0$ and $X_1,X_2,\ldots,X_T$ is the time series observed, (similar to $X_i$ forming a triangular array, the underlying process may be different for different sample sizes $T$). Define $\sigma_j=EX_iX_{i-j}=EX_0X_{-j}$.''',[14],[],[r'\sigma_j',r'EX_i=0'],'Lag-only autocovariance of the mean-zero weakly stationary process, which may vary with T. This Section3 setting applies to autocovariance/autocorrelation inference; it is not imposed on Theorem1’s general nonstationary products.','Section 3 — Autocovariances and standing stationarity context')
add(7,'sample autocovariances',r'''\[
\widehat\sigma_j=\frac1T\sum_{i=j+1}^TX_iX_{i-j}
\]''',[14],[],[r'\widehat\sigma_j'],'Raw lag-product estimator, denominator T and lower index j+1. No estimated-mean centering, denominator T−j or circular extension is inserted. Its arithmetic definition does not itself assume stationarity.','Section 3 — Sample autocovariance, equation (16)',context='we use the sample autocovariances and the sample autocorrelations as estimators',context_page=14)
add(8,'autocorrelations',r'''the autocorrelations $\rho_j=\sigma_j/\sigma_0$.''',[14],[6],[r'\rho_j=\sigma_j/\sigma_0'],'Population autocorrelation as the lag covariance divided by positive lag-zero variance. Theorem2(ii) separately assumes σ0>c; ratio conventions outside that domain are not specified.','Section 3 — Population autocorrelations')
add(9,'sample autocorrelations',r'''$\widehat\rho_j=\widehat\sigma_j/\widehat\sigma_0$.''',[14],[7],[r'\widehat\rho_j'],'Ratio of the sample covariances from (16). The printed source does not prescribe a zero-denominator convention.','Section 3 — Sample autocorrelation, equation (16)',context='we use the sample autocovariances and the sample autocorrelations as estimators',context_page=14)
add(10,'linear combinations','Let $a_{ij}$'+STATEMENTS[0].split('Let $a_{ij}$',1)[1].split(' Assume that',1)[0],[11],[],[r'Z_{i,k}',r'a_{kj}',r'p_1=O(T^{\alpha_{p_1}})'],'General deterministic linear combinations of individually centered lag products, with uniform squared-coefficient sum and separate dimension-growth bound. Centering may depend on i. The five inequalities and nondegeneracy premise stay separately in the complete theorem and auxiliary conditions.','Theorem 1 — Linear combinations and coefficient bounds (10)',kind='theorem_excerpt',context='this parameter represents the number of simultaneous linear combinations taken into consideration',context_page=12)
add(11,'linear combinations',r'''Define
\[
Z_{i,j}=-\frac{\sigma_j}{\sigma_0^2}(X_i^2-\sigma_0)+\frac1{\sigma_0}(X_iX_{i-j}-\sigma_j)
\]''',[15],[6],[r'Z_{i,j}',r'-\frac{\sigma_j}{\sigma_0^2}'],'Autocorrelation linearization, including the lag-zero variance correction and positive denominator requirement. Theorem2 uses the same Z symbol as Theorem1 with a new local definition.','Theorem 2(ii) — Autocorrelation linearization',kind='theorem_excerpt',context='in Section 3 and Section 4, we estimate the autocovariances, autocorrelations, and AR coefficients with maximum lag $d$, respectively, $p$. Therefore, the number of simultaneous linear combinations considered in these sections are smaller or equal to $d$.',context_page=12)
add(12,'AR coefficients',r'''Suppose that the stochastic process $\{X_i,i\in\mathbb Z\}$ is weakly stationary (i.e., satisfies Definition 1.3.2 in Brockwell and Davis (1991)), and for a given positive integer $p$, suppose that the solution $a_1,\ldots,a_p$ of the Yule-Walker system
\[
\sigma_k=\sum_{j=1}^pa_j\sigma_{|k-j|},\text{ where }k=1,2,\ldots,p.
\]
(26)
exists. Then, $a_1,\ldots,a_p$ are called the AR coefficients of order $p$.''',[17],[6],[r'a_1,\ldots,a_p',r'\sigma_{|k-j|}'],'Original Yule–Walker coefficients for a general weakly stationary process, assuming a solution exists. They describe the best linear predictor, not a requirement that data arise from a linear AR model with iid innovations. Theorem3 separately ensures uniqueness by a uniform covariance eigenvalue bound.','Definition 3 (AR coefficients of order p for a general time series)')
add(13,'Yule-Walker estimators',r'''Replacing the autocovariances $\sigma_j$ by sample estimators and solving the corresponding linear system, i.e.,
\[
\widehat\sigma_k=\sum_{j=1}^p\widehat a_j\widehat\sigma_{|j-k|},\text{ where }\widehat\sigma_k\text{ satisfies equation (16),}
\]
(24)
leads to the set of moment estimators of $a_j$, $j=1,2,\ldots,p$, known as Yule-Walker estimators.''',[16],[7,12],[r'\widehat a_j',r'\widehat\sigma_{|j-k|}'],'Sample moment equations defining estimated AR coefficients. The original definition specifies a solution; the Moore–Penrose convention is explicit for bootstrap coefficients later, and is not silently substituted here.','Section 4 — Yule–Walker estimators (24)')
add(14,'matrix',r'''Define the matrix $\Sigma=\{\sigma_{|j-k|}\}_{j,k=1,\ldots,p}$ and assume that it is non-singular for every $p\in\mathbb N$. Let $e_i=(\underbrace{0,0,\ldots,0}_{i-1},1,0,\ldots,0)^T\in\mathbb R^p$ be the vector with the one appearing in the $i$th position, $\gamma=(\sigma_1,\sigma_2,\ldots,\sigma_p)^T$ and $T_i$ the $p\times p$ matrix, $T_i=\{t^{(i)}_{|j-k|}\}_{j,k=1,\ldots,p}$, $i=0,1,\ldots,p-1$ such that $t_s^{(i)}=1$ if $s=i$ and $0$ otherwise.''',[18],[6],[r'\Sigma',r'\gamma',r'T_i'],'Toeplitz covariance matrix, lag-covariance vector, coordinate vectors and lag-selector matrices for the Yule–Walker derivative. The symbol e_i here is a finite-dimensional basis vector, not an innovation in Section2.','Section 4 — Covariance matrix and derivative notation')
add(15,'matrix',r'''Define the matrix $B=\{b_{jk}\}_{j=1,\ldots,p,k=0,1,\ldots,p}=(b_0,b_1,\ldots,b_p)\in\mathbb R^{p\times(p+1)}$ such that $b_0=-\Sigma^{-2}\gamma$; $b_i=\Sigma^{-1}e_i-\Sigma^{-1}T_i\Sigma^{-1}\gamma$ for $i=1,\ldots,p-1$; and $b_p=\Sigma^{-1}e_p$.''',[18],[14],[r'b_0=-\Sigma^{-2}\gamma',r'b_i=\Sigma^{-1}e_i-\Sigma^{-1}T_i\Sigma^{-1}\gamma',r'b_p=\Sigma^{-1}e_p'],'All p+1 columns of the population Yule–Walker derivative matrix, including the special endpoints k=0 and k=p. B here is a matrix, distinct from dimension-growth or simulation-count scalars also called B.','Section 4 — Matrix of AR linearization coefficients')
add(16,'linear combinations',r'''Finally, for $j=1,2,\ldots,p$, let
\[
Z_{i,j}=\sum_{k=0}^pb_{jk}(X_iX_{i-k}-\sigma_k^{(i)}).
\]
(27)''',[18],[6,15],[r'Z_{i,j}',r'\sigma_k^{(i)}'],'Population AR linearization using the derivative coefficients. The printed σ_k^(i) is not defined in this main text; weak stationarity suggests σ_k, but that interpretation remains a separate source note.','Section 4 — AR linearization (27)',context='in Section 3 and Section 4, we estimate the autocovariances, autocorrelations, and AR coefficients with maximum lag $d$, respectively, $p$. Therefore, the number of simultaneous linear combinations considered in these sections are smaller or equal to $d$.',context_page=12)
add(17,'Kernel function',r'''$K(\cdot):\mathbb R\to[0,\infty)$ is a symmetric, continuously di-fferentiable function, with $K(0)=1$, $\int_{\mathbb R}K(x)\,dx<\infty$ and $K(x)$ decreasing on $[0,\infty)$. Define the Fourier transformation of $K$ as $FK(x)=\int_{\mathbb R}K(t)\exp(-2\pi itx)\,dt$, where $i=\sqrt{-1}$. Assume $FK(x)\ge0$ for all $x\in\mathbb R$ and $\int_{\mathbb R}FK(x)\,dx<\infty$.''',[12],[],[r'K(0)=1',r'FK(x)\ge0'],'Full kernel definition, including nonnegative integrable Fourier transform, symmetry, differentiability and monotonicity. No unit-integral normalization is imposed. These properties support a positive-semidefinite multiplier covariance matrix. Preserve the unusual printed di-fferentiable word.','Definition 2 (Kernel function)',context='Definition 2 (Kernel function)',context_page=12)
add(18,'bandwidth',r'''$k_T>0$ is a bandwidth and $k_T\to\infty$ as $T\to\infty$.
\[
v_T=\begin{cases}k_T^{2-\alpha}&\text{if }2<\alpha<3,\\\log(k_T)/k_T&\text{if }\alpha=3,\\1/k_T&\text{if }\alpha>3.\end{cases}
\]''',[13],[],[r'v_T',r'\log(k_T)/k_T'],'Three-case numerical bandwidth bias sequence from Lemma3. Theorem4 invokes its definition with α=α_X, not every assumption of the covariance-estimation Lemma3. Separate bandwidth growth restrictions are retained branchwise.','Lemma 3 — Bandwidth and bias sequence',kind='source_passage')
add(19,'probability and expectation in the bootstrap world',r'''We use the notation $\operatorname{Prob}^*$ and $E^*$, defined as $\operatorname{Prob}^*(\cdot)=\operatorname{Prob}(\cdot\mid X_1,\ldots,X_T)$ and $E^*\cdot=E(\cdot\mid X_1,\ldots,X_T)$, to represent probability and expectation in the bootstrap world.''',[19],[],[r'\operatorname{Prob}^*',r'E^*'],'Conditional probability and expectation with the observed series fixed. The Op and op rates in Theorem4 refer to outer randomness in the original data.','Section 5 — Conditional bootstrap probability')
add(20,'second-order residuals',r'''Define the ‘second-order residuals’ $\widehat\epsilon_i^{(j)}=X_iX_{i-j}-\widehat\sigma_j$ for $j=0,1,\ldots,d$ and $i=j+1,j+2,\ldots,T$.''',[21],[7],[r'\widehat\epsilon_i^{(j)}'],'Residuals of observed lag products, not residuals from fitting an autoregression. Each lag has its own valid observation range and sample autocovariance centering.','Algorithm 1, step 1 — Second-order residuals')
add(21,'joint normal random variables',r'''Generate joint normal random variables $\varepsilon_1,\ldots,\varepsilon_T$ such that $E\varepsilon_j=0$ and $E\varepsilon_{j_1}\varepsilon_{j_2}=K((j_1-j_2)/k_T)$.''',[21],[17],[r'\varepsilon_{j_1}\varepsilon_{j_2}',r'K((j_1-j_2)/k_T)'],'Mean-zero dependent Gaussian multipliers with kernel covariance at the time-index difference divided by bandwidth. Generated in the conditional bootstrap experiment. They are distinct from the process innovations e_i and lag-product residuals.','Algorithm 1, step 2 — Gaussian multipliers')
add(22,'Second-Order Wild Bootstrap',r'''Then calculate
\[
\widehat\sigma_j^*=\widehat\sigma_j+\frac1T\sum_{i=j+1}^T\widehat\epsilon_i^{(j)}\times\varepsilon_i\text{ for }j=0,1,\ldots,d
\]
(38)''',[21],[7,20,21],[r'\widehat\sigma_j^*',r'\widehat\epsilon_i^{(j)}\times\varepsilon_i'],'Bootstrap autocovariance perturbation from dependent multipliers times second-order residuals, with denominator T and the exact lag-dependent lower summation bound. This resamples products rather than generating a new underlying time series.','Algorithm 1, step 2 — Bootstrap autocovariances (38)',context='Algorithm 1 (Second-Order Wild Bootstrap)',context_page=21)
add(23,'sample autocorrelations',r'''$\widehat\rho_j^*=\widehat\sigma_j^*/\widehat\sigma_0^*\text{ for }j\in\mathcal I$.''',[22],[22],[r'\widehat\rho_j^*',r'\widehat\sigma_0^*'],'Bootstrap autocorrelation is the ratio of perturbed covariances, not a linearized multiplier statistic. No convention for zero bootstrap variance is supplied by the source.','Algorithm 1, step 3 — Bootstrap autocorrelations (40)',context=r'Calculate the sample autocovariances $\widehat\sigma_j$, $j=0,1,\ldots,d$ and the sample autocorrelations $\widehat\rho_j$, $j=1,2,\ldots,d$ as in (16).',context_page=21)
add(24,'AR coefficients',r'''Define $\widehat\Sigma^*$ and $\widehat\gamma^*$ as
\[
\widehat\Sigma^*=\{\widehat\sigma^*_{|j-k|}\}_{j,k=1,\ldots,p}\text{ and }\widehat\gamma^*=(\widehat\sigma_1^*,\ldots,\widehat\sigma_p^*)^T
\]
(39)
\[
\widehat a^*=(\widehat a_1^*,\ldots,\widehat a_p^*)^T=\widehat\Sigma^{*\dagger}\widehat\gamma^*
\]
(40)
recall that $\dagger$ represents the Moore-Penrose pseudo inverse.''',[22],[22],[r'\widehat\Sigma^{*\dagger}',r'\widehat a^*'],'Bootstrap Yule–Walker coefficient vector obtained with the Moore–Penrose inverse of the perturbed Toeplitz matrix. It is not an inverse of the unperturbed population covariance.','Algorithm 1, step 3 — Bootstrap AR coefficients (39)–(40)',context='Then calculate the sample AR coefficients',context_page=21)
add(25,'cumulative distribution function',r'''where $\tau\in\{\sigma,\rho,a\}$; and $H_\sigma(x)$, $H_\rho(x)$, $H_a(x)$, respectively, represent $\operatorname{Prob}(\max_{j\in\mathcal H}|\xi_j|\le x)$ in (19), $\operatorname{Prob}(\max_{j\in\mathcal I}|\zeta_j|\le x)$ in (21) and $\operatorname{Prob}(\max_{j=1,\ldots,p}|\xi_j|\le x)$ in (29).''',[23],[6,11,16],[r'H_\sigma(x)',r'H_\rho(x)',r'H_a(x)'],'Three distinct Gaussian maximum target CDFs, with the Gaussian means and covariances specified in Theorems2 and3. The target and dimension may vary with T. The repeated ξ symbol denotes different vectors in (19) and (29). The misindexed covariance in (19) is retained as a source issue.','Section 5 — Gaussian target distribution functions',context='the empirical cumulative distribution function',context_page=22)
# Readable titles use only source terms; every added keyword has its own context.
def title_keywords(n,parts):
    x=interfaces[n-1];m=members['D'+str(n)]
    for term,context,page in parts:
        assert term in context
        cid=m['local_id']+'/name'+str(len(x['source_keywords'])+1)
        m.setdefault('naming_context',[]).append(dict(context_id=cid,text=context,evidence=[dict(page=page,location='Original naming context')]))
        x['source_keywords'].append(dict(paper_id=PID,local_id=m['local_id'],source_text=term,label=term[0].upper()+term[1:],kind='term',context_id=cid))
    x['name']=' · '.join(k['label'] for k in x['source_keywords'])
title_keywords(11,[('autocorrelations','in Section 3 and Section 4, we estimate the autocovariances, autocorrelations, and AR coefficients',12)])
title_keywords(15,[('AR coefficients','approximation result for the AR coefficients.',18)])
title_keywords(16,[('AR coefficients','approximation result for the AR coefficients.',18)])
title_keywords(22,[('sample autocovariances','Calculate the sample autocovariances',21)])
title_keywords(23,[('Second-Order Wild Bootstrap','Algorithm 1 (Second-Order Wild Bootstrap)',21)])
title_keywords(24,[('Second-Order Wild Bootstrap','Algorithm 1 (Second-Order Wild Bootstrap)',21)])
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
