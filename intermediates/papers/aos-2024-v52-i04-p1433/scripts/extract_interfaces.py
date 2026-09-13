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


add('D1','Heavy tailed series priors',r'''
Heavy tailed series priors. Depending on the setting, we construct priors in $L^2:=L^2[0,1]$ via series expansions in either an orthonormal basis $\{\varphi_k:k\ge1\}$ or an orthonormal boundary-corrected wavelet basis $\{\psi_{lk}:l\ge0,\ k\in\mathcal K_l\}$ where $\mathcal K_l=\{0,\ldots,2^l-1\}$ and where we denote the scaling function as the first wavelet $\psi_{00}$. Without loss of generality we have taken the coarsest scale to be 1, while it is straightforward to accommodate for coarsest scales finer than 1. For more details, see [40, Section 4.3].

Prior $\Pi$ on functions. For $\langle\cdot,\cdot\rangle$ the usual inner product on $L^2$, let $f_k:=\langle f,\varphi_k\rangle$, respectively $f_{lk}:=\langle f,\psi_{lk}\rangle$, denote the coefficients of $f\in L^2$ onto the considered bases, so that
\[
f=\sum_{k=1}^\infty f_k\varphi_k,\qquad\text{or}\qquad f=\sum_{l=0}^\infty\sum_{k\in\mathcal K_l}f_{lk}\psi_{lk}.
\]
Let us define a prior $\Pi$ on $f$ by letting, for $(\sigma_k),(s_l)$ sequences to be chosen below, and $(\zeta_k),(\zeta_{lk})$ independent identically distributed random variables of common law $H$ with heavy tails, also to be specified,
\[
f_k\overset{\mathrm{ind.}}\sim\sigma_k\zeta_k,\tag{3}
\]
in the case of a single–index basis $(\varphi_k)$, or for a double–index basis
\[
f_{lk}\overset{\mathrm{ind.}}\sim s_l\zeta_{lk}.\tag{4}
\]
''',[3],'Heavy tailed series priors — constructions (3) and (4)',symbols=[r'\sigma_k\zeta_k',r's_l\zeta_{lk}'],shape='Original two-branch series construction. Basis, coefficient sequence and common innovation law are explicit inputs. Single-index and wavelet branches are distinguished in each theorem use; no fixed scale, moment or density condition is inserted into the generic construction.')
add('D2','scale parameters',r'''
A key choice of scale parameters $\sigma_k$ and $s_l$ throughout the paper is, for any $k\ge1$ and $l\ge0$,
\[
\sigma_k=e^{-(\log k)^2},\qquad s_l=2^{-l^2}.\tag{5}
\]
''',[4],'Scale parameters — equation (5)',symbols=[r'\sigma_k=e^{-(\log k)^2}',r's_l=2^{-l^2}'],shape='Two matching scales in (5), selected according to the coefficient basis. This is the square-log/square-level choice, not every rapidly decaying scale.')
add('D3','scale parameters',r'''
Another possible choice we consider, again for any such $k,l$ and some $\alpha>0$ is
\[
\sigma_k=k^{-1/2-\alpha},\qquad s_l=2^{-l(1/2+\alpha)}.\tag{6}
\]
''',[4],'Scale parameters — equation (6)',context=members['D2']['statement_original'],symbols=[r'\sigma_k=k^{-1/2-\alpha}',r's_l=2^{-l(1/2+\alpha)}'],shape='Polynomial-index and matching wavelet scales with alpha positive. Stronger alpha restrictions in particular theorem branches remain in those statements.')
add('D4','scale parameters',r'''
suppose $(\sigma_k)$ is defined, for some $a,\delta>0$, by
\[
\sigma_k=e^{-a(\log k)^{1+\delta}},\tag{21}
\]
''',[12],'Theorem 6 — scale in the second branch, equation (21)',kind='theorem_excerpt',context=members['D2']['statement_original'],context_pages=[4],symbols=[r'\sigma_k=e^{-a(\log k)^{1+\delta}}'],shape='General single-index scale in Theorem 6, also used through its reference in Theorem 9. Parameters a and delta are positive; the rate (22) retains delta. This passage ends before the following density and tail assumptions.')
add('D5','density',r'''
To complete the prior’s description, let us now specify the distribution $H$ of the $\zeta$ variables as above. Suppose that $H$ admits a density $h$ on $\mathbb R$ and that for $c_1>0$ and $\kappa\ge0$,
\[
h\text{ is symmetric, positive, bounded and decreasing on }[0,\infty),\tag{7}
\]
\[
\log(1/h(x))\le c_1(1+\log^{1+\kappa}(1+x)),\qquad x\ge0.\tag{8}
\]
''',[4],'Density conditions (7)–(8)',kind='condition',symbols=[r'\log(1/h(x))',r'\log^{1+\kappa}(1+x)'],phrases=['symmetric, positive, bounded and decreasing'],shape='The two jointly referenced conditions on the innovation density. The density lower bound through negative log is not a moment or an upper-tail bound; retain c1 positive and kappa nonnegative.')
add('D6','moment assumption',r'''
In this section, we consider series priors as in (3)-(5), defined via a heavy-tailed density $h$ satisfying the moment assumption, for some $q\ge1$,
\[
\int_{-\infty}^\infty |x|^q h(x)dx<\infty.\tag{14}
\]
''',[7],'Moment assumption (14)',kind='condition',symbols=[r'|x|^q h(x)'],shape='Finite absolute q-th innovation moment, q at least one. Theorems 1, 2 and 4 use q=2; Theorem 3 uses q at least one. Theorem 5 does not assume (14).')
add('D7','tail condition',r'''
As a slight variant to the moment assumption (14), here we require the tail condition: for some $c_2>0$,
\[
\bar H(x):=\int_x^\infty h(u)du\le c_2/x^2,\qquad x\ge1.\tag{19}
\]
''',[12],'Tail condition (19)',kind='condition',symbols=[r'\bar H(x)',r'\int_x^\infty h(u)du\le c_2/x^2'],shape='One-sided survival tail upper bound. The bar on H is printed in the PDF. Mention of (14) is a comparison, not a requirement or a dependency: (19) does not imply a finite second moment.')
add('D8','Sobolev-type',r'''
When working with an orthonormal basis $\{\varphi_k\}$, we consider Sobolev-type assumptions. Recalling that $f_k=\langle f,\varphi_k\rangle$, for $\beta,L>0$, denote
\[
\mathcal S^\beta(L)=\left\{f=(f_k),\ \sum_{k\ge1}k^{2\beta}f_k^2\le L^2\right\}.\tag{9}
\]
''',[4],'Sobolev-type regularity ball — equation (9)',symbols=[r'\mathcal S^\beta(L)',r'\sum_{k\ge1}k^{2\beta}f_k^2'],shape='Coefficient ellipsoid in the selected single-index orthonormal basis, with non-strict bound. Identification with classical derivative smoothness depends on the basis; that identification is not silently assumed.')
add('D9','Hölder–type',r'''
[Hölder–type] For $f_{lk}=\langle f,\psi_{lk}\rangle$ and $\beta,L>0$, let
\[
\mathcal H^\beta(L)=\left\{f=(f_{lk}),\ \max_{k\in\mathcal K_l}|f_{lk}|\le2^{-l(1/2+\beta)}L\text{ for all }l\ge0\right\}.\tag{10}
\]
''',[5],'Hölder-type regularity ball — equation (10)',symbols=[r'\mathcal H^\beta(L)',r'\max_{k\in\mathcal K_l}|f_{lk}|'],shape='Wavelet coefficient hyperrectangle with a bound at every level, including level zero. Classical Hölder interpretation requires sufficient basis regularity and distinguishes integer smoothness.')
add('D10','Besov–type',r'''
[Besov–type] For $\beta,L>0$ and $1\le r\le2$, let
\[
\mathcal B^\beta_{rr}(L)=\left\{f=(f_{lk}),\ \sum_{l\ge0}2^{rl(\beta+1/2-1/r)}\sum_{k\in\mathcal K_l}|f_{lk}|^r<L^r\right\}.\tag{11}
\]
''',[5],'Besov-type regularity ball — equation (11)',symbols=[r'\mathcal B^\beta_{rr}(L)',r'2^{rl(\beta+1/2-1/r)}'],shape='Strict coefficient ball, with the two Besov summability indices equal to r in [1,2]. Theorems 4 and 10 additionally assume beta greater than 1/r-1/2.')
add('D11','posterior distribution',r'''
Consider a statistical model $\{P_f^{(n)},\ f\in\mathcal F\}$ indexed by a function $f$ with observations $X=X^{(n)}$. Examples considered below include nonparametric regression, density estimation and classification. Given a prior distribution $\Pi$ on $f$, the Bayesian model sets $X\mid f\sim P_f^{(n)}$ and $f\sim\Pi$. The posterior distribution $\Pi[\cdot\mid X]$ is the conditional distribution $f\mid X$. Assuming the model is dominated, the posterior is given as usual by Bayes’ formula. Taking a frequentist approach, we analyse the posterior $\Pi[\cdot\mid X]$ under the assumption that $X$ has actually been generated from $P_{f_0}^{(n)}$ for some fixed true function $f_0$. We refer to the book [38] for more context and references.
''',[4],'Frequentist analysis — posterior distribution',symbols=[r'\Pi[\cdot\mid X]',r'P_{f_0}^{(n)}'],shape='Usual conditional posterior, analyzed under a fixed true sampling law. Prior and model are formal inputs; individual prior scales and models are connected from the theorem, not universally attached here.')
add('D12','Gaussian white noise model',r"""
For $f\in L^2$ and $n\ge1$, the Gaussian white noise model writes
\[
dY^{(n)}(t)=f(t)dt+dW(t)/\sqrt n,\qquad t\in[0,1],\tag{12}
\]
where $W$ is standard Brownian motion.
""",[6],'Nonparametric regression — Gaussian white noise model (12)',kind='source_passage',symbols=[r'dY^{(n)}(t)',r'dW(t)/\sqrt n'],shape='White noise experiment with f in L2[0,1], noise precision n at least one and W standard Brownian motion.')
add('D13','normal sequence model',r'''
By projecting (12) onto a single-index orthonormal basis $\{\varphi_k\}$ of $L^2$, one obtains the normal sequence model, with $f_k=\langle f,\varphi_k\rangle$,
\[
X_k\mid f_k\sim \mathcal N(f_k,1/n),\tag{13}
\]
independently for $k\ge1$, with $X_k=\int_0^1\varphi_k(t)dY^{(n)}(t)$. We denote $X=X^{(n)}=(X_1,X_2,\ldots)$ the corresponding observation sequence.
''',[7],'Normal sequence model — equation (13)',{'D12':'Equation (13) explicitly defines X_k by projecting the white noise observation in (12).'},kind='source_passage',symbols=[r'X_k\mid f_k\sim \mathcal N(f_k,1/n)'],shape='Single-index independent Gaussian observations with variance 1/n. The basis and coefficient map are ambient inputs, not a demand for a prior.')
add('D14','Linear inverse problems',r'''
A synthetic prototypical model in linear inverse problems arises when projecting onto the SVD of the forward operator: the observation model is, for some $\nu\ge0$, independently for $k\ge1$,
\[
X_k\mid f_k\sim \mathcal N(\kappa_kf_k,1/n),\qquad\kappa_k\asymp k^{-\nu}.\tag{15}
\]
''',[8],'Linear inverse problems — observation model (15)',context='Linear inverse problems, Sobolev smoothness.',kind='source_passage',symbols=[r'\kappa_k\asymp k^{-\nu}'],shape='Independent Gaussian inverse sequence experiment with polynomial singular-value order. The degree nu includes zero. No particular Volterra operator from the later simulation is assumed.')
add('D15','normal sequence model',r'''
In this case, we expand in a wavelet orthonormal basis, and the projection of model (12) becomes a normal sequence model
\[
X_{lk}\mid f_{lk}\sim \mathcal N(f_{lk},1/n),\tag{16}
\]
independently over relevant indices $l,k$. Again, we denote by $X^{(n)}$ the observation sequence.
''',[9],'Normal sequence model — wavelet equation (16)',{'D12':'The source explicitly obtains (16) by projecting model (12) into the wavelet basis.'},kind='source_passage',symbols=[r'X_{lk}\mid f_{lk}\sim \mathcal N(f_{lk},1/n)'],shape='Double-index Gaussian experiment. Its indexing follows the boundary-corrected wavelet basis on page 3.')
add('D16','multi-scale sequence spaces',r'''
For monotone increasing weighting sequences $w=(w_l)_{l\ge0}$, $w_l\ge1$, we define multi-scale sequence spaces
\[
\mathcal M\equiv\mathcal M(w)\equiv\left\{x=\{x_{lk}\}:\|x\|_{\mathcal M(w)}\equiv\sup_l\frac{\max_k|x_{lk}|}{w_l}<\infty\right\}.\tag{17}
\]
''',[11],'Multi-scale sequence spaces — equation (17)',symbols=[r'\mathcal M(w)',r'\frac{\max_k|x_{lk}|}{w_l}'],shape='Weighted supremum sequence norm with the original w_l>=1 convention at every l>=0. Theorem 5 prints power weights vanishing at level zero; keep this source discrepancy visible instead of silently shifting l.')
add('D17','separable closed subspace',r'''
However, the following space $\mathcal M_0$ forms a separable closed subspace for the same norm
\[
\mathcal M_0=\mathcal M_0(w)=\left\{x\in\mathcal M(w):\lim_{l\to\infty}\max_k\frac{|x_{lk}|}{w_l}=0\right\}.\tag{18}
\]
''',[11],'Separable closed subspace — equation (18)',{'D16':'The subspace consists of elements of M(w) and uses its weighted supremum norm.'},symbols=[r'\mathcal M_0(w)',r'\lim_{l\to\infty}\max_k\frac{|x_{lk}|}{w_l}'],shape='Weighted vanishing-level subspace, with the same norm as (17). Do not replace it with the whole nonseparable bounded sequence space.')
add('D18','white noise',r'''
The white noise model (12) can be rewritten as the sequence model $X^{(n)}=f+\mathbb W/\sqrt n$, where in slight abuse of notation $f$ is identified with the sequence of its coefficients $f=(f_{lk})$ and $\mathbb W=(\int\psi_{lk}dW(t))_{l,k}$ has the distribution of an iid sequence of $\mathcal N(0,1)$ variables.
''',[11],'White noise — coefficient sequence and its law',{'D12':'The sequence W is the wavelet projection of the Brownian noise in model (12).'},symbols=[r'\mathbb W',r'\mathcal L(\mathbb W)'],shape='Standard independent Gaussian coefficient sequence. Theorem 5 uses its law L(W); membership in M0 requires weight growth, as recorded in adjacent source context.')
add('D19','induced posterior distribution',r'''
Denote $\tau:f\mapsto\sqrt n(f-X^{(n)})$. Then $\Pi[\cdot\mid X^{(n)}]\circ\tau^{-1}$ denotes the induced posterior distribution on $\mathcal M_0$, shifted and rescaled by $\tau$.
''',[11],'Induced posterior distribution — centering and rescaling',{'D11':'The distribution being pushed forward is the ordinary conditional posterior.','D15':'The center X^(n) is the wavelet observation sequence in this section.','D17':'The pushed-forward posterior is regarded as a probability law on M0.'},symbols=[r'\tau:f\mapsto\sqrt n(f-X^{(n)})',r'\Pi[\cdot\mid X^{(n)}]\circ\tau^{-1}'],shape='Data-dependent affine pushforward. Tau inverse in the pushforward notation means preimage, not a separately estimated inverse function.')
add('D20','bounded-Lipschitz metric',r'''
For $S$ a given metric space, let $\beta_S(P,Q)$ denote the bounded-Lipschitz metric over probability distributions $P,Q$ on $S$. It is well-known that $\beta_S$ metrises weak convergence on $S$.
''',[11],'Bounded-Lipschitz metric',symbols=[r'\beta_S(P,Q)',r'\beta_{\mathcal M_0}'],shape='Named bounded-Lipschitz probability metric. The paper does not specify its test-function normalization; do not fabricate a defining formula. Its application here is on the separable metric subspace M0.')
add('D21','tempered posteriors',r'''
While we were able in Section 2 to derive all the results for classical posteriors, here we use instead tempered posteriors: these are defined as, for $0<\rho\le1$, by
\[
\Pi_\rho[B\mid X]=\frac{\int_B\left(p_f^{(n)}(X)\right)^\rho d\Pi(f)}{\int\left(p_f^{(n)}(X)\right)^\rho d\Pi(f)},
\]
for measurable $B$. The usual posterior corresponds to $\rho=1$ while $\rho<1$ ‘tempers’ the influence of the likelihood.
''',[13],'Tempered posteriors — likelihood power',symbols=[r'\Pi_\rho',r'\left(p_f^{(n)}(X)\right)^\rho'],shape='Normalized likelihood-power posterior, defined for 0<rho<=1. Theorems 8-10 assume rho<1 within that ambient range; do not interpret them as permitting nonpositive rho. Reference to the usual posterior is comparative, not a requirement for its computation first.')
add('D22','prior on densities',r'''
From a prior defined by (4) and (5), a prior on densities on $[0,1]$ is easily defined by exponentiation and renormalisation: for $f$ bounded and measurable, let
\[
g(x)=g_f(x)=\frac{e^{f(x)}}{\int_0^1e^{f(u)}du}.\tag{25}
\]
''',[13],'Prior on densities — equation (25)',symbols=[r'g_f(x)',r'\frac{e^{f(x)}}{\int_0^1e^{f(u)}du}'],shape='Normalized exponential map and its prior pushforward. The displayed map applies to any bounded measurable f; Theorem 8 explicitly selects both prior branches of Theorem 7, extending the opening prose example (4),(5). Prior choices are supplied by theorem edges, not fixed on this map.')
add('D23','binary regression function',r'''
Consider independent observations $(X_1,Y_1),\ldots,(X_n,Y_n)$ from a given distribution of a random variable $(X,Y)$, where $Y\in\{0,1\}$ is binary and $X$ takes values in $\mathcal X=[0,1]^d$ for $d\ge1$. The interest is in estimating the binary regression function $h_0(x)=P(Y=1\mid X=x)$.
''',[14],'Classification — observations and binary regression function',kind='source_passage',symbols=[r'h_0(x)=P(Y=1\mid X=x)',r'\mathcal X=[0,1]^d'],shape='Independent binary observations with a covariate cube of dimension d>=1. The preceding series definitions are one-dimensional; no higher-dimensional basis or rate convention is supplied here.')
add('D24','logistic link function',r'''
Consider the logistic link function $\Lambda(u)=1/(1+e^{-u})$ and denote its inverse by $\Lambda^{-1}$.
''',[14],'Classification — logistic link function',symbols=[r'\Lambda(u)=1/(1+e^{-u})',r'\Lambda^{-1}'],shape='Logistic map and inverse logit. Theorem 9 defines f0 via Lambda inverse applied to h0; do not identify f0 with the binary probability h0.')
add('D25','binary regression functions',r'''
setting
\[
h_f(x)=\Lambda(f(x))\tag{26}
\]
induces a prior distribution $\Pi$ on binary regression functions.
''',[14],'Classification — prior map (26)',{'D24':'The defining formula applies the logistic link Lambda.'},symbols=[r'h_f(x)=\Lambda(f(x))'],shape='Logistic pushforward of an input function prior. The immediately preceding wavelet-prior sentence is retained as auxiliary context; Theorem 9 explicitly selects its prior parameters via Theorem 6. That discrepancy is not repaired or used to insert an extra fixed scale.')
add('D26','density of the data',r'''
The density of the data $(X,Y)$ given $f$ equals $p_f(x,y)=h_f(x)^y(1-h_f(x))^{1-y}g(x)$, where $g(x)$ denotes the marginal density of $X$.
''',[14],'Classification — joint density of the data',{'D23':'The response y is binary and x is the covariate from the classification model.','D25':'The Bernoulli success probability h_f is the logistic image of f.'},symbols=[r'p_f(x,y)',r'h_f(x)^y(1-h_f(x))^{1-y}g(x)'],shape='Joint density on the covariate-response product. Theorem 9 prints p_f-p_f0 in a norm described on the covariate domain only; the unresolved domain mismatch is preserved.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
