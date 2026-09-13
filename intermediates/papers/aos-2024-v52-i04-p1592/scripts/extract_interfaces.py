"""Rebuild original main-text passages and local dependencies for this paper.

The saved data is manually transcribed; source audit is a separate stage.
"""
import json
from pathlib import Path
from save_inventory import PID, claims

ROOT = Path(__file__).resolve().parents[1]
interfaces, members, edges = [], {}, {}


def add(lid, term, body, pages, heading, deps=None, *, kind='definition',
        symbols=(), phrases=(), context=None, context_pages=None, shape):
    evidence = [dict(page=p, location=heading) for p in pages]
    member = dict(paper_id=PID, local_id=lid, local_label=heading,
        source_heading=heading, source_kind=kind, statement_original=body.strip(),
        relation='exact', depends_on=list(deps or {}), evidence=evidence,
        highlight_symbols=list(symbols), highlight_phrases=list(phrases))
    keyword = dict(paper_id=PID, local_id=lid, source_text=term,
                   label=term[0].upper()+term[1:], kind='term')
    if term not in body:
        assert context and term in context, (lid, term)
        member['naming_context'] = [dict(context_id=lid+'/name', text=context,
            evidence=[dict(page=p, location=heading+' — naming context') for p in (context_pages or pages)])]
        keyword['context_id'] = lid+'/name'
    interfaces.append(dict(interface_id=PID+'/'+lid, rank_group='all', name=keyword['label'],
        lean_role='hypothesis' if kind in ('condition', 'assumption') else 'definition',
        type_shape=shape, semantic_boundary=shape, members=[member], source_keywords=[keyword],
        central_claim_uses=[], dependencies=[], theorem_explanations={}))
    members[lid] = member
    edges[lid] = deps or {}

