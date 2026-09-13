"""Rebuild original main-text passages and local dependencies for this paper.

The saved data is manually transcribed; source audit is a separate stage.
"""
import json
from pathlib import Path
from save_inventory import PID, claims

ROOT = Path(__file__).resolve().parents[1]
interfaces, members, edges = [], {}, {}


def add(lid, term, body, pages, heading, deps=None, *, kind='definition',
        symbols=(), phrases=(), context=None, context_pages=None, shape):
    evidence = [dict(page=p, location=heading) for p in pages]
    member = dict(paper_id=PID, local_id=lid, local_label=heading,
        source_heading=heading, source_kind=kind, statement_original=body.strip(),
        relation='exact', depends_on=list(deps or {}), evidence=evidence,
        highlight_symbols=list(symbols), highlight_phrases=list(phrases))
    keyword = dict(paper_id=PID, local_id=lid, source_text=term,
                   label=term[0].upper()+term[1:], kind='term')
    if term not in body:
        assert context and term in context, (lid, term)
        member['naming_context'] = [dict(context_id=lid+'/name', text=context,
            evidence=[dict(page=p, location=heading+' — naming context') for p in (context_pages or pages)])]
        keyword['context_id'] = lid+'/name'
    interfaces.append(dict(interface_id=PID+'/'+lid, rank_group='all', name=keyword['label'],
        lean_role='hypothesis' if kind in ('condition', 'assumption') else 'definition',
        type_shape=shape, semantic_boundary=shape, members=[member], source_keywords=[keyword],
        central_claim_uses=[], dependencies=[], theorem_explanations={}))
    members[lid] = member
    edges[lid] = deps or {}


add('D1','couplings',r'''
where $\Pi(\mu,\nu)$ is the set of all couplings of $\mu$ and $\nu$, i.e., each $\pi\in\Pi(\mu,\nu)$ is a probability distribution on $\mathcal{X}\times\mathcal{Y}$ that has $\mu$ and $\nu$ as its first and second marginals, respectively.
''',[5],'Section 2.1 — couplings',{},symbols=['\\Pi(\\mu,\\nu)'],shape='A probability law on the product space with the specified two marginals.')

interfaces[-1]["interface_id"]='couplings'

add('D3','Entropic optimal transport',r'''
EOT is a convexification of the classical OT problem by means of an entropic penalty. For a regularization parameter $\varepsilon>0$, EOT is given by

\[
\mathsf{OT}_{c,\varepsilon}(\mu,\nu)\coloneqq\inf_{\pi\in\Pi(\mu,\nu)}\int c\,d\pi+\varepsilon\mathsf{D}_{\mathsf{KL}}(\pi\|\mu\otimes\nu),
\]
(4)
''',[6],'Section 2.1 — entropic optimal transport (4)',{'D1': 'The infimum is over couplings with the fixed marginals.', 'D11': 'The penalty is KL relative to the product of the marginals.'},symbols=['\\mathsf{OT}_{c,\\varepsilon}'],shape='Entropic OT with positive regularization, a possibly negative lower-semicontinuous cost, and KL against the product reference measure.',context='Entropic optimal transport.')

interfaces[-1]["interface_id"]='gw-D3'

add('D4','GW distance',r'''
Towards a complete resolution,
one of our main contributions is to quantify the empirical convergence rate of the $(2,2)$-GW distance between Euclidean mm spaces $(\mathbb{R}^{d_{x}},\|\cdot\|,\mu)$ and $(\mathbb{R}^{d_{y}},\|\cdot\|,\nu)$ of different dimensions. Abbreviating $\Delta^{\mathbb{R}^{d_{x}},\mathbb{R}^{d_{y}}}_{2}=\Delta$, the distance of interest is

\[
\begin{aligned}
\mathsf{D}(\mu,\nu) & \coloneqq\inf_{\pi\in\Pi(\mu,\nu)}\|\Delta\|_{L^{2}(\pi\otimes\pi)} \\ =\inf_{\pi\in\Pi(\mu,\nu)}\left(\int_{\mathbb{R}^{d_{x}}\times\mathbb{R}^{d_{y}}}\int_{\mathbb{R}^{d_{x}}\times\mathbb{R}^{d_{y}}}\big|\|x-x^{\prime}\|^{2}-\|y-y^{\prime}\|^{2}\big|^{2}d\pi\otimes\pi(x,y,x^{\prime},y^{\prime})\right)^{\frac{1}{2}}.
\end{aligned}
\]
(7)

We drop subscripts from our notation because we focus on the $(2,2)$-GW case from here on out. For finiteness we will always assume $\mu\in\mathcal{P}_{4}(\mathbb{R}^{d_{x}})$ and $\nu\in\mathcal{P}_{4}(\mathbb{R}^{d_{y}})$.
''',[7],'Section 2.2 — quadratic Euclidean GW distance (7)',{'D1': 'The quadratic distortion is minimized over couplings.', 'D10': 'The paper explicitly assumes fourth absolute moments for finiteness.'},symbols=['\\mathsf{D}(\\mu,\\nu)'],shape='The (2,2)-GW distance is the square root of the optimized squared distortion. The four-fold product integrand uses squared Euclidean distances in possibly different dimensions.')

