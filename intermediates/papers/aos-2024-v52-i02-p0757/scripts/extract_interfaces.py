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
add('D1','random object',r'''
To introduce and motivate these key notions, we assume that data and random objects of interest are situated in a totally bounded separable metric space $(\Omega,d)$. Consider a probability space $(S,\mathcal S,\mathbb P)$, where $S$ is a sample space, $\mathcal S$ is a sigma algebra of subsets of $S$, and $\mathbb P$ is a probability measure. A random object $X$ is an $\Omega$-valued random variable, i.e., a measurable map $X:S\to\Omega$ and $P$ is a Borel probability measure that governs the distribution of $X$, $X\sim P$, i.e., $P(A)=\mathbb P(\{s\in S:X(s)\in A\})=:\mathbb P(X\in A)=\mathbb P(X^{-1}(A))=:\mathbb PX^{-1}(A)$, for any Borel measurable $A\subseteq\Omega$.
''',[7],'Section 3 — random objects and the metric probability model',kind='source_passage',phrases=['random object'],symbols=[r'(\Omega,d)',r'X:S\to\Omega'],shape='Measurable random objects in a totally bounded separable metric space, with a Borel law P distinct from the underlying probability measure. Total boundedness is the standing Section 3 setting and supplies bounded distances, but does not imply completeness or compactness.')
add('D2','distance profile',r'''
For any $\omega\in\Omega$, let $F_\omega$ denote the cumulative distribution function (cdf) of the distribution of the distance between $\omega$ and a random element $X$ that is distributed according to $P$. In our notation, we suppress the dependence of $F_\omega$ on $P$ and $d$.

Formally, for any $t\geq0$, we define the distance profile at $\omega$ as
\[
F_\omega(t)=\mathbb P(d(\omega,X)\leq t),\tag{8}
\]
so that $F_\omega$ is a one-dimensional distribution that captures the probability mass enclosed by a metric ball in $\Omega$ that has center $\omega$ and radius $t$, for all $t\geq0$.
''',[7],'Section 3 — distance profile, equation (8)',{'D1':'The distance and probability law belong to the metric random-object model.'},phrases=['distance profile'],symbols=[r'F_\omega(t)',r'\mathbb P(d(\omega,X)\leq t)'],shape='The CDF of distance from a fixed anchor, using a closed ball. Its extension to t<0 is zero because distances are nonnegative. It is not the original object-valued distribution.')
members['D2']['application_context']=[dict(text=r'''Consider the distance profile $F_X$ of a random object $X\in\Omega$, $F_X(u)=\mathbb P_{X'}(d(X,X')\leq u)=\int_S\mathbb I(d(X,X'(s))\leq u)d\mathbb P(s)$, where $X'$ is an independent copy of $X$.''',evidence=[dict(page=8,location='Section 3 — random anchor and independent copy')])]
add('D3','strong negative type',r'''
if $(\Omega,d)$ is a metric space such that the kernel $K:\Omega\times\Omega\to\mathbb R$ given by $K(\omega,\omega')=d^\theta(\omega,\omega')$ for a $\theta>0$ is of strong negative type (Klebanov 2005; Lyons 2013). This means that for all Borel probability measures $P$ on $\Omega$ and all measurable functions $h:\Omega\to\mathbb R$ it holds that $\int_\Omega\int_\Omega K(\omega,\omega')h(\omega)h(\omega')dP(\omega)dP(\omega')\leq0$ with equality if and only if $h=0$ $P$-a.e. Equivalently, for all Borel probability measures $P_1,P_2$ on $\Omega$ one has
\[
\int_\Omega\int_\Omega K(\omega,\omega')dP_1(\omega)dP_1(\omega')
+\int_\Omega\int_\Omega K(\omega,\omega')dP_2(\omega)dP_2(\omega')-2\int_\Omega\int_\Omega K(\omega,\omega')dP_1(\omega)dP_2(\omega')\leq0,\tag{9}
\]
where equality holds if and only if $P_1=P_2$; for further discussion see Section 8.
''',[8],'Section 3 — strong negative type, equation (9)',{'D1':'The kernel and probability measures are on the given metric space.'},phrases=['strong negative type'],symbols=[r"K(\omega,\omega')=d^\theta(\omega,\omega')",r'\tag{9}'],shape='The source gives a powered-distance kernel and an energy inequality with equality characterizing identical probability measures. Its preceding claim for all h omits the usual mean-zero and integrability constraints and is not equivalent as printed. Theorem 4.1(d) invokes strong negative type of d itself; a property of some other distance power is not silently substituted.')
interfaces[-1]['lean_role']='predicate'
add('D4','transport ranks',r'''
This motivates the notion of transport ranks to measure centrality of an element $\omega\in\Omega$ with respect to $P$ as the expit of the expected integrated mass transfer when transporting $F_\omega$ to $F_X$, where $P=\mathbb PX^{-1}$. We use the expit function $\operatorname{expit}(x)=e^x/(1+e^x)$ in the definition of these ranks to ensure that the proposed ranks are scaled to lie in $(0,1)$; any strictly monotone invertible function from $\mathbb R$ to $[0,1]$ can be used for this purpose. Formally,
\[
R_\omega=\operatorname{expit}\left[\mathbb E\left\{\int_0^1[F_X^{-1}(u)-F_\omega^{-1}(u)]du\right\}\right].\tag{12}
\]
''',[9],'Section 3 — transport ranks, equation (12)',{'D2':'The integrated quantile difference uses the fixed-anchor profile F_omega and the profile at an independent-law random anchor X.'},phrases=['transport ranks'],symbols=[r'R_\omega',r'\operatorname{expit}(x)=e^x/(1+e^x)'],shape='A scalar logistic transform of the expected signed quantile integral. It is not a Wasserstein norm or a function of the threshold u. Generalized inverse convention is preserved in the auxiliary source record; bounded distances supply finite integrals.')
add('D5','transport median set',r'''
Equipped with an ordering of the elements of $\Omega$ by means of their transport ranks, we define the transport median set $\mathcal M_\oplus$ of $P$ as the collection of points in the support $\Omega_P\subset\Omega$ of $P$ which have maximal transport rank and are therefore most central,
\[
\mathcal M_\oplus=\operatorname*{argmax}_{\omega\in\Omega_P}R_\omega.\tag{13}
\]
''',[9],'Section 3 — transport median set, equation (13)',{'D4':'The set maximizes the population transport rank.','D1':'The maximization domain is the support of the object law P, not all of Omega.'},phrases=['transport median set'],symbols=[r'\mathcal M_\oplus',r'\Omega_P'],shape='The possibly set-valued population argmax over the support of P. Nonemptiness is explicitly assumed in Theorem 5.3; total boundedness alone does not ensure that the supremum is attained.')
add('D6','transport mode',r'''
Consider a situation where the distribution $P$ of $X$ concentrates around a point $\omega_\oplus\in\Omega$. Specifically, if there exists an element $\omega_\oplus\in\Omega$ such that
\[
F_{\omega_\oplus}(u)\geq F_\omega(u)\tag{14}
\]
for any $\omega\in\Omega$ and any $u\geq0$, we refer to $\omega_\oplus$ as an $\Omega$-valued transport mode of $P$.
''',[11],'Section 4 — transport mode, equation (14)',{'D2':'A transport mode dominates all anchor distance profiles at every nonnegative radius.'},phrases=['transport mode'],symbols=[r'F_{\omega_\oplus}(u)\geq F_\omega(u)'],shape='The source-defined all-radii stochastic dominance property for a distinguished anchor. It is not a density mode, and its existence is a separate hypothesis in parts (b)/(c) of Theorem 4.1.')
interfaces[-1]['lean_role']='predicate'
add('D7','empirical estimates',r'''
While so far we have introduced the notions of the distance profiles, transport ranks and transport median sets at the population level, in practice one needs to estimate these quantities from a data sample of random objects $\{X_i\}_{i=1}^n$ consisting of $n$ independent realizations of $X$. For obtain the distance profiles $F_\omega$, $\omega\in\Omega_P$ from a sample, we use empirical estimates
\[
\widehat F_\omega(t)=\frac1n\sum_{i=1}^n\mathbb I(d(\omega,X_i)\leq t),\qquad t\geq0,\tag{15}
\]
where $\mathbb I(A)$ is the indicator function for an event $A$.
''',[11,12],'Section 5 — empirical distance profiles, equation (15)',{'D2':'The empirical CDF estimates the anchor-specific population distance profile.','D1':'The observations are independent realizations under the same object law.'},phrases=['empirical estimates'],symbols=[r'\widehat F_\omega(t)',r'\frac1n\sum_{i=1}^n'],shape='Full-sample empirical distance CDF, defined initially for anchors in the support and nonnegative t. Theorem 5.1 uses the same formula for all Omega and real t. The random-anchor leave-one-out version used in the rank estimator is a distinct convention.')
add('D8','estimates for the transport rank',r'''
Replacing expectations with empirical means and using estimated distance profiles $\widehat F_{X_i}$ given by $\widehat F_{X_i}(t)=\frac1{n-1}\sum_{1\leq j\leq n,j\ne i}\mathbb I(d(X_j,X_i)\leq t)$ for $t\geq0$ as surrogates of $F_{X_i}$, we obtain estimates for the transport rank of $\omega\in\Omega$ defined in (12) as
\[
\widehat R_\omega=\operatorname{expit}\left[\frac1n\sum_{i=1}^n\left\{\int_0^1[\widehat F_{X_i}^{-1}(u)-\widehat F_\omega^{-1}(u)]du\right\}\right].\tag{16}
\]
''',[12],'Section 5 — empirical transport rank, equation (16)',{'D7':'The fixed-anchor term uses the full-sample empirical profile from (15), while the displayed random-anchor term explicitly removes the observation itself.','D4':'The estimator uses the same logistic transform and signed quantile-integral construction as the population transport rank.'},phrases=['estimates for the transport rank'],symbols=[r'\widehat R_\omega',r'\frac1{n-1}',r'\widehat F_{X_i}^{-1}(u)'],shape='Empirical signed-transport rank with leave-one-out random-anchor profiles and a full-sample fixed-anchor profile. The source overloads F-hat_Xi, so evaluation at an observed anchor requires retaining the two roles rather than replacing both by a common denominator.')
add('D9','estimated transport median set',r'''
Finally we define the estimated transport median set
\[
\widehat{\mathcal M}_\oplus=\operatorname*{argmax}_{\omega\in\{X_1,X_2,\ldots,X_n\}}\widehat R_\omega.\tag{17}
\]
''',[12],'Section 5 — estimated transport median set, equation (17)',{'D8':'The empirical median maximizes the empirical transport rank.','D7':'Its search domain is the observed finite sample, not the full metric space.'},phrases=['estimated transport median set'],symbols=[r'\widehat{\mathcal M}_\oplus'],shape='Finite-sample argmax over observed objects, retaining all maximizing points and allowing repeated observations without inventing a tie-breaker.')
add('D10','metric entropy',r'''
Let $N(\varepsilon,\Omega,d)$ be the covering number of the space $\Omega$ with balls of radius $\varepsilon$ and $\log N(\varepsilon,\Omega,d)$ the corresponding metric entropy. Then
\[
\varepsilon\log N(\varepsilon,\Omega,d)\to0\quad\text{as}\quad\varepsilon\to0.\tag{18}
\]
''',[12],'Assumption 1',{'D1':'The covering number concerns the original object metric space.'},kind='assumption',phrases=['metric entropy','Assumption 1'],symbols=[r'\varepsilon\log N(\varepsilon,\Omega,d)'],shape='Small-scale entropy restriction on metric covering numbers, with radius epsilon tending to zero. It is a property of the space, distinct from a generic empirical-process Donsker conclusion.')
add('D11','density',r'''
For every $\omega\in\Omega$, $F_\omega$ is absolutely continuous with continuous density $f_\omega$. For $\underline\Delta_\omega=\inf_{t\in\operatorname{support}(f_\omega)}f_\omega(t)$ and $\overline\Delta_\omega=\sup_{t\in\mathbb R}f_\omega(t)$, $\underline\Delta_\omega>0$ for each $\omega\in\Omega$ and there exists $\Delta>0$ such that $\sup_{\omega\in\Omega}\overline\Delta_\omega\leq\Delta$.
''',[12],'Assumption 2',{'D2':'The smoothness and density bounds apply to every distance profile.'},kind='assumption',phrases=['density','Assumption 2'],symbols=[r'\underline\Delta_\omega',r'\overline\Delta_\omega',r'f_\omega'],shape='Continuous profile densities with an anchorwise positive lower bound on their support and one uniform upper bound. The lower bound is not uniform over anchors. Literal global continuity and a positive infimum over support are problematic at finite support boundaries; that source convention is not repaired.')
add('D12','function class',r'''
For functions $y_{\omega,t}:\Omega\to\mathbb R$ with $y_{\omega,t}(x)=\mathbb I\{d(\omega,x)\leq t\}$ and the function class $\mathcal F=\{y_{\omega,t}:\omega\in\Omega,t\in\mathbb R\}$,
''',[12],'Section 5 — closed-ball indicator function class',{'D1':'The class consists of metric-ball indicators on the object space.'},phrases=['function class'],symbols=[r'y_{\omega,t}(x)=\mathbb I\{d(\omega,x)\leq t\}',r'\mathcal F'],shape='Indicators indexed by anchor and radius, including negative radii as empty events. The following Donsker assertion is the result of Theorem 5.1, not an additional assumed property.')
add('D13','Hausdorff metric',r'''
\[
\rho_H(\widehat{\mathcal M}_\oplus,\mathcal M_\oplus)=\max\left(\sup_{\omega\in\widehat{\mathcal M}_\oplus}d(\omega,\mathcal M_\oplus),\sup_{\omega\in\mathcal M_\oplus}d(\omega,\widehat{\mathcal M}_\oplus)\right),\tag{19}
\]
where for any $\omega\in\Omega$ and any subset $A\subset\Omega$, $d(\omega,A)=\inf_{s\in A}d(\omega,s)$.
''',[13],'Section 5 — Hausdorff distance between median sets, equation (19)',{'D5':'One set is the population median argmax over the support.','D9':'The other is the empirical argmax over the observed sample.'},context=r'To conclude this section we consider the convergence of the estimated transport median set $\widehat{\mathcal M}_\oplus$ to $\mathcal M_\oplus$ in the Hausdorff metric',phrases=[],symbols=[r'\rho_H',r'd(\omega,A)=\inf_{s\in A}d(\omega,s)'],shape='The maximum of both directed distances between the two median sets, using infimum point-to-set distance. No one-sided set convergence is substituted for this printed Hausdorff statement.')
add('D14','identifiability of transport medians',r'''
For some $\eta'>0$, for any $0<\varepsilon<\eta'$,
\[
\alpha(\varepsilon)=\inf_{\widetilde\omega\in\mathcal M_\oplus}\inf_{d(\omega,\widetilde\omega)>\varepsilon}|R_\omega-R_{\widetilde\omega}|>0.
\]
''',[14],'Assumption 3',{'D5':'The outer infimum is over every population median.','D4':'The strict separation is a gap in population transport rank.'},kind='assumption',context='Assumption 3 deals with the identifiability of transport medians and stipulates that the transport median set is a union of single point sets which are separated from each other by a minimum fixed distance.',phrases=['Assumption 3'],symbols=[r'\alpha(\varepsilon)',r'\inf_{d(\omega,\widetilde\omega)>\varepsilon}'],shape='Literal positive rank gap outside each individual median’s epsilon ball. The source prose describes separated multiple medians, but the formula excludes any pair of distinct medians when epsilon is smaller than their distance. It is not rewritten as separation from the entire median set.')
add('D15','Two-sample testing',r'''
Assume that $X_1,X_2,\ldots,X_n$ is a sample of random objects taking values in $\Omega$, generated according to a Borel probability measure $P_1$ on $\Omega$, and that $Y_1,Y_2,\ldots,Y_m$ is another sample of $\Omega$-valued random objects generated analogously according to a Borel probability measure $P_2$. Two-sample testing in this setting concerns the null (20) and alternative (21) hypotheses
\[
H_0:P_1=P_2\tag{20}
\]
\[
H_1:P_1\ne P_2.\tag{21}
\]
We require some notations. For $\omega\in\Omega$, the distance profile of $\omega$ with respect to $X\sim P_1$ and $Y\sim P_2$ respectively are given by $F^X_\omega(\cdot)$ and $F^Y_\omega(\cdot)$, where for $u\in\mathbb R$,
\[
F^X_\omega(u)=\mathbb P(d(x,X)\leq u)\quad\text{and}\quad F^Y_\omega(u)=\mathbb P(d(x,Y)\leq u).\tag{22}
\]
''',[14],'Section 6.1 — two-sample model and profiles, equations (20)-(22)',{'D1':'Both samples take values in the same metric random-object space.','D2':'The two population profiles specialize the anchor-distance CDF to the two object laws.'},kind='source_passage',phrases=['Two-sample testing'],symbols=[r'H_0:P_1=P_2',r'F^X_\omega(u)',r'F^Y_\omega(u)'],shape='Two Borel laws on one metric space and their anchor-distance CDFs. Equation (22) literally uses x inside the distance despite indexing the CDF by omega; the mismatch is retained. The intervening literature-comparison paragraph is omitted, with the two source passages joined explicitly below.')
members['D15']['statement_original']=members['D15']['statement_original'].replace('We require some notations.','[Separate source passage.]\n\nWe require some notations.')
add('D16',['in-sample distance profiles','out-of-sample distance profiles'],r'''
Let $\widehat F^X_{X_1}(\cdot),\widehat F^X_{X_2}(\cdot),\ldots,\widehat F^X_{X_n}(\cdot)$ be the estimated in-sample distance profiles of $X_1,\ldots,X_n$, respectively, with respect to the observations from $P_1$, i.e.,
\[
\widehat F^X_{X_i}(u)=\frac1{n-1}\sum_{j\ne i}\mathbb I(d(X_i,X_j)\leq u).
\]
Then we obtain the out-of-sample distance profiles of $X_1,\ldots,X_n$, respectively, with respect to the observations from $P_2$, given by $\widehat F^Y_{X_1}(\cdot),\widehat F^Y_{X_2}(\cdot),\ldots,\widehat F^Y_{X_n}(\cdot)$, where
\[
\widehat F^Y_{X_i}(u)=\frac1m\sum_{j=1}^m\mathbb I(d(X_i,Y_j)\leq u).
\]
Similarly we estimate the in-sample and the out-of-sample distance profiles of $Y_1,\ldots,Y_m$ with respect to the observations from $P_2$ and $P_1$, respectively, given by $\widehat F^Y_{Y_1}(\cdot),\widehat F^Y_{Y_2}(\cdot),\ldots,\widehat F^Y_{Y_m}(\cdot)$ and $\widehat F^X_{Y_1}(\cdot),\widehat F^X_{Y_2}(\cdot),\ldots,\widehat F^X_{Y_m}(\cdot)$ respectively, where for $u\geq0$
\[
\widehat F^Y_{Y_j}(u)=\frac1{m-1}\sum_{j\ne i}\mathbb I(d(Y_j,Y_i)\leq u)
\]
and
\[
\widehat F^X_{Y_j}(u)=\frac1n\sum_{i=1}^n\mathbb I(d(Y_j,X_i)\leq u).
\]
''',[14,15],'Section 6.1 — four empirical distance profiles',{'D15':'The four empirical profiles use the two samples from P1 and P2, with the anchor observation excluded only for a within-sample profile.'},phrases=['in-sample distance profiles','out-of-sample distance profiles'],symbols=[r'\frac1{n-1}',r'\frac1{m-1}'],shape='Four explicitly distinguished empirical distance CDFs. Within-sample profiles use n-1 or m-1 observations; cross-sample profiles use the entire opposite sample. The source sum written j not equal i in the Y_j profile is preserved; the free anchor is j and the intended summation variable is i.')
add('D17','weighted test statistic',r'''
To enhance flexibility, we also consider a generalized weighted version of the test statistic, where for each observation $X_i$ or $Y_i$, we allow for data adaptive weight profiles $\widehat w_{X_i}(\cdot)$ and $\widehat w_{Y_i}(\cdot)$ that can be tuned appropriately to enhance the detection capacity of the test statistic. This leads to weighted versions of $T^X_{nm}$ and $T^Y_{nm}$,
\[
T^{X,w}_{nm}(X,Y)=\frac1n\sum_{i=1}^n\int\widehat w_{X_i}(u)\{\widehat F^X_{X_i}(u)-\widehat F^Y_{X_i}(u)\}^2du
\]
and
\[
T^{Y,w}_{nm}(X,Y)=\frac1m\sum_{i=1}^m\int\widehat w_{Y_i}(u)\{\widehat F^X_{Y_i}(u)-\widehat F^Y_{Y_i}(u)\}^2du
\]
and the weighted test statistic
\[
T^w_{nm}(X,Y)=\frac{nm}{n+m}\{T^{X,w}_{nm}+T^{Y,w}_{nm}\}.\tag{24}
\]
Note that the test statistic in equation (23) is a version of the generalized test statistic in equation (24) with $\widehat w_{X_i}(\cdot)=\widehat w_{Y_i}(\cdot)\equiv1$.
''',[15],'Section 6.1 — weighted test statistic, equation (24)',{'D16':'The two integrated squared differences use the four empirical profiles, retaining the distinct within-sample denominators.'},phrases=['weighted test statistic','data adaptive weight profiles'],symbols=[r'T^w_{nm}(X,Y)',r'\frac{nm}{n+m}'],shape='The harmonic-size-scaled sum of two sample averages of weighted squared profile differences, integrated against du. The weight functions are inputs; their regularity is separately assumed by Assumption 4, not part of the bare definition. Unit weights recover (23).')
add('D18','weight profiles',r'''
For each $x\in\Omega$, there exists a population limit of the estimated weight profiles such that (25) is satisfied; there exists $C_w>0$ such that $\sup_{x\in\Omega}\sup_u|w_x(u)|\leq C_w$; for some $L_w>0$ it holds that $\sup_{x\in\Omega}|w_x(u)-w_x(v)|\leq L_w|u-v|$.
''',[17],'Assumption 4',{'D1':'The uniform weight conditions range over all anchors in the original object space.'},kind='assumption',phrases=['weight profiles','Assumption 4'],symbols=[r'|w_x(u)|\leq C_w',r'L_w|u-v|'],shape='Uniform stochastic convergence of estimated weights to population weights, uniform boundedness, and a common Lipschitz constant. Equation (25) is included verbatim in the application context. The printed assumption does not impose nonnegative weights, despite the later covariance and chi-square representation.')
members['D18']['application_context']=[dict(text=r'''Suppose that for each $x\in\Omega$, there exists a population limit of the estimated data adaptive weight profile $\widehat w_x(\cdot)$ given by $w_x(\cdot)$ such that
\[
\sup_{x\in\Omega}\sup_u|\widehat w_x(u)-w_x(u)|=o_{\mathbb P}(1).\tag{25}
\]''',evidence=[dict(page=15,location='Equation (25) — weight convergence referenced by Assumption 4')])]
add('D19','densities',r'''
For each $x\in\Omega$, $X\sim P_1$ and $Y\sim P_2$, $F^X_x(t)=\mathbb P(d(x,X)\leq t)$ and $F^Y_x(t)=\mathbb P(d(x,Y)\leq t)$ are absolutely continuous, with densities $f^X_x(t)$ and $f^Y_x(t)$, respectively, that satisfy $\inf_{t\in\operatorname{supp}(f^X_x)}f^X_x(t)>0$, $\inf_{t\in\operatorname{supp}(f^Y_x)}f^Y_x(t)>0$. There exist $L_X,L_Y>0$ such that $\sup_{x\in\Omega}\sup_{t\in\mathbb R}|f^X_x(t)|\leq L_X$ and $\sup_{x\in\Omega}\sup_{t\in\mathbb R}|f^Y_x(t)|\leq L_Y$.
''',[17],'Assumption 5',{'D15':'These two density restrictions apply to the profile laws under P1 and P2 separately.'},kind='assumption',phrases=['densities','Assumption 5'],symbols=[r'f^X_x(t)',r'f^Y_x(t)'],shape='Absolute continuity of both population profiles, anchorwise strictly positive lower bounds on their density supports, and separate uniform upper bounds. Unlike Assumption 2, this statement does not explicitly require continuous densities. The lower bound is not uniform in x.')
add('D20','sample sizes',r'''
There exists $0<c<1$ such that sample sizes $n$ and $m$ satisfy $n/(n+m)\to c$ as $n,m\to\infty$.
''',[17],'Assumption 6',{'D15':'The two sizes refer to the P1 and P2 samples of the two-sample model.'},kind='assumption',phrases=['sample sizes','Assumption 6'],symbols=[r'0<c<1',r'n/(n+m)\to c'],shape='Both sample groups have nonvanishing limiting proportions. This first-order balance is separate from the root-total-size accuracy additionally imposed in the final clause of Theorem 6.3.')
add('D21','weight profile dependent quantities',r'''
The weight profile dependent quantities
\[
D^w_{XY}(P_1,P_2)=\mathbb E\left\{\int w_{X'}(u)(F^X_{X'}(u)-F^Y_{X'}(u))^2du\right\}
+\mathbb E\left\{\int w_{Y'}(u)(F^X_{Y'}(u)-F^Y_{Y'}(u))^2du\right\},\tag{26}
\]
where $F^X_\omega(\cdot)$ and $F^Y_\omega(\cdot)$ are as defined in equation (22) and $X'\sim P_1$ and $Y'\sim P_2$ capture the population version of the proposed test statistic (24).
''',[16],'Section 6.1 — population weighted discrepancy, equation (26)',{'D15':'The integrands compare the two population distance profiles at anchors drawn from their respective object laws.'},phrases=['weight profile dependent quantities'],symbols=[r'D^w_{XY}(P_1,P_2)'],shape='Sum of two population expectations of integrated weighted squared profile differences. The function family w is supplied as an input, while Assumption 4 separately constrains it. Identifying zero discrepancy with equality of object laws requires extra conditions discussed after (26); these are not imported into the definition or all of Theorems 6.1-6.3.')
add('D22','sequence of alternatives',r'''
To study the asymptotic power of the proposed test, we consider a sequence of alternatives
\[
H_{nm}=\{(P_1,P_2):X\sim P_1,Y\sim P_2,\tag{29}
\]
\[
\text{with }D^w_{XY}=a_{nm},\ a_{nm}\to0,\ nm/(n+m)a_{nm}\to\infty,\ n,m\to\infty\},
\]
with $D^w_{XY}$ as in (26). The $\{H_{nm}\}$ form a sequence of contiguous alternatives shrinking towards $H_0$.
''',[17],'Section 6.2 — alternatives, equation (29)',{'D21':'The alternatives are specified by the population discrepancy (26), including its local magnitude a_nm.','D15':'The pairs are the two object laws and the target null is their equality.'},phrases=['sequence of alternatives'],symbols=[r'H_{nm}',r'nm/(n+m)a_{nm}\to\infty'],shape='Discrepancy shrinks to zero but exceeds the inverse effective sample size by a divergent factor. The source calls this contiguous; no separate Le Cam contiguity assertion is inferred from that terminology.')
add('D23','covariance surface',r'''
a random variable $L=2\sum_{j=1}^\infty Z_j^2\mathbb E_V(\lambda_j^V)$, where $Z_1,Z_2,\ldots$ is a sequence of i.i.d. $N(0,1)$ random variables, $V\sim P$ where $P=P_1=P_2$ under $H_0$ and for any $x\in\Omega$, $\lambda_1^x\geq\lambda_2^x\geq\ldots$ are the eigenvalues of the covariance surface given by
\[
C^x(u,v)=\sqrt{w_x(u)w_x(v)}\operatorname{Cov}(\mathbb I(d(x,V')\leq u),\mathbb I(d(x,V')\leq v))
\]
with $V'\sim P$.
''',[17],'Theorem 6.1 — inline definition of the null limit law',{'D15':'The null law identifies P1 and P2 and evaluates distance-ball indicators under their common law.'},kind='theorem_excerpt',phrases=['covariance surface'],symbols=[r'L=2\sum_{j=1}^\infty Z_j^2\mathbb E_V(\lambda_j^V)',r'C^x(u,v)'],shape='The literal inline random-series definition uses twice the averaged pointwise eigenvalues and independent squared standard normals. The text does not specify the operator space or base measure defining these covariance eigenvalues. This excerpt defines the object used in subsequent results; it does not import a proof of Theorem 6.1 or add positivity to Assumption 4.')
add('D24','asymptotic critical value',r"""
To obtain the asymptotic power of the test, we work with $q_\alpha$, the asymptotic critical value for rejecting $H_0$, where $q_\alpha=\inf\{t:\Gamma_L(t)\geq1-\alpha\}$ and $\Gamma_L(\cdot)$ is the cumulative distribution function of the asymptotic null distribution corresponding to the law of $L$ (see Theorem 6.1).
""",[16],'Section 6.1 — asymptotic null critical value',{'D23':'The cutoff is the upper alpha quantile of the null random-series law.'},phrases=['asymptotic critical value'],symbols=[r'q_\alpha',r'\Gamma_L'],shape='The generalized inverse quantile of the null-law CDF at 1-alpha, with an unrestricted real infimum domain. It is distinct from the empirical permutation cutoff and the mixture-reference cutoff; defining it does not require an alternative sequence or a power calculation.')
add('D25','random permutation scheme',r'''
Let $\Pi_{nm}$ denote the collection of all $(n+m)!$ permutations of $\{1,2,\ldots,n+m\}$ and $\Pi$ a random variable that follows a uniform distribution on $\Pi_{nm}$ and is independent of the observations $X_1,\ldots,X_n$ and $Y_1,\ldots,Y_m$. Let $V_1,V_2,\ldots,V_{n+m}$ denote the pooled sample where $V_i=X_i$ if $i\leq n$ and $V_i=Y_{i-n}$ if $i\geq n+1$. Let $\Pi_1,\Pi_2,\ldots,\Pi_K$ denote i.i.d. replicates of $\Pi$. Each $\Pi_j=(\Pi_j(1),\ldots,\Pi_j(n+m))$ is a random permutation of $\{1,2,\ldots,n+m\}$ and when applied to the data yields $V_{\Pi_j}=\{V_{\Pi_j(1)},V_{\Pi_j(2)},\ldots,V_{\Pi_j(n+m)}\}$, $j=1,\ldots,K$, which constitute a collection of randomly permuted pooled data. For each $j=1,\ldots,K$, split the data $V_{\Pi_j}$ into $X_{\Pi_j}=\{V_{\Pi_j(1)},V_{\Pi_j(2)},\ldots,V_{\Pi_j(n)}\}$ and $Y_{\Pi_j}=\{V_{\Pi_j(n+1)},V_{\Pi_j(2)},\ldots,V_{\Pi_j(n+m)}\}$. With $X_{\Pi_j}$ and $Y_{\Pi_j}$ being the proxies for the two samples of sizes $n$ and $m$, respectively, evaluate the test statistic replicates $T_{\Pi_j}=T^w_{nm}(X_{\Pi_j},Y_{\Pi_j})$. Define $\widehat\Gamma_{nm}(\cdot)$ as
\[
\widehat\Gamma_{nm}(t)=\frac1K\sum_{j=1}^K\mathbb I(T_{\Pi_j}\leq t),\tag{27}
\]
which approximates the randomization distribution of $T^w_{nm}$ using the random permutations $\Pi_1,\Pi_2,\ldots,\Pi_K$. Then a natural estimate of $q_\alpha$ is
\[
\widehat q_\alpha=\inf\{t:\widehat\Gamma_{nm}(t)\geq1-\alpha\}.\tag{28}
\]
''',[16],'Section 6.1 — permutation distribution and critical value, equations (27)-(28)',{'D15':'The pooled observations are the two original samples.','D17':'Each permuted replicate evaluates the weighted statistic on the regrouped observations.'},context=r'we estimate $q_\alpha$ using a random permutation scheme in practice, as follows.',phrases=['equations (27)-(28)'],symbols=[r'\widehat\Gamma_{nm}(t)',r'\widehat q_\alpha'],shape='Monte Carlo permutation CDF from K independent uniform permutations, and its upper-alpha generalized inverse. The second displayed entry of Y_Pi_j is literally V_Pi_j(2), not V_Pi_j(n+2); this inconsistent split is preserved and separately flagged. Re-evaluation is expressed as the same statistic functional, not a fixed-weight shortcut.')
add('D26','mixture distribution',r'''
under alternatives $P_1\ne P_2$ we consider a mixture distribution $\overline P=cP_1+(1-c)P_2$ with $0\leq c\leq1$. Assume $\overline X=\{\overline X_1,\ldots,\overline X_n\}$ and $\overline Y=\{\overline Y_1,\ldots,\overline Y_m\}$ are i.i.d. samples from $\overline P$ and $T^w_{nm}(\overline X,\overline Y)$ is the test statistic obtained using the samples $\overline X$ and $\overline Y$. We show in the proof of Theorem 6.3 in the Supplement that under Assumptions 1, 4, 5 and 6, Theorem 6.1 can be utilized to obtain the asymptotic distribution of $T^w_{nm}(\overline X,\overline Y)$ with cumulative distribution $\overline\Gamma_L(\cdot)$ and $\overline q_\alpha=\inf\{t\geq0:\overline\Gamma_L(t)\geq1-\alpha\}$.
''',[17,18],'Section 6.2 — mixture reference law and quantile',{'D15':'The pooled reference law mixes the two original object laws.','D17':'The reference statistic applies the same functional to two independent samples from the mixture.','D23':'The referenced limiting CDF is obtained by applying the Theorem 6.1 law to that common mixture distribution.'},kind='source_passage',phrases=['mixture distribution'],symbols=[r'\overline P=cP_1+(1-c)P_2',r'\overline\Gamma_L',r'\overline q_\alpha'],shape='Mixture reference distribution, the common-law statistic and its limiting CDF and quantile. The source explicitly restricts the quantile infimum to t>=0 here, unlike the oracle and empirical quantiles. Only this main-text definition and assertion is recorded; the referenced supplement proof is excluded.')
add('D27','power function',r'''
\[
\widetilde\beta^w_{nm}=\mathbb P_{H_{nm}}(T^w_{nm}>\widehat q_\alpha)\tag{31}
\]
is the power function of the test under the sequence of the contiguous alternatives $H_{nm}$ when using the permutation-derived critical value $\widehat q_\alpha$ instead of $q_\alpha$.
''',[18],'Section 6.2 — permutation power, equation (31)',{'D17':'The event uses the same weighted test statistic.','D22':'The alternative sequence is the discrepancy-defined H_nm.','D25':'The rejection cutoff is the estimated quantile of the permutation CDF.'},phrases=['power function'],symbols=[r'\widetilde\beta^w_{nm}',r'\widehat q_\alpha'],shape='Rejection probability with the random permutation cutoff under H_nm. This is distinct from the oracle-cutoff power in (30), even though the alternative sequence and test statistic are the same.')
add('D28','power',r'''
The power of the test under this sequence is
\[
\beta^w_{nm}=\mathbb P_{H_{nm}}(T^w_{nm}>q_\alpha),\tag{30}
\]
where $q_\alpha=\inf\{t:\Gamma_L(t)\geq1-\alpha\}$ and $\Gamma_L(\cdot)$ is the cumulative distribution function of the asymptotic null distribution corresponding to the law of $L$ in Theorem 6.1.
''',[17],'Section 6.2 — oracle critical value and power, equation (30)',{'D17':'The rejection event compares the weighted sample statistic with an oracle cutoff.','D22':'The probability is under the stipulated shrinking alternatives.','D24':'The rejection threshold is the oracle null critical value, with its CDF and quantile convention defined in Section 6.1.'},phrases=['power'],symbols=[r'\beta^w_{nm}',r'q_\alpha=\inf\{t:\Gamma_L(t)\geq1-\alpha\}'],shape='Strict-exceedance rejection power under H_nm and the generalized inverse quantile of the null-law CDF. The source probability over a composite alternative is not explicitly defined as an infimum or supremum, so no minimax or uniform-power convention is silently imposed.')
# Source-inspected selector amendment; original statements are unchanged.
members['D3']['highlight_symbols'] = ["K(\\omega,\\omega')=d^\\theta(\\omega,\\omega')"]
members['D3']['highlight_phrases'] = ['strong negative type', '(9)']

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source interfaces.')


if __name__ == "__main__":
    main()
