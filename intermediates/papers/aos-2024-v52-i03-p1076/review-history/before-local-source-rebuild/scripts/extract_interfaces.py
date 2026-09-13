"""Transcribe spectral two-sample prerequisites from the main text only."""
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
add('D1','two-sample testing',r'''Given $\mathbb X_N:=(X_i)_{i=1}^N\overset{i.i.d.}{\sim}P$, and $\mathbb Y_M:=(Y_j)_{j=1}^M\overset{i.i.d.}{\sim}Q$, where $P$ and $Q$ are defined on a measurable space $\mathcal X$, the problem of two-sample testing is to test $H_0:P=Q$ against $H_1:P\ne Q$.''',[1],'Section 1 — two-sample testing setup',kind='source_passage',symbols=[r'\mathbb X_N',r'\mathbb Y_M',r'H_0:P=Q'],shape='Two iid sample collections from distributions on a common measurable space, with equality versus inequality hypotheses. Blackboard-bold sample collections are distinct from individual observations.')
add('D2','RKHS of real-valued functions',r'''$(\mathcal X,\mathcal B)$ is a second countable (i.e., completely separable) space endowed with Borel $\sigma$-algebra $\mathcal B$. $(\mathscr H,K)$ is an RKHS of real-valued functions on $\mathcal X$ with a continuous reproducing kernel $K$ satisfying $\sup_x K(x,x)\le\kappa$.''',[6],'Assumption (A0)',kind='assumption',symbols=[r'\sup_x K(x,x)\le\kappa'],shape='Throughout-paper topological and kernel assumption: a second-countable domain with its Borel sigma algebra and a continuous bounded-diagonal real reproducing kernel. The source parenthetical completely separable is retained, not strengthened to completeness or a Polish-space hypothesis.')
add('D3','RKHS embedding',r'''
Formally, the RKHS embedding of a probability measure $P$ is defined as
\[
\mu_P=\int_{\mathcal X}K(\cdot,x)\,dP(x)\in\mathscr H,
\]
where $K:\mathcal X\times\mathcal X\to\mathbb R$ is the unique reproducing kernel (r.k.) associated with the RKHS $\mathscr H$ with $P$ satisfying $\int_{\mathcal X}\sqrt{K(x,x)}\,dP(x)<\infty$.
''',[2],'Section 1 — RKHS mean embedding',symbols=[r'\mu_P'],shape='Kernel mean element under the source square-root-diagonal integrability condition. The definition itself does not require a characteristic or uniformly bounded kernel; A0 separately supplies boundedness in the theorems.')
add('D4',['maximum mean discrepancy','kernel distance'],r'''
If $K$ is characteristic (Sriperumbudur et al., 2010, 2011), this embedding induces a metric on the space of probability measures, called the maximum mean discrepancy (MMD) or the kernel distance (Gretton et al., 2012, 2006), defined as
\[
D_{\mathrm{MMD}}(P,Q)=\|\mu_P-\mu_Q\|_{\mathscr H}.\tag{1.1}
\]
MMD has the following variational representation (Gretton et al., 2012, Sriperumbudur et al., 2010) given by
\[
D_{\mathrm{MMD}}(P,Q):=\sup_{f\in\mathscr H:\|f\|_{\mathscr H}\le1}\int_{\mathcal X}f(x)\,d(P-Q)(x),\tag{1.2}
\]
''',[2],'Section 1 — MMD (1.1)–(1.2)',{'D3':'The discrepancy is the Hilbert norm of the difference of the two kernel mean embeddings.'},symbols=[r'D_{\mathrm{MMD}}(P,Q)'],shape='Kernel mean discrepancy and its unit-RKHS-ball variational form. The source mentions characteristic kernels when calling it a metric; A0 does not itself require characteristicness. Preserve the distinction between the definition and its metric property.')
add('D5','U-statistic estimator',r'''
Gretton et al. (2012) proposed a test based on the asymptotic null distribution of the U-statistic estimator of $D_{\mathrm{MMD}}^2(P,Q)$, defined as
\[
\begin{aligned}
\widehat D_{\mathrm{MMD}}^2(X,Y)={}&\frac1{N(N-1)}\sum_{i\ne j}K(X_i,X_j)+\frac1{M(M-1)}\sum_{i\ne j}K(Y_i,Y_j)\\
&-\frac2{NM}\sum_{i,j}K(X_i,Y_j),
\end{aligned}
\]
''',[2],'Section 1 — unbiased squared-MMD estimator',{'D1':'The estimator uses the two original sample collections and their separate sizes.','D4':'The target is the squared kernel mean discrepancy.'},symbols=[r'\widehat D_{\mathrm{MMD}}^2'],shape='Unbiased squared-MMD estimator with off-diagonal within-sample sums and all cross pairs. Its finite-sample value need not be nonnegative. Thresholds in Theorem 3.1 are bound inside that theorem, not the cited asymptotic test.')
add('D6','test',r'''Let $\phi(\mathbb X_N,\mathbb Y_M)$ be any test that rejects $H_0$ when $\phi=1$ and fails to reject $H_0$ when $\phi=0$. Denote the class of all such asymptotic (resp. exact) $\alpha$-level tests to be $\Phi_\alpha$ (resp. $\Phi_{N,M,\alpha}$).''',[2],'Section 1 — asymptotic and exact level-test classes',{'D1':'Each decision is a function of the two sample collections and tests the equality hypothesis.'},symbols=[r'\Phi_{N,M,\alpha}',r'\Phi_\alpha'],shape='Binary test convention and the two named level-alpha classes. Theorem 3.2 takes the infimum over the exact finite-sample class. Do not replace it by the asymptotic class or silently enlarge it to randomized decisions.')
add('D7','inclusion operator',r'''
where $R=\frac{P+Q}{2}$ and $u=\frac{dP}{dR}-1$. Define $\mathfrak I:\mathscr H\to L^2(R)$, $f\mapsto[f-\mathbb E_Rf]_\sim$, which is usually referred in the literature as the inclusion operator (e.g., see Steinwart and Christmann, 2008, Theorem 4.26), where $\mathbb E_Rf=\int_{\mathcal X}f(x)\,dR(x)$. It can be shown (Sriperumbudur and Sterge, 2022, Proposition C.2) that $\mathfrak I^*:L^2(R)\to\mathscr H$, $f\mapsto\int K(\cdot,x)f(x)\,dR(x)-\mu_R\mathbb E_Rf$.
''',[6],'Section 3 — centered inclusion and adjoint',{'D3':'The adjoint subtracts the R-mean embedding multiplied by the scalar R-expectation.'},symbols=[r'\mathfrak I',r'\mathfrak I^*'],shape='Centered RKHS-to-L2 inclusion and its adjoint, with mixture reference measure R and contrast u. Fraktur I is not the identity operator. The uncentered alternative discussed in Remark 3.1 is not substituted.')
add('D8','integral operator',r'''
Define $\mathcal T:=\mathfrak I\mathfrak I^*:L^2(R)\to L^2(R)$. It can be shown (Sriperumbudur and Sterge, 2022, Proposition C.2) that $\mathcal T=\Upsilon-(1\otimes_{L^2(R)}1)\Upsilon-\Upsilon(1\otimes_{L^2(R)}1)+(1\otimes_{L^2(R)}1)\Upsilon(1\otimes_{L^2(R)}1)$, where $\Upsilon:L^2(R)\to L^2(R)$, $f\mapsto\int K(\cdot,x)f(x)\,dR(x)$.
''',[6],'Section 3 — centered integral operator',{'D7':'The centered integral operator is the inclusion composed with its adjoint, and its expanded form uses R-centering.'},symbols=[r'\mathcal T',r'\Upsilon'],context='where $\mathcal T:L^2(R)\to L^2(R)$ is an integral operator defined by $K$ (see Section 3 for details),',shape='Double-centered integral operator on L2(R), not the uncentered Upsilon operator. Kernel-dependent smoothness and spectral rates use this operator.')
members['D8']['naming_context'][0]['evidence']=[dict(page=3,location='Section 1 — name of the centered operator')]
add('D9',['eigenvalues','eigenfunctions'],r'''
Since $K$ is bounded, it is easy to verify that $\mathcal T$ is a trace class operator, and thus compact. Also, it is self-adjoint and positive, thus spectral theorem (Reed and Simon, 1980, Theorems VI.16, VI.17) yields that
\[
\mathcal T=\sum_{i\in I}\lambda_i\widetilde\phi_i\otimes_{L^2(R)}\widetilde\phi_i,
\]
where $(\lambda_i)_i\subset\mathbb R^+$ are the eigenvalues and $(\widetilde\phi_i)_i$ are the orthonormal system of eigenfunctions (strictly speaking classes of eigenfunctions) of $\mathcal T$ that span $\overline{\operatorname{Ran}(\mathcal T)}$ with the index set $I$ being either countable in which case $\lambda_i\to0$ or finite. In this paper, we assume that the set $I$ is countable, i.e., infinitely many eigenvalues. Note that $\widetilde\phi_i$ represents an equivalence class in $L^2(R)$. By defining $\phi_i:=\frac{\mathfrak I^*\widetilde\phi_i}{\lambda_i}$, it is clear that $\mathfrak I\phi_i=[\phi_i-\mathbb E_R\phi_i]_\sim=\widetilde\phi_i$ and $\phi_i\in\mathscr H$. Throughout the paper, $\phi_i$ refers to this definition.
''',[6],'Section 3 — spectral system and RKHS representatives',{'D8':'The eigenvalues and L2 equivalence classes belong to the centered integral operator.','D7':'The pointwise RKHS representatives use the adjoint divided by the eigenvalue.','D2':'The source invokes boundedness of K to obtain the trace-class spectral setting.'},symbols=[r'\widetilde\phi_i',r'\phi_i',r'\lambda_i'],shape='Infinitely many positive eigenvalues with L2-normalized classes and separately defined RKHS representatives. The source sup-norm condition concerns phi_i, not an arbitrary representative of tilde-phi_i; the normalization divides by lambda_i, not its square root.')
add('D10','probability metric',r'''where $\rho^2(P,Q):=\frac12\int\frac{(dP-dQ)^2}{dP+dQ}$''',[7],'Section 3 — separation metric',symbols=[r'\rho^2(P,Q)'],context='with $\rho$ being a probability metric that is topologically equivalent to the Hellinger distance',shape='Squared separation metric given by half the triangular discrimination integral. It is not literally the squared Hellinger distance, although the source states topological equivalence.')
members['D10']['naming_context'][0]['evidence']=[dict(page=3,location='Section 1 — description of rho')]
add('D11','alternatives',r'''
This naturally leads to the class of $\Delta$-separated alternatives,
\[
\mathcal P:=\mathcal P_{\theta,\Delta}:=\left\{(P,Q):\frac{dP}{dR}-1\in\operatorname{Ran}(\mathcal T^\theta),\ \rho^2(P,Q)\ge\Delta\right\},\tag{1.4}
\]
for $\theta>0$,
''',[4],'Section 1 — smooth separated alternative class (1.4)',{'D8':'The smoothness restriction is the range of a power of the centered integral operator, which depends on the distribution pair.','D10':'The separation requirement uses rho squared, with the source normalization.'},symbols=[r'\mathcal P_{\theta,\Delta}',r'\operatorname{Ran}(\mathcal T^\theta)'],shape='Pair-dependent range-smoothness class separated in rho squared. Uniform source-norm bounds are additional theorem assumptions; they are not inserted into the original class definition. Spectral powers and the local definitions of R,u are resolved separately.')

