"""Preserve original regular-variation, estimator and Gaussian-limit passages."""
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
add(1,'regularly varying',r'''is regularly varying with index 1 and satisfies
\[
a^*(u)\mathbb P(u^{-1}X^*\in\cdot)\xrightarrow{v}\mu^*(\cdot),\qquad u\to\infty,
\]
(2)
for some normalized exponent measure $\mu^*$ which is homogeneous of order $-1$''',[3],[],[r'a^*(u)\mathbb P(u^{-1}X^*\in\cdot)',r'\mu^*'],'The regular-variation clause for X* with index1, a scaling function a* and homogeneous exponent measure mu*. Standardized marginal normalization is separately Eq3. The source’s E includes the origin although the usual vague-convergence domain needs an origin-exclusion or equivalent cone convention; retain this issue. No non-standard model is required merely to state regular variation of X*.','Section 2 — Regular variation (2)',kind='source_passage')
add(2,'normalized exponent measure',r'''\[
\mu^*(\{x\in E:x_i>1\})=\lim_{u\to\infty}a^*(u)\mathbb P(X_i^*>u)=1,
\]
(3)
i.e. $a^*(u)\sim\mathbb P(X_i^*>u)^{-1}$ for all $i=1,\ldots,d$.''',[3],[1],[r'\mu^*(\{x\in E:x_i>1\})',r'\mathbb P(X_i^*>u)^{-1}'],'Unit marginal tail normalization for every coordinate, with a* asymptotic to the reciprocal tail probability. This is not an assumption of exactly Pareto finite-threshold margins.','Section 2 — Marginal normalization (3)',kind='assumption',context=r'for some normalized exponent measure $\mu^*$ which is homogeneous of order $-1$ and')
add(3,'spectral component',r'''Eq. (2) can be equivalently expressed in terms of a spectral component for an arbitrary norm $\|\cdot\|$ on $\mathbb R^d$. More precisely, we obtain the weak convergence
\[
\mathcal L(u^{-1}X^*\mid\|X^*\|>u)\xrightarrow{w}\mathcal L(Y\Theta),\qquad u\to\infty,
\]
(5)
where $Y$ is a unit Pareto random variable and, independently from $Y$, $\Theta$ is a $[0,\infty)^d$-valued random vector satisfying $\|\Theta\|=1$ almost surely, i.e.
\[
\mathbb P(\Theta\in S^+_{d-1})=1,\qquad\text{where }S^+_{d-1}=\{x\in[0,\infty)^d:\|x\|=1\}.
\]
In the following, we will focus on the maximum norm $\|\cdot\|=\|\cdot\|_\infty$ which is not a serious restrictions as all norms on $\mathbb R^d$ are equivalent.''',[3],[1],[r'\mathcal L(Y\Theta)',r'S^+_{d-1}',r'\|\cdot\|=\|\cdot\|_\infty'],'Probability spectral law on the nonnegative maximum-norm sphere, coupled with an independent unit-Pareto radial variable. The same Y and Theta occur in the two factors of Theorem5’s covariance. The probability spectral measure is distinct from the exponent measure and its total scale tau.','Section 2 — Spectral component and Pareto radial limit (5)')
add(4,'extremal coefficient',r'''\[
\tau=\mu^*(\{x\in E:\|x\|>1\})=\lim_{u\to\infty}a^*(u)\mathbb P(\|X^*\|>u).
\]
(7)''',[3],[1],[r'\tau=\mu^*',r'\mathbb P(\|X^*\|>u)'],'Global maximum-norm extremal coefficient. The main-text normalization gives 1≤tau≤d; it multiplies the probability spectral expectation, and is not absorbed into the law of Theta. It is the full-coordinate case of tau_I.','Section 2 — Global extremal coefficient (7)',context=r'One of the most popular summary statistics for the extremal dependence of the (sub-)vector $(X_i^*)_{i\in I}$ is the extremal coefficient $\tau_I$ given by Eq. (13), i.e.',context_page=11)
add(5,'convex combinations',r'''$v\in\partial B_1^+(0)=\partial B_1(0)\cap[0,\infty)^d$, i.e. we consider only convex combinations of components of $X^*$ with positive coefficients, while allowing for arbitrary powers of these combinations.''',[4],[],[r'\partial B_1^+(0)',r'\partial B_1(0)\cap[0,\infty)^d'],'Nonnegative l1-unit simplex; zero coefficients are permitted by the printed set despite the word positive. The preceding definition is partial B1={x in R^d:||x||1=1}. Masking v outside I does not renormalize its remaining coordinates.','Section 2 — Nonnegative convex-combination weights')
members['D5']['naming_context']=[dict(context_id='D5/domain',text=r'$v\in\partial B_1(0)=\{x\in\mathbb R^d:\|x\|_1=1\}$',evidence=[dict(page=4,location='l1-unit boundary in the paragraph following (9)')])]
add(6,'functional',r'''spectral vectors are often normalized w.r.t. some less complex functional $\ell_I(x)=\bigvee_{i\in I}x_i$ over some smaller subset $I\subset\{1,\ldots,d\}$.''',[5],[],[r'\ell_I(x)=\bigvee_{i\in I}x_i'],'Coordinate maximum over the nonempty subset I. It is positively homogeneous but not a norm on all d coordinates for a proper subset. The theorems and estimators restrict I to nonempty sets.','Section 2 — Subset-maximum functional')
add(7,'weight vectors',r'''we will consider weight vectors $v_I$ where $v_I$ is the vector with components $v_i$ for $i\in I$ and 0 otherwise. Thus, we obtain $v_I^\top X^*=\sum_{i\in I}v_iX_i^*$.''',[6],[],[r'v_I',r'\sum_{i\in I}v_iX_i^*'],'Coordinate masking, with no rescaling to restore unit l1 norm. The associated indicator vector 1_I and all-ones vector1 are preserved in additional original source context.','Section 3.1 — Coordinate-masked weights')
members['D7']['naming_context']=[dict(context_id='D7/indicator',text=r'where $\mathbf1=(1,\ldots,1)\in\mathbb R^d$, i.e., according to the notation introduced above, $\mathbf1_I$ is the vector with the $i$th component being equal to 1 if $i\in I$ and being equal to 0 otherwise. Furthermore, $v_I^\top X^*=v^\top(\mathbf1_I\circ X^*)$.',evidence=[dict(page=7,location='Indicator-vector convention before (22)')])]
add(8,'extremal coefficient',r'''\[
\tau_I=\mu^*(\{x\in E:\ell_I(x)>1\})=\lim_{u\to\infty}a^*(u)\mathbb P(\ell_I(X^*)>u)
\]
(13)
exists and by Eq. (2) equals $\mu^*(\{x\in E:\ell_I(x)>1\})$, and for every $I\ne\emptyset$ it satisfies the relation
\[
\tau_I=\mathbb E[\ell_I(\Theta)]\cdot\tau\in[1,|I|].
\]
(14)''',[5],[1,3,4,6],[r'\tau_I',r'\mathbb E[\ell_I(\Theta)]\cdot\tau'],'Subset extremal coefficient, with tau_ij denoting the pair {i,j}. It is distinct from tau for all coordinates. In Theorem8 its pair specialization appears in the Hill covariance.','Section 2 — Subset extremal coefficient (13)–(14)',context=r'One of the most popular summary statistics for the extremal dependence of the (sub-)vector $(X_i^*)_{i\in I}$ is the extremal coefficient $\tau_I$ given by Eq. (13), i.e.',context_page=11)
add(9,'spectral vector',r'''Using the property $\mathbb E[\ell_I(\Theta)]>0$ for every $I\ne\emptyset$, we can study the behavior of the $\ell_I$-spectral vector $\Theta^I$ whose distribution can be defined from the original spectral measure via the relation
\[
\mathbb P(\Theta^I\in A)=\frac1{\mathbb E[\ell_I(\Theta)]}\int_{[0,\infty)^d}\mathbf1\{\theta/\ell_I(\theta)\in A\}\ell_I(\theta)\mathbb P(\Theta\in d\theta),
\]
(15)
where $A\subset\{w\in[0,\infty)^d:\ell_I(w)=1\}$.''',[5],[3,6],[r'\Theta^I',r'\ell_I(\theta)\mathbb P(\Theta\in d\theta)'],'Angular law tilted by ell_I(Theta) before rescaling, not the distribution of Theta/ell_I(Theta) under the original probability. Only the I coordinates are used in the specialized Gaussian covariance. Zero-weight angles require an implicit convention for the otherwise undefined rescaling.','Section 2 — Subset-normalized spectral law (15)')
add(10,'perturbed vector',r'''In the following, let $(s\circ X^*)^{1/\beta}=(s_i^{1/\beta_i}X_i^{*1/\beta_i})_{1\le i\le d}$.
More precisely, we consider $s\in A_{\delta,I}$ and $\beta\in[(1+\delta)^{-1},1+\delta]^d$ where
\[
A_{\delta,I}=\{x\in(0,\infty)^d:x_i=0\text{ for all }i\notin I,\ (1+\delta)^{-1}\le x_i\le1+\delta\text{ for all }i\in I\}
\]
for some $\delta\ge0$, i.e. we allow for a perturbation of a factor and a power between $(1+\delta)^{-1}$ and $1+\delta$ in each component of $s$ and in each component of $\beta$. We also denote the disjoint unions
\[
A_\delta=\bigcup_{\emptyset\ne I\subset\{1,\ldots,d\}}A_{\delta,I}\qquad\text{and}\qquad A'_\delta=\bigcup_{\emptyset\ne I\subset\{1,\ldots,d\}}A_{\delta,I}\times[(1+\delta)^{-1},1+\delta]^d.
\]''',[7],[],[r'A_{\delta,I}',r"A'_\delta",r'(s\circ X^*)^{1/\beta}'],'Componentwise scaling and positive coordinate powers, with stratified support domain. The source prints (0,infinity)^d together with zero off I, making proper-support strata empty literally. Preserve this inconsistency rather than silently replacing the orthant. Theorem10 derivative domains and masked weights require additional interpretation recorded separately.','Section 3.1 — Perturbations and index domains',context=r'In our extended version of the functional central limit theorem, we will not restrict our attention to the vector $\mathbf1_I\circ X^*$ being extreme, but allow for a perturbed vector $(s\circ X^*)^{1/\beta}$ with $s$ being close to $\mathbf1_I$ and $\beta$ being close to $\mathbf1$.')
add(11,'generalized estimator',r'''Replacing $\mathbf1_I\circ X^*/u$ in Eq. (22) by $(s\circ X^*/u)^{1/\beta}$, we obtain the generalized estimator
\[
\widehat M_{n,u}(v,s,\beta,p)=\frac1n\sum_{l=1}^n\left(v^\top\frac{(s\circ X_l^*/u)^{1/\beta}}{\|(s\circ X_l^*/u)^{1/\beta}\|}\right)^p\mathbf1\{\|(s\circ X_l^*/u)^{1/\beta}\|>1\}
\]
\[
=\frac1n\sum_{l=1}^n\left(v^\top\frac{(s\circ X_l^*/u)^{1/\beta}}{\|(s\circ X_l^*/u)^{1/\beta}\|}\right)^p\mathbf1\{\|s\circ X_l^*\|>u\}
\]
for $v\in\partial B_1^+(0)$, $(s,\beta)\in A'_\delta$ and $p\in\mathbb N_0$.''',[7],[5,10],[r'\widehat M_{n,u}(v,s,\beta,p)',r'\|s\circ X_l^*\|>u'],'Sample average of powered angular convex combinations restricted to exceedances. It is not yet divided by an exceedance count and has deterministic threshold u. Its sample is iid normalized X* in Theorem5; statistical distribution assumptions are theorem binders, not needed to evaluate the formula on data.','Section 3.1 — Generalized empirical moment estimator')
add(12,'define',r'''Analogously, with the convention $0^0=1$ we define $\widehat P_{n,u}(s)=\widehat M_{n,u}(v,s,\beta,0)$ which depends neither on $v\in\partial B_1^+(0)$ nor on $\beta\in[(1+\delta)^{-1},1+\delta]^d$, and satisfies $\widehat P_{n,u,I}=\widehat P_{n,u}(\mathbf1_I)$.''',[7],[7,11],[r'\widehat P_{n,u}(s)=\widehat M_{n,u}(v,s,\beta,0)',r'0^0=1'],'Deterministic-threshold exceedance proportion, defined as the zeroth empirical moment. The zero-power convention is explicit; finite-sample zero denominators are not explicitly resolved in the source.','Section 3.1 — Zeroth moment and exceedance proportion')
# Use an actual author keyword for this estimator, from the defining empirical-ratio context.
interfaces[-1]['source_keywords']=[dict(paper_id=PID,local_id='D12',source_text='empirical estimators',label='Empirical estimators',kind='term',context_id='D12/name')]
interfaces[-1]['name']='Empirical estimators'
members['D12']['naming_context']=[dict(context_id='D12/name',text='The associated empirical estimators are of the form',evidence=[dict(page=6,location='Empirical-ratio definition (21), including denominator')])]
add(13,'function',r'''\[
c(v,s,\beta,p):=\frac1{\mathbb E[\|s\circ\Theta\|]}\cdot\mathbb E\left[\left(v^\top\frac{(Ys\circ\Theta)^{1/\beta}}{\|(Ys\circ\Theta)^{1/\beta}\|}\right)^p\mathbf1\{Y\|s\circ\Theta\|>1\}\right].
\]''',[8],[3,5,10],[r'c(v,s,\beta,p)',r'\frac1{\mathbb E[\|s\circ\Theta\|]}'],'Normalized spectral/Pareto moment target c on the simplex and perturbation domain. Tau cancels between numerator and denominator. Theorem10 differentiates this function in s_i and beta_i and evaluates it at masked v_I; no derivative formula from an appendix is substituted.','Section 3.1 — Ratio target after (26)',context='Imposing some additional conditions on the function $c$, we obtain the following main result.',context_page=11)
add(14,'asymptotic bias',r'''Let the assumptions of Thm. 5 hold and assume that there exist some $\delta\ge0$ and some finite subset $K\subset\mathbb N$ such that, for all $p\in K\cup\{0\}$,
\[
\sqrt{\frac n{a^*(u_n)}}\left|a^*(u_n)\mathbb E[\widehat M_{n,u_n}(v,s,\beta,p)]-\tau\mathbb E[\|s\circ X^*\|]c(v,s,\beta,p)\right|\to0
\]
(27)
uniformly in $v\in\partial B_1^*(0)$ and $(s,\beta)\in A'_\delta$.''',[8],[1,2,3,4,5,10,11,13],[r'\mathbb E[\|s\circ X^*\|]',r'K\cup\{0\}',r'\partial B_1^*(0)'],'Corollary6 assumptions explicitly imported by Theorem10, including the assumptions of Theorem5. Preserve printed X* in the centering factor and the undefined starred B1 domain, both differing from surrounding formulas. This bias requirement is not imported into expectation-centered Theorem5. Full Theorem5 assumption excerpt and sequence binders are separately retained in ambient prerequisites.','Corollary 6 — Assumptions and uniform bias (27)',kind='assumption',context=r'Applying Thm. 5 and using the functional Delta method, we can even establish the desired functional limit theorem for the ratio estimator $\widehat M_{n,u_n}(v,s,\beta,p)/\widehat P_{n,u_n}(s)$, provided that we can neglect the asymptotic bias that arises from the fact that Eq. (23) yields an asymptotic relation only.')
add(16,'order statistics',r'''More precisely, let $X_{k:n,i}$ denote the $k$th upper order statistic of $X_{1i},\ldots,X_{ni}$ for $i=1,\ldots,d$ and let $X_{k:n}=(X_{k:n,1},\ldots,X_{k:n,d})$. With no loss of generality we assume that $X_{k:n,i}>0$, $1\le i\le d$.''',[9],[],[r'X_{k:n,i}',r'X_{k:n}'],'Coordinatewise kth upper sample order statistics, assumed positive so that coordinate ratios are defined. The random-threshold exceedance proportion Ptilde is the original denominator expression archived as A3; it depends on these order statistics and ell_I, not on the Hill estimator. Strict exceedances and ties are retained.','Section 3.2 — Marginal order statistics',context=r'To cope with these difficulties, we propose to work with an estimator $\widehat\alpha$ of $\alpha$ and order statistics of $X$.')
add(17,'estimator',r'''We propose the following estimator
\[
\frac{\widetilde M_{n,k,I}(v,p)}{\widetilde P_{n,k,I}}=\frac{n^{-1}\sum_{l=1}^n\left(v_I^\top\frac{(X_l/X_{k:n})^{\widehat\alpha}}{\ell_I((X_l/X_{k:n})^{\widehat\alpha})}\right)^p\mathbf1\{\ell_I(X_l/X_{k:n})>1\}}{n^{-1}\sum_{l=1}^n\mathbf1\{\ell_I(X_l/X_{k:n})>1\}}
\]
for some $k<n$, where the ratio of vectors $X_l/X_{k:n}$ is to be interpreted componentwise.''',[9],[5,6,7,16,19],[r'\widetilde M_{n,k,I}(v,p)',r'\widetilde P_{n,k,I}',r'\ell_I(X_l/X_{k:n})>1'],'Random-threshold moment ratio with coordinatewise Hill powers. Its denominator is the unpowered threshold exceedance proportion; the source’s explicit denominator is independently archived as A3 to avoid a spurious circular dependency between this moment estimator and the Hill estimator. Theorem10 writes the argument v_I; masking is idempotent and no weight renormalization is inserted.','Section 3.2 — Random-threshold moment estimator')
add(19,'marginal Hill estimators',r'''the marginal Hill estimators $\widehat\alpha_{k,n,i}$ defined via order statistics as
\[
\frac1{\widehat\alpha_{n,k,i}}=\frac{n^{-1}\sum_{l=1}^n\log\left(\ell_{\{i\}}(X_l/X_{k:n})\right)\mathbf1\{\ell_{\{i\}}(X_l/X_{k:n})>1\}}{\widetilde P_{n,k,\{i\}}}
\]
(33)''',[10],[6,16],[r'\widehat\alpha_{n,k,i}',r'\widetilde P_{n,k,\{i\}}'],'Reciprocal marginal Hill index estimate using strict order-statistic exceedances and their actual empirical proportion. Its Ptilde denominator is archived as A3; it does not depend on the estimated angular moment numerator. Preserve the prose k,n versus formula n,k order. The vector alphahat is coordinatewise, and inverse in Theorem8 is componentwise.','Section 3.2 — Hill estimators (33)')
members['D19']['naming_context']=[dict(context_id='D19/vector',text=r'To this end, we will first specify our estimators $\widehat\alpha_{n,k}=(\widehat\alpha_{n,k,1},\ldots,\widehat\alpha_{n,k,d})$ of $\alpha$ which will be componentwise Hill estimators.',evidence=[dict(page=9,location='Hill estimator vector at the end of Section3.2 introduction')])]
add(20,'second order condition',r'''In order to neglect the bias we assume the following second order condition from De Haan and Ferreira [2006]:
There exists an auxiliary positive function $A_i^*$ such that $A_i^*(t)\to0$ as $t\to\infty$ and
\[
\lim_{x\to\infty}\frac{a^*(x)\mathbb P(X_i^*>xs)-s^{-1}}{A_i^*(a^*(x))}=K_i(s)
\]
(30)
where $K_i$ is not identically 0 for any $1\le i\le d$.''',[10],[1,2],[r'A_i^*(a^*(x))',r'K_i(s)',r'a^*(x)\mathbb P(X_i^*>xs)-s^{-1}'],'Second-order marginal tail condition with positive vanishing auxiliary function and nonzero limit function, for positive scalar s. Theorem8 additionally requires sqrt(k_n) A_i*(n/k_n)→0 for every margin. This is not a hypothesis of Theorem5; Theorem10 explicitly imports it through Theorem8.','Section 3.2 — Second-order tail condition (30)',kind='assumption')
add(22,'tight centered Gaussian process',STATEMENTS[0].split('converges weakly')[1].split('to a ',1)[1],[8],[3,4,5,10],[r'G(v,s,\beta,p_1)',r'G(w,t,\gamma,p_2)'],'Original centered Gaussian law G from Theorem5, identified by covariance(25). The p=0 restriction G^0 is defined in the original main-text context below. Referencing this limit object does not import the bias assumptions of Corollary6. Coupling with Gtilde and Htilde is separately specified by D26.','Theorem 5 — Gaussian limit and covariance (25)',kind='theorem_excerpt')
members['D22']['naming_context']=[dict(context_id='D22/zero',text=r'To ease notation, we just write $G^0(s)=G(\cdot,s,\cdot,0)$.',evidence=[dict(page=11,location='Zeroth-moment Gaussian restriction immediately before Theorem10')])]
add(23,'ratio estimator',r'''Then, the sequence of processes $(\{\widetilde G_n(v,s,\beta,p);v\in\partial B_1^+(0),(s,\beta)\in A'_\delta,p\in K\})_{n\in\mathbb N}$ with
\[
\widetilde G_n(v,s,\beta,p)=\sqrt{\frac n{a^*(u_n)}}\left(\frac{\widehat M_{n,u_n}(v,s,\beta,p)}{\widehat P_{n,u_n}(s)}-c(v,s,\beta,p)\right)
\]
converges weakly in $\ell^\infty(\partial B_1^+(0)\times A'_\delta\times K)$ to a tight centered Gaussian process $\widetilde G$.
\[
\operatorname{Cov}(\widetilde G(v,\mathbf1_I,\mathbf1,p_1),\widetilde G(w,\mathbf1_I,\mathbf1,p_2))
=\frac1{\tau_I}\operatorname{Cov}((v^\top\Theta_I^I)^{p_1},(w^\top\Theta_I^I)^{p_2}).
\]''',[8],[5,7,8,9,10,11,12,13],[r'\widetilde G_n(v,s,\beta,p)',r'\Theta_I^I',r'\frac1{\tau_I}'],'Original Corollary6 Gaussian ratio limit and the last equality of its specialized main-text covariance in Remark7.1. These are separate source excerpts, not a replacement general covariance. Theorem10 needs only beta=1,s=1_I, for which the main text supplies the complete covariance. General covariance(48) lies in an excluded appendix. Bias assumptions are a separate D14 assumption import.','Corollary 6 and Remark 7.1 — Gaussian ratio limit and subset covariance',kind='source_passage',context=r'Consequently, the ratio estimator $\widehat M_{n,u_n}(v,s,\beta,p)/\widehat P_{n,u_n}(s)$ is consistent:')
add(24,'centered Gaussian random vector',STATEMENTS[1].split('where ',1)[1],[10],[3,4,8,27],[r'\widetilde H',r'\frac{2-\tau_{ij}}{\alpha_i\alpha_j}'],'Theorem8’s joint centered Gaussian vector of reciprocal-Hill limits. Covariances retain coordinate-specific alpha_i alpha_j and pair extremal coefficients. This is a limit-law reference, not an assumption that the empirical Hill estimator already has its limiting law.','Theorem 8 — Joint Hill Gaussian limit',kind='theorem_excerpt')
add(26,'joint convergence',r'''We can show the joint convergence of the different estimates to the limit processes $G$ and $\widetilde G$ and the variables $\widetilde H_i$, $i=1,\ldots,d$, as obtained in Thm. 5, Cor. 6 and Thm. 8, respectively. The covariance between the processes $G$ and $\widetilde G$ is given in Rem. 7.2. Similar calculations as above reveal that for all $v\in\partial B_1^+(0)$, $J\subset\{1,\ldots,d\}$ and $p\in\mathbb N_0$,
\[
\operatorname{Cov}(\widetilde H_i,G(v,\mathbf1_J,\mathbf1,p))=\frac\tau{\alpha_i}\mathbb E\left[-\log\left(1\wedge\frac{\|\Theta_J\|}{\Theta_i}\right)\cdot\left(v^\top\frac{\Theta_J}{\|\Theta_J\|}\right)^p\cdot(\Theta_i\wedge\|\Theta_J\|)\right].
\]
(34)
In particular, this implies that $\operatorname{Cov}(\widetilde H_i,\widetilde G(v,\mathbf1_J,\mathbf1,p))=0$ if $i\in J$.''',[10,11],[5,7,22,23,24],[r'\operatorname{Cov}(\widetilde H_i,G(v,\mathbf1_J,\mathbf1,p))',r'\operatorname{Cov}(\widetilde H_i,\widetilde G(v,\mathbf1_J,\mathbf1,p))=0'],'Joint coupling of all Gaussian components used in Theorem10, not independent copies of their marginal limits. The p=0,J={j} case of(34) gives Hill/G^0 cross covariance; the final sentence gives the Hill/Gtilde zero covariance for the needed i in I. The G/Gtilde cross covariance from Remark7.2 is preserved as A4. The intervening general formula(35) has a vector/scalar notation issue and is not silently repaired or needed for this specialization.','Remark 9 — Joint Gaussian limits and required cross covariances',kind='source_passage')
add(27,'non-standard regularly varying',r'''Let $X=(X_1,\ldots,X_d)^\top$ be a non-standard regularly varying $E=[0,\infty)^d$-valued random vector, with different tail indices $\alpha_1,\ldots,\alpha_d>0$. We assume the existence of scaling factors $r_1,\ldots,r_d>0$ such transformed vector $X^*=(r_1^{-1}X_1^{\alpha_1},\ldots,r_d^{-1}X_d^{\alpha_d})$ is regularly varying with index 1 and satisfies
\[
a^*(u)\mathbb P(u^{-1}X^*\in\cdot)\xrightarrow{v}\mu^*(\cdot),\qquad u\to\infty,
\]
(2)''',[3],[1],[r'\alpha_1,\ldots,\alpha_d>0',r'X^*=(r_1^{-1}X_1^{\alpha_1},\ldots,r_d^{-1}X_d^{\alpha_d})'],'Non-standard regularly varying model and coordinate-specific power standardization. Theorem8 instead prints an unindexed alpha in that mapping; preserve both source passages and record the inconsistency, without imposing equal marginal indices on the Section2 model.','Section 2 — Non-standard model and standardization',kind='source_passage')
def keyword(n,term,context,page):
    lid='D'+str(n);a=members[lid];ctx=lid+'/keyword-'+str(len(a.get('naming_context',[])))
    assert term in context
    a.setdefault('naming_context',[]).append(dict(context_id=ctx,text=context,evidence=[dict(page=page,location='Original source heading or naming context')]))
    x=next(x for x in interfaces if x['members'][0]['local_id']==lid)
    x['source_keywords'].append(dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term',context_id=ctx))
    x['name']=' · '.join(k['label'] for k in x['source_keywords'])
keyword(6,'spectral vectors','Instead, spectral vectors are often normalized w.r.t. some less complex functional',5)
keyword(12,'deterministic thresholds','3.1 Asymptotic normality for deterministic thresholds',6)
keyword(13,'ratio estimator',r'Consequently, the ratio estimator $\widehat M_{n,u_n}(v,s,\beta,p)/\widehat P_{n,u_n}(s)$ is consistent:',8)
keyword(17,'random thresholds','3.2 Asymptotic normality for random thresholds via order statistics',9)
keyword(23,'tight centered Gaussian process',r"converges weakly in $\ell^\infty(\partial B_1^+(0)\times A'_\delta\times K)$ to a tight centered Gaussian process $\widetilde G$.",8)
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
