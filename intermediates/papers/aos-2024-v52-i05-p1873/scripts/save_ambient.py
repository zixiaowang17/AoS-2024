# -*- coding: utf-8 -*-
"""Preserve auxiliary source statements, inheritance and unresolved source issues."""
import json
from save_inventory import PID, ROOT, STATEMENTS
A=[];ISSUES=[]
def passage(n,s,pages,note):A.append(dict(local_id=f'A{n}',statement_original=s,evidence=[dict(page=p,location=f'Auxiliary source passage A{n}') for p in pages],scope_note=note))
def issue(key,text,pages):ISSUES.append(dict(issue_id=key,description=text,evidence=[dict(page=p,location='Source scope or notation',**({'before_main_text_end':True} if p==34 else {})) for p in pages]))
passage(1,r'''Assume that $y=(y_1',y_2',\ldots,y_k')'$ is a $p$-dimensional random (column) vector, in which the sub-vector $y_t$ possesses dimension $p_t$ for $t\in[[k]]$, such that $\sum_{t=1}^kp_t=p$, where $[[k]]:=\{1,2,\ldots,k\}$. Denote by $\mu_t=\mathbb E(y_t)$ the mean vector, by $\Sigma_{ij}=\operatorname{Cov}(y_i,y_j)$ the cross covariance matrix, by $\mu=\mathbb E(y)$ and $\Sigma=\operatorname{Cov}(y,y)$ the mean and the covariance of the full vector. A fundamental hypothesis testing problem is
\[
H_0:y_t\text{'s are independent},\qquad\text{v.s.}\qquad H_1:\text{not }H_0.
\]
(1)''',[1],'Block observation model and H0 used in Assumptions 1.6/1.19. The mean vector mu_t is not the spectral probability measure with the same symbol in Section 1.2.')
passage(2,r'''Hence, collecting all the observations, we can construct the data matrices,
\[
Y:=(y(1),\ldots,y(N)),\qquad Y_t:=(y_t(1),\ldots,y_t(N)),\qquad t\in[[k]].
\]''',[2],'Raw matrices used by Definitions 1.1 and 1.2 and the H-hat binder; the normalized X matrices differ by the structural model and square-root-N scaling.')
passage(3,r'''In random matrix theory and high-dimensional multivariate statistics, a commonly adopted structural assumption is
\[
y_t(i)=T_tx_t(i)+\mu_t,\qquad T_tT_t'=\Sigma_{tt}\succ0,\qquad t\in[[k]]\quad\text{and}\quad i\in[[N]],
\]
where $x_i$ consists of independent mean $0$ variance $1$ components and $T_t\in\mathbb R^{p_t\times p_t}$ is an invertible matrix. For simplicity, we present the notations and results for the case that $\mu=0$ and consider the matrix $B$ at first.''',[3],'Standing structural model resolves the raw and normalized representations in (4). The printed x_i wording differs from x_t(i); retain it without rewriting. Sample distribution details are governed by the separately stated entry assumptions.')
passage(4,r'''with $y_t:=p_t/N$.''',[4],'Dimensional ratio reused by Assumption 1.7, Marchenko-Pastur formulas, Corollaries and contour regimes; this algebraic ratio does not itself require the projection ESD interface.')
passage(5,r'''In the sequel, for convenience, we also write $p_{\max}:=\max_tp_t$, $y_{\max}:=\max_ty_t$.''',[5],'Definitions of maxima used in the strengthened dimensional condition in Theorem 1.17.')
passage(6,r'''Throughout this paper, we regard $N$ as our fundamental large parameter. Any quantities that are not explicit constant or fixed may depend on $N$; we almost always omit the argument $N$ from our notation. We use $\|u\|_\alpha$ to denote the $\ell_\alpha$-norm of a vector $u$. We further use $\|A\|_{(\alpha,\beta)}$ to denote the induced norm $\sup_{x\in\mathbb C^n,\|x\|_\alpha=1}\|Ax\|_\beta$ for an $A\in\mathbb C^{m\times n}$. We write $\|A\|\equiv\|A\|_{(2,2)}$ for the usual operator norm of a matrix $A$. We use $C$ to denote some generic (large) positive constant. The notation $a\sim b$ means $C^{-1}b\leq|a|\leq Cb$ for some positive constant $C$. Similarly, we use $a\lesssim b$ to denote the relation $|a|\leq Cb$ for some positive constant $C$. When we write $a\ll b$ and $a\gg b$ for possibly $N$-dependent quantities $a\equiv a(N)$ and $b\equiv b(N)$, we mean $|a|/b\to0$ and $|a|/b\to\infty$ when $N\to\infty$, respectively.''',[11],'Source asymptotic conventions: k~1 means comparability, not equality or necessarily a constant sequence. Distinguished constants and N-dependence are preserved.')
passage(7,r'''Observe that
\[
\lim_{\eta\to\infty}\frac{F_\mu(i\eta)}{i\eta}=1,
\]
(8)
and note that $F_\mu$ is analytic on $\mathbb C^+$ with nonnegative imaginary part.''',[4],'The normalization explicitly referenced when defining free additive convolution on page 5.')
passage(8,r'''Assume that $X=(X_{ab})$ in (3) has i.i.d. columns. For its entries, we further impose the following assumptions,

• Under $H_0$, $X_{ab}$'s ($a\in[[p]]$, $b\in[[N]]$) are independent.

• $\mathbb E[X_{ab}]=0$, $\mathbb E[|X_{ab}|^2]=1/N$ for all $a\in[[p]]$ and $b\in[[N]]$.''',[5],'The introductory iid-column convention and first two bullets retained by Assumption 1.19. The third all-moment bullet is deliberately excluded from this inherited excerpt.')
passage(9,r'''If $\hat y\in(0,\infty)$, under Assumptions 1.6 and 1.7, we have
\[
\frac{\operatorname{Tr}B^2-a_1}{b_1}\Rightarrow\mathcal N(0,1),
\]
where
\[
a_1=N\left(\sum_{r\ne s}^ky_ry_s+\sum_{t=1}^ky_t\right),\qquad b_1=4\sum_{r\ne s}^ky_ry_s(1-y_r)(1-y_s).
\]''',[8],'Complete Corollary 1.14 (Schott’s statistics), expressly inherited by Theorems 1.18 and 1.20 under their specified substitutions. The printed denominator b1 is not a square root; preserve it.')
passage(10,r'''If $\hat y\in(0,1)$, under Assumptions 1.6 and 1.7, we have
\[
\frac{\operatorname{Tr}\log(B)-a_2}{b_2}\Rightarrow\mathcal N(0,1),
\]
where
\[
a_2=\sum_{t=1}^k\left(N-p_t-\frac12\right)\log(1-y_t)-\left(N-Ny-\frac12\right)\log(1-y),
\]
\[
b_2=-2\log(1-y)+2\sum_{t=1}^k\log(1-y_t).
\]''',[8],'Complete Corollary 1.15 (Wilks’ statistics). Its dimensional regime is restricted to hat-y in (0,1); the printed denominator b2 is not replaced by its square root.')
passage(11,r'''For notational simplicity, we further define
\[
Q_t:=X_t'(X_tX_t')^{-2}X_t,\qquad W_t:=(X_tX_t')^{-1}X_t,\qquad t\in[[k]].
\]''',[18],'Q_t is used in Theorem 5.3 alpha and K. This unnamed matrix-product abbreviation is kept locally without inventing an API title. W_t is retained because it shares the source display, but has no Theorem dependency in this inventory.')
passage(12,r'''We also remark here in the general statement (14), $\mu_1\boxplus\mu_2\cdots\boxplus\mu_k$ could be $N$-dependent.''',[6],'Remark 1.10 distinguishes the moving free-convolution approximation from a fixed limiting law.')
passage(13,r'''For the case of $\hat y\in(0,1)$ and thus $H$ has trivial $0$ eigenvalues, we will use a contour which does not enclose $0$. While for other cases, we will simply use sufficiently large contour that encloses $\operatorname{supp}(\mu_\boxplus)$ (c.f., Lemma 4.1).''',[6],'Context distinguishing contours that exclude zero from contours enclosing the entire support; preserve the resulting ambiguity for Tr f(H) with a singular f at zero.')
passage(14,r'''The second assumption on dimensional parameters is to ensure that the sample covariance matrix $X_tX_t'$ is invertible with high probability.''',[5],'Remark 1.8 gives probabilistic motivation for inverse expressions; it does not define their value on singular samples. Do not silently supply a pseudoinverse.')
passage(15,r'''For any Hermitian matrix $A\in\mathbb C^{n\times n}$ we use $\lambda_1(A)\geq\cdots\geq\lambda_n(A)$ to denote the ordered eigenvalues of $A$ and sometime we also use the notation $\lambda_{\max}(A)\equiv\lambda_1(A)$ and $\lambda_{\min}(A)\equiv\lambda_n(A)$ instead.''',[11],'Ambient spectral ordering; standard functional calculus, transposition, matrix inverses, analytic derivatives, contour integration and weak/distributional convergence retain their usual mathematical meaning unless a source issue below says otherwise.')
issue('registered-source','The source is the registered 103-page arXiv v2 dated 8 Sep 2022, not assumed identical to the journal version. Main text ends on page 34 before Appendix A; appendix bodies are outside scope.',[1,34])
issue('density-normalization','Theorem 1.9 equation (16) prints denominator 2x rather than 2*pi*x. This is retained literally and is not silently asserted to be a normalized probability density. Theorem 1.17 calls the finite-y counterpart mu_mp,y without restating its density.',[6,9])
issue('truncated-centering','Theorem 5.3 subtracts a bare contour integral of E^chi Tr G times f without a Cauchy prefactor. The following proof writes -1/(2*pi*i). The inventory preserves the statement and records the discrepancy.',[29])
issue('variance-qualification','Theorems 1.11, 1.17 and 1.18 explicitly require variance greater than a fixed positive c; Theorem 5.3 does not repeat such a restriction. No extra condition is inserted.',[7,9,29])
issue('corollary-scales','Corollaries 1.14 and 1.15 print b1 and b2 themselves in the standardized denominator, with formulas usually suggestive of variance. Neither square root nor a squared b label is supplied by the extraction.',[8])
issue('contour-superscripts','Equation (18) defines gamma1^0 and gamma2^0 using gamma rather than gamma^0 on their right-hand sides, despite the preceding distinction. Both the source equation and the explanatory context are preserved.',[6,7])
issue('contour-endpoints','C7 ends at Im z=epsilon2, whereas C3 starts at sqrt(epsilon1^2-epsilon2^2). The written inequalities do not generally make these coincide. No repair to the contour is made.',[6])
issue('zero-eigenvalues','Definition 1.4 sums all eigenvalues of H. The hat-y<1 contours exclude zero and allow functions singular there. The statements do not explicitly redefine Tr f(H) as a sum only over nonzero eigenvalues; retain this unresolved convention.',[3,4,6,7,9])
issue('nonzero-spectrum','H is N by N, B is p by p and they share nonzero eigenvalues. Their zero multiplicities may differ. Do not identify all spectral statistics without accounting for f(0). The unknown-mean matrices have an additional centering rank constraint.',[3,9])
issue('inverse-domains','Definitions use inverse block covariance matrices and inverse square roots. Under the all-moment assumption samples can be discrete; high-probability invertibility does not specify a value on singular samples. No pseudoinverse or conditioning convention is invented.',[2,3,5,17,29])
issue('iid-columns','Assumption 1.6 has iid columns, but does not require all matrix entries to have the same distribution. Assumption 1.19 keeps the first two bullets and replaces the third; the introductory iid-column setting remains standing context.',[5,9,10])
issue('moment-replacement','Theorem 1.20 inherits conclusions under Assumptions 1.19 and 1.7, not under both 1.19 and the stronger all-moment Assumption 1.6. Its graph must not reach the full D13 assumption.',[10])
issue('growing-k','Assumption 1.7 permits k depending on N and states coordinatewise limits y_t -> hat-y_t for t=1,...,k. Uniformity of this indexing when k grows is not separately spelled out. Case 1 uses k~1 rather than the literal phrase fixed k.',[5,6,11])
issue('centered-block-index','The page-2 definition prints Y-hat_i with entries indexed by t and the range t in [[k]]. Theorem 1.18 consistently uses i in its diagonal. Preserve the source mismatch instead of rewriting the original passage.',[2,9])
issue('structural-index','The structural model uses x_t(i), while the next prose says x_i consists of independent components. This local notation discrepancy is preserved.',[3])
issue('stieltjes-differential','Equation (6) prints mu_N(dz) beside integrand 1/(lambda-z); the generic Stieltjes definition on page 4 uses dmu(x). Preserve the source differential, do not confuse it with the spectral parameter.',[3,4])
issue('mean-vector-measure','The mean vector mu_t in Section 1.1 and the Bernoulli probability measure mu_t in Section 1.2 are different objects reusing a symbol; the source passages and explanations keep them distinct.',[1,4])
issue('trace-normalization','Every lower-case tr is N^-1 Tr, even for p_t by p_t matrices. Theorem 1.18 changes its explicit centering from N to N-1, but does not globally redefine all source traces.',[4,9,11,29])
issue('tilde-substitution','Theorem 1.18 binds tilde Bernoulli parameters p_t/(N-1), retains its -1/z mean correction, and specifies simultaneous B->B-hat and N->N-1 in both Corollaries. The substitutions also affect y_t and y through their definitions; they do not change block sizes p_t.',[4,8,9])
issue('truncated-expectation','E^chi is a weighted expectation, not a conditional expectation or an expectation divided by E Xi. Its finite-N cutoff and fixed large K are preserved; alpha and beta in Theorem 5.3 are deterministic expectations defined inline.',[17,18,29])
issue('contour-bars','A bar over gamma in Section 4 denotes removing the near-real-axis pieces. A bar over C in Section 1.3 denotes complex conjugation. These are distinct source operations.',[6,18,29])
issue('complex-extensions','Generic Stieltjes and subordination functions are introduced on C+, while contour formulas also use the lower half-plane. The usual reflected analytic continuation is not separately defined in the main statements. No appendix was opened to supply it.',[4,7,9])
issue('subordination-k','Proposition 1.5 is stated for k probability measures; uniqueness in degenerate cases and its k=1 instance are not repaired here. Assumption 1.7 supplies a nontrivial spread condition for the actual matrix theorems.',[4,5])
issue('theorem-5-3-scope','Theorem 5.3 lies in the main-text proof section and therefore remains inventoried. Approximate subordination functions, stochastic domination and cumulant expansions occurring in proofs are not extra statement dependencies of the six inventoried Theorems.',[17,18,29])
issue('source-heading-typo','Assumption 1.6 is headed Assumption on matrix entrices; Assumption 1.19 prints entries. Both are retained as source terminology without renaming them to a synthesized condition.',[5,9])
REFS=[dict(from_claim_id=PID+'/T1.18',to_auxiliary_ids=['A9','A10'],reference_kind='conclusion_inheritance_with_substitutions',substitutions={'B':'B-hat','N':'N-1'},preserved_conditions='Retain each Corollary dimensional regime and substitute N consistently in y_t and y; retain Assumptions 1.6 and 1.7 as printed in Theorem 1.18.',evidence=[dict(page=9,location='Final sentence of Theorem 1.18')]),dict(from_claim_id=PID+'/T1.20',to_claim_ids=[PID+'/T1.11',PID+'/T1.17',PID+'/T1.18'],to_auxiliary_ids=['A9','A10'],reference_kind='conclusion_inheritance_with_replacement_assumption',replaces='Assumption 1.6 moment bullet',replacement='Assumption 1.19, with Assumption 1.7 retained',preserved_conditions='Retain analytic-function/contour regimes, positive-variance qualifications, the pmax restriction for the inherited 1.17 result, and the centered-matrix substitutions for inherited 1.18. The branches are separate retained results, not one conjunction of all their special conditions.',evidence=[dict(page=10,location='Theorem 1.20')])]
def main():
    d=dict(paper_id=PID,status='extracted',unranked_auxiliary_passages=A,source_issues=ISSUES,source_claim_references=REFS,ambient_prerequisites=['Finite-dimensional real vectors, block matrices, transpose, positive-definite inverse square roots and spectral functional calculus on their stated domains.','Probability laws, Bernoulli measures, standard normal law, point masses, positive part and weak convergence in probability; no mathlib availability verdict is made.','Complex differentiation, analytic functions, contour integrals and the source Stieltjes sign convention.','N-dependent models, sample-size normalization, fixed small/large constants and the precise asymptotic comparison conventions in A6.'],statement_local_bindings={'T1.9':'ell and the two special regimes; limiting Bernoulli laws are inline binders, not the finite-N projection ESD.','T1.11':'f, positive-variance qualification and complete a_f/sigma_f formulas (20)-(21).','T1.17':'pmax restriction, finite-y transform m_y and its distinct a_f/sigma_f formulas.','T1.18':'H-hat, tilde measures, their subordination functions and complete tilde centering/variance formulas; generic LSS uses member D8g.','T1.20':'All inherited claim/Corollary bodies remain saved, with replacement moment assumption and branch-specific restrictions; no all-moment dependency.','T5.3':'alpha_t, beta_t and K(z1,z2) are fully defined inline; Q_t is A11, with X_t resolved by D1; E^chi and clipped contours are D18 and D17.'})
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(A)} auxiliary passages and {len(ISSUES)} source issues.')
if __name__=='__main__':main()