interfaces[-1]["interface_id"]='gw-D4'

add('D5','entropic regularization',r'''
We also treat the GW distance with entropic regularization, which, for $\varepsilon>0$, is defined as

\[
\mathsf{S}_{\varepsilon}(\mu,\nu)\coloneqq\inf_{\pi\in\Pi(\mu,\nu)}\|\Delta\|^{2}_{L^{2}(\pi\otimes\pi)}+\varepsilon\mathsf{D}_{\mathsf{KL}}(\pi\|\mu\otimes\nu).
\]
''',[7],'Section 2.2 — entropic regularization of GW',{'D1': 'Optimization is over couplings of the two marginals.', 'D4': 'Delta is the quadratic Euclidean distortion specified in (7), with the paper-wide fourth-moment domain.', 'D11': 'The entropic penalty is KL relative to the product marginal measure.'},symbols=['\\mathsf{S}_{\\varepsilon}(\\mu,\\nu)'],shape='The entropic functional uses squared L2 distortion and no square root; at zero regularization its source convention is D squared. This is not a debiased Sinkhorn divergence.')

interfaces[-1]["interface_id"]='gw-D5'

add('D6','EGW functional',r'''
Next, by expanding the $(2,2)$-GW cost, we split the EGW functional into two terms as

\[
\mathsf{S}_{\varepsilon}(\mu,\nu)=\mathsf{S}^{1}(\mu,\nu)+\mathsf{S}^{2}_{\varepsilon}(\mu,\nu),
\]
(8)

where

\[
\begin{aligned}
\mathsf{S}^{1}(\mu,\nu)\coloneqq\int\|x-x^{\prime}\|^{4}d\mu\otimes\mu(x,x^{\prime})+\int\|y-y^{\prime}\|^{4}d\nu\otimes\nu(y,y^{\prime})-4\int\|x\|^{2}\|y\|^{2}d\mu\otimes\nu(x,y) \\ \mathsf{S}^{2}_{\varepsilon}(\mu,\nu)\coloneqq\inf_{\pi\in\Pi(\mu,\nu)}\int-4\|x\|^{2}\|y\|^{2}d\pi(x,y)-8\sum_{\begin{subarray}{c}1\leq i\leq d_{1}\\
1\leq j\leq d_{2}\end{subarray}}\Big(\intx_{i}y_{j}d\pi(x,y)\Big)^{2}+\varepsilon\mathsf{D}_{\mathsf{KL}}(\pi\|\mu\otimes\nu).
\end{aligned}
\]
''',[8],'Section 3.2 — EGW decomposition (8)',{'D1': 'The second component optimizes over couplings and their mixed moments.', 'D11': 'Its penalty is the source KL divergence.', 'D5': 'The left side is the entropic GW functional.', 'D12': 'The preceding section convention centers both marginals before this decomposition.'},symbols=['\\mathsf{S}^{1}', '\\mathsf{S}^{2}_{\\varepsilon}'],shape='Components S^1 and S_epsilon^2 of the centered decomposition; superscripts are labels, not powers. The second component can be negative. Retain the printed sum indices d1,d2.')

interfaces[-1]["interface_id"]='gw-D6'

