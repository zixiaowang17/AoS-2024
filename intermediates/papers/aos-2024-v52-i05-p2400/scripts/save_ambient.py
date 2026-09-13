"""Keep source conditions, proof context and unresolved source conventions separate."""
import json
from save_inventory import ROOT,PID

def main():
    aux=[]
    def add(n,s,pages,note,deps=()):aux.append(dict(local_id='A'+str(n),statement_original=s,evidence=[dict(page=p,location='Original main-text context A'+str(n)) for p in pages],scope_note=note,depends_on=list(deps)))
    add(1,r'''\[
y_i=f_0(x_i)+\epsilon_i,\qquad i=1,\ldots,n,
\]
(1)
where $f_0:\mathcal X\to\mathbb R$ is the (unknown) regression function to be estimated, and $\epsilon_i$, $i=1,\ldots,n$ are mean zero stochastic errors.''',[1],'Introductory regression model. Section5 strengthens the error law to independent normal noise with common variance; mere zero means are insufficient for the stated statistical theorems.',['D12'])
    add(2,r'''Here $\lambda\ge0$ denotes a tuning parameter, $y=(y_1,\ldots,y_n)\in\mathbb R^n$ is the response vector,''',[2],'Common squared-loss penalty convention. The generalized-lasso and KTF objectives use no 1/n scaling; retain the original lambda prescriptions.',['D9','D15'])
    add(3,r'''for deterministic sequences $a_n,b_n$ we write $a_n=O(b_n)$ when $a_n/b_n$ is upper bounded for large enough $n$, we write $a_n=\Omega(b_n)$ when $a_n^{-1}=O(b_n^{-1})$, and $a_n\asymp b_n$ when both $a_n=O(b_n)$ and $a_n=\Omega(b_n)$. For random sequences $A_n,B_n$, we write $A_n=O_{\mathbb P}(B_n)$ when $A_n/B_n$ is bounded in probability. In the theory that follows, all asymptotics are for $n\to\infty$ with $k,d$ fixed.''',[15],'Preserve the distinction between stochastic estimation-error bounds, deterministic lower bounds on expected minimax risk, and two-sided rates. Positive variance and fixed k,d are implicit in rate constants.',['D18'])
    add(4,r'''For a univariate function $g:[a,b]\to\mathbb R$, recall that its total variation is defined as
\[
\operatorname{TV}(g;[a,b])=\sup_{a<z_1<\cdots<z_{m+1}<b}\sum_{i=1}^m|g(z_i)-g(z_{i+1})|.
\]''',[1],'The introduction’s unrestricted pointwise variation is refined to essential variation in(19). Theorem1 explicitly uses the refinement, so this earlier convention is not substituted for D3.',['D3'])
    add(5,r'''\[
(\Delta\theta)(x_i)=\begin{cases}\theta(x_{i+1})-\theta(x_i)&\text{if }i\le n-1,\\0&\text{else.}\end{cases}
\]
Naturally, we can view $\Delta\theta$ as a vector in $\mathbb R^n$ with components $(\Delta\theta)(x_i)$, $i=1,\ldots,n$. Higher-order discrete derivatives are obtained by repeated application of the same formula; we abbreviate $(\Delta^2\theta)(x_i)=(\Delta(\Delta\theta))(x_i)$, and so on.
\[
(\Delta_{x_j}\theta)(x)=\begin{cases}\theta(x+e_j/N)-\theta(x)&\text{if }x,x+e_j/N\in Z_{n,d},\\0&\text{else.}\end{cases}
\]
\[
\underset{\theta\in\mathbb R^n}{\operatorname{minimize}}\quad\frac12\sum_{i=1}^n\big(y_i-\theta(x_i)\big)^2+\lambda\sum_{j=1}^d\sum_{x\in Z_{n,d}}|(\Delta_{x_j^{k+1}}\theta)(x)|.
\]
(6)''',[3],'Literal fixed-length zero-boundary difference and claimed alternative KTF formulation. For k≥1, repeated application introduces extra near-boundary terms not in the shrinking-row matrix(4). Preserve this source discrepancy; statistical theorems explicitly use matrix formulation(7).',['D5','D6','D7','D9'])
    add(6,r'''if $f\in W^{1,1}(U)$, that is, $f$ is in $L^1(U)$ and it is weakly differentiable and its weak derivative $\nabla f$ is also in $L^1(U)$, then
\[
\operatorname{TV}(f;U)=\int_U\|\nabla f(x)\|_1\,dx.
\]
(18)''',[12],'Smooth/Sobolev special-case formula explains anisotropy. Theorem1 is for all BV functions and does not assume weak differentiability.',['D1','D2'])
    add(7,r'''Now we recall the traditional definition for the $k$th order Holder class of functions from $[0,1]^d$ to $\mathbb R$, of radius $L>0$:
\[
\mathcal C^k(L;[0,1]^d)=\left\{f:[0,1]^d\to\mathbb R:f\text{ is }k\text{ times differentiable and for all integers }\alpha_1,\ldots,\alpha_d\ge0,\text{ with }\alpha_1+\cdots+\alpha_d=k,\left|\frac{\partial^kf(x)}{\partial x_1^{\alpha_1}\cdots\partial x_d^{\alpha_d}}-\frac{\partial^kf(z)}{\partial x_1^{\alpha_1}\cdots\partial x_d^{\alpha_d}}\right|\le L\|x-z\|_2,\text{ for all }x,z\in[0,1]^d\right\}.
\]''',[14],'Continuum Holder class with Lipschitz kth mixed derivatives. The source names it kth order; do not silently rename it an order-k seminorm or import absolute bounds on lower derivatives. It is lower-bound proof context, not the parameter class assumed by Theorem6.')
    add(8,r'''We define a discretized version of this class by simply evaluating the functions in $\mathcal C^k(L;[0,1]^d)$ on the lattice $Z_{n,d}$:
\[
\mathcal C_{n,d}^k(L)=\{\theta\in\mathbb R^n:\text{there exists some }f\in\mathcal C^k(L;[0,1]^d)\text{ such that }\theta(x)=f(x),x\in Z_{n,d}\}.
\]
(25)''',[14],'Discretized Holder class used in the proof-related embedding. Preserve it separately without adding an implication-only edge from the Sobolev or KTV class to this subset.',['D5'])
    add(9,r'''The discrete classes in (23)–(25) satisfy, for any $L>0$,
\[
\mathcal C_{n,d}^k(L)\subseteq\mathcal W_{n,d}^{k+1}\big(c_1Ln^{\frac12-\frac{k+1}d}\big)\subseteq\mathcal T_{n,d}^k\big(c_2Ln^{1-\frac{k+1}d}\big),
\]
(26)
where $c_1,c_2>0$ are constants depending only on $k,d$.''',[14],'Proposition3, credited to Sadhanala et al.(2017). Theorem6’s lower-bound justification refers to this embedding, but does not assume its signal lies in the smaller Holder class. This is proof context, not a seventh Theorem.',['D10','D11'])
    add(10,r'''By the inequality $\|v\|_2\le\sqrt p\|\theta\|_1$ for vectors $v\in\mathbb R^p$, and the fact that the number of rows of $D_{n,d}^{(k+1)}$ can be upper bounded by $dn$, we have the following embedding:
\[
\mathcal W_{n,d}^{k+1}(\rho)\subseteq\mathcal T_{n,d}^k(\sqrt{dn}\rho),\qquad\text{for any }\rho>0.
\]''',[14],'The printed vector-norm inequality has mismatched v/theta and does not justify the displayed embedding; the needed inequality is ||v||_1≤sqrt(p)||v||_2. Preserve the original passage and flag it separately. No dependency edge follows from class inclusion alone.',['D10','D11'])
    add(11,r'''The null space of the KTF penalty matrix in (8) has dimension $(k+1)^d$. Furthermore, it is spanned by a polynomial basis made up of elements
\[
p(x)=x_1^{a_1}x_2^{a_2}\cdots x_d^{a_d},\qquad x\in Z_{n,d},
\]
for all $a_1,\ldots,a_d\in\{0,\ldots,k\}$.''',[9],'Proposition1 identifies the max-degree polynomial null space used for Theorem5’s polynomial projection. Retain the statement as context; its appendix proof is excluded.',['D5','D7','D20'])
    issues=[]
    def issue(i,pages,note):issues.append(dict(issue_id=i,evidence=[dict(page=p,location='Source scope or notation issue') for p in pages],note=note))
    issue('anisotropic-essential-variation',[11,12,13],'Theorem1 uses the infinity-norm test-field constraint in(17) and essential variation(19), not isotropic TV or pointwise unrestricted variation. Approximate continuity is only described and externally cited; the formal definition is unresolved locally. BV representatives and exceptional slices are understood modulo Lebesgue-null sets.')
    issue('slice-endpoints-and-dimension',[12,13],'Theorem1 takes open bounded convex U but writes closed endpoint intervals for fibers. The essential-variation supremum uses strict interior points, so no endpoint value is selected by it. For d=1 the projected space is R^0 with its usual singleton measure convention, implicit in the source; no special case is printed.')
    issue('difference-boundary-discrepancy',[2,3,4],'The fixed-length Delta operator sets the final entry to zero and is then iterated literally. For order2 its penultimate entry is minus the last first difference, whereas the shrinking-row matrix D^(2) omits that boundary term. The source calls(6) and(7) equivalent; retain the discrepancy and pin theorem definitions to the explicitly referenced matrix formulation(7).')
    issue('lattice-order-and-seminorm-domains',[1,2,4,9,13,14],'N=n^(1/d) must be integral and sufficiently large relative to k+1 for the displayed difference matrices. KTV and discrete Sobolev balls constrain seminorms, leaving the max-degree polynomial null space unbounded. The 1/n risk terms represent finite-dimensional components and must be retained.')
    issue('generalized-lasso-incoherence',[15,16],'Theorem2 bounds left singular vectors in R^r by mu/sqrt(n), exactly as printed, with an arbitrary exceptional set I. Its rate constants hide fixed noise scale. Theorem3 uses Theorem2 in its proof; this is not a new explicit incoherence premise on the KTF signal or an import of generic D into its statement.')
    issue('risk-versus-probability-bounds',[15,16,18],'Theorems2–3 state OP bounds on squared estimation error, whereas Theorems4–6 concern expected minimax risk. A pointwise in-probability bound alone does not certify a uniform expectation-risk upper bound. Preserve the paper’s stated attainment conclusions without claiming an independent proof of those transitions.')
    issue('radii-and-truncation-orders',[13,14,18],'The classes are defined for positive radii. Theorem5’s expression C_n^2*log(1+n/C_n^2)/n needs a limiting convention at zero, and its tau scaling can fall below1 for sufficiently small radii. Q must be an integer-index subset of [N]^d, retain the polynomial null space, and have feasible truncation; rounding/clipping conventions are implicit rather than printed.')
    issue('canonical-rate-floor',[14,18],'Theorem6 first includes 1/n, then reports the canonical rate L_n^(2/(2s+1))*n^(−2s/(2s+1)) without that term or an explicit lower restriction on L_n. This simplification requires the displayed nonparametric term to dominate 1/n; for very small L_n, retain the earlier full rate. Do not repair its final original sentence.')
    issue('critical-logarithm-and-linear-rates',[18],'In Theorem5 the critical term is (C_n^2/n)*log(1+n/C_n^2), with multiplication by the logarithm. It is not division by a logarithm. Preserve the three regimes, the explicit log-factor attainment qualification, and the additional C_n^2=O(n^alpha), alpha<1, statement.')
    issue('singular-basis-and-polynomial-space',[9,17,18],'The projection uses right singular vectors indexed coordinatewise by [N]^d, including zero modes, rather than Theorem2’s left singular vectors. The tensor-product basis and choices in repeated eigenspaces are implicit. Max degree k means each coordinate exponent≤k, not total degree≤k.')
    issue('holder-embedding-norm-typo',[14],'The explanatory inequality before the discrete Sobolev-to-KTV embedding prints ||v||_2≤sqrt(p)||theta||_1. The embedding requires the other one-to-two norm inequality with a consistent vector. Preserve this typo separately from the correct class definitions and Proposition3’s printed inclusion.')
    issue('proof-context-not-assumptions',[14,16,18],'Theorem6’s complete italic statement mentions Holder embedding as the reason for its lower bound. Preserve the original Holder classes and Proposition3 as unranked proof context. Neither that inclusion nor Theorem3’s application of Theorem2 creates a theorem-statement dependency on a smaller parameter class or additional assumption.')
    bindings={
      'T1':dict(domain='Open bounded convex U; f in BV(U). No data model, lattice or weak differentiability premise.',objects=['D1','D2','D3','D4'],external_reference='Approximate continuity: Evans and Gariepy(2015), Section1.7.2; paper supplies description only.'),
      'T2':dict(domain='General fixed matrix D in R^(r×n), Gaussian experiment(29). No KTF or lattice restriction.',objects=['D12','D15','D16','D17'],parameters='Rank q; sorted nonzero singular values; selected left singular vectors; exceptional I⊆[q]; mu≥1. Tuning and all three error terms retained.'),
      'T3':dict(domain='Lattice KTF(7), Gaussian experiment, k,d fixed; C_n=||D theta_0||_1>0.',objects=['D8','D9','D12','D18'],regimes=['s<1/2: sqrt(log n)','s=1/2: log n','s>1/2: (log n)^(1/(2s+1))*(n/C_n)^((2s−1)/(2s+1))'],conclusion='OP(1/n+lambda*C_n/n), not a standalone uniform expectation assertion.'),
      'T4':dict(domain='KTV ball with positive radius C_n≤n; Gaussian minimax experiment.',objects=['D10','D13','D18'],conclusion='Omega(1/n+C_n/n+(C_n/n)^(2/(2s+1))). No canonical radius imposed.'),
      'T5':dict(domain='KTV ball with positive C_n≤sqrt(n); Gaussian minimax linear risk.',objects=['D10','D14','D18','D19','D20'],regimes=['s<1/2','s=1/2','s>1/2'],attainment='Full projection and polynomial-projection paragraphs retained, including the critical log-factor qualification and C_n^2=O(n^alpha), alpha<1.'),
      'T6':dict(domain='Discrete coordinatewise Sobolev ball, positive B_n≤sqrt(n), Gaussian minimax experiment.',objects=['D11','D13','D18','D19','D21'],conclusion='Two-sided 1/n+(B_n^2/n)^(1/(2s+1)), with specified spectral truncation and final canonical specialization.',proof_context=['A7','A8','A9'],qualification='Canonical simplification omits the 1/n floor when L_n is very small; retained as source issue.')}
    refs=[dict(claim_id=PID+'/T1',reference='(17),(19)',reference_kind='definition_reference',resolution='D1–D4 preserve anisotropic BV and coordinate-fiber essential variation.'),dict(claim_id=PID+'/T1',reference='Approximate continuity, Evans and Gariepy(2015), Section1.7.2',reference_kind='external_definition_reference',resolution='D3 preserves the source description and citation; no external definition fetched.'),dict(claim_id=PID+'/T3',reference='(7) and (29)',reference_kind='definition_reference',resolution='Matrix KTF and Gaussian experiment, D7,D9,D12; the proof’s general-lasso invocation is not an additional assumption.'),dict(claim_id=PID+'/T3',reference='application of Theorem2',reference_kind='proof_only',resolution='Recorded in prose on page16. No D15/D16/D17 graph edges added to T3.'),dict(claim_id=PID+'/T5',reference='(23),(34) and max degree',reference_kind='definition_reference',resolution='KTV ball D10, spectral projection D19 and max-degree convention D20.'),dict(claim_id=PID+'/T6',reference='(24),(27),(34)',reference_kind='definition_reference',resolution='Sobolev ball D11, canonical radius D21 and projection D19.'),dict(claim_id=PID+'/T6',reference='Holder embedding in(26) and Sadhanala et al.(2017) lower bound',reference_kind='proof_only',resolution='Original theorem sentence retained; A7–A9 preserve the supporting class definitions and inclusion, without assuming the target belongs to that subset.'),dict(claim_id=PID+'/T5',reference='Proposition1 polynomial null space',reference_kind='definition_reference',resolution='D20 and A11 preserve the exact max-degree space used in the polynomial projection.')]
    data=dict(paper_id=PID,unranked_auxiliary_passages=aux,source_issues=issues,statement_local_bindings=bindings,source_claim_references=refs,ambient_conventions=['Finite-dimensional Euclidean norms, identity and Kronecker matrices, singular values, ordinary expectation and coordinate derivatives are ambient mathematics; no library availability is decided.','An integer a≥1 has [a]={1,...,a}; source matrix and spectral indices use this convention. Fixed k,d and positive-radius domains are preserved without silently extending all expressions to zero.','Unranked proof passages retain source wording and evidence. Class inclusions alone do not create definition dependencies.'])
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
