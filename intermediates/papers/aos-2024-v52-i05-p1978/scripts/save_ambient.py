"""Retain original local formulas, source conventions and statement-local bindings."""
import json
from save_inventory import ROOT,PID
def main():
    aux=[]
    def add(n,s,pages,note,deps=()):
        aux.append(dict(local_id='A'+str(n),statement_original=s,evidence=[dict(page=p,location='Original main-text context A'+str(n)) for p in pages],scope_note=note,depends_on=list(deps)))
    add(1,r'''We use the convention that a function $g:\mathbb R^p\to\mathbb R$ applied to a matrix $M\in\mathbb R^{m\times p}$ is the vector formed from applying $g$ to each row of $M$, that is, $g(M):=(g(M_i))_{i=1}^m$ where $M_i\in\mathbb R^p$ is the $i$th row of $M$.''',[6],'Footnote 1: rowwise function evaluation resolves tilde-mu(X) and auxiliary matrix evaluations.')
    add(2,r'''Here we have written $\hat\pi_i:=\hat\pi(X_i)=\psi(X_i^\top\hat\gamma)$ and $\pi_i=\pi(X_i)$ for simplicity.''',[5],'Indexed true and estimated propensities.',['D6','D10'])
    add(3,r'''\[
\widetilde Y_i:=\frac{T_iY_i(1-\hat\pi_i)}{\hat\pi_i}+\frac{(1-T_i)Y_i\hat\pi_i}{1-\hat\pi_i},
\]
(8)
and $\widetilde{\mathbf Y}:=(\widetilde Y_i)_{i=1}^n$''',[6],'Original unnamed transformed outcome; kept as a local formula rather than given an invented API title. Its expansion in the quadratic program uses the data and fitted propensity.',['D1','D10'])
    add(4,r'''Here $\widetilde{\mathbf Y}_A$ is the equivalent of $\widetilde{\mathbf Y}$ but with $Y_i$ and $T_i$ in definition (8) replaced by $Y_{A,i}$ and $T_{A,i}$ for $i=1,\ldots,n_A$; for later use, we similarly define $\widetilde{\mathbf Y}_B$.''',[6],'Auxiliary versions of (8), used by the quadratic constraint; not an equivalence of the datasets.',['D9','D10'])
    add(5,r'''This $\tilde\mu$ may be formed either through

(a) regressing $\widetilde{\mathbf Y}_B$ onto $\mathbf X_B$, or;

(b) estimating each of $r_1$ and $r_0$ by regressing treatment and control groups onto the confounders separately, and forming $\tilde\mu(x)=\{1-\hat\pi(X_i)\}\hat r_1(X_i)+\hat\pi(X_i)\hat r_0(X_i)$.

See Section 6 for illustrations of each of these approaches.''',[7],'Optional fitting recipes, not mandatory regression models or consistency hypotheses. The source changes x to X_i within (b); this is not repaired.',['D4','D9','D10','D12'])
    add(6,r'''For simplicity of exposition, throughout this section we assume that $n=n_A$.''',[9],'Standing Section 3.1 sample-size convention; it does not say n_B=n. In the cyclic three-fold construction both auxiliary folds have the same size as the corresponding main fold.',['D9'])
    add(7,r'''Let $\mathcal D:=(\mathbf X,\mathcal D_A,\mathcal D_B)$.''',[9],'Conditioning information for Theorems 2-3, consisting of main covariates and both auxiliary datasets, not the main Y/T observations.',['D1','D9'])
    add(8,r'''\[
\bar\sigma^2:=\frac1n\sum_{i=1}^n\left(\frac{\mathbb E\{\varepsilon_i(1)^2\mid X_i\}}{\pi_i}+\frac{\mathbb E\{\varepsilon_i(0)^2\mid X_i\}}{1-\pi_i}\right)
\]''',[10],'Original local conditional residual-variance quantity in Theorem 2. Its formula is preserved without assigning a synthetic mathematical name.',['D6','D19'])
    add(9,r'''\[
\bar\rho^3:=\frac1n\sum_{i=1}^n[\mathbb E\{|\varepsilon_i(1)|^3\mid X_i\}+\mathbb E\{|\varepsilon_i(0)|^3\mid X_i\}].
\]''',[10],'Original local conditional third-absolute-moment sum for Theorem 2; no propensity denominator belongs in this definition.',['D19'])
    add(10,r'''\[
\rho^3:=\mathbb E\left|r_1(X)-r_0(X)-\tau+\frac{T\varepsilon(1)}{\pi(X)}-\frac{(1-T)\varepsilon(0)}{1-\pi(X)}\right|^3.
\]
(20)''',[11],'Original local population absolute third moment for Theorems 3 and 5, distinct from bar-rho cubed. Its definition is expanded when resolving its statement prerequisites.',['D2','D4','D6','D19'])
    add(11,r'''\[
\mu_{\mathrm{ORA}}(X_i)=:\mu_{\mathrm{ORA},i}=\mathbb E(\widetilde Y_{\mathrm{ORA},i}\mid X_i),
\]
(13)
where $\widetilde Y_{\mathrm{ORA},i}$ is like $\widetilde Y_i$ (8) but with $\hat\pi_i$ replaced with the true propensity score $\pi_i$; see Section A.2 in the appendix for a derivation of the final equality.''',[7],'Evaluated oracle function and alternative conditional-expectation identity. Appendix derivation is not read and is not a theorem dependency.',['D6','D8'])
    add(12,r'''Let us write $\tilde\mu(\mathbf X)\in\mathbb R^n$ for the vector with $i$th component $\tilde\mu_j(X_i)$ if $i\in I_j$.''',[14],'Foldwise evaluation of the initial fits in Theorem 5. It is not the optimized concatenated mu-hat of Theorem 4.',['D12','D24'])
    add(13,'Here and below, the constants in the conclusions of our results may depend upon quantities introduced as constants in the relevant conditions for these results.',[10],'Footnote 2 attached to Theorem 2(i), also governing later theorem constants.')
    add(14,r'''Then $\tau=\mathbb E\{r_1(X)-r_0(X)\}$.''',[3],'Population contrast identity immediately after the regression definition; it is not required to define r_t or the conditional target bar-tau.',['D2','D4'])
    issues=[]
    def issue(key,text,pages):issues.append(dict(issue_id=key,description=text,evidence=[dict(page=p,location='Main-text statement or definition') for p in pages]))
    issue('normal-critical-value','The main text uses Phi in Gaussian approximation and z_alpha in (24), but no explicit main-text definition of z_alpha or its tail convention was located. The usual two-sided normal critical value is an interpretation, not a recovered source quotation; the interval formula retains the original symbol.',[10,11,13,14])
    issue('zero-variance-denominators','Theorems 2,3 and 5 divide by variances that are not explicitly required to be positive under Assumptions 1-5. In particular sigma_mu can be zero under exact correction. Do not add Assumption 7 to these results or invent a zero-denominator convention.',[10,11,14])
    issue('variance-constant-name','Assumption 7 writes sigma_epsilon, while Theorem 4 names c_epsilon in its constants. Their identification is not explicitly made in the inspected main text; both original names are preserved.',[13])
    issue('sequence-sign','Theorem 5 says any sequence e_n without an explicit sign restriction, although e_n multiplies a nonnegative norm in a bound for absolute delta. Preserve this wording and record the missing domain qualification.',[14])
    issue('inherited-m','Theorem 3 imports Theorem 2(i), including its m-dependent probability bound, without repeating m in its own preamble. The subpart reference is retained with that scope.',[10,11])
    issue('reference-scope','Theorem 5 constructs the estimator as in Theorem 4 but explicitly assumes 1-5. It does not inherit Assumptions 6-7 or the confidence-interval conclusion. Theorem 3 likewise imports only setup and bias part (i), not Theorem 2(ii).',[11,14])
    issue('fold-sample-size','Theorem 4 prints eta=c_eta*sqrt(log(p)/n), while its three main folds each contain n/3 observations. Preserve that n and the sufficiently-large-constant convention; do not silently substitute a different sample size into the theorem.',[12,13])
    issue('conditional-versus-marginal','Theorem 3 has a conditional normal approximation for zeta_1, a marginal one for zeta_2 and zero conditional cross moment. This is not an independence statement or a guarantee that their sum is marginally normal.',[11,12])
    issue('marginal-residual-bound','Assumption 7 lower-bounds Var(epsilon(t)) marginally. It is not a uniform conditional-variance bound over covariate values.',[13])
    issue('initial-fit-index','The optional fitting formula on page 7 has tilde-mu(x) on the left and fitted regressions evaluated at X_i on the right. The source notation is retained in the auxiliary passage.',[7])
    issue('source-probability-sign','A commentary sentence on page 11 bounds the probability of sigma_mu being controlled by 1-P(Omega^c)+c(p^-m+n^-m), with a printed plus sign. This is not a theorem statement and is not substituted for the actual failure bounds in the inventory.',[11])
    issue('source-scalar-vector','Theorem 2 initially writes plain mu-hat in R^n, then uses a bold correction vector in its norm. These are the same source correction in context, with the original typeface difference retained. Tilde-mu(X) is also written as a scalar function applied to a matrix using the rowwise/foldwise conventions.',[6,10,14])
    refs=[dict(from_claim_id=PID+'/T3',to_claim_id=PID+'/T2',reference_kind='setup_and_subpart',scope='Initial estimator/data/Assumptions 1-5 setup and conclusion (i) only; do not import the local moments from conclusion (ii).'),dict(from_claim_id=PID+'/T5',to_claim_id=PID+'/T4',reference_kind='estimator_construction',scope='Cross-fit estimator and sufficiently large tuning constant only; no Assumptions 6-7 or confidence-interval conclusion.')]
    bindings={
      'T2':'Delta, zeta and the result constants are local. The theorem uses basic auxiliary-data DIPW with n_A=n, Assumptions 1-5 and its displayed tuning. Sigma_mu is D22; bar-sigma and bar-rho are the exact local formulas A8-A9, resolved through the residual definition D19 and true propensity D6. Conditioning D is A7. Phi is standard normal CDF notation. No additional sparsity rate or residual lower bound is inserted.',
      'T3':'The setup and bias bound (i) of T2 are inherited. The target is population tau, and rho cubed is the original local formula A10; the conditional moments A8-A9 from T2(ii) are not inherited. Delta,zeta_1,zeta_2 are local, with the stated conditional cross moment. The m in the referenced bias bound retains its T2 quantifier.',
      'T4':'Three-fold construction D24-D25, all Assumptions 1-7, the printed tuning and interval D26 are required. The high-probability event supports every alpha in (0,1] at once. The conditioned target is bar-tau over the full observed covariate matrix. b_n comes from Assumption 6; c_epsilon versus sigma_epsilon and z_alpha are retained source conventions.',
      'T5':'Only estimator construction/tuning is inherited from T4; the theorem explicitly requires Assumptions 1-5. The initial foldwise vector is A12, not the optimized mu-hat vector. Population tau, sigma and rho are used; e_n and delta,zeta are local. The sign omission for e_n is recorded separately.'}
    out=dict(paper_id=PID,status='extracted',unranked_auxiliary_passages=aux,source_issues=issues,source_claim_references=refs,statement_local_bindings=bindings,ambient_prerequisites=['Potential outcomes and consistency Y=Y(T) are stated in the source passage for the population target; the same model underlies conditional outcomes. This does not impose independence of Y(0) and Y(1).','Standard expectations, conditional expectations, conditional independence, finite-dimensional norms, matrix products, normal CDF, probability complements, variances and third absolute moments retain their source meanings. No mathlib availability claim is made.','Unnamed local formulas A3,A8,A9,A10 and A12 remain explicit source-backed prerequisites. Their listed dependencies are expanded when connecting theorem statements or local definitions to ranked entries; they are not given invented natural-language titles.','The source does not supply a main-text z_alpha tail convention. No appendix definition is imported to fill that gap.'])
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