add('D12','spectral regularizer',r'''where the spectral regularizer, $g_\lambda:(0,\infty)\to(0,\infty)$ satisfies $\lim_{\lambda\to0}xg_\lambda(x)\asymp1$ (more concrete assumptions on $g_\lambda$ will be introduced later).''',[9],'Section 4 — spectral regularizer',kind='source_passage',symbols=[r'g_\lambda:(0,\infty)\to(0,\infty)'],shape='Introductory scalar regularizer description. The open positive domain here does not assign g_lambda(0), although the subsequent functional calculus and A1–A4 use it. Do not silently extend the domain or infer extra hypotheses for the generic permutation level results.')
add('D13','functional calculus',r'''
By functional calculus, we define $g_\lambda$ applied to any compact, self-adjoint operator $\mathcal B$ defined on a separable Hilbert space, $H$ as
\[
g_\lambda(\mathcal B):=\sum_{i\ge1}g_\lambda(\tau_i)(\psi_i\otimes_H\psi_i)+g_\lambda(0)\left(I-\sum_{i\ge1}\psi_i\otimes_H\psi_i\right),\tag{4.1}
\]
where $\mathcal B$ has the spectral representation, $\mathcal B=\sum_i\tau_i\psi_i\otimes_H\psi_i$ with $(\tau_i,\psi_i)_i$ being the eigenvalues and eigenfunctions of $\mathcal B$.
''',[9],'Section 4 — functional calculus (4.1)',symbols=[r'g_\lambda(\mathcal B)',r'g_\lambda(0)'],shape='Spectral multiplier including its action on the orthogonal complement of the nonzero spectral subspace. The source says any compact self-adjoint operator although the scalar domain initially excludes zero and negative arguments; retain this domain issue. No A1–A4 inequalities are part of this construction.')
add('D14','spectral regularized discrepancy',r'''
To this end, we define the spectral regularized discrepancy as
\[
\eta_\lambda(P,Q):=4\langle\mathcal T g_\lambda(\mathcal T)u,u\rangle_{L^2(R)},
\]
''',[9],'Section 4 — population regularized discrepancy',{'D8':'The discrepancy applies the centered integral operator to the mixture contrast u.','D12':'The introduction describes the scalar spectral regularizer used here.','D13':'The multiplier g_lambda(T) is defined by the functional calculus (4.1).'},symbols=[r'\eta_\lambda(P,Q)'],shape='Population regularized squared discrepancy with the original factor four. This auxiliary population target is not a theorem dependency merely because it occurs in the power proofs. The inconsistent unsquared supremum in Remark 4.2 is retained separately as a source issue.')
add('D15','covariance operator',r'''
Define $\Sigma_R:=\Sigma_{PQ}=\mathfrak I^*\mathfrak I:\mathscr H\to\mathscr H$, which is referred to as the covariance operator. It can be shown (Sriperumbudur and Sterge, 2022, Proposition C.2) that $\Sigma_{PQ}$ is a positive, self-adjoint, trace-class operator, and can be written as
\[
\begin{aligned}
\Sigma_{PQ}&=\int_{\mathcal X}(K(\cdot,x)-\mu_R)\otimes_{\mathscr H}(K(\cdot,x)-\mu_R)\,dR(x)\\
&=\frac12\int_{\mathcal X\times\mathcal X}(K(\cdot,x)-K(\cdot,y))\otimes_{\mathscr H}(K(\cdot,x)-K(\cdot,y))\,dR(x)\,dR(y),\tag{4.2}
\end{aligned}
\]
where $\mu_R=\int_{\mathcal X}K(\cdot,x)\,dR(x)$.
''',[10],'Section 4 — mixture covariance operator (4.2)',{'D7':'The covariance is the adjoint inclusion composed with the centered inclusion.','D3':'Its first integral subtracts the kernel mean under the mixture R.'},symbols=[r'\Sigma_{PQ}',r'\Sigma_R'],shape='Centered RKHS covariance under the mixture R=(P+Q)/2, with its pairwise difference representation and factor one half. It differs from the centered L2 operator T and from the sum of within-group covariances.')
add('D16','covariance operator',r'''Define $\Sigma_{PQ,\lambda}:=\Sigma_{PQ}+\lambda I$.''',[10],'Section 4 — shifted covariance operator',{'D15':'The shifted operator adds lambda times the identity to the mixture covariance.'},symbols=[r'\Sigma_{PQ,\lambda}'],context='Define $\Sigma_R:=\Sigma_{PQ}=\mathfrak I^*\mathfrak I:\mathscr H\to\mathscr H$, which is referred to as the covariance operator.',shape='Positive identity shift of the mixture covariance. The source gives no separate natural-language name; its covariance-operator keyword is indexed with the distinct shift passage, not asserted equivalent to the unshifted operator.')
add('D17','split the samples',r'''
We first split the samples $(X_i)_{i=1}^N$ into $(X_i)_{i=1}^{N-s}$ and $(X_i^1)_{i=1}^s:=(X_i)_{i=N-s+1}^N$, and $(Y_j)_{j=1}^M$ to $(Y_j)_{j=1}^{M-s}$ and $(Y_j^1)_{j=1}^s:=(Y_j)_{j=M-s+1}^M$. Then, the samples $(X_i^1)_{i=1}^s$ and $(Y_j^1)_{j=1}^s$ are used to estimate the covariance operator $\Sigma_{PQ}$ while $(X_i)_{i=1}^{N-s}$ and $(Y_i)_{i=1}^{M-s}$ are used to estimate the mean elements $\mu_P$ and $\mu_Q$, respectively. Define $n:=N-s$ and $m:=M-s$.
''',[11],'Section 4.1 — sample split',{'D1':'The construction reserves the last s observations of each original iid collection.','D15':'The reserved samples estimate the mixture covariance.','D3':'The remaining samples estimate the two kernel mean elements.'},symbols=[r'n:=N-s',r'm:=M-s',r'X_i^1',r'Y_j^1'],shape='Separate last-s blocks reserved from each group; n,m are remaining group sizes. Theorems that choose s proportional to both original sizes add their own conditions; no such proportionality is imposed by this split definition.')
add('D18','one-sample U-statistic estimator',r'''
\[
\widehat\Sigma_{PQ}:=\frac1{2s(s-1)}\sum_{i\ne j}^s(K(\cdot,Z_i)-K(\cdot,Z_j))\otimes_{\mathscr H}(K(\cdot,Z_i)-K(\cdot,Z_j)),
\]
which is a one-sample U-statistic estimator of $\Sigma_{PQ}$ based on $Z_i=\alpha_iX_i^1+(1-\alpha_i)Y_i^1$, for $1\le i\le s$, where $(\alpha_i)_{i=1}^s\overset{i.i.d.}{\sim}\operatorname{Bernoulli}(\frac12)$. It is easy to verify that $(Z_i)_{i=1}^s\overset{i.i.d.}{\sim}R$.
''',[11],'Section 4.1 — estimated mixture covariance',{'D17':'The Bernoulli-selected observations use the two reserved blocks.','D15':'The covariance estimator discretizes the pairwise representation of the mixture covariance.'},symbols=[r'\widehat\Sigma_{PQ}',r'Z_i=\alpha_iX_i^1+(1-\alpha_i)Y_i^1'],shape='Pairwise covariance estimate from iid mixture observations constructed from reserved data. The original linear-combination notation for binary selection is preserved even though A0 permits a general domain; independence of selector randomness is the sampling construction convention, not a vector-space assumption.')
add('D19','two-sample U-statistic',r'''
Using the form of $\eta_\lambda$ in (4.5), we estimate it using a two-sample U-statistic (Hoeffding, 1992),
\[
\widehat\eta_\lambda:=\frac1{n(n-1)}\frac1{m(m-1)}\sum_{1\le i\ne j\le n}\sum_{1\le i'\ne j'\le m}h(X_i,X_j,Y_{i'},Y_{j'}),\tag{4.6}
\]
where
\[
h(X_i,X_j,Y_{i'},Y_{j'}):=\left\langle g_\lambda^{1/2}(\widehat\Sigma_{PQ})A(X_i,Y_{i'}),g_\lambda^{1/2}(\widehat\Sigma_{PQ})A(X_j,Y_{j'})\right\rangle_{\mathscr H},
\]
''',[11],'Section 4.1 — regularized statistic (4.6)',{'D13':'The square-root multiplier of the estimated covariance uses the functional calculus.','D18':'The random operator inside the statistic is the reserved-sample covariance estimate.','D17':'The U-statistic sums over the two remaining samples, with sizes n and m.'},symbols=[r'\widehat\eta_\lambda',r"h(X_i,X_j,Y_{i'},Y_{j'})"],shape='Finite-sample regularized statistic, conditionally a two-sample U-statistic given the reserved mixture observations. The inline feature difference A is retained as unranked auxiliary passage A10. Its displayed formula determines it without a population target, smoothness class, or A1–A4. The introductory target reference is contextual and not a prerequisite of the formula.')

