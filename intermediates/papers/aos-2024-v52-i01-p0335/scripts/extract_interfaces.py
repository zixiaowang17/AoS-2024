"""Transcribe statement prerequisites from the inspected pinned preprint, without supplements."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
interfaces=[];members={};edges={}
def add(lid,term,body,pages,heading,deps=None,*,kind='definition',symbols=(),phrases=(),context=None,note=None,shape):
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,
        statement_original=body.strip(),relation='exact',depends_on=list(deps or {}),
        evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=list(symbols),highlight_phrases=list(phrases))
    if note:m['variant_note']=note
    terms=term if isinstance(term,list) else [term];keywords=[]
    for t in terms:
        key=dict(paper_id=PID,local_id=lid,source_text=t,label=t[0].upper()+t[1:],kind='term')
        if t not in body:
            assert context and t in context,(lid,t)
            m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])];key['context_id']=lid+'/name'
        keywords.append(key)
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=' · '.join(k['label'] for k in keywords),
        lean_role='hypothesis' if kind in ('condition','assumption') else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}

def scope(lids,text,pages,heading):
    for lid in lids:
        members[lid]['source_scope_original']=dict(text=text,evidence=[dict(page=p,location=heading) for p in pages])
        members[lid]['statement_original']=text+'\n\n'+members[lid]['statement_original']
        members[lid]['excerpt_selection']='Original parent assumption header followed by this subclause; other numbered subclauses are preserved in separate members.'
        for p in pages:
            record=dict(page=p,location=heading)
            if record not in members[lid]['evidence']:members[lid]['evidence'].append(record)

add('D1','Kullback-Leibler (KL) divergence',r'''
For two probability distributions $\mathrm P_1\in\mathcal P(\mathbb X)$ and $\mathrm P_2\in\mathcal P(\mathbb X)$, we denote by $\operatorname{KL}(\mathrm P_1,\mathrm P_2)$ the Kullback-Leibler (KL) divergence from $\mathrm P_2$ to $\mathrm P_1$, which is defined by $\operatorname{KL}(\mathrm P_1,\mathrm P_2):=\int\log(\frac{d\mathrm P_1}{d\mathrm P_2})d\mathrm P_1$ if $\mathrm P_1\ll\mathrm P_2$ and $\operatorname{KL}(\mathrm P_1,\mathrm P_2):=\infty$ otherwise. For simplicity, we slightly abuse a notation to denote $\operatorname{KL}(\boldsymbol\alpha_1,\boldsymbol\alpha_2):=\operatorname{KL}(\operatorname{Cat}(\boldsymbol\alpha_1),\operatorname{Cat}(\boldsymbol\alpha_2))$ for any $\boldsymbol\alpha_1,\boldsymbol\alpha_2\in\Delta_m$ and any $m\in\mathbb N$, where $\operatorname{Cat}(\boldsymbol\alpha)$ stands for the categorical distribution with probability vector $\boldsymbol\alpha$.
''',[4],'Section 1.1 — Kullback-Leibler divergence',phrases=['Kullback-Leibler (KL) divergence'],symbols=[r'\operatorname{KL}'],shape='Extended-real KL integral with first measure as integrating measure and infinity outside absolute continuity; categorical probability-vector shorthand retained.')
add('D2',['statistical experiment','likelihood'],r'''
We describe our setup for a statistical experiment, which, in this paper, is defined as a pair of a sample space and a set of some distributions on the sample space. For each sample size $n\in\mathbb N$, suppose that we observe a $\mathbb Y_n$-valued sample $\mathbf Y^{(n)}$, where $\mathbb Y_n$ is a measurable sample space equipped with a reference $\sigma$-finite measure $\mu_n$. We then model the sample as having a distribution $\mathrm P_{\boldsymbol\lambda}^{(n)}\in\mathcal P(\mathbb Y_n)$ determined by a natural parameter $\boldsymbol\lambda$ in a measurable natural parameter space $\Lambda_n$. The natural parameter space can be infinite-dimensional, for instance, see Example 1 below, where the natural parameter space is given as the space of density functions. We assume that there exists a nonnegative function $\mathrm p_n:\Lambda_n\times\mathbb Y_n\mapsto\mathbb R_{\geq0}$, called a likelihood (function), such that, for every parameter $\boldsymbol\lambda\in\Lambda_n$, $\int_{\mathbb Y_n}\mathrm p_n(\boldsymbol\lambda,\mathbf y^{(n)})d\mu_n(\mathbf y^{(n)})=1$ and
\[
\mathrm P_{\boldsymbol\lambda}^{(n)}(d\mathbf y^{(n)})=\mathrm p_n(\boldsymbol\lambda,\mathbf y^{(n)})\mu_n(d\mathbf y^{(n)})\tag{2.1}
\]
for any $\mathbf y^{(n)}\in\mathbb Y_n$. We denote by $\mathcal P(\mathbb Y_n;\mathrm p_n,\Lambda_n)$ the set of all distributions of the form (2.1).
''',[4,5],'Section 2.1 — statistical experiment and likelihood',kind='source_passage',phrases=['statistical experiment','likelihood'],symbols=[r'\mathrm P_{\boldsymbol\lambda}^{(n)}'],shape='Dominated statistical experiment indexed by a measurable natural parameter, with normalized likelihood relative to a sigma-finite reference measure. No iid structure is assumed in this general experiment.')
add('D3',['model space','natural parameterization map'],r'''
With a countable set of model indices $\mathcal M_n$ that we call a model space, we consider a collection of probability models $\{\mathcal P_{n,m}\}_{m\in\mathcal M_n}$ for estimation based on the sample $\mathbf Y^{(n)}$, where each model is of the form
\[
\mathcal P_{n,m}:=\left\{\mathrm P_{\mathrm T(\boldsymbol\theta)}^{(n)}\in\mathcal P(\mathbb Y_n;\mathrm p_n,\Lambda_n):\boldsymbol\theta\in\Theta_{n,m}\right\}
\]
with a parameter space $\Theta_{n,m}$ and a measurable map $\mathrm T:\bigcup_{m\in\mathcal M_n}\Theta_{n,m}\mapsto\Lambda_n$ called a natural parameterization map. For simplicity, we let $\Theta_{n,\mathcal M_n}:=\bigcup_{m\in\mathcal M_n}\Theta_{n,m}$. The map $\mathrm T$ may depend on the sample size $n$ but we do not specify the subscript $n$ to this for brevity. We refer to “submodels” $\{\mathcal P_{n,m}\}_{m\in\mathcal M_n}$ as individual models or simply models.

In order to obtain computational tractability (see Section 2.3), we assume that the parameter spaces $\{\Theta_{n,m}\}_{m\in\mathcal M_n}$ are disjoint.
''',[5],'Section 2.1 — model spaces and natural parameterization',{'D2':'Each model is a subset of the dominated experiment indexed through T.'},kind='source_passage',phrases=['model space','natural parameterization map'],symbols=[r'\Theta_{n,m}',r'\mathrm T'],shape='Countable family of disjoint parameter spaces and measurable map into the natural parameter space. Images under T need not be disjoint and T need not be injective.')
add('D4','hierarchical prior distribution',r'''
Following the idea of the use of a hierarchical prior on model and parameter spaces suggested in the previous studies on Bayesian adaptation [Lember and van der Vaart, 2007, Ghosal et al., 2008, Gao et al., 2020, Han, 2021], we consider a hierarchical prior distribution $\Pi_n$ on the entire parameter space $\Theta_{n,\mathcal M_n}$, which is of the form
\[
\Pi_n=\sum_{m\in\mathcal M_n}\alpha_{n,m}\Pi_{n,m},\tag{2.4}
\]
where $\boldsymbol\alpha_n:=(\alpha_{n,m})_{m\in\mathcal M_n}\in\Delta_{|\mathcal M_n|}$ and $\Pi_{n,m}\in\mathcal P(\Theta_{n,m})$ for each $m\in\mathcal M_n$. As $\Pi_n(\boldsymbol\theta\in\Theta_{n,m})=\sum_{m\in\mathcal M_n}\alpha_{n,m}\Pi_{n,m}(\boldsymbol\theta\in\Theta_{n,m})=\alpha_{n,m}$, the term $\alpha_{n,m}$ represents the prior probability of a model $m\in\mathcal M_n$.
''',[7],'Section 2.2 — hierarchical prior, equation (2.4)',{'D3':'Prior components are supported on the disjoint local parameter spaces.'},phrases=['hierarchical prior distribution'],symbols=[r'\alpha_{n,m}',r'\Pi_{n,m}'],shape='Mixture prior with a probability vector of model weights and probability measures on the individual spaces. No rate or particular weight formula is required to define it.')
add('D5','posterior distribution',r'''
The (original) posterior distribution induced from the prior in (2.4) is given by
\[
d\Pi_n(\boldsymbol\theta\mid\mathbf Y^{(n)}):=\frac{\mathrm p_n(\mathrm T(\boldsymbol\theta),\mathbf Y^{(n)})d\Pi_n(\boldsymbol\theta)}{\int\mathrm p_n(\mathrm T(\boldsymbol\theta),\mathbf Y^{(n)})d\Pi_n(\boldsymbol\theta)}.\tag{2.5}
\]
''',[7],'Section 2.2 — original posterior, equation (2.5)',{'D4':'The posterior updates the hierarchical prior.','D2':'The update uses the normalized statistical likelihood.','D3':'The likelihood is evaluated at the natural parameter T(theta).'},phrases=['posterior distribution'],symbols=[r'\Pi_n(\boldsymbol\theta\mid\mathbf Y^{(n)})'],shape='Bayesian likelihood update of the prior, with its marginal-likelihood normalizer retained; no unprinted zero-normalizer convention.')
add('D6','variational family',r'''
Instead of exactly computing the posterior $\Pi_n(\cdot\mid\mathbf Y^{(n)})$, here we seek the closest distribution, denoted by $\widehat Q_n$, to the posterior among a variational family $\mathcal Q_n\subset\mathcal P(\Theta_{n,\mathcal M_n})$ of “hierarchical” distributions given by
\[
\mathcal Q_n:=\left\{\sum_{m\in\mathcal M_n}\gamma_{n,m}Q_{n,m}:(\gamma_{n,m})_{m\in\mathcal M_n}\in\Delta_{|\mathcal M_n|},Q_{n,m}\in\mathcal Q_{n,m}\right\},\tag{2.6}
\]
where $\mathcal Q_{n,m}\subset\mathcal P(\Theta_{n,m})$ is a predefined set of some distributions over the individual model $m\in\mathcal M_n$.
''',[7],'Section 2.2 — hierarchical variational family, equation (2.6)',{'D3':'The mixture family combines supplied families supported on the individual parameter spaces.'},phrases=['variational family'],symbols=[r'\mathcal Q_n',r'\mathcal Q_{n,m}'],shape='All model mixtures of distributions in the supplied individual families, with arbitrary simplex weights. This definition does not fix an optimizer or a concrete application family.')
add('D7','variational posterior',r'''
That is, we consider the variational posterior defined as
\[
\widehat Q_n\in\operatorname*{argmin}_{Q\in\mathcal Q_n}\operatorname{KL}\left(Q,\Pi_n(\cdot\mid\mathbf Y^{(n)})\right).\tag{2.7}
\]
''',[7],'Section 2.2 — variational posterior, equation (2.7)',{'D1':'The objective is the KL divergence from an approximating distribution to the original posterior.','D5':'The target of the approximation is the Bayesian posterior.','D6':'Optimization ranges over the hierarchical variational family.'},phrases=['variational posterior'],symbols=[r'\widehat Q_n'],shape='Any minimizing distribution in the specified family; optimization attainment and a measurable choice are not supplied by an explicit algorithm in this definition.')
add('D8','evidence lower bound (ELBO)',r'''
We define
\[
\mathcal E_n(Q,\Pi,\mathrm p_n):=-\int\log\mathrm p_n(\mathrm T(\boldsymbol\theta),\mathbf Y^{(n)})dQ(\boldsymbol\theta)+\operatorname{KL}(Q,\Pi)\tag{2.8}
\]
for any distributions $Q,\Pi\in\mathcal P(\Theta_{n,\mathcal M_n})$, where we suppress the dependence on the natural parametrization map $\mathrm T$ and the sample $\mathbf Y^{(n)}$ for simplicity.
''',[7,8],'Section 2.2 — negative ELBO, equation (2.8)',{'D1':'The objective contains KL(Q,Pi).','D3':'The likelihood is composed with the natural parameterization T.','D2':'The statistical likelihood is the input p_n.'},context=r'The negative of the function $\mathcal E_n$ is called the evidence lower bound (ELBO) in the related literature, which is named after the property that the ELBO is a lower bound of the log marginal likelihood, i.e., $\log\mathrm p_{n,\Pi}(\mathbf Y^{(n)})\geq-\mathcal E_n(Q,\Pi,\mathrm p_n)$.',symbols=[r'\mathcal E_n'],shape='Negative expected log likelihood plus KL to a supplied prior; E_n is the negative of the ELBO, not the ELBO itself.')
add('D9','individual variational posterior',r'''
\[
\widehat Q_{n,m}\in\operatorname*{argmin}_{Q\in\mathcal Q_{n,m}}\mathcal E_n(Q,\Pi_{n,m},\mathrm p_n)\tag{2.11}
\]
''',[8],'Theorem 2.1 — individual variational posterior, equation (2.11)',{'D8':'The local posterior minimizes the negative ELBO functional.','D4':'Its prior input is the model-specific Pi_n,m.','D6':'Its admissible distributions are the supplied individual family Q_n,m.'},kind='theorem_excerpt',context=r'Furthermore, since each individual variational posterior is computed separately, the adaptive variational Bayes procedure is easily parallelizable.',symbols=[r'\widehat Q_{n,m}'],shape='Individual-model negative-ELBO minimizer, explicitly bound in Theorem 2.1 and consumed by Theorem 3.1.')
add('D10','Testing',r'''
There exist a test function $\phi_{n,m}:\mathbb Y_n\mapsto[0,1]$ such that
\[
\max\left\{\mathrm P_{\boldsymbol\lambda^\star}^{(n)}[\phi_{n,m}],\sup_{\boldsymbol\theta\in\Theta_{n,m}:\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq J_0\zeta}\mathrm P_{\mathrm T(\boldsymbol\theta)}^{(n)}[1-\phi_{n,m}]\right\}\leq\exp(-\mathfrak c_1n\zeta^2)\tag{3.2}
\]
for any $\zeta>\zeta_{n,m}\geq n^{-1/2}$.
''',[11],'Assumption A1 (Testing)',{'D2':'The two testing errors use the data distributions of the experiment.','D3':'The alternatives range over one parameter space mapped through T.'},kind='assumption',context='Testing',phrases=['Assumption A1'],symbols=[r'\zeta_{n,m}'],shape='Uniform exponentially small testing errors outside a metric ball within each individual model, with constants and quantifiers supplied by the Assumption A header.')
add('D11','Prior and variational family',r'''
There exists a distribution $Q^*_{n,m}\in\mathcal Q_{n,m}$ such that
\[
\operatorname{KL}(Q^*_{n,m},\Pi_{n,m})+Q^*_{n,m}\left[\operatorname{KL}\left(\mathrm P_{\boldsymbol\lambda^\star}^{(n)},\mathrm P_{\mathrm T(\boldsymbol\theta)}^{(n)}\right)\right]\leq\mathfrak c_2n(\eta_{n,m}+\zeta_{n,m})^2.\tag{3.3}
\]
''',[11],'Assumption A2 (Prior and variational family)',{'D1':'The condition controls a sum of parameter-space and sampling-distribution KL divergences.','D4':'The first KL term uses the individual prior.','D6':'The witnessing distribution must belong to the individual variational family.'},kind='assumption',context='Prior and variational family',phrases=['Assumption A2'],symbols=[r'\eta_{n,m}',r'Q^*_{n,m}'],shape='Existence of a model-wise approximating distribution satisfying the joint KL budget; independent of the testing condition A1.')
scope(['D10','D11'],r'There exist absolute constants $J_0>0$, $\mathfrak c_1>0$ and $\mathfrak c_2>0$ such that the following hold for any $\boldsymbol\lambda^\star\in\Lambda_n^\star$, any $m\in\mathcal M_n$ and any sufficiently large $n\in\mathbb N$.',[11],'Assumption A header')
add('D12','oracle rate',r'''
\[
\varepsilon_n:=\varepsilon_n(\mathcal M_n):=\inf_{m\in\mathcal M_n}(\eta_{n,m}+\zeta_{n,m}).\tag{3.5}
\]
''',[12],'Section 3.2 — oracle rate, equation (3.5)',{'D3':'The infimum ranges over the model index set.'},context=r'for inference, which contracts at an oracle rate defined as',symbols=[r'\varepsilon_n'],shape='Infimum of the supplied approximation-plus-estimation errors over models. The same formula is reused with the errors of E2; it does not by itself impose A1 or A2.')
add('D13','Model space',r'''
The cardinality of the model space $\mathcal M_n$ is bounded as
\[
|\mathcal M_n|\leq\exp(\mathfrak c_3n\varepsilon_n^2).\tag{3.6}
\]
''',[12],'Assumption B1 (Model space)',{'D3':'This is a bound on the supplied countable model index set.','D12':'The bound uses the oracle rate from equation (3.5).'},kind='assumption',context='Model space',phrases=['Assumption B1'],shape='Model-count upper bound at the oracle rate, with absolute constants and eventual-n scope from Assumption B.')
add('D14','Prior model probabilities: regularization',r'''
The prior model probabilities $\boldsymbol\alpha_n:=(\alpha_{n,m})_{m\in\mathcal M_n}\in\Delta_{|\mathcal M_n|}$ satisfies
\[
\sum_{m\in\mathcal M_n:\zeta_{n,m}\geq H\varepsilon_n}\alpha_{n,m}\leq\exp(-\mathfrak c_4n(H\varepsilon_n)^2)\tag{3.7}
\]
for any $H>H_0$.
''',[12],'Assumption B2 (Prior model probabilities: regularization)',{'D4':'The left side sums prior model probabilities over high-complexity models.','D12':'The complexity threshold and exponential budget use the oracle rate.'},kind='assumption',context='Prior model probabilities: regularization',phrases=['Assumption B2'],shape='Exponential prior tail on models whose estimation error exceeds H times the oracle rate; not imposed by the ivB theorems or quasi-posterior results.')
add('D15','Prior model probabilities: concentration',r'''
There exists a model $m_n^*\in\mathcal M_n$ such that $\eta_{n,m_n^*}+\zeta_{n,m_n^*}\leq(1+\mathfrak c_5)\varepsilon_n$ and
\[
\alpha_{n,m_n^*}\geq\exp(-\mathfrak c_6n\varepsilon_n^2).\tag{3.8}
\]
''',[12],'Assumption B3 (Prior model probabilities: concentration)',{'D4':'The near-optimal model must receive sufficient prior model probability.','D12':'Near-optimality and the mass budget use the oracle rate.'},kind='assumption',context='Prior model probabilities: concentration',phrases=['Assumption B3'],shape='At least one near-oracle model with sufficient prior mass; it does not impose a prior tail on other models.')
scope(['D13','D14','D15'],r'There exist absolute constants $H_0>1$ and $\mathfrak c_3,\ldots,\mathfrak c_6>0$ such that the following hold for any sufficiently large $n\in\mathbb N$.',[12],'Assumption B header')
add('D16','variational approximation gap',r'''
\[
\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\operatorname{KL}\left(\widehat Q_n,\Pi_n(\cdot\mid\mathbf Y^{(n)})\right)\right]\lesssim n\varepsilon_n^2.\tag{3.1}
\]
''',[10],'Section 3 — variational approximation gap, equation (3.1)',{'D1':'The gap is measured by KL divergence.','D7':'Its first argument is the adaptive variational posterior.','D5':'Its target is the original posterior.'},kind='condition',context='bound the variational approximation gap by an upper bound of an appropriate order as',symbols=[r'\operatorname{KL}'],shape='Expected posterior-approximation KL bound at a supplied rate; this is the referenced conclusion of Theorem 3.3, not a new assumption on every contraction theorem.')
add('D17','overly complex',r'''
We define
\[
\mathcal M_n^{\mathrm{over}}(H):=\{m\in\mathcal M_n:\zeta_{n,m}\geq H\varepsilon_n\}\tag{3.13}
\]
for $H>1$, which is the set of models whose estimation errors are somewhat larger than the oracle rate, that is, the models that are overly complex.
''',[14],'Section 3.3 — overly complex models, equation (3.13)',{'D12':'The estimation-error threshold is measured in units of the oracle rate.'},phrases=['overly complex'],symbols=[r'\mathcal M_n^{\mathrm{over}}'],shape='Models above an estimation-error threshold; this is distinct from the ivB-penalty threshold set.')
add('D18','less expressive models',r'''
Define
\[
\mathcal M_n^{\mathrm{under}}(\eta^*;\boldsymbol\lambda^\star):=\left\{m\in\mathcal M_n:\inf_{\boldsymbol\theta\in\Theta_{n,m}}\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq\eta^*\right\}\tag{3.15}
\]
for $\eta^*>0$ and $\boldsymbol\lambda^\star\in\Lambda_n^\star$, which is the set of less expressive models that cannot approximate the true parameter $\boldsymbol\lambda^\star$ accurately.
''',[15],'Section 3.3 — less expressive models, equation (3.15)',{'D3':'Expressibility is the infimum of metric distance over the natural image of each local parameter space.'},phrases=['less expressive models'],symbols=[r'\mathcal M_n^{\mathrm{under}}'],shape='Models separated from the true parameter by at least a supplied metric approximation gap. No beta-min condition is built into this general definition.')

add('D19',['nested','combinatorial'],r'''
1. We say that a model space $\mathcal M_n$ is nested or has a nested structure if $\mathcal M_n$ is a subset of $\mathbb N^q$ for some $q\in\mathbb N$.
2. We say that a model space $\mathcal S_n$ is combinatorial or has a combinatorial structure if $\mathcal S_n$ is the powerset of some subset $\bar S$ of $\mathbb N$, i.e., $\mathcal S_n=\mathbb P(\bar S):=\{S:S\subset\bar S\}$.
''',[5],'Definition 1 (Model spaces)',phrases=['nested','combinatorial'],shape='Author-defined model-index structures: a subset of a finite Cartesian power of N, or a powerset. Nested here does not assert inclusion of the statistical distributions.')
add('D20','parameter space',r'''
Let $\mathcal M_n$ and $\mathcal S_n$ be nested and combinatorial model spaces, respectively, and let $\Theta_{n,m,S}$ be an individual parameter space indexed by $m\in\mathcal M_n$ and $S\in\mathcal S_n$. If computationally tractable, we can conduct variational optimization over a “merged” parameter space $\Theta_{n,m}:=\bigcup_{S\in\mathcal S_n}\Theta_{n,m,S}$ for each $m\in\mathcal M_n$, instead of every $\Theta_{n,m,S}$. By doing so, we have the adaptive variational posterior of the same form as in (2.10).
''',[19],'Section 5.1 — merged parameter spaces',{'D19':'The construction combines a nested index and a combinatorial index.','D3':'The merged spaces serve as the individual parameter spaces of the general construction.'},symbols=[r'\Theta_{n,m,S}'],shape='Merge all combinatorial support cells for each nested index before variational optimization. The conditional prior decomposition is retained as a separate source passage below.')
add('D21','conditional prior model probabilities',r'''
For ease of description, we write
\[
\Pi_{n,m}=\sum_{S\in\mathcal S_n}\alpha_{n,S\mid m}\Pi_{n,m,S}
\]
with $\alpha_{n,S\mid m}:=\Pi_{n,m}(\Theta_{n,m,S})$ and $\Pi_{n,m,S}(\cdot):=\Pi_{n,m}(\cdot\mid\Theta_{n,m,S})$.

for every $m\in\mathcal M_n$.
''',[19],'Section 5.1 — conditional prior decomposition',{'D20':'The prior is decomposed over the combinatorial parameter cells within each merged model.','D4':'Pi_n,m is the individual prior in the hierarchy.'},context=r'We expect that the conditional prior model probabilities $(\alpha_{n,S\mid m})_{m\in\mathcal M_n,S\in\mathcal S_n}$ penalize overly dense models with large complexities.',symbols=[r'\alpha_{n,S\mid m}'],shape='Conditional prior weights and prior restrictions to combinatorial cells, with no supplied convention for conditional distributions on zero-mass cells.')
add('D22','Testing',r'''
There exist a test function $\phi_{n,m,S}:\mathbb Y_n\mapsto[0,1]$ such that
\[
\max\left\{\mathrm P_{\boldsymbol\lambda^\star}^{(n)}[\phi_{n,m,S}],\sup_{\boldsymbol\theta\in\Theta_{n,m,S}:\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq J_0\zeta}\mathrm P_{\mathrm T(\boldsymbol\theta)}^{(n)}[1-\phi_{n,m,S}]\right\}\leq\exp(-\mathfrak c_1n\zeta^2)\tag{5.1}
\]
for any $\zeta>\zeta_{n,m,S}\geq n^{-1/2}$.
''',[20],'Assumption D1 (Testing)',{'D20':'Testing alternatives are restricted to a single (m,S) cell, rather than the full merged model.','D2':'The error probabilities use the underlying sampling experiment.'},kind='assumption',context='Testing',phrases=['Assumption D1'],shape='Cell-specific exponential testing errors with the common quantifiers and constants from Assumption D.')
add('D23','Prior and variational family',r'''
There exists a distribution $Q^*_{n,m}\in\mathcal Q_{n,m}$ such that
\[
\operatorname{KL}(Q^*_{n,m},\Pi_{n,m})+Q^*_{n,m}\left[\operatorname{KL}\left(\mathrm P_{\boldsymbol\lambda^\star}^{(n)},\mathrm P_{\mathrm T(\boldsymbol\theta)}^{(n)}\right)\right]\leq\mathfrak c_2n\inf_{S\in\mathcal S_n}(\eta_{n,m,S}+\zeta_{n,m,S})^2.\tag{5.2}
\]
''',[20],'Assumption D2 (Prior and variational family)',{'D1':'The approximation budget consists of two KL terms.','D20':'The witness lives on a merged parameter space and the budget optimizes over combinatorial cells.','D4':'The witness is compared with the individual prior.','D6':'The witness belongs to the individual variational family over that merged model.'},kind='assumption',context='Prior and variational family',phrases=['Assumption D2'],shape='Merged-model variational witness with budget controlled by the best combinatorial approximation/estimation error; it does not assume D1.')
add('D24','contraction rate',r'''
Now define
\[
\varepsilon_n:=\varepsilon_n(\mathcal M_n\times\mathcal S_n):=\inf_{(m,S)\in\mathcal M_n\times\mathcal S_n}(\eta_{n,m,S}+\zeta_{n,m,S}).\tag{5.3}
\]
''',[20],'Section 5.1 — rate over the combinatorial model space, equation (5.3)',{'D20':'The rate optimizes over both nested and combinatorial model indices.'},context=r'A potential problem of this strategy from a theoretical perspective is that the complexity of the merged parameter space $\Theta_{n,m}$ may be excessively large in high-dimensional settings, so we may fail to obtain a good contraction rate.',symbols=[r'\varepsilon_n'],shape='Oracle approximation-plus-estimation rate over pairs (m,S), distinct from the one-index rate in equation (3.5).')
members['D24']['naming_context'][0]['text']='A potential problem of this strategy from a theoretical perspective is that the complexity of the merged parameter space $\Theta_{n,m}$ may be excessively large in high-dimensional settings, so we may fail to obtain a good contraction rate.'
members['D24']['naming_context'][0]['evidence']=[dict(page=19,location='Section 5.1 paragraph before Assumption D')]
add('D25','Model space and prior model probabilities',r'''
The model space $\mathcal M_n\times\mathcal S_n$, prior model probabilities $(\alpha_{n,m})_{m\in\mathcal M_n}$ and conditional prior model probabilities $(\alpha_{n,S\mid m})_{m\in\mathcal M_n,S\in\mathcal S_n}$ satisfy
\[
\left|\{(m,S)\in\mathcal M_n\times\mathcal S_n:\zeta_{n,m,S}\leq H\varepsilon_n\}\right|\leq\exp(\mathfrak c_3n(H\varepsilon_n)^2),\tag{5.4}
\]
\[
\sum_{(m,S)\in\mathcal M_n\times\mathcal S_n:\zeta_{n,m,S}\geq H\varepsilon_n}\alpha_{n,m}\alpha_{n,S\mid m}\leq\exp(-\mathfrak c_4n(H\varepsilon_n)^2)\tag{5.5}
\]
for any $H>H_0$. Moreover, there exists a model $(m_n^*,S_n^*)\in\mathcal M_n\times\mathcal S_n$ such that $\eta_{n,m_n^*,S_n^*}+\zeta_{n,m_n^*,S_n^*}\leq(1+\mathfrak c_5)\varepsilon_n$ and
\[
\alpha_{n,m_n^*}\alpha_{n,S_n^*\mid m_n^*}\geq\exp(-\mathfrak c_6n\varepsilon_n^2).\tag{5.6}
\]
''',[20],'Assumption D3 (Model space and prior model probabilities)',{'D21':'The bounds use products of nested-model weights and conditional combinatorial weights.','D24':'Every complexity threshold and mass budget uses the pair-index oracle rate.'},kind='assumption',context='Model space and prior model probabilities',phrases=['Assumption D3'],shape='Three distinct bounds: count of low-complexity cells, prior tail on high-complexity cells, and sufficient mass near the oracle; preserve all inequalities and quantifiers.')
scope(['D22','D23','D25'],r'There exist absolute constants $J_0>0$, $H_0>1$ and $\mathfrak c_1,\ldots,\mathfrak c_6>0$ such that the following hold for any $\boldsymbol\lambda^\star\in\Lambda_n^\star$, any $m\in\mathcal M_n$, $S\in\mathcal S_n$ and any sufficiently large $n\in\mathbb N$.',[19],'Assumption D header')

add('D26','neural network (function)',r'''
For a positive integer $K\in\mathbb N_{\geq2}$ larger than 1 and a $(K+1)$-dimensional vector of positive integers $\mathbf M_{1:(K+1)}:=(M_1,\ldots,M_{K+1})\in\mathbb N^{K+1}$, we denote $\widehat\Theta_{\mathbf M_{1:(K+1)}}:=\bigotimes_{k=1}^K(\mathbb R^{M_{k+1}\times M_k}\times\mathbb R^{M_{k+1}})$. For a network parameter $\boldsymbol\theta=((\mathbf W_k,\mathbf b_k))_{k\in[K]}\in\widehat\Theta_{\mathbf M_{1:(K+1)}}$, we define the neural network (function) $\operatorname{net}(\boldsymbol\theta):\mathbb R^{M_1}\mapsto\mathbb R^{M_{K+1}}$ induced by the network parameter $\boldsymbol\theta$ as
\[
\operatorname{net}(\boldsymbol\theta):\mathbf x\mapsto[\mathbf W_K,\mathbf b_K]\circ\operatorname{ReLU}\circ[\mathbf W_{K-1},\mathbf b_{K-1}]\circ\cdots\circ\operatorname{ReLU}\circ[\mathbf W_1,\mathbf b_1]\mathbf x,
\]
where $[\mathbf W_k,\mathbf b_k]:\mathbf x'\mapsto\mathbf W_k\mathbf x'+\mathbf b_k$ denotes the affine transformation represented as a multiplication by the weight matrix $\mathbf W_k$ and an addition of the bias vector $\mathbf b_k$ and $\operatorname{ReLU}:\mathbf x'\mapsto\mathbf x'\vee\mathbf0$, does the elementwise ReLU (rectified linear unit) activation function. Since we focus on the estimation of real-valued functions supported on $[0,1]^d$, we only consider network parameters in $\Theta^d:=\bigcup_{K=2}^\infty\bigcup_{\mathbf M_{1:(K+1)}\in\mathbb N^{K+1}:M_1=d,M_{K+1}=1}\widehat\Theta_{\mathbf M_{1:(K+1)}}$, the set of network parameters with input and output dimensions being $d$ and 1, respectively.
''',[15,16],'Section 4.1 — neural network function',phrases=['neural network (function)'],symbols=[r'\operatorname{net}',r'\operatorname{ReLU}'],shape='Composition of K affine layers with coordinatewise ReLU between them and no final ReLU; retain layer dimensions and scalar-output input-cube convention.')
add('D27','network architecture',r'''
In the application of adaptive variational Bayes to deep learning, we consider multiple disjoint parameter spaces indexed by the number of hidden layers $K\in\mathbb N_{\geq2}$ and the number of hidden nodes of each layer $M\in\mathbb N$ such as
\[
\Theta_{(K,M)}:=\Theta^d_{(K,M)}:=\widehat\Theta_{(d,M_2,\ldots,M_K,1)}\text{ with }M_2=\cdots=M_K=M.\tag{4.1}
\]
We refer to $K$ and $M$ as (network) depth and width, respectively, and further, a pair $(K,M)$ as a network architecture. We denote by $J_{(K,M)}$ the dimension of the space $\Theta_{(K,M)}$, i.e.,
\[
J_{(K,M)}:=(d+1)M+(K-2)(M^2+M)+(M+1).
\]
Since $\Theta_{(K,M)}\cong\mathbb R^{J_{(K,M)}}$, we can deal with each member in the parameter space $\Theta_{(K,M)}$ as a $J_{(K,M)}$-dimensional real vector. For a technical reason (see Remark 5 below), we restrict network parameters to be bounded. For a given magnitude bound $B>0$, define
\[
\Theta^{\leq B}_{(K,M)}:=\Theta^{d,\leq B}_{(K,M)}:=\{\boldsymbol\theta\in\Theta^d_{(K,M)}:|\boldsymbol\theta|_\infty\leq B\}.\tag{4.2}
\]
In our collection of neural network models, we let each parameter space be of the form $\Theta^{\leq B_n}_{(K,M)}$ for each $n\in\mathbb N$, where the sequence of magnitude bounds $(B_n)_{n\in\mathbb N}\subset\mathbb R_{\geq0}$ is a positive sequence that diverges at a suitable rate.
''',[16],'Section 4.1 — network architecture and bounded parameters',{'D26':'The architecture fixes the layer sizes of the neural network parameter tuple.'},phrases=['network architecture'],symbols=[r'\Theta^{\leq B}_{(K,M)}',r'\Theta_{(K,M)}^{\leq B_n}'],shape='Fixed hidden width and depth with componentwise parameter bound; preserve the printed layer-count wording and dimension formula.')
add('D28','prior distribution',r'''
We describe our prior and variational family for neural networks. Let $\mathcal M_n\subset\mathbb N_{\geq2}\times\mathbb N$ be a set of some network architectures to be considered in consequent inference tasks. We impose the prior distribution
\[
\Pi_n=\sum_{(K,M)\in\mathcal M_n}\alpha_{n,(K,M)}\Pi_{n,(K,M)},\text{ where}\quad\Pi_{n,(K,M)}:=\operatorname{Unif}(-B_n,B_n)^{\otimes J_{(K,M)}}\text{ and }\alpha_{n,(K,M)}:=\frac{e^{-\mathfrak a_0(KM)^2\log n}}{\sum_{(K',M')\in\mathcal M_n}e^{-\mathfrak a_0(K'M')^2\log n}}\tag{4.3}
\]
for $\mathfrak a_0>0$.
''',[16],'Section 4.1 — neural-network prior, equation (4.3)',{'D27':'The component dimension and uniform parameter bound are determined by the network architecture.','D4':'The application specifies the components and weights of the hierarchical prior.'},phrases=['prior distribution'],symbols=[r'\operatorname{Unif}(-B_n,B_n)'],shape='Uniform product prior on each bounded network parameter space, mixed with exponential depth-width weights independent of the truth.')
add('D29','variational family',r'''
For each network architecture $(K,M)\in\mathcal M_n$, we consider the variational family given by
\[
\mathcal Q_{n,(K,M)}:=\left\{\bigotimes_{j=1}^{J_{(K,M)}}\operatorname{Unif}(-\psi_{1,j},\psi_{2,j}):-B_n\leq\psi_{1,j}<\psi_{2,j}\leq B_n\right\}.\tag{4.4}
\]
''',[16],'Section 4.1 — neural-network variational family, equation (4.4)',{'D27':'The product has one factor per network parameter and retains the bound B_n.'},phrases=['variational family'],symbols=[r'\operatorname{Unif}(-\psi_{1,j},\psi_{2,j})'],note='The source writes a negative first endpoint in Unif(-psi_1,j,psi_2,j) but bounds psi_1,j<psi_2,j. This possible sign inconsistency is preserved.',shape='Printed product of uniform distributions with the exact source endpoint constraints; do not silently remove the minus sign or add an interval-validity constraint.')
add('D30','nonparametric regression experiment',r'''
In this subsection, we consider a nonparametric regression experiment with standard Gaussian errors. In this case, we observe $n$ independent outputs $\mathbf Y^{(n)}:=(Y_1,\ldots,Y_n)\in\mathbb Y_n:=\mathbb R^n$, where each $Y_i$ is associated with a fixed $d$-dimensional input $\mathbf x_i$ that has been rescaled so that $\mathbf x_i\in[0,1]^d$. We model the sample $\mathbf Y^{(n)}$ using a probability model $\mathcal P(\mathbb R^n;\mathrm p_n^{\mathrm{Ga}},\mathcal F^d)$ with a likelihood function $\mathrm p_n^{\mathrm{Ga}}:\mathcal F^d\times\mathbb R^n\mapsto\mathbb R_{\geq0}$ defined as
\[
\mathrm p_n^{\mathrm{Ga}}(f,\mathbf Y^{(n)})=\mathrm p_n^{\mathrm{Ga}}(f,\mathbf Y^{(n)};(\mathbf x_i)_{i\in[n]})=\prod_{i=1}^ng_{\mathrm N(0,1)}(Y_i-f(\mathbf x_i))\text{ for }f\in\mathcal F^d,\tag{4.5}
\]
where $g_{\mathrm N(0,1)}$ stands for the density function of the standard Gaussian distribution. Here, we assume that the variance of the output distribution is fixed to be 1 for technical simplicity, however, we can easily extend this to an unknown variance case. We denote by $\mathrm P_f^{(n)}$ the distribution that has the density function $\mathrm p_n(f,\cdot)$.
''',[17],'Section 4.2 — Gaussian nonparametric regression',kind='source_passage',phrases=['nonparametric regression experiment'],shape='Independent Gaussian unit-variance responses at fixed inputs in the unit cube; no random-design or unknown-variance assumption is imported into Theorem 4.1.')
add('D31','empirical L2 distance',r'''
Assuming that $\mathbf Y^{(n)}\sim\mathrm P_{f^\star}^{(n)}$ for some true regression function $f^\star\in\mathcal F^d$, our aim is to accurately estimate $f^\star$ in terms of the empirical $\mathcal L^2$ distance defined as
\[
\|f_0-f_1\|_{n,2}=\left(\frac1n\sum_{i=1}^n(f_0(\mathbf x_i)-f_1(\mathbf x_i))^2\right)^{1/2}\text{ for }f_0,f_1\in\mathcal F^d.
\]
''',[17],'Section 4.2 — empirical L2 distance',context='empirical L2 distance',phrases=['distance'],symbols=[r'\|f_0-f_1\|_{n,2}',r'\|\operatorname{net}(\boldsymbol\theta)-f^\star\|_{n,2}'],shape='Root mean squared function discrepancy over fixed observed design points; a seminorm on functions, not population integrated L2 loss.')

members['D31']['naming_context'][0]['typesetting_note']='Natural-language label normalizes the source mathematical typography in empirical L^2 distance; the original source phrase and formula remain in statement_original.'

add('D32','factor model',r'''
Consider a factor model, where a $d_n$-dimensional real-valued sample $\mathbf Y^{(n)}:=(\mathbf Y_1,\ldots,\mathbf Y_n)\in\mathbb Y_n:=(\mathbb R^{d_n})^{\otimes n}$ of size $n$ is assumed to follow a distribution $\mathrm P_{\boldsymbol\Sigma}^{(n)}:=\bigotimes_{i=1}^n\mathrm N(\mathbf0_{d_n},\boldsymbol\Sigma)$ with a covariance matrix given by
\[
\boldsymbol\Sigma=\mathrm T(\mathbf L):=\mathbf L\mathbf L^\top+\mathbf I_{d_n}\in\mathbb S_{++}^{d_n}
\]
for a factor loading matrix $\mathbf L\in\mathbb R^{d_n\times m}$ and the factor dimensionality $m\in\mathbb N$.
''',[6],'Example 3 (Sparse factor model) — sampling model',kind='source_passage',phrases=['factor model'],symbols=[r'\mathrm T(\mathbf L)',r'\mathbf L\mathbf L^\top'],shape='Iid centered multivariate Gaussian observations with covariance LL-transpose plus identity; loading dimension m is the factor-model index.')
add('D33','“row” support',r'''
For a matrix $\mathbf L=(L_{j,k})_{j\in[d_n],k\in[m]}\in\mathbb R^{d_n\times m}$, let $\mathbf L_{j,:}:=(L_{j,k})_{k\in[m]}$ be the $j$-th row of $\mathbf L$ for $j\in[d_n]$ and we denote the “row” support of $\mathbf L$ by
\[
\operatorname{supp}(\mathbf L):=\{j\in[d_n]:|\mathbf L_{j,:}|_0>0\}.
\]
''',[6],'Example 3 — row support',phrases=['“row” support'],symbols=[r'\operatorname{supp}(\mathbf L)'],shape='Indices of nonzero rows of a loading matrix, rather than entrywise support or number of nonzero columns.')
add('D34','parameter spaces',r'''
Given an upper bound $m_{\max}\in\mathbb N$ of the factor dimensionality, we consider parameter spaces defined as
\[
\Theta_{n,m,S}:=\{\mathbf L\in\mathbb R^{d_n\times m}:\operatorname{supp}(\mathbf L)=S\}.
\]
for each $m\in[m_{\max}]$ and $S\subset[d_n]$, which are disjoint. Note that the model space $[m_{\max}]\times\mathbb P([d_n])$ has both nested and combinatorial structures and its cardinality $m_{\max}2^{d_n}$ is exponential in the dimension $d_n$ of the sample.
''',[7],'Example 3 — exact-support loading spaces',{'D33':'Each cell fixes exactly the row-support set of the loading matrix.'},phrases=['parameter spaces'],symbols=[r'\Theta_{n,m,S}'],shape='Loading matrices with exact row support S and m columns. Within an m model, all support cells are merged for variational optimization.')
add('D35','spike-and-slab prior distribution',r'''
To appropriately address the sparse structure of the loading matrix, we impose a spike-and-slab prior distribution on the loading matrix $\mathbf L\in\mathbb R^{d_n\times m}$ conditional on $m\in\mathcal M_n$. Concretely, we assume
\[
\Pi_n=\sum_{m\in\mathcal M_n}\alpha_{n,m}\Pi_{n,m},\quad\text{where }\alpha_{n,m}:=1/|\mathcal M_n|\quad\text{and }\Pi_{n,m}:=\{(1-\omega_{n,m})\delta(\cdot;\mathbf0_m)+\omega_{n,m}\mathrm N(\mathbf0_m,\tau_0\mathbf I_m)\}^{\otimes d_n}\text{ with }\omega_{n,m}:=d_n^{-(1+\mathfrak a_0)m}\tag{5.10}
\]
for given constants $\tau_0>0$ and $\mathfrak a_0>0$.
''',[21],'Section 5.2.1 — sparse-factor prior, equation (5.10)',{'D4':'The model prior is a hierarchy with uniform factor-dimensionality weights.','D34':'The rowwise mixture is supported on the union of exact-support loading spaces.'},phrases=['spike-and-slab prior distribution'],symbols=[r'\omega_{n,m}'],shape='Independent row spikes at zero and Gaussian slabs of covariance tau_0 I_m, with the dimension-dependent slab probability and uniform weights on m.')
add('D36','variational family of spike-and-slab distributions',r'''
For each model index $m\in\mathcal M_n$, we consider a variational family of spike-and-slab distributions such as
\[
\mathcal Q_{n,m}:=\left\{\bigotimes_{j=1}^{d_n}\{(1-\nu_j)\delta(\cdot;\mathbf0_m)+\nu_j\mathrm N(\boldsymbol\psi_j,\boldsymbol\Phi_j)\}:\boldsymbol\psi_j\in\mathbb R^m,\boldsymbol\Phi_j\in\mathbb S_{++}^m,\nu_j\in[0,1]\right\}.
\]
''',[21],'Section 5.2.1 — sparse-factor variational family',{'D34':'The distributions range over loading matrices of a given column dimension and varying row support.'},phrases=['variational family of spike-and-slab distributions'],symbols=[r'\nu_j',r'\boldsymbol\Phi_j'],shape='Independent row spike-and-slab distributions with arbitrary Gaussian row means, positive-definite within-row covariances and inclusion probabilities; not an entrywise diagonal Gaussian family.')
add('D37',['operator norm','singular values'],r'''
For a $d\times m$-dimensional matrix $\mathbf L$, we denote the operator norm of the matrix $\mathbf L$ by $\|\mathbf L\|_{\mathrm{op}}$, that is, $\|\mathbf L\|_{\mathrm{op}}:=\sup_{\mathbf x\in\mathbb R^m:|\mathbf x|_2=1}|\mathbf L\mathbf x|_2$. Let $\sigma_1(\mathbf L)\geq\cdots\geq\sigma_{d\wedge m}(\mathbf L)$ be the ordered singular values of $\mathbf L$.
''',[21],'Section 5.2.2 — operator norm and ordered singular values',phrases=['operator norm','singular values'],symbols=[r'\|\mathbf L\|_{\mathrm{op}}',r'\sigma_1'],shape='Euclidean matrix operator norm and descending singular-value notation, used for covariance loss and spectral restrictions; no Frobenius norm substitution.')
add('D38','true covariance matrix',r'''
Let $r_n\in\mathbb N$ be the true factor dimensionality and $s_n\in[d_n]$ be the row sparsity of the true loading matrix. We assume that $s_n\geq r_n$ throughout this section because, if not, the rank of the true loading matrix is less than $r_n$ and the estimation of the factor dimensionality is not meaningful anymore. We assume that the true covariance matrix belongs to a set defined as
\[
\Lambda_n^\star:=\{\mathrm T(\mathbf L)\in\mathbb S_{++}^{d_n}:\mathbf L\in\mathbb R^{d_n\times r_n},|\operatorname{supp}(\mathbf L)|\leq s_n,\sigma_1(\mathbf L\mathbf L^\top)\leq\bar\sigma\}
\]
with some fixed $\bar\sigma>0$.
''',[21],'Section 5.2.2 — class of true covariance matrices',{'D32':'The covariance is the natural image LL-transpose plus identity of a loading matrix.','D33':'The sparsity bound counts nonzero rows.','D37':'The class bounds the largest singular value of LL-transpose.'},kind='condition',phrases=['true covariance matrix'],symbols=[r'\Lambda_n^\star'],shape='True covariance class with at most s_n active rows, r_n loading columns and bounded top signal eigenvalue; no lower signal eigenvalue is imposed here.')
add('D39','additional conditions',r'''
Under the following additional conditions on the true covariance matrix,
\[
\Lambda_n^\star(\eta^*):=\left\{\mathrm T(\mathbf L)\in\Lambda_n^\star:\min\left\{\sigma_{r_n}(\mathbf L\mathbf L^\top),\min_{j\in\operatorname{supp}(\mathbf L)}|\mathbf L_{j,:}|_2^2\right\}\geq\eta^*\right\},\tag{5.12}
\]
for $\eta^*>0$, the adaptive variational posterior can nearly consistently estimate the true factor dimensionality $r_n$ and sparsity $s_n$.
''',[22],'Section 5.2.2 — additional signal conditions, equation (5.12)',{'D38':'This is a restricted subset of the original covariance truth class.','D33':'The inner minimum is over nonzero loading rows.','D37':'The spectral condition bounds the r_n-th singular value of the signal covariance from below.'},kind='condition',phrases=['additional conditions'],symbols=[r'\Lambda_n^\star(\eta^*)'],shape='Joint lower bounds on the r_n-th signal eigenvalue and squared norm of each active loading row. These conditions enter Theorem 5.3 only.')
add('D40','same assumptions',r'''
Assume that $s_nr_n\log d_n=o(n)$, $s_n\geq r_n$ and $\log d_n\gtrsim\log n$. Then if $\mathcal M_n=[m_{\max,n}]$ with $r_n\leq m_{\max,n}\leq n$,
''',[21],'Theorem 5.2 — assumptions imported by Theorem 5.3',kind='theorem_excerpt',context='Suppose that the same assumptions as in Theorem 5.2 hold.',phrases=['Theorem 5.2'],shape='The exact rate and model-index restrictions explicitly imported by Theorem 5.3; neither the covariance bound conclusion nor a proof of Theorem 5.2 is treated as a premise.')
members['D40']['naming_context'][0]['evidence']=[dict(page=22,location='Theorem 5.3 opening')]
interfaces[-1]['lean_role']='hypothesis'
add('D41','implicit variational Bayes penalty',r'''
\[
\Psi_{n,m}:=\sup_{\widetilde\Pi\in\mathcal P(\Theta_{n,m})}\inf_{Q\in\mathcal Q_{n,m}}\{\operatorname{KL}(Q,\Pi_{n,m})-\operatorname{KL}(Q,\widetilde\Pi)\}.\tag{6.1}
\]
This, we call the implicit variational Bayes penalty (ivB penalty) for a model $m\in\mathcal M_n$, can be viewed as a penalty that is “implicitly” imposed by the variational Bayes procedure to that model, in the sense that this is not explicitly specified by an user unlike the prior penalty $-\log(\alpha_{n,m})$ used in the previous sections.
''',[22],'Section 6 — implicit variational Bayes penalty, equation (6.1)',{'D1':'The minimax functional takes differences of two KL divergences.','D4':'The first KL target is the model-specific prior.','D6':'The infimum is over the specified individual variational family.'},phrases=['implicit variational Bayes penalty'],symbols=[r'\Psi_{n,m}'],shape='Supremum over auxiliary priors of an infimum of KL differences. The order of extrema is essential; the definition is independent of the likelihood and model prior weight.')
add('D42','ivB penalties',r'''
\[
\mathcal M_n^{\mathrm{ivB,over}}(A):=\{m\in\mathcal M_n:\Psi_{n,m}\geq An\varepsilon_n^2\},\tag{6.2}
\]
which is a set of models with substantially large ivB penalties.
''',[23],'Section 6 — models with large ivB penalties, equation (6.2)',{'D41':'Membership is determined by the implicit variational Bayes penalty.','D12':'The threshold is A times n times the squared oracle rate.'},phrases=['ivB penalties'],symbols=[r'\mathcal M_n^{\mathrm{ivB,over}}'],shape='Models whose ivB penalty exceeds An epsilon_n squared, distinct from the estimation-error threshold set M_over.')
add('D43','maximal complexity',r'''
Theorem 6.1 enables us to focus on a “sieve” $\mathcal M_n^{\mathrm{ivB,regular}}(A_n):=\mathcal M_n\setminus\mathcal M_n^{\mathrm{ivB,over}}(A_n)$ of appropriate complexity when we analyze the contraction behavior. The contraction rate is then determined by the maximal complexity $\zeta_n^\ddagger$ of the models in the sieve $\mathcal M_n^{\mathrm{ivB,regular}}(A_n)$, which is given as
\[
\zeta_n^\ddagger:=\max_{m\in\mathcal M_n^{\mathrm{ivB,regular}}(A_n)}\zeta_{n,m}=\max_{m\in\mathcal M_n:\Psi_{n,m}<A_nn\varepsilon_n^2}\zeta_{n,m},\tag{6.4}
\]
as shown in the next theorem.
''',[23],'Section 6 — maximal complexity of the ivB sieve, equation (6.4)',{'D42':'The sieve excludes the large-ivB-penalty model set.'},phrases=['maximal complexity'],symbols=[r'\zeta_n^\ddagger'],shape='Maximum estimation complexity over models below the strict ivB-penalty threshold; the given sequence A_n controls both this sieve and the theorem threshold.')

add('D44','quasi-posterior',r'''
For a given quasi-likelihood function $\mathrm p_n^\natural:\Lambda_n\times\mathbb Y_n\mapsto\mathbb R_{\geq0}$, the quasi-posterior given the sample $\mathbf Y^{(n)}\in\mathbb Y_n$ is defined as
\[
d\Pi_n^\natural(\boldsymbol\theta\mid\mathbf Y^{(n)}):=\frac{\mathrm p_n^\natural(\mathrm T(\boldsymbol\theta),\mathbf Y^{(n)})d\Pi_n(\boldsymbol\theta)}{\int\mathrm p_n^\natural(\mathrm T(\boldsymbol\theta),\mathbf Y^{(n)})d\Pi_n(\boldsymbol\theta)}.\tag{7.1}
\]
''',[24],'Section 7.1 — quasi-posterior, equation (7.1)',{'D4':'The quasi-likelihood updates the same hierarchical prior.','D3':'It is evaluated at the natural parameter T(theta).'},phrases=['quasi-posterior'],symbols=[r'\Pi_n^\natural'],shape='Normalized prior update using a supplied nonnegative quasi-likelihood; no normalization over the sample space is required of that quasi-likelihood.')
add('D45','adaptive variational quasi-posterior',r'''
Given a variation family $\mathcal Q_n\subset\mathcal P(\Theta_{n,\mathcal M_n})$, we define an adaptive variational quasi-posterior $\widehat Q_n^\natural$ by
\[
\begin{aligned}
\widehat Q_n^\natural&\in\operatorname*{argmin}_{Q\in\mathcal Q_n}\operatorname{KL}(Q,\Pi_n^\natural(\cdot\mid\mathbf Y^{(n)}))\\
&=\operatorname*{argmin}_{Q\in\mathcal Q_n}\left\{\mathcal E_n(Q,\Pi_{n,m},\mathrm p_n^\natural):=-\int\log\mathrm p_n^\natural(\mathrm T(\boldsymbol\theta),\mathbf Y^{(n)})dQ(\boldsymbol\theta)+\operatorname{KL}(Q,\Pi_n)\right\}.
\end{aligned}\tag{7.2}
\]
''',[25],'Section 7.1 — adaptive variational quasi-posterior, equation (7.2)',{'D1':'The quasi-posterior is approximated in KL divergence.','D44':'The target is the original quasi-posterior, not the ordinary posterior.','D6':'The adaptive approximation uses the hierarchical variational family.'},phrases=['adaptive variational quasi-posterior'],symbols=[r'\widehat Q_n^\natural'],note='The objective argument is printed as Pi_n,m while the KL term is KL(Q,Pi_n); both source symbols are preserved.',shape='KL projection onto the hierarchical family, with the source alternative negative-quasi-log-likelihood objective retained exactly, including its prior-subscript discrepancy.')
add('D46','Quasi-likelihood',r'''
For any $\boldsymbol\lambda\in\Lambda_n$, the quasi-likelihood $\mathrm p_n^\natural:\Lambda_n\times\mathbb Y_n\mapsto\mathbb R_{\geq0}$ satisfies
\[
\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\frac{\mathrm p_n^\natural(\boldsymbol\lambda,\mathbf Y^{(n)})}{\mathrm p_n^\natural(\boldsymbol\lambda^\star,\mathbf Y^{(n)})}\right]\leq e^{-\mathfrak c_1n\mathcal d_n^2(\boldsymbol\lambda,\boldsymbol\lambda^\star)},\tag{7.6}
\]
\[
\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\left(\frac{\mathrm p_n^\natural(\boldsymbol\lambda^\star,\mathbf Y^{(n)})}{\mathrm p_n^\natural(\boldsymbol\lambda,\mathbf Y^{(n)})}\right)^\rho\right]\leq e^{\mathfrak c_2n\mathcal d_n^2(\boldsymbol\lambda,\boldsymbol\lambda^\star)}.\tag{7.7}
\]
''',[25],'Assumption E1 (Quasi-likelihood)',{'D2':'Expectations are under the actual sampling distribution, rather than a law normalized from the quasi-likelihood.'},kind='assumption',context='Quasi-likelihood',phrases=['Assumption E1'],symbols=[r'\mathrm p_n^\natural',r'\rho'],shape='Two moment bounds for forward quasi-likelihood ratios and powered inverse ratios, with rho>0 and the full Assumption E scope. This is not a standard normalized-likelihood assumption.')
add('D47','Prior and variational family',r'''
There exists a distribution $Q^*_{n,m}\in\mathcal Q_{n,m}$ such that
\[
\operatorname{KL}(Q^*_{n,m},\Pi_{n,m})+Q^*_{n,m}\left[n\mathcal d_n^2(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\right]\leq\mathfrak c_3n(\eta_{n,m}+\zeta_{n,m})^2.\tag{7.8}
\]
''',[25],'Assumption E2 (Prior and variational family)',{'D1':'The parameter-space approximation budget contains KL to the prior.','D4':'Pi_n,m is the individual prior.','D6':'The witness must belong to the individual variational family.','D3':'The squared metric loss is evaluated after the natural parameterization.'},kind='assumption',context='Prior and variational family',phrases=['Assumption E2'],shape='A KL-plus-n-times-squared-metric approximation budget; distinguish it from A2, whose second summand is a sampling-distribution KL.')
add('D48','Prior model probabilities',r'''
There exists a model $m_n^*\in\mathcal M_n$ such that $\eta_{n,m_n^*}+\zeta_{n,m_n^*}\leq(1+\mathfrak c_4)\varepsilon_n$ and $\alpha_{n,m_n^*}\geq\exp(-\mathfrak c_5n\varepsilon_n^2)$, where $\varepsilon_n$ is the oracle rate defined in (3.5).
''',[25],'Assumption E3 (Prior model probabilities)',{'D4':'A near-optimal model must receive enough prior model probability.','D12':'The one-index oracle-rate formula (3.5) is reused with the errors appearing in E2.'},kind='assumption',context='Prior model probabilities',phrases=['Assumption E3'],shape='Prior mass on one near-oracle model; no separate cardinality bound or prior tail is required by Assumption E.')
scope(['D46','D47','D48'],r'There exist absolute constants $\mathfrak c_1,\ldots,\mathfrak c_5>0$ and $\rho>0$ such that the followings hold for any $\boldsymbol\lambda^\star\in\Lambda_n^\star$, any $m\in\mathcal M_n$ and any sufficiently large $n\in\mathbb N$.',[25],'Assumption E header')
add('D49','variational approximation gap',r'''
\[
\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\operatorname{KL}(\widehat Q_n^\natural,\Pi_n^\natural(\cdot\mid\mathbf Y^{(n)}))\right]\lesssim n\varepsilon_n^2\tag{7.5}
\]
''',[25],'Section 7.2 — variational approximation gap, equation (7.5)',{'D1':'The gap is measured by KL divergence.','D45':'The approximation is the adaptive variational quasi-posterior.','D44':'The target is the original quasi-posterior.'},kind='condition',context='bound the variational approximation gap as',symbols=[r'\widehat Q_n^\natural'],shape='Expected KL gap to a quasi-posterior at a supplied rate; referenced by the last clause of Theorem 7.1 and distinct from the ordinary-posterior gap (3.1).')

# Source-inspected selector amendment; original statements are unchanged.
members['D28']['highlight_symbols'] = ['\\operatorname{Unif}(-B_n,B_n)^{\\otimes J_{(K,M)}}']

def main():
 for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('interface-draft.json',interfaces)]:
  (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(f'Saved {len(interfaces)} source interfaces (draft extraction; not a completed census).')
if __name__=='__main__':main()
