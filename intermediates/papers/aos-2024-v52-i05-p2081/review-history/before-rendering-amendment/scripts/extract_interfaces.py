"""Preserve original main-text source entries for the two-Theorem census."""
import json
from save_inventory import ROOT,PID
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,boundary,heading,kind='definition',context=None,context_page=None,phrases=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=phrases or [])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=boundary,semantic_boundary=boundary,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'Hellinger distance',r'''For two positive functions $f,g:\mathbb R^D\to\mathbb R$ we write the Hellinger distance as
\[
\mathrm d_H(f,g)=\left\{\int_{\mathbb R^D}(\sqrt{f(x)}-\sqrt{g(x)})^2\,dx\right\}^{1/2}.
\]''',[4],[],[r'\mathrm d_H(f,g)'],'Source Hellinger normalization without a factor 1/sqrt(2). Defined for positive functions, not restricted in this passage to normalized densities.','Section 1.4 — Hellinger distance')
add(2,'offset',r'''More precisely there exists $\delta>0$ unknown and typically small such that $P_0(M^\delta)=1$, where $M^\delta$ is the $\delta$-offset of $M$: it is the set of points that are at distance less than $\delta$ from $M$,
\[
M^\delta:=\bigcup_{x\in M}B(x,\delta)=\{z\in\mathbb R^D\mid d(z,M)\leq\delta\}.
\]''',[5],[],[r'M^\delta'],'Source offset convention. Preserve the mismatch between less than in prose and less-than-or-equal in the set display. M is a closed submanifold; the theorem uses tau-offsets as well.','Section 2 — Offset',kind='source_passage')
add(3,'effective smoothness',r'''Letting $\boldsymbol\beta=(\beta_1,\ldots,\beta_D)\in(\mathbb R_+^*)^D$, which will represent the regularity indices along each axis, we define
\[
\alpha=(\alpha_1,\ldots,\alpha_D)\quad\text{where}\quad\alpha_i=\beta/\beta_i\in[0,D]\quad\text{and}\quad\beta^{-1}=\frac1D\sum_i\beta_i^{-1}.
\]
(1)
The coefficient $\beta$ acts as the effective smoothness of the function $f$. Notice that $\alpha_1+\cdots+\alpha_D=D$.''',[6],[],[r'\beta^{-1}',r'\alpha_i=\beta/\beta_i'],'Harmonic-mean effective smoothness and normalized anisotropy. The tangent/normal specialization (5) is retained in A1. The same scalar beta and vector beta have distinct types.','Section 2.1 — Effective smoothness (1)')
add(4,'anisotropic Hölder spaces',r'''The anisotropic Hölder spaces $\mathcal H_{an}^{\boldsymbol\beta}(\mathcal U,L)$ is the set of all functions $f:\mathcal U\to\mathbb R$ satisfying:
i) For any multi-index $k\in\mathbb N^D$ such that $\langle k,\alpha\rangle<\beta$, the partial derivative $D^kf$ is well defined on $\mathcal U$ and $|D^kf(x)|\leq L(x)$ for all $x\in\mathcal U$;
ii) For any multi-index $k\in\mathbb N^D$ such that $\beta-\alpha_{max}\leq\langle k,\alpha\rangle<\beta$, there holds
\[
|D^kf(y)-D^kf(x)|\leq L(x)\sum_{i=1}^D|y_i-x_i|^{\frac{\beta-\langle k,\alpha\rangle}{\alpha_i}\wedge1}\qquad\forall x,y\in\mathcal U.
\]
(2)''',[6],[3],[r'\mathcal H_{an}^{\boldsymbol\beta}',r'\langle k,\alpha\rangle',r'\alpha_{max}'],'Complete Definition 2.1, including all mixed derivatives of admissible weighted order and local envelope L(x). U is bounded open in the main-text definition; no appendix extension is imported.','Definition 2.1')
add(5,'isotropic Hölder spaces',r'''The usual isotropic Hölder spaces are special cases of our definition of $\mathcal H_{an}^{\boldsymbol\beta}(\mathcal U,L)$ corresponding to $\boldsymbol\beta=(\beta,\ldots,\beta)$ with $\beta>0$. In this case we write
\[
\mathcal H_{iso}^{\beta}(\mathcal U,L):=\mathcal H_{an}^{\boldsymbol\beta}(\mathcal U,L)\quad\text{for}\quad\boldsymbol\beta=(\beta,\ldots,\beta).
\]''',[7],[4],[r'\mathcal H_{iso}^{\beta}'],'Isotropic specialization of this paper own Hölder definition. Vector-valued maps use the coordinatewise convention A2, not an invented operator-norm Hölder definition.','Remark 1 — Isotropic Hölder spaces')
add(6,'local parametrizations',r'''To define such a class of functions, we assume that $M$ is a closed submanifold with reach bounded from below by $\tau>0$ (see Appendix A for definition and properties of the reach) and we consider local parametrizations at any $x_0\in M$
\[
\Psi_{x_0}:V_{x_0}\to M,
\]
where $V_{x_0}$ is a neighborhood of $0$ in $T_{x_0}M$.''',[7,8],[5],[r'\Psi_{x_0}',r'V_{x_0}'],'Main-text charts use the exponential map, domain B_T(0,tau/8), and uniform isotropic regularity (3); those complete adjoining passages are retained in A3. Reach is named with its definition deferred to Appendix A, which is not imported.','Section 2.2 — Local parametrizations',kind='source_passage')
add(7,'local parametrization',r'''then one can construct a map
\[
\bar\Psi_{x_0}:\begin{cases}V_{x_0}\times N_{x_0}M\to\mathbb R^D,\\(v,\eta)\mapsto\Psi_{x_0}(v)+N_{x_0}(v,\eta),\end{cases}
\]
where $N_{x_0}(v,\cdot)$ is an isometry from $N_{x_0}M$ to $N_{\Psi_{x_0}(v)}M$ and where $v\mapsto N_{x_0}(v,\cdot)\in\mathcal H_{iso}^{\beta_M-1}(V_{x_0},C_M^\perp)$ for some other constant $C_M^\perp$ depending on $C_M$, $\tau$ and $\beta_M$. We refer to Appendix A for further details concerning the construction of $\bar\Psi_{x_0}$ and the proof of its regularity. When restricting the latter map, one gets a local parametrization of the offset $M^{\tau/2}$ around $x_0$
\[
\bar\Psi_{x_0}:V_{x_0}\times B_{N_{x_0}M}(0,\tau/2)\to M^{\tau/2}
\]
as shown in Lemma A.2. This parametrization is such that $\operatorname{pr}_M(\bar\Psi_{x_0}(v,\eta))=\Psi_{x_0}(v)$ for any $(v,\eta)\in V_{x_0}\times B_{N_{x_0}M}(0,\tau/2)$ and $\bar\Psi_{x_0}$ is a diffeomorphism from $V_{x_0}\times B_{N_{x_0}M}(0,\tau/2)$ to its image which satisfies
\[
\bar\Psi_{x_0}\in\mathcal H_{iso}^{\beta_M-1}(V_{x_0}\times B_{N_{x_0}M}(0,\tau/2),C_M^*)
\]
(4)
for some $C_M^*>0$ depending on $C_M$, $\tau$ and $\beta_M$.''',[8],[2,5,6],[r'\bar\Psi_{x_0}',r'N_{x_0}(v,\eta)'],'Offset chart and all main-text regularity assertions. The construction of normal isometries and proof of the diffeomorphism are appendix-only and remain unexpanded.','Section 2.2 — Offset parametrization (4)',kind='source_passage')
add(8,'rescaled version',r'''For any $\delta>0$, we define $\bar\Psi_{x_0,\delta}(v,\eta):=\bar\Psi_{x_0}(v,\delta\eta)$ to be the rescaled version of $\bar\Psi_{x_0}$ in the normal directions. It is a well defined parametrization of $M^{\tau/2}$ on the set $\mathcal W_{x_0,\delta}:=V_{x_0}\times B_{N_{x_0}M}(0,\tau/2\delta)$.''',[8],[7],[r'\bar\Psi_{x_0,\delta}',r'\mathcal W_{x_0,\delta}'],'Only normal coordinates are scaled by delta. The printed radius tau/2delta is retained; its intended tau/(2delta) is supported by the rescaling, without changing the quotation.','Section 2.2 — Rescaled chart')
add(9,'manifold-anisotropic Hölder',r'''Let $L:\mathbb R^D\to\mathbb R_+$ be a function; the class $\mathcal H_\delta^{\beta_0,\beta_\perp}(M,L)$ is the set of all functions $f:\mathbb R^D\to\mathbb R$ which satisfy:
i) $f$ is supported on $M^\delta$;
ii) For any $x_0\in M$, set $\bar f_{x_0,\delta}:=\delta^{D-d}f\circ\bar\Psi_{x_0,\delta}$ and $L_{x_0,\delta}:=\delta^{D-d}L\circ\bar\Psi_{x_0,\delta}$, then
\[
\bar f_{x_0,\delta}\in\mathcal H_{an}^{\boldsymbol\beta_{0,\perp}}(\mathcal W_{x_0,\delta},L_{x_0,\delta}).
\]
(6)''',[9],[2,3,4,8],[r'\mathcal H_\delta^{\beta_0,\beta_\perp}',r'\bar f_{x_0,\delta}',r'\delta^{D-d}'],'Original Definition 2.2: support and normalized chart pullbacks. The general class contains functions; density status is a separate theorem setting. Keep the delta^(D-d) factor and the tangent/normal smoothness vector from A1.','Definition 2.2',context='We call such functions manifold-anisotropic Hölder, or sometimes simply M-anisotropic.',context_page=7)
add(10,'centered Gaussian',r'''where, for any positive definite matrix $\Sigma$,
\[
\varphi_\Sigma(z):=\frac1{\det^{1/2}(2\pi\Sigma)}\exp\left\{-\frac12\|z\|_{\Sigma^{-1}}^2\right\},
\]
is the density of a centered Gaussian with covariance matrix $\Sigma$.''',[10],[],[r'\varphi_\Sigma(z)',r'\det^{1/2}(2\pi\Sigma)'],'Normalized Gaussian with positive-definite covariance. The source norm notation is the quadratic form defined in Section 1.4, retained in A10.','Section 2.3 — Gaussian density')
add(11,'Location-scale mixtures',r'''We parametrize the covariances of the components by $\Sigma=O^T\Lambda O$ where $O$ is a unitary matrix and $\Lambda=\operatorname{diag}(\lambda_1,\cdots,\lambda_D)$ is diagonal. Location-scale mixtures can then be written as:
\[
f_P(x)=\int_{\mathbb R^D}\varphi_{O^T\Lambda O}(x-\mu)\,dP(\mu,O,\Lambda),\qquad P=\sum_{k=1}^K p_k\delta_{(\mu_k,O_k,\Lambda_k)},\qquad K\in\mathbb N\cup\{+\infty\},
\]
(7)''',[10],[10],[r'f_P(x)',r'O^T\Lambda O'],'Original discrete location-scale mixture. The integral label R^D does not display the full location/orientation/eigenvalue product space; preserve it and record the measure variables rather than correcting the formula. Real unitary matrices are the paper orthogonal matrices.','Section 2.3 — Mixture (7)')
add(12,'Dirichlet process priors',r'''Recall that if $P$ follows a Dirichlet process priors with parameters $A$ and $H$ where $A>0$ and $H$ is a probability measure on some measurable space $\Theta$, then
\[
P=\sum_{k=1}^\infty p_k\delta_{\theta_k}\quad\text{with}\quad p_k=V_k\prod_{i<k}(1-V_i),\quad V_i\overset{iid}{\sim}\operatorname{Beta}(1,A)\quad\text{and}\quad\theta_k\overset{iid}{\sim}H.
\]''',[10,11],[],[r'V_i\overset{iid}{\sim}\operatorname{Beta}(1,A)',r'p_k=V_k\prod_{i<k}(1-V_i)'],'Original stick-breaking description and positive concentration parameter. Preserve the printed iid specifications; do not add a new quoted independence clause between arrays. This is one of the prior alternatives, not a simultaneous MFM requirement.','Section 2.3 — Dirichlet process')
add(13,'mixture of finite mixtures',r'''If $P$ follows a mixture of finite mixtures prior of parameters $\alpha_K$ and $\pi_K$ where $\alpha_K>0$ and $\pi_K$ is a probability measure on $\mathbb N$, then
\[
P=\sum_{k=1}^Kp_k\delta_{\theta_k}\quad\text{with}\quad K\sim\pi_K,\quad(p_1,\cdots,p_K)\mid K\sim\mathcal D(\alpha_K,\ldots,\alpha_K)\quad\text{and}\quad\theta_k\overset{iid}{\sim}H.
\]''',[11],[],[r'K\sim\pi_K',r'\mathcal D(\alpha_K,\ldots,\alpha_K)'],'Original random finite component count and conditional symmetric Dirichlet weights. The count-tail condition (9) is archived separately in A6 and applies only to MFM branches.','Section 2.3 — Mixture of finite mixtures')
add(14,'Partial location-scale mixtures',r'''The eigenvalues $\Lambda$ of the covariance of the Gaussians are common accross components,
\[
f_{\Lambda,P}(x)=\int_{\mathbb R^D}\varphi_{O^T\Lambda O}(x-\mu)\,dP(\mu,O),\qquad P=\sum_{k=1}^K p_k\delta_{(\mu_k,O_k)},\qquad K\in\mathbb N\cup\{+\infty\}
\]
(8)
where $P$ is a probability distribution on $\mathbb R^D\times O(D)$ (where $O(D)$ is the set of unitary matrices in $\mathbb R^D$) and is either a Dirichlet process prior or a mixture of finite mixtures.''',[11],[10,12,13],[r'f_{\Lambda,P}(x)',r'\delta_{(\mu_k,O_k)}'],'Shared covariance eigenvalues, with component-specific locations and orientations. D12 and D13 encode alternative prior families; dependency reach does not assert they both hold.','Section 2.3 — Partial location-scale mixtures',context='Partial location-scale mixtures:')
add(15,'Hybrid location-scale mixtures',r'''The density $f_P$ is written as (7) where $P$ conditionally on a probability $Q_2$ on $\mathbb R_+^D$ follows a Dirichlet process mixture or a mixture of finite mixtures with base measure $H_0(d\mu,dO,d\lambda)=H_1(d\mu,dO)\otimes Q_2(d\lambda)$, and $Q_2$ follows a distribution $\widetilde\Pi_\Lambda$.''',[11],[11,12,13],[r'H_1(d\mu,dO)\otimes Q_2(d\lambda)',r'\widetilde\Pi_\Lambda'],'Hierarchical random eigenvalue base measure shared across mixture components. The two prior families remain alternatives. This hierarchy is distinct from sampling one shared eigenvalue vector.','Section 2.3 — Hybrid location-scale mixtures',context='Hybrid location-scale mixtures:')
add(16,'base measure',r'''The base measure $H(d\mu,dO)=h(\mu,O)\,d\mu\,dO$ where $d\mu$ designates the Lebesgue measure on $\mathbb R^D$ and $dO$ the Haar measure on $O(D)$, and we further assume that there exist $c_1,b_1>0$ and $b_2>2D-1$ such that
\[
e^{-c_1\|\mu\|^{b_1}}\lesssim h(\mu,O)\lesssim(1+\|\mu\|)^{-b_2}\quad\text{with}\quad\forall\mu,O.
\]
(10)''',[12],[],[r'h(\mu,O)',r'b_2>2D-1'],'Location-orientation base density bounds against Lebesgue times Haar measure. Applied to H in partial mixtures and H1 in hybrid mixtures. Independent location/orientation sampling is only an example, not imposed here.','Section 2.3 — Base measure condition (10)',kind='condition')
add(17,'Conditions on the partial location-scale mixtures',r'''We also assume that $\Lambda$ is drawn from a probability measure $\Pi_\Lambda$ that has a density $\pi_\Lambda$ with respect to Lebesgue measure on $\mathbb R^D$, and that this density satisfies: there exist $c_2,c_3,b_3>0$ and $b_4>D(D-1)/2$ such that
\[
e^{-c_2\sum_{i=1}^D\lambda_i^{-d/2}}\lesssim\pi_\Lambda(\lambda_1,\cdots,\lambda_D)\quad\text{for small }\lambda_1,\ldots,\lambda_D\in(\mathbb R_+^*)^D,
\]
\[
\Pi_\Lambda\left(\min_{1\leq i\leq D}\lambda_i<x\right)\lesssim e^{-c_3x^{-b_3}}\quad\text{for small }x>0,
\]
and
\[
\Pi_\Lambda\left(\max_{1\leq i\leq D}\lambda_i>x\right)\lesssim x^{-b_4}\quad\text{for large }x>0.
\]
(11)''',[12],[14],[r'\pi_\Lambda',r'\lambda_i^{-d/2}',r'x^{-b_4}'],'Eigenvalue prior for the partial-mixture branch. Small-ball density and lower-eigenvalue tails differ from the polynomial upper tail; constants and thresholds are preserved. Condition (9) for MFM and shared condition (10) are separately retained.','Section 2.3 — Partial scale condition (11)',kind='condition',context='Conditions on the partial location-scale mixtures.',context_page=11)
add(18,'Conditions on the hybrid location-scale mixtures',r'''$H_1$ satisfies (10) and $Q_2$ is random with distribution $\widetilde\Pi_\lambda$ which satisfies: for all $b>0$ there exists $B_0,c_2>0$ such that for $x_1^2\leq x_2$ both small,
\[
\widetilde\Pi_\Lambda\left[Q_2\left([x_1,x_1(1+x_1^b)]^d\times[x_2,x_2(1+x_1^b)]^{D-d}\right)\geq x_1^{B_0}\right]\gtrsim e^{-c_2x_1^{-d/2}}.
\]
(12)
Moreover we assume that for some positive constant $c_3,b_3,c_4,b_4>0$ such that,
\[
\mathbb E_{\widetilde\Pi_\Lambda}\left[Q_2\left(\min_{1\leq i\leq D}\lambda_i\leq x\right)\right]\lesssim e^{-c_3x^{-b_3}}\quad\text{for small }x,
\]
\[
\mathbb E_{\widetilde\Pi_\Lambda}\left[Q_2\left(\max_{1\leq i\leq D}\lambda_i>x\right)\right]\lesssim e^{-c_4x^{b_4}}\quad\text{for large }x.
\]
(13)''',[12],[15,16],[r'x_1^2\leq x_2',r'x_1^{B_0}',r'\mathbb E_{\widetilde\Pi_\Lambda}'],'Random-base small-ball mass and expected tails. The product box has d and D-d coordinate blocks and both use relative width x_1^b. Preserve the source lowercase lambda alias in prose. This branch has an exponential upper tail, unlike (11).','Section 2.3 — Hybrid conditions (12) and (13)',kind='condition',context='Conditions on the hybrid location-scale mixtures.')
add(19,'kernel integral operator',r'''For any function $f:\mathbb R^D\to\mathbb R$, we define
\[
K_\Sigma f(x):=\int_{M^\tau}\varphi_{\Sigma(y)}(x-y)f(y)\,dy,
\]
where we recall that $\varphi_{\Sigma(y)}$ is the density of a centered Gaussian with variance $\Sigma(y)$.''',[18],[2,3,6,10],[r'K_\Sigma f(x)',r'\Sigma(y)'],'Location-dependent Gaussian operator. The original tangent/normal frame, diagonal scales and Sigma formula are retained in A7. The integral is over M^tau, not the whole ambient space by default, and is not a convolution.','Section 3.2 — Gaussian integral operator',context='This dependence in $y$ is crucial to adapt to the geometry of the manifold but considerably complicates the proof as the underlying kernel integral operator can no longer be written as a convolution.')
for i in [4,5,9,16,17,18]:interfaces[i-1]['lean_role']='predicate'
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