# Unpack the four numbered assumptions without transferring them into level-only tests.
regularizer_context='where the spectral regularizer, $g_\lambda:(0,\infty)\to(0,\infty)$ satisfies $\lim_{\lambda\to0}xg_\lambda(x)\asymp1$ (more concrete assumptions on $g_\lambda$ will be introduced later).'
common=r'''where $\Gamma:=[0,\kappa]$, $\varphi\in(0,\xi]$ with the constant $\xi$ being called the qualification of $g_\lambda$, and $C_1$, $C_2$, $C_3$, $B_3$, $C_4$ are finite positive constants, all independent of $\lambda>0$.'''
for lid,num,formula,shape in [
 ('D21',1,r'\sup_{x\in\Gamma}|xg_\lambda(x)|\le C_1','Uniform upper bound on x times the regularizer.'),
 ('D22',2,r'\sup_{x\in\Gamma}|\lambda g_\lambda(x)|\le C_2','Uniform upper bound on lambda times the regularizer.'),
 ('D23',3,r'\sup_{\{x\in\Gamma:xg_\lambda(x)<B_3\}}|B_3-xg_\lambda(x)|x^{2\varphi}\le C_3\lambda^{2\varphi}','Restricted-sublevel approximation condition for every qualification exponent varphi in (0,xi]. This is weaker than the usual uniform residual condition with B3=1; do not replace it by that condition or assign Tikhonov qualification one half.'),
 ('D24',4,r'\inf_{x\in\Gamma}g_\lambda(x)(x+\lambda)\ge C_4','Uniform positive lower bound on the shifted scalar multiplier, including at zero; this condition is not needed by the generic permutation level theorem.')]:
    add(lid,'spectral regularizer','\\[\n'+formula+'\n\\]\n'+common,[12],f'Assumption (A{num})',kind='assumption',symbols=[formula],context=regularizer_context,shape=shape+' The original shared constant/domain paragraph is archived with each condition; only its applicable constants are consumed by that condition.')
    members[lid]['naming_context'][0]['evidence']=[dict(page=9,location='Section 4 — scalar regularizer terminology')]
