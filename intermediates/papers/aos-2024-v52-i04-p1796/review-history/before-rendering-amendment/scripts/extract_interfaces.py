"""Restore manually transcribed main-text passages; independent review is separate.

Running this script is not a new source review. The general Algorithm 1
is an unresolved supplement reference, whose body must not be reconstructed.
"""
import json
from save_inventory import PID, ROOT
interfaces=[]
members={}
def add(n,term,s,pages,deps,symbols,description,heading,kind='definition',context=None,context_page=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=[])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])]
        kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=description,semantic_boundary=description,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))

add(1,'risk',r'''Let $O$ be a prototypical data point consisting of the observed data $Z$ lying in a space $\mathcal Z$ and an integer indexing variable $A$ in a finite set $\mathcal A$ containing zero. The variable $A$ indicates whether the data point comes from the target population ($A=0$) or a source population ($A\in\mathcal A\setminus\{0\}$). The observed data $(O_1,\ldots,O_n)$ is an independent and identically distributed (i.i.d.) sample from an unknown distribution $P_*$. We will use a subscript $*$ to denote components of $P_*$ throughout this paper. Data $Z$ is observed from both the source and target populations, i.e., for both $A=0$ and $A\ne0$.

The estimand of interest is the risk, namely the average value of a given loss function $\ell:\mathcal Z\to\mathbb R$, in the target population:
\[
r_*:=R(P_*):=\mathbb E_{P_*}[\ell(Z)\mid A=0].
\]
(1)
We often focus on the supervised setting where $Z=(X,Y)$, with $X\in\mathcal X$ being the covariate or feature and $Y\in\mathcal Y$ being the outcome or label. In this case, our observed data are i.i.d. triples $(X_i,Y_i,A_i)\in\mathcal X\times\mathcal Y\times\mathcal A$ distributed according to $P_*$.''',[7],[],[r'R(P_*)',r'\ell(Z)',r'\mathcal A'],'Observed-target setup and target conditional risk. Section 3 separately allows an unobserved target Q; do not impose this observed-target restriction on that general case. Footnote 1 is contextual terminology.','Section 2 — Risk (1)',kind='source_passage')
add(2,'target population risk',r'''In this section, we may use $Q$ to denote the target population and allow data from $Q$ not to be observed, namely $\mathcal A$ might not contain index $0$. We still use $r_*=\mathbb E_Q[\ell(Z)]$ to denote the target population risk. We allow $Z$ to be a general random variable rather than just $(X,Y)$ and allow more than one source population to be present.''',[10],[],[r'\mathbb E_Q[\ell(Z)]'],'Section 3 target risk under Q, potentially without target observations. The iid observed-data law P_* remains ambient context, with Section 2 target-observation restrictions overridden.','Section 3.1 — Target population risk',kind='source_passage')
add(3,'components',r'''Thus, let $Z$ be decomposed into $K\geq1$ components $(Z_1,\ldots,Z_K)$. Define $\bar Z_0:=\emptyset$, $\bar Z_k:=(Z_1,\ldots,Z_k)$, and $\mathcal Z_{k-1}$ to be the support of $\bar Z_{k-1}\mid A=0$ for $k\in[K]$. The condition is as follows.''',[10],[2],[r'\bar Z_0',r'\bar Z_k',r'\mathcal Z_{k-1}'],'Sequential prefixes and target-support notation. The source writes A=0 in the just-introduced unobserved-target setup; DS.0 subsequently identifies support under Q. Preserve this scope issue.','Section 3.1 — Components and supports')
add(4,'General sequential conditionals',r'''For every $k\in[K]$, there exists a known nonempty subset $\mathcal S'_k\subset\mathcal A$ such that, (i) the distribution of $\bar Z_{k-1}$ under $Q$ is dominated by $\bar Z_{k-1}\mid A\in\mathcal S'_k$ under $P_*$, and (ii) for all $a\in\mathcal S'_k$, $Z_k\mid\bar Z_{k-1}=\bar z_{k-1},A=a$ is distributed identically as $Z_k\mid\bar Z_{k-1}=\bar z_{k-1}$ under $Q$ for $Q$-almost every $\bar z_{k-1}$ in the support $\mathcal Z_{k-1}$ of $\bar Z_{k-1}$ under $Q$.''',[10],[2,3],[r"\mathcal S'_k",r'\bar Z_{k-1}'],'Known nonempty relevant-population sets, target-history domination and Q-almost-everywhere conditional equality. DS.0 is an additional final branch of Theorem 1, not a global premise of its drift-corrected expansion.','Condition DS.0 (General sequential conditionals)',kind='condition',context='Condition DS.0 (General sequential conditionals).')
add(5,'Sequential conditionals',r'''Condition DS.0 holds with $0\in\mathcal A$ and $0\in\mathcal S'_k$ for every $k$.''',[10],[4],[r"0\in\mathcal S'_k"],'Observed-target specialization of DS.0. Relevant source sets without the target may be empty.','Condition DS.0† (Sequential conditionals)',kind='condition',context='Condition DS.0† (Sequential conditionals).')
add(6,'Concept shift in the features',r'''$X\perp\!\!\!\perp A$.''',[10],[1],[r'X\perp\!\!\!\perp A'],'Feature marginal independence for the one-source setup A={0,1}; conditional response distributions may differ. The binary convention is retained separately and is essential for the formula using 1-a.','Condition DS.1 (Concept shift in the features)',kind='condition',context='Condition DS.1 (Concept shift in the features).')
add(7,'Radon-Nikodym derivative',r'''For Condition DS.0, let $\lambda_*^{k-1}$ denote the Radon-Nikodym derivative of the distribution of $\bar Z_{k-1}$ under $Q$ relative to that of $\bar Z_{k-1}\mid A\in\mathcal S'_k$ under $P_*$.''',[12],[2,3],[r'\lambda_*^{k-1}'],'Target-history density ratio relative to pooled relevant source history. Absolute continuity is needed for the stated meaning. The source presents it for DS.0, but this must not become an unstated global theorem premise.','Section 3.1 — Radon-Nikodym derivative')
add(8,'conditional probability',r'''For Condition $\mathrm{DS.0}^\dagger$, define the conditional probability of each population
\[
\Pi_*^{k,a}:\bar z_k\mapsto P_*(A=a\mid\bar Z_k=\bar z_k)\quad\text{for }k\in[0:K-1],\ a\in\mathcal A,
\]
and let $\pi_*^a:=\Pi_*^{0,a}=P_*(A=a)$ denote the marginal probabilities of all populations ($a\in\mathcal A$); thus, $\pi_*^0=\rho_*$ for $\rho_*$ from Section 2.''',[12],[3],[r'\Pi_*^{k,a}',r'\pi_*^a'],'Conditional and marginal population probabilities. Marginal pi remains meaningful in the general mixture; pi^0=rho_* concerns an observed target.','Section 3.1 — Conditional probability and marginal probabilities')
add(9,'conditional odds',r'''Define the conditional odds of relevant source populations versus the target population:
\[
\theta_*^{k-1}:=\frac{\sum_{a\in\mathcal S_k}\Pi_*^{k-1,a}}{\Pi_*^{k-1,0}}\quad\text{for }k\in[K].
\]
Under the stronger condition $\mathrm{DS.0}^\dagger$, it follows from Bayes’ Theorem that
\[
\lambda_*^{k-1}=\frac{\sum_{a\in\mathcal S'_k}\pi_*^a}{\pi_*^0(1+\theta_*^{k-1})}.
\]
(4)''',[12],[8,7,5],[r'\theta_*^{k-1}',r'\lambda_*^{k-1}'],'Relevant-source-versus-target odds and the stated density-ratio identity under the dagger condition. S_k excludes 0; zero and infinite denominator conventions require separate retention.','Section 3.1 — Conditional odds (4)')
add(10,'conditional means',r'''For both Conditions DS.0 and $\mathrm{DS.0}^\dagger$, we also define conditional means of the loss starting with $\ell_*^K:=\ell$ and letting recursively
\[
\ell_*^k:\bar z_k\mapsto\mathbb E_{P_*}[\ell_*^{k+1}(\bar Z_{k+1})\mid\bar Z_k=\bar z_k,A\in\mathcal S'_{k+1}]\quad\text{for }\bar z_k\in\mathcal Z_k,\ k\in[K-1].
\]
(5)
We allow $\ell_*^k$ to take any value outside $\mathcal Z_k$, for example, when the support of $\bar Z_k\mid A\in\mathcal S'_{k+1}$ is larger than the support $\mathcal Z_k$ of $\bar Z_k\mid A=0$. Under Condition DS.0, $\ell_*^k(\bar z_k)=\mathbb E_Q[\ell(Z)\mid\bar Z_k=\bar z_k]$ for $\bar z_k\in\mathcal Z_k$. We discuss the consequences of the non-unique definition of $\ell_*^k$ without Condition DS.0 in more detail in Section 3.4.''',[12,13],[2,3],[r'\ell_*^K',r'\ell_*^k'],'Backward conditional means on target supports, with arbitrary extensions outside. Equality with Q is expressly restricted to DS.0; arbitrary extensions must not be replaced by a unique global regression.','Section 3.1 — Conditional means of the loss (5)')

