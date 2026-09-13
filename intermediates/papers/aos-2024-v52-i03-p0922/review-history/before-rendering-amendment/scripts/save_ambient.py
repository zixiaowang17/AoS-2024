"""Archive local constants and referenced clauses without inventing API names."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
from save_inventory import claims as original_claims
claims={c['claim_id'].split('/T')[-1]:c for c in original_claims};aux=[]
def add(key,text,pages,location):aux.append(dict(local_id=key,statement_original=text.strip(),evidence=[dict(page=p,location=location) for p in pages]))
add('A1',r'''
For any vector $\boldsymbol v=(v_1,\ldots,v_p)\in\mathbb R^p$, we denote the $\ell_q$-norm by $\|\boldsymbol v\|_q:=(\sum_{k=1}^p|v_k|^q)^{1/q}$ and the $\ell_\infty$-norm by $\|\boldsymbol v\|_\infty:=\max_k|v_k|$. Denote by $\boldsymbol v_S=(v_{i_1},v_{i_2},\ldots,v_{i_s})^\top$ for any given $S=\{i_1,i_2,\ldots,i_s\}\subset\{1,2,\ldots,p\}$. For any matrix $A=(a_{ij})$, we define $\|A\|_1=\max_j(\sum_i|a_{ij}|)$, $\|A\|_2=\max_{\|\boldsymbol v\|_2=1}\|A\boldsymbol v\|_2$, $\|A\|_\infty=\max_i(\sum_j|a_{ij}|)$ and $\|A\|_{\max}:=\max_{i,j}|a_{ij}|$. Also, for a sequence of random variables $X_n$ and a sequence of real numbers $a_n$, we let $X_n=O_{\mathbb P}(a_n)$ denote that $\{X_n/a_n\}$ is bounded in probability and $X_n=o_{\mathbb P}(a_n)$ denote that $\{X_n/a_n\}$ converges to zero in probability. For any positive sequences $\{a_n\}$ and $\{b_n\}$, we write $a_n\lesssim b_n$ if $a_n=O(b_n)$, and $a_n\asymp b_n$ if $a_n\lesssim b_n$ and $b_n\lesssim a_n$.
''',[9,10],'Section 1.2 — notation')
add('A2',r'''One popular and convenient normalization method suggested in Horowitz (1992) is to require $|\theta_1^*|=1$, where $\theta_1$ denotes the first entry of $\boldsymbol\theta^*$. Without loss of generality, we suppose $\theta_1^*=1$ and let $\boldsymbol\theta^*=(1,\boldsymbol\beta^{*\top})^\top$ and $\boldsymbol W=(X,\boldsymbol Z^\top)^\top$, which leads to model (1) and estimator (2).''',[11],'Remark 1 — fixed coefficient scale')
add('A3','where $V$'+claims['3.1']['statement_original'].split('where $V$',1)[1],[16],'Theorem 3.1 — definition of U in (10)')
add('A4',r'''\[
T\geq\log_2\left(\frac{3\alpha}{2\alpha+1}\cdot\frac{\log(n/p)}{\log(m/p)}\right),\tag{13}
\]''',[19],'After Theorem 3.3 — iteration threshold (13)')
add('A5',r'''
Similar to (10), we define
\[
U_\ell:=\pi_U\mathbb E_{\boldsymbol Z\in\mathcal H_\ell}\left(\sum_{k=1}^\alpha\frac{2(-1)^{k+1}}{k!(\alpha-k)!}F_\ell^{(k)}(0\mid\boldsymbol Z)\rho_\ell^{(\alpha-k)}(0\mid\boldsymbol Z)\boldsymbol Z\right),
\]
which is related to the bias of SMSE on each machine.
''',[23],'Section 4.1 — U_l')
add('A6',claims['3.3']['statement_original'].split(' By choosing',1)[0],[19],'Theorem 3.3 — inherited assumption clauses')
add('A7',claims['5.1']['statement_original'].split(' By specifying',1)[0],[28,29],'Theorem 5.1 — inherited assumption clauses')
add('A8',r'''Theorem 5.2 summarizes the $\ell_2$ and $\ell_1$ error bounds of $\widehat{\boldsymbol\beta}^{(t)}$ in Algorithm 3. The detailed statement, including proper choices for $h_t$, $\lambda_n^{(t)}$ and $H(\cdot)$ and the formal definition of $r_m$, are relegated to Section A of Appendix.''',[30],'After Theorem 5.2 — explicit appendix-only details')
add('A9',r'''Compute an initial estimator $\widehat{\boldsymbol\beta}^{(0)}$ by minimizing (2) or (4) on a small subset of the data;''',[14],'Algorithm 1 — optional initialization construction')
add('A10',r'''For the multiround method, we aim to apply the iterative smoothing to minimize a weighted sum of the objective functions on each machine, that is, $\sum_{\ell=1}^LW_\ell F_{h,\ell}(\boldsymbol\beta)$,''',[23],'Section 4.1 — prose before defining update (18)')
add('A11',r'''We propose Algorithm 2, which applies (mSMSE) after selecting an estimate set $\mathcal A$ for $\mathcal A^*$ based on local SMSE estimators computed on subsets $\{\mathcal H_\ell^{(0)}\}$, where $\mathcal H_\ell^{(0)}$ contains a constant proportion $\omega$ of the local data. Now we provide the convergence rates for the estimators $\{\widehat{\boldsymbol\beta}^{(t)}\}$ in Algorithm 2.''',[25],'Section 4.2 — algorithm selection and split fraction')
add('A12',r'''Note that a feasible solution of (26) can be obtained by linear programming. A complete algorithm is presented in Algorithm 3.''',[28],'After (26) — sparse algorithm implementation')
resolution={
 'shared':'Real finite-dimensional vectors, Euclidean/coordinate norms, matrix products, transpose, inverses, eigenvalues, conditional distributions, ordinary derivatives and expectations are ambient. A1 preserves the actual norm and stochastic-order conventions. Dimension, sample size, bandwidth, tuning constants, integer iterations and nonzero direction vectors are local binders, not new interfaces. The coefficient scale is fixed by A2. Conditions (a)–(d) are standing assumptions under each active section law. No proof dependencies or appendix-only mathematics are imported.',
 '3.1':'D2 supplies the iid baseline; D3 the standing identification conditions; Assumptions 1–5 are D5–D9; D11 is the averaged estimator. The local sizes are D4. U is bound inside this theorem (A3), with rho,F,pi_U resolved through D5–D7. The bandwidth, machine constraint, direction and normal limit remain in the original statement.',
 '3.3':'D2,D3 supply baseline sampling and standing conditions. D5–D9 are Assumptions 1–5. D13 is the update conditional on an initial value satisfying the printed rate; D12,D4 supply local derivatives and partition. c_2, the initial rate, bandwidth schedule and all powers are theorem-local binders. Equation (13) is subsequent prose, not part of this theorem.',
 '3.4':'The reference to Theorem 3.3 imports its assumption clauses A6, including dimension and initial-rate conditions; D5–D9 and D2,D3 resolve them. The estimator uses D13 with the inherited first T bandwidths and a separately specified final bandwidth. A4 resolves (13); A3 resolves U. lambda_h and the nonzero direction are local binders. No plug-in estimators from Corollary 3.5 are required.',
 '4.1':'Section 4.1 replaces global iid/equal-batch assumptions with D14. D3 remains standing, D5 is Assumption 1, D9 Assumption 5, and D15–D18 Assumptions 6–9. D20 is the weighted average. U_l is local notation in A5, using D5,D15,D16 and the machine laws. Do not import homogeneous Assumptions 2–4 or a common noise CDF.',
 '4.2':'The same Section 4.1 setting and numbered assumptions as 4.1 apply, but the estimator is D21, not a local-minimizer average. U_l is A5; barred U_W,V_W are bound in the theorem. delta_0 is a generic initial error scale; the statement does not print delta_0=o(1). The unsuffixed local size m and sufficiently large T are preserved without inventing their missing connection to unequal m_l.',
 '4.3':'D22 is the overriding coefficient-shift model; global iid/common-coefficient sampling is not reintroduced by the reference to Theorem 3.3. Its numbered conditions D5–D9 and other assumption clauses A6 are retained, interpreted under the active local models, with the ambiguity recorded. D23 is the actual Algorithm 2 update, not Algorithm 1. D3 remains standing. The theorem itself binds epsilon_0, delta_m,0 and bandwidths; omega and C_0 come from Algorithm 2 and A11. The inherited initial-rate requirement and the newly defined delta_m,0 are not silently equated.',
 '5.1':'D2,D3 retain baseline sampling and standing conditions; Assumptions 1–4 are D5–D8, while Assumption 5 is replaced by the explicitly printed bounded-covariate and directional-second-moment conditions. D24 defines sparsity s; D25 is the constrained sparse update with D12 local derivatives. nu,c,s,delta_m,0,barred B,C_0,h_1 and lambda_n^(1) are locally quantified in the theorem.',
 '5.2':'Theorem 5.1 assumption clauses A7 are inherited with D2,D3,D5–D8,D24,D25. The main-text reference A8 explicitly leaves the proper bandwidth, regularization, kernel choices and formal r_m definition in excluded Appendix A. The original abbreviated statement is complete as printed; those implementation details remain unresolved within scope.'
}
issues=[
 'The pinned source is arXiv v4, not the final journal layout; equivalence to the published wording has not been established.',
 'The model normalizes the coefficient of X to +1. Remark 1 also discusses an indicator-coded response, whereas (1) uses {-1,+1}; only (1) is used for the audited model.',
 'Conditional median zero and the other identification conditions in Section 2.1 are standing assumptions for the entire paper, not newly invented numbered assumptions.',
 'The homogeneous iid law is overridden by explicit covariate-shift and coefficient-shift sections; generic model notation is interpreted under the active machine law.',
 'The sampling description does not restate a complete triangular-array independence specification in Section 4.1. Heterogeneous distribution is preserved without asserting iid observations globally.',
 'Assumption 1 permits signed higher-order kernels; nonnegativity is not stated. Its boundary constants imply unit integral as noted in main text, but positivity is not added.',
 'Assumption 2 and Assumption 6 have different boundedness wording. Assumption 6 explicitly makes derivative bounds uniform across machines; the original versions are retained separately.',
 'Assumptions 4 and 8 print strict Lambda_min<Lambda_max, which is stronger than nonsingularity and cannot hold for scalar matrices. The inequalities are not silently weakened.',
 'Population V, V_s and U are different from empirical V_m,l^(t) and U_m,l^(t); subscript s denotes the score-moment matrix, not sparsity.',
 'SMSE argmin existence, uniqueness and measurable selection are not fully specified. Newton updates have no printed fallback for singular empirical Hessians.',
 'Algorithm 1 says minimizing (2) although (2) is an argmax. The theorem accepts an initial estimator through a rate assumption, so this optional construction does not become a required proof dependency.',
 'Theorem 3.3 uses 2^(t-1), not 2^t minus 1, in its third term. Equation (13) is outside that theorem and explicitly referenced only by Theorem 3.4 among the stored statements.',
 'Theorem 3.4 inherits assumptions of 3.3 and then uses a separate final bandwidth and negative lambda_h exponent in the variance denominator. No confidence-interval corollary is added.',
 'Assumption 9 declares c_w but uses c_W in its lower bound. This casing mismatch is preserved.',
 'Assumption 9 gives norm bounds and identity sum for general matrices, without symmetry or positive definiteness. These conditions alone do not visibly ensure the weighted Hessian is invertible; the source claims are preserved, not certified.',
 'The prose before (18) calls a sum of matrix weights times scalar objectives a minimization objective. Such a sum is matrix-valued; the actual vector update (18) is retained as the operative definition.',
 'Theorem 4.1 prints a gtrsim minimum-batch condition, whereas Remark 5 describes it as ensuring a little-o condition. The printed rate hypothesis is not strengthened.',
 'Theorem 4.2 uses an unsuffixed local m despite unequal m_l in Section 4.1, a generic delta_0 without explicitly saying it tends to zero, and sufficiently large T without a displayed bound. These are unresolved statement conventions, not repaired assumptions.',
 'Theorem 4.3 inherits assumptions of 3.3 while changing to coefficient shift, a selected machine subset and a different initial error scale. Section 4.2 supplies the intended local setting; the source does not restate every inherited assumption with machine subscripts.',
 'Algorithm 2 takes floor(omega*m) observations but normalizes complementary derivatives by (1-omega)*m, not the exact residual count. Preserve both expressions.',
 'Theorem 4.3 h_0 uses p log L divided by m, while delta_m,0 and the selection threshold use omega*m. The factors are not normalized away.',
 'Algorithm 2 calls omega,C_0 preselected constants; the adjacent prose calls omega a constant proportion. A numerical lower bound for C_0 is not specified in the main-text theorem.',
 'The sparse update uses a global gradient and a single-machine Hessian. A path through the dense inverse-Hessian update would be incorrect.',
 'Theorem 5.1 prints log m in s^2 log m/(m h_1^3)=o(1), but the following explanation uses log p. The theorem retains log m, and lambda and the bound retain log p.',
 'Theorem 5.1 keeps delta_m,0 outside the last square root and uses barred B but plain C_0. Its l1/l2 comparison holds with probability tending to one, whereas 5.2 states a stochastic-order comparison.',
 'Theorem 5.2 explicitly defers the exact proper tuning and the definition of r_m to Appendix A. Main text only calls r_m infinitesimal; the excluded details remain unresolved.',
 'Asymptotic claims are sequence-level statements, but not every source constant has explicit uniform-in-n quantification. No extra uniform-risk conclusion is imported from Remark 4 or Appendix C.'
]
data=dict(paper_id=PID,auxiliary_passages=aux,standard_ambient_resolution=resolution,unresolved_source_conventions=issues,
 unresolved_statement_references=[dict(claim_id=PID+'/T5.2',reference='Section A of Appendix',items=['Proper choices of h_t, lambda_n^(t) and H','Formal definition of r_m'],status='outside_main_text_scope',evidence=[dict(page=30,location='Paragraph after Theorem 5.2')])])
def main():
    (ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved twelve auxiliary passages, all theorem resolutions and twenty-seven source conventions.')


if __name__ == "__main__":
    main()