add('D25',['intrinsic dimensionality','degrees of freedom'],r'''
Define
\[
\mathcal N_1(\lambda):=\operatorname{Tr}(\Sigma_{PQ,\lambda}^{-1/2}\Sigma_{PQ}\Sigma_{PQ,\lambda}^{-1/2})\quad\text{and}\quad\mathcal N_2(\lambda):=\left\|\Sigma_{PQ,\lambda}^{-1/2}\Sigma_{PQ}\Sigma_{PQ,\lambda}^{-1/2}\right\|_{\mathcal L^2(\mathscr H)},
\]
which capture the intrinsic dimensionality (or degrees of freedom) of $\mathscr H$.
''',[13],'Section 4.2 — effective dimensions',{'D16':'Both dimensions use the inverse square root of the shifted mixture covariance.','D15':'The sandwiched unshifted operator is the mixture covariance.'},symbols=[r'\mathcal N_1(\lambda)',r'\mathcal N_2(\lambda)'],shape='Two distinct effective-dimension quantities: trace and Hilbert–Schmidt norm, respectively. N2 is the norm rather than its square; do not merge their roles in separate oracle and power conditions.')
add('D26','assumption',r'''$M<N<DM$ for some constant $D\ge1$.''',[14],'Assumption (B)',kind='assumption',symbols=[r'M<N<DM'],context='For the rest of the paper, we make the following assumption.',shape='Strict sample-size comparability assumed from this point onward. It differs from the nonstrict comparability explicitly bound in Theorems 3.1 and 3.2; do not apply B retroactively.')

