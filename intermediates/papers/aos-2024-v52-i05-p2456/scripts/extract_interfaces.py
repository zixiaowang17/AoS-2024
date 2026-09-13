"""Preserve original RKHS, projection, model and bootstrap source passages."""
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
add(1,'positive definite kernel',r'''Let $\mathcal X\subset\mathbb R^d$, $d\in\mathbb N$, denote the support of $X$. Let $m:\mathcal X\to\mathbb R$ be any measurable function, and let $K:\mathcal X\times\mathcal X\to\mathbb R$ be a positive definite kernel, i.e., a symmetric function such that for any $n\in\mathbb N$, $c_1,\ldots,c_n$ in $\mathbb R$ and $x_1,\ldots,x_n$ in $\mathcal X$,
\[
\sum_{i=1}^n\sum_{j=1}^nc_ic_jK(x_i,x_j)\ge0.
\]''',[6],[],[r'K:\mathcal X\times\mathcal X\to\mathbb R',r'\sum_{i=1}^n\sum_{j=1}^nc_ic_jK(x_i,x_j)\ge0'],'Real symmetric positive semidefinite covariance kernel; positive definite is the source term but strict positivity is not required. The index domain is abstract for the general dual-space theorem, with the covariate support used for the statistical application.','Section 3 — Positive definite kernel')
add(2,'RKHS',r'''Associated to the covariance kernel $K$, there is a unique RKHS $\mathcal H_K$ with inner product $\langle\cdot,\cdot\rangle_K$ and norm $\|\cdot\|_K$. Let $\mathcal B_K=\{h\in\mathcal H_K:\|h\|_K\le1\}$ denote the unit ball in $\mathcal H_K$.''',[9],[1],[r'\mathcal H_K',r'\mathcal B_K=\{h\in\mathcal H_K:\|h\|_K\le1\}'],'Real reproducing kernel Hilbert space with its own norm and unit ball. The standing separability convention is preserved with the dual-space passage. Do not identify this RKHS norm with the L2(mu) norm used for the projected-kernel spectrum.','Section 3.3 — RKHS and unit ball')
add(3,'dual space',r"""define the standard operator norm for $S\in\mathcal H_K^*$
\[
\|S\|:=\sup_{a\in\mathcal B_K}|S(a)|.
\]
To avoid measurability issues, we assume that $\mathcal H_K$ is separable (hence $\mathcal H_K^*$ is separable). A sufficient condition is that $\mathcal X$ is separable and $K$ is continuous in $\mathcal X\times\mathcal X$.
In this section we give a weak convergence theorem for sequences of random elements in $\mathcal H_K^*$, the space of linear bounded functionals on $\mathcal H_K$, which is equipped with the standard operator norm. We consider weak convergence in the metric space $\mathcal H_K^*$ in the sense of J. Hoffmann-Jorgensen (see, e.g., [9], p. 94). The symbol $\Longrightarrow$ denotes weak convergence in $\mathcal H_K^*$ and the corresponding Borel $\sigma$ field.""",[9,10],[2],[r'\mathcal H_K^*',r'\|S\|:=\sup_{a\in\mathcal B_K}|S(a)|'],'Original space and topology passages, with the intervening statistic illustration omitted. S_n in Theorem4.1 is an arbitrary sequence of random bounded functionals in this separable dual, whereas Theorem4.4 uses conditional distributional convergence of its scalar squared norm.','Sections 3.3 and 4.1 — Dual space, operator norm and weak convergence',context=r'dual space of $\mathcal H_K$, denoted as $\mathcal H_K^*$',context_page=9)
add(4,'Assumption A',r'''(i) For all $a\in\mathcal H_K$, $S_n(a)\xrightarrow{d}N(0,\sigma^2(a))$, where $\sigma^2(a)=\sigma(a,a)\ge0$, and $\sigma(\cdot,\cdot)$ is a continuous, positive symmetric bilinear form on $\mathcal H_K$; (ii) for some orthonormal basis $\{e_j\}_{j\in\mathbb N}$ of $\mathcal H_K$ we have $\sum_{j=1}^\infty\sigma^2(e_j)<\infty$; and (iii) for any $\varepsilon>0$,
\[
\lim_{J\to\infty}\limsup_{n\to\infty}P\left(\sum_{j\ge1+J}S_n^2(e_j)\ge\varepsilon\right)=0.
\]''',[10],[3],[r'S_n(a)',r'\sum_{j\ge1+J}S_n^2(e_j)'],'Coordinate Gaussian limits, trace summability for one orthonormal basis and the uniform tail-tightness condition, with the printed order of limits. S_n is the arbitrary dual-valued sequence specified immediately before this assumption. No statistical sampling model is imposed by this general theorem.','Assumption A',kind='assumption',context='Assumption A',phrases=['Assumption A'])
add(5,'linear operator',r'''Define the linear operator $T_\sigma:\mathcal H_K\to\mathcal H_K$, with $K_x(\cdot)=K(x,\cdot)$, as
\[
T_\sigma a(x):=\sigma(a,K_x).
\]
Under Assumption A, the operator $T_\sigma$ is trace class and self-adjoint. Thus, there exists an spectrum $\{\mu_j,\phi_j\}_{j\in\mathbb N}$ such that $\{\phi_j\}_{j\in\mathbb N}$ is orthonormal in $\mathcal H_K$ and $T_\sigma\phi_j=\mu_j\phi_j$, for $j\in\mathbb N$. We apply Assumption A to the orthonormal basis $\{\phi_j\}_{j\in\mathbb N}$ of eigenfunctions.''',[10,11],[2,4],[r'T_\sigma a(x):=\sigma(a,K_x)',r'T_\sigma\phi_j=\mu_j\phi_j'],'Covariance operator and spectral notation for the abstract Gaussian limit. The covariance form sigma is supplied by Assumption A; mu_j and H_K-orthonormal phi_j are distinct from lambda_j and L2(mu)-orthonormal varphi_j in the application. These letters normalize font variants only.','Section 4.1 — Covariance operator and its spectrum')
add(6,'random element',r'''Define the random element of $\mathcal H_K^*$
\[
S_\infty(\cdot)=\sum_{j=1}^\infty\sqrt{\mu_j}\langle\phi_j,\cdot\rangle_KU_j,
\]
where, henceforth, $\{U_j\}_{j\in\mathbb N}$ are iid standard normals.''',[11],[3,5],[r'S_\infty',r'\sqrt{\mu_j}'],'Centered Gaussian random bounded functional constructed from the covariance-operator spectrum. Its square-root coefficient and RKHS-orthonormal basis are preserved; U_j are the common iid standard-normal convention used later, not a requirement to import Assumption A into the applied theorems.','Section 4.1 — Gaussian random element')
add(7,'measurable moment function',r'''for a measurable moment function $\varepsilon:\mathcal Z\times\Theta\longrightarrow\mathbb R^q$ that is assumed to be known up-to the finite-dimensional parameter $\theta_0\in\Theta$, with $\Theta\subset\mathbb R^p$, $p\in\mathbb N$. For simplicity of exposition, we focus on the one-dimensional moment case $q=1$, as tests statistics in the general case $q\in\mathbb N$ are simply the sum of the test statistics corresponding to each component of $\varepsilon(Z,\theta_0)$ (see Remark 1 in Section 3.3). The observed random vector $W$ contains the non-overlapping elements of $Z$ and $X$, and it is defined on the probability space $(\Omega,\mathcal F,P)$.
when we observe an independent and identically distributed (iid) sample $\{W_i\}_{i=1}^n$ of size $n\ge1$, with the same distribution as $W$.''',[1],[],[r'\varepsilon:\mathcal Z\times\Theta\longrightarrow\mathbb R^q',r'\{W_i\}_{i=1}^n'],'Original moment-function and sampling passages, separately excerpted around the model-testing hypotheses. Scalar q=1 is the base theory. W_i carries the joint observation (Z_i,X_i); Z and X are not assumed independent. The CMR null itself is stored separately and is not imposed by this data definition.','Section 1 — Moment function and iid observations',kind='source_passage')
add(8,'Conditional Moment Restrictions',r'''A large class of models in the social sciences are defined through Conditional Moment Restrictions (CMR) of the form
\[
E[\varepsilon(Z,\theta_0)\mid X]=0\text{ almost surely (a.s.) for some unknown }\theta_0\in\Theta,
\]
(1)
With this motivation in mind, the aim of this paper is to propose tests for the hypotheses
\[
H_0:(1)\text{ holds}\qquad\text{vs}\qquad H_1:P(E[\varepsilon(Z,\theta)\mid X]=0)<1\text{ for all }\theta\in\Theta,
\]''',[1],[7],[r'E[\varepsilon(Z,\theta_0)\mid X]=0',r'H_0'],'Existence of a model parameter satisfying the conditional moment restriction almost surely, versus failure for every parameter. H0 is explicitly printed in Theorem4.3 but not Theorem4.4; preserve that difference. The intervening source data prose is stored separately.','Section 1 — Conditional moment restriction (1) and testing hypotheses',kind='condition')
add(9,'conditional score',r'''we define the score and the conditional score, respectively, as follows
\[
s(Z,\theta_0):=\frac{\partial\varepsilon(Z,\theta_0)}{\partial\theta}\quad\text{and}\quad g(X,\theta_0):=E[s(Z,\theta_0)\mid X],
\]''',[3],[7],[r's(Z,\theta_0)',r'g(X,\theta_0)'],'Derivative of the known moment function and its conditional expectation given the covariates. These are p-vector scores. Known functional form of g up to theta is the base construction; the separate Section5 nonparametric extension is not silently folded into it.','Section 1.2 — Score and conditional score')
add(10,'orthogonal projection operator',r'''we suggest using the orthogonal projection operator, for $a\in L_2(X)$,
\[
\Pi a(x)=a(x)-G(a,\theta_0)\Gamma^{-1}g(x,\theta_0),
\]
(13)
where $G(a,\theta):=E[a(X)g'(X,\theta)]$ and $\Gamma:=E[g(X,\theta_0)g'(X,\theta_0)]$ is assumed to be non-singular. The linear operator $\Pi$ projects orthogonally onto the orthocomplement of the conditional score $g$.''',[8],[9],[r'\Pi a(x)',r'\Gamma^{-1}g(x,\theta_0)'],'Population L2(P_X) projection off the p-dimensional score span, with a nonsingular score Gram matrix. This is distinct from both the empirical projection and the L2(mu) eigenbasis; nonsingularity is not replaced by a generalized inverse. L2(X) means square-integrable measurable functions of X as defined on page3.','Section 3.2 — Population orthogonal projection (13)')
add(11,'Neyman-orthogonal kernel',r'''Define the kernel
\[
\Upsilon(x_1,x_2)=g'(x_1,\theta_0)\Gamma^{-1}g(x_2,\theta_0).
\]
\[
K^\perp(x_i,x_j):=K(x_i,x_j)-E[\Upsilon(X,x_i)K(X,x_j)]-E[\Upsilon(X,x_j)K(X,x_i)]+E[\Upsilon(x_i,X)K(X,\widetilde X)\Upsilon(\widetilde X,x_j)].
\]
The kernel $K^\perp$ is called the Neyman-orthogonal kernel pertaining to $\Pi A$. These kernels are also referred in the literature to as “reduced” kernels.''',[8],[1,9,10],[r'K^\perp(x_i,x_j)',r'\Upsilon(x_1,x_2)'],'Original defining formula inside Lemma3.3, plus its preceding auxiliary kernel and following name; the lemma is not added to the theorem inventory. Xtilde is an independent copy in the joint-source convention. Kperp uses population expectations and population Gamma, not the fitted Gram matrix.','Section 3.2 and Lemma 3.3 — Neyman-orthogonal kernel')
add(12,'sample analog',r'''and $\widehat\Pi a(X_i)=a(X_i)-G_n(a,\widehat\theta)\Gamma_n^{-1}g(X_i,\widehat\theta)$ is the sample analog of $\Pi a$ in (13), with $G_n(a,\theta)=n^{-1}\sum_{i=1}^ng'(X_i,\theta)a(X_i)$ and $\Gamma_n=n^{-1}\sum_{i=1}^ng(X_i,\widehat\theta)g'(X_i,\widehat\theta)$. Note the matrix $\Gamma_n$ is non-singular for a sufficiently large $n$, by Assumption B in Section 4.2.''',[9],[9,10],[r'\widehat\Pi a(X_i)',r'\Gamma_n^{-1}'],'Sample projection uses fitted conditional scores and empirical averaging, while theta-hat is the supplied estimator. The source claims eventual nonsingularity under B but gives no rule for singular finite samples. That applicability claim does not make B part of the definition body or create a dependency cycle.','Section 3.3 — Sample projection following (15)')
add(13,'Gram matrix',r'''2. Compute the $n\times p$ matrix of scores $\mathbb G$ with $i$-th row $g(X_i,\widehat\theta)'$, $i=1,\ldots,n$.
3. Let $\mathbb K$ be a Gram matrix with $ij$-th element $K(X_i,X_j)/n$, $i,j=1,\ldots,n$.
4. Compute $\widehat{\mathbb K}=\widehat\Pi_{\mathbb G}'\mathbb K\widehat\Pi_{\mathbb G}$, where $\widehat\Pi_{\mathbb G}=I_n-\mathbb G(\mathbb G'\mathbb G)^{-1}\mathbb G'$ and $I_n$ is the $n\times n$ identity matrix.''',[8],[1,9],[r'K(X_i,X_j)/n',r'\widehat{\mathbb K}',r'\widehat\Pi_{\mathbb G}'],'Algorithm1 steps2–4: the raw Gram matrix contains exactly one factor1/n; the fitted projection is applied on both sides. AssumptionB(ii) names the raw mathbb K, not the projected matrix. Population G(a,theta), sample G_n and the score design mathbb G are separate objects.','Algorithm 1 — Score design and Gram matrices')
add(14,'Neyman-orthogonal function-parametric empirical process',r'''where $\widehat R_n(a)$ is the Neyman-orthogonal function-parametric empirical process given by
\[
\widehat R_n(a)=\frac1{\sqrt n}\sum_{i=1}^n(\widehat\Pi a(X_i))\widehat\varepsilon_i,\qquad a\in\mathcal H_K,
\]
(15)''',[9],[2,12,23],[r'\widehat R_n(a)',r'\frac1{\sqrt n}'],'Feasible dual-valued process with fitted residuals and fitted score projection, indexed by the original RKHS. It is not the infeasible R_n(Pi a) at the true parameter and not the resampled multiplier process.','Section 3.3 — Feasible empirical process (15)')
add(15,'test statistic',r'''5. Compute the test statistic $n\widehat Q_K^\perp=\widehat\varepsilon'\widehat{\mathbb K}\widehat\varepsilon$.
\[
n\widehat Q_K^\perp=\sup_{a\in\mathcal B_K}(\widehat R_n(a))^2,
\]
(14)''',[8,9],[13,14,23],[r'n\widehat Q_K^\perp',r'\widehat\varepsilon\prime'],'Algorithm1 step5 and its original dual representation(14). The factor n belongs to the statistic whose limit is asserted. Dependence on fitted scores/residuals is retained through their definitions; no GP integration is needed to state this empirical quadratic statistic.','Algorithm 1 and equation (14) — Test statistic')
# The source uses a prime in this expression; select its literal TeX representation.
members['D15']['highlight_symbols']=[r'n\widehat Q_K^\perp',r"\widehat\varepsilon'\widehat{\mathbb K}\widehat\varepsilon"]
add(16,'measure',r'''Define $\sigma_\varepsilon^2(X,\theta_0):=E[\varepsilon^2(Z,\theta_0)\mid X]$ and the measure $\mu$ such that $d\mu(x):=\sigma_\varepsilon^2(x,\theta_0)dF_X(x)$. We assume
\[
\kappa^\perp:=\int_{\mathcal X}K^\perp(x,x)d\mu(x)<\infty.
\]
(16)''',[9],[7,11],[r'd\mu(x):=\sigma_\varepsilon^2(x,\theta_0)dF_X(x)',r'\kappa^\perp'],'Conditional second-moment-weighted measure, not necessarily a probability measure. sigma_epsilon squared is not a conditional variance outside H0. The kappa-perp integrability clause is later explicitly consumed by B(ii).','Section 3.4 — Weighted measure and integrability (16)')
add(17,'Spectral Representations',r'''Let $L_2(\mu)$ denote the Hilbert space of $\mu$-square integrable measurable functions of $X$. Under (16), the linear operator $T_{K^\perp}:L_2(\mu)\to L_2(\mu)$ defined by
\[
T_{K^\perp}f(x_2):=\int_{\mathcal X}K^\perp(x_1,x_2)f(x_1)d\mu(x_1)
\]
is trace class and self-adjoint, with a sequence of eigenelements $\{\lambda_j,\varphi_j(\cdot)\}_{j\in\mathbb N}$ such that $\lambda_j\ge0$, and $\{\varphi_j(\cdot)\}_{j\in\mathbb N}$ are orthonormal in $L_2(\mu)$. Moreover, the following expansion holds in an $L_2(\mu\times\mu)$ sense, see Theorem 3.1 in [34],
\[
K^\perp(x_1,x_2)=\sum_{j=1}^\infty\lambda_j\varphi_j(x_1)\varphi_j(x_2),\qquad\mu\times\mu\text{-a.s.}
\]
(17)''',[10],[11,16],[r'T_{K^\perp}',r'\lambda_j',r'\varphi_j'],'Integral-operator spectrum in the weighted L2(mu), not the covariance-operator spectrum orthonormal in H_K. The source explicitly states an L2 and almost-everywhere expansion, not uniform pointwise convergence. Its nonnegative eigenvalue convention leaves zero modes and RKHS representatives implicit.','Section 3.4 — Spectral Representations',context='3.4. Spectral Representations.',context_page=9)
add(18,'measure',r'''Let $\Theta_0$ be an arbitrary small neighborhood around $\theta_0$ in $\mathbb R^p$. Define the measure $d\mu_s(x)=\sigma_s^2(x,\theta_0)dF_X(x)$, where $\sigma_s^2(X,\theta_0)=E[s(Z,\theta_0)s'(Z,\theta_0)\mid X]$. Set $\kappa_s:=\int_{\mathcal X}K(x,x)d\mu_s(x)$. Let $\lambda_{\max}(V)$ denote the maximum eigenvalue of the positive semidefinite symmetric matrix $V$. Define $\dot g(x,\theta):=(\partial/\partial\theta)g(x,\theta)$ and $\dot s(z,\theta):=(\partial/\partial\theta)s(z,\theta)$.''',[11],[1,9],[r'd\mu_s(x)',r'\kappa_s',r'\dot s(z,\theta)'],'Source score-second-moment measure and differentiability notation. For p>1, s*s-prime is matrix-valued, while the source writes kappa_s<infinity without specifying a scalarization. Preserve this ambiguity; do not silently replace it by a trace. Theta_0 is a small Euclidean neighborhood, including possible boundary-domain questions.','Section 4.2 — Score measure and derivative notation')
add(19,'Assumption B',r'''(i) $\mathcal X$ is separable, $K$ is continuous and $E[K(X,X)]<\infty$; (ii) $\kappa^\perp,\kappa_s<\infty$, and $\lambda_{\max}(\mathbb K)=O_P(n^{-1})$; (iii) $\varepsilon(Z,\theta)$ is twice continuously differentiable in $\Theta$, a.s., with a score satisfying $E[\sup_{\theta\in\Theta_0}|s(Z,\theta)|^2]<\infty$ and $E[\sup_{\theta\in\Theta_0}|\dot s(Z,\theta)|^2]<\infty$. Furthermore, $E[g(X,\theta)g'(X,\theta)]$ is positive definite in $\Theta_0$ and $E[\sup_{\theta\in\Theta_0}(\varepsilon(Z,\theta))^2]<\infty$; (iv) $\Theta$ is compact in $\mathbb R^p$ and $|\widehat\theta-\theta_0|=O_P(n^{-1/2})$.''',[11,12],[1,7,9,13,16,18],[r'\lambda_{\max}(\mathbb K)=O_P(n^{-1})',r'|\widehat\theta-\theta_0|=O_P(n^{-1/2})'],'Full AssumptionB(i)–(iv) as it exists at Theorems4.3 and4.4. Preserve the raw-Gram eigenvalue order, every uniform moment bound, nonsingular conditional-score Gram and root-n stochastic rate. Later B(v) is only introduced for local-power Proposition4.5. A root-n rate does not assert an asymptotic linear expansion or almost-sure estimator rate.','Assumption B(i)–(iv)',kind='assumption',context='Assumption B',phrases=['Assumption B'])
add(20,'Bootstrap-Based Tests',r'''We approximate the asymptotic non-pivotal distribution of $\widehat R_n$ by that of $\widehat R_n^*$, where
\[
\widehat R_n^*(a)=\frac1{\sqrt n}\sum_{i=1}^n(\widehat\Pi a(X_i))V_i\widehat\varepsilon_i,
\]
and $\{V_i\}_{i=1}^n$ is a sequence of iid random variables (r.v.'s) with zero mean, unit variance, bounded support and also independent of the original data $\{W_i\}_{i=1}^n$.''',[12],[2,12,23],[r'\widehat R_n^*(a)',r'V_i\widehat\varepsilon_i'],'Multiplier bootstrap process on the same RKHS. The fitted residuals and projection remain fixed conditional on the original data; only bounded iid mean-zero variance-one multipliers are resampled. The examples of two-point weights are optional, not extra theorem assumptions.','Section 4.3 — Bootstrap-Based Tests',context='4.3. Bootstrap-Based Tests.')
add(21,'a.s. consistency',r'''For justification of the bootstrap we use the concept of a.s. consistency, denoted by $\xrightarrow{d}$ a.s., see [21] or Chapter 2.9 in [55].''',[13],[],[], 'The source names almost-sure bootstrap consistency and cites its formal definition externally. Interpret the a.s. qualifier as applying to conditional distributional convergence over data realizations, not pathwise convergence of the resampled random statistic. No local conditional-probability metric definition is supplied.','Section 4.3 — Almost-sure bootstrap consistency',kind='source_passage',phrases=['a.s. consistency'])
add(22,'Asymptotic Null Distribution',r'''where $R_\infty(a)=\sum_{j=1}^\infty\lambda_j\langle\varphi_j,\Pi a\rangle_{K^\perp}U_j$.''',[12],[2,10,17],[r'R_\infty(a)',r'\langle\varphi_j,\Pi a\rangle_{K^\perp}'],'Limit functional defined within Theorem4.3 and reused by Theorem4.4. U_j are iid standard normals under the standing convention on page11. Preserve lambda_j and the projected-kernel RKHS inner product: varphi_j is normalized in L2(mu), unlike the abstract covariance basis in Theorem4.1. No AssumptionA or H0 is smuggled into this formula’s definition dependencies.','Theorem 4.3 — Limit functional',kind='theorem_excerpt',context='4.2. Asymptotic Null Distribution.',context_page=11)
add(23,'residuals',r'''1. Obtain $\widehat\theta$ and construct the residuals $\widehat\varepsilon=(\widehat\varepsilon_1,\ldots,\widehat\varepsilon_n)'$, $\widehat\varepsilon_i=\varepsilon(Z_i,\widehat\theta)$, $i=1,\ldots,n$.''',[8],[7],[r'\widehat\varepsilon_i=\varepsilon(Z_i,\widehat\theta)'],'Residuals evaluated at the supplied fitted parameter. Their definition imposes no estimator rate; the root-n requirement is separately in B(iv). They are held fixed in the multiplier bootstrap rather than recomputed from a resampled estimator.','Algorithm 1 — Fitted residuals')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
