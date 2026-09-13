"""Save source conventions, source issues and excluded references separately."""
import json
from pathlib import Path
from save_inventory import PID
ROOT=Path(__file__).resolve().parents[1]
aux=[]

def add(lid,text,pages,location):
    aux.append(dict(local_id=lid,statement_original=text.strip(),evidence=[dict(page=p,location=location) for p in pages]))

add('A1',r'''
The batching CI is given by
\[
CI_B:=\left(\frac1K\sum_i\psi(\widehat P_i)\pm t_{K-1,\alpha/2}\frac{S_{batch}}{\sqrt K}\right)
\]
''',[4],'Section 3 — batching confidence interval')
add('A2',r'''
The sectioning CI is given by
\[
CI_S:=\left(\psi(\widehat P)\pm t_{K-1,\alpha/2}\frac{S_{sec}}{\sqrt K}\right)
\]
''',[4],'Section 3 — sectioning confidence interval')
add('A3',r'''
The SB CI is
\[
CI_{SB}:=\left(\psi(\widehat P)\pm t_{K-1,\alpha/2}\frac{S_{batch}}{\sqrt K}\right).
\]
SB is a modified sectioning [Nakayama, 2014] that is viewed as a middle ground between batching and sectioning. It uses the same variance estimator $S_{batch}^2$ as batching, but the same interval center $\psi(\widehat P)$ as sectioning.
''',[4],'Section 3 — sectioning-batching confidence interval')
add('A4',r'''
The SJ CI is given by
\[
CI_{SJ}:=\left(\bar J\pm t_{K-1,\alpha/2}\frac{S_{SJ}}{\sqrt K}\right)
\]
where $S_{SJ}^2=\frac1{K-1}\sum_{i=1}^K(J_i-\bar J)^2$.
''',[4],'Section 3 — sectioned jackknife confidence interval and variance')
add('A5',r'''
The four CIs we have introduced above are two-sided and symmetric in the sense that each of the CI has a midpoint at the respective point estimate.
''',[5],'Section 3 — meaning of symmetric confidence interval')
add('A6',r'''
Note that $-t_{K-1,\alpha/2}\le W_B\le t_{K-1,\alpha/2}\Leftrightarrow\psi\in CI_B$ and similar arguments hold for sectioning, SJ and SB and for one-sided CIs. Therefore, to study the higher-order coverage errors, it suffices to study the distributions of $W_B,W_S,W_{SB}$ and $W_{SJ}$, and how much they deviate from $t_{K-1}$.
''',[5],'Section 3 — confidence coverage as a statistic event')
add('A7',r'''
For batching (only), we can use an alternative algorithm that leverages Theorem 1. This algorithm, which is detailed in Appendix C, works regardless of the value of $K$. When $K\ge5$, both this algorithm and Algorithm 1 would give unbiased estimators for the coefficient of $n^{-1}$ error term, but Algorithm 1 would have a smaller variance due to the conditioning argument in its construction.
''',[14],'Section 6 — Algorithm 1 batch-count context and excluded alternative')
add('A8',r'''
In what follows, we illustrate how to compute the polynomials $a,b_1,b_2,d,e,E_2,b_1',d'$ as required by Steps 2 and 3 of Algorithm 1 using sectioning as an example. The computation for other schemes can be found in Section B.
''',[12],'Section 6 — coefficient naming and appendix-only formulas')
add('A9',r'''
In Theorem 3, we didn't make a claim that the coverage error of a symmetric CI is of order $O(n^{-1})$ since the expansion in Jensen [1989] doesn't discuss the oddness and evenness of the polynomials in the Edgeworth expansion.
''',[9],'After Theorem 3 — scope of the symmetric-coverage conclusion')

