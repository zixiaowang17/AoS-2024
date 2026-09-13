"""Preserve unranked source conventions and unresolved issues for this paper."""
import json
from save_inventory import PID, ROOT
A=[]
def passage(n,s,pages,note):
    A.append(dict(local_id=f'A{n}',statement_original=s,evidence=[dict(page=p,location=f'Auxiliary source passage A{n}') for p in pages],scope_note=note))
passage(1,r'''For the pair of a scalar response $Y$ and a $d$-dimensional covariate $\mathbf X\equiv(X_1,\ldots,X_d)^\top$, we study additive regression when $d$ is allowed to be much larger than the sample size $n$. Throughout this paper, we assume that each covariate $X_j$ is compactly supported, say on $[0,1]$.''',[4],'Standing population and compact-support convention. Statements on unbounded domains are not added to the census.')
passage(2,r'''Suppose that we observe i.i.d. copies $(\mathbf X_i,Y_i)$ of $(\mathbf X,Y)$. We write $\mathbf X_i=(X_{i1},\ldots,X_{id})^\top$.''',[4],'Sampling convention for all empirical quantities. The sample mean Y-bar is used in the source with its ordinary meaning n^{-1} sum_i Y_i; it is not a separate ranked interface.')
passage(3,r'''For a tuple of $d$ functions, $\boldsymbol\eta=(\eta_1,\ldots,\eta_d)^\top:[0,1]^d\to\mathbb R^d$, let $\|\boldsymbol\eta\|_q$ be defined by $\|\boldsymbol\eta\|_q^2:=\sum_{j=1}^d\|\eta_j\|_q^2$. Likewise, we define the inner product of two tuples in an obvious way.''',[7],'Tuple norm is the sum of component squared norms; it differs from the scalar norm of the sum. The scalar convention is D9.')
passage(4,r'''The fLasso-SBF algorithm actually produces $\widehat f_k^{(r,j)}$ that satisfies the constraint (2.4) for all $1\leq j,k\leq d$ and $r\geq1$, provided that the initial $\widehat{\mathbf f}^{(0)}$ is chosen so that all its components satisfy the constraint.''',[8],'Original initialization condition: empirical centering of each initial component. This standing algorithm convention is retained without inserting it into Theorem 1.')
passage(5,r'''We now discuss the convergence of the fLasso-SBF algorithm. Let
\[
R:=\max_{\mathbf g:L_n^{\mathrm{pen}}(\mathbf g)\leq L_n^{\mathrm{pen}}(\widehat{\mathbf f}^{(0)})}\sum_{j=1}^d\|g_j-\widehat f_j\|_{\widehat p}.
\]
(2.15)''',[8],'Theorem 1 level-set radius depends on D10, D15 and D9. The source writes max, not sup. It is an auxiliary parameter of the theorem rather than an invented reusable definition.')
passage(6,r'''Put
\[
p_j^h(x_j):=E(\widehat p_j(x_j))=\int_0^1K_{h_j}(x_j,u_j)p_j(u_j)du_j.
\]''',[10],'Expected smoothed marginal density used in D23 and D24. Its integral variable u_j is distinct from the evaluation variable used to normalize K_h.')
passage(7,r'''We also make a note here that under the assumptions (A1), (A4) and (A5) there exist absolute constants $0<c_{r,L}<c_{r,U}<\infty$ such that, with probability tending to one,
\[
c_{r,L}<\min_{1\leq j\leq d}\inf_{x_j\in[0,1]}\frac{\widehat p_j(x_j)}{p_j^h(x_j)}\leq\max_{1\leq j\leq d}\sup_{x_j\in[0,1]}\frac{\widehat p_j(x_j)}{p_j^h(x_j)}<c_{r,U}.
\]
(2.18)
We refer to Lemma S.1 in the Supplementary Material for such a result.''',[10,11],'These are the fixed ratio constants in D24. The explicit main-text restriction is archived; the supplementary proof was not read and is not a statement dependency.')
passage(8,r'''In the theorem and throughout this paper, we use the following notions of “approximate” inequalities. For a stochastic sequence $\{Z_n\}$ and a deterministic one $\{a_n>0\}$, we write $Z_n\lesssim a_n$ if there exists an absolute constant $0<C<\infty$ such that $|Z_n|/a_n\leq C$ with probability tending to one. Also, we often write $Z_n\ll a_n$ if $Z_n=o_p(a_n)$. For two deterministic sequences $\{a_n>0\}$ and $\{b_n>0\}$, we write $a_n\lesssim b_n$ if $a_n/b_n\leq C$ for all $n$, and $a_n\ll b_n$ if $a_n/b_n\to0$ as $n\to\infty$.''',[11],'The paper-specific stochastic lesssim is stronger than generic boundedness in probability. Standard expectations, probabilities, sequence limits, extrema, cardinality and elementary real operations remain ambient.')
passage(9,r'''For $0\leq\ell\leq2$, put
\[
C_{f,\ell}:=\max_{1\leq j\leq d}\sup_{x_j\in[0,1]}|f_j^{(\ell)}(x_j)|,
\]
(2.19)
where $f_j^{(\ell)}$ denotes the $\ell$th derivatives of $f_j$. By the assumption (A3), the constants $0\leq C_{f,\ell}<\infty$ are bounded. Let $a\wedge b$ denote $\min\{a,b\}$, and $C_1$ be an absolute constant such that
\[
C_1>4\sqrt3\max\left\{\frac{\sqrt2c_{h,U}^{3/2}c_{p,U}C_{f,1}}{\sqrt{c_{p,L}}},\frac{\sqrt{10}c_K\sigma\sqrt{c_{p,U}c_{h,U}}}{c_{p,L}c_{h,L}}\right\}.
\]''',[11],'C1 in Theorem 2 and (2.21) uses A1, A3, A4, A5 and A6 constants. Square-root extents were checked against an enlarged PDF crop. The source claim about inactive derivatives remains an unresolved convention.')
passage(10,r'''\[
2C_1\left(\sqrt{\frac{\log(d\vee n)}{nh}}+h^{3/2}\right)\leq\lambda\lesssim\sqrt{\frac{\log(d\vee n)}{nh}}+h^{3/2},
\]
(2.21)''',[12],'The penalty restriction cited in Theorems 3–5 has both lower and upper bounds. C1 is A9; the nearby compatibility condition is liminf phi > 0. Theorem 2 itself requires only the lower bound.')
passage(11,r'''Recall that $I:\mathcal H_1\times\cdots\times\mathcal H_d\to\mathcal H_1\times\cdots\times\mathcal H_d$ is the identity operator.''',[14],'Identity and coordinate projections are ordinary operators. The source also specifies I_j(eta)=eta_j on page 14; Section 2 represents the identity formally with a Dirac delta kernel, not a bounded function.')
passage(12,r'''Recall $\widehat{\mathbf m}^{A}=(\widehat m_1^{A},\ldots,\widehat m_d^{A})^\top$ and $\widehat{\mathbf m}^{B}=(\widehat m_1^{B},\ldots,\widehat m_d^{B})^\top$,
\[
\widehat m_j^{A}(x_j):=\widehat p_j(x_j)^{-1}\cdot n^{-1}\sum_{i=1}^nK_{h_j}(x_j,X_{ij})\epsilon_i,
\]
\[
\widehat m_j^{B}(x_j):=\widehat p_j(x_j)^{-1}\cdot n^{-1}\sum_{i=1}^nK_{h_j}(x_j,X_{ij})\left\{E(Y)+\sum_{k=1}^df_k(X_{ik})\right\}.
\]''',[16],'Explicit component formulas for D32; A uses noise, B uses the conditional-mean signal. No independence or constant-variance assumption from the later unnumbered CLT is imported.')
passage(13,r'''Now, we state a theorem that gives an upper bound of $s_q\vee s_q^*$. For $\alpha\in(0,1)$ and $\beta>0$, put
\[
c_q(\alpha,\beta):=\min\left\{\frac{1-\alpha}{2\sqrt{2(1+\alpha)}},\frac1\alpha\left(\frac{\beta(1-\alpha^q)}{2(1+\beta)}\right)^{1/q}\right\}.
\]''',[18],'Theorem 7 numerical coefficient, with q>0 from the theorem. Enlarged PDF inspection confirms that 2(1+alpha) is entirely inside the root and the leading 2 is outside.')
passage(14,r'''where $p$ is the joint density function of $\mathbf X$.''',[9],'Population density notation: p_j is the marginal density of X_j (page 4), and p_jk is the two-dimensional density of (X_j,X_k) (page 5). These population primitives do not depend on their empirical estimators.')
passage(15,r'''In the statements of the assumptions and throughout this paper, by “absolute constant” we mean a constant independent of $n$. Let $a\vee b:=\max\{a,b\}$.''',[9],'The source permits d and the active set to depend on n. Uniformity in coordinate indices is preserved when explicitly stated.')
ISSUES=[]
def issue(key,text,pages):
    ISSUES.append(dict(issue_id=key,description=text,evidence=[dict(page=p,location='Original source notation or scope') for p in pages]))