GENERIC=r'''Let $\boldsymbol\ell_*:=(\ell_*^k)_{k=1}^{K-1}$, $\boldsymbol\lambda_*:=(\lambda_*^k)_{k=1}^{K-1}$, $\boldsymbol\theta_*:=(\theta_*^k)_{k=1}^{K-1}$, and $\boldsymbol\pi_*:=(\pi_*^a)_{a\in\mathcal A}$ be collections of true nuisances. For any given collections $\boldsymbol\ell=(\ell^k)_{k=1}^{K-1}$, $\boldsymbol\lambda:=(\lambda^k)_{k=1}^{K-1}$, $\boldsymbol\theta=(\theta^k)_{k=1}^{K-1}$ and $\boldsymbol\pi:=(\pi^a)_{a\in\mathcal A}$ of nuisances, a scalar $r$ and $\ell^K:=\ell$, define the pseudo-losses $\widetilde{\mathcal T}(\boldsymbol\ell,\boldsymbol\lambda,\boldsymbol\pi)$ and $\mathcal T(\boldsymbol\ell,\boldsymbol\theta,\boldsymbol\pi):\mathcal O\to\mathbb R$ based on these nuisances, so that for $o=(z,a)$,'''
add(11,'pseudo-losses',r'''\[
\widetilde{\mathcal T}(\boldsymbol\ell,\boldsymbol\lambda,\boldsymbol\pi)(o)=\sum_{k=2}^K\frac{\mathbb1(a\in\mathcal S'_k)}{\sum_{b\in\mathcal S'_k}\pi^b}\lambda^{k-1}(\bar z_{k-1})[\ell^k(\bar z_k)-\ell^{k-1}(\bar z_{k-1})]+\frac{\mathbb1(a\in\mathcal S'_1)}{\sum_{b\in\mathcal S'_1}\pi^b}\ell^1(z_1).
\]
(6)''',[13],[3,7,8,10],[r'\widetilde{\mathcal T}'],'General pseudo-loss with generic nuisance inputs, which need not equal the true nuisance functions. Preserve normalized pooled-source weights and the first-component term.','Section 3.1 — Pseudo-loss (6)',context=GENERIC)
add(12,'pseudo-losses',r'''\[
\mathcal T(\boldsymbol\ell,\boldsymbol\theta,\boldsymbol\pi)(o)=\sum_{k=2}^K\frac{\mathbb1(a\in\mathcal S'_k)}{\pi^0(1+\theta^{k-1}(\bar z_{k-1}))}\{\ell^k(\bar z_k)-\ell^{k-1}(\bar z_{k-1})\}+\frac{\mathbb1(a\in\mathcal S'_1)}{\pi^0(1+\theta^0)}\ell^1(z_1).
\]
(7)''',[13],[3,8,9,10],[r'\mathcal T(\boldsymbol\ell,\boldsymbol\theta,\boldsymbol\pi)'],'Odds pseudo-loss, with theta^0=sum_{a in S_1}pi^a/pi^0. Preserve independently from (6); equivalence requires the displayed density-ratio transformation.','Section 3.1 — Pseudo-loss (7)',context=GENERIC)
IFCONTEXT=r'''A key result we will use is that the efficient influence function for estimating $r_*$ (i) equals $D_{\mathrm{GSC}}(\boldsymbol\ell_*,\boldsymbol\lambda_*,\boldsymbol\pi_*,r_*)$ under Condition DS.0 and when $\lambda_*^k$ are uniformly bounded away from zero and infinity as a function of $\bar z_k\in\mathcal Z_k$ for all $k\in[0:K-1]$, and (ii) specializes to $D_{\mathrm{SC}}(\boldsymbol\ell_*,\boldsymbol\theta_*,\boldsymbol\pi_*,r_*)$ under Condition $\mathrm{DS.0}^\dagger$ and when $\theta_*^k$ are bounded functions for all $k\in[0:K-1]$.'''
add(13,'efficient influence function',r'''Further, given any scalar $r$, with $\theta^0:=\sum_{a\in\mathcal S_1}\pi^a/\pi^0$, define
\[
D_{\mathrm{GSC}}(\boldsymbol\ell,\boldsymbol\lambda,\boldsymbol\pi,r):o=(z,a)\mapsto\widetilde{\mathcal T}(\boldsymbol\ell,\boldsymbol\lambda,\boldsymbol\pi)(o)-\frac{\mathbb1(a\in\mathcal S'_1)}{\sum_{b\in\mathcal S'_1}\pi^b}r,
\]
(8)''',[13],[11,8],[r'D_{\mathrm{GSC}}'],'General centered pseudo-loss for arbitrary r and nuisances. Adjacent efficient influence-function identification has its own qualifications; these are not global premises of every theorem branch.','Section 3.1 — Influence function (8)',context=IFCONTEXT)
add(14,'efficient influence function',r'''\[
D_{\mathrm{SC}}(\boldsymbol\ell,\boldsymbol\theta,\boldsymbol\pi,r):o=(z,a)\mapsto\mathcal T(\boldsymbol\ell,\boldsymbol\theta,\boldsymbol\pi)(o)-\frac{\mathbb1(a\in\mathcal S'_1)}{\pi^0(1+\theta^0)}r.
\]
(9)''',[13],[12,8],[r'D_{\mathrm{SC}}'],'Odds-based centered pseudo-loss. Generic theta^0 follows the definition immediately preceding (8), retained as auxiliary context rather than making D_GSC a mathematical prerequisite.','Section 3.1 — Influence function (9)',context=IFCONTEXT)
add(15,'asymptotic variance',r'''Consequently, the smallest possible asymptotic variance of a sequence of RAL estimators (scaled by $n^{1/2}$) is
\[
\sigma_{*,\mathrm{GSC}}^2:=\mathbb E_{P_*}[D_{\mathrm{GSC}}(\boldsymbol\ell_*,\boldsymbol\lambda_*,\boldsymbol\pi_*,r_*)(O)^2]
\]
(10)
under Condition DS.0 and specializes to $\sigma_{*,\mathrm{SC}}^2:=\mathbb E_{P_*}[D_{\mathrm{SC}}(\boldsymbol\ell_*,\boldsymbol\theta_*,\boldsymbol\pi_*,r_*)(O)^2]$ under Condition $\mathrm{DS.0}^\dagger$.''',[13],[13,14,2,26],[r'\sigma_{*,\mathrm{GSC}}^2',r'\sigma_{*,\mathrm{SC}}^2'],'Second moments of the respective influence functions. Efficient-bound interpretation inherits the adjacent qualifications. Theorem 1 divides by the general standard deviation without separately stating strict positivity.','Section 3.1 — Asymptotic variance (10)')
add(16,'Cross-fit risk estimator',r'''The corresponding estimator for more general condition DS.0 is similar and described in Alg. 1 in the Supplemental Material.''',[14],[2],[],'Opaque main-text reference to the general Algorithm 1. Theorem 1 names its nuisance inputs and Line 9 output. Missing algorithm steps and dependencies are not reconstructed from the dagger algorithm.','Section 3.2 — General Algorithm 1 reference',kind='source_passage',context='3.2 Cross-fit risk estimator',context_page=13)
members['D16']['highlight_phrases']=['Alg. 1']
members['D16']['unresolved_reference']=dict(reference='Alg. 1 in the Supplemental Material',reason='Algorithm body outside the main-text-only scope.',available_main_text_pages=[14,17,18],body_inspected=False)
add(26,'asymptotically linear',r'''An estimator $\widehat\theta$ of a parameter $\theta_*=\theta_*(P_*)$ is said to be asymptotically linear if $\widehat\theta=\theta_*+n^{-1}\sum_{i=1}^n\mathrm{IF}(O_i)+o_p(n^{-1/2})$ for a function $\mathrm{IF}\in L_0^2(P_*)$. This asymptotic linearity implies that $\sqrt n(\widehat\theta-\theta_*)\xrightarrow{d}N(0,\mathbb E_{P_*}[\mathrm{IF}(O)^2])$. The function $\mathrm{IF}$ is called the influence function of $\widehat\theta$. Under a semiparametric model, there may be infinitely many influence functions, but there exists a unique efficient influence function, which is the influence function of regular asymptotically linear (RAL) estimators with the smallest asymptotic variance. Under a nonparametric model, all RAL estimators of a parameter $\theta_*$ share the same influence function, which equals the efficient influence function.''',[9],[],[r'\mathrm{IF}(O_i)',r'L_0^2(P_*)'],'Main-text asymptotic linearity and efficiency terminology. Full regularity definitions are not supplied here and are not imported from the supplementary review.','Section 2 — Asymptotic linearity and efficiency')