add('D7','cost function',r'''
where $\mathsf{OT}_{\mathbf{A},\varepsilon}$ is the EOT problem with cost function $c_{\mathbf{A}}:(x,y)\in\mathbb{R}^{d_{x}}\times\mathbb{R}^{d_{y}}\mapsto-4\|x\|^{2}\|y\|^{2}-32x^{\intercal}\mathbf{A}y$.
''',[9],'Theorem 1 — EOT cost function',{'D3': 'OT_A,epsilon means the EOT problem specialized to the displayed cost.'},symbols=['c_{\\mathbf{A}}'],shape='The theorem binds the explicit quartic/bilinear cost c_A. A ranges over all real dx-by-dy matrices before the attained compact-box restriction.',kind='theorem_excerpt')

interfaces[-1]["interface_id"]='gw-D7'

add('D8','empirical measures',r'''
Let $X_{1},\ldots,X_{n}$ and $Y_{1},\ldots,Y_{n}$ be independently and identically distributed (i.i.d.) samples from $\mu$ and $\nu$, respectively, and denote their empirical measures by $\hat{\mu}_{n}=n^{-1}\sum_{i=1}^{n}\delta_{X_{i}}$ and $\hat{\nu}_{n}=n^{-1}\sum_{i=1}^{n}\delta_{Y_{i}}$.
''',[9],'Section 3.3 — empirical measures',{},symbols=['\\hat{\\mu}_{n}', '\\hat{\\nu}_{n}'],shape='The source specifies iid samples from each population and empirical measures with equal sample size n; preserve its joint sampling wording.')

interfaces[-1]["interface_id"]='gw-D8'

add('D9','sub-Weibull',r'''
A probability distribution $\rho\in\mathcal{P}(\mathbb{R}^{d})$ is called $\beta$-sub-Weibull with parameter $\sigma^{2}$ for $\sigma\geq 0$ if $\int\exp\left(\|x\|^{\beta}/2\sigma^{2}\right)d\rho(x)\leq 2$.
''',[4],'Section 1.4 — sub-Weibull condition',{},symbols=['\\sigma^{2}'],shape='Exponential absolute-norm condition with parameter sigma squared in the denominator. Theorem 2 specializes beta to four and uses a common strictly positive parameter. The definition permits sigma=0 without stating a division-by-zero convention.',kind='condition')

interfaces[-1]["interface_id"]='gw-D9'

add('D10','absolute moment',r'''
For $p\in[1,\infty)$, let $\mathcal{P}_{p}(\mathbb{R}^{d})$ be the space of Borel probability measures with finite $p$-th absolute moment, i.e., $M_{p}(\rho)\coloneqq\int_{\mathbb{R}^{d}}\|x\|^{p}d\rho(x)<\infty$ for any $\rho\in\mathcal{P}_{p}(\mathbb{R}^{d})$.
''',[4],'Section 1.4 — absolute moments',{},symbols=['M_{p}', '\\mathcal{P}_{p}'],shape='Absolute pth moment and the finite-moment probability class, with p in [1,infinity). In Theorem 1 the fourth-moment class and second-moment product have different roles.')

interfaces[-1]["interface_id"]='absolute-moments'

add('D11','KL divergence',r'''
where the KL divergence is given by $\mathsf{D}_{\mathsf{KL}}(\alpha\|\beta)\coloneqq\int\log(d\alpha/d\beta)\,d\alpha$ if $\alpha\ll\beta$, and equals $+\infty$ otherwise.
''',[6],'Section 2.1 — KL divergence',{},symbols=['\\mathsf{D}_{\\mathsf{KL}}'],shape='Extended relative entropy: integral when absolutely continuous, plus infinity otherwise; no truncation or symmetrization.')

interfaces[-1]["interface_id"]='kl-divergence'

add('D12','centered',r'''
Towards the dual form, first observe that $\mathsf S_\varepsilon$ is invariant to isometric operations on the marginal spaces, such as translation and orthonormal rotation. Thus, without loss of generality (w.l.o.g.), we assume that $\mu$ and $\nu$ are centered, i.e., $\int x\,d\mu(x)=\int y\,d\nu(y)=0$.
''',[8],'Section 3.2 — centered marginals',kind='condition',symbols=[r'\int x\,d\mu(x)=\int y\,d\nu(y)=0'],shape='Explicit centering convention for the subsequent dual decomposition. Translation invariance permits recentering but does not make raw moments of uncentered measures interchangeable with centered moments.')
interfaces[-1]['interface_id']='gw-D12'

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source interfaces; full review remains pending.')
if __name__=='__main__':main()
