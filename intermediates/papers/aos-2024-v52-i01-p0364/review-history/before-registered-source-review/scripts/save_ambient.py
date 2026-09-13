"""Preserve local notation, imported inline conditions and unresolved source issues."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
inv=json.loads((ROOT/'theorem-inventory.json').read_text());claims={c['claim_id'].split('/T')[-1]:c for c in inv['claims']}
aux=[]
def add(aid,body,pages,location,role):
 aux.append(dict(auxiliary_id=aid,statement_original=body.strip(),evidence=[dict(page=p,location=location) for p in pages],resolution=role))
add('A1',r'''
In this paper, we use $a\asymp b$ to denote $a=O(b)$ and $b=O(a)$ (also $a\asymp_P b$ for $a=O_P(b)$ and $b=O_P(a)$), while $a\succeq b$ is equivalent to $b=O(a)$, and $a\succ b$ is equivalent to $b=o(a)$. We also use $\|\cdot\|$ to denote the $L_2$ norm (of a vector or a matrix), and $\|\cdot\|_F$ to denote the Frobenius norm, while $\|\cdot\|_{max}$ represents the maximum element (of a vector or a matrix). We also use $\|A\|_\infty=\max_i\sum_j|a_{ij}|$ and $\|A\|_1=\max_j\sum_i|a_{ij}|$ to denote the $L_\infty$ and $L_1$ norm of a matrix $A$ respectively. The notation $\operatorname{vec}(\cdot)$ represents the vectorization of a matrix, stacking columns of the matrix from left to right. We also use $\mathbf1_m$ to represent a vector of ones with length $m$, whereas $\mathbf I_m$ is the identity matrix with size $m$. The notation $\operatorname{diag}(A)$ of a square matrix $A$ is the diagonal matrix with only the diagonal elements of $A$ remain, and everything else set to 0. This notation is also used to represent a block diagonal matrix. For instance, $\operatorname{diag}(A_1,\ldots,A_n)$ is the block diagonal matrix with diagonal block matrices $A_1,\ldots,A_n$. For a positive integer $m$, we define $[m]:=\{1,\ldots,m\}$.

Please refer to the Appendix in Section 7 for some basic tensor manipulations related to this paper.
''',[4],'Section 2 — Notations','Unranked ambient notation used throughout the statements. The matrix L2 norm is interpreted as spectral norm, with the source description preserved; no appendix convention was inspected.')
add('A2',r'''
The basic idea is, in estimating the mode-$k$ factor loading matrix $\mathbf A_k$, we can write the tensor factor model (3.1) as
\[
\mathcal X_t=\boldsymbol\mu+\mathcal F_{t,-k}\times_k\mathbf A_k+\mathcal E_t,
\]
where $\mathcal F_{t,-k}=\mathcal F_t\times_1\mathbf A_1\times_2\cdots\times_{k-1}\mathbf A_{k-1}\times_{k+1}\mathbf A_{k+1}\times_{k+2}\cdots\times_K\mathbf A_K$, and we have
\[
\operatorname{mat}_k(\mathcal X_t)=\operatorname{mat}_k(\boldsymbol\mu)+\mathbf A_k\operatorname{mat}_k(\mathcal F_{t,-k})+\operatorname{mat}_k(\mathcal E_t),\tag{3.2}
\]
where $\operatorname{mat}_k(\cdot)$ is the mode-$k$ unfolding matrix of a tensor. Let $\mathbf x_{t,-k,i}$, $i\in[d_{-k}]$ be the $i$-th mode-$k$ fiber of $\mathcal X_t$. In other words, $\mathbf x_{t,-k,i}$ is the $i$-th column vector of $\operatorname{mat}_k(\mathcal X_t)$. Then we have,
\[
\mathbf x_{t,-k,i}=\boldsymbol\mu_{-k,i}+\mathbf A_k\mathbf f_{t,-k,i}+\mathbf e_{t,-k,i},\quad i\in[d_{-k}],\tag{3.3}
\]
where the $\mathbf f_{t,-k,i}$'s, $\mathbf e_{t,-k,i}$'s and $\boldsymbol\mu_{-k,i}$'s are the mode-$k$ fibers of $\mathcal F_{t,-k}$, $\mathcal E_t$ and $\boldsymbol\mu$ respectively.
''',[5],'Section 3 — main-text unfolding and fiber conventions','Local model expansion consumed by full and sampled fiber sums and projected data. It provides the meaning of d_-k as the fiber count, without importing the appendix indexing map.')
add('A3',r'''
where $\mathbf D_k=\operatorname{diag}(\mathbf A_k^\top\mathbf A_k)$ is a diagonal matrix consisting of the diagonal elements of $\mathbf A_k^\top\mathbf A_k$, and $\boldsymbol\Sigma_{A,k}$ is positive definite with all eigenvalues bounded away from 0 and infinity. Let $(\mathbf D_k)_j$ be the $j$-th diagonal element of $\mathbf D_k$, then we assume $(\mathbf D_k)_j\asymp d_k^{\alpha_{k,j}}$ for $j\in[r_k]$, and $0<\alpha_{k,r_k}\leq\cdots\leq\alpha_{k,2}\leq\alpha_{k,1}\leq1$.

For each $k\in[K]$, let $s_k=\sum_{j=1}^{r_k}\left(\sum_{i=1}^{d_k}(\mathbf A_k)_{ij}\right)^2\asymp\sum_{j=1}^{r_k}d_k^{2\kappa_{k,j}}$, and $s_{-k}:=\prod_{l=1;l\ne k}^K s_l$.
''',[8],'Assumptions L1 and L2 — defining notation excerpts','Original excerpts for D_k, alpha exponents and column-sum scales. Using the scalar definition of s to form normalized data does not impose L2 inequality (3.7). Theorem 8 uses the paper factor-strength notation without explicitly importing every L1 restriction; that scope issue is separately recorded.')
add('A4',r'''
From Theorem 4, setting $z_k=1$ there, we obtain $\widehat{\mathbf q}_{k,pre}:=\widehat{\mathbf Q}_{k,pre,(1)}=\widehat{\mathbf U}_{k,pre,(1)}\mathbf P_{k,pre,(1)}=\pm\widehat{\mathbf U}_{k,pre,(1)}$ (WLOG we take the plus sign in the presentations hereafter), with an error rate
\[
\|\widehat{\mathbf q}_{k,pre}-\mathbf U_{k,(1)}\|=O_P\left(\sqrt{\frac{r_k}T}+d_k^{-\alpha_{k,1}}c_{k,max}^{1/2}\right).\tag{4.2}
\]

For each $k\in[K]$, we create the projected data $\mathbf y_t^{(k)}$ as in (4.1), using
\[
\mathbf q_{-k}=\widehat{\mathbf q}_{-k,pre}:=\widehat{\mathbf q}_{K,pre}\otimes\cdots\otimes\widehat{\mathbf q}_{k+1,pre}\otimes\widehat{\mathbf q}_{k-1,pre}\otimes\cdots\otimes\widehat{\mathbf q}_{1,pre}.\tag{4.3}
\]
Then we define $\check{\mathbf q}_k^{(1)}$ to be the eigenvector corresponding to the largest eigenvalue of the matrix
\[
\widetilde{\boldsymbol\Sigma}_y^{(k)}:=T^{-1}\sum_{t=1}^T\mathbf y_t^{(k)}\mathbf y_t^{(k)\top}.
\]
''',[17,18],'Section 4.1 — one-column initialization, sign convention and first projection','The initialization of D20 is the one-column D14 estimator. The rate proof is not imported as a hypothesis merely to define the algorithm; the printed algorithm step 2 disagrees with the minus-k product here.')
add('A5',r'''
where the last rate is from (4.2) with $r_{max}:=\max_{k\in[K]}r_k$.
''',[19],'Section 4.1 — definition following equation (4.6)','The maximal mode rank used in Theorem 6 is explicitly defined here. This does not define the unindexed r that also occurs in its rates.')
add('A6',r'''
\[
\check g_{-k}:=\check{\mathbf q}_{-k}^{(m)\top}\mathbf A_{-k}\mathbf A_{-k}^\top\check{\mathbf q}_{-k}^{(m)}
\]
''',[23],'Section 5.1 — defining first line of equation (5.3)','Scalar signal strength used in (5.4), with the other-mode product convention from (4.3). The subsequent rate inequality and reference to a derivation from Theorem 6 are omitted from this definition-only excerpt; they do not impose all Theorem 6 assumptions on Theorem 8.')
add('A7',claims['6']['statement_original'],[20],'Theorem 6 — full statement reused to resolve imported inline hypotheses','Theorems 7 and 9 import all Theorem 6 assumptions, including its small-o requirements, additional rate restrictions and final iterative-refinement condition. The scalars g_s, S_psi and b_k are bound here. This is an unranked reference copy, not a second theorem record or a newly named API.')
add('A8',claims['4']['statement_original'],[15],'Theorem 4 — full statement reused to resolve c_k,max and transformations','Theorem 6 refers to c_j,max defined within Theorem 4. H-double-dot-k-pre is defined in Theorem 2; the max-sample analogue follows the parallel sample convention on pages 11-12. Original rate and transformation references are preserved without inventing a replacement theorem.')
add('A9',claims['8']['statement_original'],[23,24],'Theorem 8 — defining population-style correlation matrix','Theorem 9 uses R_y,m+1^(k), defined inside Theorem 8. It depends on covariance interface D23. Theorem 8 rate conclusions are not new assumptions of Theorem 9.')
add('A10',r'Let $\lambda_j(\mathbf B)$ to be the $j$-th largest eigenvalue of matrix $\mathbf B$.',[9],'Section 3.1.3 — spectral ordering convention','All eigenvalue indices in covariance selection and rank estimation use decreasing order.')
issues=[
 dict(id='source_version',evidence=[dict(page=1,location='arXiv stamp')],detail='The inspected source is arXiv:2208.04012v1, dated 8 August 2022. The title and authors match the journal entry, but equality with the 2024 publication is not established.'),
 dict(id='appendix_tensor_conventions',evidence=[dict(page=4,location='Section 2 final paragraph'),dict(page=5,location='model and unfolding')],detail='The main text refers to Appendix Section 7 for basic tensor manipulations. It describes mode products and unfolding but does not supply the complete entry-index ordering. No appendix body was read.'),
 dict(id='unindexed_dimensions',evidence=[dict(page=19,location='RE1'),dict(page=20,location='Theorem 6'),dict(page=21,location='Theorem 7')],detail='A main-text search found no explicit definitions of the bare d and r used in RE1 and Theorems 6, 7 and 9. Products of mode dimensions and ranks are plausible interpretations, but are not substituted as source facts. d_-k is used as the number of mode-k fibers on page 5; r_-k is explicitly a product in F1 on page 7.'),
 dict(id='projection_index_mismatch',evidence=[dict(page=18,location='Algorithm step 2 and equation (4.3)'),dict(page=17,location='equation (4.1)')],detail='Algorithm step 2 prints mat_k(X_t-X_bar) times check-q_k^(i-1), whereas (4.1) and (4.3) multiply by the other-mode product q_-k. In general these have different dimensions. The original algorithm is retained; correcting k to minus-k would be a separate interpretation.'),
 dict(id='theorem6_chained_equality',evidence=[dict(page=20,location='Theorem 6 first display')],detail='The source prints d_k=O(g_s)=(r_e+sqrt(T))S_psi^(k). No extra O, inequality, or conjunction is inserted to repair this unusual expression.'),
 dict(id='theorem2_rank_subscript',evidence=[dict(page=14,location='Theorem 2 continuation')],detail='After defining H-double-dot-k-pre, the printed rank expression uses H-double-dot-k without pre. The inventory preserves this.'),
 dict(id='theorem4_trailing_comma',evidence=[dict(page=15,location='Theorem 4 definition of c_k,max')],detail='The numerator d-squared-minus-k has a trailing comma in its subscript. This source typography remains in the transcription.'),
 dict(id='filter_trace_square',evidence=[dict(page=19,location='RE1 trace display')],detail='The second trace condition is printed as T^-1 tr(A^T A)^2, with the square outside the parentheses. Whether it denotes trace of a square or square of a trace is not disambiguated by reading appendix proofs; placement is retained.'),
 dict(id='innovation_independence_scope',evidence=[dict(page=6,location='E1'),dict(page=7,location='E2 and F1')],detail='E1/E2 specify noise-component independence and F1 specifies iid factor innovations. The inspected assumptions do not explicitly assert independence between the factor and noise innovation families. No such hypothesis is silently added.'),
 dict(id='eigenvector_signs_ties',evidence=[dict(page=10,location='PCA estimator'),dict(page=12,location='maximum-ratio sample'),dict(page=17,location='plus-sign convention'),dict(page=18,location='iterative algorithm')],detail='The source supplies orthonormality and an idealized plus-sign convention but no complete deterministic eigenvector or sample-selection tie rule. Distinctness in L1-prime concerns population G_k and does not itself specify sample tie-breaking.'),
 dict(id='zero_denominators_and_empty_max',evidence=[dict(page=12,location='ER_m,j quotient and index range'),dict(page=22,location='equations (5.1)-(5.2)')],detail='Eigenvalue ratios need nonzero denominator eigenvalues; inverse diagonal square roots need positive variances. A finite-sample totalization and the value of max(empty set) in the rank estimator are not specified. The allowable ratio-index range can also be empty outside the stated asymptotic regimes.'),
 dict(id='theorem8_assumption_scope',evidence=[dict(page=23,location='RE2 and Theorem 8'),dict(page=8,location='L1 factor-strength notation')],detail='Theorem 8 explicitly lists E1, F1 and RE2 while using factor-strength exponents introduced in L1 and an estimated projection direction discussed under stronger assumptions. The graph resolves the defined objects but does not silently import L1, E2, R1, R2, L2-prime, RE1 or Theorem 6 rate hypotheses.'),
 dict(id='fixed_direction_expectation',evidence=[dict(page=23,location='prose following (5.4)')],detail='The source calls (5.4) the expected value pretending the estimated direction is constant. It is archived as an explicit formula, not identified with the actual conditional expectation given the data-dependent direction.'),
 dict(id='sample_selection_scaling',evidence=[dict(page=15,location='paragraph before Theorem 4'),dict(page=16,location='opening explanation')],detail='Comparability s_l,m asymptotic to s_l,max for all selected samples is assumed in the population-parameter restatement. It is not treated as a consequence of the selection algorithm alone and is not imposed in Theorem 2.'),
 dict(id='source_notation_typography',evidence=[dict(page=6,location='E1 sum defining Psi'),dict(page=9,location='L1-prime'),dict(page=24,location='Theorem 9 cases display')],detail='E1 alternates ell and l in a summation index; L1-prime calls the entries on G_k singular values although (3.8) defines G_k with Gram eigenvalues; Theorem 9 prints [d_k]/[r_k] for the complementary index range. Original wording and symbols are retained, with the last interpreted as set difference only in analysis.')
]
resolution={
 'all_theorems':'T,d_k,r_k,K,loading matrices and tensors come from D1; expectations, covariance, independence, iid variables, norms, spectral eigenvalues, matrix powers, sums and products use conventional finite-dimensional probability and linear algebra. Asymptotic orders are sequence-level and use the paper conventions in A1. This census does not assign library availability.',
 '1':'Direct assumptions E1/E2/F1/L1/L2/R1; L1-prime only in the final clause. Q_k,U_k resolve through D7; Q-hat and V-double-dot through D10; F-double-dot through D9. H-double-dot, c_k and P_k are defined or bound inside the theorem; U_k,(z_k) is defined there as the first columns.',
 '2':'Same printed numbered assumptions are applied to every chosen random sample, as explicitly stated. Selected-sample data and scales use D11/D14 and scalar analogues of A3. H-double-dot-pre, c_k,pre, rotations and aligned U-hat are defined inside the theorem. The printed rank subscript discrepancy remains unresolved.',
 '4':'Uses E1/E2/F1/L1/L2-prime/R1/R2 and selected-scale comparability D18; L1-prime only in the last clause. Pre and max estimators are D14/D13. Transformations and aligned eigenvectors refer to Theorems 1/2 and the sample-parallel convention; c_k,max is inline.',
 '6':'Imports all Theorem 4 assumptions including L1-prime, adds RE1, and contains its own rate restrictions. q-check uses D20 and U_(1) D7. g_s,S_psi,b_k are inline; c_j,max is in A8; r_max is A5. Bare r,d and the chained rate equality remain unresolved as documented.',
 '7':'Imports all Theorem 6 assumptions, including its final refinement condition, with the full original source in A7; q-check and sample covariance come from D20. U-check and its orthogonal rotation are existentially bound. All nested rates are retained.',
 '8':'Only E1/F1/RE2 are explicit assumptions. Its covariance is D23, whose direction uses D20; R is defined in the statement. S_psi is the inline scalar sum from A7, without importing Theorem 6 hypotheses. Factor-strength notation is recorded in A3, with unresolved implicit-scope issue explicitly retained.',
 '9':'Imports all Theorem 6 assumptions plus RE2, then adds two displayed restrictions and a_T=o(1). All inherited inline hypotheses are in A7. Sample correlation uses D24, population correlation is defined in A9 over D23, and rank estimate is D25. delta,a_T,C,eta_T are bound or specified inside the theorem.'
}
(ROOT/'ambient-conventions.json').write_text(json.dumps(dict(paper_id=PID,auxiliary_passages=aux,standard_ambient_resolution=resolution,unresolved_source_conventions=issues),indent=2,ensure_ascii=False)+'\n')
print('Saved',len(aux),'auxiliary passages and',len(issues),'source issues.')
