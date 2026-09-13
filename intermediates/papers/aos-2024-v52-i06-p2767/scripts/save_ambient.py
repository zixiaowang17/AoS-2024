"""Archive source conventions, proof-only context and unresolved statements."""
import json
from save_inventory import ROOT,PID

def main():
    aux=[]
    def add(n,s,ps,note,deps=()):aux.append(dict(local_id='A'+str(n),statement_original=s,evidence=[dict(page=p,location='Original main-text context A'+str(n)) for p in ps],scope_note=note,depends_on=list(deps)))
    add(1,r'''For a random variable $X$, let $\mathcal L(X)$ be the law (i.e. probability distribution) of $X$. For a probability distribution $P$ on a probability space $\Omega$ and a measurable map $T:\Omega\to\Omega'$, let $P\circ T^{-1}$ denotes the pushforward probability measure, i.e. $\mathcal L(T(X))$ with $\mathcal L(X)=P$. For a probability measure $P$, let $P^{\otimes n}$ be the $n$-fold product measure. For a positive integer $n$, let $[n]\triangleq\{1,\ldots,n\}$, and $x^n\triangleq(x_1,\ldots,x_n)$.''',[7],'Original law, pushforward, product and index notation. Randomized amplifiers require kernel interpretation beyond a deterministic map.')
    add(2,r'''Finally, we also define the sample amplification complexity as the smallest $n$ such that an amplification from $n$ to $n+1$ samples is possible:
\[
n^\star(\mathcal P)\triangleq\min\{n\in\mathbb N:m^\star(\mathcal P,n)\ge1\}.\tag{6}
\]''',[8],'Related source quantity. The inventoried7.1/7.2 statements use the amplification existence predicate directly; do not add complexity definitions solely because corollaries use them.',['D6'])
    add(3,r'''In the exponential family, the statistic $T(x)$ is sufficient and complete, and several well-known identities include $\mathbb E_\theta[T(X)]=\nabla A(\theta)$, and $\operatorname{Cov}_\theta[T(X)]=\nabla^2A(\theta)$.''',[12],'Original moment/derivative identities behind standardized Assumption2. Completeness and boundary differentiability require the appropriate regular family conventions, not assumed by a word alone.',['D7','D9'])
    add(4,r'''\[
\Delta(\mathcal M,\mathcal N)=\max\left\{\inf_{T_1}\sup_\theta\|P_\theta\circ T_1^{-1}-Q_\theta\|_{\mathrm{TV}},\inf_{T_2}\sup_\theta\|Q_\theta\circ T_2^{-1}-P_\theta\|_{\mathrm{TV}}\right\},
\]
where the loss function is taken over all measurable functions $L:\Theta\times\mathcal A\to[0,1]$.''',[8],'Original kernel characterization excerpt from Definition3.1, not its entire decision-risk display. The identity with amplification error is explanatory; Eq4 does not need the decision-theoretic characterization to be defined.',['D1'])
    add(5,r'''Given $n$ i.i.d. samples from an unknown distribution in $\mathcal P$, define the following Bayes risk and minimax risk:
\[
r_B(\mathcal P,n,L,\mu)=\inf_{\widehat\theta}\int_\Theta\mathbb E_\theta[L(\theta,\widehat\theta(X^n))]\mu(d\theta),
\]
\[
r(\mathcal P,n,L)=\inf_{\widehat\theta}\sup_{\theta\in\Theta}\mathbb E_\theta[L(\theta,\widehat\theta(X^n))],
\]
where the infimum is over all possible estimators $\widehat\theta(\cdot)$ taking value in $\mathcal A$.''',[17],'Source lower-bound proof machinery. No inventoried theorem statement requires a supplied prior or Bayes risk; Lemma6.1 is not promoted to a theorem dependency.')
    add(6,r'''In this model, $T_{n+m}$ is complete and sufficient, and we choose $S=S(X^{n+m})=(S_1,\ldots,S_{n+m-1})$ with $S_i=X_{i+1}-X_1$ for all $i$. Clearly $S$ is ancillary, and $X^{n+m}$ could be recovered from $(T_{n+m},S)$ via
\[
X_1=T_{n+m}-\frac{\sum_{i=1}^{n+m-1}S_i}{n+m},\qquad X_{i+1}=X_1+S_i,\quad i\in[n+m-1].
\]
Therefore, the choice of $S$ satisfies both conditions. Consequently, we can draw $Z^{n+m}\sim\mathcal N(0,\Sigma)^{\otimes(n+m)}$, compute $S=S(Z^{n+m})$ (where $S_i=Z_{i+1}-Z_1$), and recover $X^{n+m}$ from $(T_{n+m},S)$.''',[11],'Original Example4.2 construction clarifies the product sampling shorthand in Example4.1. It is a way to implement that conditional distribution, not an additional requirement in6.2.',['D7','D16','D17'])
    add(7,r'''1. Input: samples $X_1,\ldots,X_n$, a given class of distributions $\mathcal P$.
2. Based on samples $X_1,\ldots,X_{n/2}$, find an estimator $\widehat P_n$ such that
\[
\sup_{P\in\mathcal P}\mathbb E_P[\chi^2(\widehat P_n,P)]\le C\cdot r_{\chi^2}(\mathcal P,n/2).
\]
3. Draw $m$ additional samples $Y_1,\ldots,Y_m$ from $\widehat P_n$.
4. Uniformly at random, shuffle the pool of $X_{n/2+1},\ldots,X_n,Y_1,\ldots,Y_m$ to obtain $(Z_1,\ldots,Z_{n/2+m})$.
5. Output: amplified samples $(X_1,\ldots,X_{n/2},Z_1,\ldots,Z_{n/2+m})$.''',[16],'Complete Algorithm2. It witnesses the upper bound but is not required to define minimax error or chi-squared estimation risk in5.2. Odd n and unattained/zero minimax-risk conventions are unspecified.',['D3','D14'])
    add(8,r'''1. Input: samples $X_1,\ldots,X_n$, a given class of product distributions $\mathcal P=\prod_{j=1}^d\mathcal P_j$
2. for $j=1,2,\ldots,d$ do
3. Based on samples $X_{1,j},\ldots,X_{n/2,j}$, find an estimator $\widehat P_{n,j}$ such that
\[
\sup_{P_j\in\mathcal P_j}\mathbb E_{P_j}[\chi^2(\widehat P_{n,j},P_j)]\le C\cdot r_{\chi^2}(\mathcal P_j,n/2).
\]
4. Draw $m$ additional samples $Y_{1,j},\ldots,Y_{m,j}$ from $\widehat P_{n,j}$.
5. Uniformly at random, shuffle $X_{n/2+1,j},\ldots,X_{n,j},Y_{1,j},\ldots,Y_{m,j}$ to obtain $(Z_{1,j},\ldots,Z_{n/2+m,j})$.
6. end for
7. For each $i\in[n/2+m]$, form the vector $Z_i=(Z_{i,1},\ldots,Z_{i,d})$.
8. Output: amplified samples $(X_1,\ldots,X_{n/2},Z_1,\ldots,Z_{n/2+m})$.''',[16],'Complete Algorithm3 with coordinatewise shuffles. Not the same operation as shuffling full observed vectors; it need not preserve original second-half vectors. No proof-only algorithm edge is imposed on5.5.',['D3','D14','D15'])
    add(9,r'''If the log-partition function $A(\theta)$ satisfies
\[
\sup_{\theta\in\Theta}\sup_{u\in\mathbb R^d\setminus\{0\}}\frac{|\nabla^3A(\theta)[u;u;u]|}{(\nabla^2A(\theta)[u;u])^{3/2}}\le M<\infty,
\]
then the exponential family satisfies the moment condition $M_k$ for all $k\in\mathbb N$. Here for a $k$-tensor $T$ and vectors $u_1,\ldots,u_k$, $T[u_1;\ldots;u_k]$ denotes the value of $\langle T,u_1\otimes\cdots\otimes u_k\rangle$.''',[12],'Original Lemma4.4 gives a sufficient criterion. It is not part of Assumption2 and is not imported backwards as a required hypothesis in4.5/4.6.',['D9','D11'])
    add(10,r'''Specifically, we drop Assumption 2 while introducing an additional assumption.''',[18],'Original transition to lower-bound Assumption3. Theorem6.3 must not inherit moment condition2 or the upper-bound algorithm.',['D18'])
    bindings={
'T4.5':'Natural exponential family, its statistic T and averaged T_n, iid samples under P_theta, Assumptions1 and2 with k=3, minimax amplification error and normalized TV. The theorem’s final existence clause uses Definition1.1. C depends on dimension and moment bound; n sufficiently large is not a dimension-free threshold. The middle TV expression is theta-specific as printed, whereas epsilon-star is a supremum-over-model minimax quantity; preserve this source mismatch.',
'T4.6':'Product of one-dimensional natural exponential families, each satisfying Assumptions1/2 with k=10; the same average-statistic identity procedure. Normalized TV, minimax error and amplification-existence predicate. The source C is independent of n,d, but does not quantify a shared moment bound over growing coordinates; preserve original statement and this limitation.',
'T5.2':'General iid model class, amplification error and expected estimator-first chi-squared estimation risk at n/2. No sufficiency, exponential family, CLT, KL divergence, or particular shuffling algorithm is required to state the bound. Preserve n,m>=0, division by n and missing n/2 rounding conventions.',
'T5.5':'Cartesian product model and its coordinate families, amplification minimax error and coordinate expected chi-squared minimax risks summed under one square root. Coordinates may differ; there is no exponential-family restriction. Sample shuffling is proof machinery, not a statement assumption.',
'T6.2':'Unknown-mean known-covariance Gaussian location family, minimax amplification error and TV between zero-mean identity-covariance Gaussians. The final sentence specifically invokes Example4.1 identity-statistic conditional-generation procedure. I_d and Gaussian measures are ambient. Singular Sigma is not excluded in the printed theorem, though its d-dimensional exact formula then needs correction.',
'T6.3':'Natural exponential family with Assumptions1 and3 only, minimax amplification error, n,m positive-integer conventions, minimum with1, universal c and family/dimension-dependent C. Neither moment Assumption2 nor upper-bound algorithm is imported. Complete continuation on19 retained.',
'T6.4':'General product model, coordinate parameter sets, epsilon in(0,1), per-coordinate pairs and alpha_j values between fixed lower/upper alpha endpoints. Two original TV inequalities at n and n+m are inline hypotheses. No Hellinger Assumption4 is added; it is used only in the next theorem. Constant c depends on the alpha endpoints.',
'T6.5':'General product model and Assumption4 with Hellinger square normalized by1/2. Its reference to6.4 imports only the product structure. For the given n, coordinate pairs exist at Hellinger-square scale1/n. Epsilon uses the surrounding(0,1) convention; ceiling is retained. For each c>0 there is c-prime depending only on c, not the model or n,d,epsilon.',
'T7.1':'Original discrete class on d+1 points with known mass p0=t in the stated interval. The theorem asserts existence of an(n,n+1,0.1) uniform-TV amplification procedure. Its if-and-only-if asymptotic Omega condition is not an exact numerical threshold. It contains no unknown-distribution learning-risk requirement.',
'T7.2':'Original isotropic rank-d projection covariance model in R^p with zero mean and unknown subspace, p>=d+1. Amplification predicate with error0.1; exact threshold n>=d. It is not the known-covariance location model of6.2.',
'T7.3':'Base L-Lipschitz probability densities on[0,1] and the distinct everywhere-c-lower-bounded subclass. L>=8 and c fixed in(0,1). Maximal additional sample count m-star uses the source fixed-small-error abbreviation, with asymptotic constants potentially depending on L,c. The theorem contains no chi-squared risk even though its proof and subsequent explanation discuss it.'}
    refs=[]
    def ref(n,target,kind,note):refs.append(dict(claim_id=PID+'/T'+n,target=target,reference_kind=kind,note=note))
    ref('4.5','Assumptions1/2; T_n on12','assumption_and_definition_reference','Use k=3 for the full family; archive actual mean-statistic definition and identity map.')
    ref('4.6','Assumptions1/2 on each one-dimensional factor','assumption_reference','Use k=10 componentwise; do not silently identify this with the same full d-dimensional moment bound as4.5.')
    ref('6.2','Example4.1','definition_reference','Final theorem sentence explicitly asserts optimality of this particular sufficiency-based procedure.')
    ref('6.3','Assumptions1/3','assumption_reference','Section6.1 expressly drops Assumption2. No upper-bound procedure is a required input.')
    ref('6.5','Assumption4 and Theorem6.4 product structure','definition_reference','Import only product structure into4, not TV-threshold hypotheses(10)–(11).')
    for n in ['5.2','5.5']:ref(n,'Algorithms2/3 and Lemma5.8','proof_only','These construct witnesses for the minimax bound; definitions of the theorem terms do not require running a chosen estimator or shuffle.')
    for n in ['6.2','6.3','6.4','6.5']:ref(n,'Lemma6.1 and decision risks','proof_only','No supplied prior/loss appears in these theorem statements.')
    for n in ['4.5','4.6','5.2','5.5','6.2','6.3','6.4','6.5','7.1','7.2','7.3']:ref(n,'Appendix B proof','proof_only','Appendix bodies are outside scope and not imported.')
    issues=[]
    def issue(key,ps,note):issues.append(dict(issue_id=key,evidence=[dict(page=p,location='Source issue '+key) for p in ps],note=note))
    issue('registered-source',[1,22],'Registered arXiv2201.04315v2: stamp18Sep2024, title-page19Sep2024,62pages. Main text ends22; Appendix A begins23. Preserve version identity rather than substituting the2024 published text.')
    issue('randomized-maps-and-conditionals',[1,7,9],'The source writes randomized maps using deterministic pushforward notation and conditions on exact sufficient-statistic values. Interpret through parameter-independent Markov kernels; common regular conditional versions and existence on arbitrary spaces are not supplied. A conditional law for one chosen P0 is defined only almost surely under its own statistic law, so transplanting it requires compatible versions.')
    issue('infimum-versus-existence',[1,7,8],'Definition1.1 requires an attained amplifier with error<=epsilon; Eq4 is an infimum. Eq5 equates its<=epsilon sublevel set with existence, which requires attainment or slack. The maximum in Eq5 may be empty or unbounded, e.g. a known singleton distribution permits arbitrarily many samples. No extended-value convention is supplied.')
    issue('pointwise-versus-minimax',[13,14],'Theorems4.5/4.6 say for theta inTheta and put a theta-specific TV distance between epsilon-star and a uniform bound. Minimax epsilon-star is controlled by a supremum of a procedure’s errors, not automatically by every pointwise value. Retain the missing supremum in original text and do not silently fix it.')
    issue('parameter-domain',[11,12,18],'Theta is the full finite-log-partition domain, which can contain boundary points. Assumption1 only says nonempty interior, while Assumption2 uses gradients/Hessian inverse at every theta. Boundary differentiability, finite moments and inverse square root require additional interpretation; do not replace Theta by its interior.')
    issue('uniformity-of-moments',[12,13,14],'Assumption2 is uniform over theta;4.5 allows its constant to depend on d and the moment bound. Theorem4.6 assumes finite tenth moments for each one-dimensional component and calls C independent of n,d; a common componentwise moment bound over growing d is not explicitly quantified. Preserve the distinction between stated uniformity and a possible needed strengthening.')
    issue('moment-criterion-not-required',[12],'Lemma4.4 is a sufficient self-concordance criterion for moments. It does not define Assumption2 or become a prerequisite for4.5/4.6. Its general claims of completeness/self-concordance require regularity but are not proof-checked in this census.')
    issue('zero-and-odd-sample-sizes',[15,16],'Theorems5.2/5.5 quantify n,m>=0 but divide by n and evaluate learning at n/2. Algorithms2/3 index n/2 observations without rounding. Retain these formulas and explicitly leave n=0, odd n and0*infinity conventions unresolved.')
    issue('divergence-orientation',[7,14,20],'Expected chi-squared risk uses chi2(estimated P, true P), with true P in the denominator. Reverse orientation is different. Hellinger has a1/2 normalization before square root; Assumption4 uses H squared, not H.')
    issue('singular-known-covariance',[10,18],'Theorem6.2 specifies a fixed covariance matrix but no positive-definiteness condition. Its exact RHS uses dimension d and removes Sigma. For Sigma=0, one observation identifies theta and amplification error is zero, whereas the printed RHS is positive for d>0,m>0. Preserve source statement and record the missing nonsingularity/rank convention; do not conflate this model with7.2.')
    issue('linear-versus-affine-independence',[18],'Assumption3 excludes only a^T T=0 almost everywhere, not a^T T=constant. General minimal exponential-family criteria require affine independence; the accompanying minimality assertion is stronger than that wording alone. Assumption1 supplies separate absolute continuity in6.3. Keep the original assumption without strengthening it.')
    issue('product-pairs-and-continuity',[19,20],'Assumption4 requires existence of two points at a prescribed Hellinger scale for each coordinate and the given n. It does not state continuity of the entire parameter map, despite subsequent prose describing continuity. Its reference to6.4 imports product structure, not the two TV bounds. Pairs may vary with n.')
    issue('epsilon-and-ceiling',[8,19,20],'Theorem6.5 leaves epsilon unquantified in its own first sentence; the surrounding context uses epsilon in(0,1). Preserve the ceiling on c epsilon n/sqrt(d) and the c-then-c-prime quantifier order. Do not remove integer rounding or make c-prime universal in c.')
    issue('rates-and-models',[21,22],'Theorem7.1 uses if-and-only-if n=Omega(1/t), an asymptotic rate rather than an exact numerical threshold. Theorem7.2 has exact n>=d for projection covariance, not arbitrary low-rank PSD matrices. Theorem7.3 gives two-sided n^(5/6) only for the lower-bounded subclass and an upper bound n^(3/4) for the larger class; do not make the latter two-sided.')
    data=dict(paper_id=PID,unranked_auxiliary_passages=aux,statement_local_bindings=bindings,source_claim_references=refs,source_issues=issues,unresolved_external_prerequisites=[],ambient_prerequisites=['Probability laws, iid product experiments, measurable maps and Markov kernels; parameter-independent randomization, regular conditional probabilities and sufficient-statistic reductions.','Finite-dimensional Gaussian measures, Euclidean norms, gradients, Hessians and positive inverse square roots; base measures, densities and log-partition normalization. Derivative identities do not certify regularity at boundary points.','Normalized TV, Hellinger and asymmetric chi-squared divergence as archived. Conditional sampling, expected risk, infima over distribution estimators and uniform suprema over model families.','Natural-number sample sizes, finite products, ceilings, min/max, asymptotic orders and dimension-dependent constants. Zero/odd sample sizes, unattained infima and unbounded maxima retain explicit source limitations.','Finite-alphabet probabilities, known mass constraints, orthonormal-column matrices and projection covariances, scalar Lipschitz densities and pointwise lower bounds. No mathlib availability or proof-correctness verdict.'],validation_limits='All original main-text Theorems and relevant source definitions are preserved. Structural/source checks do not certify theorem truth or fill missing kernel, domain, uniformity, attainment and endpoint conventions. Appendix bodies are excluded.')
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
