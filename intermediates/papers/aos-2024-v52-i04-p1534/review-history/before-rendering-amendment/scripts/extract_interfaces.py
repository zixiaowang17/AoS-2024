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

add('D1','Bochner measurable functions',r'''
The space $L^2(P;\mathcal V)$ is the Hilbert space containing all Bochner measurable functions $f:\mathcal Z\to\mathcal V$ such that
\[
\|f\|_{L^2(P;\mathcal V)}:=\left(\int\|f(z)\|_{\mathcal V}^2P(dz)\right)^{1/2}<\infty.
\]
''',[4],'Section 2.1 — Hilbert-valued square integrability',symbols=[r'\|f\|_{L^2(P;\mathcal V)}'],shape='Bochner square-integrability in a real Hilbert space. The norm is taken under the indicated distribution, which need not be the distribution indexing the estimated influence function.')
add('D2','quadratic mean differentiable',r'''
Let $\mathcal P$ be a collection of distributions defined on a common Polish space $(\mathcal Z,\mathcal B)$, which we refer to as the model. Suppose that the model is dominated by a $\sigma$-finite measure $\lambda$. A submodel $\{P_\epsilon:\epsilon\in[0,\delta)\}\subset\mathcal P$ is said to be quadratic mean differentiable at $P$ if and only if there exists a score function $s\in L^2(P)$ such that
\[
\left\|p_\epsilon^{1/2}-p^{1/2}-\epsilon sp^{1/2}/2\right\|_{L^2(\lambda)}=o(\epsilon),\tag{1}
\]
where, for $\epsilon\ge0$, $p_\epsilon^{1/2}=\sqrt{\frac{dP_\epsilon}{d\lambda}}$ and $p^{1/2}=\sqrt{\frac{dP}{d\lambda}}$. Let $\mathscr P(P,\mathcal P,s)$ refer to the set of quadratic mean differentiable submodels at $P$ with score function $s$.
''',[4],'Section 2.2 — quadratic mean differentiable submodels (1)',symbols=[r'\mathscr P(P,\mathcal P,s)',r'\epsilon sp^{1/2}/2'],shape='One-sided dominated submodels with square-root-density expansion in L2(lambda). Keep [0,delta), the factor one-half and score/base-law indexing.')
add('D3','tangent space',r'''
The set $\{s\in L^2(P):\mathscr P(P,\mathcal P,s)\ne\varnothing\}$ is called the tangent set, and its closed linear span is called the tangent space of $\mathcal P$ at $P$, denoted by $\dot{\mathcal P}_P$. For all $s\in\dot{\mathcal P}_P$, $Ps=\int s\,dP=0$. We let $L^2_0(P):=\{h\in L^2(P):Ph=0\}$, which is the largest possible tangent space at $P$. Any model with this tangent space at all distributions $P$ it contains is referred to as locally nonparametric.
''',[4],'Section 2.2 — tangent set and tangent space',{'D2':'The tangent set consists of scores admitted by quadratic mean differentiable submodels.'},symbols=[r'\dot{\mathcal P}_P'],shape='Closed linear span of admitted scores, distinct from the tangent set. The general theorems do not assume a locally nonparametric model.')
add('D4','pathwise differentiable',r'''
Let $\mathcal H$ be a set known as the action space and $\nu:\mathcal P\to\mathcal H$ a parameter whose value is to be estimated. Throughout we assume that $\mathcal H$ is a real separable Hilbert space. The parameter $\nu$ is said to be pathwise differentiable at $P$ if and only if there exists a continuous linear operator $\dot\nu_P:\dot{\mathcal P}_P\to\mathcal H$ such that, for all $\{P_\epsilon:\epsilon\in[0,\delta)\}\in\mathscr P(P,\mathcal P,s)$,
\[
\|\nu(P_\epsilon)-\nu(P)-\epsilon\dot\nu_P(s)\|_{\mathcal H}=o(\epsilon).\tag{2}
\]
''',[4],'Section 2.2 — pathwise differentiability (2)',{'D3':'The continuous linear derivative is defined on the tangent space.','D2':'The norm expansion holds along every admitted quadratic mean differentiable submodel.'},symbols=[r'\dot\nu_P',r'\|\nu(P_\epsilon)-\nu(P)-\epsilon\dot\nu_P(s)\|_{\mathcal H}'],shape='Hilbert-norm differentiation along every submodel via a bounded linear local parameter. This does not itself imply a Hilbert-valued EIF exists.')
add('D5','efficient influence operator',r'''
The operator $\dot\nu_P$ is called the local parameter of $\nu$ at $P$ and its Hermitian adjoint, denoted by $\dot\nu_P^*:\mathcal H\to\dot{\mathcal P}_P$, is referred to as the efficient influence operator.
''',[4,5],'Section 2.2 — local parameter and its adjoint',{'D4':'The efficient influence operator is the Hilbert adjoint of the pathwise derivative.'},symbols=[r'\dot\nu_P^*:\mathcal H\to\dot{\mathcal P}_P'],shape='Bounded operator into score equivalence classes, distinct from its pointwise functional at a particular observation.')
add('D6','local parameter space',r'''
The image of the local parameter $\dot\nu_P$, denoted by $\dot{\mathcal H}_P$, is a closed subspace of $\mathcal H$ that is referred to as the local parameter space. Throughout we equip $\dot{\mathcal H}_P$ with the inner product $\langle\cdot,\cdot\rangle_{\mathcal H}$, so that $\dot{\mathcal H}_P$ is itself a Hilbert space.
''',[5],'Section 2.2 — local parameter space',{'D4':'The stated local parameter space is the image of the pathwise derivative.'},symbols=[r'\dot{\mathcal H}_P'],shape='The source calls the image closed rather than defining its closure or imposing a closed-range condition. A bounded linear operator need not have closed range; preserve this source issue.')
add('D7','efficient influence process',r'''
At times in this work, we will consider pointwise evaluations of the efficient influence operator of the form $\dot\nu_P^*(h)(z)$. When doing so, we always assume that suitably ‘nice’ elements of the $P$-a.s. equivalence classes defined by the elements $\dot\nu_P^*(h)$ of $L^2(P)$ are used to define these evaluations. In particular, we select these elements so that the efficient influence process, which we define as $\{\dot\nu_P^*(h):h\in\mathcal H\}$, is a separable stochastic process, in the sense that there exists a countable dense subset $\mathcal H'$ of $\mathcal H$ and a $P$-probability one subset $\mathcal Z'$ of $\mathcal Z$ such that, for all $h\in\mathcal H$ and $z\in\mathcal Z'$, there exists an $\mathcal H'$-valued sequence $(h_j)_{j=1}^\infty$ that converges to $h$ and satisfies $\dot\nu_P^*(h_j)(z)\to\dot\nu_P^*(h)(z)$ as $j\to\infty$.
''',[5],'Section 2.2 — selected versions and separable efficient influence process',{'D5':'Pointwise evaluation uses selected representatives of the efficient influence operator outputs.'},symbols=[r'\{\dot\nu_P^*(h):h\in\mathcal H\}',r'\dot\nu_P^*(h_j)(z)\to\dot\nu_P^*(h)(z)'],shape='Common full-measure set and dense-index approximation convention, not separate exceptional sets for every h.')
add('D8','efficient influence function',r'''
The parameter $\nu$ is said to have an EIF $\phi_P:\mathcal Z\to\mathcal H$ when there exists a $P$-probability-one set $\mathcal Z'$ such that
\[
\dot\nu_P^*(h)(z)=\langle h,\phi_P(z)\rangle_{\mathcal H}\qquad\text{for all }(h,z)\in\mathcal H\times\mathcal Z'.\tag{3}
\]
By the Riesz representation theorem, $\nu$ has an EIF if and only if $\dot\nu_P^*(\cdot)(z):\mathcal H\to\mathbb R$ is a bounded linear functional $P$-almost surely; in those cases, $\phi_P(z)$ is $P$-a.s. equal to the Riesz representation of $\dot\nu_P^*(\cdot)(z)$.
''',[5],'Section 2.2 — efficient influence function (3)',{'D5':'The EIF represents the pointwise efficient influence operator by an inner product.','D7':'The definition uses the selected representatives and common almost-sure version convention.'},context='One-step estimation based on the efficient influence function',context_pages=[6],symbols=[r'\dot\nu_P^*(h)(z)=\langle h,\phi_P(z)\rangle_{\mathcal H}'],shape='Hilbert-valued Riesz representative on one common full-measure set. Bochner square-integrability is separately imposed where needed.')
add('D9','feature map',r'''
We begin by establishing the existence and form of the EIF at a generic $P\in\mathcal P$ in an interesting class of problems. In particular, we consider cases where $\mathcal H$ is an RKHS over a space $\mathcal T$ or, more generally, the local parameter space $\dot{\mathcal H}_P$ is an RKHS over $\mathcal T$. Denote the feature map of $\dot{\mathcal H}_P$ by $t\mapsto K_t$. For $P\in\mathcal P$, define $\widetilde\phi_P:\mathcal Z\to\mathcal H$ as follows for each $t\in\mathcal T$:
\[
\widetilde\phi_P(z)(t)=\dot\nu_P^*(K_t)(z)\qquad P\text{-a.s. }z.\tag{5}
\]
''',[6],'Section 2.3 — RKHS feature map and candidate influence function (5)',{'D6':'The RKHS may be the local parameter space with its inherited inner product.','D5':'The candidate evaluates the efficient influence operator at the feature K_t.','D7':'These point evaluations use the selected versions of the efficient influence process.'},symbols=[r'\widetilde\phi_P(z)(t)=\dot\nu_P^*(K_t)(z)',r't\mapsto K_t'],shape='Feature-map formula for the candidate EIF. Preserve the source for-each-t/P-a.s.-z quantifiers. No bounded-kernel assumption from a particular example is added.')
add('D10','cross-fitting',r'''
For simplicity, we focus on the case of 2-fold cross-fitting and suppose that the sample size is an even number. The generalizations to $k$-fold cross-fitting ($k\ge2$) and to the case where $n$ is not divisible by $k$ are straightforward and so are omitted. Let $\widehat P_n^1\in\mathcal P$ denote an estimate of $P_0$ based on $\{Z_i\}_{i=1}^{n/2}$ and let $P_n^1$ denote the empirical distribution of the remainder of the sample $\{Z_i\}_{i=n/2+1}^n$. Define $\widehat P_n^2$ and $P_n^2$ similarly, but with the roles of the two subsamples reversed. We note that, in a slight abuse of notation, $P_n^j$ denotes an empirical distribution derived from $n/2$ observations rather than a $j$-fold product distribution derived from $j$ independent draws from the empirical distribution $P_n$ of the full sample $\{Z_i\}_{i=1}^n$.
''',[9],'Section 2.5 — two-fold sample split',symbols=[r'\widehat P_n^1\in\mathcal P',r'\{Z_i\}_{i=n/2+1}^n'],shape='Complementary training/evaluation halves of an even-sized iid sample. P_n^j is the held-out empirical measure, distinct from a product law.')
add('D11','cross-fitted one-step estimator',r'''
This cross-fitted one-step estimator takes the form $\bar\nu_n:=\frac12\sum_{j=1}^2[\nu(\widehat P_n^j)+P_n^j\phi_n^j]$, where $\phi_n^j:=\phi_{\widehat P_n^j}$.
''',[9],'Section 2.5 — cross-fitted one-step estimator',{'D10':'Each plug-in and EIF is trained on one half and evaluated on the opposite half.','D8':'The correction uses the EIF at each fitted distribution.'},symbols=[r'\bar\nu_n:=\frac12\sum_{j=1}^2',r'\phi_n^j:=\phi_{\widehat P_n^j}'],shape='Average of held-out one-step corrections targeting the untransformed parameter.')
add('D12','remainder terms',r'''
where $\mathcal R_n^j:=\nu(\widehat P_n^j)+P_0\phi_n^j-\nu(P_0)$ and $\mathcal D_n^j:=(P_n^j-P_0)(\phi_n^j-\phi_0)$. We call $\mathcal R_n^j$ the remainder terms and $\mathcal D_n^j$ the drift terms, $j\in\{1,2\}$.
''',[13],'Section 4.1 — remainder and drift terms after (21)',{'D10':'Both terms use the same training/evaluation folds.','D8':'They involve the fitted-law and true-law efficient influence functions.'},symbols=[r'\mathcal R_n^j',r'\mathcal D_n^j'],shape='Two distinct errors in one original passage: the population expansion remainder and held-out empirical drift. Their separate negligibility assumptions remain intact.')
interfaces[-1]['source_keywords'].append(dict(paper_id=PID,local_id='D12',source_text='drift terms',label='Drift terms',kind='term'))
interfaces[-1]['name']='Remainder terms · Drift terms'
add('D13','regular',r'''
An estimator sequence $(\widetilde\nu_n)_{n=1}^\infty$ is said to be regular at $P_0\in\mathcal P$ if and only if there is a tight $\mathcal H$-valued random variable $\widetilde{\mathbb H}$ such that, for every score in the tangent set, quadratic mean differentiable submodel $\{P_\epsilon:\epsilon\}\in\mathscr P(P_0,\mathcal P,s)$, and every sequence $\epsilon_n=O(n^{-1/2})$, $\sqrt n[\widetilde\nu_n-\nu(P_{\epsilon_n})]$ converges weakly to $\widetilde{\mathbb H}$ under iid sampling of $n$ observations from $P_{\epsilon_n}$. We say that an estimator $\widetilde\nu_n$ is regular when the implied estimator sequence $(\widetilde\nu_n)_{n=1}^\infty$ is clear from context.
''',[14],'Section 4.1 — regular estimator sequence',{'D2':'Regularity is tested along quadratic mean differentiable submodels and local parameter sequences.','D3':'The quantifier ranges over scores in the tangent set, not arbitrary elements of its closed span.'},symbols=[r'\epsilon_n=O(n^{-1/2})',r'\sqrt n[\widetilde\nu_n-\nu(P_{\epsilon_n})]'],shape='Common tight law under every local submodel sequence. Admissibility in the one-sided submodel domain is implicit; no two-sided extension is inserted.')
add('D14','standardization operator',r'''
Our proposed confidence set is built based upon a quadratic form $w(\,\cdot\,;\Omega):h\mapsto\langle\Omega(h),h\rangle_{\mathcal H}$ that is parameterized by a standardization operator $\Omega$ that belongs to the set $\mathcal O$ of continuous, self-adjoint, positive definite linear operators mapping from $\mathcal H$ to $\mathcal H$.
''',[14],'Section 4.2 — standardization operator and quadratic form',symbols=[r'\langle\Omega(h),h\rangle_{\mathcal H}',r'\mathcal O'],shape='Bounded self-adjoint positive quadratic-form operator. No uniform coercivity, bounded inverse or unregularized inverse covariance is required by the original definition.')
add('D15','confidence set',r'''
In particular, letting $\zeta\ge0$ be a specified threshold and $\Omega_n\in\mathcal O$ an estimator of a some possibly-$P_0$-dependent operator $\Omega_0\in\mathcal O$, our confidence set will take the form
\[
\mathcal C_n(\zeta):=\{h\in\mathcal H:w(\bar\nu_n-h;\Omega_n)\le\zeta/n\}.\tag{24}
\]
''',[14,15],'Section 4.2 — confidence set (24)',{'D11':'The set is centered at the cross-fitted one-step estimator.','D14':'The inequality uses the estimated standardization operator and quadratic form.'},symbols=[r'\mathcal C_n(\zeta)',r'w(\bar\nu_n-h;\Omega_n)\le\zeta/n'],shape='Original-parameter confidence set at threshold zeta/n. The source phrase an estimator of a some is retained.')
add('D16','bootstrap',r'''
A consistent estimator of $\zeta_{1-\alpha}$ can be defined using the bootstrap (Efron, 1979). To define this estimator, we let $Z_1^\sharp,\ldots,Z_{n/2}^\sharp\overset{\mathrm{iid}}\sim P_n^2$ be sampled independently of $Z_{n/2+1}^\sharp,\ldots,Z_n^\sharp\overset{\mathrm{iid}}\sim P_n^1$. We then let $P_n^{2,\sharp}$ be the empirical distribution of $Z_1^\sharp,\ldots,Z_{n/2}^\sharp$ and $P_n^{1,\sharp}$ be the empirical distribution of $Z_{n/2+1}^\sharp,\ldots,Z_n^\sharp$. We let $\mathbb H_n^\sharp:=n^{1/2}\sum_{j=1}^2(P_n^{j,\sharp}-P_n^j)\phi_n^j/2$. The threshold $\widehat\zeta_n$ is taken to be equal to the $(1-\alpha)$-quantile of $w(\mathbb H_n^\sharp,\Omega_n)$, conditionally on the original sample $(Z_1,\ldots,Z_n)$ used to define $P_n^1$ and $P_n^2$.
''',[15],'Section 4.2 — split bootstrap and conditional threshold',{'D10':'The bootstrap separately resamples the empirical halves with the original reversed fold labels.','D8':'The bootstrap mean uses the original fitted-law EIFs held fixed.','D14':'The conditional quantile is taken after applying the estimated quadratic form.'},symbols=[r'\mathbb H_n^\sharp',r'(P_n^{j,\sharp}-P_n^j)\phi_n^j/2'],shape='Exact conditional split-bootstrap quantile. Monte Carlo approximation and refitting are not part of the threshold definition in the theorem.')
add('D17','regularized EIF',r'''
If $\nu$ is pathwise differentiable at $P$ and $\beta\in\ell^2_*$, then $r_P^\beta(\cdot)(z):\mathcal H\to\mathbb R$ is a bounded linear functional on a $P$-probability one set $\mathcal Z^\beta$ with Riesz representation
\[
\phi_P^\beta(z):=\sum_{k=1}^\infty\beta_k\dot\nu_P^*(h_k)(z)h_k.
\]
Moreover, $\sigma_P(\beta):=\|\phi_P^\beta\|_{L^2(P;\mathcal H)}=[\sum_{k=1}^\infty\beta_k^2P\dot\nu_P(h_k)^2]^{1/2}\le\|\dot\nu_P^*\|_{\mathrm{op}}\|\beta\|_{\ell^2}<\infty$.
''',[8],'Lemma 1 — definition and square-integrability of the regularized EIF',{'D5':'The series uses the efficient influence operator evaluated at the fixed basis elements.','D7':'The pointwise series and Riesz representation use the selected operator versions.','D1':'The lemma gives the Bochner square-integrability norm of the regularized function.'},kind='source_passage',context=r'Given this similarity, we call $\phi_P^\beta$ the $\beta$-regularized EIF of $\nu$ at $P$.',symbols=[r'\phi_P^\beta(z):=\sum_{k=1}^\infty\beta_k\dot\nu_P^*(h_k)(z)h_k'],shape='Original Lemma 1 passage defining the regularized function even without an original EIF. The middle sigma formula prints dot-nu without an adjoint star; preserve the type mismatch. The auxiliary record gives r_P^beta and ell2-star, so no original-EIF existence is imported.')
add('D18','regularized one-step estimator',r'''
Let $\phi_n^{j,\beta}:=\phi_{\widehat P_n^j}^\beta$. The cross-fitted $\beta$-regularized one-step estimator takes the form $\bar\nu_n^\beta:=\frac12\sum_{j=1}^2[\nu(\widehat P_n^j)+P_n^j\phi_n^{j,\beta}]$.
''',[9],'Section 2.5 — cross-fitted regularized one-step estimator',{'D10':'The estimator uses the two complementary training/evaluation halves.','D17':'The correction uses the regularized influence function at each fitted law.'},symbols=[r'\bar\nu_n^\beta:=\frac12\sum_{j=1}^2',r'\phi_n^{j,\beta}:=\phi_{\widehat P_n^j}^\beta'],shape='Regularized correction with an untransformed plug-in, targeting nu(P0). It is distinct from the tilde estimator whose plug-in targets Gamma_beta composed with nu.')
add('D19','regularization bias term',r'''
where, for $P'\in\mathcal P$, we let $\mathcal B_{P'}^\beta:=\sum_{k=1}^\infty(1-\beta_k)\langle\nu(P')-\nu(P_0),h_k\rangle_{\mathcal H}h_k$. Our formal study of the regularized one-step estimator in Section 5.1 builds on the above. Informally speaking, that study will show that the latter term above plays the role of a regularization bias term that decays as $\beta$ grows entrywise to $(1,1,1,\ldots)$ under conditions, and the leading term plays the role of a variance term whose magnitude typically grows with that of $\beta$.
''',[8],'Section 2.4 — regularization bias after (9)',symbols=[r"\mathcal B_{P'}^\beta",r"(1-\beta_k)\langle\nu(P')-\nu(P_0),h_k\rangle_{\mathcal H}"],shape='Complementary spectral coefficients of the plug-in estimation error, not of nu(P0) alone. The fixed orthonormal basis and beta-domain conventions are ambient; no EIF is needed to state this bias.')
add('D20','drift and remainder terms',r'''
To establish (25), we introduce regularized versions of the drift and remainder terms considered in Section 4.1. In particular, for $j\in\{1,2\}$ and $\beta=(\beta_k)_{k=1}^\infty\in\ell^2$, define the $\mathcal H$-valued random elements $\mathcal D_n^{j,\beta}:=(P_n^j-P_0)(\phi_n^{j,\beta}-\phi_0^\beta)$ and $\mathcal R_n^{j,\beta}:=\mathcal R_{\widehat P_n^j}^\beta$, where, for $P\in\mathcal P$,
\[
\mathcal R_P^\beta:=\nu(P)-\nu(P_0)+P_0\phi_P^\beta-\sum_{k=1}^\infty(1-\beta_k)\langle\nu(P)-\nu(P_0),h_k\rangle_{\mathcal H}h_k.\tag{26}
\]
''',[16],'Section 5.1 — regularized drift and remainder (26)',{'D10':'The regularized errors use the same fitted-law and empirical fold conventions.','D17':'They use the fitted and true regularized influence functions.'},symbols=[r'\mathcal D_n^{j,\beta}',r'\mathcal R_P^\beta'],shape='Regularized drift and population remainder after subtracting the spectral bias. The definition paragraph allows beta in ell2, whereas Theorem 5 restricts beta_n to ell2-star; retain both original scopes.')
add('D21','transformation',r'''
In what follows we fix $\beta\in\ell^2_*$ and define $\Gamma_\beta:\mathcal H\to\mathcal H$ as $\Gamma_\beta(h)=\sum_{k=1}^\infty\beta_k\langle h,h_k\rangle_{\mathcal H}h_k$.

If $\nu$ is pathwise differentiable at $P$, then its transformation $\nu^\beta:=\Gamma_\beta\circ\nu$ is pathwise differentiable at $P$ with local parameter $\dot\nu_P^\beta:=\Gamma_\beta\circ\dot\nu_P$ and EIF $\phi_P^\beta\in L^2(P;\mathcal H)$.
''',[18],'Section 5.2 and Lemma 7 — transformed parameter and derivative',{'D4':'The transformed derivative is Gamma_beta composed with the original pathwise derivative.','D17':'The transformed parameter has the regularized influence function of the original parameter.','D1':'The lemma places that transformed-parameter EIF in the Bochner L2 space.'},kind='source_passage',symbols=[r'\Gamma_\beta(h)=\sum_{k=1}^\infty\beta_k\langle h,h_k\rangle_{\mathcal H}h_k',r'\nu^\beta:=\Gamma_\beta\circ\nu',r'\dot\nu_P^\beta:=\Gamma_\beta\circ\dot\nu_P'],shape='Fixed diagonal transformation, transformed parameter and its derivative. Existence of its EIF does not assert the original parameter has an EIF. The two original passages are the opening definition and the full Lemma 7 body.')
add('D22','one-step estimator',r'''
Since $\nu^\beta$ has an EIF, the methods from Section 4.2 can be used to construct a confidence set for $\nu^\beta(P_0)$ based on a one-step estimator. This one-step estimator takes the form $\widetilde\nu_n^\beta:=\frac12\sum_{j=1}^2[\Gamma_\beta\circ\nu(\widehat P_n^j)+P_n^j\phi_n^{j,\beta}]$.
''',[18],'Section 5.2 — one-step estimator of the transformed parameter',{'D21':'The plug-in is transformed by Gamma_beta and targets nu^beta(P0).','D10':'The estimator uses the original cross-fitting convention.','D17':'The held-out correction is the regularized influence function.'},symbols=[r'\widetilde\nu_n^\beta:=\frac12\sum_{j=1}^2',r'\Gamma_\beta\circ\nu(\widehat P_n^j)'],shape='Estimator with transformed plug-in, distinct from bar-nu_n^beta in the rate theorem. Theorem 6 assumes its asymptotic linearity and does not import the unregularized theorem hypotheses.')
add('D23','spherical confidence set',r'''
\[
\mathcal C_n^\beta(\widehat\zeta_n):=\{h\in\mathcal H:\|\widetilde\nu_n^\beta-h\|_{\mathcal H}^2\le\widehat\zeta_n/n\}.\tag{29}
\]
''',[18],'Section 5.2 — spherical confidence set (29)',{'D22':'The sphere is centered at the estimator of the transformed parameter.'},context=r'a spherical confidence set for $\nu^\beta(P_0)$ would take the form',symbols=[r'\mathcal C_n^\beta(\widehat\zeta_n)',r'\|\widetilde\nu_n^\beta-h\|_{\mathcal H}^2\le\widehat\zeta_n/n'],shape='Sphere for the fixed transformed parameter. Theorem 6 accepts a consistent threshold; the example bootstrap construction in surrounding prose is not made mandatory.')
add('D24','preimage',r'''
To transform the confidence set for $\nu^\beta(P_0)$ into one for $\nu(P_0)$, we take the preimage $\Gamma_\beta^{-1}[\mathcal C_n^\beta(\widehat\zeta_n)]:=\{h\in\mathcal H:\Gamma_\beta(h)\in\mathcal C_n^\beta(\widehat\zeta_n)\}$.

To simplify the discussion, hereafter we focus on the special case where $\mathcal C_n^\beta(\widehat\zeta_n)$ takes the spherical form in (29). In this case, $\Gamma_\beta^{-1}[\mathcal C_n^\beta(\widehat\zeta_n)]$ takes the elliptical form
\[
\left\{h\in\mathcal H:\sum_{k=1}^\infty\beta_k^2\left[\frac12\sum_{j=1}^2\left\{\langle\nu(\widehat P_n^j),h_k\rangle_{\mathcal H}+P_n^j\dot\nu_n^{j,*}(h_k)\right\}-\langle h,h_k\rangle_{\mathcal H}\right]^2\le\widehat\zeta_n/n\right\}.\tag{30}
\]
''',[18],'Section 5.2 — preimage definition and elliptical form (30)',{'D21':'The set is pulled back by the fixed diagonal transformation.','D23':'The displayed ellipse is the preimage of the spherical confidence set (29).','D10':'The expanded coefficients retain the two fitted laws and held-out empirical measures.','D5':'The coefficients evaluate the efficient influence operator at the fixed basis elements.'},symbols=[r'\Gamma_\beta^{-1}[\mathcal C_n^\beta(\widehat\zeta_n)]',r'P_n^j\dot\nu_n^{j,*}(h_k)'],shape='Set preimage, not a globally bounded inverse operator. Theorem 6 fixes all beta entries positive, while the definition itself allows zeros. Keep the original expanded coefficients and squared beta weights.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
