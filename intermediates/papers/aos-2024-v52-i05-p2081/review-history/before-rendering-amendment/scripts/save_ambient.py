"""Keep all main-text assumptions and prior branches, without appendix expansion."""
import json
from save_inventory import ROOT,PID
def main():
    aux=[]
    def add(n,s,pages,note,deps=()):
        aux.append(dict(local_id='A'+str(n),statement_original=s,evidence=[dict(page=p,location='Original main-text context A'+str(n)) for p in pages],scope_note=note,depends_on=list(deps)))
    add(1,r'''We let $\beta_0,\beta_\perp$ be two positive real numbers, and define the vector
\[
\boldsymbol\beta_{0,\perp}=(\underbrace{\beta_0,\ldots,\beta_0}_{d},\underbrace{\beta_\perp,\ldots,\beta_\perp}_{D-d})\in\mathbb R^D.
\]
and define $\alpha$ to be the counterpart of $\boldsymbol\beta_{0,\perp}$ as in (1):
\[
\alpha=(\alpha_0,\ldots,\alpha_0,\alpha_\perp,\ldots,\alpha_\perp)\quad\text{with}\quad\alpha_0=\beta/\beta_0,\quad\alpha_\perp=\beta/\beta_\perp,
\]
and
\[
\beta^{-1}=\frac dD\beta_0^{-1}+\frac{D-d}D\beta_\perp^{-1}.
\]
(5)''',[8],'Exact tangent/normal specialization of the effective smoothness and anisotropy in D3. Retain both dimension weights and the multiplicities.',['D3'])
    add(2,r'''For a multi-index $k=(k_1,\ldots,k_D)\in\mathbb N^D$, we set $|k|=k_1+\cdots+k_D$ and $k!=k_1!\ldots k_D!$.''',[4],'Multi-index convention for the weighted derivatives. Derivatives, Euclidean products, sup norms and finite-dimensional tangent/normal spaces use the definitions in Section 1.4.')
    add(3,r'''For purely practical matter, we choose $\Psi_{x_0}$ to be the exponential map $\exp_{x_0}$, although the results in this paper could be carried out with other well-behaved parametrizations, such as the one mentioned above. In particular, in the case of the exponential maps, we can define the domain of $\Psi_{x_0}$ to be $B_{T_{x_0}M}(0,\pi\tau)$, see Appendix A. In the rest of this paper, we set
\[
V_{x_0}:=B_{T_{x_0}M}(0,\tau/8),
\]
with factor $1/8$ being there for technical reasons. If all the maps $\Psi_{x_0}$ are of regularity $\beta_M>1$, meaning that there exists a constant $C_M>0$ such that
\[
\Psi_{x_0}\in\mathcal H_{iso}^{\beta_M}(V_{x_0},C_M),\ \forall x_0\in M
\]
(3)
(in particular $M$ is at least $C^k$ with $k=\lceil\beta_M-1\rceil$),''',[8],'Original uniform chart regularity. Theorems impose the stronger beta_M bound through their own assumptions; the definition of reach and existence facts cited to Appendix A remain unexpanded.',['D5','D6'])
    add(4,r'''Recall that $X_1,\ldots,X_n$ is an $n$ sample drawn from a distribution $P_0$ with density $f_0$. Recall that $f_0=f_{0,n}$ might depend on $n$, but that all the constants appearing in the subsequent conditions do not.

Conditions on $M$: the submanifold $M$ is of dimension $d$ and has a reach greater than $\tau>0$. Furthermore, there exists $\beta_M>4$ and $C_M>0$ such that $\Psi_{x_0}\in\mathcal H_{iso}^{\beta_M}(V_{x_0},C_M)$, $\forall x_0\in M$. In particular, $M$ also satisfies (4).''',[13],'Standing main-result model and uniform-in-n constants. Reach is strictly greater than tau here, stronger than the earlier bounded-from-below wording.',['D5','D6'])
    add(5,r'''Conditions on $f_0$: the density $f_0$ is in $\mathcal H_\delta^{\beta_0,\beta_\perp}(M,L)$ with $\delta=\delta_n\leq\tau/2$. Furthermore, there exists $c_5,\kappa>0$,
\[
f_0(x)\lesssim e^{-c_5\|x\|^\kappa}\qquad\forall x\in\mathbb R^D,
\]
(14)
and for some $\omega>6\beta$ and $C_0<\infty$,
\[
\int_{\mathcal W_{x_0,\delta}}\left|\frac{D^k\bar f_{x_0,\delta}}{\bar f_{x_0,\delta}}\right|^{\omega/\langle k,\alpha\rangle}\bar f_{\delta,x_0}\leq C_0\quad\text{and}\quad\int_{\mathcal W_{x_0,\delta}}\left|\frac{L_{x_0,\delta}}{\bar f_{x_0,\delta}}\right|^{\omega/\beta}\bar f_{\delta,x_0}\leq C_0.
\]
(15)
for all $\delta$ small, $x_0\in M$ and all $0\leq\langle k,\alpha\rangle<\beta$. Recall that the quantities $\alpha$ and $\beta$ are defined through $\beta_0$ and $\beta_\perp$ through (5).''',[13],'Both complete assumptions (14)-(15), including uniform small-delta/chart quantifiers. Preserve the printed zero-order exponent division, swapped indices on the integration weight, and omitted differential. Do not insert a density-zero convention. Theorem 3.1 strengthens omega separately.',['D3','D8','D9'])
    add(6,r'''$f$ is modelled as in (8) and $P$ follows either a Dirichlet process with base measure $H$ or a mixture of finite mixtures with base measure $H$ and prior on $K$ satisfying
\[
-\log\Pi_K(K=x)\simeq x(\log x)^r,\qquad r=0,1.
\]
(9)''',[11],'MFM component-count mass condition. Table 1 applies (9) to both partial-MFM and hybrid-MFM combinations, not to DPM alternatives. Pi_K and pi_K are the source aliases for this prior.',['D12','D13','D14'])
    add(7,r'''To explain the construction, we denote, for any $x\in M^\tau$, $T_x=T_{\operatorname{pr}_M(x)}M$ and $N_x=N_{\operatorname{pr}_M(x)}M$. We set $\mathcal B_x^0$ an orthonormal basis of $T_x$, $\mathcal B_x^\perp$ an orthonormal basis of $N_x$, and let $O_x$ be the matrix of the linear map $z\mapsto(\operatorname{pr}_{T_x}z,\operatorname{pr}_{N_x}z)$ from the canonical basis to the concatenated basis $(\mathcal B_x^0,\mathcal B_x^\perp)$. We finally write $\Sigma(x)=O_x^\top\Delta_{\sigma,\delta}^2O_x$ where
\[
\Delta_{\sigma,\delta}=\begin{pmatrix}\sigma^{\alpha_0}\operatorname{Id}_d&0\\0&\delta\sigma^{\alpha_\perp}\operatorname{Id}_{D-d}\end{pmatrix}.
\]
Note that $\Sigma(x)$ does not depends on the choice of the bases $\mathcal B_x^0$ and $\mathcal B_x^\perp$ since for any orthonormal basis change $P$ that preserves $T_x$ (whence $N_x$), one has $P^\top\Delta_{\sigma,\delta}P=\Delta_{\sigma,\delta}$.''',[17,18],'Original geometric covariance. Delta contains standard-deviation scales and is squared in Sigma. Unique nearest projection relies on the standing reach condition. Theorem 3.4 also uses Delta_(1,delta) explicitly in its chart coordinates.',['D2','D3','D6'])
    add(8,r'''We assume that we observe $X_1,\ldots,X_n$ independent and identically distributed from $P_0$ on $\mathbb R^D$ with density $f_0$ with respect to Lebesgue measure.''',[5],'The n-sample in Theorem 3.1 is iid with a Lebesgue density. This does not describe observations drawn directly from Hausdorff measure on the manifold.')
    add(9,r'''We would like to underline here that $\delta$ is to be understood as $\delta=\delta_n$ which can either stay constant (and smaller than the reach of $M$, defined in Appendix A) or goes to $0$ as $n$ goes to infinity, in which case $f_0=f_{0,n}$ and $X_j=X_{j,n}$ is a triangular array of data.''',[5],'Offset width and true density may vary with n; constants in the main-result assumptions remain uniform.',['D2'])
    add(10,r'''For any matrix $A\in\mathbb R^{k\times k}$, the notation $\|\cdot\|_A^2$ will refer to the quadratic form over $\mathbb R^k$ defined by $x\mapsto\langle Ax,x\rangle$, which is a squared norm if $A$ is positive definite.''',[4],'Quadratic-form convention used by the Gaussian density. No extra square of A is involved.')
    add(11,r'''As a final remark, we will use the same notations for the spaces of multivalued functions when their coordinate functions are all in the corresponding space. For instance, if $\Psi:\mathcal U\to\mathbb R^{D_1}$, for $D_1>1$, then
\[
\Psi=(\Psi_1,\ldots,\Psi_{D_1})\in\mathcal H_{an}^{\boldsymbol\beta}(\mathcal U,L)\quad\Longleftrightarrow_{def}\quad\Psi_i\in\mathcal H_{an}^{\boldsymbol\beta}(\mathcal U,L)\text{ for all }i\in\{1,\ldots,D_1\},
\]
and the same holds for the other spaces defined in this subsection.''',[7],'Coordinatewise convention for vector-valued charts and normal isometry maps.',['D4','D5'])
    add(12,r'''We let $\mathcal U\subset\mathbb R^D$ be a bounded open subset and $L:\mathcal U\to\mathbb R_+$ be any non-negative function.''',[6],'Domain and envelope binder preceding Definition 2.1. The extension to general open sets is deferred to Appendix C.1.')
    add(13,r'''We denote by $\Pi$ the prior on the parameter and we consider the following assumptions on $\Pi$. These conditions differs wether $\Pi$ is assumed to come from a partial location-scale mixture prior or a hybrid location-scale mixture prior.''',[11],'Theorem posterior Pi is the conditional law under the selected prior and iid sampling model. No explicit Bayes formula is printed here; the usual conditional-law meaning remains ambient.',['D14','D15'])
    add(14,r'''In the rest of this paper the symbols $\simeq$, $\lesssim$ and $\gtrsim$ denote equalities or inequalities up to a constant depending on $D$, $d$, $\tau$, $\beta_M$, $C_M$, $\beta_0$, $\beta_\perp$ and all the other constants appearing in conditions (9) to (15).''',[13],'Exact main-result comparison-constant scope. Together with A4, these constants do not vary with n or the shrinking offset.')
    issues=[]
    def issue(key,text,pages):issues.append(dict(issue_id=key,description=text,evidence=[dict(page=p,location='Original main-text statement or convention') for p in pages]))
    issue('offset-boundary','The offset prose says distance less than delta; its display uses distance at most delta. Both originals remain. The census does not choose an open/closed-ball convention to repair the discrepancy.',[5])
    issue('appendix-only-geometry','Reach is named but its definition/properties and the construction of the normal isometries are deferred to Appendix A. Main-text chart and regularity assertions are retained; the appendix construction is not fabricated or imported.',[7,8,13])
    issue('weighted-zero-order','Equation (15) quantifies 0<=<k,alpha><beta, while its first exponent is omega/<k,alpha>. At k=0 this is undefined without a convention. The source also does not specify ratios where fbar=0. These are unresolved source meanings, not reasons to delete the zero order.',[13])
    issue('pullback-index-alias','Equation (15) writes fbar_(x0,delta) in ratios but fbar_(delta,x0) as weight. Definition 2.2 defines only the former. The original indices and omitted differential are preserved, with the correspondence recorded as an apparent source alias.',[9,13])
    issue('prior-product-domain','The mixture integrals (7)-(8) are labeled R^D while P includes orientation and sometimes scale variables. Preserve the source display; the surrounding text specifies the intended product-space mixing parameters.',[10,11])
    issue('prior-alternatives','Table 1 combines one weight-family column and one scale-family column. MFM adds (9); DPM does not. Both use (10). Partial scales require (11), hybrid scales (12)-(13). Dependency reach is the union of these conditional branches, not their conjunction.',[11,12,13,14])
    issue('prior-notation-aliases','The source switches pi_K/Pi_K for the count law and tilde-Pi_lambda/tilde-Pi_Lambda for the random scale law. These printed aliases remain. Independent location and orientation or inverse-Gamma scale laws are examples, not new theorem conditions.',[11,12])
    issue('scale-square','Sigma is O_x^T Delta^2 O_x: Delta contains standard deviations, not eigenvalues. Theorem 3.4 uses Delta_(1,delta)^(-1) in its coordinate formula. No square or inverse is dropped.',[17,18])
    issue('partition-locality','Theorem 3.4 places a packing in M^tau and uses chart centers x_j, although Section 2 charts are indexed by points of M. Its partition is referred to Section D.1; the main-text proof later mentions Lemma B.4. Preserve these references and this location ambiguity without importing appendix constructions.',[8,18,24])
    issue('approximation-coefficients','Theorem 3.4 specifies smooth bounded d_(j,k) depending on chi_j and M, but does not give full coefficient formulas or separately describe d_0 in its statement. Retain the existential expansion. It neither asserts that g is nonnegative nor normalizes g to be a density.',[18])
    issue('approximation-quantifiers','Theorem 3.4 prints existence of g before for any H>0, while the packing region includes log(1/sigma) and the asserted bound uses H. Preserve that quantifier order and do not insert hidden dependence or uniformity restrictions. Positive small scales are implicit in preceding constructions; the statement itself prints sigma,delta<=1.',[17,18])
    issue('chart-domain-extension','The main text defines offset charts on tau/2 neighborhoods but Theorem 3.4 invokes a tau-offset packing and arbitrary x. Local inverse-chart terms require a locality/extension convention not fully supplied by its statement. The theorem and appendix reference are preserved without inventing a global inverse.',[8,18])
    refs=[dict(from_claim_id=PID+'/T3.1',to_source_label='Table 1; (14)-(15); (5)',reference_kind='assumptions',scope='Choose exactly one weight prior and one scale prior; density and geometry assumptions are common. Omega is strengthened explicitly in this theorem.'),dict(from_claim_id=PID+'/T3.1',to_claim_id=PID+'/T3.4',reference_kind='proof_only',scope='The approximation result is used for prior-mass control in the proof on page 21, not to define the posterior-contraction statement.'),dict(from_claim_id=PID+'/T3.4',to_source_label='Section D.1; Appendix A',reference_kind='appendix_definition',scope='Retain the partition-of-unity and chart construction references without consulting appendix bodies.')]
    branches=[dict(weight_family='MFM',scale_family='partial',conditions=['9','10','11']),dict(weight_family='DPM',scale_family='partial',conditions=['10','11']),dict(weight_family='MFM',scale_family='hybrid',conditions=['9','10','12','13']),dict(weight_family='DPM',scale_family='hybrid',conditions=['10','12','13'])]
    bindings={'T3.1':'The iid Lebesgue-density sample and triangular-array conventions are A8-A9. E_0^n averages under the true product law and Pi(.|X_n) is the posterior of the selected prior A13. Hellinger is D1 and f_P is D11 (f_(Lambda,P) in the partial branch D14). D12/D13 are alternative weight priors; D14/D15 alternative scale constructions. Table 1 is recorded as four branches. Conditions (9)-(13) are A6,D16-D18 with their branch scopes. D6/A3-A4 give geometry; D9 and A5 give density support, smoothness, tail and normalized derivative assumptions. D3/A1 resolve beta,alpha_0,alpha_perp; the strengthened omega and epsilon_n,p are bound in the theorem. No K_Sigma or approximation machinery is imported through the proof.','T3.4':'The function class is D9 with A5=(14)-(15), geometry is D6/A3-A4, and effective parameters D3/A1. K_Sigma is D19 with Gaussian D10 and geometric covariance A7. The theorem binds g,H,d_0,d_(j,k),packing,chi_j and z_(j,x); the pullback overline(chi_j f0) uses the normalization of D9 and charts D7-D8. Delta_(1,delta) is A7 with sigma=1. The partition construction and locality conventions are appendix-only and unresolved, explicitly retained as source references. No priors, posterior, Hellinger correction or normalization of g is required by this statement.'}
    out=dict(paper_id=PID,status='extracted',unranked_auxiliary_passages=aux,source_issues=issues,source_claim_references=refs,statement_local_bindings=bindings,prior_condition_branches=branches,prior_branch_evidence=[dict(page=13,location='Table 1')],unresolved_appendix_references=['Appendix A: definition/properties of reach and chart construction.','Section D.1: partition of unity in Theorem 3.4; main-text proof additionally cites Lemma B.4.'],ambient_prerequisites=['Finite-dimensional real spaces, tangent/normal spaces, orthogonal projection, exponential maps, partial derivatives, Haar and Lebesgue measures, Gaussian densities, Dirichlet and Beta laws, conditional probability and iid product expectations retain the source meanings. No mathlib verdict is made.','Natural vector beta and scalar harmonic-mean beta are distinct. The theorem k is a multi-index, alpha a weighted-order vector and alpha_0/alpha_perp are its repeated tangent/normal entries.','The source uses unitary for real orthogonal matrices. Sigma is positive definite for positive scales; the theorem prints only the upper bound on sigma and delta, with positivity inherited from the model construction.','Source quantities whose definitions are deferred exclusively to appendices remain referenced and unresolved. No reconstructed appendix theorem or invented source definition is used.','Theorem 3.4 is an approximation by a real-valued function g. The Hellinger-normalized density in Corollary 3.5 is a downstream result and is neither an inventoried Theorem nor a dependency of Theorem 3.4.'])
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