add(17,'Cross-fit estimator',r'''Cross-fit estimator of $r_*=\mathbb E_{P_*}[\ell(Z)\mid A=0]$ under Condition $\mathrm{DS.0}^\dagger$

Require: Data $\{O_i=(Z_i,A_i)\}_{i=1}^n$, relevant source population sets $\mathcal S'_k$ ($k\in[K]$), number $V$ of folds, classifier $\mathcal C$, regression estimator $\mathcal K$

1: Randomly split data into $V$ folds of approximately equal sizes. Denote the index set of data points in fold $v$ by $I_v$, and the index set of data points with $A\in\mathcal S'_k$ by $J_k$ for $k\in[K]$.

2: for $v\in[V]$ do

3: For all $k\in[K-1]$, estimate $\theta_*^k$ using data out of fold $v$, by classifying $A=0$ against $A\in\mathcal S_{k+1}$ via the classifier $\mathcal C$ with covariates $\bar Z_k$ in the subsample with $A\in\mathcal S'_{k+1}$; that is, set $\widehat\theta_v^k:=\mathcal C(\mathbb1(A\ne0),\bar Z_k,([n]\setminus I_v)\cap J_{k+1})$ and $\widehat{\boldsymbol\theta}_v:=(\widehat\theta_v^k)_{k=1}^{K-1}$.

4: Set $\widehat\pi_v^a:=|I_v|^{-1}\sum_{i\in I_v}\mathbb1(A_i=a)$ for all $a\in\mathcal A$, $\widehat{\boldsymbol\pi}_v:=(\widehat\pi_v^a)_{a\in\mathcal A}$, $\widehat\theta_v^0:=\sum_{a\in\mathcal S_1}\widehat\pi_v^a/\widehat\pi_v^0$, and $\widehat\ell_v^K$ to be $\ell$.

5: for $k=K-1,\ldots,1$ do

6: Estimate $\ell_*^k$ using data out of fold $v$ by regressing $\widehat\ell_v^{k+1}(\bar Z_{k+1})$ on $\bar Z_k$ in the subsample with $A\in\mathcal S'_{k+1}$; that is, set $\widehat\ell_v^k:=\mathcal K(\widehat\ell_v^{k+1}(\bar Z_{k+1}),\bar Z_k,([n]\setminus I_v)\cap J_{k+1})$.

7: Set $\widehat{\boldsymbol\ell}_v:=(\widehat\ell_v^k)_{k=1}^{K-1}$.

8: Compute an estimator of $r_*$ for fold $v$:
\[
\widehat r_v:=\frac1{|I_v|}\sum_{i\in I_v}\mathcal T(\widehat{\boldsymbol\ell}_v,\widehat{\boldsymbol\theta}_v,\widehat{\boldsymbol\pi}_v)(O_i)
\]
(11)
9: Compute the cross-fit estimator combining estimators $\widehat r_v$ from all folds: $\widehat r:=\frac1n\sum_{v=1}^V|I_v|\widehat r_v$.''',[15],[1,3,5,8,9,10,12],[r'\widehat r_v',r'\widehat{\boldsymbol\theta}_v',r'\widehat\pi_v^a'],'Complete main-text Algorithm 1-dagger. Marginal probabilities are fitted in-fold; classification and regression use out-of-fold data. Its motivating dagger label does not prohibit Theorem 1 from studying drift when shift conditions fail.','Algorithm 1† — Cross-fit estimator')
add(18,'oracle estimator',r'''Define the oracle estimator $h_v^{k-1}$ of $\ell_*^{k-1}$ based on $\widehat\ell_v^k$, evaluated under the true distribution $P_*$, as
\[
h_v^{k-1}:\bar z_{k-1}\mapsto\mathbb E_{P_*}[\widehat\ell_v^k(\bar Z_k)\mid\bar Z_{k-1}=\bar z_{k-1},A\in\mathcal S'_k],
\]''',[14],[3,10],[r'h_v^{k-1}'],'Conditional expectation of the next fitted regression. Footnote 5 freezes fitted nuisances and integrates a fresh observation; the output remains random through the fitted functions.','Section 3.2 — Oracle estimator')
add(19,'product bias term',r'''\[
\begin{aligned}
&\frac{\sum_{a\in\mathcal S'_k}\pi_*^a}{\sum_{a\in\mathcal S'_k}\widehat\pi_v^a}\mathbb E_{P_*}\left[\{\widehat\lambda_v^{k-1}(\bar Z_{k-1})-\lambda_*^{k-1}(\bar Z_{k-1})\}\{h_v^{k-1}(\bar Z_{k-1})-\widehat\ell_v^{k-1}(\bar Z_{k-1})\}\mid A\in\mathcal S'_k\right]\\
&+\left\{\frac{\sum_{a\in\mathcal S'_k}\pi_*^a}{\sum_{a\in\mathcal S'_k}\widehat\pi_v^a}-\frac{\sum_{a\in\mathcal S'_1}\pi_*^a}{\sum_{a\in\mathcal S'_1}\widehat\pi_v^a}\right\}\mathbb E_Q[h_v^{k-1}(\bar Z_{k-1})-\widehat\ell_v^{k-1}(\bar Z_{k-1})].
\end{aligned}
\]
(12)
for Condition DS.0 and Alg. 1, which reduces to''',[14,15],[2,7,8,10,18],[r'\widehat\lambda_v^{k-1}',r'h_v^{k-1}'],'Full general B_{k,v}, including the marginal-probability correction. The PDF display is interrupted by Algorithm 1-dagger; both mathematical parts are preserved together.','Section 3.2 — Product bias term (12)',context=r'and the product bias term $B_{k,v}$ as')
add(20,'product bias term',r'''\[
\begin{aligned}
&\frac{\sum_{a\in\mathcal S'_k}\pi_*^a}{\sum_{a\in\mathcal S'_k}\widehat\pi_v^a}\mathbb E_{P_*}\left[\left\{\frac{\sum_{a\in\mathcal S'_k}\widehat\pi_v^a}{\widehat\pi_v^0(1+\widehat\theta_v^{k-1}(\bar Z_{k-1}))}-\frac{\sum_{a\in\mathcal S'_k}\pi_*^a}{\pi_*^0(1+\theta_*^{k-1}(\bar Z_{k-1}))}\right\}\{h_v^{k-1}(\bar Z_{k-1})-\widehat\ell_v^{k-1}(\bar Z_{k-1})\}\mid A\in\mathcal S'_k\right]\\
&+\left(\frac{\sum_{a\in\mathcal S'_k}\pi_*^a}{\sum_{a\in\mathcal S'_k}\widehat\pi_v^a}-\frac{\sum_{a\in\mathcal S'_1}\pi_*^a}{\sum_{a\in\mathcal S'_1}\widehat\pi_v^a}\right)\mathbb E_{P_*}[h_v^{k-1}(\bar Z_{k-1})-\widehat\ell_v^{k-1}(\bar Z_{k-1})\mid A=0].
\end{aligned}
\]
(13)
for Condition $\mathrm{DS.0}^\dagger$ and Alg. $1^\dagger$ when $\widehat\lambda_v^{k-1}$ is transformed from $\widehat\theta_v^{k-1}$ and $\widehat\pi_v$ as in (4).''',[15],[1,8,9,10,18],[r'\widehat\theta_v^{k-1}',r'h_v^{k-1}'],'Odds-transformed specialization of B_{k,v}, with a target conditional expectation in the correction. Equivalence to (12) is restricted to the stated transformation.','Section 3.2 — Product bias term (13)',context=r'and the product bias term $B_{k,v}$ as',context_page=14)
add(21,'Condition ST.1',r'''For every fold $v\in[V]$,

1. the following term is $o_p(n^{-1/2})$ for Condition DS.0 and Alg. 1, or for Condition $\mathrm{DS.0}^\dagger$ and Alg. $1^\dagger$:
\[
\sum_{k=2}^K B_{k,v};
\]
(14)
2. the following term is $o_p(1)$ for Condition DS.0 and Alg. 1, or for Condition $\mathrm{DS.0}^\dagger$ and Alg. $1^\dagger$, respectively:
\[
\left\|\left(\sum_{a\in\mathcal S'_1}\widehat\pi_v^a\right)\widetilde{\mathcal T}(\widehat{\boldsymbol\ell}_v,\widehat{\boldsymbol\lambda}_v,\widehat{\boldsymbol\pi}_v)-\left(\sum_{a\in\mathcal S'_1}\pi_*^a\right)\widetilde{\mathcal T}(\boldsymbol\ell_*,\boldsymbol\lambda_*,\boldsymbol\pi_*)\right\|_{L^2(P_*)}
\]
(15)
or
\[
\left\|\left(\sum_{a\in\mathcal S'_1}\widehat\pi_v^a\right)\mathcal T(\widehat{\boldsymbol\ell}_v,\widehat{\boldsymbol\theta}_v,\widehat{\boldsymbol\pi}_v)-\left(\sum_{a\in\mathcal S'_1}\pi_*^a\right)\mathcal T(\boldsymbol\ell_*,\boldsymbol\theta_*,\boldsymbol\pi_*)\right\|_{L^2(P_*)}.
\]
(16)''',[16],[8,11,12,19,20],[r'B_{k,v}',r'\widetilde{\mathcal T}',r'\mathcal T'],'Per-fold bias sum and L2 pseudo-loss consistency, with matching general or dagger formulas. Illustrative nuisance limits and sufficient regression rates are not extra requirements.','Condition ST.1',kind='condition',context='Condition ST.1.')
add(22,'Condition ST.2',r'''For each fold $v\in[V]$, Condition ST.1 holds with the $o_p(n^{-1/2})$ in part 1 replaced by $o_p(1)$ and the $o_p(1)$ in part 2 replaced by $O_p(1)$.''',[17],[21],[r'o_p(n^{-1/2})',r'O_p(1)'],'Weaker branchwise rates: bias sum tends to zero and L2 pseudo-loss discrepancy is stochastically bounded. Preserve capital O_p.','Condition ST.2',kind='condition',context='Condition ST.2.')
add(23,'conditional risk function',r'''To do so, define $\mathcal E_*:x\mapsto\mathbb E_{P_*}[\ell(X,Y)\mid X=x,A=0]$, the conditional risk function in the target population. Recall that $\rho_*$ denotes $P_*(A=0)$.''',[25],[1],[r'\mathcal E_*'],'Conditional target risk given features. Theorem 2 allows an arbitrary common L2 limit E_infinity; only its final efficient branch identifies that limit with E_*.','Section 4.1 — Conditional risk function')
add(24,'efficient influence function',r'''For scalars $\rho\in(0,1)$, $r\in\mathbb R$, and a function $\mathcal E:\mathcal X\to\mathbb R$, define
\[
D_{\mathrm{Xcon}}(\rho,\mathcal E,r):o=(x,y,a)\mapsto\frac{1-a}{\rho}\{\ell(x,y)-\mathcal E(x)\}+\mathcal E(x)-r.
\]
(23)''',[25],[1],[r'D_{\mathrm{Xcon}}'],'Explicit feature-shift formula for arbitrary conditional-risk argument, not necessarily E_*. The binary population convention is essential. The explicit formula does not require the general DSC formula as a prerequisite.','Section 4.1 — Influence function (23)',context=r'We first present the efficient influence function for the risk $r_*$ under concept shift in the features, where $X\perp\!\!\!\perp A$ (DS.1).')
add(25,'Cross-fit estimator',r'''Cross-fit estimator of risk $r_*$ under Condition DS.1, concept shift in the features

Require: Data $\{O_i=(Z_i,A_i)\}_{i=1}^n$, number $V$ of folds, regression estimation method for $\mathcal E_*$

1: Randomly split all data (from both populations) into $V$ folds. Let $I_v$ be the indices of data points in fold $v$.

2: for $v\in[V]$ do Estimate $\mathcal E_*$ by $\widehat{\mathcal E}^{-v}$ using data out of fold $v$.

3: for $v\in[V]$ do (Obtain an estimating-equation-based estimator for fold $v$)

4: With $\widehat\rho^v:=|I_v|^{-1}\sum_{i\in I_v}\mathbb1(A_i=0)$, set
\[
\widehat r_{\mathrm{Xcon}}^v:=\frac1{|I_v|}\sum_{i\in I_v}\left\{\frac{\mathbb1(A_i=0)}{\widehat\rho^v}[\ell(X_i,Y_i)-\widehat{\mathcal E}^{-v}(X_i)]+\widehat{\mathcal E}^{-v}(X_i)\right\}.
\]
(24)
5: Obtain the cross-fit estimator: $\widehat r_{\mathrm{Xcon}}:=\frac1n\sum_{v=1}^V|I_v|\widehat r_{\mathrm{Xcon}}^v$.''',[26],[1,23],[r'\widehat r_{\mathrm{Xcon}}^v',r'\widehat\rho^v',r'\widehat{\mathcal E}^{-v}'],'Complete Section 4 Algorithm 1: out-of-fold regression, in-fold target proportion, weighted fold aggregation. Distinct from the supplement Algorithm 1. Preserve the conflicting rho superscript in Theorem 2 separately.','Section 4.2 — Algorithm 1, Cross-fit estimator')

def main():
    interfaces.sort(key=lambda x:int(x['members'][0]['local_id'][1:]))
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,data in [('source-passages.json',dict(paper_id=PID,status='extracted',scope='Original main-text source passages; consult the separate paper audit for source-review status.',source_passages=[members[k] for k in sorted(members,key=lambda k:int(k[1:]))])),('interface-extraction.json',dict(paper_id=PID,status='extracted',interfaces=interfaces))]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(members)} source entries; validation status is recorded separately.')
if __name__=='__main__':main()