issue('level-set-radius','Theorem 1 assumes only R<infinity, while its display divides by R squared. R=0 is not excluded explicitly. The definition also writes a maximum without establishing attainment.',[8])
issue('minimizer-selection','The source defines a minimizer and an optimization solution without giving a tie-breaking or measurable-selection convention, or separately proving existence in the main-text definitions.',[5,6,14])
issue('subgradient-selection','At a zero component, the printed unit-ball description permits multiple subgradients. The stationarity equation requires a compatible selection; not every unit-ball choice satisfies it.',[7])
issue('frechet-at-zero','The source calls the derivative of the nonsmooth penalized loss a Frechet derivative when a subgradient is needed at zero. The census does not turn this proof claim into a premise.',[7])
issue('empirical-zero-density','Marginal regression and empirical conditional-density kernels divide by p-hat_j without specifying behavior on zero-density events. Later high-probability bounds do not define those exceptional events.',[5,6,13])
issue('zero-threshold','Algorithm 1 and the estimator threshold formula divide by a residual norm. The usual zero-output convention at zero residual is implicit, not printed in these equations.',[6,8])
issue('algorithm-initialization','The centered initial tuple is a standing condition in the preceding algorithm discussion, not repeated in Theorem 1. The unchanged-coordinate line in Algorithm 1 omits hats.',[8])
issue('function-representatives','L2 functions are treated as pointwise functions without explicitly specifying the almost-everywhere quotient or versions needed for point evaluations, derivatives and sup norms.',[4,18])
issue('kernel-normalization','The normalizer integrates in x. The claimed 1<=c_h<=2 and interior equality require the later kernel conditions and sufficiently small bandwidths; they do not follow from support alone.',[4,10])
issue('tuple-versus-sum','A tuple squared norm is a sum of component squared norms. It is distinct from the scalar squared norm of the sum in the compatibility cone and Theorem 1.',[7,8,11])
issue('operator-kernel-domain','Generic integral kernels are assigned function-space operators without a separate integrability or boundedness condition. The Dirac identity representation is distributional, not an ordinary bounded kernel.',[6])
issue('centered-redefinition','Section 3 reuses Pi-hat after subtracting the empirical marginal density from off-diagonal kernels. Its printed tilde-pi domain is [0,1] times [0,1]^d while its arguments are written as two bold vectors. Both source notation and the separate definitions are retained.',[13])
issue('active-set','S uses population norms and S_n uses empirical norms. Their equality is conditional on density-ratio bounds. Empty S makes several gamma, bandwidth and compatibility expressions undefined unless extra conventions are supplied.',[9,11,14])
issue('inactive-derivatives','A3 bounds derivatives of active functions, but C_f,ell takes a maximum over all components. Inactive components vanish only in the population L2 sense; representative and differentiability conventions are implicit.',[10,11])
issue('a2-domain-clause','A2 prints an ambiguous coordinate-domain clause in its Lipschitz supremum. It is preserved rather than silently rewritten as a different quantified condition.',[10])
issue('conditional-mgf','A6 is a conditional subexponential MGF bound over a finite transform-parameter interval. The source does not identify sigma squared as the error variance; the response second moment may diverge with dimension.',[10])
issue('compatibility-domain','The compatibility infimum restricts to p^h-centered tuples with a nonzero active denominator. It uses expected smoothed density, not p or p-hat. Existence of an admissible tuple and empty-cone conventions are implicit.',[11])
issue('ratio-constants','The c_r constants are introduced by a main-text high-probability statement citing a supplementary proof. Only that explicit statement is retained; the lemma is outside scope.',[10,11])
issue('stochastic-rate','The paper defines stochastic lesssim using one fixed absolute bound with probability tending to one; replacing it by generic O_P would weaken the recorded conclusion.',[11])
issue('asymptotic-array','d, S, bandwidths and other model quantities may depend on n. Absolute constants are defined as independent of n; no extra fixed-dimensional interpretation is imposed.',[9,10])
issue('spectral-assertion','The source claims that I+Pi has eigenvalues in [0,1]. This is preserved as a source assertion, not established by the census or used to infer invertibility. The source separately assumes invertibility.',[15])
issue('inverse-kernels','Writing the inverse as I+Theta with ordinary coordinate kernels and finite row sup norms entails well-definedness conditions not separately spelled out by the main-text inverse definition.',[15,18])
issue('gamma-domain','Gamma involves the unknown true active-set size and an unspecified diverging sequence a_n. Feasibility and implementability of that theoretical tuning choice are not certified.',[14])
issue('optimizer-branch','Theorem 6 changes the feasible set for its second branch by adding a candidate-kernel derivative constraint; it also assumes a separate derivative bound on the true kernel. These two roles are preserved separately.',[18])
issue('derivative-coordinate','A7 differentiates the discrepancy magnitude in u_j. Theorem 6 uses the second kernel coordinate x_k. These are different regularity restrictions.',[16,18])
issue('optimizer-grid','The numerical approximation maximizes over i not equal to i-prime, although the continuous objective takes the supremum over the full square. The discretization is not substituted for the theorem estimator.',[14,15])
issue('q-zero','The q=0 formula is explicitly interpreted as a count of nonzero kernels, which entails a convention for a zero norm raised to power zero. Theorem 7 instead requires strictly positive q.',[18])
issue('adjoint-index','The source calls Theta_jk star the adjoint of Theta_jk but writes its kernel as Theta_kj with swapped arguments. This is the block-transpose convention as printed; the individual-block index interpretation is not silently repaired.',[18])
issue('sparsity-analogy','The source compares inverse-kernel row/column summaries with a precision-matrix sparsity parameter. The keyword is retained as an analogy; no equality of these mathematical objects is asserted.',[18])
issue('theorem-condition-inheritance','Theorems 4 and 5 assume the conditions of Theorem 3, not its conclusion. Theorem 6 cites only A1, A2, A4, A5 and A7; Theorem 7 cites none of the A assumptions.',[16,17,18])
issue('pointwise-versus-uniform','Theorem 4 fixes an interior point for each j, whereas Theorem 5 takes a maximum over j and a supremum over the closed unit interval. Their bandwidth restrictions are different.',[16,17])
issue('unnumbered-clt','The normal limit, confidence interval and test after Theorem 5 are not labeled Theorem. Their additional error independence and homoskedasticity assumptions do not become assumptions of Theorems 4 or 5.',[17])
issue('selection-prose','Page 12 says the estimator vanishes for all j in S under suitable conditions, although S denotes significant components. This possible source typo is not used to alter the definition or invent a theorem.',[9,12])
issue('excluded-proofs','Appendix and supplementary bodies are excluded. Main-text references to them are preserved without following the references or certifying the proofs.',[8,11,16,18])
RESOLUTION={
    'shared':{'local_objects':'D1 resolves the additive model and population centering; D2 the coordinate function spaces; D3–D16 the empirical estimators, scalar norms and Algorithm 1; D17–D24 assumptions A1–A6 and compatibility; D25–D35 the centered operators, debiasing, A7 and Section 4 norms and constraints.', 'ambient_or_bound':'A1–A3 preserve compact support, iid sampling and tuple norms. Population densities are ambient in A14, not dependent on their estimators. A8/A15 preserve the special rate convention and absolute constants. Ordinary finite indices, real functions, expectation, probability, integration, identity operators, algebra and sequence limits remain ambient.', 'source_scope':'Main text only. An appendix or supplement citation is retained as an unresolved/excluded reference, not followed.'},
    '1':{'local_objects':'D4 gives p-hat; D9 gives weighted norms; D10 gives the penalized loss and minimizer; D15 gives iterates and initialization. A5 resolves R through the same loss, minimizer and initial tuple.', 'ambient_or_bound':'q0, r and the centered test tuple eta are quantified in the theorem. A4 records the standing initialization condition; A3 distinguishes tuple and sum norms.', 'branch_scope':'Nonasymptotic statement; no A1–A7 or asymptotic bandwidth assumptions are imported.'},
    '2':{'local_objects':'D17–D22 resolve A1–A6, D24 phi, D16 the active-set size, D10 the estimator, D1 the true components and D9 the norm.', 'ambient_or_bound':'The bandwidth inequality (2.20) is bound in the theorem. C1 is A9 and uses the listed assumption constants. Lambda has only the stated lower bound; A8 resolves lesssim and ll.', 'branch_scope':'Phi is positive for each d but may approach zero; the conclusion is a sum of errors.'},
    '3':{'local_objects':'A1–A6 are D17–D22 and A7 is D31. D24 gives phi; D28 gives the debiased estimator, D1 the true components, D9 the norm and D30 s1. The referenced bandwidth restriction (2.20) uses D16 and D24.', 'ambient_or_bound':'(2.20) is the displayed local inequality in Theorem 2, not its conclusion. (2.21) is A10 with C1 in A9. Gamma is part of D27.', 'branch_scope':'Phi must now be bounded away from zero. The conclusion is a maximum of component errors.'},
    '4':{'local_objects':'The conditions of Theorem 3 resolve to D17–D22, D31, D24 and D16. D28 is the debiased estimator; D1 the true components; D27 the estimated inverse; D30 s1; D32 the noise smoother.', 'ambient_or_bound':'A11 resolves I_j; A12 gives the explicit noise formula. h_j is in A5/D21. The three bounds in (3.11) and a fixed interior x_j are local hypotheses. C1 and (2.21) are A9/A10.', 'branch_scope':'Inherits the hypotheses of Theorem 3, not its error conclusion. The leading stochastic term is not itself asserted normal here.'},
    '5':{'local_objects':'Same inherited conditions and estimator/noise objects as Theorem 4: D17–D22, D31, D24, D16, D28, D1, D27, D30 and D32.', 'ambient_or_bound':'I_j and m-hat-A are A11/A12. The condition (1+s1^2)nh^3->0 is locally bound. (2.20) and (2.21) are inherited restrictions; no (3.11) is imported.', 'branch_scope':'Uniform over all coordinates and all x_j in [0,1]. The later unnumbered normal limit is excluded.'},
    '6':{'local_objects':'Only D17, D18, D20, D21 and D31 are directly assumed A conditions. D27 gives the estimated inverse and gamma, D29 its population target, D26 the mixed norm, D30 s1, D33 the sup norm and second-coordinate derivative, D34 s_q and D35 the extra candidate constraint.', 'ambient_or_bound':'The true-kernel derivative bound is an inline hypothesis in the second branch. q ranges over [0,1]; D34 records the zero-count convention. A8 resolves stochastic bounds.', 'branch_scope':'The second branch changes the optimization problem and adds true-kernel smoothness. No A3, A6, penalty-rate (2.21), or debiased estimator is imported.'},
    '7':{'local_objects':'D34 gives s_q and s_q star through population inverse D29 and the kernel sup norm D33. The displayed density-ratio norm also uses D33.', 'ambient_or_bound':'A14 resolves population densities and A13 c_q. q, alpha, beta, the coordinate permutation and the exponential decay inequality are bound in the theorem. The source later permits alpha/beta to vary with d.', 'branch_scope':'Entirely population-level: no empirical estimator, gamma, A1–A7, or preceding theorem conclusion is imported.'}}
def main():
    data=dict(paper_id=PID,unranked_auxiliary_passages=A,source_issues=ISSUES,statement_resolution=RESOLUTION,unresolved_source_references=[dict(reference='Appendix A and Supplementary Material',status='excluded_by_scope',resolution='Main-text citations preserved; referenced bodies not consulted.')])
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(A)} auxiliary passages and {len(ISSUES)} source issues.')
if __name__=='__main__':main()
