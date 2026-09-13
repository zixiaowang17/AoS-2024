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


add('D1','empirical distribution',r'''
Suppose the data size is $N=nK$. Divide the data into $K$ batches each with size $n$ and denote $\widehat P_i$ as the empirical distribution for the $i$-th batch where $i=1,2,\ldots,K$. Denote $\widehat P$ as the entire empirical distribution using all of the $N=nK$ data.
''',[4],'Section 3 — empirical distributions and batch sizes',symbols=[r'\widehat P_i',r'N=nK'],shape='Generic partition and empirical distributions. Independence is imposed separately. The dependent-data sections explicitly reuse these operations on gapped observations or cycle pairs.')
add('D2','statistical functional',r'''
Consider the problem of constructing a CI for $\psi(P)$ where $P$ is an unknown distribution, $\psi$ is a known statistical functional and we have data $X_1,\ldots,X_N$ drawn i.i.d. from $P$.
''',[4],'Section 3 — independent data and statistical functional',{'D1':'N=nK and the empirical batch construction are given immediately afterward.'},kind='condition',symbols=[r'\psi(P)'],phrases=['drawn i.i.d.'],shape='Independent observations for the baseline setting. This law is not imported when the formulas are reused with dependent data or regenerative cycle pairs.')
add('D3','target value',r'''
Here $\psi:=\psi(P)$ is the target value and the limit is as $n\to\infty$ with $K$ fixed.
''',[5],'Section 3 — target and baseline asymptotic regime',symbols=[r'\psi:=\psi(P)'],shape='Target abbreviation and the stated baseline limit. Theorem 7 explicitly replaces this limiting regime with fixed n and K tending to infinity; the target abbreviation is unchanged.')
add('D4','sample variance',r'''
\[
S_{batch}^2=\frac1{K-1}\sum_{i=1}^K\left(\psi(\widehat P_i)-\frac1K\sum_j\psi(\widehat P_j)\right)^2
\]
''',[4],'Section 3 — batching variance',{'D1':'The sample variance uses the K empirical batch estimates.'},context=r'That is, batching uses the batch estimates $\psi(\widehat P_i)$ as primitives and the sample mean and sample variance of these batch estimates to construct a CI.',symbols=[r'S_{batch}^2'],shape='Sample variance centered at the average of batch estimates, with divisor K-1. It is not centered at the full empirical estimate.')
add('D5','variance estimator',r'''
\[
S_{sec}^2=\frac1{K-1}\sum_{i=1}^K\left(\psi(\widehat P_i)-\psi(\widehat P)\right)^2.
\]
Compared with batching, sectioning uses the point estimate $\psi(\widehat P)$ constructed from the entire empirical distribution in both the center of the interval and the center in the variance estimator $S_{sec}^2$.
''',[4],'Section 3 — sectioning variance',{'D1':'Both batch and full empirical estimates are used.'},symbols=[r'S_{sec}^2'],shape='Variance surrogate centered at the full empirical estimate, distinct from the batching sample variance.')
add('D6','Sectioned jackknife',r"""
Let $\widehat P_{(i)}$ be the empirical distribution of all samples except for those from the $i$-th section. Let $J_i=K\psi(\widehat P)-(K-1)\psi(\widehat P_{(i)})$.
""",[4],'Section 3 — sectioned jackknife pseudovalues',{'D1':'The construction removes one whole batch from the full empirical distribution.'},context='Sectioned jackknife (SJ):',symbols=[r'J_i=K\psi(\widehat P)'],shape='Leave-one-batch-out pseudovalues. Their mean is the implicit arithmetic mean bar J. The confidence interval and variance formula are archived separately as auxiliary context.')
add('D7','batching',r'''
\[
W_B:=\frac{\sqrt{nK}\left(\frac1K\sum_i\psi(\widehat P_i)-\psi\right)}{\sqrt{\frac1{K-1}\sum_{i=1}^K\left(\sqrt n\psi(\widehat P_i)-\frac1K\sum_j\sqrt n\psi(\widehat P_j)\right)^2}}
\]
''',[5],'Section 3 — definition of batching statistic in its convergence display',{'D1':'The statistic uses each empirical batch estimate.','D3':'The centering target is the abbreviation psi(P).','D4':'The denominator is sqrt(n) times the batching standard deviation.'},context='For batching, this can be seen by the fact that the corresponding statistic has a limiting',symbols=[r'W_B:='],shape='Original statistic formula, extracted before its displayed convergence arrow. The formula is reused under each data construction. Theorem 7 changes the limiting regime explicitly.')
add('D8','Sectioning',r'''
\[
W_S:=\frac{\sqrt{nK}(\psi(\widehat P)-\psi)}{\sqrt{\frac1{K-1}\sum_{i=1}^K(\sqrt n\psi(\widehat P_i)-\sqrt n\psi(\widehat P))^2}}
\]
''',[5],'Section 3 — definition of sectioning statistic in its convergence display',{'D1':'The numerator uses the full empirical estimate and the denominator uses all batches.','D3':'The target is psi(P).','D5':'The denominator is sqrt(n) times the sectioning standard deviation.'},context='Sectioning is also asymptotically exact since',symbols=[r'W_S:='],shape='Full-sample center with a variance centered at that same estimate. The original formula is separated from its subsequent asymptotic equality.')
add('D9','Sectioning-batching',r'''
\[
W_{SB}:=\frac{\sqrt{nK}(\psi(\widehat P)-\psi)}{\sqrt{\frac1{K-1}\sum_{i=1}^K\left(\sqrt n\psi(\widehat P_i)-\frac1K\sum_j\sqrt n\psi(\widehat P_j)\right)^2}}
\]
''',[5],'Section 3 — definition of sectioning-batching statistic',{'D1':'The numerator uses the full empirical estimate.','D3':'The target is psi(P).','D4':'The denominator uses the batching sample variance.'},context='Sectioning-batching (SB): The SB CI is',context_pages=[4],symbols=[r'W_{SB}:='],shape='Full empirical center combined with the batching denominator. Theorem 7 does not state a limit for this statistic.')
add('D10','Sectioned jackknife',r'''
\[
W_{SJ}:=\frac{\sqrt{nK}(\bar J-\psi_0)}{\sqrt{\frac1{K-1}\sum_{i=1}^K(\sqrt nJ_i-\sqrt n\bar J)^2}}
\]
''',[5],'Section 3 — definition of sectioned jackknife statistic',{'D6':'The numerator and denominator use the original pseudovalues and their mean.','D3':'The source previously names the target psi(P), but this display switches to psi_0; retain this alias rather than editing the formula.'},context='Sectioned jackknife (SJ):',context_pages=[4],symbols=[r'W_{SJ}:='],shape='Studentized mean of sectioned-jackknife pseudovalues. The printed psi_0 differs from the previously introduced target abbreviation; its intended target role is recorded separately.')
add('D11','t-distribution',r'''
$t_{K-1,\alpha/2}$ is the upper $\alpha/2$-quantile of the $t_{K-1}$, the $t$-distribution with degree of freedom $K-1$.
''',[4],'Section 3 — Student law and upper quantile',context='the t-distribution with degree of freedom K − 1.',symbols=[r't_{K-1}'],shape='Student law with K-1 degrees of freedom and upper-tail quantile convention. The sample denominators require K>1; no new t-density formula is fabricated.')

