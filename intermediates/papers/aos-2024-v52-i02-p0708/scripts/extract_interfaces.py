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
    terms=[] if term is None else term if isinstance(term,list) else [term];keywords=[]
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
add('D1','simple networks',r'''
We consider simple networks in the sense that there are no self-loops and there exists at most one edge from one node to another for a directed network, and at most one edge between two nodes for an undirected network. Such a network with $p$ nodes can be represented by an adjacency matrix $\mathbf X=(X_{i,j})_{p\times p}$, where $X_{i,i}\equiv0$, and $X_{i,j}=1$ indicating an edge from the $i$-th node to the $j$-th node, and $0$ otherwise. For undirected networks, $X_{i,j}=X_{j,i}$. In this paper, we always assume that the $p$ nodes are fixed and are labeled as $1,\ldots,p$. Then a simple network can be represented entirely by its adjacency matrix.
''',[3],'Section 2.1 — simple networks',kind='source_passage',phrases=['simple networks'],symbols=[r'X_{i,i}\equiv0',r'X_{i,j}=X_{j,i}'],shape='Finite labeled simple networks with binary adjacency, no loops, and symmetry in the undirected case used by the beta-model.')
add('D2','β-model',r'''
The so-called β-model (Chatterjee, Diaconis and Sly, 2011) for undirected networks is characterized by $p$ parameters $\boldsymbol\theta=(\theta_1,\ldots,\theta_p)^\top\in\mathbb R^p$ which define the probability function
\[
\mathbb P(X_{i,j}=1)=\frac{\exp(\theta_i+\theta_j)}{1+\exp(\theta_i+\theta_j)},\qquad i\ne j.\tag{3.1}
\]
The parameter $\theta_i$ in this model has a natural interpretation as it measures the propensity of node $i$ to have connections with other nodes. Namely, the larger $\theta_i$ is, the more likely node $i$ is connected to other nodes. The likelihood function for β-model is given by
\[
f(\mathbf X;\boldsymbol\theta)=\prod_{i,j:\,i<j}\frac{\exp\{(\theta_i+\theta_j)X_{i,j}\}}{1+\exp(\theta_i+\theta_j)}\propto\exp(U_1\theta_1+\cdots+U_p\theta_p),
\]
where $U_i=\sum_{j:\,j\ne i}X_{i,j}$ is the degree of the $i$-th node.
''',[6],'Section 3.1 — β-model, equation (3.1)',{'D1':'The model is a law on the simple undirected adjacency matrices with labeled nodes.'},kind='source_passage',phrases=['β-model'],symbols=[r'\boldsymbol\theta=(\theta_1,\ldots,\theta_p)^\top',r'\exp(\theta_i+\theta_j)'],shape='Independent undirected Bernoulli edges with additive node logits. The displayed product likelihood supplies joint independence; the parameter symbol theta is distinct from the beta noise probability.')
add('D3','data release mechanism',r'''
For $\mathcal I$ specified just after (2.1) above, we define a data release mechanism as follows:
\[
Z_{i,j}=X_{i,j}I(\varepsilon_{i,j}=0)+I(\varepsilon_{i,j}=1)\tag{2.3}
\]
for each $(i,j)\in\mathcal I$. In the above expression, $\{\varepsilon_{i,j}\}_{(i,j)\in\mathcal I}$ are independent random variables only taking three possible values $-1,0$ and $1$ with
\[
\mathbb P(\varepsilon_{i,j}=1)=\alpha,\quad\mathbb P(\varepsilon_{i,j}=0)=1-\alpha-\beta\quad\text{and}\quad\mathbb P(\varepsilon_{i,j}=-1)=\beta,\tag{2.4}
\]
where $\alpha,\beta\in[0,0.5]$. For an undirected network, $Z_{i,j}=Z_{j,i}$ for $j>i$. Then it follows from (2.3) and (2.4) that
\[
\mathbb P(Z_{i,j}=1\mid X_{i,j}=0)=\alpha\quad\text{and}\quad\mathbb P(Z_{i,j}=0\mid X_{i,j}=1)=\beta.\tag{2.5}
\]
''',[5],'Section 2.2 — jittering mechanism, equations (2.3)-(2.5)',{'D1':'Jittering acts on the admissible edge indices of the original simple network.'},symbols=[r'Z_{i,j}=X_{i,j}I(\varepsilon_{i,j}=0)+I(\varepsilon_{i,j}=1)'],phrases=['data release mechanism'],shape='Edgewise three-point replacement noise, with symmetric extension for an undirected graph. The mechanism is specified by independent noises and the printed conditional flip probabilities; independence of the noise from the original graph is implicit in its use as a release kernel, not separately stated here.')
add('D4','privacy level',r'''
We always confine $(\alpha,\beta)\in\mathcal M(\gamma;C_1)$ with
\[
\mathcal M(\gamma;C_1)=\big\{(\alpha,\beta):C_1<\alpha,\beta<0.5,1-\alpha-\beta=\gamma\big\}
\]
for some $\gamma\in(0,1]$ and $C_1\in(0,0.5)$. Our theoretical analysis allows $\gamma$ to be a constant, or to vary with respect to $p$. Of particular interest are the cases when $\gamma\to0$ (at different rates) together with $p\to\infty$. When $(\alpha,\beta)\in\mathcal M(\gamma;C_1)$ for some fixed constants $C_1\in(0,0.5)$, it follows from Remark 1 in Section 2.2 that the privacy level $\pi\asymp\gamma$.
''',[8],'Section 3.3 — restriction on the privacy parameters',{'D3':'Alpha and beta are the edge-flip probabilities in the jittering release mechanism.'},kind='condition',symbols=[r'\mathcal M(\gamma;C_1)',r'1-\alpha-\beta=\gamma'],phrases=['privacy level'],shape='A sequence-level restriction on two jitter probabilities with fixed positive C_1 and attenuation gamma. Gamma may vary with p. The strict inequalities make the class empty for gamma>=1-2C_1 despite the wider nominal interval (0,1].')
add('D5','Condition 1',r'''
There exists a universal constant $C_3>0$ such that $|\boldsymbol\theta|_\infty\leq C_3$.
''',[8],'Condition 1',{'D2':'The bounded vector is the node-logit parameter of the beta-model.'},kind='condition',context='Condition 1.',phrases=['Condition 1'],symbols=[r'|\boldsymbol\theta|_\infty\leq C_3'],shape='A uniform bound on the dense-model node parameters, independent of p. It is assumed by Theorems 1-3 and is not imported into the sparse-model theorem.')
add('D6',None,r'''
For $\tau\in\{0,1\}$, put
\[
\varphi_\tau(x)=(x-\alpha)^\tau(1-\beta-x)^{1-\tau}
\]
with $x\in\{0,1\}$. Then for any $i\ne j$,
\[
\mathbb P(X_{i,j}=0)=\frac{\mathbb E\{\varphi_0(Z_{i,j})\}}{1-\alpha-\beta}\quad\text{and}\quad\mathbb P(X_{i,j}=1)=\frac{\mathbb E\{\varphi_1(Z_{i,j})\}}{1-\alpha-\beta}.\tag{3.4}
\]
To simplify the notation, we write $\varphi_\tau(Z_{i,j})$ as $\varphi_{(i,j),\tau}$ for any $i\ne j$ and $\tau\in\{0,1\}$.
''',[7],'Section 3.2 — corrected edge functions and notation',{'D3':'The correction functions use the sanitized edges and the two known flip probabilities.'},symbols=[r'\varphi_\tau(x)',r'\varphi_{(i,j),\tau}'],shape='Two affine corrections to a binary edge observation. The exponent notation selects tau=0 or 1; the two functions are not probabilities themselves and can be negative.')
add('D7',None,r'''
For each $\ell\in[p]$, let
\[
\mu_{\ell,1}=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\mathbb E\{\varphi_{(i,\ell),1}\varphi_{(i,j),0}\varphi_{(\ell,j),1}\},\tag{3.6}
\]
\[
\mu_{\ell,2}=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\mathbb E\{\varphi_{(i,\ell),0}\varphi_{(i,j),1}\varphi_{(\ell,j),0}\},\tag{3.7}
\]
where $\mathcal H_\ell=\{(i,j):i,j\ne\ell\text{ such that }i<j\}$. By (3.5), we have
\[
\theta_\ell=\frac12\log\left(\frac{\mu_{\ell,1}}{\mu_{\ell,2}}\right).
\]
''',[7],'Section 3.2 — population moments, equations (3.6)-(3.7)',{'D6':'Each triangle moment is an expectation of three corrected edge functions.','D2':'The expectations and their log-ratio identity are taken under the beta-model and its sanitized network.'},symbols=[r'\mu_{\ell,1}',r'\mu_{\ell,2}',r'\mathcal H_\ell'],shape='Two triangle-product population moments indexed by unordered pairs avoiding node ell. Node indices lie in [p]; p>=3 is needed for a nonempty average. The source gives their log-ratio identity for theta.')
add('D8','moment-based estimator',r'''
Hence a moment-based estimator for $\theta_\ell$ can be defined as
\[
\widehat\theta_\ell=\frac12\log\left(\frac{\widehat\mu_{\ell,1}}{\widehat\mu_{\ell,2}}\right),\tag{3.8}
\]
where
\[
\widehat\mu_{\ell,1}=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\varphi_{(i,\ell),1}\varphi_{(i,j),0}\varphi_{(\ell,j),1},\tag{3.9}
\]
\[
\widehat\mu_{\ell,2}=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\varphi_{(i,\ell),0}\varphi_{(i,j),1}\varphi_{(\ell,j),0}.\tag{3.10}
\]
''',[8],'Section 3.2 — moment-based estimator, equations (3.8)-(3.10)',{'D6':'The sample triangle products are built from the corrected sanitized edge functions.','D7':'The index set H_ell is specified with the population moments in (3.6)-(3.7).'},phrases=['moment-based estimator'],symbols=[r'\widehat\theta_\ell',r'\widehat\mu_{\ell,1}',r'\widehat\mu_{\ell,2}'],shape='Log-ratio of two triangle-product averages. No finite-sample fallback is specified when the denominator is zero or the ratio is nonpositive; the census does not silently truncate or totalize the estimator.')
add('D9',None,r'''
For any $i\ne\ell$, let
\[
\lambda_{i,\ell}=\frac1{p-2}\sum_{j:\,j\ne\ell,i}\left[\frac1{\mu_{\ell,1}}\mathbb E\{\varphi_{(\ell,j),1}\}\mathbb E\{\varphi_{(i,j),0}\}+\frac1{\mu_{\ell,2}}\mathbb E\{\varphi_{(\ell,j),0}\}\mathbb E\{\varphi_{(i,j),1}\}\right].\tag{3.11}
\]
''',[9],'Section 3.3.2 — coefficients, equation (3.11)',{'D7':'The coefficients divide by the two population triangle moments.','D6':'The coefficient sum uses expectations of the corrected edge functions.'},symbols=[r'\lambda_{i,\ell}'],shape='Population coefficients in the linear variance contribution; a finite average over nodes distinct from i and ell.')
add('D10','asymptotic variances',r'''
Put
\[
b_\ell=\frac1{p-1}\sum_{i:\,i\ne\ell}\lambda_{i,\ell}^2\operatorname{Var}(Z_{i,\ell}),\tag{3.12}
\]
\[
\widetilde b_\ell=\frac1{2N}\left(\frac{\mu_{\ell,1}+\mu_{\ell,2}}{\mu_{\ell,1}\mu_{\ell,2}}\right)^2\sum_{i,j:\,i\ne j,\,i,j\ne\ell}\operatorname{Var}(Z_{i,\ell})\operatorname{Var}(Z_{\ell,j})\operatorname{Var}(Z_{i,j}).\tag{3.13}
\]
''',[9],'Section 3.3.2 — variance contributions, equations (3.12)-(3.13)',{'D9':'The first variance contribution uses squared lambda coefficients.','D7':'The second uses both population triangle moments.','D3':'Both variance contributions use the law of sanitized edges Z.'},context=r'Theorem 1 cannot be used to construct confidence intervals for $\theta_\ell$ directly since we would have to overcome two obstacles: (i) to identify the most appropriate phase in terms of relative sizes between $\gamma$ and $p$, and (ii) to estimate $b_\ell$ and $\widetilde b_\ell$ which determine the asymptotic variances.',symbols=[r'b_\ell',r'\widetilde b_\ell'],shape='Two distinct population variance contributions. The cubic contribution sums over ordered distinct pairs and has factor 1/(2N), with N=(p-1)(p-2). They are not plug-in estimates.')
members['D10']['naming_context'][0]['evidence']=[dict(page=10,location='Remark 3(c) — asymptotic variances')]
add('D11',None,r'''
where $\nu_\ell=(p-2)b_\ell+\widetilde b_\ell$.
''',[11],'Section 4.1 — variance in equation (4.1)',{'D10':'Nu combines the two variance contributions with the factor p-2.'},symbols=[r'\nu_\ell=(p-2)b_\ell+\widetilde b_\ell'],shape='Population variance for the N^(1/2)-normalized estimator across the three regimes. This is a linear combination of the original variance components, not their estimates.')
add('D12','bootstrap samples',r'''
Recall $\mathcal I=\{(i,j):1\leq i<j\leq p\}$. For a given constant $\delta\in(0,0.5)$, we draw bootstrap samples $\mathbf Z^\dagger=(Z_{i,j}^\dagger)_{p\times p}$ according to
\[
Z_{i,j}^\dagger\equiv Z_{j,i}^\dagger=Z_{i,j}I(\eta_{i,j}=0)+I(\eta_{i,j}=1),\qquad(i,j)\in\mathcal I,\tag{4.2}
\]
where $\{\eta_{i,j}\}_{(i,j)\in\mathcal I}$ are independent and identically distributed random variables only taking three possible values $-1,0$ and $1$ with
\[
\mathbb P(\eta_{i,j}=0)=1-2\delta,\quad\mathbb P(\eta_{i,j}=1)=\delta\quad\text{and}\quad\mathbb P(\eta_{i,j}=-1)=\delta.
\]
''',[11],'Section 4.1 — bootstrap samples, equation (4.2)',{'D3':'The bootstrap adds a second independent replacement-noise step to the already sanitized network Z.'},phrases=['bootstrap samples'],symbols=[r'\mathbf Z^\dagger',r'\eta_{i,j}',r'\delta\in(0,0.5)'],shape='Second edgewise jittering with symmetric replacement probability delta. Delta can be a sequence as required by the theorems. Independence from the first-stage data is implicit in drawing fresh bootstrap noise; no conditional asymptotic theorem is added.')
add('D13',None,r'''
For $i\ne j$ and $\tau\in\{0,1\}$, put
\[
\varphi_\tau^\dagger(x)=\{x-\delta-\alpha(1-2\delta)\}^\tau\{1-\delta-\beta(1-2\delta)-x\}^{1-\tau}
\]
with $x\in\{0,1\}$. To simplify the notation, we write $\varphi_\tau^\dagger(Z_{i,j}^\dagger)$ as $\varphi_{(i,j),\tau}^\dagger$ for any $i\ne j$ and $\tau\in\{0,1\}$.
''',[11],'Section 4.1 — corrected bootstrap edge functions',{'D12':'The correction uses the twice-jittered edge and the second-stage noise probability delta.','D3':'It also retains both original jittering probabilities alpha and beta.'},symbols=[r'\varphi_\tau^\dagger(x)',r'\varphi_{(i,j),\tau}^\dagger'],shape='The corrected bootstrap edge functions account for both noise stages; replacing them by the original phi functions would change the population center.')
add('D14','bootstrap estimator',r'''
Similarly, we define a bootstrap estimator for $\theta_\ell$ as:
\[
\widehat\theta_\ell^\dagger=\frac12\log\left(\frac{\widehat\mu_{\ell,1}^\dagger}{\widehat\mu_{\ell,2}^\dagger}\right),\tag{4.4}
\]
where
\[
\widehat\mu_{\ell,1}^\dagger=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\varphi_{(i,\ell),1}^\dagger\varphi_{(i,j),0}^\dagger\varphi_{(\ell,j),1}^\dagger,
\]
\[
\widehat\mu_{\ell,2}^\dagger=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\varphi_{(i,\ell),0}^\dagger\varphi_{(i,j),1}^\dagger\varphi_{(\ell,j),0}^\dagger.
\]
''',[11],'Section 4.1 — bootstrap estimator, equation (4.4)',{'D13':'The estimator uses the bootstrap-corrected edge functions in each triangle product.','D7':'Its averaging pairs use the same H_ell as the original population moments.'},phrases=['bootstrap estimator'],symbols=[r'\widehat\theta_\ell^\dagger',r'\widehat\mu_{\ell,1}^\dagger'],shape='A twice-jittered triangle log-ratio estimator with original population center theta. It has the same unresolved finite-sample log-domain issue as the original estimator.')
add('D15','bootstrap analogues',r'''
For $\mu_{\ell,1}$, $\mu_{\ell,2}$ and $\lambda_{i,\ell}$ defined as (3.6), (3.7) and (3.11), we define their bootstrap analogues, respectively, as
\[
\mu_{\ell,1}^\dagger=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\mathbb E\{\varphi_{(i,\ell),1}^\dagger\varphi_{(i,j),0}^\dagger\varphi_{(\ell,j),1}^\dagger\},
\]
\[
\mu_{\ell,2}^\dagger=\frac1{|\mathcal H_\ell|}\sum_{(i,j)\in\mathcal H_\ell}\mathbb E\{\varphi_{(i,\ell),0}^\dagger\varphi_{(i,j),1}^\dagger\varphi_{(\ell,j),0}^\dagger\},
\]
\[
\lambda_{i,\ell}^\dagger=\frac1{p-2}\sum_{j:\,j\ne\ell,i}\left[\frac1{\mu_{\ell,1}^\dagger}\mathbb E\{\varphi_{(\ell,j),1}^\dagger\}\mathbb E\{\varphi_{(i,j),0}^\dagger\}+\frac1{\mu_{\ell,2}^\dagger}\mathbb E\{\varphi_{(\ell,j),0}^\dagger\}\mathbb E\{\varphi_{(i,j),1}^\dagger\}\right].
\]
''',[11,12],'Section 4.1 — bootstrap population moments and coefficients',{'D13':'The expectation formulas use the corrected bootstrap edge functions.','D7':'The pair-averaging set H_ell is defined in the original moment block.'},phrases=['bootstrap analogues'],symbols=[r'\mu_{\ell,1}^\dagger',r'\mu_{\ell,2}^\dagger',r'\lambda_{i,\ell}^\dagger'],shape='Unconditional population moments and coefficients of the twice-jittered network, distinct from their sample analogues. References to the original formulas explain the analogy and do not import a proof dependency on their variance expansion.')
add('D16',None,r'''
Then $\widehat\theta_\ell^\dagger$ admits a similar asymptotic property as (4.1). To present it explicitly, we let
\[
\nu_\ell^\dagger=(p-2)b_\ell^\dagger+\widetilde b_\ell^\dagger,\qquad\ell\in[p],\tag{4.5}
\]
where
\[
b_\ell^\dagger=\frac1{p-1}\sum_{i:\,i\ne\ell}(\lambda_{i,\ell}^\dagger)^2\operatorname{Var}(Z_{i,\ell}^\dagger),
\]
\[
\widetilde b_\ell^\dagger=\frac1{2N}\left(\frac{\mu_{\ell,1}^\dagger+\mu_{\ell,2}^\dagger}{\mu_{\ell,1}^\dagger\mu_{\ell,2}^\dagger}\right)^2\sum_{i,j:\,i\ne j,\,i,j\ne\ell}\operatorname{Var}(Z_{i,\ell}^\dagger)\operatorname{Var}(Z_{\ell,j}^\dagger)\operatorname{Var}(Z_{i,j}^\dagger).
\]
''',[12],'Section 4.1 — bootstrap population variance, equation (4.5)',{'D15':'The bootstrap variance uses the bootstrap population moments and squared lambda-dagger coefficients.','D12':'Its variance factors are under the population law of the twice-jittered edges.'},symbols=[r'\nu_\ell^\dagger',r'b_\ell^\dagger',r'\widetilde b_\ell^\dagger'],shape='Combined bootstrap population variance with N=(p-1)(p-2). The variance is not a sample variance over repeated bootstrap draws; that later estimator is not the normalization in Theorems 2 or 3.')
add('D17','sparse β-model',r'''
To model the sparse networks, Chen, Kato and Leng (2021) consider the sparse β-model defined as
\[
\mathbb P(X_{i,j}=1)=\frac{\exp(\xi+\check\theta_i+\check\theta_j)}{1+\exp(\xi+\check\theta_i+\check\theta_j)},\tag{6.1}
\]
where $\xi\in\mathbb R$ and $\check{\boldsymbol\theta}=(\check\theta_1,\ldots,\check\theta_p)^\top\in\mathbb R_+^p$ are both unknown parameters with $|\check{\boldsymbol\theta}|_0\ll p$ and $\min_{\ell\in[p]}\check\theta_\ell=0$. Denote by $S$ the support of $\check{\boldsymbol\theta}$, that is $S=\{\ell\in[p]:\check\theta_\ell\ne0\}$. Write $|S|=s$. Given some constants $\omega_1\in[0,2)$ and $\omega_2\in[0,1)$ such that $0\leq\omega_1-\omega_2<1$, Chen, Kato and Leng (2021) consider the reparametrization
\[
\xi=-\omega_1\log p+\xi^+\quad\text{and}\quad\check\theta_\ell=\omega_2\log p+\check\theta_\ell^+\text{ for all }\ell\in S,
\]
where $|\xi^+|=o(\log p)$ and $\max_{\ell\in S}|\check\theta_\ell^+|=o(\log p)$. Let
\[
\theta_\ell=\frac\xi2+\check\theta_\ell,\qquad\ell\in[p].\tag{6.2}
\]
''',[17],'Section 6 — sparse β-model and reparametrization, equations (6.1)-(6.2)',{'D2':'The sparse model is the same independent-edge beta-model after substituting theta_ell=xi/2+check-theta_ell, without the dense bound in Condition 1.'},phrases=['sparse β-model'],symbols=[r'\xi=-\omega_1\log p+\xi^+',r'\check\theta_\ell=\omega_2\log p+\check\theta_\ell^+',r'|S|=s'],shape='Sparse nonnegative node effects, support size s=o(p), intercept and logarithmic reparametrization with little-o residuals. Theorem 4 narrows omega_1 and omega_2 further. Nonnegativity includes zero, as the source minimum equals zero. Empty support and its maximum are not explicitly given a convention.')
add('D18',None,r'''
By (6.2) and $s\ll p$ in the sparse β-model, we can estimate $\xi$ and $\check\theta_\ell$ as follows:
\[
\widehat\xi=\frac2p\sum_{\ell\in[p]}\widehat\theta_\ell\quad\text{and}\quad\widehat{\check\theta}_\ell=\widehat\theta_\ell-\frac{\widehat\xi}2.\tag{6.3}
\]
''',[18],'Section 6 — sparse parameter estimates, equation (6.3)',{'D17':'The parameters being estimated are the intercept and sparse effects in (6.1)-(6.2).','D8':'Both estimates are deterministic linear combinations of the original moment-based estimates theta-hat from (3.8).'},symbols=[r'\widehat\xi=\frac2p\sum_{\ell\in[p]}\widehat\theta_\ell',r'\widehat{\check\theta}_\ell'],shape='Intercept estimated by twice the average fitted logit, and sparse effects by subtracting half that intercept. The formula does not threshold or constrain the sparse-effect estimate to be nonnegative.')
add('D19','positive stochastic sequence',r'''
For the positive stochastic sequence $\{a_p\}$ and the positive sequence $\{c_p\}$, we write $a_p=\widetilde O_p(c_p)$ if $a_p=O_p(p^\epsilon c_p)$ for some sufficiently small fixed constant $\epsilon>0$.
''',[18],'Section 6 — stochastic-order convention',symbols=[r'\widetilde O_p(c_p)',r'O_p(p^\epsilon c_p)'],phrases=['positive stochastic sequence'],shape='The paper-specific tilde-O_p convention permits a small fixed polynomial factor, not merely logarithmic factors. The source says some sufficiently small epsilon and does not quantify every epsilon.',kind='source_passage')
interfaces[-1]['lean_role']='notation'
# Keyword groups retain separate source passages and local dependency edges.
# A shared title indexes the construction; it does not assert equivalence of its parts.
groups=[('D1',['D1']),('D2',['D2']),('D3',['D3']),('D4',['D4']),('D5',['D5']),('D8',['D6','D7','D8']),('D10',['D9','D10','D11']),('D12',['D12']),('D14',['D13','D14']),('D15',['D15','D16']),('D17',['D17','D18']),('D19',['D19'])]
byid={x['members'][0]['local_id']:x for x in interfaces};grouped=[]
for anchor,lids in groups:
    x=byid[anchor];x['members']=[members[lid] for lid in lids]
    if len(lids)>1:
        x['semantic_boundary']='Source-keyword group containing distinct component constructions; original bodies and local dependency identities are retained. '+x['semantic_boundary']
        for m in x['members']:
            m['relation']='distinct';m['variant_note']='This is an original component passage within the source-keyword group, not an equivalent alternative definition of the other components.'
    grouped.append(x)
interfaces=grouped
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(interfaces),'source-keyword groups containing',len(members),'distinct source passages.')


if __name__ == "__main__":
    main()