add('D27','permutations',r'''
Define $(U_i)_{i=1}^n:=(X_i)_{i=1}^n$, and $(U_{n+j})_{j=1}^m:=(Y_j)_{j=1}^m$. Let $\Pi_{n+m}$ be the set of all possible permutations of $\{1,\ldots,n+m\}$ with $\pi\in\Pi_{n+m}$ be a randomly selected permutation from the $D$ possible permutations, where $D:=|\Pi_{n+m}|=(n+m)!$. Define $(X_i^\pi)_{i=1}^n:=(U_{\pi(i)})_{i=1}^n$ and $(Y_j^\pi)_{j=1}^m:=(U_{\pi(n+j)})_{j=1}^m$. Let $\widehat\eta_\lambda^\pi:=\widehat\eta_\lambda(X^\pi,Y^\pi,Z)$ be the statistic based on the permuted samples. Let $(\pi_i)_{i=1}^B$ be $B$ randomly selected permutations from $\Pi_{n+m}$. For simplicity, define $\widehat\eta_\lambda^i:=\widehat\eta_\lambda^{\pi_i}$ to represent the statistic based on permuted samples w.r.t. the random permutation $\pi_i$.
''',[17],'Section 4.3 — pooled permutations with fixed covariance sample',{'D17':'Only the n+m remaining observations are pooled and permuted; the reserved mixture sample stays fixed.','D19':'Each permuted value reevaluates the same regularized statistic on reassigned X,Y groups and the original Z.'},symbols=[r'\Pi_{n+m}',r'\widehat\eta_\lambda^\pi'],shape='Permutation action on the two remaining groups, preserving the reserved covariance sample. D here is a factorial count, distinct from the comparability constant D in B. Uniform independent permutation draws are the probabilistic interpretation needed by the stated empirical-CDF guarantee; the source prose says randomly selected.')
add('D28','permutation distribution function',r'''
Given the samples $(X_i)_{i=1}^n$, $(Y_j)_{j=1}^m$ and $(Z_i)_{i=1}^s$, define
\[
F_\lambda(x):=\frac1D\sum_{\pi\in\Pi_{n+m}}\mathbb1(\widehat\eta_\lambda^\pi\le x)
\]
to be the permutation distribution function, and define
\[
q_{1-\alpha}^\lambda:=\inf\{q\in\mathbb R:F_\lambda(q)\ge1-\alpha\}.
\]
''',[17],'Section 4.3 — full permutation distribution and quantile',{'D27':'The exact CDF averages over all pooled permutations and their statistic values.'},symbols=[r'F_\lambda(x)',r'q_{1-\alpha}^\lambda'],shape='Conditional full-enumeration CDF and left quantile for the regularized statistic. This is auxiliary context for the empirical construction, not the different whole-sample MMD quantile bound inline in Theorem 3.1.')
add('D29','empirical permutation distribution function',r'''
Furthermore, we define the empirical permutation distribution function based on $B$ random permutations as
\[
\widehat F_\lambda^B(x):=\frac1B\sum_{i=1}^B\mathbb1(\widehat\eta_\lambda^i\le x),
\]
and define
\[
\widehat q_{1-\alpha}^{B,\lambda}:=\inf\{q\in\mathbb R:\widehat F_\lambda^B(q)\ge1-\alpha\}.
\]
''',[17],'Section 4.3 — sampled permutation distribution and quantile',{'D27':'The empirical CDF averages the B randomly permuted statistic values.'},symbols=[r'\widehat F_\lambda^B(x)',r'\widehat q_{1-\alpha}^{B,\lambda}'],shape='Empirical CDF and left quantile from B random permutations, without adding the original statistic as a B+1st point. The theorem-specific quantile level substitutes w alpha or its multiplicity-adjusted value; all rejection inequalities remain nonstrict as printed.')
add('D30','finite set',r'''Define $\Lambda:=\{\lambda_L,2\lambda_L,\ldots,\lambda_U\}$, where $\lambda_U=2^b\lambda_L$, for $b\in\mathbb N$. Clearly $|\Lambda|=b+1=1+\log_2\frac{\lambda_U}{\lambda_L}$ is the cardinality of $\Lambda$.''',[19],'Section 4.4 — dyadic regularization grid',symbols=[r'\Lambda',r'\lambda_U=2^b\lambda_L'],context='In this section, we construct a test based on the union (aggregation) of multiple tests for different values of $\lambda$ taking values in a finite set, $\Lambda$, that guarantees to be minimax optimal (up to log factors) for a wide range of $\theta$ (and $\beta$ in case of polynomially decaying eigenvalues).',shape='Finite dyadic regularization grid with an exact power-of-two endpoint ratio. Adaptation theorem formulas specify endpoints without an explicit rounding convention enforcing this relation; retain that source compatibility issue.')
add('D31','local alternatives',r'''
\[
\widetilde{\mathcal P}:=\widetilde{\mathcal P}_{\theta,\Delta,K}:=\left\{(P,Q):\frac{dP}{dR}-1\in\operatorname{Ran}(\mathcal T_K^\theta),\ \rho^2(P,Q)\ge\Delta\right\},
\]
with $\mathcal T_K$ being defined similar to $\mathcal T$ for $K\in\mathcal K$.
''',[21],'Section 4.5 — kernel-indexed alternative class',{'D8':'For each kernel K, the operator T_K uses the centered integral-operator construction.','D10':'The pair is separated by the same rho-squared metric.'},symbols=[r'\widetilde{\mathcal P}_{\theta,\Delta,K}',r'\mathcal T_K'],context='In the discussion so far, a kernel is first chosen which determines the test statistic, the test, and the set of local alternatives, $\mathcal P$.',shape='Alternative class indexed by the chosen kernel, with its own centered operator and range smoothness. Do not require one pair to satisfy every kernel-specific class or replace the theorem infimum over kernels by an intersection of alternatives.')
add('D32','test statistic',r'''
Let $\widehat\eta_{\lambda,K}$ be the test statistic based on kernel $K$ and regularization parameter $\lambda$. We reject $H_0$ if $\widehat\eta_{\lambda,K}\ge\widehat q_{1-\frac{w\alpha}{|\Lambda||\mathcal K|}}^{B,\lambda,K}$ for any $(\lambda,K)\in\Lambda\times\mathcal K$. Similar to Theorem 4.10, it can be shown that this test has level $\alpha$ if $|\mathcal K|<\infty$.
''',[21],'Section 4.5 — aggregation over a finite kernel family',{'D19':'Each kernel-indexed statistic is the construction (4.6) with that kernel.','D29':'The corresponding empirical permutation quantile is recomputed for that kernel and regularization value.','D30':'The rejection event ranges over the regularization grid together with the kernel family.'},symbols=[r'\widehat\eta_{\lambda,K}',r'|\mathcal K|<\infty'],shape='Joint union test over the regularization grid and a finite kernel family, with cardinality-adjusted empirical quantiles. Kernel-specific operators, eigenvalues, eigenfunctions and covariance quantities are understood separately; their numeric values are not shared across the family.')

add('D33','smoothness index',r'''where $\operatorname{Ran}(A)$ denotes the range space of an operator $A$, $\theta$ is the smoothness index (large $\theta$ corresponds to “smooth” $u$), and $\mathcal T^\theta$ is defined by choosing $g_\lambda(x)=x^\theta$, $x\ge0$ in (4.1).''',[4],'Section 1 — range smoothness and operator powers',{'D8':'The fractional power is formed from the centered operator T.','D13':'The source explicitly defines the power by substituting the scalar power into the functional calculus (4.1).'},symbols=[r'\mathcal T^\theta',r'g_\lambda(x)=x^\theta'],shape='Spectral powers and range smoothness; the power multiplier is a separate functional-calculus substitution, not an assumption that x^theta satisfies regularizer conditions A1–A4. The inverse power in uniform source-norm bounds is understood on its spectral domain, without adding invertibility of T on all L2(R).')
for lid in ['D11','D31']:
    members[lid]['depends_on'].append('D33')
    edges[lid]['D33']='The range condition uses the source definition of the fractional operator power and smoothness index.'

if __name__=='__main__':
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source passages and their local dependencies.')