resolution={
'shared':'The baseline has N=nK iid observations. D1 contains the empirical operations without imposing independence; D2 adds the iid law only where appropriate. D3 names psi(P) and the baseline fixed-K limit. The four statistics D7-D10 are evaluated with the functional and empirical-law substitutions required by each section. Bar J is the arithmetic mean of the K pseudovalues, and unbounded sums over batch indices have range 1,...,K. The source does not specify behavior on a zero sample denominator. A1-A6 retain the CIs and event correspondence as auxiliary context; they are not additional theorem assumptions. Standard probability, expectations, covariance, vector norms, Gaussian CDF/density, cumulants, asymptotic O/o/O_p notation, derivatives and empirical measures are ambient.',
'1':'D16 is the complete uniform scalar Edgeworth and parity assumption for the batch estimate, with original target D3 and empirical batch D1 under the iid law D2. W_B is D7, which uses sample variance D4. The reference law is D11. The expansion order r and K are fixed in this regime; at least two batches are necessary for the displayed sample variance and Student degrees of freedom. The theorem does not require the sufficient smooth-function assumptions in Theorem 2.',
'2':'The original model is D12, with iid law D2, Cramer condition D13, moment/covariance clause D14 and derivative clause D15. The K>=r+3 first conclusion and K>=4 symmetric conclusion retain their own scope. The final replacement sentence covers all four statistic formulas and the Student law. There is no assertion of a common coefficient shared across methods.',
'3':'D17 and D18 provide the transformed scalar objective and retained batches separated by n^delta gaps. D19 and D20 supply the named mixing and recurrence definitions. The recurrent atom, return time tau, absolute reward sum G, uniform Cramer condition, cycle moments, r derivatives of f and coefficient variables are bound inside the theorem. A recurrent atom has the usual Markov-kernel meaning, but the paper supplies no formal definition. The printed n->0 and vector expression iuX_1 are retained as source issues. All four statistic formulas use the gapped empirical substitution, with no iid raw-data edge. A9 confirms that no symmetric O(n^-1) conclusion is stated here.',
'4':'The same gap construction, transformed objective, mixing and Harris definitions apply. D21 preserves the full in-theorem split-process construction, including both branches, initial law, Q, tau, tilde g, Sigma_g,n and G. Conditions (i)-(iv) distinguish the phi_C initial law from P and their r+3 versus r+1 moments. The statistic formulas use the gapped empirical data, not observations of the artificial split variable b itself. The source does not restate an f differentiability condition here; the Section 5 discussion invokes regularity of the smooth-function model, but no unstated precise order is inserted into the original theorem.',
'5':'D22 defines recurrent return times and cycle rewards. D23 defines the cycle-pair observations, ratio of expectations and substitution into all four statistics. The Cramer condition, r+2 moments, nonsingular covariance and positive expected cycle length are bound inside this theorem. The denominator condition supports a smooth ratio near the true mean. The inherited stationary setting does not turn these cycle batches into the fixed-time gapped construction. Regenerative independence and the treatment of the first incomplete cycle follow the stated cycle construction; the original theorem is not strengthened by fabricated conditions.',
'6':'Theorem 2 is inherited at r=2: fourth moments, nonsingular covariance, third derivatives, nonzero gradient and the vector Cramer condition, together with the K>=5 expansion regime corroborated by A7. D24 defines the coefficient c. D28 and D26 jointly preserve the entire original Algorithm 1, while D25 gives the full expressions in (7) and D27 the available sectioning coefficients. Original-data cumulants and covariance are inputs; X_i is then reused for fresh Gaussian simulation. Derivatives are evaluated at the original mean m=EX_1 and f_0 denotes the true f(m), as contextual interpretations, not changes to quotations. I_C is the indicator of the displayed region; the vector A is assembled from A_0,B_1,...,B_(K-1). The missing appendix formulas, unexplained c and other inconsistencies remain unresolved, so no executable estimator or proof of unbiasedness is claimed by this census.',
'7':'The iid Section 3 construction and target are reused, but n is fixed and K tends to infinity. The theorem assumes nonzero batch bias, finite batch variance and a positive finite influence-function variance, together with continuous Gateaux differentiability; D29 only names the influence function. No topology or stronger differentiability condition is supplied. The theorem gives limits for W_B,W_S,W_SJ only, not W_SB. Each sectioning Gaussian-CDF argument has division by sigma outside the square root, as verified in a high-resolution source crop. No Student-law limit is imported through the statistic definitions in this different asymptotic regime.'}
issues=[
'The pinned source is arXiv:2111.06859v1 dated 12 November 2021, 46 pages. Precise versioned URL and hash are retained; the register filename and unversioned export URL are aliases for the same bytes.',
'Seven original Theorems occur in main text. Theorem 2 continues on page 8 and Theorem 4 on page 11. Main text and references end above Appendix A on page 22; no appendix body is admitted.',
'The baseline consists of iid raw observations. Theorems 3-4 instead use retained stationary observations with gaps; Theorem 5 uses cycle reward-duration pairs. Reuse of the statistic formulas does not import iid raw observations into those settings.',
'The source defines the target as psi=psi(P), then prints psi_0 in W_SJ. The original target alias is preserved and explained rather than replaced in the formula.',
'The sample variance for batching centers at the average batch estimate; sectioning centers at the full empirical estimate. Their denominators and the SB hybrid are not interchangeable.',
'The sample variance formulas require K>1 and may vanish on finite samples. The source gives no totalized statistic value on a zero denominator; no convention is fabricated.',
'Theorem 1 assumes a uniform scalar Edgeworth expansion with alternating parity. The p_j here are not automatically the same objects as the density-weighted p_1,p_2 later defined for Algorithm 1.',
'Theorem 2 has separate K>=r+3 and K>=4 conclusions. The source comment about potentially relaxing K with a Peano remainder is not inserted into the original theorem.',
'Definition 1 uses sigma instead of alpha in its final alpha(n) expression. The two-field mixing formula is otherwise explicit. Both printed symbols are retained.',
'Definition 2 says there exists a measure mu, without nonzero or sigma-finite qualifications. These normally relevant requirements are not silently added to the quotation.',
'Theorem 3 prints the mixing limit as n->0, despite the surrounding large-batch-size setting. It is retained as printed.',
'Theorem 3 uses r derivatives of f whereas Theorem 2 uses r+1. Its uniform Cramer expression involves iuX_1 with vector u; the pairing convention and the role of g are not clarified by silently rewriting it.',
'Theorem 3 requires a recurrent atom but does not define one in the main text. It makes no symmetric-coverage O(n^-1) claim, as the following paragraph explicitly confirms.',
'Theorem 4 states only positive lambda while its split transition and residual kernel require probability-kernel constraints, including a meaningful inverse of 1-lambda. The binary-state range for delta is implicit, and delta is also used for the gap exponent.',
'Theorem 4 uses alpha for an initial distribution as well as alpha(n) for mixing, and P for both stationary law and transition kernel. The local roles are preserved and disambiguated in analysis.',
'Theorem 4 does not explicitly repeat a differentiability requirement on f. The general Section 5 regularity discussion is recorded without choosing and inserting an unstated derivative order into the theorem.',
'Theorem 4 uses G as a centered cycle sum, while Theorem 3 uses G as an absolute reward sum. The different definitions and starting laws in the moment conditions remain separate.',
'The regenerative construction starts at T_1 and excludes the initial incomplete cycle. Its target is a ratio of expectations, not an expectation of cycle ratios. No fixed calendar-time gap scheme is imposed on these pairs.',
'Theorem 6 inherits Theorem 2 with r=2 and targets the symmetric n^(-1) coefficient. Main-text discussion corroborates K>=5; the separate batching-only algorithm in Appendix C is excluded.',
'Algorithm 1 reuses X_i for freshly simulated Gaussian draws after taking original-law covariance and cumulants as inputs. This simulation step is not a Gaussian original-data assumption.',
'Equation (7) calls p_1,p_2 polynomials but includes the Gaussian density factor, and p_1 includes a leading 1. These exact source expressions are retained, not replaced by conventional Edgeworth density polynomials.',
'Algorithm 1 Step 3 divides a term in F_xx by an unexplained c. F_+ and F_- contain no division by the first gradient coordinate, although the stated hypotheses only require a nonzero gradient, not a normalized first coordinate.',
'Algorithm 1 Step 4 uses y_x, rather than y_x^(-), in the printed y_xx^(-) formula. It is not silently corrected.',
'Algorithm 1 Step 5 has no printed plus sign between the first bracketed term and the following parenthesis. It also uses p_1(x(A)) without specifying a scalar-versus-joint convention and has phi-prime only in the last negative-side term. All these expressions remain as printed.',
'The sectioning example alternates A_i and X_i and uses m and f_0 without a local definition. It prints b_2 as a contraction of the second-derivative tensor v with three vectors. No correction to w is inserted.',
'The sectioning prose names coefficients d,d-prime but its formulas and Algorithm 1 use lambda,lambda-prime. The inline factor 2 in the lambda-prime display is multiplication, not a superscript square; visual comparison resolved that typography.',
'Explicit Taylor coefficients for batching, SB and SJ are relegated to excluded Section B. The generic Taylor instructions in Algorithm 1 are preserved, but unavailable original formulas are not reconstructed and presented as quotations.',
'Theorem 7 fixes n and lets K grow, and gives no SB limit. Its spelling differantiable is retained. The source defines no full influence-function formula or tangent topology for its Gateaux assumption.',
'Theorem 7 places division by sigma outside the square root in both sectioning CDF arguments. A high-resolution crop confirms this; it is not a source error to be repaired.',
'This census checks original statements and their dependencies. It does not certify the paper proofs, the validity of every source formula or executable unbiasedness of the printed simulation algorithm.'
]
excluded=[dict(reference='Appendices A-E',location='Appendix A begins at y=202.908 on PDF page 22',status='excluded_not_opened',reason='Appendix bodies are outside the requested scope.'),dict(reference='Section B',location='Algorithm 1 and Section 6 main-text references',status='excluded_not_opened',reason='Explicit coefficients for the other batching schemes are unavailable in main text; generic Taylor instructions are retained without fabricated quotations.'),dict(reference='Appendix C',location='Section 6, PDF page 14',status='excluded_not_opened',reason='The alternative batching-only simulation algorithm is not Algorithm 1 and is outside scope.'),dict(reference='Appendices D-E',location='Theorem 1 proof and discussion before Theorem 2',status='excluded_not_opened',reason='Proof arguments do not expand the main-text theorem inventory.'),dict(reference='Jensen (1989), Malinovskii (1987), Hall (1992) and other cited results',location='Main-text expansion arguments',status='external_not_expanded',reason='Original local conditions are preserved; external definitions or proofs are not imported as new original assumptions.')]

def main():
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(dict(paper_id=PID,scope='main_text_only',auxiliary_source_passages=aux,statement_resolution=resolution,source_issues=issues,excluded_references=excluded),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(aux)} auxiliary passages and {len(issues)} source notes.')

if __name__=='__main__':main()
