"""Preserve original interaction models, assumptions and estimator definitions."""
import json,hashlib
from save_inventory import ROOT,PID,STATEMENTS
REVIEW_ROOT=ROOT
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
add(1,'2-order interaction model',r'''Here, $\epsilon_i$'s are assumed to be centered error independent of $X$ and the functions $f_{0,J}:\mathbb R^{|J|}\mapsto\mathbb R$. For simplicity of exposition, we henceforth confine ourselves to a 2-order interaction model. The extension of our analysis from a 2-order interaction model to a general $k$-order interaction model is purely technical and the proof ideas will be outlined at the end of the relevant sections. For $k=2$, the the model presented in equation (2.1) simplifies to:
\[
Y_i=\sum_{j=1}^df_{0,j}(X_{i,j})+\sum_{j<k}f_{0,jk}(X_{i,j},X_{i,k})+\epsilon_i\equiv f_0(X_i)+\varepsilon_i.\tag{2.2}
\]
where $f'_{0,j}$s are univariate functions and $f_{0,jk}$'s are bivariate functions.''',[4],[],[r'f_0(X_i)',r'f_{0,jk}'],'Original two-way model and centered error independent of X. Preserve the typographic prime/plural in f component prose; it is not a derivative condition. Independence across observations is not explicitly specified here.','Section 2 — Model (2.2)',kind='source_passage')
add(2,'ASSUMPTION 2.1',r'''$X$ is supported on $[0,1]^d$ and admits a density function $p$ such that $\sup_{x\in[0,1]^d}p(x)=:p_{\max}<\infty$, where $p_{\max}$ is free of $d$. We assume $\epsilon$ is sub-gaussian with sub-gaussian constant $\sigma_\epsilon^2$.''',[4],[],[r'p_{\max}',r'\sigma_\epsilon^2'],'Joint density upper bound uniform in dimension; no lower bound or coordinate independence. Sub-Gaussian constant convention is not defined in the main text.','Assumption 2.1',kind='assumption',context='ASSUMPTION 2.1.',phrases=['Assumption 2.1'])
add(3,'Identifiability and boundedness',r'''We assume the following conditions for identifiability purpose and boundedness:

1. All the univariate functions in (2.2) integrates to $0$, i.e. $\int_0^1f_{0,j}(x)\,dx=0$ for $1\le j\le d$.
2. All the bivariate functions have $0$ marginals, i.e.
\[
\int_0^1f_{0,ij}(x,y)\,dx=\int_0^1f_{0,ij}(x,y)\,dy=0.
\]
3. $\|f_0\|_\infty\le B$ for some $B>0$, where $f_0$ is defined in (2.2).''',[5],[1],[r'\int_0^1f_{0,ij}(x,y)\,dx',r'\|f_0\|_\infty\le B'],'All three original clauses; marginal centering is with respect to Lebesgue measure, not P_X or conditional means. The bound is on the total mean, distinct from component bound(3.6).','Assumption 2.2 (Identifiability and boundedness)',kind='assumption',context='ASSUMPTION 2.2 (Identifiability and boundedness).',phrases=['Assumption 2.2'])
add(4,'Holder',r'''The functions $\{f_{0,j}\}$ and $\{f_{0,ij}\}$ are assumed to be $(\beta,L)$-Holder smooth, i.e. the functions are $\lfloor\beta\rfloor$ times differentiable and $\lfloor\beta\rfloor$th derivative are Holder with exponent $\beta-\lfloor\beta\rfloor$ and constant $L$.''',[5],[1],[r'(\beta,L)',r'\beta-\lfloor\beta\rfloor'],'Original smoothness convention. The paper later assigns beta1 to univariate and beta2 to bivariate components and calls the class Sigma(beta,L). Preserve integer-beta ambiguity and the lack of explicit lower-derivative bounds.','Assumption 2.3',kind='assumption',phrases=['Assumption 2.3'])
add(5,'neural networks',r'''For a neural network, we denote by $L$ the number of hidden layers (termed as depth) and by $N$, the maximum number of neurons at the hidden layers (denoted by width). Henceforth, we denote by $\mathcal F_{NN}(d,N,L,W,o)$ by the collection of all neural networks with depth $L$, width $N$, the total number of active (non-zero) weights $W$, input dimension $d$ and output dimension $o$. We may sometimes omit the input and output dimensions in the specification of the class of neural networks when it is clear from the context.''',[6],[],[r'\mathcal F_{NN}(d,N,L,W,o)'],'Original architecture class, with hidden-layer depth, maximum width, active weights and dimensions. ReLU is identified in main-text context on10 and20; bias counting, exact versus upper-bound architecture and integer rounding are not explicitly defined.','Section 2 — Neural-network class')
add(6,'specially structured neural networks',r'''\[
\mathcal F^1_{NN}=\mathcal F_{NN}\left(d,c_1dN_1\log N_1,c_2L_1\log L_1,c_3d(N_1\log N_1)^2L_1\log L_1,1\right)\tag{2.4}
\]
\[
\mathcal F^2_{NN}=\mathcal F_{NN}\left(d,c_1d^2N_2\log N_2,c_2L_2\log L_2,c_3d^2(N_2\log N_2)^2L_2\log L_2,1\right)\tag{2.5}
\]
for some constants $c_1,c_2,c_3$. For example, in $\mathcal F^2_{NN}$, all pairwise interactions are used as input variables. Note that we are not using a fully connected neural network here. Rather, we estimate each univariate (resp. bivariate) component function via fully-connected neural networks of width $N_1\log N_1$ (resp. $N_2\log N_2$) and depth $L_1\log L_1$ (resp. $L_2\log L_2$) and then add them. See Figure 2 for an illustration. With slight abuse of notation, we still use $\mathcal F^1_{NN}$ and $\mathcal F^2_{NN}$ to denote these specially structured neural networks. The quantities $N_i$ and $L_i$ typically depend on the sample size $n$ and will be specified later.''',[7],[5],[r'\mathcal F^1_{NN}',r'\mathcal F^2_{NN}'],'Original architecture pair, including the structural restriction from prose. Theorem2.7 uses this depth-dependent version, not the revised constant-depth one.','Section 2 — Structured networks (2.4)–(2.5)')
add(7,'constant depth',r'''Therefore, we work with the neural network with constant depth and optimize over width. So, $\mathcal F^1_{NN}$ and $\mathcal F^2_{NN}$ (equation (2.4) and (2.5)) can be revised as:
\[
\mathcal F^1_{NN}=\mathcal F_{NN}\left(d,c_1dN_1\log N_1,c_2,c_3d(N_1\log N_1)^2,1\right),\tag{2.7}
\]
\[
\mathcal F^2_{NN}=\mathcal F_{NN}\left(d,c_1\binom d2N_2\log N_2,c_2,c_3\binom d2(N_2\log N_2)^2,1\right).\tag{2.8}
\]''',[10],[5],[r'\mathcal F^1_{NN}',r'\mathcal F^2_{NN}'],'Revised constant-depth architecture pair in Section2.2, retaining the source structured sum convention from7. It is not substituted into the earlier approximation theorem. The generic class is a prerequisite; earlier numerical depth formulas are not.','Section 2.2 — Revised networks (2.7)–(2.8)')
add(8,'ERM estimator',r'''We select two neural networks $(\widehat\phi_1,\widehat\phi_2)$ via minimizing the squared-error loss:
\[
(\widehat\phi_1,\widehat\phi_2)=\operatorname{argmin}_{\phi_1\in\mathcal F^1_{NN},\phi_2\in\mathcal F^2_{NN}}\frac1n\sum_{i=1}^n(Y_i-\phi_1(X_i)-\phi_2(X_i))^2\tag{2.3}
\]
and set estimate $\widehat f_{\mathrm{big}}:=\widehat\phi_1+\widehat\phi_2$. Finally set the estimator $\widehat f:=\operatorname{sgn}(\widehat f_{\mathrm{big}})(|\widehat f_{\mathrm{big}}|\wedge B)$, i.e. truncate the output of $\widehat f$ at $[-B,B]$ as we assume $\|f_0\|_\infty\le B$ (see point 3 of Assumption 2.2).''',[7],[3,7],[r'\widehat f_{\mathrm{big}}',r'\operatorname{sgn}(\widehat f_{\mathrm{big}})'],'Full global least-squares estimator plus output clipping. For Theorem2.9 the same Eq2.3 definition is instantiated with the revised classes from10. A gradient-descent estimator is not asserted equivalent; minimizer existence/selection remains unstated.','Section 2 — Estimator (2.3), as used in Section 2.2',context='the ERM estimator $\widehat f$ of $f_0$ defined in equation (2.3)',context_page=11)
add(9,'ASSUMPTION 2.6',r'''We assume that $d$ is growing with $n$ and
\[
\left(dn^{-\frac{2\beta_1}{2\beta_1+1}}+\binom d2n^{-\frac{\beta_2}{\beta_2+1}}\right)\log^{4.5}n=o(1).
\]''',[9],[4],[r'\log^{4.5}n=o(1)'],'Original dimension-growth condition with separate smoothness indices and full logarithmic factor. Section2.1 adopts it before2.7 and Section2.3 repeats it before2.12, despite its omission from those theorem bodies.','Assumption 2.6',kind='assumption',context='ASSUMPTION 2.6.',phrases=['Assumption 2.6'])
add(10,'training sample',r'''$\mathbf S_n:=\{(X_i,Y_i),i\in[n]\}$ be the training sample.''',[10],[1],[r'\mathbf S_n'],'Original training-sample notation for conditional prediction error. The source does not expressly specify iid sampling or fresh-test independence in this defining clause.','Section 2.2 — Training sample')
add(11,'minimax risk',r'''For our estimation problem, the minimax risk is defined as:
\[
\mathfrak M(n,d,\mathcal F)=\inf_{\widehat f}\sup_{\substack{f\in\mathcal F\\X\sim P_X}}\mathbb E_f\left[\left(\widehat f(X)-f(X)\right)^2\right]
\]
Here $f(X)=\sum_{j=1}^df_j(X_j)+\sum_{i<j}f_{ij}(X_i,X_j)$ and the supremum is taken over all $\{f_j\}$ and $\{f_{ij}\}$ where the component functions belongs $\Sigma(\beta,L)$ (see Assumption 2.3).''',[12],[1,4],[r'\mathfrak M(n,d,\mathcal F)',r'\Sigma(\beta,L)'],'Original expected minimax risk and function class. The source writes X~P_X beneath the supremum without specifying the design-law family or exact expectation convention. Do not identify it with the expectation-free3.9 formula.','Section 2.3 — Minimax risk')
add(12,'two-way sparse additive model',r'''The two-way sparse additive model is defined as follows:
\[
Y_i=\sum_{j\in S_1}f_{0,j}(X_{ij})+\sum_{(k,l)\in S_2}f_{0,kl}(X_{ik},X_{il})+\varepsilon_i\equiv f_0(X_i)+\varepsilon_i,\tag{3.1}
\]
where $S_1\subset[d]$, $S_2\subset[d]\times[d]$ with $S_1,S_2$ sparse, i.e., $s_i:=|S_i|\ll n$ for $i=1,2$. Define this class of functions by $\mathcal F_{\mathrm{sp}}$. Here also we assume that the univariate components are $\beta_1$ smooth and the bivariate components are $\beta_2$ smooth.''',[13],[4],[r'\mathcal F_{\mathrm{sp}}',r's_i:=|S_i|'],'Original sparse mean class and cardinalities with smoothness. Preserve S2 subset of full product, even though later sums use ordered distinct pairs. Centered independent noise follows the section-wide model convention, recorded separately as ambient context.','Section 3 — Sparse model (3.1)')
add(13,'neural networks',r'''\[
\mathcal F_{NN,1}=\mathcal F_{NN}(1,c_1N_1\log N_1,c_2,c_3N_1^2\log^2N_1,1)\tag{3.2}
\]
\[
\mathcal F_{NN,2}=\mathcal F_{NN}(2,c_4N_2\log N_2,c_5,c_6N_2^2\log^2N_2,1).\tag{3.3}
\]''',[13],[5],[r'\mathcal F_{NN,1}',r'\mathcal F_{NN,2}'],'Separate univariate/bivariate component architecture classes; input dimension1 or2, not the full d-dimensional aggregate classes. These are paired source definitions, not equivalence of the component types.','Section 3 — Component networks (3.2)–(3.3)',context='we estimate univariate and bivariate components using neural networks with different architecture',context_page=14)
add(14,'best approximator',r'''From Theorem 2.9, there exists $\{\phi_j^\star\}_{j\in S_1},\{\phi_{kl}^\star\}_{(j,k)\in S_2}$, $j\in S_1,(j,k)\in S_2$, such that, $\phi_j^\star\in\mathcal F_{NN,1}$, $\phi_{jk}^\star\in\mathcal F_{NN,2}$ and
\[
\|f_{0,j}-\phi_j^\star\|_\infty\le C_1N_1^{-2\beta_1}\ \forall j\in S_1,\qquad\|f_{0,kl}-\phi_{kl}^\star\|_\infty\le C_2N_2^{-\beta_2}\ \forall(k<l)\in S_2.
\]
Finally, define
\[
\phi^\star=\sum_{j\in S_1}\phi_j^\star+\sum_{(k<l)\in S_2}\phi_{kl}^\star.\tag{3.4}
\]''',[13],[12,13],[r'\phi^\star',r'\phi_j^\star'],'Source sparse component approximants and their sum. Preserve mixed jk/kl indexing and the cited2.9 number. These are witnesses satisfying approximation bounds, not an explicit unique argmin. Inactive components needed in3.9 are not explicitly set to zero here.','Section 3 — Approximants and sum (3.4)',context='which is the best approximator of $f_0$ from the class of neural networks.',context_page=16)
add(15,'ASSUMPTION 3.1',r'''The sparsity parameters $s_1,s_2$ corresponding to the univariate components and bivariate components satisfy the following condition:
\[
s_1\left(n^{-\frac{2\beta_1}{2\beta_1+1}}\log^4n+\frac{\log d}n\right)+s_2\left(n^{-\frac{\beta_2}{\beta_2+1}}\log^4n+\frac{\log d}n\right)=o(1).
\]''',[14],[12],[r's_1',r'\log^4n'],'Original sparsity-growth condition with logarithmic factor4, different from4.5 in Assumption2.6. The analogy with2.6 does not make the sparse setting require dense growth.','Assumption 3.1',kind='assumption',context='ASSUMPTION 3.1.',phrases=['Assumption 3.1'])
add(16,'norm',r'''$\|\cdot\|_n$ is the $L_2(\mathbb P_n)$ norm''',[14],[],[r'\|\cdot\|_n'],'Original empirical L2 norm notation. It is a seminorm on functions outside the sample. Algorithm1 overloads n after splitting; no replacement of normalization is inserted into original text.','Section 3.1 — Empirical norm')
add(17,'bound',r'''Furthermore, for technical simplicity, we assume the following $l^\infty$ bound:
\[
\|f_j\|_\infty\le B,\qquad\|f_{jk}\|_\infty\le B.\tag{3.6}
\]
Consequently, for numerical stability, we truncate the component neural networks (i.e. $\phi_j,\phi_{jk}$) at level $B$.''',[14],[12],[r'\|f_j\|_\infty\le B',r'\|f_{jk}\|_\infty\le B'],'Original individual-component bound and truncation convention. This differs from the total mean bound in Assumption2.2; neither is silently substituted for the other.','Section 3.1 — Component bound (3.6)',kind='condition')
add(18,'estimator',r'''Our estimator $\widehat f=\sum_j\widehat\phi_j+\sum_{k<l}\widehat\phi_{kl}$ where components are defined as
\[
\{\widehat\phi_j\},\{\widehat\phi_{kl}\}=\operatorname{argmin}_{\substack{\phi_j\in\mathcal F_{NN,1}\\\phi_{kl}\in\mathcal F_{NN,2}}}\left[\frac1n\sum_i\left(Y_i-\sum_j\phi_j(X_{ij})-\sum_{k<l}\phi_{kl}(X_{ik},X_{il})\right)^2+\left(\lambda_{n,1}\sum_j\|\phi_j\|_n+\lambda_{n,2}\sum_{k<l}\|\phi_{kl}\|_n\right)\right]\tag{3.5}
\]
where $\mathcal F_{NN,1}$ and $\mathcal F_{NN,2}$ are defined in (3.2) and (3.3) respectively, $\|\cdot\|_n$ is the $L_2(\mathbb P_n)$ norm and $\lambda_{n,1},\lambda_{n,2}$ to be specified later.''',[14],[13,16,17],[r'\lambda_{n,1}\sum_j\|\phi_j\|_n',r'\lambda_{n,2}\sum_{k<l}\|\phi_{kl}\|_n'],'Global penalized empirical minimizer over component networks, with Section3.1 clipping convention. Lambda parameters are inputs here; their theorem-specific choices are separately recorded. This penalty is not asserted to equal an L1 penalty on final-layer weights.','Section 3.1 — Penalized estimator (3.5)')
add(19,'approximation error',r'''where $\rho_{n,1}$ (resp. $\rho_{n,2}$) is the approximation error of the univariate (resp. bivariate) components of the mean function by neural networks, bounded by (3.8)

\[
\rho_{n,1}\le C_1N_1^{-2\beta_1},\qquad\rho_{n,2}\le C_2N_2^{-\beta_2},\tag{3.8}
\]
for some constants $C_1,C_2>0$.''',[15],[12,13],[r'\rho_{n,1}',r'\rho_{n,2}'],'Original component approximation-error notation plus its main-text bound. The excerpt stops before the theorem penalty clause, retained separately. These are component errors, distinct from the aggregate squared rho_n in2.9.','Theorem 3.2 — Approximation errors and equation (3.8)',kind='theorem_excerpt')
add(20,'penalty parameters',r'''\[
\lambda_{n,1}=C_3\sqrt{\frac{V_{n,1}\log n}{n}+\frac{2\log d}{n}},\qquad\lambda_{n,2}=C_4\sqrt{\frac{V_{n,2}\log n}{n}+\frac{3\log d}{n}},\tag{3.7}
\]
with $V_{n,1}=N_1^2\log^3N_1$ and $V_{n,2}=N_2^2\log^3N_2$.''',[15],[13],[r'\lambda_{n,1}',r'\lambda_{n,2}'],'Original prescribed penalties with full radicands and component complexity formulas. Positive sufficiently large constants, architecture tuning and n after splitting are not fully quantified in the theorem.','Theorem 3.2 — Penalty choices (3.7)',kind='theorem_excerpt',context='Input: Constant $c_1,c_2$ and penalty parameters $\lambda_{n,1}$, $\lambda_{n,2}$.',context_page=18)
add(21,'restricted strong convexity',r'''There exist constants $\kappa_1,\kappa_2>0$, such that for any function $\phi=\sum_j\phi_j+\sum_{k<l}\phi_{kl}$ that satisfies:
\[
\lambda_{n,1}\sum_{j\in S_1^c}\|\phi_j-\phi_j^\star\|_n+\lambda_{n,2}\sum_{(k<l)\in S_2^c}\|\phi_{kl}-\phi_{kl}^\star\|_n
\le4(s_1\rho_{n,1}^2+s_2\rho_{n,2}^2)+3\lambda_{n,1}\sum_{j\in S_1}\|\phi_j-\phi_j^\star\|_n+3\lambda_{n,2}\sum_{(k<l)\in S_2}\|\phi_{kl}-\phi_{kl}^\star\|_n+s_1\lambda_{n,1}^2+s_2\lambda_{n,2}^2\tag{3.9}
\]
also satisfies:
\[
\kappa_1^2\sum_{j\in S_1}\|\phi_j-\phi_j^\star\|_n^2+\kappa_2^2\sum_{(k<l)\in S_2}\|\phi_{kl}-\phi_{kl}^\star\|_n^2\le\|\phi-\phi^\star\|_n^2\tag{3.10}
\]
where $\phi^\star$ is defined by (3.4), $\rho_{n,1}$ and $\rho_{n,2}$ are defined in Theorem 3.2 and $\lambda_{n,1}$ and $\lambda_{n,2}$ are defined in (3.7).''',[15],[12,14,16,19,20],[r'\kappa_1^2',r'\kappa_2^2',r'\phi-\phi^\star'],'Complete RSC condition, including the approximate cone with additive approximation and penalty terms. Preserve any-function quantifier; network membership and zero inactive approximants are not explicit in the statement. It is not the ordinary linear restricted-eigenvalue condition.','Assumption 3.4',kind='assumption',context='Assume that the restricted strong convexity assumption (Assumption 3.4)',context_page=18,phrases=['Assumption 3.4'])
add(22,'minimal signal strength',r'''Assume that all the component functions has minimal signal strength $r_n$, i.e. $\min_{j\in S_1}\|f_j^0\|_2\ge r_n$, $\min_{(j,k)\in S_2}\|f_{j,k}^0\|_2\ge r_n$ where:
\[
r_n\gtrsim\sqrt{\left(s_1\left(n^{-\frac{2\beta_1}{1+2\beta_1}}\log^4n+\frac{\log d}n\right)+s_2\left(n^{-\frac{\beta_2}{1+\beta_2}}\log^4n+\frac{\log d}n\right)\right)}.
\]''',[18],[12],[r'r_n',r'\min_{j\in S_1}\|f_j^0\|_2'],'Original unsquared component L2 signal bound and square root of the squared-error rate. Preserve superscript0 versus earlier subscript0 notation. Underlying measure and empty-active-set conventions are not specified in this assumption.','Assumption 3.7',kind='assumption',phrases=['Assumption 3.7'])
add(23,'Estimation under random design setting',r'''Input: Constant $c_1,c_2$ and penalty parameters $\lambda_{n,1}$, $\lambda_{n,2}$.

Output: $\widehat f$: the estimator based on neural network.

Data: Dataset $\{(X_1,Y_1),\ldots,(X_n,Y_n)\}$.

1. Divide the dataset into two equal halves with $n/2$ data in each set (if $n$ is odd, then take $(n+1)/2$ data in the first half and $(n-1)/2$ in the second half). Denote the halves by $\mathcal D_1$ and $\mathcal D_2$.
2. Using $\mathcal D_1$, estimate the component functions $\{\widehat\phi_j^{\mathrm{init}}\}$ and $\{\widehat\phi_{jk}^{\mathrm{init}}\}$ by solving (3.5).
3. Set $\widehat S_1=\{j:\|\widehat\phi_j^{\mathrm{init}}\|_n\ge c_1\lambda_{n,1}\}$ and $\widehat S_2=\{(j<k):\|\widehat\phi_{jk}^{\mathrm{init}}\|_n\ge c_2\lambda_{n,2}\}$.
4. Re-estimate component functions on the estimated active set $\widehat S_1$ and $\widehat S_2$ by minimizing (un-penalized) squared error loss:
\[
\{\widehat\phi_j^{\mathrm{final}}\}_{j\in\widehat S_1},\{\widehat\phi_{jk}^{\mathrm{final}}\}_{(j,k)\in\widehat S_2}=\operatorname{argmin}_{\substack{\phi_j\in\mathcal F_{NN,1}\\\phi_{j,k}\in\mathcal F_{NN,2}}}\frac1n\sum_i\left(Y_i-\sum_{j\in\widehat S_1}\phi_j(X_{ij})-\sum_{(j,k)\in\widehat S_2}\phi_{jk}(X_{ij},X_{ik})\right)^2.\tag{3.17}
\]
5. Return the final estimate $\widehat f^{\mathrm{final}}=\sum_{j\in\widehat S_1}\widehat\phi_j^{\mathrm{final}}+\sum_{(j<k)\in\widehat S_2}\widehat\phi_{jk}^{\mathrm{final}}$.''',[18],[13,16,18,20],[r'\widehat S_1',r'\widehat S_2',r'\widehat f^{\mathrm{final}}'],'Complete Algorithm1. Preceding prose on17 says the unpenalized refit uses the second half; original display leaves sum_i/n unqualified. Threshold constants refer to appendix proof and remain unspecified, not invented.','Algorithm 1: Estimation under random design setting',context='Algorithm 1: Estimation under random design setting')
add(24,'Random design setting',r'''Here, we extend our analysis to the random design model, namely when $X_i$'s are random variables with distribution satisfying Assumption 2.1.

Hence, in this setup we need to bound the expected squared error loss, i.e. $\|\widehat f-f_0\|_{L_2(P_X)}^2$ instead of empirical squared error loss, i.e. $\|\widehat f-f_0\|_n^2$.''',[17],[2],[r'\|\widehat f-f_0\|_{L_2(P_X)}^2'],'Original random-design section convention and contrast of population versus empirical loss. It does not assert the same RSC event simultaneously for every possible design.','Section 3.2 — Random design setting',kind='source_passage',context='3.2. Random design setting.')
# Numbered source headings are readable terms when the source supplies no descriptive title.
for n,label,page in [(2,'2.1',4),(9,'2.6',9),(15,'3.1',14)]:
    m=members['D'+str(n)];x=interfaces[n-1];cid=m['local_id']+'/heading'
    m['naming_context']=[dict(context_id=cid,text='ASSUMPTION '+label+'.',evidence=[dict(page=page,location='Printed assumption heading')])]
    x['source_keywords']=[dict(paper_id=PID,local_id=m['local_id'],source_text='ASSUMPTION '+label,label='Assumption '+label,kind='term',context_id=cid)];x['name']='Assumption '+label

def main():
    review=json.loads((REVIEW_ROOT/'inventory-review.json').read_text());assert review['status']=='complete' and review['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==review['inventory_sha256']
    assert len(interfaces)==len(members)==24
    for x in interfaces:
        m=x['members'][0];assert set(m['depends_on'])<=set(members)
        assert any(v in m['statement_original']+' '+m['local_label'] for v in m['highlight_symbols']+m['highlight_phrases'])
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved24 original source entries; full census review remains pending.')
if __name__=='__main__':main()
