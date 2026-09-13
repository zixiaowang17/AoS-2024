"""Reproduce the manually reviewed source extraction from Sections 2–4.

Running this script restores source passages; it does not perform a fresh
mathematical review or change the paper completion status.
"""
import json
from pathlib import Path
from save_inventory import PID,ROOT
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,description,heading=None,context=None,context_page=None,kind='definition'):
    lid=f'D{n}';heading=heading or 'Section 2 — '+term[0].upper()+term[1:]
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=[])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context for '+lid)])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='hypothesis' if kind in ['assumption','condition'] else 'definition',type_shape=description,semantic_boundary=description,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'Additive regression',r'''Additive regression assumes that the mean function $f:=E(Y|\mathbf X=\cdot)$ admits
\[
f(\mathbf x)=E(Y)+f_1(x_1)+\cdots+f_d(x_d)
\]
(2.1)
for some square integrable univariate functions $f_j$ satisfying the constraints
\[
\int_0^1 f_j(x_j)p_j(x_j)dx_j=0,\qquad1\leq j\leq d,
\]
where $\mathbf x=(x_1,\ldots,x_d)^\top$ and $p_j$ denotes the marginal density of $X_j$.''',[4],[],[r'f_j',r'p_j',r'f(\mathbf x)'],'Population conditional-mean additivity with each component centered under its own marginal density. Compact covariate support and iid sampling are standing source conventions, preserved separately.',kind='source_passage')
add(2,'space of additive functions',r'''Let $L^2$ denote the space of square integrable functions $g:[0,1]^d\to\mathbb R$, and $\mathcal H\subset L^2$ the space of additive functions $g$ of the form $g(\mathbf x)=g_1(x_1)+\cdots+g_d(x_d)$ with univariate functions $g_j$. We may embed these univariate functions $g_j$ into $\mathcal H$ by interpreting them as a function $\widetilde g_j:[0,1]^d\to\mathbb R$ such that $\widetilde g_j(\mathbf x)=g_j(x_j)$. With slight abuse of notation, we continue to write $g_j$ for these functions defined on $[0,1]^d$, instead of $\widetilde g_j$, throughout this paper. Let $\mathcal H_j$, as a subspace of $\mathcal H$, denote the space of such functions. In this way, we can write $\mathcal H=\mathcal H_1+\cdots+\mathcal H_d$.''',[4],[],[r'\mathcal H_j',r'\mathcal H',r'L^2'],'Coordinate function subspaces embedded into functions on the full cube. This is a sum space; tuple products and weighted norms remain separate conventions.')
add(3,'normalized kernel function',r'''For a baseline kernel function $K$ supported on $[-1,1]$, let $K_h(\cdot,\cdot)$ be the normalized kernel function defined by
\[
K_h(x,u):=c_h(u)\cdot\frac1h K\left(\frac{x-u}{h}\right),
\]
where $h$ is the bandwidth and $c_h(u)$ is determined so that $\int_0^1K_h(x,u)dx=1$ for all $u\in[0,1]$. We note that
\[
1\leq c_h(u)\leq2\qquad\text{for all }u\in[0,1].
\]
(2.2)
The normalized kernel weight $K_h(x,\cdot):[0,1]\to[0,\infty)$ equals the conventional one $K_h(x-\cdot)$ when $x\in[2h,1-2h]$, where $K_h(v):=h^{-1}K(v/h)$.''',[4],[],[r'K_h',r'c_h(u)'],'Boundary-normalized kernel, integrating over evaluation coordinate x at each fixed u. Positivity, kernel mass and small-bandwidth conventions behind the stated bound are source issues; (A4) is kept distinct.')
add(4,'kernel density estimator',r'''Let $\widehat p_j$ be a kernel density estimator of $p_j$ defined by
\[
\widehat p_j(x_j):=n^{-1}\sum_{i=1}^nK_{h_j}(x_j,X_{ij}).
\]
Here, the bandwidth $h_j$ are allowed to be different for different $j$. Because of the normalization property of $K_h$, the marginalization of the joint density estimator
\[
\widehat p(\mathbf x):=n^{-1}\sum_{i=1}^n\prod_{k=1}^dK_{h_k}(x_k,X_{ik})
\]
at the $j$th coordinate $x_j$ reduces to $\widehat p_j(x_j)$, that is, $\int_{[0,1]^{d-1}}\widehat p(\mathbf x)d\mathbf x_{-j}=\widehat p_j(x_j)$, where $d\mathbf x_{-j}=\prod_{k=1,\ne j}^d dx_k$.''',[4,5],[3],[r'\widehat p_j',r'\widehat p'],'The marginal and joint normalized product-kernel density estimates and their exact marginalization. Independent-coordinate covariates are not assumed.')
add(5,'smooth backfitting technique',r'''When $d$ is fixed, the smooth backfitting technique [44] for estimating the model (2.1) is to minimize
\[
L_n(\mathbf g):=\frac1{2n}\sum_{i=1}^n\int_{[0,1]^d}\left(Y_i-\overline Y-\sum_{j=1}^d g_j(x_j)\right)^2\prod_{j=1}^d K_{h_j}(x_j,X_{ij})d\mathbf x
\]
(2.3)
over tuples of univariate functions $\mathbf g=(g_1,\ldots,g_d)^\top$ subject to the constraints
\[
\int_0^1g_j(x_j)\widehat p_j(x_j)dx_j=0,\qquad1\leq j\leq d.
\]
(2.4)''',[5],[2,3,4],[r'L_n',r'\widehat p_j'],'Empirical integrated squared loss and empirical centering constraints. The fixed-d motivation is preserved; this same loss is later penalized for high dimensions.')
add(6,'marginal regression estimator',r'''Let $\widehat m_j$ be the marginal regression estimator of $E(Y|X_j=\cdot)$ defined by
\[
\widehat m_j(x_j):=\widehat p_j(x_j)^{-1}\cdot n^{-1}\sum_{i=1}^nK_{h_j}(x_j,X_{ij})Y_i,
\]
(2.5)''',[5],[3,4],[r'\widehat m_j'],'Univariate kernel regression using the boundary-normalized kernel and empirical marginal density. Zero-denominator events require a source convention.')
add(7,'two-dimensional density',r'''and $\widehat p_{jk}$ be the kernel estimator of the two-dimensional density $p_{jk}$ of $(X_j,X_k)$ defined by
\[
\widehat p_{jk}(x_j,x_k):=n^{-1}\sum_{i=1}^n K_{h_j}(x_j,X_{ij})K_{h_k}(x_k,X_{ik}).
\]''',[5],[3],[r'\widehat p_{jk}',r'p_{jk}'],'Bivariate marginal density and its product-kernel estimate, using observations with the same sample index in both factors. This is not a product of separate marginal estimates.')
add(8,'projection operator',r'''where $\widehat\pi_j:L^2\to\mathcal H_j$ is a projection operator defined by
\[
(\widehat\pi_jg)(x_j):=\int_{[0,1]^{d-1}}g(\mathbf x)\frac{\widehat p(\mathbf x)}{\widehat p_j(x_j)}d\mathbf x_{-j}.
\]
(2.7)''',[5],[2,4],[r'\widehat\pi_j'],'The source empirical conditional-expectation projection onto a coordinate function space. Its weighted-space and zero-density qualifications are retained separately.')
add(9,'norm',r'''Throughout this paper, we let the norm $\|\cdot\|_q$ for a density function $q$ on $[0,1]^d$ be defined by
\[
\|\eta\|_q^2:=\int\eta^2(\mathbf x)q(\mathbf x)d\mathbf x,\qquad\eta:[0,1]^d\to\mathbb R.
\]
We also let $\langle\cdot,\cdot\rangle_q$ be the associated inner product.''',[5],[],[r'\|\eta\|_q',r'\|\widehat f_j-f_j\|_p',r'\|\eta_j\|_{\widehat p}'],'Density-weighted L2 norm for a scalar function; tuple norms and sum-space norms are distinguished in auxiliary source context.')
add(10,'fLasso-SBF estimator',r'''We add a penalty term to the objective functional $L_n$ at (2.3):
\[
L_n^{\mathrm{pen}}(\mathbf g):=L_n(\mathbf g)+\lambda\sum_{j=1}^d\|g_j\|_{\widehat p},
\]
(2.8)
where $\lambda>0$ is a penalty parameter. It is worthwhile to note that $\|g_j\|_{\widehat p}^2=\int g_j(\mathbf x)^2\widehat p(\mathbf x)d\mathbf x=\int g_j(x_j)^2\widehat p_j(x_j)dx_j$ for $g_j\in\mathcal H_j$. We minimize $L_n^{\mathrm{pen}}(\mathbf g)$ over $\mathbf g$ to obtain the fLasso-SBF estimator, denoted by $\widehat{\mathbf f}\equiv(\widehat f_1,\ldots,\widehat f_d)$. As in the fixed $d$ case, the minimizer of $L_n^{\mathrm{pen}}$ is not given explicitly but implicitly as the solution of the following system of equations:
\[
\widehat f_j^*=\widehat m_j-\overline Y-\sum_{k=1,\ne j}^d\widehat\pi_j\widehat f_k,\qquad
\widehat f_j=\left(1-\frac\lambda{\|\widehat f_j^*\|_{\widehat p}}\right)_+\widehat f_j^*,\quad1\leq j\leq d,
\]
(2.9)
where $a_+=\max\{0,a\}$.''',[5,6],[5,9,4,6,8],[r'L_n^{\mathrm{pen}}',r'\widehat{\mathbf f}',r'\widehat f_j'],'Functional Lasso penalty and the resulting minimizer with its source threshold characterization. A zero residual norm needs an implicit zero-output convention; existence and selection of minimizers are not certified by the census.')
add(11,'integral operators',r'''For a collection of functions $\Xi_{jk}:[0,1]^d\times[0,1]^d\to\mathbb R$ for $1\leq j,k\leq d$ such that $\Xi_{jk}(\mathbf u,\mathbf x)=\widetilde\Xi_{jk}(u_j,x_k)$ for some bivariate function $\widetilde\Xi_{jk}:[0,1]\times[0,1]\to\mathbb R$, define the corresponding collection of integral operators $\Xi_{jk}:\mathcal H_k\to\mathcal H_j$ by
\[
\Xi_{jk}(g)(\mathbf u):=\int\Xi_{jk}(\mathbf u,\mathbf x)g(\mathbf x)d\mathbf x,\qquad g\in\mathcal H_k.
\]
It is important to note that the integral operators involve only one-dimensional integration and $\Xi_{jk}(g)$ is a univariate function. Here and throughout this paper, with slight abuse of notation again, we do not distinguish the integral operator and its kernel by writing $\Xi_{jk}$ for both. Also, we often write kernels $\Xi_{jk}$ as bivariate functions, that is, identify $\Xi_{jk}(u_j,x_k)$ with $\Xi_{jk}(\mathbf u,\mathbf x)$. With a collection $\{\Xi_{jk}:1\leq j,k\leq d\}$ of integral operators of such kinds and for a tuple $\mathbf g=(g_1,\ldots,g_d)^\top\in\mathcal H_1\times\cdots\times\mathcal H_d$, define $\Xi:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_1\times\cdots\times\mathcal H_d$ by
\[
\Xi(\mathbf g):=\left[\sum_{k=1}^d\Xi_{1k}(g_k),\ldots,\sum_{k=1}^d\Xi_{dk}(g_k)\right]^\top.
\]
(2.10)''',[6],[2],[r'\Xi_{jk}',r'\Xi(\mathbf g)'],'Coordinate integral kernels and their block operator acting on tuples. The source writes a cube integral but explicitly identifies it with a one-dimensional integral; boundedness conditions and kernel/operator identification remain source conventions.')
add(12,'integral operators',r'''Let $\widehat\pi_{jk}:\mathcal H_k\to\mathcal H_j$ for $k\ne j$ be the restriction of $\widehat\pi_j$ defined at (2.7) to $\mathcal H_k$. Note that their respective kernels, still denoted by $\widehat\pi_{jk}$, are given by $\widehat\pi_{jk}(\mathbf u,\mathbf x)=\widehat p_{jk}(u_j,x_k)/\widehat p_j(u_j)$. Put $\widehat\Pi_{jk}=\widehat\pi_{jk}$ for $j\ne k$ and $\widehat\Pi_{jj}\equiv0$. Let $\widehat\Pi$ and $I+\widehat\Pi$ be defined as $\Xi$ in (2.10) with the kernels $\Xi_{jk}=\widehat\Pi_{jk}$ and $\Xi_{jk}=\delta_{jk}+\widehat\Pi_{jk}$, respectively, for $1\leq j,k\leq d$, where $\delta_{jk}=0$ for $k\ne j$ and $\delta_{jj}(\mathbf u,\mathbf x)=\delta(u_j-x_j)$ with the Dirac delta $\delta$. Note that the integral operators $\delta_{jk}$ and $\widehat\Pi_{jk}$ satisfy
\[
\sum_{k=1}^d\delta_{jk}(g_k)(\mathbf u)=g_j(u_j),\qquad1\leq j\leq d,
\]
\[
\sum_{k=1}^d\widehat\Pi_{jk}(g_k)(\mathbf u)=\sum_{k=1,\ne j}^d\int_0^1g_k(x_k)\frac{\widehat p_{jk}(u_j,x_k)}{\widehat p_j(u_j)}dx_k,\qquad1\leq j\leq d.
\]
(2.11)''',[6],[8,7,4,11],[r'\widehat\Pi_{jk}',r'\widehat\Pi'],'The uncentered empirical off-diagonal operator in Section 2 and its identity extension. Keep it distinct from the centered redefinition at (3.1). The Dirac diagonal is a source distributional convention, not an ordinary bounded kernel.',heading='Section 2 — Integral operators (2.11)')
add(13,'subderivative vector',r'''Let $\nu(\widehat{\mathbf f})$ be a subderivative vector of the penalty term $\sum_j\|g_j\|_{\widehat p}$ at $\widehat{\mathbf f}$. Specifically, $\nu(\widehat{\mathbf f})=(\nu_1,\ldots,\nu_d)^\top$ where $\nu_j=\widehat f_j/\|\widehat f_j\|_{\widehat p}$ if $\|\widehat f_j\|_{\widehat p}\ne0$ and $\nu_j\in\{v_j\in\mathcal H_j:\|v_j\|_{\widehat p}\leq1\}$ otherwise. Then, the minimizer $\widehat{\mathbf f}$ of the objective functional $L_n^{\mathrm{pen}}$ at (2.8) is the solution of the equation
\[
(I+\widehat\Pi)\widehat{\mathbf f}=\widehat{\mathbf m}-\overline Y\cdot\mathbf1-\lambda\cdot\nu(\widehat{\mathbf f}).
\]
(2.13)''',[7],[10,9,12,6,2],[r'\nu(\widehat{\mathbf f})',r'\nu_j'],'The penalty subgradient evaluated at a minimizer, with a unit-ball choice at zero components and the source stationarity equation. Only a choice satisfying that equation can be used in the debiasing identity.')
add(14,'iterative algorithm',r'''Here, we present an iterative algorithm that solves (2.13) for the fLasso-SBF estimator $\widehat{\mathbf f}$. Define $\widehat\Pi_j:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_j$ by
\[
\widehat\Pi_j(\mathbf g)(\mathbf u):=\sum_{k=1}^d\widehat\Pi_{jk}(g_k)(\mathbf u)=\sum_{k=1}^d\int_0^1\widehat\Pi_{jk}(u_j,x_k)g_k(x_k)dx_k
\]
for a tuple $\mathbf g=(g_1,\ldots,g_d)^\top\in\mathcal H_1\times\cdots\times\mathcal H_d$. Then, from (2.13) it holds that $\widehat f_j+\lambda\cdot\nu_j=\widehat m_j-\overline Y-\widehat\Pi_j(\widehat{\mathbf f})$. We note that $\widehat\Pi_j(\widehat{\mathbf f})$ for each $j$ does not involve $\widehat f_j$. Let $\widehat\Pi_j^\ominus:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_j$ be defined by
\[
\widehat\Pi_j^\ominus(\mathbf g)(\mathbf u):=\widehat m_j(u_j)-\overline Y-\widehat\Pi_j(\mathbf g)(\mathbf u),\qquad\mathbf g\in\mathcal H_1\times\cdots\times\mathcal H_d.
\]''',[7],[12,6],[r'\widehat\Pi_j^\ominus',r'\widehat\Pi_j'],'The row operator and partial residual map used by the iterative algorithm. The stationarity equation is retained as motivation; the maps themselves require only the empirical operator and marginal regression, not the unknown minimizer.',heading='Section 2.2 — Iterative algorithm: row and residual maps')
add(15,'fLasso-SBF',r'''Initialize: Choose appropriate initial $\widehat{\mathbf f}^{(0)}:=(\widehat f_1^{(0)},\ldots,\widehat f_d^{(0)})^\top$.