add('D1','observed sample',r'''
Let $(\boldsymbol Z_1,\ldots,\boldsymbol Z_n)$ be the observed sample where each observation is an independent copy of the tuple $\boldsymbol Z=(\boldsymbol L,A,Y)$ with support $\mathcal Z=\mathcal L\times\mathcal A\times\mathcal Y$. Here $\mathcal L\subseteq\mathbb R^d$ and $\boldsymbol L$ is the vector containing the $d$ potential confounder variables (covariates); $\mathcal A\subseteq\mathbb R$ and $A$ is the continuous treatment dosage received; $\mathcal Y\subseteq\mathbb R$ and $Y$ is the observable outcome of interest. We let $P$ denote the distribution of $\boldsymbol Z$ and $p_0(\boldsymbol z)=p_0(y|\boldsymbol l,a)p_0(a|\boldsymbol l)p_0(\boldsymbol l)$ denote the corresponding density function with respect to some dominating measure $\nu$.
''',[9],'Section 2.1 — observed sample',symbols=[r'\boldsymbol Z=(\boldsymbol L,A,Y)'],kind='source_passage',shape='Independent identically distributed observational triples; continuous treatment and arbitrary real outcome. The dominating measure is not necessarily Lebesgue measure on the whole product space.')
add('D2','outcome regression function',r'''
Let $\mu_0(\boldsymbol l,a):=\mathbb E(Y|\boldsymbol L=\boldsymbol l,A=a)$ denote the outcome regression function.
''',[9],'Section 2.1 — outcome regression',{'D1':'The conditional mean concerns the outcome and observed covariates in the sampled triples.'},symbols=[r'\mu_0(\boldsymbol l,a)'],shape='Conditional mean under the observed law, distinct from the potential-outcome estimand.')
add('D3','conditional density or propensity score function',r'''
Similarly, let $\pi_0(a|\boldsymbol l):=\frac{\partial}{\partial a}P(A\le a|\boldsymbol L=\boldsymbol l)$ denote the conditional density or propensity score function of $A$ given $\boldsymbol L$ and $\varpi_0(a):=\frac{\partial}{\partial a}P(A\le a)$ denote the marginal density function of $A$ (both of which densities are assumed to exist).
''',[9],'Section 2.1 — treatment densities',{'D1':'Both treatment densities are taken under the observed law.'},symbols=[r'\pi_0(a|\boldsymbol l)',r'\varpi_0(a)'],shape='Continuous-treatment conditional and marginal densities; no binary propensity interpretation. The adjacent marginal-density definition is preserved in the same original sentence.')
add('D4','empirical distribution',r'''
For a function $f$ on $\mathbb R$, we let $\mathbb P\{f(\boldsymbol Z)\}:=\int_{\mathcal Z}f(\boldsymbol z)\,dP(\boldsymbol z)$. And for $p\ge1$, we use $\|f\|_p:=\{\int f(\boldsymbol z)^p\,dP(\boldsymbol z)\}^{1/p}$ to denote the $L_p(P)$ norm and use $\|f\|_{\mathcal X}:=\sup_{x\in\mathcal X}|f(x)|$ to denote the uniform norm over the range $\mathcal X$. We use $\mathbb P_n$ to denote the empirical distribution defined on the observed data so that $\mathbb P_n\{f(\boldsymbol Z)\}:=\int f(\boldsymbol z)\,d\mathbb P_n(\boldsymbol z)=n^{-1}\sum_{i=1}^n f(\boldsymbol Z_i)$.
''',[9],'Section 2.1 — integration and norm conventions',{'D1':'The empirical distribution averages over the original independent sample.'},symbols=[r'\mathbb P_n',r'\|f\|_p'],shape='Blackboard P is expectation notation and blackboard P_n is the empirical functional. Preserve the printed Lp formula without absolute values and its stated function domain; note their scope issues separately.')
add('D5','potential outcome',r'''
To characterize the problem, let $Y^a$ be the potential outcome [Rubin, 1975] when treatment level $a$ is applied.
''',[9],'Section 2.1 — potential outcome',symbols=[r'Y^a'],shape='Potential outcome indexed by continuous treatment; not automatically equal to the observed outcome.')
add('D6','causal estimand',r'''
Then the causal estimand that we are interested in learning about (developing a hypothesis test for) is $\theta_0(a):=\mathbb E(Y^a)$, and we wish to test if this function is constant. Specifically, we want to test
\[
H_0:\theta_0\equiv c\in\mathbb R\quad\text{versus}\quad H_1:\theta_0\text{ is nonconstant},\tag{2.1}
\]
where we will assume that $\theta_0(\cdot)$ satisfies some smoothness assumptions if it is nonconstant.
''',[9],'Section 2.1 — causal estimand and hypotheses (2.1)',{'D5':'The estimand averages the potential outcome at each treatment level.'},symbols=[r'\theta_0(a):=\mathbb E(Y^a)',r'H_0'],shape='Constant average potential-outcome curve versus a nonconstant curve. Theorem 3.1 cites (M.4), while this main-text formula is (2.1); do not substitute an appendix definition.')
add('D7','doubly robust mapping',r'''
In Kennedy et al. [2017], the authors derived a doubly robust mapping for estimating the continuous treatment effect curve. Like doubly robust estimators in binary treatment cases, the doubly robust mapping depends on both the outcome regression function and the propensity score function, and can be written as
\[
\xi(\boldsymbol Z;\pi,\mu)=\frac{Y-\mu(\boldsymbol L,A)}{\pi(A|\boldsymbol L)}\int_{\mathcal L}\pi(A|\boldsymbol l)\,dP(\boldsymbol l)+\int_{\mathcal L}\mu(\boldsymbol l,A)\,dP(\boldsymbol l).\tag{2.2}
\]
where $\pi(a|\boldsymbol l)$ and $\mu(\boldsymbol l,a)$ are some propensity score and outcome regression functions, respectively.
''',[10],'Section 2.2 — doubly robust mapping (2.2)',{'D2':'The mapping uses a candidate outcome regression function.','D3':'The mapping uses a candidate conditional treatment density and its covariate average.','D1':'The covariate integrals use the marginal law of the observed covariate vector.'},symbols=[r'\xi(\boldsymbol Z;\pi,\mu)'],shape='Population pseudo-outcome mapping with generic nuisance inputs; its algebraic definition does not require the double-robustness identification assumptions.')
add('D8','pseudo-outcome',r'''
Since we do not actually know $\mu_0,\pi_0$, we plug in estimators $\widehat\mu,\widehat\pi$ for $\mu_0,\pi_0$. To compute $\xi$ we also need to know $dP(\boldsymbol l)$ in two places; since we do not, we plug in $\mathbb P_n(\boldsymbol l)$ for $P(\boldsymbol l)$, and we denote this by $\widehat\xi$. Thus, our estimate of the pseudo-outcome $\xi(\boldsymbol Z;\pi_0,\mu_0)$ is
\[
\widehat\xi(\boldsymbol Z;\widehat\pi,\widehat\mu)=\frac{Y-\widehat\mu(\boldsymbol L,A)}{\widehat\pi(A|\boldsymbol L)}\int_{\mathcal L}\widehat\pi(A|\boldsymbol l)\,d\mathbb P_n(\boldsymbol l)+\int_{\mathcal L}\widehat\mu(\boldsymbol l,A)\,d\mathbb P_n(\boldsymbol l).\tag{2.4}
\]
''',[10],'Section 2.2 — estimated pseudo-outcome (2.4)',{'D7':'This is the plug-in version of the population mapping.','D4':'Both covariate integrals use the empirical distribution.'},symbols=[r'\widehat\xi(\boldsymbol Z;\widehat\pi,\widehat\mu)'],shape='Same-sample nuisance estimates and empirical covariate integration. The formula itself contains no sample splitting or cross-fitting.')
add('D9','local linear estimator',r'''
To define the local linear estimator, we let $\widehat\beta_h(a)=\operatorname{argmin}_{\beta\in\mathbb R^2}\mathbb P_n\left[K_{ha}(A)\{\widehat\xi(\boldsymbol Z;\widehat\pi,\widehat\mu)-g_{ha}(A)^T\beta\}^2\right]$, where $g_{ha}(t)=(1,\frac{t-a}{h})^T$, $K_{ha}(t)=h^{-1}K\{(t-a)/h\}$, and $K(\cdot)$ is a kernel function, and then we let $\widehat\theta_h(a)=g_{h,0}(0)^T\widehat\beta_h(a)$.
''',[11],'Section 2.2 — local linear estimator',{'D8':'The response in the local least-squares fit is the estimated pseudo-outcome.','D4':'The objective is an empirical average over the same sample.'},symbols=[r'\widehat\theta_h(a)',r'K_{ha}(t)=h^{-1}K\{(t-a)/h\}'],shape='Local weighted linear least squares with two regressors. Kernel regularity is a separate assumption; no minimizer uniqueness or tie convention is supplied here.')
add('D10','statistic',r'''
We propose to test our hypothesis (M.4) of a constant treatment effect curve (i.e., no treatment effect) using the following statistic
\[
T_n=n\sqrt h\int_{\mathcal A}\left(\widehat\theta_h(a)-\mathbb P_n\widehat\xi(\boldsymbol Z)\right)^2w(a)\,da,\tag{2.5}
\]
where $w(\cdot)$ is a user-specified weight function, $\widehat\theta_h(a)$ is the local linear estimator applied to $\{(\widehat\xi(\boldsymbol Z_i;\widehat\pi,\widehat\mu),A_i)\}_{i=1}^n$.
''',[11],'Section 2.2 — test statistic (2.5)',{'D9':'The integrated deviation uses the fitted local linear curve.','D8':'The centering is the sample mean of estimated pseudo-outcomes.','D4':'The centering functional is the empirical distribution.','D1':'The Lebesgue integral is over the treatment support.'},symbols=[r'T_n=n\sqrt h'],shape='Integrated squared deviation from the fitted constant, scaled by n sqrt(h). The source references (J.1) in later statements; retain that discrepancy. Smoothness of w is theorem-bound, and nonnegativity is not added.')
add('D11','Consistency',r'''
1. Consistency: $A=a$ implies $Y=Y^a$.
''',[13],'Assumption I.1',{'D5':'Consistency links the potential outcome to the observed outcome at the received treatment.','D1':'A and Y are components of an observed triple.'},kind='assumption',phrases=['Consistency'],shape='Observed outcome equals the potential outcome at the actual treatment; not an estimator consistency statement.')
add('D12','Positivity',r'''
2. Positivity: $\pi_0(a|\boldsymbol l)\ge\pi_{\min}>0$ for all $\boldsymbol l\in\mathcal L$ and all $a\in\mathcal A$.
''',[13],'Assumption I.2',{'D3':'Positivity is a uniform lower bound on the conditional treatment density.'},kind='assumption',symbols=[r'\pi_{\min}>0'],shape='Common strictly positive lower bound for all covariates and treatment levels in the stated supports.')
add('D13','Ignorability',r'''
3. Ignorability: $\mathbb E(Y^a|\boldsymbol L,A)=\mathbb E(Y^a|\boldsymbol L)$.
''',[13],'Assumption I.3',{'D5':'The conditional mean concerns a potential outcome.','D1':'The conditioning variables are the observed covariates and treatment.'},kind='assumption',phrases=['Ignorability'],shape='Mean ignorability only; do not replace by full conditional independence.')
add('D14','support',r'''
1. The support of $A$ (i.e., $\mathcal A$), is a compact subset of $\mathbb R$.
''',[13],'Assumption D.1',{'D1':'The assumption restricts the support of the observed treatment.'},kind='assumption',phrases=['compact subset'],shape='Compact treatment support. No interval, connectedness or differentiable-boundary assumption is added.')
add('D15','twice continuously differentiable',r'''
2. The treatment effect curve $\theta_0(a)$ and the marginal density function $\varpi_0(a)$ are twice continuously differentiable.
''',[13],'Assumption D.2',{'D6':'The smooth curve is the causal estimand.','D3':'The other smooth function is the marginal treatment density.'},kind='assumption',phrases=['twice continuously differentiable'],shape='Twice continuous differentiability of both named treatment-level functions.')
add('D16','uniformly bounded',r'''
3. The conditional density $\pi_0(a|\boldsymbol l)$ and the outcome regression function $\mu_0(\boldsymbol l,a)$ are uniformly bounded.
''',[13],'Assumption D.3',{'D3':'The bounded density is the true conditional treatment density.','D2':'The bounded regression is the true conditional outcome mean.'},kind='assumption',phrases=['uniformly bounded'],shape='Uniform boundedness of both true nuisance functions; not of Y itself.')
add('D17','conditional variance',r'''
4. Let $\tau(\boldsymbol l,a):=\operatorname{Var}(Y|\boldsymbol L=\boldsymbol l,A=a)$ be the conditional variance of $Y$ given covariates and treatment level. Assume there exist $\tau_{\max}>0$ such that $0<\tau(\boldsymbol l,a)\le\tau_{\max}$ for all $\boldsymbol l\in\mathcal L$ and $a\in\mathcal A$. Moreover, define
\[
S_\tau:=\{\boldsymbol l\in\mathcal L:\tau(\boldsymbol l,a)\text{ is a continuous function of }a\},
\]
\[
S_{\pi_0}:=\{\boldsymbol l\in\mathcal L:\pi_0(a|\boldsymbol l)\text{ is a continuous function of }a\},
\]
\[
S_{\mu_0}:=\{\boldsymbol l\in\mathcal L:\mu_0(\boldsymbol l,a)\text{ is a continuous function of }a\};
\]
assume we have $P(S_\tau\cup S_\pi\cup S_\mu)=1$.
''',[13],'Assumption D.4',{'D1':'The variance conditions are under the observed joint law.','D3':'The continuity sets include the true conditional treatment density.','D2':'The continuity sets also include the outcome regression.'},kind='assumption',symbols=[r'\tau(\boldsymbol l,a)',r'P(S_\tau\cup S_\pi\cup S_\mu)=1'],shape='Pointwise positive conditional variance with a uniform upper bound, and the printed union-of-continuity-sets condition. Preserve union and missing zero subscripts; do not strengthen them to an intersection or uniform lower variance bound.')
add('D18','uniform entropy integral',r'''
For a generic class of functions $\mathcal F$, let $F$ denote an envelope function for $\mathcal F$, i.e., $\sup_{f\in\mathcal F}|f|\le F$. Let $N(\varepsilon,\mathcal F,\|\cdot\|)$ denote the covering number, i.e., the minimal number of $\varepsilon$-balls (with distance defined on $\|\cdot\|$) needed to cover $\mathcal F$. Let
\[
J_m(\delta,\mathcal F,L_2):=\int_0^\delta\sup_Q(1+\log N(\varepsilon\|F\|_{Q,2},\mathcal F,L_2(Q)))^{m/2}\,d\varepsilon,\tag{2.7}
\]
where the sup is over all probability measures $Q$ and $L_2(Q)\equiv\|\cdot\|_{2,Q}$ is the $L_2$ semimetric under the distribution $Q$, i.e., $\|f\|_{2,Q}=(\int f^2\,dQ)^{1/2}$. If $J_1(1,\mathcal F,L_2)<\infty$ we say $\mathcal F$ has a finite uniform entropy integral. We will at times require $J_m(1,\mathcal F,L_2)<\infty$ for differing values of $m\in\{1,2,3,4\}$. Following standard convention, we sometimes let $J(\cdot,\cdot,\cdot)$ refer to $J_1(\cdot,\cdot,\cdot)$.
''',[13,14],'Section 2.3 — entropy integral (2.7)',symbols=[r'J_m(\delta,\mathcal F,L_2)',r'J_4(1,\mathcal F,L_2)'],shape='Uniform entropy integral with exponent m/2 and supremum over all probability measures Q inside the integral. This is not restricted to finitely supported Q.')
add('D19','Vapnik-Chervonenkis',r'''
For the assumption on our kernel, we also need to define a Vapnik-Chervonenkis (VC) (Dudley, 1999) class. If a class of functions $\mathcal F$ is a VC class, we have that
\[
\sup_Q N(\tau\|F\|_{2,Q},\mathcal F,L_2(Q))\le\left(\frac C\tau\right)^v\tag{2.8}
\]
for some positive $C,v$ and all $\tau>0$ (and again the sup is over all probability measures $Q$).
''',[14],'Section 2.3 — VC covering bound (2.8)',{'D18':'The covering bound uses the envelope-normalized covering number and L2 semimetric.'},kind='condition',symbols=[r'\left(\frac C\tau\right)^v'],shape='Preserve the actual covering-number inequality invoked by E(A).3, including the printed all-tau-positive range. Do not silently replace it with a combinatorial VC definition or restrict the range.')
add('D20','bandwidth',r'''
1. The bandwidth $h\equiv h_n$ fulfills $c_1^h n^{-1/5}\le\liminf h_n\le\limsup h_n\le c_2^h n^{-1/5}$ for some constants $0<c_1^h\le c_2^h<\infty$.
''',[14],'Assumption E(A).1',kind='assumption',symbols=[r'c_1^h n^{-1/5}\le\liminf h_n'],shape='The printed bound uses unnormalized liminf and limsup; retain the source expression rather than silently replacing it with h_n asymptotic to n^(-1/5).')
add('D21','limits of the estimators',r'''
2. Let $\bar\pi$ and $\bar\mu$ denote the limits of the estimators $\widehat\pi$ and $\widehat\mu$ such that $\|\widehat\pi-\bar\pi\|_{\mathcal Z}=o_p(\sqrt h)$ and $\|\widehat\mu-\bar\mu\|_{\mathcal Z}=o_p(\sqrt h)$, where $h$ is the bandwidth used in local linear estimator. And we have either $\bar\pi=\pi_0$ or $\bar\mu=\mu_0$.
''',[14],'Assumption E(A).2',{'D2':'One possible correct limit is the true outcome regression.','D3':'The alternative correct limit is the true conditional density.','D4':'The errors use the source uniform norm over the joint support.'},kind='assumption',symbols=[r'\|\widehat\pi-\bar\pi\|_{\mathcal Z}',r'\bar\pi=\pi_0'],shape='Both estimators converge uniformly to limits at little-o sqrt(h); at least one limit is correct. Do not require both nuisance models to be correctly specified.')
add('D22','kernel function',r'''
3. The kernel function $K$ for the local linear estimator is a continuous symmetric probability density function with support on $[-1,1]$. Moreover, we assume the class of functions $\{K((\cdot-a)/h):a\in\mathbb R,h>0\}$ satisfies condition (2.8).
''',[14],'Assumption E(A).3',{'D19':'The translated and scaled kernel class must satisfy the source covering bound (2.8).'},kind='assumption',symbols=[r'\{K((\cdot-a)/h):a\in\mathbb R,h>0\}'],shape='Kernel regularity and VC-type covering condition; separate from the definition of a local linear fit and from any particular Epanechnikov kernel used in simulations.')
add('D23','convergence rates',r'''
4. Let $r_n^\infty$ and $s_n^\infty$ be such that
\[
\sup_{a\in\mathcal A}\|\widehat\pi(a|\boldsymbol L)-\pi_0(a|\boldsymbol L)\|_2=O_p(r_n^\infty)
\]
\[
\sup_{a\in\mathcal A}\|\widehat\mu(\boldsymbol L,a)-\mu_0(\boldsymbol L,a)\|_2=O_p(s_n^\infty).
\]
We assume $s_n^\infty r_n^\infty=o\{(n\sqrt h)^{-1/2}\}$.
''',[14],'Assumption E(A).4',{'D2':'The regression error is measured relative to the true mean.','D3':'The density error is measured relative to the true conditional density.','D4':'The L2 norm integrates over the observed covariate law, and the outer supremum ranges over treatment levels.'},kind='assumption',symbols=[r's_n^\infty r_n^\infty=o\{(n\sqrt h)^{-1/2}\}'],context='under some assumptions about complexity and boundedness conditions of $\widehat\mu$ and $\widehat\pi$ and the product of their convergence rates,',context_pages=[10],shape='Mixed uniform-in-treatment and L2-in-covariates errors about the truth, with a little-o product-rate condition; distinct from uniform convergence to possibly misspecified limits.')
add('D24','Estimator assumption part B',r'''
The estimators $\widehat\pi,\widehat\mu$ and their limits $\bar\pi,\bar\mu$ are contained in uniformly bounded function classes $\mathcal F_\pi,\mathcal F_\mu$, which satisfy that $J_m(1,\mathcal F,L_2)<\infty$ for $\mathcal F=\mathcal F_\pi$ or $\mathcal F=\mathcal F_\mu$, with $1/\widehat\pi$ also uniformly bounded. Moreover, we assume $P(S_{\bar\pi}\cup S_{\bar\mu})=1$, where we let
\[
S_{\bar\pi}:=\{\boldsymbol l\in\mathcal L:\bar\pi(a|\boldsymbol l)\text{ is a continuous function of }a\}
\]
\[
S_{\bar\mu}:=\{\boldsymbol l\in\mathcal L:\bar\mu(\boldsymbol l,a)\text{ is a continuous function of }a\}.
\]
''',[15,16],'Assumption E(B)m',{'D21':'The function classes contain the estimators and the limits defined in E(A).2.','D18':'The assumption requires finiteness of the mth uniform entropy integral.'},kind='assumption',symbols=[r'J_m(1,\mathcal F,L_2)',r'P(S_{\bar\pi}\cup S_{\bar\mu})=1'],context="In addition to the above E(A) (‘Estimator assumption part A’) assumption, we make one more assumption (‘Estimator assumption part B’).",context_pages=[15],shape='m-indexed nuisance complexity assumption. Preserve the printed or and union. Theorem 3.1 uses m=3; Theorem 3.2 does not invoke E(B); Theorem 3.4 explicitly adds J4 for both classes.')
add('D25','Dudley metric',r'''
To metrize weak convergence, we use the Dudley metric [Chapter 14, Section 2, Shorack, 2000] (although any topologically equivalent metric would work), which is defined as
\[
d(\mu,\nu):=\sup\left\{\int g\,d\mu-\int g\,d\nu:\|g\|_{BL}\le1\right\},\tag{3.1}
\]
where $X$ and $Y$ are random variables with probability distributions/laws $\mu$ and $\nu$, respectively, and where $\|g\|_{BL}:=\sup_{x\in\mathbb R}|g(x)|+\sup_{x\ne y}|g(x)-g(y)|/|x-y|$.
''',[16],'Section 3 — Dudley metric (3.1)',symbols=[r'd(\mu,\nu)',r'\|g\|_{BL}'],shape='Bounded-Lipschitz metric with the sum norm convention on real-valued laws. The approximating normal law may depend on n.')
add('D26','convolution product',r'''
For a kernel function $K$, we use $K^{(s)}$ to denote the $s$-times convolution product of $K$, that is $K^{(s)}(x)=\int K^{(s-1)}(y)K(x-y)\,dy$, with $K^{(1)}=K$. And we let $K_h^{(s)}(x):=K^{(s)}(x/h)$.
''',[16,17],'Section 3 — repeated kernel convolution',symbols=[r'K^{(s)}',r'K_h^{(s)}(x):=K^{(s)}(x/h)'],shape='Repeated convolution, not pointwise powers. The scaled convolution here has no 1/h prefactor, unlike the local-linear kernel K_ha.')
add('D27','limit distribution',r'''
Let
\[
\sigma^2(a)=\mathbb E\left[\frac{\tau(\boldsymbol L,a)+\{\mu_0(\boldsymbol L,a)-\bar\mu(\boldsymbol L,a)\}^2}{\{\bar\pi(a|\boldsymbol L)/\bar\varpi(a)\}^2/\{\pi_0(a|\boldsymbol L)/\varpi_0(a)\}}\right]-\{\theta_0(a)-\bar m(a))\}^2,\tag{3.2}
\]
where $\bar\varpi(a):=\int\bar\pi(a|\boldsymbol l)\,dP(\boldsymbol l)$ and $\bar m(a):=\int\bar\mu(\boldsymbol l,a)\,dP(\boldsymbol l)$. We can now state our main theorem, which gives the limit distribution of our test statistic under the null hypothesis.
''',[17],'Section 3 — function (3.2) preceding the limit distribution',{'D17':'Formula (3.2) uses the conditional variance tau from D.4; the definition of tau is distinct from the regularity restrictions also recorded in that assumption.','D2':'The numerator includes the true outcome regression.','D3':'The denominator uses the true conditional and marginal treatment densities.','D21':'Barred nuisance functions are the estimator limits, with their covariate averages defined in this passage.','D6':'The subtracted square uses the causal effect curve.'},symbols=[r'\sigma^2(a)',r'\bar\varpi(a)',r'\bar m(a)'],shape='Source keyword indexes the original preparatory function for the limit distribution, not a renamed variance definition. Preserve the extra closing parenthesis in (3.2). Mean b_0h and variance V are bound by Theorem 3.1 itself; b_h in bootstrap theorems is not separately defined in admitted main text.')
add('D28','conditional law',r'''
Let $\mathcal L^*(X):=\mathcal L(X|\boldsymbol Z_1,\ldots \boldsymbol Z_n)$ denote the conditional law of a random variable $X$.
''',[20],'Section 3 — conditional bootstrap law',{'D1':'The conditional law fixes the full original sample.'},symbols=[r'\mathcal L^*(X)'],shape='Distribution conditional on the data, distinct from the unconditional probability law. Convergence in probability is over original data.')
add('D29','bootstrap observations',r'''
For the following theorem, we let $\widehat\varepsilon_i:=\widehat\xi(\boldsymbol Z_i;\widehat\pi,\widehat\mu)-\sum_{i=1}^n\widehat\xi(\boldsymbol Z_i;\widehat\pi,\widehat\mu)/n$ be centered at the null estimate, and we take $\varepsilon_i^*$ to be the Rademacher choice so equal to $\pm\widehat\varepsilon_i$ with probability $1/2$ each. Then we proceed as discussed in Subsection 2.2, with $(\xi_i^*=\mathbb P_n\widehat\xi+\varepsilon_i^*,A_i)$ as bootstrap observations and defining $T_n^*$ by (J.1) but using the bootstrap observations.
''',[20],'Before Theorem 3.3 — null-centered Rademacher bootstrap',{'D8':'The residual uses estimated pseudo-outcomes.','D4':'Residuals are centered at their sample mean.','D10':'The source applies the test-statistic functional to bootstrap observations while keeping A_i fixed; the appendix-labelled formula reference remains preserved.'},symbols=[r'\xi_i^*=\mathbb P_n\widehat\xi+\varepsilon_i^*',r'\pm\widehat\varepsilon_i'],shape='Null-centered Rademacher residual bootstrap in Theorem 3.3. Not the Mammen two-point option or smoother-centered variant.')
add('D30','bootstrap',r'''
Next we consider the bootstrap where $\widehat\varepsilon_i:=\widehat\xi(\boldsymbol Z_i;\widehat\pi,\widehat\mu)-\widehat\theta_h(A_i)$ (and the rest of the procedure is as described in the paragraph preceding the previous theorem). We study this case in the next theorem, which requires an extra entropy condition ($J_4<\infty$).
''',[21],'Before Theorem 3.4 — smoother-centered Rademacher bootstrap',{'D9':'The residual subtracts the fitted local linear curve at A_i.','D8':'The residual response is the estimated pseudo-outcome.','D4':'The resampled outcomes remain centered at the original sample mean.','D10':'The same integrated statistic is evaluated on bootstrap observations.'},symbols=[r'\widehat\xi(\boldsymbol Z_i;\widehat\pi,\widehat\mu)-\widehat\theta_h(A_i)'],shape='Smoother-centered residuals replace the preceding null-centered residuals. Rademacher signs and bootstrap response centering are retained from page 20; the replaced null-residual definition is not a prerequisite. J4 is an explicit separate theorem hypothesis.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages; full census review remains pending.')
if __name__=='__main__':main()
