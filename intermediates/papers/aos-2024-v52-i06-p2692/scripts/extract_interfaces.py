"""Preserve original stereographic sampler definitions and theorem assumptions."""
import json,hashlib
from save_inventory import ROOT,PID,STATEMENTS
REVIEW_ROOT=ROOT
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
add(1,'stereographic projection',r'''Let $\mathbb S^d$ denote the unit sphere in $\mathbb R^{d+1}$ centered at the origin. A stereographic projection describes a bijection from $\mathbb S^d\setminus\{(0,\ldots0,1)\}$ to $\mathbb R^d$. Within this paper, we shall restrict attention to projections indexed by a single parameter $R\in\mathbb R^+$ and described by the mapping
\[
x=\mathrm{SP}(z):=\left(R\frac{z_1}{1-z_{d+1}},\ldots,R\frac{z_d}{1-z_{d+1}}\right)^T,
\]
with Jacobian determinant at $x\in\mathbb R^d$ satisfying
\[
J_{\mathrm{SP}}(x)\propto(R^2+\|x\|^2)^d,\tag{2}
\]
and inverse $\mathrm{SP}^{-1}:\mathbb R^d\to\mathbb S^d\setminus\{(0,\ldots0,1)\}$ given by
\[
z_i=\frac{2Rx_i}{\|x\|^2+R^2},\quad\forall1\le i\le d,\qquad z_{d+1}=\frac{\|x\|^2-R^2}{\|x\|^2+R^2}.\tag{3}
\]''',[5,6],[],[r'\mathrm{SP}(z)',r'\mathrm{SP}^{-1}',r'\mathbb S^d'],'The original radius-indexed map, inverse and proportional Jacobian between Euclidean space and the unit sphere without its north pole. The radius scales the map, not the sphere.','Section 2.1 — Stereographic projection (2)–(3)')
add(2,'transformed target',r'''We denote the transformed target as $\pi_S(z)$ then for $x=\mathrm{SP}(z)$ we have
\[
\pi_S(z)\propto\pi(x)(R^2+\|x\|^2)^d.\tag{4}
\]''',[6],[1],[r'\pi_S(z)'],'Transformed target density evaluated through the original stereographic projection. It is used explicitly by SBPS; the SPS algorithm instead prints its acceptance ratio directly.','Section 2.1 — Transformed target (4)')
add(3,'Stereographic Projection Sampler',r'''• Let the current state be $X^d(t)=x$;
• Compute the proposal $\widehat X$:
– Let $z:=\mathrm{SP}^{-1}(x)$;
– Sample independently $\mathrm d\widetilde z\sim\mathcal N(0,h^2I_{d+1})$;
– Let $\mathrm dz:=\mathrm d\widetilde z-\frac{(z^T\cdot\mathrm d\widetilde z)z}{\|z\|^2}$ and $\widehat z:=\frac{z+\mathrm dz}{\|z+\mathrm dz\|}$;
– The proposal $\widehat X:=\mathrm{SP}(\widehat z)$.
• $X^d(t+1)=\widehat X$ with probability $1\wedge\frac{\pi(\widehat X)(R^2+\|\widehat X\|^2)^d}{\pi(x)(R^2+\|x\|^2)^d}$; otherwise $X^d(t+1)=x$.''',[6],[1],[r'\widehat X:=\mathrm{SP}(\widehat z)',r'X^d(t+1)'],'Full Algorithm1, including tangent Gaussian proposal, normalization and accept/reject step. This original sampler is separate from the coordinate-spliced RSPS.','Algorithm 1 — Stereographic Projection Sampler (SPS)',kind='source_passage',context='Algorithm 1: Stereographic Projection Sampler (SPS)')
add(4,'uniformly ergodic',r'''Recall that a Markov chain $X$ on state space $E$ with transition kernel $P$ is uniformly ergodic if $\forall\epsilon>0$, there exists, $N\in\mathbb N$ such that $\|P^N(x,\cdot)-\pi\|_{\mathrm{TV}}\le\epsilon,\forall x\in E$, where $\pi$ denotes the chain's (unique) invariant distribution and $\|\cdot\|_{\mathrm{TV}}$ represents total variation distance.''',[7],[],[r'\|P^N(x,\cdot)-\pi\|_{\mathrm{TV}}'], 'Discrete-time uniform ergodicity with a time N common to all starting states. Preserve the source punctuation; do not replace with geometric ergodicity.','Section 2.1 — Uniform ergodicity of a Markov chain',phrases=['uniformly ergodic'])
add(5,'Stereographic Bouncy Particle Sampler',r'''• Initialize $z^{(0)}\in\mathbb S^d$ and $v^{(0)}$ such that $v^{(0)}\cdot z^{(0)}=0$ and $\|v^{(0)}\|=1$.
• Simulate BPS on unit sphere: for $i=1,2,\ldots$
– Simulate bounce time $\tau_{\mathrm{bounce}}$ of a Poisson process of intensity
\[
\chi(t)=\lambda(\sin(t)v^{(i-1)}+\cos(t)z^{(i-1)},\cos(t)v^{(i-1)}-\sin(t)z^{(i-1)}),
\]
where
\[
\lambda(z,v):=\max\{0,[-v\cdot\nabla_z\log\pi_S(z)]\}.
\]
– Simulate refreshment time $\tau_{\mathrm{refresh}}\sim\mathrm{Exponential}(\lambda_{\mathrm{refresh}})$.
– Let $\tau_i=\min\{\tau_{\mathrm{bounce}},\tau_{\mathrm{refresh}}\}$ and
\[
z^{(i)}=\sin(\tau_i)v^{(i-1)}+\cos(\tau_i)z^{(i-1)}.
\]
– If $\tau_i=\tau_{\mathrm{refresh}}$, sample new $v^{(i)}$ independently
\[
v^{(i)}\sim\mathrm{Uniform}\{v:z^{(i)}\cdot v=0,\|v\|=1\}
\]
– If $\tau_i=\tau_{\mathrm{bounce}}$, compute
\[
v^{(i)}=v_{\mathrm{temp}}-2\left[\frac{v_{\mathrm{temp}}\cdot\widetilde\nabla_z\log\pi_S(z^{(i)})}{\widetilde\nabla_z\log\pi_S(z^{(i)})\cdot\widetilde\nabla_z\log\pi_S(z^{(i)})}\right]\widetilde\nabla_z\log\pi_S(z^{(i)}),
\]
where
\[
v_{\mathrm{temp}}=\cos(\tau_i)v^{(i-1)}-\sin(\tau_i)z^{(i-1)}
\]
\[
\widetilde\nabla_z\log\pi_S(z^{(i)})=\nabla_z\log\pi_S(z^{(i)})-\left[z^{(i)}\cdot\nabla_z\log\pi_S(z^{(i)})\right]z^{(i)}.
\]
– If $\sum_{j=1}^i\tau_j\ge T$ (where $T$ is some constant time), exit.
• Return $x=\mathrm{SP}(z)$ where $z$ denotes BPS on unit sphere.''',[8],[1,2],[r'\lambda(z,v)',r'\tau_{\mathrm{refresh}}',r'\widetilde\nabla_z\log\pi_S(z^{(i)})'],'Full printed SBPS algorithm with great-circle flow, bounce hazard, constant-rate refreshment and tangent reflection. Preserve source stopping convention and record unresolved gradient-zero, north-pole and velocity-domain conventions separately.','Algorithm 2 — Stereographic Bouncy Particle Sampler (SBPS)',kind='source_passage',context='Algorithm 2: Stereographic Bouncy Particle Sampler (SBPS)')
add(6,'uniformly ergodic',r'''For a Markov process $X$ with state space $E$, transition semi-group $P$, and invariant distribution $\pi$, it is uniformly ergodic if $\forall\epsilon>0$ there exists $T$ such that $\|P^T(x,\cdot)-\pi\|_{\mathrm{TV}}\le\epsilon,\forall x\in E$.''',[9],[],[r'\|P^T(x,\cdot)-\pi\|_{\mathrm{TV}}'],'Continuous-time semigroup version, separate from the discrete-time chain definition. Preserve the exact common-time quantifier.','Section 2.2 — Uniform ergodicity of a Markov process',phrases=['uniformly ergodic'])
add(7,'multivariate Gaussian targets',r'''We consider multivariate Gaussian targets with mean vector $\mu$ and covariance matrix $\Sigma$:
\[
\pi_{\mu,\Sigma}(x)\propto\exp\left(-\frac12(x-\mu)^T\Sigma^{-1}(x-\mu)\right),
\]
where
\[
\Sigma=\operatorname{Diag}(\lambda_1,\ldots,\lambda_d),\qquad\mu=(\mu_1,\ldots,\mu_d)^T.
\]
We are interested in the robustness when $\mu\ne0$ and $\Sigma\ne I_d$.''',[14],[],[r'\pi_{\mu,\Sigma}(x)',r'\Sigma=\operatorname{Diag}'],'Original diagonal-covariance Gaussian class for Theorem4.1. Mean and eigenvalue bounds and dimension-uniform constants are bound in the theorem itself. No generalized-projection algorithm is imported.','Section 4.2 — Multivariate Gaussian targets',kind='source_passage')
add(8,'product i.i.d. form',r'''We assume the target $\pi(x)$ has a product i.i.d. form:
\[
\pi(x)=\prod_{i=1}^df(x_i).\tag{12}
\]''',[16],[],[r'\pi(x)=\prod_{i=1}^df(x_i)'],'Original product density across coordinates, with the same marginal f as dimension varies; does not mean independent successive MCMC states.','Section 5.1 — Product target (12)',kind='assumption')
add(9,'normalized',r'''Without loss of generality, we assume $f$ is normalized such that
\[
\mathbb E_f(X^2)=\int x^2f(x)\,\mathrm dx=1,\qquad\mathbb E_f(X^6)<\infty.\tag{13}
\]''',[16],[],[r'\mathbb E_f(X^2)',r'\mathbb E_f(X^6)'],'Second moment equals one and finite sixth moment. No zero-mean condition is printed; a finite sixth moment is a substantive assumption, not achieved by rescaling arbitrary tails.','Section 5.1 — Normalization and moment assumptions (13)',kind='assumption')
add(10,'Lipschitz continuous',r'''We further assume $f'/f$ is Lipschitz continuous, $\lim_{x\to\pm\infty}xf'(x)=0$, and
\[
\mathbb E_f\left[\left(\frac{f'(X)}{f(X)}\right)^8\right]<\infty,\qquad\mathbb E_f\left[\left(\frac{f''(X)}{f(X)}\right)^4\right]<\infty,\qquad\mathbb E_f\left[\left(\frac{Xf'(X)}{f(X)}\right)^4\right]<\infty.\tag{14}
\]''',[16],[],[r"f'/f",r"\lim_{x\to\pm\infty}xf'(x)=0",r"\frac{f''(X)}{f(X)}"],'Complete regularity, boundary and three integrability conditions. The eighth score moment and the fourth second-derivative/weighted-score moments remain distinct.','Section 5.1 — Score regularity and integrability (14)',kind='assumption')
add(11,'full support',r'''In this section, we consider $f$ has full support in $\mathbb R$. ''' , [16],[],[], 'Original full-support section convention. Preserve support versus strict pointwise positivity as an unresolved distinction where ratios require values. The adjacent isotropy assertion is not part of this assumption.','Section 5.1 — Full support',kind='assumption',phrases=['full support'])
add(12,'step size',r'''To simplify the final result, we replace the step size $h$ by another parameter $\ell$ via
\[
h=\frac1{\sqrt{d-1}}\left[\frac1{\left(1-\frac{\ell^2}{2d}\frac{4\lambda}{(1+\lambda)^2}\right)^2}-1\right]^{1/2}\tag{15}
\]
which implies $\frac1{\sqrt{1+h^2(d-1)}}=1-\frac{\ell^2}{2d}\frac{4\lambda}{(1+\lambda)^2}$. Note that $\ell$ is simply a re-parameterization of $h$. When $\ell$ is a fixed constant, $h$ is scaled as $O(d^{-1})$ since $h\approx\frac\ell d\sqrt{4\lambda/(1+\lambda)^2}$.''',[17],[],[r'\frac1{\sqrt{d-1}}',r'\frac{\ell^2}{2d}\frac{4\lambda}{(1+\lambda)^2}'],'Original stepsize reparameterization. The positive square-root branch requires a positive right side in the printed implication and d>1. Fixed ell and lambda make this meaningful eventually. T5.2 uses ell under the continuing section convention without explicitly repeating Eq.(15).','Section 5.2 — Step size (15)')
add(13,'Expected Squared Jumping Distance',r'''Expected Squared Jumping Distance (ESJD):
\[
\mathrm{ESJD}:=\mathbb E_{X\sim\pi}\mathbb E_{\widehat X\mid X}\left[\|\widehat X-X\|^2\left(1\wedge\frac{\pi(\widehat X)(R^2+\|\widehat X\|^2)^d}{\pi(X)(R^2+\|X\|^2)^d}\right)\right].
\]''',[19],[3],[r'\mathrm{ESJD}',r'\|\widehat X-X\|^2'],'Exact joint expectation under the stationary SPS proposal. This is distinct from the product-of-expectations approximation in Eq.(16).','Definition 5.1 — Expected Squared Jumping Distance (ESJD)')
add(14,'Revised Stereographic Projection Sampler',r'''• Let the current state be $X^d(t)=x$;
• Compute the proposal $\widehat X$:
– Let $z:=\mathrm{SP}^{-1}(x)$;
– Sample independently $\mathrm d\widetilde z',\mathrm d\widetilde z''\sim\mathcal N(0,h^2I_{d+1})$;
– Let $\mathrm dz':=\mathrm d\widetilde z-\frac{(z^T\cdot\mathrm d\widetilde z')z}{\|z\|^2}$ and $\mathrm dz'':=\mathrm d\widetilde z-\frac{(z^T\cdot\mathrm d\widetilde z'')z}{\|z\|^2}$;
– Let $\widehat z':=\frac{z+\mathrm dz'}{\|z+\mathrm dz'\|}$ and $\widehat z'':=\frac{z+\mathrm dz''}{\|z+\mathrm dz''\|}$;
– Two independent proposals $\widehat X':=\mathrm{SP}(\widehat z')$ and $\widehat X'':=\mathrm{SP}(\widehat z'')$;
– The proposal $\widehat X:=(\widehat X'_1,\widehat X''_{2:d})$.
• $X^d(t+1)=\widehat X$ with probability $1\wedge\frac{\pi(\widehat X)(R^2+\|\widehat X\|^2)^d}{\pi(x)(R^2+\|x\|^2)^d}$; otherwise $X^d(t+1)=x$.''',[20],[1],[r"\widehat X:=(\widehat X'_1,\widehat X''_{2:d})",r"\mathrm d\widetilde z',\mathrm d\widetilde z''"],'Full printed Algorithm4. Preserve the unprimed d-tilde-z in both tangent-increment leading terms; the source prose states two independent proposals and coordinate splicing. Do not silently repair that discrepancy or attribute this diffusion theorem to SPS.','Algorithm 4 — Revised Stereographic Projection Sampler (RSPS)',kind='source_passage',context='Algorithm 4: Revised Stereographic Projection Sampler (RSPS)')
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D10']['highlight_symbols'] = ["f'/f", "\\lim_{x\\to\\pm\\infty}xf'(x)=0", "\\left(\\frac{f''(X)}{f(X)}\\right)^4"]

def main():
    review=json.loads((REVIEW_ROOT/'inventory-review.json').read_text())
    assert review['status']=='complete' and review['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==review['inventory_sha256']
    assert len(interfaces)==len(members)==14
    for x in interfaces:
        a=x['members'][0];own=a['statement_original']+' '+a['local_label'];assert any(v in own for v in a['highlight_symbols']+a['highlight_phrases'])
        assert set(a['depends_on'])<=set(members)
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved14 original source entries; dependency finalization and full source review remain pending.')
if __name__=='__main__':main()