For $r=0,1,2,\ldots$ do

$\widehat{\mathbf f}^{(r,0)}\leftarrow\widehat{\mathbf f}^{(r)}$.

For $j=1,\ldots,d$ do
\[
\widehat f_j^{(r,j)}\leftarrow\left(1-\frac\lambda{\|\widehat\Pi_j^\ominus(\widehat{\mathbf f}^{(r,j-1)})\|_{\widehat p}}\right)_+\widehat\Pi_j^\ominus(\widehat{\mathbf f}^{(r,j-1)})
\]
$f_k^{(r,j)}=f_k^{(r,j-1)}$ for $k\ne j$.

end for

$\widehat{\mathbf f}^{(r+1)}\leftarrow\widehat{\mathbf f}^{(r,d)}$

end for''',[8],[14,9,4],[r'\widehat{\mathbf f}^{(r)}',r'\widehat{\mathbf f}^{(0)}'],'Sequential coordinate sweeps using the most recently updated tuple. The source unchanged-coordinate line lacks hats; it is preserved. Initial centering and zero-residual behavior are separate source conventions.',heading='Algorithm 1 — fLasso-SBF',context='''ALGORITHM 1
fLasso-SBF''')
add(16,'index set',r'''Let $S$ be the index set of the true significant component functions $f_j$, that is,
\[
S:=\{1\leq j\leq d:\|f_j\|_p\ne0\},
\]
where $p$ is the joint density function of $\mathbf X$. We note that the dimension $d$ of $\mathbf X$ is allowed to diverge with $n$. Hence, $d$ and thus $S$ with other terms involving $d$ depend on $n$, although we suppress the dependence throughout the paper unless it pertains to the sample $\{(\mathbf X_i,Y_i):1\leq i\leq n\}$. We allow $|S|$ to diverge as $n\to\infty$, where $|A|$ for a set $A$ denotes the cardinality of $A$. The index set $S$ should be differentiated from
\[
S_n:=\{1\leq j\leq d:\|f_j\|_{\widehat p}\ne0\}.
\]
Note that $S_n=S$ if
\[
0<\min_{1\leq j\leq d}\inf_{x_j\in[0,1]}\frac{\widehat p_j(x_j)}{p_j(x_j)}\leq\max_{1\leq j\leq d}\sup_{x_j\in[0,1]}\frac{\widehat p_j(x_j)}{p_j(x_j)}<\infty.
\]''',[9],[1,9,4],[r'S_n',r'|S|',r'S:='],'True active set and the distinct empirical-norm set, with the explicitly stated sufficient density-ratio condition for equality. Sparsity and dimension may grow with sample size.')
add(17,'marginal density functions',r'''The marginal density functions $p_j$ satisfy
\[
c_{p,L}\leq\min_{1\leq j\leq d}\inf_{x_j\in[0,1]}p_j(x_j)\leq\max_{1\leq j\leq d}\sup_{x_j\in[0,1]}p_j(x_j)\leq c_{p,U}
\]
for some absolute constants $0<c_{p,L}<c_{p,U}<\infty$, and are differentiable on $[0,1]$ with derivatives $p_j'$ being bounded uniformly on $[0,1]$ and for $1\leq j\leq d$ by an absolute positive constant.''',[10],[1],[r'p_j',r'c_{p,L}',r'c_{p,U}'],'Uniform positive lower and finite upper marginal-density bounds and bounded first derivatives. Absolute means independent of sample size.',heading='Assumption (A1)',kind='assumption')
add(18,'absolute constants',r'''There exist absolute constants $0<C_p,L_p<\infty$ such that
\[
\max_{1\leq j\ne k\leq d}\sup_{x_j,x_k\in[0,1]}p_{jk}(x_j,x_k)\leq C_p,
\]
\[
\max_{1\leq j\ne k\leq d}\sup\left\{\frac{|p_{jk}(x_j,x_k)-p_{jk}(x_j',x_k')|}{|x_j'-x_j|+|x_k'-x_k|}:x_j\ne x_j'\text{ or }x_k\ne x_k'\in[0,1]\right\}\leq L_p.
\]''',[10],[],[r'p_{jk}',r'C_p',r'L_p'],'Uniform boundedness and Lipschitz restriction on population pairwise densities. Their meaning is given in the source bivariate-density passage; no dependence on its estimator is implied. The printed domain clause is preserved.',heading='Assumption (A2)',kind='assumption')
add(19,'true component functions',r'''The true component functions $f_j$ for $j\in S$ are twice differentiable on $[0,1]$. Their first and second derivatives denoted by $f_j'$ and $f_j''$, respectively, as well as themselves are bounded uniformly for $u\in[0,1]$ and $j\in S$ by some absolute positive constants.''',[10],[1,16],[r'f_j',r'j\in S'],'Uniform boundedness through second derivative for true active components, without a lower signal-strength restriction.',heading='Assumption (A3)',kind='assumption')
add(20,'baseline kernel function',r'''The baseline kernel function $K$ is nonnegative, symmetric, compactly supported on $[-1,1]$, $\int K=1$ and satisfies $\sup_{v\in[-1,1]}K(v)\leq c_K$ and $|K(u)-K(u')|\leq L_K|u-u'|$ for some absolute constants $0<c_K,L_K<\infty$.''',[10],[],[r'K',r'c_K',r'L_K'],'Nonnegative symmetric compactly supported unit-mass kernel with uniform supremum and Lipschitz constants. This condition is separate from the normalized-kernel construction.',heading='Assumption (A4)',kind='assumption')
add(21,'bandwidths',r'''The bandwidths $h_j$ satisfy $c_{h,L}h\leq h_j\leq c_{h,U}h$ for all $1\leq j\leq d$ for some absolute constants $0<c_{h,L}<c_{h,U}<\infty$, where $h=o(1)$ and $\log(d\vee n)=O(nh^2)$ as $n\to\infty$.''',[10],[],[r'h_j',r'h=o(1)',r'c_{h,L}'],'Comparable coordinate bandwidths with a vanishing reference scale and a dimension-growth bound. Further theorem-specific bandwidth restrictions remain distinct.',heading='Assumption (A5)',kind='assumption')
add(22,'subexponential random variable',r'''The error term $\epsilon:=Y-E(Y)-\sum_{j=1}^d f_j(X_j)$ is a subexponential random variable with some parameters $(\sigma^2,\alpha)$ such that $E(\exp(\upsilon\epsilon)|\mathbf X=\cdot)\leq\exp(\upsilon^2\sigma^2/2)$ a.s. for all $|\upsilon|\leq1/\alpha$''',[10],[1],[r'\epsilon',r'\sigma^2',r'|\upsilon|\leq1/\alpha'],'Conditional moment-generating-function bound only in the stated finite parameter interval; not a global sub-Gaussian assumption or a bounded response-variance assumption.',heading='Assumption (A6)',kind='assumption')
add(23,'marginalization properties',r'''Let $p^h:[0,1]^d\to[0,\infty)$ be defined by $p^h(\mathbf x):=E(\widehat p(\mathbf x))$. We note that $p^h$ also has the marginalization properties as $\widehat p$ and $p$. Namely, for example, it holds that
\[
\int_{[0,1]^{d-1}}p^h(\mathbf x)d\mathbf x_{-j}=p_j^h(x_j).
\]''',[11],[4],[r'p^h',r'p_j^h'],'Expected smoothed joint density and its marginalization. The original defining equation for p_j^h on page 10 is retained as auxiliary context; the measure is distinct from both p and the random p-hat.')
add(24,'compatibility constant',r'''For $a>0$, define
\[
\phi(a):=\inf\left\{\frac{\|\sum_{k=1}^d\eta_k\|_{p^h}^2}{\sum_{k\in S}\|\eta_k\|_{p^h}^2}:\eta_k\in\mathcal H_k,\ \sum_{k\in S^c}\|\eta_k\|_{p^h}\leq a\sum_{k\in S}\|\eta_k\|_{p^h},\ \sum_{k\in S}\|\eta_k\|_{p^h}^2\ne0,\ \int\eta_k(x_k)p_k^h(x_k)dx_k=0\text{ for }1\leq k\leq d\right\}.
\]
We note that $\phi(a)$ decreases as $a$ increases. In Proposition S.1 in the Supplementary Material we show that $\phi(a)$ defined in terms of $p^h$ can also relate the two norms in terms of $\widehat p$, $\|\sum_{k=1}^d\eta_k\|_{\widehat p}^2$ and $\sum_{k\in S}\|\eta_k\|_{\widehat p}^2$. Put
\[
\phi:=\phi(6\sqrt{c_{r,U}/c_{r,L}}),
\]
where $c_{r,L}$ and $c_{r,U}$ are the constants at (2.18). The “compatibility constant” $\phi$ depends on $n$ and $d$ as well as on the joint density $p$.''',[11],[23,9,16,2],[r'\phi(a)',r'\phi'],'Cone-restricted ratio of the squared sum norm to the active-component squared tuple norm, with p^h centering and nonzero denominator. The cr constants are retained from main-text (2.18); the supplementary proposition is not used as a theorem dependency.')

