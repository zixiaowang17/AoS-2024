"""Reproduce original source passages; see the separate paper audit for validation status."""
import json
from save_inventory import PID,ROOT
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,description,heading=None,context=None,kind='definition',context_page=None):
    lid=f'D{n}';heading=heading or 'Source definition — '+term[0].upper()+term[1:]
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=[])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=description,semantic_boundary=description,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'isotropic Gaussian',r'''Consider i.i.d. samples $\{X_i\}_{1\leq i\leq N}\in\mathbb R^d$ generated from an isotropic Gaussian mixture $\rho^\star*\mathcal N(0,I_d)$ with density function
\[
(\rho^\star*\phi)(x)=\int_{\mathbb R^d}\phi(x-y)\rho^\star(dy),
\]
where $\rho^\star$ is a mixing distribution over $\mathbb R^d$, and $\phi(x)=(2\pi)^{-d/2}\exp(-\|x\|_2^2/2)$ is the density function of the isotropic Gaussian distribution $\mathcal N(0,I_d)$. The goal is to learn the Gaussian mixture $\rho^\star*\mathcal N(0,I_d)$ from $N$ samples.''',[1],[4],[r'\phi(x)',r'\rho^\star*\phi',r'\mathcal N(0,I_d)'],'Isotropic unit-covariance Gaussian density and its convolution with a mixing distribution. The statistical setup has iid data; the optimization statements may condition on the observed sample.',heading='Section 1 — Isotropic Gaussian mixture',kind='source_passage')
add(2,'negative log-likelihood',r'''The negative log-likelihood for this problem is defined as
\[
\ell_N(\rho)=-\frac1N\sum_{i=1}^N\log[(\rho*\phi)(X_i)].
\]''',[2],[1],[r'\ell_N(\rho)',r'\rho*\phi'],'Empirical average negative log mixture density, using the fixed observed sample and the unit-covariance Gaussian convolution.',heading='Section 1 — Negative log-likelihood')
add(3,'nonparametric maximum likelihood estimator',r'''To overcome this limitation, Kiefer and Wolfowitz (1956) proposed the nonparametric maximum likelihood estimator (NPMLE) which prescribes to minimize $\ell_N$ over the set $\mathcal P(\mathbb R^d)$ of all probability distributions over $\mathbb R^d$:
\[
\widehat\rho\in\operatorname*{argmin}_{\rho\in\mathcal P(\mathbb R^d)}\ell_N(\rho).
\]
(1.1)''',[2],[2,4],[r'\widehat\rho',r'\operatorname*{argmin}_{\rho\in\mathcal P(\mathbb R^d)}'],'Any minimizer over all probability measures, without a fixed atom count or a finite-second-moment restriction. Existence is a theorem conclusion; uniqueness is not assumed.',heading='Section 1 — Nonparametric maximum likelihood estimator (1.1)')
add(4,'space of probability measures',r'''We use $\mathcal P(\mathbb R^d)$ to denote the space of probability measures over $\mathbb R^d$, $\mathcal P_2(\mathbb R^d)$ to denote the space of probability measures over $\mathbb R^d$ with finite second moments, and $\mathcal P_{\mathrm{ac}}(\mathbb R^d)$ to denote the space of probability measures that are absolutely continuous with respect to the Lebesgue measure on $\mathbb R^d$.''',[3],[],[r'\mathcal P(\mathbb R^d)',r'\mathcal P_2(\mathbb R^d)',r'\mathcal P_{\mathrm{ac}}(\mathbb R^d)'],'Three distinct probability-measure classes. Neither a finite second moment nor a density is silently imposed on every measure.',heading='Notation — Spaces of probability measures')
add(5,'support set',r'''For any $\rho\in\mathcal P(\mathbb R^d)$, $\operatorname{supp}(\rho)$ denotes its support set, i.e. the smallest closed set $C\subseteq\mathbb R^d$ such that $\rho(C)=1$.''',[3],[4],[r'\operatorname{supp}(\rho)'],'Closed full-measure support; a full-support initialization differs from a finite particle initialization.',heading='Notation — Support set')
add(6,'pushforward',r'''For any mapping $T:\mathbb R^d\to\mathbb R^d$ and any distribution $\rho\in\mathcal P(\mathbb R^d)$, let $T_\#\rho$ be the pushforward (or image measure) of $\rho$ by $T$, which is defined by $T_\#\rho(A)=\rho(T^{-1}(A))$ for any Borel set $A$ in $\mathbb R^d$.''',[3],[4],[r'T_\#\rho'],'Image measure on Borel sets. The source says any mapping without explicitly imposing measurability; the issue is retained separately.',heading='Notation — Pushforward')
add(7,'weakly converges',r'''For a sequence $\{\rho_n\}_{n=0}^{\infty}$ in $\mathcal P(\mathbb R^d)$ and $\rho\in\mathcal P(\mathbb R^d)$, we write $\rho_n\xrightarrow{\mathrm w}\rho$ if $\rho_n$ weakly converges to $\rho$, i.e. $\int_{\mathbb R^d}f(x)\rho_n(dx)\to\int_{\mathbb R^d}f(x)\rho(dx)$ holds for every bounded continuous function $f:\mathbb R^d\to\mathbb R$.''',[3],[4],[r'\rho_n\xrightarrow{\mathrm w}\rho',r'\rho_n\xrightarrow{\mathrm w}\widehat\rho'],'Weak convergence against all bounded continuous real test functions. In Theorems 2 and 4 this is an assumption, not a proved convergence guarantee.',heading='Notation — Weakly converges')
add(8,'distributional solution',r'''Let $C_c^\infty(\mathbb R^d)$ be the set of smooth functions with compact support in $\mathbb R^d$. We say that $(\rho_t)_{t\geq0}$ is a distributional solution to the partial differential equation (PDE) $\partial_t\rho_t=-\operatorname{div}(\rho_tv_t)+\rho_t\alpha_t$ where $v_t:\mathbb R^d\to\mathbb R^d$ and $\alpha_t:\mathbb R^d\to\mathbb R$, if for any $\varphi\in C_c^\infty(\mathbb R^d)$ it holds that
\[
\frac{d}{dt}\int_{\mathbb R^d}\varphi(x)\rho_t(dx)=\int_{\mathbb R^d}[\langle\nabla\varphi(x),v_t(x)\rangle+\varphi(x)\alpha_t(x)]\rho_t(dx).
\]''',[3],[4],[r'C_c^\infty(\mathbb R^d)',r'\partial_t\rho_t',r'\frac{d}{dt}'],'The source weak PDE convention uses spatial compactly supported smooth test functions and a time derivative. Temporal regularity and whether equality is pointwise or almost everywhere in time are not separately specified.',heading='Notation — Distributional solution')
add(9,'first variation',r'''In this section, we examine optimality conditions for the optimization problem (1.1). To that end, denote by $\delta\ell_N(\rho)$ the first variation of $\ell_N$ at a measure $\rho$ and observe that it is given by
\[
\delta\ell_N(\rho):x\mapsto-\frac1N\sum_{i=1}^N\frac{\phi(x-X_i)}{(\rho*\phi)(X_i)}.
\]
(2.1)''',[3],[2,1,4],[r'\delta\ell_N(\rho)',r'\delta\ell_N(\widehat\rho)'],'Specific representative of the likelihood first variation, with its fixed additive constant convention. It depends on the functional and Gaussian kernel, not on existence of an NPMLE.',heading='Section 2 — First variation (2.1)')
add(10,'WFR gradient descent',r'''To overcome the first obstacle, we employ a straightforward time-discretization scheme to obtain a WFR gradient descent. This algorithm produces a sequence of probability measures $\{\rho_n\}_{n\geq0}$. It makes the following two steps alternately:
\[
\frac{d\widetilde\rho_n}{d\rho_n}=1-\eta[1+\delta\ell_N(\rho_n)]\qquad\text{(Fisher-Rao gradient update)}
\]
(3.7a)
\[
\rho_{n+1}=[\operatorname{id}-\eta\nabla\delta\ell_N(\widetilde\rho_n)]_\#\widetilde\rho_n\qquad\text{(Wasserstein gradient update)}
\]
(3.7b)
for $n=0,1,\ldots$, where $\eta>0$ is the step size.''',[6],[4,6,9],[r'\widetilde\rho_n',r'\rho_{n+1}',r'\delta\ell_N(\rho_n)'],'Ordered two-stage measure update: change weights first, then push the intermediate measure using its own first variation. It is distinct from the finite-particle Algorithm 1, whose update order and source indices require separate review.',heading='Section 3.2 — WFR gradient descent (3.7)')
add(11,'Wasserstein-Fisher-Rao gradient flow',r'''The gradient flow $\{\rho_t\}_{t\geq0}$ of the negative log-likelihood $\ell_N(\rho)$ in $\mathcal P_2(\mathbb R^d)$ with respect to the Wasserstein-Fisher-Rao distance $d_{\mathrm{WFR}}(\cdot,\cdot)$ is given by
\[
\partial_t\rho_t=-[1+\delta\ell_N(\rho_t)]\rho_t+\operatorname{div}(\rho_t\nabla\delta\ell_N(\rho_t)).
\]
(3.6)''',[5],[4,9,8,15,18],[r'\partial_t\rho_t',r'd_{\mathrm{WFR}}'],'Likelihood flow with both reaction and transport terms. Its geometric meaning uses the preceding gradient-flow construction and WFR distance; the source characterizes it by the distributional PDE.',heading='Section 3.2 — Wasserstein-Fisher-Rao gradient flow (3.6)',context=r'''The following theorem gives a precise characterization of the Wasserstein-Fisher-Rao gradient flow initialized from $\rho_0$.''',context_page=6)
add(12,'Fisher-Rao gradient flow',r'''We show in Appendix C.2.1 that the Fisher-Rao gradient flow $(\rho_t)_{t\geq0}$ of the function $\ell_N(\rho)$ is defined by the following PDE:
\[
\partial_t\rho_t=-[1+\delta\ell_N(\rho_t)]\rho_t.
\]
(3.11)''',[7],[4,9,8,15,16],[r'\partial_t\rho_t',r'\delta\ell_N(\rho_t)'],'Reaction-only likelihood flow under the Fisher-Rao geometry. The appendix reference is retained but its body is excluded; the main-text PDE and geometric definition are sufficient to archive the claimed meaning.',heading='Section 3.3 — Fisher-Rao gradient flow (3.11)')
add(13,'Fisher-Rao gradient descent',r'''By time discretization, one readily obtains the Fisher-Rao gradient descent updates $\{\rho_n\}_{n\geq0}$:
\[
\frac{d\rho_{n+1}}{d\rho_n}=1-\gamma[1+\delta\ell_N(\rho_n)],\qquad n=0,1,\ldots,
\]
(3.12)
where $\gamma>0$ is the step size.''',[7],[4,9],[r'\frac{d\rho_{n+1}}{d\rho_n}',r'\gamma'],'Explicit reaction-only update of probability measures. Its step size is gamma in the source, whereas Theorem 4 uses eta without stating their identification. The continuous-time flow is motivation, not an input to this formula.',heading='Section 3.3 — Fisher-Rao gradient descent (3.12)')
add(14,'Wasserstein gradient flow',r'''In Appendix C.3 we derive the gradient flow of $\ell_N(\rho)$ under the Wasserstein geometry, which evolves according to the PDE
\[
\partial_t\rho_t=\operatorname{div}(\rho_t\nabla\delta\ell_N(\rho_t))
\]
(3.18)''',[9],[4,9,8,15,17],[r'\partial_t\rho_t',r'\nabla\delta\ell_N(\rho_t)'],'Transport-only likelihood flow under the quadratic Wasserstein geometry, with the main-text distributional PDE characterization. The appendix derivation is not used.',heading='Section 3.3 — Wasserstein gradient flow (3.18)',context='the following theorem gives a concise characterization of the Wasserstein gradient flow.')
add(15,'gradient flow',r'''We follow their approach and define the gradient flow of $\ell_N$ with respect to a suitable geometry with geodesic distance $d(\cdot,\cdot)$ over the space of probability measures as
\[
\partial_t\rho_t=\lim_{\eta\to0}\frac{\rho_t^\eta-\rho_t}{\eta},
\]
where
\[
\rho_t^\eta:=\operatorname*{argmin}_{\rho\in\mathcal P(\mathbb R^d)}\left\{\int_{\mathbb R^d}\delta\ell_N(\rho_t)d(\rho-\rho_t)+\frac1{2\eta}d^2(\rho,\rho_t)\right\}
\]
Given a distance, the existence of a limiting absolutely continuous curve $(\rho_t)_{t\geq0}$ is an important and central question that we omit in this overview.''',[4],[4,9],[r'\rho_t^\eta',r'd^2(\rho,\rho_t)'],'The source formal linearized proximal construction parameterized by a geodesic distance. Its measure-derivative limit topology, minimizer selection and existence are not specified; this is not a certified well-posed construction.',heading='Section 3.1 — Gradient flow over a metric space')
add(16,'Fisher-Rao distance',r'''The Fisher-Rao distance is linked to reaction equations of the form
\[
\partial_t\rho_t=\rho_t\left(\alpha_t-\int\alpha_td\rho_t\right),
\]
(3.1)
where $\alpha_t(x)\in\mathbb R$ is a scalar that governs how much mass is created at $x\in\mathbb R^d$ and time $t$. It is easy to see that these dynamics preserve the total mass 1 of probability distributions. Among all such curves that link $\rho_0$ to $\rho_1$, the Fisher-Rao geodesic is the one that minimizes the total length. More specifically, the Fisher-Rao distance $d_{\mathrm{FR}}$ is defined as (Bauer et al., 2016),
\[
d_{\mathrm{FR}}^2(\rho_0,\rho_1)=\inf\left\{\int_0^1\int\left[\left(\alpha_t-\int\alpha_td\rho_t\right)^2\right]d\rho_tdt:(\rho_t,\alpha_t)_{t\in[0,1]}\text{ solves }\partial_t\rho_t=\rho_t\left(\alpha_t-\int\alpha_td\rho_t\right)\right\}.
\]
(3.2)''',[4],[4,8],[r'd_{\mathrm{FR}}^2',r'\alpha_t-\int\alpha_td\rho_t'],'Probability-preserving reaction action with a centered reaction field. Endpoints are fixed by the preceding prose. The subsequent Hellinger formula is retained separately as an unresolved source assertion rather than silently replacing this definition.',heading='Section 3.1 — Fisher-Rao distance (3.1)–(3.2)')
add(17,'Wasserstein distance',r'''Given two probability measures $\rho_0,\rho_1\in\mathcal P(\mathbb R^d)$, the (quadratic) Wasserstein distance between $\rho_0$ and $\rho_1$ is defined as (Villani, 2009)
\[
d_{\mathrm W}^2(\rho_0,\rho_1)=\inf_{\pi\in\Pi(\rho_0,\rho_1)}\int\|x-y\|_2^2\pi(dx,dy),
\]
where the infimum is taken over all couplings of $\rho_0$ and $\rho_1$.

It also admits a geodesic distance interpretation by means of the Benamou-Brenier formula:
\[
d_{\mathrm W}^2(\rho_0,\rho_1)=\inf\left\{\int_0^1\int\|v_t\|^2d\rho_tdt:(\rho_t,v_t)_{t\in[0,1]}\text{ solves }\partial_t\rho_t=-\operatorname{div}(\rho_tv_t)\right\}.
\]
(3.3)
Here admissible curves are given by the continuity equation
\[
\partial_t\rho_t=-\operatorname{div}(\rho_tv_t),
\]
(3.4)
which describes the evolution of a density of particles in $\mathbb R^d$ evolving according to time-dependent vector field $v_t:\mathbb R^d\to\mathbb R^d$.''',[5],[4,8],[r'd_{\mathrm W}^2',r'\Pi(\rho_0,\rho_1)'],'Quadratic coupling cost and the stated dynamic action, with endpoint and admissibility conventions inherited from the geometric discussion. The displayed domain is all probability measures, so finiteness is not automatic.',heading='Section 3.1 — Wasserstein distance (3.3)–(3.4)')
add(18,'Wasserstein-Fisher-Rao distance',r'''In turn, the Wasserstein-Fisher-Rao distance $d_{\mathrm{WFR}}$ is defined as (Chizat et al., 2018; Gallouët and Monsaingeon, 2017; Kondratyev et al., 2016; Liero et al., 2018)
\[
d_{\mathrm{WFR}}^2(\rho_0,\rho_1)=\inf\left\{\int_0^1\int\left[\|v_t\|^2+\left(\alpha_t-\int\alpha_td\rho_t\right)^2\right]d\rho_tdt:(\rho_t,v_t,\alpha_t)_{t\in[0,1]}\text{ solves }\partial_t\rho_t=-\operatorname{div}(\rho_tv_t)+\rho_t\left(\alpha_t-\int\alpha_td\rho_t\right)\right\}.
\]
(3.5)''',[5],[4,8],[r'd_{\mathrm{WFR}}^2',r'\alpha_t-\int\alpha_td\rho_t'],'Transport-plus-centered-reaction action on probability measures. Its formula does not require either component distance as an input, despite the explanatory description as a composite geometry.',heading='Section 3.1 — Wasserstein-Fisher-Rao distance (3.5)')

# Source-inspected rendering amendment; see the explicit saved review plan.
members['D17']['highlight_symbols'] = ['d_{\\mathrm W}^2', '\\inf_{\\pi\\in\\Pi(\\rho_0,\\rho_1)}']

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,data in [('source-passages.json',dict(paper_id=PID,status='extracted',scope='Original main-text likelihood, measure conventions, updates, flows and geometric definitions.',source_passages=list(members.values()))),('interface-extraction.json',dict(paper_id=PID,status='extracted',interfaces=interfaces))]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(members)} source entries; see the separate paper audit for validation status.')
if __name__=='__main__':main()
