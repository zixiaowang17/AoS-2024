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
add('D1','independent identically distributed',r'''
To be precise, let $X_1,\ldots,X_n$ denote independent identically distributed $p$-dimensional random vectors with distribution function $F$. Note that formally $F$ depends on the dimension $p$, which varies with $n$, but we will not reflect this dependence in our notation throughout this paper.
''',[4],'Section 2 — sampling model',kind='source_passage',phrases=['independent identically distributed'],shape='An iid sample of p-dimensional vectors whose distribution can change with the dimension and sample size. Dependence among coordinates within a vector is allowed.')
add('D2','symmetric kernel',r'''
For some positive integer $m$ let
\[
h=(h_1,\ldots,h_d)^\top:(\mathbb R^p)^m\to\mathbb R^d\tag{2.1}
\]
denote a measurable symmetric function with finite expectation
\[
\theta_F=(\theta_1,\ldots,\theta_d)^\top=\mathbb E_F[h(X_1,\ldots,X_m)]\in\mathbb R^d,\tag{2.2}
\]
which defines our parameter of interest.
''',[4],'Section 2 — kernel and expectation parameter, equations (2.1)-(2.2)',{'D1':'The kernel expectation is evaluated on m independent vectors with the sample law F.'},context=r'where $h_i$, the ith component of the vector $h$ in (2.1), is a symmetric kernel of order $m$.',symbols=[r'\theta_F',r'h=(h_1,\ldots,h_d)^\top'],shape='Measurable symmetric vector kernel of positive integer order m and its finite expectation. Kernel dimension d need not equal observation dimension p.')
members['D2']['naming_context'][0]['evidence']=[dict(page=6,location='Section 2.1 continuation — symmetric kernel')]
add('D3','U-statistic',r'''
In order to estimate the parameter $\theta_F$ we consider the U-statistic of order $m$
\[
U=(U_1,\ldots,U_d)^\top=\binom nm^{-1}\sum_{1\leq l_1<\ldots<l_m\leq n}h(X_{l_1},\ldots,X_{l_m}).\tag{2.3}
\]
''',[4],'Section 2 — vector U-statistic, equation (2.3)',{'D2':'The estimator averages the order-m symmetric vector kernel over distinct sample indices.'},phrases=['U-statistic'],symbols=[r'U=(U_1,\ldots,U_d)^\top'],shape='Complete order-m U-statistic with each increasing tuple counted once. Coordinate U_i is repeated explicitly in (2.6). No particular pairwise dependence measure or covariance kernel is assumed.')
add('D4','dependence measure',r'''
To be precise, for $1\leq i<j\leq p$ let
\[
d_{ij}=d(X_{1i},X_{1j})=\mathbb E_F[\widetilde h(X_{1i},X_{1j},\ldots,X_{mi},X_{mj})]\tag{2.4}
\]
denote a dependence measure between the ith and jth components of the random vector $X_1=(X_{11},\ldots,X_{1p})^\top$, which can be expressed as the expectation of a kernel $\widetilde h:\mathbb R^{2m}\to\mathbb R$ of order $m$ evaluated at $(X_{1i},X_{1j},\ldots,X_{mi},X_{mj})$. In this case the function $h$ in (2.1) is defined by
\[
h(X_1,\ldots,X_m)=\operatorname{vech}\big((h_{ij}(X_1,\ldots,X_m))_{i,j=1,\ldots,p}\big)
=\operatorname{vech}\big((\widetilde h(X_{1i},X_{1j},\ldots,X_{mi},X_{mj}))_{i,j=1,\ldots,p}\big),
\]
where the second equality defines the functions $h_{ij}:\mathbb R^{pm}\to\mathbb R$ in an obvious manner and $\operatorname{vech}(\cdot)$ is the operator that stacks the columns above the diagonal of a symmetric $p\times p$ matrix as a vector with $d=p(p-1)/2$ components. Note that the index $(i,j)$ in the definition of the function $h_{ij}$ is only used to emphasize that each $h_{ij}$ acts on different components of the vectors $X_1,\ldots,X_m$. Similarly, the vector $\theta_F$ is defined by $\theta_F=\operatorname{vech}\big((d_{ij})_{i,j=1,\ldots,p}\big)$,
''',[5],'Example 2.1 — pairwise dependence and upper-triangle vectorization, equation (2.4)',{'D2':'The pairwise kernel construction specializes the general parameter h and theta_F.'},phrases=['dependence measure'],symbols=[r'd_{ij}',r'\operatorname{vech}'],shape='Pairwise kernel-expectation dependence measures arranged in an upper-triangle vector. The source uses vech for columns above the diagonal, excluding the diagonal; this convention is not replaced by the usual lower-triangle convention.')
add('D5','relevant hypotheses',r'''
Recall that, in this paper, we are not interested in testing the “classical” hypotheses $H_0:\theta_F=0$ versus $H_1:\theta_F\neq0$, but want to investigate if at least one of the components $\theta_i$ of the vector $\theta_F=(\theta_1,\ldots,\theta_d)^\top$ exceeds a given threshold $\Delta>0$, that is
\[
H_0:\max_{i=1}^d|\theta_i|\leq\Delta\quad\text{versus}\quad H_1:\max_{i=1}^d|\theta_i|>\Delta,\tag{2.5}
\]
where $\Delta$ denotes the largest deviation that is still considered as negligible. Hypotheses of this form are often called relevant hypotheses.
''',[5],'Section 2 — relevant hypotheses, equation (2.5)',{'D2':'The hypotheses constrain the maximum absolute coordinate of the expectation parameter theta_F.'},kind='condition',phrases=['relevant hypotheses'],symbols=[r'\Delta>0',r'\max_{i=1}^d|\theta_i|'],shape='Composite null that all coordinate magnitudes are at most a positive threshold, versus any exceedance. The threshold is not zero and the alternative inequality is strict.')
add('D6','non-degenerate',r'''
and introduce the notations
\[
\zeta_{1,i}=\operatorname{Var}_F(h_{1,i}(X_1))\quad\text{and}\quad
h_{1,i}(x)=\mathbb E_F[h_i(X_1,\ldots,X_m)\mid X_1=x].\tag{2.8}
\]
If $\zeta_{1,i}>0$, the kernel $h_i$ of the statistic $U_i$ is called non-degenerate. Note that this property depends on the kernel $h_i$ and on the distribution $F$.
''',[6],'Section 2.1 — first projection and non-degeneracy, equation (2.8)',{'D2':'The first-coordinate conditional expectation is taken for each kernel h_i under F.'},kind='source_passage',phrases=['non-degenerate'],symbols=[r'\zeta_{1,i}',r'h_{1,i}(x)'],shape='Uncentered first conditional projection and its variance, with the source non-degeneracy criterion. This records the definition without imposing positivity on every coordinate.')
add('D7','Jackknife based estimator',r'''
\[
\widehat\sigma_i^2:=\frac{m^2(n-1)}{n(n-m)^2}\sum_{k=1}^n(q_{k,i}-U_i)^2\tag{2.10}
\]
is a Jackknife based estimator of the variance of $U_i$ and $q_{k,i}$ is defined by
\[
q_{k,i}:=\binom{n-1}{m-1}^{-1}
\sum_{1\leq l_1<\ldots<l_{m-1}\leq n,\ l_j\neq k}
h_i(X_k,X_{l_1},\ldots,X_{l_{m-1}})
\]
''',[6],'Section 2.1 — jackknife variance estimator, equation (2.10)',{'D3':'The centering is U_i and each jackknife average holds one sample vector fixed.'},phrases=['Jackknife based estimator'],symbols=[r'\widehat\sigma_i^2',r'q_{k,i}'],shape='Jackknife estimate of the finite-sample variance of U_i, with the exact n,m factor. The test uses its nonnegative square root. Zero empirical variance requires a convention absent from the source.')
add('D8','test statistic',r'''
We propose to use the test statistic
\[
\mathcal T_{n,\Delta}:=\max_{1\leq i\leq d}\frac{U_i^2-\Delta^2}{2\widehat\sigma_i\Delta}\tag{2.9}
\]
for testing the hypotheses in (2.5),
''',[6],'Section 2.1 — normalized squared statistic, equation (2.9)',{'D3':'U_i estimates the corresponding kernel expectation.','D7':'The coordinate difference is divided by the jackknife standard error.','D5':'Delta is the positive relevance threshold in (2.5).'},phrases=['test statistic'],symbols=[r'\mathcal T_{n,\Delta}'],shape='Maximum of coordinatewise squared-expectation differences normalized by twice the positive threshold times each empirical standard error. This is distinct from the later unnormalized absolute statistic.')
add('D9','standard Gumbel distribution',r'''
where $q_{1-\alpha}=-\log(\log(\frac1{1-\alpha}))$ is the $(1-\alpha)$-quantile of the standard Gumbel distribution with distribution function $\exp(-\exp(-x))$, $x\in\mathbb R$, and
\[
a_d=\sqrt{2\log d}\quad\text{and}\quad b_d=a_d-\frac{\log(\log d)+\log(4\pi)}{2a_d}.
\]
''',[6],'Section 2.1 — Gumbel quantile and normalizing constants after (2.11)',phrases=['standard Gumbel distribution'],symbols=[r'q_{1-\alpha}',r'a_d',r'b_d'],shape='Standard Gumbel law, its explicit quantile and the extreme-value normalizers used by the asymptotic critical threshold. These formulas need d>1; the source growth regime is recorded separately.')
add('D10','Orlicz norm',r'''
In what follows, we will need the function $\psi_\beta(x)=\exp(x^\beta)-1$ and the corresponding Orlicz norm
\[
\|Z\|_{\psi_\beta}:=\inf\{\nu>0:\mathbb E[\psi_\beta(|Z|/\nu)]\leq1\}\tag{2.13}
\]
of a real-valued random variable $Z$.
''',[7],'Section 2.1 — exponential Orlicz quantity, equation (2.13)',phrases=['Orlicz norm'],symbols=[r'\psi_\beta',r'\|Z\|_{\psi_\beta}'],shape='The source exponential Orlicz quantity for scalar variables. The parameter range beta in (0,2] comes from the assumptions; for beta<1 it is conventionally a quasi-norm rather than a norm, but the source wording is preserved.')
add('D11','uniform tail probability decay',r'''
For some constant $\beta\in(0,2]$ there exist a non-negative sequence $(B_n)_{n\in\mathbb N}$ and a constant $D>0$ such that for all $d=d(n)$, $n\in\mathbb N$,
\[
\max_{1\leq i\leq d}\|h_i(X_1,\ldots,X_m)-\theta_i\|_{\psi_\beta}\leq B_n,\qquad
\max_{1\leq i\leq d}\zeta_{1,i}\leq D,\qquad
\max_{1\leq i\leq d}\mathbb E_F[(h_{1,i}(X_1)-\theta_i)^4]\leq DB_n^2.
\]
''',[7],'Assumption (A1)',{'D2':'The kernel coordinates and their expectations occur in the centered tail bound.','D6':'The variance and fourth-moment bounds concern the first conditional projection.','D10':'The centered kernel tail is measured by the psi_beta Orlicz quantity.'},kind='assumption',context='Assumption (A1) is a technical condition that captures a uniform tail probability decay from which we will deduce concentration inequalities for the components of the U-statistic defined in (2.3).',phrases=['(A1)'],symbols=[r'DB_n^2'],shape='All three source conditions: exponential centered-kernel tail, bounded projection variance and projection fourth moment. B_n is only required to be nonnegative; it is not silently assumed uniformly positive or bounded.')
add('D12','uniform non-degeneracy requirement',r'''
There exist constants $\underline b>0$ and $c\in(0,\Delta)$ such that $\min_{1\leq i\leq d,|\theta_i|>c}\zeta_{1,i}>\underline b$ for all $d=d(n)$, $n\in\mathbb N$. Here and in the following, a minimum over the empty set is defined as $+\infty$.
''',[7],'Assumption (A2)',{'D6':'The lower bound is on the first-projection variance.','D5':'The cutoff c lies strictly between zero and the relevance threshold Delta.'},kind='assumption',context='Assumption (A2) is a uniform non-degeneracy requirement which is a standard condition for deriving Gaussian approximation results,',phrases=['(A2)'],symbols=[r'\min_{1\leq i\leq d,|\theta_i|>c}',r'\underline b'],shape='Uniform positive projection variance only for parameters bounded away from zero. The strict cutoff and strict lower bound, and the empty-minimum value, are preserved.')
add('D13','correlation',r'''
Let $\kappa_{i,j}=\operatorname{Corr}_F(h_{1,i}(X_1),h_{1,j}(X_1))\in(-1,1)$ denote the correlation between $h_{1,i}(X_1)$ and $h_{1,j}(X_1)$. There exist a constant $\epsilon>0$ and a sequence $\gamma_n=o(1)$ such that for all $d=d(n)$, $n\in\mathbb N$
\[
\sum_{1\leq i\neq j\leq d}\frac{|\kappa_{i,j}|}{\sqrt{1-\kappa_{i,j}^2}}
\exp\left(-\frac{(2-\epsilon)\log d}{1+|\kappa_{i,j}|}\right)\leq\gamma_n.
\]
''',[7],'Assumption (A3)',{'D6':'The correlations are between first conditional projections of kernel coordinates.'},kind='assumption',phrases=['correlation','(A3)'],symbols=[r'\kappa_{i,j}',r'\gamma_n=o(1)'],shape='Off-diagonal correlation summability condition for the Gumbel approximation, with each stated correlation strictly between minus one and one. It is not needed by the bootstrap theorems.')
add('D14','null hypothesis',r'''
For a precise statement consider the set of all distribution functions on $\mathbb R^d$ satisfying Assumptions (A1) - (A3), and define
\[
V_0:=\{z=(z_1,\ldots,z_d)^\top\in\mathbb R^d\mid\max_{1\leq i\leq d}|z_i|\leq\Delta\}\tag{2.14}
\]
as the parameter space corresponding to the null hypothesis in (2.5). Note that these sets depend on $n$ (through the dimension $d=d(n)$). We define
\[
\mathcal H_0(\Delta):=\{F\in\mathcal F\mid\theta_F\in V_0,\ F\text{ satisfies Assumptions (A1), (A2), (A3)}\}\tag{2.15}
\]
as the set of distribution functions satisfying the null hypothesis (and the basic assumptions) with existing expectation $\mathbb E_F[U]$. Note that $\mathcal H_0(\Delta)$ depends on the constants $\underline b$, $D$ and on $n$ (through the dimension $d=d(n)$ and sequence $(B_n)_{n\in\mathbb N}$) which is not reflected in our notation.
''',[8],'Section 2.1 — composite null distribution class, equations (2.14)-(2.15)',{'D5':'V_0 is the expectation-parameter null region.','D11':'The class imposes all conditions in (A1).','D12':'The class imposes the restricted non-degeneracy condition (A2).','D13':'The class imposes the correlation condition (A3).'},kind='condition',phrases=['null hypothesis'],symbols=[r'\mathcal H_0(\Delta)',r'V_0'],shape='Composite null class for the Gumbel-calibrated test. The source opening says distributions on R^d although the sampling class F was defined on R^p; both source conventions are preserved.')
add('D15','alternatives',r'''
Next we turn to the consistency of the test (2.11) and define
\[
V(c)=\{z\in\mathbb R^d\mid\max_{1\leq i\leq d}|z_i|\geq\Delta+cB_n((\log d)/n)^{1/2}\}
\]
as a set of alternatives (note that for a bounded kernel $h$ the sequence $B_n$ can be chosen as a constant sequence). We will study the power of the test (2.11) against alternatives in the set
\[
\mathcal H_1(c)=\{F\in\mathcal F\mid\theta_F\in V(c);\ F\text{ satisfies Assumption (A1)}\}.\tag{2.18}
\]
''',[8,9],'Section 2.1 — separated alternatives, equation (2.18)',{'D5':'The alternatives are separated from the relevance threshold Delta.','D11':'The class uses the sequence B_n and imposes (A1), but not (A2) or (A3).'},kind='condition',phrases=['alternatives'],symbols=[r'\mathcal H_1(c)',r'\Delta+cB_n((\log d)/n)^{1/2}'],shape='Uniform alternative class with maximum parameter magnitude at least Delta plus the specified separation. The lower bound is weak and only Assumption (A1) enters the class. The bootstrap theorem substitutes a logarithmically inflated argument.')
add('D16','parameter space',r'''
\[
V_0:=\{z=(z_1,\ldots,z_d)^\top\in\mathbb R^d\mid\max_{1\leq i\leq d}|z_i|\leq\Delta\}\tag{2.14}
\]
as the parameter space corresponding to the null hypothesis in (2.5).
''',[8],'Section 2.1 — null parameter region, equation (2.14)',phrases=['parameter space'],symbols=[r'V_0'],shape='Closed coordinatewise threshold region in parameter space. Its definition does not impose any distributional tail, non-degeneracy or correlation assumption.')
members['D14']['depends_on'].append('D16');edges['D14']['D16']='The class requires theta_F in the null parameter region V_0 defined in (2.14).'
add('D17','von-Mises conditions',r'''
Let Assumption (A1) hold and assume that the constant $\beta\in(0,2]$ and the sequence $(B_n)_{n\in\mathbb N}$ satisfy additionally $\max_{1\leq i\leq d}\|h_i(X_{j_1},\ldots,X_{j_m})\|_{\psi_\beta}\leq B_n$, for all $j_1,\ldots,j_m\in\{1,\ldots,n\}$.
''',[10],"Assumption (A1')",{'D11':'The strengthened condition includes all of (A1), and then adds bounds for repeated sample indices.'},kind='assumption',context=r'Additionally, we need some conditions on the entries $h_i(X_1,\ldots,X_1,X_{m-k},\ldots,X_m)$ for all $1\leq k\leq m$, which are known as von-Mises conditions in the literature',phrases=["(A1')"],symbols=[r'\|h_i(X_{j_1},\ldots,X_{j_m})\|_{\psi_\beta}'],shape='Additional uncentered Orlicz bounds on all index tuples, including repeated indices, with the same B_n and beta. This strengthens (A1); it does not add the Gumbel correlation condition (A3).')
add('D18','bootstrap analogue',r'''
To be precise, let $X_1^*,\ldots,X_n^*$ be drawn with replacement from $X_1,\ldots,X_n$ and define for $i=1,\ldots,d$ by
\[
U_i^*=\binom nm^{-1}\sum_{1\leq l_1<\ldots<l_m\leq n}h_i(X_{l_1}^*,\ldots,X_{l_m}^*)\tag{2.19}
\]
a bootstrap analogue of the statistic introduced in (2.6).
''',[9],'Section 2.2 — resampled U-statistic, equation (2.19)',{'D3':'The bootstrap applies the same U-statistic kernel to a replacement sample from the empirical distribution.'},phrases=['bootstrap analogue'],symbols=[r'U_i^*'],shape='Empirical bootstrap U-statistic, conditionally iid resampling the observed vectors with replacement. Repeated original observations can enter a tuple despite its distinct bootstrap indices.')
add('D19','V-statistic',r'''
Note that the conditional expectation of $U_i^*$ given $X_1,\ldots,X_n$ is given by the V-statistic
\[
V_i=\mathbb E_F[U_i^*\mid X_1,\ldots,X_n]=\frac1{n^m}\sum_{l_1,\ldots,l_m=1}^n h_i(X_{l_1},\ldots,X_{l_m}).\tag{2.20}
\]
''',[9],'Section 2.2 — conditional bootstrap expectation, equation (2.20)',{'D18':'V_i is the conditional mean of the resampled U-statistic, equivalently a full index-tuple average.'},phrases=['V-statistic'],symbols=[r'V_i=\mathbb E_F[U_i^*\mid X_1,\ldots,X_n]'],shape='Full V-statistic including repeated indices, equal to the conditional expectation of U_i*. This is not the original distinct-index U-statistic.')
add('D20','truncated version',r'''
Next we define a truncated version of $V_i$, that is
\[
V_{i,\Delta}=\begin{cases}V_i,&\text{if }|V_i|\leq\Delta,\\\Delta,&\text{otherwise}\end{cases}
\quad i=1,\ldots,d\tag{2.21}
\]
and note that $|\mathbb E[U_i^*-V_i+V_{i,\Delta}\mid X_1,\ldots,X_n]|\leq\Delta$ a.s.
''',[10],'Section 2.2 — truncation to the null, equation (2.21)',{'D19':'The truncation acts on the V-statistic conditional mean.','D5':'Delta is the positive relevance threshold.'},phrases=['truncated version'],symbols=[r'V_{i,\Delta}'],shape='The source truncation keeps V_i inside the interval and maps every outside value, positive or negative, to positive Delta. It is not silently replaced by signed clipping.')
add('D21','bootstrap analogue',r'''
We finally define
\[
\mathcal T_n^*=\max_{1\leq i\leq d}\frac{(U_i^*-V_i+V_{i,\Delta})^2-V_{i,\Delta}^2}{2\widehat\sigma_i\Delta}\tag{2.22}
\]
as the bootstrap analogue of the statistic $\mathcal T_{n,\Delta}$ defined in (2.9) and denote by $q_{1-\alpha}^*$ the $(1-\alpha)$-quantile of the distribution of $\mathcal T_n^*$. We propose to reject the null hypothesis in (2.5), whenever
\[
\mathcal T_{n,\Delta}>q_{1-\alpha}^*.\tag{2.23}
\]
''',[10],'Section 2.2 — normalized bootstrap statistic and test, equations (2.22)-(2.23)',{'D18':'The statistic uses the resampled U_i*.','D19':'It recenters by its V-statistic conditional mean.','D20':'It adds back the null-truncated mean and subtracts its square.','D8':'The observed statistic and standard-error normalization are those of (2.9).'},phrases=['bootstrap analogue'],symbols=[r'\mathcal T_n^*',r'q_{1-\alpha}^*'],shape='Conditionally calibrated squared bootstrap maximum with the original-data jackknife normalization. Its quantile is conditional on the observations, as required by the bootstrap construction.')
add('D22','null hypothesis',r'''
where
\[
\mathcal H_{0,\mathrm{boot}}(\Delta):=\{F\in\mathcal F\mid\theta_F\in V_0;\ F\text{ satisfies Assumptions (A1'), (A2)}\}\tag{2.26}
\]
and $V_0$ is defined in (2.14).
''',[10],'Theorem 2.5 — bootstrap null distribution class, equation (2.26)',{'D2':'The class constrains the expectation parameter theta_F.','D16':'V_0 is the common null parameter region; it carries no correlation restriction.','D17':'The class imposes the repeated-index kernel bounds (A1-prime).','D12':'The class also imposes restricted non-degeneracy (A2).'},kind='theorem_excerpt',context=r'We propose to reject the null hypothesis in (2.5), whenever $\mathcal T_{n,\Delta}>q_{1-\alpha}^*$.',symbols=[r'\mathcal H_{0,\mathrm{boot}}(\Delta)'],shape='Composite null distribution class for the bootstrap test, with (A1-prime) and (A2), and without (A3). It is not identified with H_0(Delta) from (2.15).')
add('D23','test statistic',r'''
To be precise, we consider the non-normalized case and define the test statistic by
\[
\mathcal T_{n,\Delta}^{\mathrm{abs}}:=\sqrt n\left(\max_{1\leq i\leq d}|U_i|-\Delta\right).\tag{2.30}
\]
''',[12],'Section 2.2 — absolute-value statistic, equation (2.30)',{'D3':'The statistic uses absolute values of the coordinate U-statistics.','D5':'It subtracts the positive relevance threshold.'},phrases=['test statistic'],symbols=[r'\mathcal T_{n,\Delta}^{\mathrm{abs}}'],shape='Unnormalized maximum absolute U-statistic centered by Delta and multiplied by square root n. It has no jackknife standard-error denominator.')
add('D24','bootstrap statistic',r'''
Therefore a valid bootstrap procedure is obtained as follows. Let $X_1^*,\ldots,X_n^*$ be drawn with replacement from $X_1,\ldots,X_n$ and recall definitions (2.19), (2.20) and (2.21). We then define the bootstrap statistic as
\[
\mathcal T_{n,\Delta}^{*,\mathrm{abs}}:=\sqrt n\max_{1\leq i\leq d}\{|U_i^*-V_i+V_{i,\Delta}|-|V_{i,\Delta}|\}\tag{2.31}
\]
and denote by $q_{1-\alpha}^{*,\mathrm{abs}}$ its $(1-\alpha)$ quantile.
''',[12],'Section 2.2 — absolute-value bootstrap statistic, equation (2.31)',{'D18':'The bootstrap uses the resampled U-statistics.','D19':'Each bootstrap coordinate is centered by its conditional mean V_i.','D20':'The mean is shifted into the null via V_i,Delta before taking absolute values.'},phrases=['bootstrap statistic'],symbols=[r'\mathcal T_{n,\Delta}^{*,\mathrm{abs}}',r'q_{1-\alpha}^{*,\mathrm{abs}}'],shape='Conditional absolute-value bootstrap maximum and its conditional quantile. The observed decision statistic in Theorem 2.8 is T_abs, not the starred statistic mistakenly printed in (2.32).')
add('D25','all tests',r'''
To be precise, we define
\[
\mathcal T_\alpha:=\{T_\alpha\mid\sup_{F\in\mathcal H_0(\Delta)}\mathbb P(T_\alpha\text{ does not reject }H_0)\leq\alpha\}
\]
as the set of all tests with (uniform) level $\alpha$.
''',[18],'Section 3.5 — purported uniform-level test class',{'D14':'The source test class takes a supremum over the composite null class H_0(Delta), including its stated assumptions.'},kind='condition',phrases=['all tests'],symbols=[r'\mathcal T_\alpha',r'\text{ does not reject }H_0'],shape='The exact source class uses a nonrejection probability under the null despite calling it level-alpha. This reverses the usual event and conflicts with the claimed lower bound; it is preserved and separately flagged.')
add('D26','covariance matrix',r'''
the covariance matrix $\Sigma=\operatorname{Cov}_F(X_1)=\mathbb E_F[(X_1-\mathbb E_F[X_1])(X_1-\mathbb E_F[X_1])^\top]$.
''',[15],'Section 3.1 — population covariance, defining excerpt',{'D1':'The covariance is that of the observation vector under F.'},phrases=['covariance matrix'],symbols=[r'\Sigma=\operatorname{Cov}_F(X_1)'],shape='Population covariance matrix. Theorem 3.5 uses off-diagonal entries as the dependence measure and explicitly sets all diagonal variances to one. The covariance kernel correspondence is archived separately; no jackknife or bootstrap estimator is needed for that lower-bound statement.')
members['D26']['application_context']=[dict(text=r'The covariance is a special case of (3.1) choosing $h(x_1,x_2)=(x_1-x_2)(x_1-x_2)^\top/2$,',evidence=[dict(page=15,location='Section 3.1 — covariance kernel')])]
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(interfaces),'source-backed interfaces; extraction remains in progress.')


if __name__ == "__main__":
    main()
