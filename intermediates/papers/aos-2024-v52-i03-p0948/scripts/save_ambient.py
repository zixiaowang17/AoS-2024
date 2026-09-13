"""Preserve local theorem notation, data-dependent targets and source ambiguities."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
from save_inventory import claims as original_claims
claims={c['claim_id'].split('/T')[-1]:c for c in original_claims};aux=[]
def add(key,text,pages,location):aux.append(dict(local_id=key,statement_original=text.strip(),evidence=[dict(page=p,location=location) for p in pages]))
add('A1',r'''The next theorem summarizes the asymptotic prediction accuracy of $\widehat{\boldsymbol\beta}_B(\lambda)$, denoted as $A_B^2(\lambda)$.''',[9],'Before Theorem 2 — accuracy notation')
add('A2',r'''Based on these assumptions, the prediction accuracy of $\widehat{\boldsymbol\beta}_{BW}(\lambda)$ and that of $\widehat{\boldsymbol\beta}_{BZ}(\lambda)$, donated separately as $A_{BW}^2(\lambda)$ and $A_{BZ}^2(\lambda)$, respectively, are given in the next theorem.''',[12],'Before Theorem 4 — accuracy notation')
add('A3',r'''where $\boldsymbol K_l=[1+n^{-1}\mathrm E\operatorname{tr}\{(\widehat{\boldsymbol\Sigma}_{BW_l}+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l\}]^{-1}\boldsymbol\Sigma_l=\lambda v_{w_l}(-\lambda)\boldsymbol\Sigma_l$.''',[12],'Theorem 3 — K_l definition reused in Theorem 4')
add('A4',r'''$\lambda\in(0,\infty)$''',[7],'Section 2.2 — positive ridge tuning domain')
add('A5',r'''by assembling marginal GWAS summary statistics $\widehat{\boldsymbol\beta}_S=n^{-1}\boldsymbol X^T\boldsymbol y$ [Pasaniuc and Price, 2017] with correlations estimated from the publicly available reference panel $\boldsymbol W$ [Ge et al., 2019] or in-house testing GWAS $(\boldsymbol Z,\boldsymbol y_z)$ [Yang and Zhou, 2020].''',[8],'Section 2.2 — training summary statistics')
add('A6',r'''In Condition 3, we assume the causal genetic effects are i.i.d random variables $\boldsymbol\beta_{(1)}\sim F(\boldsymbol0_m,p^{-1}\cdot\boldsymbol\Sigma_\beta)$, where $\boldsymbol\Sigma_\beta=\sigma_\beta^2\cdot\boldsymbol I_m$.''',[22],'Section 7 — source interpretation of Condition 3')
add('A7',r'''The new versions of Conditions 4, 5, and 6 under the independent random effects assumption can be found in the supplementary file.''',[22],'Section 7 — excluded extension of the assumptions')
add('A8',r'''The $\widehat{\boldsymbol\beta}_B(\lambda)$ is related to the traditional ridge estimator $\widehat{\boldsymbol\beta}_R(\lambda)=n^{-1}(\widehat{\boldsymbol\Sigma}+\lambda\boldsymbol I_p)^{-1}\boldsymbol X^T\boldsymbol y$ for $\lambda\in(0,\infty)$, where $\widehat{\boldsymbol\Sigma}=n^{-1}\boldsymbol X^T\boldsymbol X$.''',[7],'Section 2.2 — background global ridge and covariance definition')
resolution={
 'shared':'Real matrices, transpose, inverse, trace, block-diagonal assembly, eigenvalues, weak convergence of probability measures and o_p(1) are ambient. Source I is a plain upright indicator in ESD formulas but bold italic I is the identity matrix. Bold Sigma and K_l are matrices; bold R_i and Q_i are scalar-valued trace abbreviations; plain K counts blocks. Source vectors beta,y and epsilon are bold. Lambda is positive by Section 2.2 (A4); negative spectral arguments are therefore away from the nonnegative spectrum. The fixed-number-of-blocks reading is consistent with the source indexing but a growing-K regime is not supplied.',
 '1':'Condition 1 includes all four subparts D3–D6, with dataset and block prerequisites D1,D4. The sample matrices are D10 and D13. D19 resolves M_l and m_l, while D18 gives the Stieltjes sign convention. Equation (4) binds the Marchenko–Pastur relation inline; H_l is the population spectral limit in D5. The source calls its population matrix Sigma_B_l at this point although Condition 1 calls it Sigma_l; retain the discrepancy. No response model, heritability or random effects are required by this trace theorem.',
 '2':'Model (1) is D2. Conditions 1–4 resolve to D3–D8 and D22, whose causal-submatrix notation is D21. The target A_B^2 is D17 instantiated with D14 as explicitly stated in A1, and h_beta^2 is D9. m_l and M_l are D19. R_1,R_2,R_3,a_l,dot a_l,lambda-star and the root equations are bound within the complete theorem; they are not renamed as invented APIs. The claimed maximizing lambda and derivative formula remain exactly as printed.',
 '3':'Condition 1 is D3–D6; the reference block covariance is D11 and v_w_l is resolved through D20 and the Stieltjes functional D18. K_l is defined in this theorem (A3), distinct from the scalar block count K. All n^{-1} factors remain n^{-1} as printed despite the reference-panel n_w limit. Neither response model nor any ridge-estimation target is a hypothesis of this trace theorem.',
 '4':'Model (1), Conditions 1–3 and 5 are D2,D3–D8,D23. Condition 5 reuses D21 causal-submatrix notation without inheriting D22 Condition 4 assumptions. A2 instantiates D17 accuracy with D15 external-reference ridge and D16 testing-panel ridge; D9 is the training heritability. Q_1–Q_7 and a_w_l,a_z_l,dot a_z_l are bound in the complete theorem. K_l comes from the original definition A3 in Theorem 3 and uses D20; Theorem 3 trace conclusions are not imported as hypotheses. The full testing covariance Sigma-hat_Z is locally defined in Condition 5.'
}
issues=[
 'The cached 60-page PDF bears arXiv:2203.12003v1 and a 22 March 2022 margin date but a 13 June 2025 title-page date. The cause is not established. Its hash, both dates and printed version identify the inspected artifact; equivalence to the final journal text is not asserted.',
 'Attached Supplementary Material starts on page 28. The altered random-effect assumptions mentioned in Section 7 and all supplementary theorems and proofs are excluded.',
 'Training and testing cohorts are described as independent while the model shares a random effect vector. The main text does not fully distinguish conditional from unconditional cohort independence after randomizing beta.',
 'Condition 1(a) describes iid innovation entries across the design matrices. The precise triangular-array coupling across sample sizes is not stated; no additional dependence construction is invented.',
 'Condition 1(a) calls population diagonal-one covariance equivalent to column-standardized data. These are not literally equivalent finite-sample operations; the source wording is retained.',
 'Known block boundaries are imposed. The theorems do not analyze learning those boundaries, despite discussion of practical block estimation.',
 'The block-count K is not explicitly given a growth rate. Each stated block aspect ratio is strictly positive; the census does not claim a growing-block result.',
 'Condition 1(b) needs the empty-prefix convention p-tilde_0=0 for the first block; only p-tilde_l=p_1+...+p_l is printed.',
 'Condition 2 prints gamma in (0,infinity), while the standing m<=p restricts a compatible gamma to at most one. Neither statement is rewritten.',
 'Condition 3 specifies a generic distribution through mean, covariance and fourth moments. Its following prose and Section 7 additionally call effect coordinates iid; isotropic covariance alone would not imply that property. The explanatory prose is archived.',
 'Condition 3 states effect independence from genetic data and independence of the two error vectors. It does not explicitly state all error-versus-design and error-versus-effect independence assumptions normally used for the prediction formulas.',
 'Training and testing error variances sigma_epsilon^2 and sigma_epsilon_z^2 are separately allowed in Condition 3. The prediction formulas only use training heritability; no equality of these variances is printed in the referenced conditions.',
 'The heritability definition is a realized training signal-energy ratio, not an expected population variance fraction. Its asserted range (0,1) presupposes nonzero signal and noise energies.',
 'The out-of-sample R^2 is an uncentered squared cosine. No intercept fitting, centering or residual-sum-of-squares definition is substituted, and zero response/prediction norms are not specified.',
 'Sample covariance matrices are uncentered Gram matrices divided by the stated sample sizes, not unbiased centered covariances.',
 'The external-reference and testing-panel ridge formulas scale their training cross-products by n_w^{-1} and n_z^{-1}. The subsequent summary-statistic prose uses n^{-1}X^Ty. These normalizations are preserved; positive rescaling cancels from squared-cosine accuracy but does not identify the estimators themselves.',
 'The training ridge introduction says black-wise instead of block-wise in one sentence. The body retains the typo; its display keyword comes from the actual subsection heading.',
 'Theorem 1 calls H_l the LSD of population Sigma_B_l, whereas Condition 1 names the population block Sigma_l. No separate population Sigma_B_l construction is supplied.',
 'Theorems 1 and 2 use the wording limit together with an o_p(1) remainder and finite-dimensional trace expressions. The original asymptotic-equivalent convention is retained without converting it to a different convergence claim.',
 'The Stieltjes transform convention is (t-z)^{-1}. Full complex-domain and branch-selection conditions are not separately written in the main text; actual theorem evaluations use negative real arguments.',
 'The printed dot-a_l and dot-a_z_l formulas have negative denominators and the source calls them first order derivatives without explicitly naming the differentiation variable. No sign is repaired or derivative theorem certified.',
 'Theorem 2 asserts that lambda-star=omega(1-h_beta^2)/h_beta^2 maximizes the blockwise accuracy. This complete optimality assertion is stored but has not been proved by the census.',
 'Theorem 3 repeatedly uses n^{-1} rather than n_w^{-1} in reference-panel formulas, including the expectation defining K_l. Theorem 4 repeats those factors in Q_2 and Q_3. They remain literal source statements.',
 'Theorem 3 equates a finite-sample expectation construction of K_l with lambda times the companion limiting transform. The distinction between exact equality and deterministic equivalence is not elaborated in that statement.',
 'Condition 4 and Condition 5 restrict trace ratios only for their listed matrices; a universal matrix homogeneity condition is not asserted. The causal submatrix notation is shared, but their conditions are distinct.',
 'The last matrix in Condition 5 has population Sigma on both ends. This is not silently changed to a product ending in sample Sigma-hat.',
 'The testing-panel estimator depends on the same testing design used for evaluation; it must not inherit the independent-reference interpretation.',
 'Theorems 2–4 use min(...,p_l) without writing every block index in that minimum. Condition 1 states its limits for each block; no extra uniform-in-l quantifier is inserted.'
]
data=dict(paper_id=PID,auxiliary_passages=aux,standard_ambient_resolution=resolution,unresolved_source_conventions=issues,unresolved_statement_references=[])
def main():
    (ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved eight auxiliary passages, four theorem resolutions and twenty-eight source notes.')


if __name__ == "__main__":
    main()
