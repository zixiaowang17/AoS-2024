"""Preserve source conventions and algorithmic ambiguities, excluding appendices."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
aux=[]
def add(lid,text,pages,location):aux.append(dict(local_id=lid,statement_original=text.strip(),evidence=[dict(page=p,location=location) for p in pages]))
add('A1',r'''
For any $t\in\mathbb Z$ and any integer pair $s_2\le s_1$, let $\mathcal X_t^*$ be an independent copy of $\mathcal X_t$ and $X_{t,\{s_1,s_2\}}=G(\mathcal F_{t,\{s_1,s_2\}}^X)$ be a coupled random variable, where
\[
\mathcal F_{t,\{s_1,s_2\}}^X=\begin{cases}\{\ldots,\mathcal X_{s_2-1},\mathcal X_{s_2}^*,\ldots,\mathcal X_{s_1}^*,\mathcal X_{s_1+1},\ldots,\mathcal X_t\},&s_1<t,\\\{\ldots,\mathcal X_{s_2-1},\mathcal X_{s_2}^*,\ldots,\mathcal X_t^*\},&s_2\le t\le s_1,\\\{\ldots,\mathcal X_t\},&t<s_2.\end{cases}\tag{5}
\]
For any $s,t\in\mathbb Z$, let $\mathcal F_{t,\{s\}}^X=\mathcal F_{t,\{s,s\}}^X$, satisfying that when $t<s$, $\mathcal F_{t,\{s\}}^X=\mathcal F_t^X$ and $X_{t,\{s\}}=X_t$.
''',[5],'Section 1.2 — innovation replacement recipe (5)')
add('A2',r'''For any vector $v\in\mathbb R^p$ and any $q\in(0,\infty]$, let $|v|_q$ be its $\ell_q$-norm. For any random variable $Z\in\mathbb R$ and any $q>0$, let $\|Z\|_q=\{\mathbb E[|Z|^q]\}^{1/q}$, if $\mathbb E[|Z|^q]<\infty$. For any matrix $A$, let $|A|_\infty$ denote its entry-wise max norm. For any set $S$, let $|S|$ denote its cardinality.''',[4],'Notation — vector versus random-variable norms')
add('A3',r'''For two deterministic or random $\mathbb R$-valued sequences $a_n,b_n>0$, write $a_n\gg b_n$ if $a_n/b_n\to\infty$ as $n$ diverges. Write $a_n\lesssim b_n$ if $a_n/b_n\le C$, for some absolute constant $C>0$ and for all $n$ sufficiently large. For a deterministic or random $\mathbb R$-valued sequence $a_n$, write that a sequence of random variable $X_n=O_p(a_n)$ if $\lim_{M\to\infty}\limsup_n\mathbb P(|X_n|\ge Ma_n)=0$. Write $X_n=o_p(a_n)$ if $\limsup_n\mathbb P(|X_n|\ge Ma_n)=0$ for all $M>0$. The convergences in distribution and probability are respectively denoted by $\xrightarrow{\mathcal D}$ and $\xrightarrow{P.}$.''',[4],'Notation — asymptotic conventions')
add('A4',r'''To be specific, let $\gamma_1(X)$ and $\gamma_1(\epsilon)$ be the functional dependence measure decay rate indicator for the covariate and noise sequences, respectively. In Assumptions 2 and 3, we in fact let $\gamma_1=\min\{\gamma_1(X),\gamma_1(\epsilon)\}$ and $\gamma_2=\min\{\gamma_2(X),\gamma_2(\epsilon)\}$.''',[11],'Section 3.1 — common worst-case exponents')
add('A5',r'''The coefficient 2 in the term $\gamma_2^{-1}$ accounts for the tail behaviour of the cross-term sequence $\{\epsilon_tX_t\}_{t=1}^n$. In Assumptions 2b and 3b, we allow $\gamma_1\in(0,\infty)$ provided that $\gamma<1$.''',[11],'Section 3.1 — combined exponent restriction')
add('A6',r'''
Denote the preliminary estimators obtained from the optimisation problem specified in (12), (13) and (14), or equivalently from Algorithm 1 as
\[
\{\widehat\eta_k\}_{k=1}^{\widehat K}=\widehat{\mathcal B}.\tag{16}
\]
Denote the corresponding regression coefficient estimators (14) as $\{\widehat\beta_k\}_{k=0}^{\widehat K}$.
''',[9],'Section 2.2 — preliminary segment and coefficient notation')
add('A7',r'''we simplify the setting by choosing $\zeta_1=\zeta_2=\zeta$ to reduce the number of tuning parameters. Our theoretical results are derived under this restriction.''',[7],'Remark 1 — common partition penalty and interval cutoff')
add('A8',r'''
Suppose that Assumptions 1, 2 and 3 hold. For $k\in\{1,\ldots,K\}$, under the vanishing regime, the long-run variance
\[
\sigma_\infty^2(k)=4\lim_{n\to\infty}\operatorname{Var}\left(n^{-1/2}\sum_{t=1}^n\epsilon_tv_k^\top X_t\right)\tag{25}
\]
exists and satisfies that $\sigma_\infty^2(k)<\infty$.
''',[12],'Lemma 2 — complete existence assertion for the variance')
add('A9',r'''
where $\varpi_k$ is the limiting drift coefficient defined in Assumption 2c, and $\mathbb W(r)$ is a two-sided standard Brownian motion defined as
\[
\mathbb W(r)=\begin{cases}\mathbb B_1(-r),&r<0,\\0,&r=0,\\\mathbb B_2(r),&r>0,\end{cases}
\]
with $\mathbb B_1(r)$ and $\mathbb B_2(r)$ being two independent standard Brownian motions.
''',[13],'Theorem 3b.2 — Brownian convention reused in Theorem 10')
add('A10',r'''To practically perform inference on change point locations based on change point estimators $\{\widetilde\eta_k\}_{k=1}^{\widehat K}$ in the vanishing jump size regime, it is crucial to have access to consistent estimators of the long-run variances $\{\sigma_\infty^2(k)\}_{k=1}^K$ and the drift coefficients $\{\varpi_k\}_{k=1}^K$, involved in the limiting distribution in Theorem 3b.2. In this section, we first propose a block-type long-run variance estimator and derive its consistency. With the help of this long-run variance estimator, we are able to provide a complete inference procedure of the vanishing regime in Section 4.1.''',[18],'Section 4 — vanishing-regime scope of Theorems 8 and 10')
add('A11',r'''
The sequence $\{Z_t\}_{t=1}^n$ is a sample version of the unobservable sequence $\{Z_t^*\}_{t=1}^n$, defined as
\[
Z_t^*=\begin{cases}2\epsilon_t\Psi_k^\top X_t-(\Psi_k^\top X_t)^2,&t=s_k,\ldots,\eta_k-1,\\2\epsilon_t\Psi_k^\top X_t+(\Psi_k^\top X_t)^2,&t=\eta_k,\ldots,e_k-1.\end{cases}
\]
''',[18],'Section 4 — oracle residual-product sequence')
add('A12',r'''aside from the long-run variance, the drift coefficients $\varpi_k=v_k^\top\Sigma v_k$, $k\in\{1,\ldots,K\}$, are also unknown.''',[19],'Section 4.1 — printed finite-sample drift wording')
add('A13',r'''$R\in\mathbb N$ satisfying $(e_k-s_k)\gg R\gg\sqrt{e_k-s_k}$, as $n$ diverges.''',[18],'Theorem 8 — block-count condition inherited by Theorem 10')
resolution={
 'shared':'Vector norms use single bars with a subscript; Lq norms of random variables use double bars (A2). Ordinary X is the observed covariate and script X its innovation. Observed epsilon differs from innovation varepsilon. F denotes the causal innovation history, not a filtration generated by observed responses. The generic independent-innovation replacement recipe is (5), archived in A1; it is reused for noise and nonstationary scalar processes without importing stationary covariate assumptions. All process and covariance parameters may form a triangular sequence as p and jump directions vary with n. K is fixed by Assumption 1. Probability, conditional expectation, covariance, matrix eigenvalues, Gaussian variables and Brownian motion are ambient. Convergence and stochastic-order conventions are A3. Argmin is written as a point-valued object by the source without a general tie-selection rule.',
 '3':'Assumptions 1–3 resolve to D2–D4,D34,D12–D18, with underlying regression, stationary process and functional-dependence definitions D1,D5,D7–D9. Assumption 4b is D21, including D20 and the exponent D19; A4–A5 give the worst-case exponent convention. D25 is the full DPDU algorithm, D22 the interval Lasso, D26 the local interval and D27 the final estimator. A6 supplies beta-hat_0 and preliminary segment notation. D28 and A8 give the long-run variance; D15 supplies the drift. Part a binds the limiting jump magnitude, the signed two-sided random walk and the extra convergence of the entire paired process inline. Part b binds the vanishing regime and two independent Brownian halves. Theorem 4 and proof-only restricted-eigenvalue results are not added as statement prerequisites.',
 '4':'D10 resolves the potentially nonstationary scalar causal process (10), and D11 resolves the cumulative functional dependence measure (11), instantiated at q=2. A1 supplies the generic block/single-innovation replacement operation. Mean zero, uniform tails, constants gamma_1(Z),gamma_2(Z),c,C_FDM, the scalar combined exponent, x>=1 and m>=3 are all bound inline. This scalar gamma(Z) has coefficient one on the tail exponent, whereas D19 has coefficient two for regression cross-products. No regression, sparsity, Lasso or change-point model is a prerequisite.',
 '8':'The phrase all assumptions and notation in Theorem 3 imports the model, sparsity, dependence, tails, covariance, strong signal-to-noise condition and DPDU/Lasso tuning. The Section 4 preamble A10 restricts the setting to the vanishing regime D33, so the non-vanishing paired-process limit is not added. The theorem separately specifies D25,D22,D26,D29 and Algorithm 2 D30. Its target is D28; the R growth condition is bound in the statement and retained in A13. The final refined locations D27 are not an input to the variance algorithm and do not become a prerequisite just because Theorem 3 analyzes them.',
 '10':'Theorem 8 supplies its assumptions, algorithmic construction and block-count growth A13, in the Section 4.1 vanishing-regime setting. D32 is the simulated minimizer (32), with variance estimate D30 and drift estimate D31; their preliminary fits and intervals are recursively resolved. D29 is the jump estimate and D34 its population analogue. The limiting drift and variance are D15,D28, with the Brownian convention A9. M=infinity, the squared jump ratio and its indicator are preserved literally. No finite-M confidence interval coverage theorem or extra Gaussian-data independence condition is invented.'
}
issues=[
 'Pinned arXiv:2207.12453v3 has margin date 1 October 2023 and title-page date 3 October 2023. Its source title says Change point while journal metadata says Change-point; authors and remaining title agree. Final journal equivalence is not asserted.',
 'Only main text and references through page 33 are used. The appendix heading is on page 34; all subsequent mathematics is excluded.',
 'Assumption 1 allows covariate-noise dependence through its conditional mean-zero requirement. No independence between their innovation streams is imposed in the extracted model.',
 'The covariate and noise causal representations separately imply strict stationarity. A jointly stationary coupling of their innovation streams is not separately specified in the main-text definitions.',
 'The high-dimensional process, jump directions and covariance may vary with n. Theorem 3 states convergence of the paired process on all integer times without specifying a path-space topology or a construction of the limiting sequence.',
 'The source normalizes the jump immediately before its location, beta-star_{eta_k-1}, not beta-star at the preceding indexed change point. Glyph coordinates confirm the minus one belongs outside the k subscript.',
 'The number K is a fixed positive integer, while minimum spacing may shrink as a fraction of n. No growing-K claim is inferred.',
 'Covariate functional dependence takes a supremum over every unit direction and fourth moments. It is not replaced by coordinatewise dependence or second moments.',
 'The scalar nonstationary dependence measure takes a supremum over time. Its q=2 instantiation in Theorem 4 is distinct from the q=4 assumptions for X and epsilon.',
 'Shared gamma_1 and gamma_2 in the regression assumptions are minima of covariate and noise exponents. Their combined gamma uses a factor two absent from Theorem 4 gamma(Z).',
 'Assumption 4b includes inequality (24) and additionally requires alpha_n >> s log(pn)^{2/gamma}. It is not an alternative to the baseline condition.',
 'The Lasso penalty is lambda times the square root of interval length times the L1 norm. Algorithm 1 divides the whole objective by interval length consistently with this scaling.',
 'The source uses one zeta for both the partition penalty and the minimum interval length. Remark 1 distinguishes their roles but says the theory uses equal values.',
 'The source interval loss omits the response-square sum and sets the loss to zero on short intervals. These printed choices are retained without asserting equivalence to another objective in every boundary case.',
 'Algorithm 1 initializes a pointer vector of length n but loops through r=n+1 and may assign p_{n+1}. Its backtracking then starts at k=n. These indexing choices are not repaired.',
 'Algorithm 1 initializes the temporary V as an element of R^p but updates it with y_l X_l transpose and multiplies it as a row vector. The printed orientation mismatch remains documented.',
 'Algorithm 1 adds each predecessor h to its output set, potentially including the boundary 1. The surrounding model treats 1 as eta_0 rather than a change point; the algorithm does not explicitly remove that boundary.',
 'Algorithm 1 lists all segment Lasso fits as output but does not explicitly detail how those fits are retained during backtracking. No missing storage step is invented.',
 'Theorems 3 and 8 list coefficient estimates from k=1, whereas refinement (17) and jump estimator (30) require beta-hat_0. Section 2.2 explicitly supplies indices k=0 through K-hat, and that passage is archived.',
 'Algorithm 2 instead uses beta-hat_k and beta-hat_{k+1}, though the surrounding jump/refinement formulas use beta-hat_{k-1} and beta-hat_k. Its input list ends at K-hat, so the final k+1 input is not supplied by the printed list.',
 'The local endpoints in (18) can be nonintegers, while (17) and Algorithm 2 use them as summation/index bounds. No rounding rule is printed there. The exterior estimated endpoints eta-hat_0 and eta-hat_{K-hat+1} are also not explicitly defined in (18).',
 'The source writes argmin as a single selected estimator. Ties in Lasso fits, partitions, local splits and discrete random-walk minima are not covered by a general selection or uniqueness convention in the main text.',
 'Lemma 2 states existence and finiteness of sigma_infty squared, but does not explicitly state strict positivity. Theorem 3 divides by sigma_infty; positive marginal noise variance alone is not substituted for an explicit positive directional long-run variance assumption.',
 'Sections 4 and 4.1 explicitly discuss vanishing jumps. Theorems 8 and 10 refer back to Theorem 3, which has both regimes; the surrounding section restriction is retained separately rather than rewriting the theorem body.',
 'Theorem 8 requires the number R of block pairs to grow faster than the square root of interval length and slower than that length. R is not the block width S.',
 'Algorithm 2 defines S=floor((e_k-s_k)/(2R)), while the following prose states 2R=floor((e_k-s_k)/S). These floor identities are not generally equivalent; the algorithm formula remains authoritative for its stored construction.',
 'Algorithm 2 divides by the estimated jump squared without specifying an output when that estimate is zero. Theorem 10 has a nonzero-jump indicator but still prints a ratio with that denominator.',
 'Assumption 2c defines varpi_k as the limit of v_k transpose Sigma v_k. Section 4.1 later writes an equality with the finite-sample quadratic form; both original passages are archived.',
 'Theorem 10 calls the squared jump estimate the kth jump size estimator, whereas equation (30) defines the unsquared norm. No square is removed from the original theorem.',
 'Step 1 of the simulation construction assumes finite M>0 and a finite Gaussian index range, while Theorem 10 sets M=infinity. A countable extension is implicit but not explicitly constructed there.',
 'The simulated process in (32) is a two-sided Gaussian partial-sum step function with ceiling on the negative side and floor on the positive side. It is not replaced by an interpolated Brownian path.',
 'Step 1 says the Gaussian variables are independent, but does not separately state their independence from the observed data or give a complete joint construction across simulation repetitions.',
 'Theorem 4 is used repeatedly in proofs of other results but is not a prerequisite of their statement definitions. No appendix-only restricted-eigenvalue theorem, proof lemma or algorithm-complexity result is included in the inventory.'
]
data=dict(paper_id=PID,auxiliary_passages=aux,standard_ambient_resolution=resolution,unresolved_source_conventions=issues,unresolved_statement_references=[])
(ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print(f'Saved {len(aux)} auxiliary passages, four theorem resolutions and {len(issues)} source notes.')