add(25,'integral operator',r'''We note that each component of $\widehat{\mathbf f}$ satisfies the constraint (2.4). Thus, $\widehat{\mathbf f}$ satisfies (2.13) with $\widehat\Pi$ being redefined with the kernels $\widetilde\pi_{jk}:[0,1]\times[0,1]^d\to\mathbb R$ such that
\[
\widetilde\pi_{jk}(\mathbf u,\mathbf x):=\widehat\pi_{jk}(\mathbf u,\mathbf x)-\widehat p_k(x_k)=\frac{\widehat p_{jk}(u_j,x_k)}{\widehat p_j(u_j)}-\widehat p_k(x_k).
\]
(3.1)
The new definition of $\widehat\Pi$ is not necessary for $\widehat{\mathbf f}$ since each of its components satisfies the constraint automatically because of the penalty term at (2.8). However, it matters for the new estimator that we introduce here. Below, we continue to use $\widehat\Pi$ to denote the new integral operator redefined with $\widetilde\pi_{jk}$.''',[13],[7,4,11],[r'\widetilde\pi_{jk}',r'\widehat\Pi'],'The centered empirical off-diagonal kernels used from Section 3 onward, with the previously defined zero diagonal retained. The formula completely specifies the kernels from empirical densities. Its explanation involving the earlier estimator does not make that estimator an input.',heading='Section 3 — Integral operator (3.1)')
add(26,'integral operator',r'''Now we describe our proposal for $\widehat\Theta$. Suppose that we are interested in a specific component $f_j$. Let $\widehat\Theta_j:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_j$ be defined by $\widehat\Theta_j(\boldsymbol\eta)=\sum_{k=1}^d\widehat\Theta_{jk}(\eta_k)$. For the $\widehat f_j^{\mathrm{de}}$ we only need to construct $\widehat\Theta_j$. For an integral operator $\Xi:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_1\times\cdots\times\mathcal H_d$, let $\Xi_j:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_j$ be defined as $\widehat\Theta_j$ with $\Xi_{jk}$ replacing $\widehat\Theta_{jk}$. Define
\[
\|\Xi_{jk}\|_1:=\sup_{u_j\in[0,1]}\left(\int_0^1\Xi_{jk}(u_j,u_k)^2du_k\right)^{1/2},
\]
\[
\|\Xi_j\|_{1,+}:=\sum_{k=1}^d\|\Xi_{jk}\|_1,\qquad\|\Xi_j\|_{1,\max}:=\max_{1\leq k\leq d}\|\Xi_{jk}\|_1,
\]
(3.5)
where $\Xi_{jk}$ in the integral is understood as the kernel of the operator $\Xi_{jk}:\mathcal H_k\to\mathcal H_j$ such that $\Xi_{jk}(\mathbf u,\mathbf x)=\Xi_{jk}(u_j,x_k)$.''',[14],[11],[r'\|\Xi_{jk}\|_1',r'\|\Xi_j\|_{1,+}',r'\|\Xi_j\|_{1,\max}'],'Mixed supremum/L2 kernel norm and row sum/max norms. These are not interchangeable with induced operator norms. The motivating estimated row is not an input to this generic construction.',heading='Section 3.1 — Integral operator norms (3.5)')
add(27,'optimization problem',r'''Define $\gamma$ by
\[
\gamma^{-1}=|S|\sqrt{nh}\left(\sqrt{\frac{\log(d\vee n)}{nh}}+h^{3/2}\right)a_n
\]
(3.6)
for a sequence $a_n\to\infty$. We propose $\widehat\Theta_j$ that solves the following optimization problem:
\[
\text{Minimize}\quad\mathcal F(\Xi):=\sum_{k=1}^d\sup_{u_j,u_k\in[0,1]}|\Xi_{jk}(u_j,u_k)|
\]
\[
\text{subject to}\quad\|[I-(I+\Xi)(I+\widehat\Pi)]_j\|_{1,\max}\leq\gamma.
\]
(3.7)''',[14],[26,25,16,11],[r'\gamma',r'\widehat\Theta_j',r'\mathcal F(\Xi)'],'Rowwise optimization for an approximate inverse using centered empirical kernels. Gamma is specified by the true active-set size and a diverging sequence. Existence, feasibility and measurable selection remain source obligations; Theorem 6 adds a separate constraint only in its second branch.',heading='Section 3.1 — Optimization problem (3.6)–(3.7)')
add(28,'debiased-fLasso-SBF estimator',r'''To remove the second term in the approximation (3.2), we consider the following debiased estimator.
\[
\widehat{\mathbf f}^{\mathrm{de}}:=\widehat{\mathbf f}+\lambda\cdot(I+\widehat\Theta)\nu(\widehat{\mathbf f}).
\]
(3.3)
We call $\widehat{\mathbf f}^{\mathrm{de}}$ the debiased-fLasso-SBF estimator of $\mathbf f$.''',[14],[10,13,27],[r'\widehat{\mathbf f}^{\mathrm{de}}',r'\widehat\Theta'],'The source debiasing correction formed from the penalized estimator, its stationarity-compatible subgradient, and the approximate inverse. The equation is preserved separately from its motivation and asymptotic conclusions.',heading='Section 3.1 — Debiased-fLasso-SBF estimator (3.3)')
add(29,'inverse',r'''Let $\Pi:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_1\times\cdots\times\mathcal H_d$ be the operator composed of $\Pi_{jk}:\mathcal H_k\to\mathcal H_j$, which are defined as at (3.1), now with kernels
\[
\Pi_{jk}(\mathbf u,\mathbf x):=\frac{p_{jk}(u_j,x_k)}{p_j(u_j)}-p_k(x_k)\quad\text{for }j\ne k\text{ and }\Pi_{jj}(\mathbf u,\mathbf x)=0.
\]
Basically, we assume that the operator $I+\Pi$ is invertible. Clearly, under the assumptions (A1) and (A2), each operator $\Pi_{jk}$ for fixed $j\ne k$ is Hilbert–Schmidt and thus compact. The operator $I+\Pi$ has eigenvalues in $[0,1]$, see [2]. If the eigenvalues are bounded away from zero, then $I+\Pi$ is invertible. Let $I+\Theta$ be the inverse of the operator $I+\Pi$.''',[15],[11],[r'\Pi_{jk}',r'I+\Theta'],'Population centered conditional-density operator and its assumed inverse. Neither empirical density estimates nor A1/A2 are inputs to the formula; their occurrence supports a source claim about compactness. The spectral assertion is preserved without certification, and the inverse kernel representation remains an implicit obligation.',heading='Section 3.2 — Population operator and inverse',kind='source_passage')
add(30,'kernels',r'''For this, put
\[
s_1:=\max_{1\leq j\leq d}\sum_{k=1}^d\sup_{u_j,u_k\in[0,1]}|\Theta_{jk}(u_j,u_k)|,\qquad
\widetilde\Delta:=I-(I+\Theta)(I+\widehat\Pi)=(I+\Theta)(\Pi-\widehat\Pi).
\]
For kernels $\widetilde\Delta_{jk}$ of the individual operators comprising $\widetilde\Delta$, define $\widetilde\delta_{jk}$ by
\[
\widetilde\delta_{jk}(u_j):=\sqrt{\int_0^1\widetilde\Delta_{jk}(u_j,x_k)^2dx_k}.
\]''',[15,16],[29,25],[r's_1',r'\widetilde\Delta',r'\widetilde\delta_{jk}'],'Population inverse row size and the discrepancy kernels and their one-variable L2 magnitudes. A7 imposes extra conditions on these objects; it is not needed to define them.',heading='Section 3.2 — Kernels preceding (A7)')
add(31,'univariate functions',r'''The univariate functions $\widetilde\delta_{jk}$ are twice differentiable with the respective, second derivatives $\widetilde\delta_{jk}''$ satisfying $\max_{1\leq j\leq d}\max_{1\leq k\leq d}\int_0^1\widetilde\delta_{jk}''(u_j)^2du_j\lesssim1$. Also, for $\gamma$ at (3.6), it holds that
\[
(1+s_1^2)\left(h+\frac{\log(d\vee n)}{nh^2}\right)\lesssim\gamma^{8/3}.
\]''',[16],[30,27],[r'\widetilde\delta_{jk}',r'\gamma^{8/3}',r's_1^2'],'Second derivatives of the one-variable discrepancy magnitudes are in u_j. The mixed asymptotic bound uses gamma from (3.6). It is distinct from the second-coordinate kernel derivative constraint in Theorem 6.',heading='Assumption (A7)',kind='assumption')
add(32,'stochastic term',r'''To motivate the definition of $\gamma$ at (3.6) and the constraint bound at (3.7), let $\widehat{\mathbf m}$ be decomposed as $\widehat{\mathbf m}=\widehat{\mathbf m}^{A}+\widehat{\mathbf m}^{B}$, where $\widehat{\mathbf m}^{A}$ and $\widehat{\mathbf m}^{B}$, respectively, are defined as $\widehat{\mathbf m}$ with $Y_i$ at (2.5) being replaced by $\epsilon_i$ and $f(\mathbf X_i)=E(Y)+\sum_{j=1}^d f_j(X_{ij})$.''',[14],[6,1],[r'\widehat{\mathbf m}^{A}',r'\widehat{\mathbf m}^{B}'],'Noise and conditional-mean components of the same marginal regression smoother, with the source formula expanded on page 16 and retained as auxiliary context. Gamma appears in motivation only, not as a mathematical input.',heading='Section 3.1 — Stochastic term and regression decomposition',context=r'''In the first term of the above approximation, $(I+\widehat\Theta)\widehat{\mathbf m}$ is decomposed into two terms. One is a stochastic term originated from $\epsilon_i=Y_i-f(\mathbf X_i)$ in $Y_i$, which $\widehat{\mathbf m}$ involves, and the other is deterministic coming from $f(\mathbf X_i)$.''')
add(33,'sup-norm',r'''The following theorem presents estimation error bounds for the integral operator $\widehat\Theta_j$ as an estimator of $\Theta_j$. The first part is in terms of the norm $\|\cdot\|_1$, and the second for the sup-norm $\|\cdot\|_\infty$ defined by
\[
\|\Xi_{jk}\|_\infty:=\sup_{u_j,u_k\in[0,1]}|\Xi_{jk}(u_j,u_k)|.
\]
The second part requires an additional assumption on the second derivative $\Theta_{jk}''$ of $\Theta_{jk}$, where $\Xi_{jk}''$ for $\Xi_{jk}:[0,1]^2\to\mathbb R$ is defined by $\Xi_{jk}''(u_j,x_k):=\frac{\partial^2}{\partial x_k^2}\Xi_{jk}(u_j,x_k)$.''',[18],[11],[r'\|\Xi_{jk}\|_\infty',r"\Xi_{jk}''"],'Supremum of the absolute kernel on the full square and the source second-coordinate derivative convention. Neither the estimated operator nor its target is an input to these generic definitions.',heading='Section 4 — Sup-norm and second derivative')
add(34,'sparsity parameter',r'''$s_q:=\max_{1\leq j\leq d}\sum_{k=1}^d\|\Theta_{jk}\|_\infty^q$.

Next, we derive an upper bound of $s_q$. The upper bound is derived under a mixing condition on the joint distributions of the pairs $(X_j,X_k)$ as in (2.23) but now with the $L^\infty$ norm replacing the $L^2$ norm. To make our discussion more general, we consider
\[
s_q^*:=\max_{1\leq k\leq d}\sum_{j=1}^d\|\Theta_{jk}\|_\infty^q,\qquad q\geq0.
\]
We note that $s_q^*$ can be defined in the same way as $s_q$ with $\Theta_{jk}$ being replaced by the kernel of the adjoint of the operator $\Theta_{jk}$, denoted by $\Theta_{jk}^*$. The kernel of $\Theta_{jk}^*$ is given by $\Theta_{jk}^*(\mathbf u,\mathbf x):=\Theta_{kj}(\mathbf x,\mathbf u)$. Indeed, $s_q^*=\max_{1\leq j\leq d}\sum_{k=1}^d\|\Theta_{jk}^*\|_\infty^q$. We also note that for $q=0$
\[
s_0\vee s_0^*=\max\left\{\max_{1\leq j\leq d}\#\{\Theta_{jk}\ne0:1\leq k\leq d\},\max_{1\leq k\leq d}\#\{\Theta_{jk}\ne0:1\leq j\leq d\}\right\}.
\]
Its role is similar to the “sparsity parameter” of the precision matrix of $\mathbf X$ that appears in precision matrix estimation; see, for example, [9].''',[18],[29,33],[r's_q',r's_q^*',r'\Theta_{jk}^*'],'Row and column sums of powers of the inverse-kernel sup norm. The first displayed definition is excerpted from Theorem 6; the remaining source discussion defines the column version and the q=0 count convention. The author uses sparsity parameter as an analogy, not an assertion that this is a precision matrix.',heading='Theorem 6 and Section 4 — Sparsity parameter comparison',kind='source_passage')
members['D34']['variant_note']='The source compares these inverse-kernel summaries with a precision-matrix sparsity parameter; the comparison does not identify the two objects.'
add(35,'additional constraint',r'''and with the additional constraint that $\max_{1\leq j,k\leq d}\sup_{u_j\in[0,1]}\int_0^1\Xi_{jk}''(u_j,x_k)^2dx_k\lesssim1$ in the optimization at (3.7)''',[18],[27,33],[r"\Xi_{jk}''"],'Additional candidate-kernel second-derivative constraint for the second branch of Theorem 6. It is separate from the preceding regularity assumption on the true inverse kernel and does not alter the first branch.',heading='Theorem 6 — Additional constraint',kind='theorem_excerpt')
interfaces[-1]['lean_role']='hypothesis'
members['D20']['highlight_symbols']=[r'\int K=1',r'c_K',r'L_K']

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    write('source-passages.json',dict(paper_id=PID,status='extracted',scope='Original source entries from Sections 2–4; see the separate paper audit for validation status.',source_passages=list(members.values())))
    write('interface-extraction.json',dict(paper_id=PID,status='extracted',interfaces=interfaces))
    print(f'Saved {len(members)} original source entries; see the separate paper audit for validation status.')
if __name__=='__main__':main()
