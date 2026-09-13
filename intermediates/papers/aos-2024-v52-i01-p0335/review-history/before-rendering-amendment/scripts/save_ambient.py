"""Archive unranked conventions, local instantiations and source ambiguities."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
aux=[]
def add(heading,body,pages,ids,note):
    aux.append(dict(local_id='A'+str(len(aux)+1),source_heading=heading,source_kind='source_passage',statement_original=body.strip(),evidence=[dict(page=p,location=heading) for p in pages],used_by_local_ids=ids,resolution_note=note))
add('Section 1.1 — probability measures and expectation',r'''
For a measurable space $(\mathbb X,\mathcal X)$, we denote by $\mathcal P(\mathbb X)$ the set of all probability measures supported on $\mathbb X$. For a probability measure $\mathrm P\in\mathcal P(\mathbb X)$ and a function $g$ on $\mathbb X$, we write $\mathrm Pg:=\int_{\mathbb X}g\,d\mathrm P$, i,e., $\mathrm Pg$ denotes the expectation of $g$ with respect to the measure $\mathrm P$.
''',[4],[],'P[Q(event)] in the theorem statements is the sampling expectation of a posterior mass; it is not an unqualified almost-sure convergence assertion.')
add('Section 3.1 — true model and contraction metric',r'''
Let $(\Lambda_n^\star)_{n\in\mathbb N}$ be a sequence of natural parameter spaces such that $\Lambda_n^\star\subset\Lambda_n$ for each $n\in\mathbb N$. Throughout this paper, we assume that the true distribution of the sample $\mathbf Y^{(n)}$ belongs to a true model $\mathcal P_n^\star:=\{\mathrm P_{\boldsymbol\lambda^\star}^{(n)}:\boldsymbol\lambda^\star\in\Lambda_n^\star\}$. Note that the true model does not need to be contained in the model $\bigcup_{m\in\mathcal M_n}\mathcal P_{n,m}$ used for estimation. Let $\mathcal d_n:\Lambda_n\times\Lambda_n\mapsto\mathbb R_{\geq0}$ be a metric that will be used to measure a degree of contraction.
''',[11],['D10','D11','D18','D22','D23','D46','D47'],'The true parameter need not lie in the fitted model union. The metric is supplied rather than synthesized from KL, and the true-class quantifier in the general results is uniform.')
add('Section 3.1 — estimation and approximation errors',r'''
We can interpret $\zeta_{n,m}>0$ and $\eta_{n,m}>0$ are estimation and approximation errors of the model $m\in\mathcal M_n$, respectively.
''',[11],['D10','D11','D12','D13','D14','D15','D17'],'Preserve the ordering: zeta is estimation error and eta approximation error. Reuse of the formula (3.5) in Assumption E does not impose the KL-based condition A2 there.')
add('Section 3.3 — posterior mass of model-index sets',r'''
We write $\widehat Q_n(\mathcal M'):=\widehat Q_n(\bigcup_{m\in\mathcal M'}\Theta_{n,m})$ for any subset $\mathcal M'\subset\mathcal M_n$ for brevity.
''',[14],['D17','D18','D20','D34','D42'],'Model-set events denote unions of parameter cells. Theorem 5.1 uses the corresponding pair-index cells; the sparse-factor model selection result uses column dimension and row support.')
add('Section 4 — function class and function norms',r'''
Let $\mathcal F^d$ be the set of all measurable real-valued functions supported on $[0,1]^d$. For $f\in\mathcal F^d$ and $q\in\mathbb N$, let $\|f\|_q:=(\int_{[0,1]^d}|f(\mathbf x)|^q\,d\mathbf x)^{1/q}$ denote the usual $\mathcal L^q$ norm and $\|f\|_\infty:=\sup_{\mathbf x\in[0,1]^d}|f(\mathbf x)|$ the $\mathcal L^\infty$ norm.
''',[15],['D26','D27','D30','D31'],'The oracle expression in Theorem 4.1 uses the source supremum norm; the contraction event uses the empirical design-point distance. No Holder or composition class is imposed on its arbitrary F-star.')
add('Section 4.1 — instantiated neural-network posterior',r'''
Since the parameter spaces $\{\Theta^{\leq B_n}_{(K,M)}\}_{(K,M)\in\mathcal M_n}$ are disjoint, by Theorem 2.1, the adaptive variational posterior is given by $\widehat Q_n=\sum_{(K,M)\in\mathcal M_n}\widehat\gamma_{n,(K,M)}\widehat Q_{n,(K,M)}$ with $\widehat Q_{n,(K,M)}\in\operatorname*{argmin}_{Q\in\mathcal Q_{n,(K,M)}}\mathcal E_n(Q,\Pi_{n,(K,M)},\mathrm p_n)$ and $\widehat\gamma_{n,(K,M)}\propto\alpha_{n,(K,M)}\exp(-\mathcal E_n(\widehat Q_{n,(K,M)},\Pi_{n,(K,M)},\mathrm p_n))$.
''',[16],['D7','D28','D29'],'Theorem 4.1 invokes the general adaptive variational posterior with these specific model/prior/family inputs and the Gaussian regression likelihood. The global KL-projection definition (2.7) is the primary construction in the dependency graph; this equivalent local-optimizer representation is preserved here.')
add('Section 5.2.1 — sparse-factor optimizer and appendix reference',r'''
The computation of each individual variational posterior $\widehat Q_{n,m}\in\operatorname*{argmin}_{Q\in\mathcal Q_{n,m}}\mathcal E_n(Q,\Pi_{n,m},\mathrm p_n)$ can be efficiently done by the optimization algorithm developed by Ning [2021], which, for the sake of completeness, are provided in Appendix E.1 in the Supplementary Material.
''',[21],['D7','D35','D36'],'The model, prior and variational family are specified in the main text. The referenced computational algorithm is outside scope and is not expanded or counted as a statement requirement.')
add('Section 2.1 — disjoint parameter spaces and natural images',r'''
Furthermore, the natural parametrization map can mitigate any restriction of the disjointness assumption. One may construct a collection of disjoint parameter spaces, which possibly yields non-disjoint natural parameter spaces such that $\{\mathrm T(\boldsymbol\theta):\boldsymbol\theta\in\Theta_{n,m'}\}\cap\{\mathrm T(\boldsymbol\theta):\boldsymbol\theta\in\Theta_{n,m}\}\neq\varnothing$ for some $m\neq m'$.
''',[5],['D3'],'Disjointness is imposed on the parameter spaces, not on the image distributions; no identifiability or injectivity of T is added.')

issues=[]
def issue(ids,pages,where,text):issues.append(dict(local_ids=ids,evidence=[dict(page=p,location=where) for p in pages],text=text))
issue(['D29'],[16],'Equation (4.4)','The source prints Unif(-psi_1,j,psi_2,j) with -B_n<=psi_1,j<psi_2,j<=B_n. Those constraints do not by themselves ensure that the printed interval endpoints are ordered. The sign is preserved rather than silently repaired.')
issue(['D45'],[25],'Equation (7.2)','The objective names Pi_n,m as an argument while its displayed KL term uses Pi_n. Both source symbols remain; no inference about an intended correction is incorporated into the original statement.')
issue(['D46','D47','D48'],[25,26],'Assumption E header and Theorem 7.1','Assumption E is scoped to lambda-star in Lambda_n-star, but Theorem 7.1 states its first inequality for lambda-star in Lambda_n. This quantifier mismatch is retained and not resolved by extending the assumption.')
issue(['D1','D41'],[4,22],'KL convention and equation (6.1)','KL is extended-real and the ivB definition subtracts KL quantities. The paper does not supply conventions for every infinity-minus-infinity case or establish existence of each extremum within the definition; no extra finiteness assumption is inserted.')
issue(['D3','D4','D6'],[4,5,7],'Countable model indices and probability simplex','The model index set is introduced as countable, whereas Delta_d is defined for finite d. Infinite-dimensional simplex and mixture convergence conventions are not explicitly specified. The source notation is preserved; conditions such as B1 later force finiteness where assumed.')
issue(['D5','D7','D9','D21','D44','D45'],[7,8,19,24,25],'Posterior normalizers, conditional priors and argmins','The displayed formulas do not separately cover zero/infinite marginal likelihoods, zero-mass conditioning cells, unattained argmins, or measurable selection of nonunique optimizers. These remain source conventions, not newly added hypotheses.')
issue(['D27'],[16,17],'Network architecture and magnitude bounds','The prose calls K the number of hidden layers, although its explicit composition has K affine maps and K-1 intervening activations. It also describes B_n as diverging, whereas Theorem 4.1 explicitly permits 1<=B_n up to a polynomial bound. Both original formulations are retained without strengthening the theorem.')
issue(['D37','D38','D39'],[21,22],'True loading dimension and covariance subclasses','The basic truth class bounds support from above and does not impose full loading rank or exactly s_n active rows. The signal-restricted class later imposes a positive r_n-th signal eigenvalue and active-row lower bound. The prose calls r_n and s_n true dimensionality/sparsity; no unprinted equality constraints are added.')
issue(['D43'],[23],'Equation (6.4)','The source writes a maximum over the ivB sieve but does not specify an empty-sieve or nonattainment convention. The bound uses the same A_n sequence as the theorem. No ideal-penalty assumption is appended.')
issue(['D46'],[25],'Equations (7.6)-(7.7)','The quasi-likelihood is only declared nonnegative, but the moment conditions contain forward and inverse ratios. Undefined ratio conventions are not supplied. The actual sampling law remains the original experiment, not a normalized quasi-likelihood law.')

data=dict(paper_id=ROOT.name,scope='Pinned arXiv:2109.03204v4 main document, PDF pages 1-29 only.',auxiliary_passages=aux,
 standard_ambient_resolution=[
  'All theorem statements remain the complete original statements in the independently reviewed inventory; references such as Assumption A or equation (3.1) are resolved in separate source records rather than inserted into quotations.',
  'Parent quantifier/constant scopes for A, B, D and E are preserved with each extracted subclause. Subclauses retain their printed source identity, even when the same natural-language title occurs in different assumptions.',
  'Theorems 3.3 and 7.1 have initial inequalities and later consequences under additional assumptions. Explanations explicitly restrict the extra assumptions to those consequences.',
  'Theorem 5.1 has a full-D contraction/no-underestimation clause and a weaker D2/D3 overestimation clause. A theorem-level union of dependencies does not assert that D1 is required for the final clause.',
  'Theorem 3.5 explicitly assumes n epsilon_n squared tends to infinity. The ivB theorems do not require B2, and Theorem 6.1 does not require A1. No such unprinted conditions are added.',
  'The general posterior definition is the KL projection (2.7). Equivalent negative-ELBO optimizer decompositions are retained where defined and in application context; a proof of equivalence is not introduced as a statement prerequisite.',
  'Theorem 4.1 binds its own oracle expression with sup over f followed by inf over network parameters. Its Gaussian model, uniform prior and product-uniform variational family are explicit application inputs. Generic A/B proofs do not become hypotheses of this application theorem.',
  'Theorem 5.2 binds its explicit contraction rate locally. Theorem 5.3 imports its source conditions plus a separate signal-restricted truth class, and concludes near-recovery within H1/H2 multiplicative constants rather than exact model selection.',
  'The ivB penalty is a sup-inf difference of KL quantities independent of the likelihood. Its threshold model set and maximal sieve complexity are different constructions. Ideal penalties are discussed after the theorem but are not assumed.',
  'The E2 approximation budget uses n times squared metric distance, whereas A2 and D2 use a sampling-distribution KL term. The one-index oracle formula is reused with the corresponding error inputs; no A2 dependency is imported into E.',
  'Standard auxiliary notation includes finite sets [m], positive-definite matrices, row and vector norms, product probability measures, Dirac masses, suprema/infima and asymptotic o/O/comparison notation. The paper defines o(a_n) as ratio tending to zero and allows absolute constants to vary from place to place.'
 ],unresolved_source_conventions=issues,excluded_proof_dependencies=[
  'Lemmas, propositions, corollaries and examples are outside the theorem inventory. In particular, Corollary 4.2 and its Holder-space/Assumption C specialization do not change Theorem 4.1.',
  'The Gaussian-mixture and stochastic-block illustrations do not instantiate any of these main-text Theorems as separate results. Main-text statements merely illustrating generic models are not ranked as additional demands.',
  'Theorem 5.3 imports assumptions of Theorem 5.2, not its proved covariance-contraction conclusion. Likewise, references to the main theorem in proof discussions do not generate statement links.',
  'Algorithm 1 is a computational summary, not an additional premise of Theorem 2.1. Supplementary optimization algorithms, approximation results, tests, change-of-measure arguments and all appendix theorems remain excluded.'
 ])
def main():
    (ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved eight auxiliary passages and ten unresolved source-convention records.')

if __name__ == '__main__':
    main()