# These are original conditions/definitions from the theorem whose assumptions
# Theorem 6 explicitly inherits, not invented replacement statements.
add('D12','statistical functional',r'''
Suppose that $\psi(\cdot)$ is a statistical functional mapping from distributions in $\mathbb R^d$ to $\mathbb R$ defined by $\psi(\overline P)=f(E_{\overline P}X)$ for a vector $X\sim\overline P$, $X\in\mathbb R^d$.
''',[7],'Theorem 2 — smooth-function functional',symbols=[r'\psi(\overline P)=f(E_{\overline P}X)'],shape='Function of a vector mean. Neither a smoothness order nor an independent observation law is part of this definition itself.')
add('D13',"Cramer's condition",r'''
Assume the following Cramer's condition holds for the distribution of $X_1\in\mathbb R^d$ (recall that $X_1,\ldots,X_{nK}$ are drawn i.i.d. from $P$):
\[
\limsup_{|t|\to\infty}|E_P(\exp\{i\langle t,X\rangle\})|<1,\tag{4}
\]
''',[7],"Theorem 2 — Cramer's condition (4)",{'D2':'This condition explicitly refers to the iid law P.'},kind='condition',symbols=[r'\limsup_{|t|\to\infty}'],shape='Vector characteristic-function Cramer condition in the independent-data theorem. This is distinct from the cycle and split-process conditions in Theorems 3-5.')
add('D14','finite moments',r'''
Suppose that for some positive integer $r$, $X$ has finite moments up to order $r+2$ with nonsingular covariance,
''',[7],'Theorem 2 — moment and covariance condition',kind='condition',symbols=[r'r+2'],phrases=['nonsingular covariance'],shape='Finite moments through r+2 and nonsingular vector covariance. Theorem 6 instantiates r=2, hence fourth moments; no higher moment condition is inserted.')
add('D15','differentiable',r'''
and $f$ is $r+1$ times differentiable in a neighborhood of $E_PX$ with $\nabla f(E_PX)\ne0$.
''',[7],'Theorem 2 — local differentiability condition',{'D12':'The derivatives are of the smooth-function model f.'},kind='condition',symbols=[r'\nabla f(E_PX)\ne0'],shape='Exactly the printed local differentiability order and nonzero gradient. It does not require a nonzero first partial derivative or normalize that derivative to one.')
add('D16','Edgeworth expansion',r'''
Suppose that $\psi(\widehat P_1)$ has a valid Edgeworth expansion, in the sense that for some $0<\sigma<\infty$,
\[
P\left(\frac{\sqrt n(\psi(\widehat P_1)-\psi)}{\sigma}\le q\right)=\Phi(q)+\sum_{j=1}^r n^{-j/2}p_j(q)\phi(q)+O\left(n^{-(r+1)/2}\right)\tag{1}
\]
holds uniformly over $q\in\mathbb R$, and $p_j$ is an even polynomial when $j$ is odd and is an odd polynomial when $j$ is even. Here $\Phi$ and $\phi$ are the distribution function and density function of standard normal.
''',[6],'Theorem 1 — uniform Edgeworth and parity assumption (1)',{'D1':'The expansion concerns an empirical batch estimate.','D3':'It is centered at the original target psi(P).'},kind='condition',symbols=[r'p_j(q)',r'0<\sigma<\infty'],shape='Uniform scalar expansion with alternating parity and stated remainder. The abstract condition is distinct from the sufficient smooth-function assumptions in Theorem 2.')
add('D17','stationary dependent sequence',r'''
Consider a stationary dependent sequence (e.g., a Markov chain) $X_1,X_2,\ldots$ and suppose we are interested in estimating $f(Eg(X_1))$ where the expectation is taken under the stationary measure and $g$ maps from the the state space of the data sequence to $\mathbb R$.
''',[8],'Section 5 — scalar transformed stationary objective',kind='source_passage',symbols=[r'f(Eg(X_1))'],shape='A scalar transform of a stationary sequence, followed by a function f. It replaces the iid data law in Section 3.')
add('D18','gap',r'''
Suppose that, between each two adjacent batches, we discard $n^\delta$ data for some $0<\delta<1$ (for convenience, suppose that after this operation, each batch has $n$ data). Intuitively, with this gap, there is more independence between adjacent batches. After this operation, we construct the CIs in the same way as introduced in Section 3. More precisely, following the convention therein, let $\widehat P_i$, $i=1,2,\ldots,K$ denote the empirical distribution of $X_j$'s in the $i$-th batch (after leaving the gap). Let $\widehat P=\frac1K\sum_{i=1}^K\widehat P_i$ and $\widehat P_{(i)}=\frac1{K-1}\sum_{1\le k\le K,k\ne i}\widehat P_k$. Let $\psi(\cdot)$ be defined as $\psi(\overline P)=f(E_{X\sim\overline P}g(X))$. With these, we construct the CIs $CI_B,CI_S,CI_{SB},CI_{SJ}$ and consider the associated statistics $W_{SJ},W_S,W_B,W_{SB}$ in terms of $\psi(\cdot),\widehat P,\widehat P_i,\widehat P_{(i)}$, $i=1,2,\ldots,K$ using the same formulas as given in Section 3.
''',[8,9],'Section 5.1 — discarded gaps and empirical-law substitution',{'D1':'The empirical operations are reused after gaps have been removed.','D17':'The transformed stationary objective supplies the substituted functional.'},symbols=[r'n^\delta',r'0<\delta<1'],shape='K retained batches of n observations with discarded gaps. This substitution describes the data used by the statistic formulas; it does not assert exact independence between batches.')
add('D19','mixing coefficient',r'''
For any two Borel $\sigma$-fields $\mathcal A$ and $\mathcal B$, define the mixing coefficient $\alpha(\mathcal A,\mathcal B):=\sup_{A\in\mathcal A,B\in\mathcal B}|P(A\cap B)-P(A)P(B)|$. For a stationary sequence $X$ with $\mathcal F_j^l:=\sigma(X_j,\ldots,X_l)$, define $\alpha(n):=\sigma(\mathcal F_{-\infty}^0,\mathcal F_n^\infty)$.
''',[9],'Definition 1 (Mixing coefficient)',symbols=[r'\alpha(n)',r'\alpha(\mathcal A,\mathcal B)'],shape='Original strong-mixing definition. The final expression prints sigma in place of the just-defined alpha; the transcription preserves and flags this mismatch.')
add('D20','Harris recurrence',r'''
A Markov chain $X$ defined on state space $\mathcal X$ is said to be Harris recurrent if there exists a measure $\mu$ such that for any measurable set $B\subset\mathcal X$ satisfying $\mu(B)>0$, we have $P_x(X_n\in B,i.o.)=1$, $\forall x\in\mathcal X$.
''',[9],'Definition 2 (Harris recurrence)',context='Harris recurrence',symbols=[r'P_x(X_n\in B,i.o.)=1'],shape='The exact original recurrence definition. Nonzero or sigma-finite qualifiers for mu are not supplied and are not silently inserted.')
# Preserve the entire original in-theorem construction, without rewriting it.
t4=claims[3]['statement_original']
split_construction=t4[t4.index('Suppose that there exist a set'):t4.index('Suppose that\n\n(i)')]
add('D21','transition probability',split_construction,[10],'Theorem 4 — split-process construction and cycle sums',{'D17':'The centered function g and its stationary mean come from the dependent-data objective.'},symbols=[r'P_{\alpha,\lambda}',r'Q(x,\cdot)',r'\tilde g(x)'],shape='Full source construction with recurrence/minorization, both transition branches, residual kernel, first split return time, centered partial sum and cycle sum. The source overloads delta and alpha; it does not explicitly give the full range of lambda needed for the probability kernel.')
add('D22','regenerative cycles',r'''
Suppose that $X_1,X_2,\ldots$ has a recurrent state $a_0$. Let $T_1=\inf\{k>0:X_k=a_0\}$ and for $i\ge2$, let $T_i=\inf\{k>T_{i-1}:X_k=a_0\}$. Let $Y_i=\sum_{k=T_i}^{T_{i+1}-1}g(X_k)$. We may regard $(Y_i,T_{i+1}-T_i)$ as the new data and perform batching for these data. For example, suppose that we are interested in $E_\pi g(X_1)$, where $\pi$ is the stationary distribution. Note that $E_\pi g(X_1)=\frac{EY_i}{E(T_{i+1}-T_i)}$ which belongs to the family of smooth function models.
''',[11],'Section 5.2 — regenerative return times and rewards',{'D17':'The original sequence and scalar g are from the stationary dependent-data setup.'},context='Approach 2: Decompose into regenerative cycles',symbols=[r'T_1=\inf',r'Y_i=\sum'],shape='Cycles begin at the first return time and end just before the next return. The initial incomplete segment is excluded. Batching uses cycle pairs, not equal-length time blocks; the regenerative independence justification is not supplied as a new invented hypothesis.')
add('D23','two-dimensional distribution',r'''
More concretely, we construct the CIs for $\psi:=E_\pi g(X_1)$ in the following way. Let $Q_i:=(Y_i,T_{i+1}-T_i)$, $i=1,2,\ldots,nK$. Let $\widehat P$, $\widehat P_i$ and $\widehat P_{(i)}$ denote the entire, batched and leave-one-batch-out empirical distributions of $\{Q_i\}_{i=1}^{nK}$ as introduced in Section 3. For any two-dimensional distribution $\overline P$, we define $\psi(\overline P)=\frac{E_{\overline P}[Q^{(1)}]}{E_{\overline P}[Q^{(2)}]}$ where $Q\sim\overline P$ and for $j=1,2$, $Q^{(j)}$ stands for the $j$-th coordinate of $Q$. Note that the target value can be written as $\psi=\frac{EQ_1^{(1)}}{EQ_1^{(2)}}$ (where the expectation is taken under the true distribution of $Q_1$). Construct $CI_B,CI_S,CI_{SB},CI_{SJ}$ and define the corresponding statistics $W_B,W_S,W_{SB},W_{SJ}$ in terms of $\psi(\cdot),\widehat P,\widehat P_i,\widehat P_{(i)}$ using the same formulas as in Section 3.
''',[11],'Section 5.2 — cycle-pair observations and ratio functional',{'D22':'Q_i contains the reward and duration of the original regenerative cycle.','D1':'The empirical operations are reused on nK cycle pairs.'},symbols=[r'Q_i:=(Y_i,T_{i+1}-T_i)',r'\psi(\overline P)'],shape='Ratio of coordinate expectations under the empirical or true cycle-pair law. Positive expected duration is imposed in Theorem 5; do not substitute an average of within-cycle ratios.')
add('D24','coefficients',r'''
\[
P(-q\le W_\cdot\le q)=P(-q\le t_{K-1}\le q)+cn^{-1}+O(n^{-3/2})\tag{6}
\]
where $W_\cdot$ can be either one of $W_S,W_B,W_{SB}$ and $W_{SJ}$ and $c$ is a constant that depends on the method used, the number of batches $K$, the underlying distribution $P$, the function $f$, and the critical point $q$, but does not depend on $n$.
''',[11,12],'Section 6 — symmetric-coverage coefficient (6)',{'D7':'The coefficient can correspond to batching.','D8':'It can correspond to sectioning.','D9':'It can correspond to sectioning-batching.','D10':'It can correspond to sectioned jackknife.','D11':'The comparison coverage is from the Student law.','D12':'Section 6 uses the smooth-function model.'},kind='source_passage',context='An algorithm to estimate coefficients of the',symbols=[r'cn^{-1}'],shape='The coefficient targeted by Theorem 6. This is a coefficient in the coverage expansion, not the bias of an individual batch point estimate.')
add('D26','Initialization',r'''
Initialization: Derivatives of $f$ at $EX_1$ up to order 3, cumulants of $X_1$ up to order 4, testing statistic $W_\cdot$ ($W_\cdot$ can be either of $W_S,W_B,W_{SB}$ and $W_{SJ}$ and is regarded as a function of batch averages and $n$)

1: Let $\Sigma=Var(X_1)$. Simulate $X_1,X_2,\ldots,X_K\stackrel{i.i.d.}{\sim}N(0,\Sigma)$. Let $A_0=\frac{X_1+\cdots+X_K}{K}$, $B_i=X_i-A_0$, $i=1,2,\ldots,K$.
''',[13],'Algorithm 1 — initialization and Gaussian simulation',{'D12':'Derivatives are taken in the original smooth-function model.','D7':'One possible input statistic is W_B.','D8':'One possible input statistic is W_S.','D9':'One possible input statistic is W_SB.','D10':'One possible input statistic is W_SJ.'},symbols=[r'\Sigma=Var(X_1)',r'A_0=\frac{X_1+\cdots+X_K}{K}'],shape='Original-data covariance and cumulants are inputs, followed by fresh Gaussian draws. The source reuses X_i for the simulated draws; this does not assert that the original observations are Gaussian.')
add('D25','polynomials',r'''
\[
p_1(x)=\phi_\Sigma(x)\left[1+\frac16\chi_{ijk}\sigma^{i\alpha}\sigma^{j\beta}\sigma^{k\gamma}x_\alpha x_\beta x_\gamma-\frac12\sigma^{ij}\chi_{ijk}\sigma^{k\alpha}x_\alpha\right]
\]
\[
\begin{aligned}
p_2(x)=\phi_\Sigma(x)\Big[&\frac1{24}\chi_{ijkl}\{\sigma^{i\alpha}\sigma^{j\beta}\sigma^{k\gamma}\sigma^{l\delta}x_\alpha x_\beta x_\gamma x_\delta-6\sigma^{i\alpha}\sigma^{j\beta}\sigma^{kl}x_\alpha x_\beta+3\sigma^{ij}\sigma^{kl}\}\\
&+\frac1{72}\chi_{ijk}\chi_{lmn}\{\sigma^{i\alpha}\sigma^{j\beta}\sigma^{k\gamma}\sigma^{l\delta}\sigma^{m\varepsilon}\sigma^{n\tau}x_\alpha x_\beta x_\gamma x_\delta x_\varepsilon x_\tau\\
&-(6\sigma^{i\alpha}\sigma^{j\beta}\sigma^{k\gamma}\sigma^{l\delta}\sigma^{mn}+9\sigma^{i\alpha}\sigma^{j\beta}\sigma^{l\gamma}\sigma^{m\delta}\sigma^{kn})x_\alpha x_\beta x_\gamma x_\delta\\
&+(9\sigma^{i\alpha}\sigma^{l\beta}\sigma^{jk}\sigma^{mn}+18\sigma^{i\alpha}\sigma^{j\beta}\sigma^{kl}\sigma^{mn}+18\sigma^{i\alpha}\sigma^{l\beta}\sigma^{jm}\sigma^{kn})x_\alpha x_\beta\\
&-(9\sigma^{ij}\sigma^{kl}\sigma^{mn}+6\sigma^{il}\sigma^{jm}\sigma^{kn})\}\Big].\tag{7}
\end{aligned}
\]
Here $\phi_\Sigma(\cdot)$ is the density of $N(0,\Sigma)$, $\sigma^{ij}$ are the coordinates of matrix $\Sigma^{-1}$, and $\chi_{ijk}$ and $\chi_{ijkl}$ stand for the joint cumulants of the coordinates of $X$. The Einstein summation convention is used here, which means we sum over repeated indices. For example, we omit the summation symbol $\sum_{1\le i,j,k,\alpha,\beta,\gamma\le d}$ when we write $\chi_{ijk}\sigma^{i\alpha}\sigma^{j\beta}\sigma^{k\gamma}x_\alpha x_\beta x_\gamma$.
''',[12],'Section 6 — expressions (7) and tensor conventions',{'D26':'Sigma and the cumulants are original-law inputs to the algorithm, before Gaussian simulation.'},context='The polynomials',symbols=[r'p_1(x)',r'p_2(x)',r'\chi_{ijk}'],shape='Both printed density-weighted expressions, including the constant 1 in p_1, all fourth-order and squared-third-cumulant contractions. They are called polynomials in the source despite Gaussian-density factors; preserve that terminology and record the issue separately.')
add('D27','polynomials',r'''
Let $u=\nabla f$, $v=\nabla^2f/2$, $w=\nabla^3f/6$. Recall the definition of $A_0,B_i$, $i=1,2,\ldots,K$ in Algorithm 1. Then
\[
\begin{aligned}
W_S&=\frac{\sqrt{nK}(f(m+n^{-1/2}A_0)-f_0)}{\sqrt{\frac1{K-1}\sum_{i=1}^K(\sqrt nf(m+n^{-1/2}X_i)-\sqrt nf(m+n^{-1/2}A_0))^2}}\\
&=\sqrt{K(K-1)}\frac{[u,A_0]+n^{-1/2}[v,A_0,A_0]+n^{-1}[w,A_0,A_0,A_0]}{\sqrt{\sum_{i=1}^K\left([u,A_i-A_0]+n^{-1/2}[v,A_i,A_i]-n^{-1/2}[v,A_0,A_0]+n^{-1}[w,A_i,A_i,A_i]-n^{-1}[w,A_0,A_0,A_0]\right)^2}}+O_p(n^{-3/2})
\end{aligned}
\]
Here, $[u,A_m];=u_iA_{m,i}$, $[v,A_m,A_m]=:v_{ij}A_{m,i}A_{m,j}$, $[w,A_m,A_m,A_m]=:w_{ijk}A_{m,i}A_{m,j}A_{m,k}$. The leading term of the denominator is $\sum_i[u,A_i-A_0]^2$. The coefficient for $n^{-1/2}$ is
\[
\lambda=2\sum_i[u,B_i]([v,B_i+A_0,B_i+A_0]-[v,A_0,A_0])
\]
The coefficient for $n^{-1}$ is
\[
e=\sum_i\left[([v,B_i+A_0,B_i+A_0]-[v,A_0,A_0])^2+2[u,B_i]([w,B_i+A_0,B_i+A_0,B_i+A_0]-[w,A_0,A_0,A_0])\right]
\]
We also have $a=[u,A_0]$, $b_1=[v,A_0,A_0]$, $b_2=[v,A_0,A_0,A_0]$. The derivatives w.r.t. $A_{0,1}$ can be computed as
\[
b_1'=2v_{11}A_{0,1}+2\sum_{j=2}^d v_{1j}A_{0,j}=2\sum_{j=1}^d v_{1j}A_{0,j}
\]
\[
\lambda'=2\sum_i[u,B_i]2\left(\sum_{j=1}^d v_{1j}(B_{i,j}+A_{0,j})-\sum_{j=1}^d v_{1j}A_{0,j}\right)=4\sum_i[u,B_i]\sum_{j=1}^d v_{1j}B_{i,j}.
\]
This gives all polynomials required by Steps 2 and 3 of Algorithm 1.
''',[12,14],'Section 6 — sectioning Taylor coefficients, continued on page 14',{'D26':'The coefficients use the simulated mean A_0 and centered Gaussian batches B_i.','D12':'The tensors are derivatives of f.','D8':'The expansion is specifically for the sectioning statistic.'},symbols=[r'b_1=[v,A_0,A_0]',r'\lambda=2\sum_i'],shape='Complete original sectioning example. The source alternates A_i/X_i, uses f_0 and m without local definitions, and prints v in a cubic contraction for b_2. The baseline variance E_2 is named as the leading squared-denominator term. The inline 2 in lambda-prime is retained as multiplication, not a superscript.')
add('D28','unbiased simulation scheme',r'''
2: Perform Taylor's expansion on $W_\cdot$ regarding $X_1,\ldots,X_K$ as the batch averages, and write it as $W_\cdot=\sqrt{K(K-1)}\frac{a+n^{-1/2}b_1+n^{-1}b_2}{\sqrt{E_2+n^{-1/2}\lambda+n^{-1}e}}+O_p(n^{-3/2})$. Express each of $a,b_1,b_2,\lambda,e,E_2$ as a polynomial of $A_0,B_1,B_2,\ldots,B_K$ (the expressions depend on the batching scheme we use. The expressions for sectioning is included in Section 6. The expressions for other schemes are given in Section B).

3: Compute the derivative of $b_1$ and $\lambda$ w.r.t. $A_{0,1}$ and denote them by $b_1'$ and $\lambda'$ respectively. Then let (denote $u=\nabla f(EX_1)$)
\[
F_x=\frac{b_1}{\sqrt{E_2}}-\frac12\frac{\lambda a}{E_2\sqrt{E_2}},\quad F_{xx}=\frac1{\sqrt{E_2}}\left(a\left(-\frac e{E_2}+\frac34\frac{\lambda^2}{E_2^2}\right)-b_1\frac\lambda c+2b_2\right),
\]
\[
F_y=\frac{a'}{\sqrt{E_2}},\quad F_{xy}=\frac{b_1'}{\sqrt{E_2}}-\frac12\frac{(\lambda a)'}{E_2\sqrt{E_2}},
\]
\[
F_+=\frac{q\sqrt{E_2}}{\sqrt{K(K-1)}}-\sum_{i=2}^d u_iA_{0,i},\quad F_-=\frac{-q\sqrt{E_2}}{\sqrt{K(K-1)}}-\sum_{i=2}^d u_iA_{0,i}.
\]

4: Compute
\[
y_x=\left.-F_x/F_y\right|_{A_{0,1}=F_+},\quad y_{xx}=\left.-(F_{xx}+2F_{xy}y_x)/F_y\right|_{A_{0,1}=F_+},
\]
\[
y_x^{(-)}=\left.-F_x/F_y\right|_{A_{0,1}=F_-},\quad y_{xx}^{(-)}=\left.-(F_{xx}+2F_{xy}y_x)/F_y\right|_{A_{0,1}=F_-}.
\]

5: Derive the error term estimator:
\[
\begin{aligned}
ER={}&I_C(A)\left[\sum_{1\le i<j\le K}p_1(x_i(A))p_1(x_j(A))+\sum_{1\le i\le K}p_2(x_i(A))\right]\\
&\left(\left.\phi_{\tilde\sigma_0}(F_+-\mu)(p_1(x(A)))\right|_{A_{0,1}=F_+}(y_x)-\left.\phi_{\tilde\sigma_0}(F_--\mu)(p_1(x(A)))\right|_{A_{0,1}=F_-}(y_x^{(-)})\right)\\
&+\left(\phi_{\tilde\sigma_0}(F_+-\mu)\left(\frac12y_{xx}\right)-\phi_{\tilde\sigma_0}(F_--\mu)\left(\frac12y_{xx}^{(-)}\right)\right)\\
&+\frac12\left(\phi_{\tilde\sigma_0}(F_+-\mu)(-(F_+-\mu)/\tilde\sigma_0)y_x^2-\phi'_{\tilde\sigma_0}(F_--\mu)(-(F_--\mu)/\tilde\sigma_0)y_x^{(-)2}\right).
\end{aligned}
\]
Here,
\[
(x_1(A),\ldots,x_K(A))^\top=
\begin{pmatrix}
1&1&&&\\
1&&1&&\\
\vdots&&&\ddots&\\
1&&&&1\\
1&-1&-1&\cdots&-1
\end{pmatrix}
\begin{pmatrix}A_0\\B_1\\\ldots\\B_{K-2}\\B_{K-1}\end{pmatrix}
\]
and $C$ represents $-q\le\sqrt{K(K-1)}\frac{[u,A_0]}{\sqrt{\sum_{i=1}^K([u,A_i-A_0])^2}}\le q$. The polynomials $p_1$ and $p_2$ are given in (7). $\tilde\sigma_0=(\sigma_0-\sigma_{01}\sigma_{11}^{-1}\sigma_{10})/K$, $\sigma_0$ is the variance of the first coordinate of $X_1$, $\sigma_{11}$ is the variance of the last $d-1$ coordinates of $X_1$, and $\sigma_{01}$ is their covariance. $\mu=\sigma_{01}\sigma_{11}^{-1}A_0'$ where $A_0'$ is the vector of the last $d-1$ coordinates of $A_0$. $\phi_\sigma(\cdot)$ is the density of $N(0,\sigma)$.

Output: An unbiased estimator of $c$ in (6) given by $ER$
''',[13],'Algorithm 1 — Taylor, boundary and output steps 2-5',{'D26':'The initial derivatives, cumulants, selected statistic and Gaussian coordinates are supplied by Algorithm 1 initialization and Step 1.','D25':'Step 5 explicitly uses p_1 and p_2 from equation (7).','D27':'Step 2 refers to the main-text sectioning coefficient example; explicit formulas for the other methods are relegated to excluded Section B.','D24':'The output targets the coefficient c in coverage expansion (6).'},context=r'An unbiased simulation scheme to compute the coefficient of the $n^{-1}$ error term',symbols=[r'ER=',r'F_{xx}=',r'y_x^{(-)}'],shape='Full remaining algorithm and auxiliary definitions, with no silent correction of its unexplained denominator c, first-gradient normalization, negative-side y_x, missing plus sign, p_1(x(A)) dimension or negative-side phi-prime. The original source is not converted into an executable unbiased estimator.')
add('D29','influence function',r'''
where $IF(\cdot)$ is the influence function of $\psi$ at $P$.
''',[5],'Section 3 — influence-function notation',kind='source_passage',symbols=[r'IF(\cdot)'],shape='The paper names the influence function but does not give a full derivative definition in main text. Theorem 7 supplies continuous Gateaux differentiability and a finite positive variance; no tangent topology or stronger differentiability condition is invented.')


# Source-inspected rendering amendment; see the explicit saved review plan.
members['D22']['highlight_symbols'] = ['T_1=\\inf', 'Y_i=\\sum_{k=T_i}^{T_{i+1}-1}g(X_k)']

def main():
    for lid,m in members.items():
        assert all(d in members for d in m['depends_on']),lid
        assert any(s in m['statement_original']+' '+m['local_label'] for s in m['highlight_symbols']+m['highlight_phrases']),lid
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages; full source audit remains pending.')

if __name__=='__main__':main()
