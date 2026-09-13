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
add('D1','probability distributions',r'''
Let $(\pi_n)_{n\geq1}=(\pi_n(\cdot\mid Y^{(n)}))_{n\geq1}$ be a sequence of probability distributions on a common product space $\mathcal X=\mathcal X_1\times\cdots\times\mathcal X_K$, where each $\pi_n$ is allowed to depend on some observed data $Y^{(n)}\in\mathcal Y^{(n)}$. In our applications, $\pi_n(\cdot\mid Y^{(n)})$ represents the posterior distribution of some unknown parameter $x\in\mathcal X$ conditioned on the data $Y^{(n)}$. For the sake of brevity, we will often omit the explicit dependence on $Y^{(n)}$.
''',[4],'Section 2.1 — sequence of targets',kind='source_passage',phrases=['probability distributions'],symbols=[r'\pi_n(\cdot\mid Y^{(n)})',r'\mathcal X_1\times\cdots\times\mathcal X_K'],shape='A data-dependent sequence of probability measures on a common fixed product space. The generic Section 2 setup is not imposed directly on the growing-dimensional hierarchical posterior.')
members['D1']['application_context']=[dict(text=r'''In particular, we assume for the rest of this section that $Y^{(n)}$ is random with distribution $Q^{(n)}\in\mathcal P(\mathcal Y^{(n)})$.''',evidence=[dict(page=5,location='Section 2.2 — random data law')])]
add('D2','deterministic-scan Gibbs sampler',r'''
Let $P_n$ be the Markov transition kernel of the deterministic-scan Gibbs sampler targeting $\pi_n$, defined as the product of $K$ kernels
\[
P_n=P_{n,1}\cdots P_{n,K}.\tag{3}
\]
For each $i\in\{1,\ldots,K\}$, $P_{n,i}$ is the transition kernel on $\mathcal X$ that updates the $i$-th coordinate drawing it from its conditional distribution $\pi_n(dx_i\mid x^{(-i)})$, where $x^{(-i)}=(x_j)_{j\ne i}$, while leaving the other components unchanged. Equivalently
\[
P_{n,i}(x,S_{x,i,A})=\int_A\pi_n(dy_i\mid x^{(-i)}),\qquad A\subset\mathcal X_i,\quad i=1,\ldots,n,
\]
with $S_{x,i,A}=\{y\in\mathcal X:y_j=x_j\ \forall j\ne i\text{ and }y_i\in A\}$.
''',[4,5],'Section 2.1 — coordinate-update kernel (3)',{'D1':'The scan targets the data-dependent measures on the common product space.'},phrases=['deterministic-scan Gibbs sampler'],symbols=[r'P_n=P_{n,1}\cdots P_{n,K}',r'\pi_n(dx_i\mid x^{(-i)})'],shape='One full ordered scan uses exact coordinate conditionals. The display says i=1,...,n although the preceding sentence correctly ranges over K coordinates; the source discrepancy is not silently repaired. Conditional-distribution existence and versions require a suitable measurable-space framework.')
members['D2']['application_context']=[dict(text=r'''Let $\widetilde P$ and $\widetilde P_n$ be the kernels of the Gibbs samplers targeting $\widetilde\pi$ and $\widetilde\pi_n$, respectively.''',evidence=[dict(page=6,location='Section 2.2 — limiting and transformed Gibbs kernels')])]
add('D3','M-warm starts',r'''
The set of $M$-warm starts relative to a distribution $\pi$ is defined as
\[
\mathcal N(\pi,M)=\{\mu\in\mathcal P(\mathcal X):\mu(A)\leq M\pi(A)\text{ for all }A\subseteq\mathcal X\},\qquad M\geq1,\ \pi\in\mathcal P(\mathcal X).\tag{5}
\]
''',[5],'Section 2.1 — warm-start class (5)',context='We will focus on worst-case mixing times with respect to M-warm starts.',phrases=[],symbols=[r'\mathcal N(\pi,M)',r'\mu(A)\leq M\pi(A)'],shape='Measure domination by M times the target on all measurable events. This generic class can be instantiated on either the fixed Section 2 space or the hierarchical space. The feasible-start theorem does not explicitly assume its initialization has a fixed deterministic domination constant.')
add('D4','sequence of transformations',r'''
There exists $\widetilde\pi\in\mathcal P(\mathcal X)$ and a sequence of transformations $\phi_n:\mathcal X\to\mathcal X$ that act coordinate-wise, i.e. where
\[
\phi_n(x)=(\phi_{n,1}(x_1),\ldots,\phi_{n,K}(x_K)),\qquad x\in\mathcal X\tag{7}
\]
with $\phi_{n,j}:\mathcal X_j\to\mathcal X_j$ injective and measurable, such that
\[
\|\widetilde\pi_n-\widetilde\pi\|_{TV}\to0\qquad\text{as }n\to\infty,\tag{8}
\]
in $Q^{(n)}$-probability, i.e. such that $\lim_{n\to\infty}Q^{(n)}(\|\widetilde\pi_n-\widetilde\pi\|_{TV}>\epsilon)=0$ for every $\epsilon\in(0,1)$, where $\widetilde\pi_n=\pi_n\circ\phi_n^{-1}$ is the law of $\widetilde x=\phi_n(x)$ under $x\sim\pi_n$.
''',[5],'(A1)',{'D1':'A1 transforms the target sequence and measures convergence under its data law Q^(n).'},kind='assumption',phrases=['sequence of transformations','(A1)'],symbols=[r'\phi_n(x)',r'\|\widetilde\pi_n-\widetilde\pi\|_{TV}'],shape='Coordinatewise measurable injective pushforwards converging in total variation in data probability to a fixed limit. The source writes phi, not varphi. Surjectivity and measurable inverse are not explicitly stated, despite later prose calling the condition bijective.')
add('D5','Bayesian model',r'''
In this setting $\pi_n(d\psi)=p(d\psi\mid Y^{(n)})$ is the posterior distribution of the Bayesian model defined as
\[
Y_i\mid\psi\overset{\mathrm{iid}}\sim f(Y\mid\psi),\qquad\psi\sim p_0(\psi),\tag{11}
\]
where $\psi=(\psi_1,\ldots,\psi_K)$, with $\mathcal X\in\mathbb R^K$, and $Y^{(n)}=(Y_1,\ldots,Y_n)$, with $Y_i\in\mathcal Y$, $i=1,\ldots,n$, so that $\mathcal Y^{(n)}=\mathcal Y^n$. Moreover, if $Y_i\overset{\mathrm{iid}}\sim Q$ for some $Q\in\mathcal P(\mathcal Y)$, we denote with $Q^{(n)}$ and $Q^{(\infty)}$ the associated product measures.
''',[9],'Section 3 — model (11)',kind='source_passage',phrases=['Bayesian model'],symbols=[r'\pi_n(d\psi)=p(d\psi\mid Y^{(n)})',r'\mathcal Y^{(n)}=\mathcal Y^n'],shape='Fixed-dimensional iid Bayesian experiment with its finite and infinite data product measures. The source prints X in R^K instead of a subset relation; preserve that notation without changing the original passage.')
add('D6','test',r'''
A test is a measurable function $u:\mathcal Y^{(n)}\to[0,1]$. The integrals in (12) represent probabilities of errors of first and second kind, respectively, when the null hypothesis $H_0:\psi=\psi^*$ is rejected with probability $u(y_1,\ldots,y_n)$.
''',[10],'Section 3 — randomized test convention',phrases=['test'],symbols=[r'u:\mathcal Y^{(n)}\to[0,1]'],shape='A randomized measurable test taking values in [0,1]. The notation for the observation space is instantiated with n observations in Theorem 3.1 and J groups in B2; no prior or sampler is part of this generic definition.')
add('D7','Fisher Information',r'''
Let the map $\psi\to\sqrt{f(y\mid\psi)}$ be continously differentiable for every $y\in\mathcal Y$, with non-singular and continuous Fisher Information $\mathcal I(\psi)$.
''',[9],'Theorem 3.1 — likelihood regularity and information',{'D5':'The density f and its parameter belong to model (11).'},kind='theorem_excerpt',phrases=['Fisher Information'],symbols=[r'\mathcal I(\psi)',r'\sqrt{f(y\mid\psi)}'],shape='The original square-root density regularity and nonsingular continuous Fisher information hypothesis. The main text does not supply a separate score-integral formula for the f-model information; that standard meaning remains ambient, distinct from the explicitly defined marginal g-model information.')
add('D8','exponential family',r'''
We assume that the prior for $\theta_j\in\mathbb R^\ell$ belongs to the exponential family, that is
\[
p(\theta\mid\psi)=h(\theta)\exp\left\{\sum_{s=1}^S\eta_s(\psi)T_s(\theta)-A(\psi)\right\},\tag{14}
\]
where $\psi\in\mathbb R^D$, $h:\mathbb R^\ell\to\mathbb R_+$ is a non-negative function and $\eta_s(\psi)$, $T_s(\theta)$ and $A(\psi)$ are known real-valued functions with domains $\mathbb R^D$, $\mathbb R^\ell$ and $\mathbb R^D$ respectively. We will always assume the family to be minimal, that is both $(\eta_1(\psi),\ldots,\eta_S(\psi))$ and $(T_1(\theta),\ldots,T_S(\theta))$ are linearly independent.
''',[10,11],'Section 4 — local exponential-family prior (14)',kind='condition',phrases=['exponential family'],symbols=[r'\sum_{s=1}^S\eta_s(\psi)T_s(\theta)-A(\psi)'],shape='The local conditional prior, with a fixed number of sufficient-statistic components and the source’s stated minimality condition. The source uses linear independence rather than an explicitly affine minimality condition; neither is silently substituted for the other. The global prior need not be exponential-family.')
add('D9','hierarchical models',r'''
We consider a general class of hierarchical models, with data divided in $J$ groups, each having a set of group-specific parameters $\theta_j$. The latter share a common prior with hyper-parameters $\psi$. Recalling (1), the model under consideration is
\[
Y_j\mid\theta_j\sim f(\cdot\mid\theta_j),\qquad\theta_j\mid\psi\overset{\mathrm{iid}}\sim p(\cdot\mid\psi),\qquad\psi\sim p_0(\cdot).\tag{13}
\]
''',[10],'Section 4 — hierarchical model (13)',{'D8':'Section 4 immediately restricts the local conditional prior p to the minimal exponential family (14).'},kind='source_passage',phrases=['hierarchical models'],symbols=[r'Y_j\mid\theta_j',r'\theta_j\mid\psi'],shape='The Section 4 two-level hierarchical experiment with J group-specific vectors and fixed-dimensional hyperparameters. Conditional independence and the exact groupwise posterior factorization are part of the source model interpretation, not a requirement that the likelihood itself be exponential-family.')
members['D9']['application_context']=[dict(text=r'''On the other hand, we let $f(y\mid\theta)$ be an arbitrary likelihood function with data $y\in\mathbb R^m$ and parameters $\theta\in\mathbb R^\ell$, dominated by a suitable $\sigma$-finite measure (usually Lebesgue or counting one).''',evidence=[dict(page=11,location='Section 4 — likelihood domain and domination')])]
add('D10','two-block Gibbs sampler',r'''
Denoting $\boldsymbol\theta=(\theta_1,\ldots,\theta_J)$, $Y_{1:J}=(Y_1,\ldots,Y_J)$ and $\pi_J(d\boldsymbol\theta,d\psi)=\mathcal L(d\boldsymbol\theta,d\psi\mid Y_{1:J})$, we are interested in studying the two-block Gibbs sampler targeting $\pi_J(d\boldsymbol\theta,d\psi)$, i.e. the kernel defined as
\[
P_J((\boldsymbol\theta^{(t-1)},\psi^{(t-1)}),(d\boldsymbol\theta^{(t)},d\psi^{(t)}))
=\pi_J(d\boldsymbol\theta^{(t)}\mid\psi^{(t-1)})\pi_J(d\psi^{(t)}\mid\boldsymbol\theta^{(t)}).\tag{15}
\]
''',[11],'Section 4 — hierarchical Gibbs kernel (15)',{'D9':'The two blocks are the local parameters and hyperparameters of the hierarchical posterior.'},phrases=['two-block Gibbs sampler'],symbols=[r'\pi_J(d\boldsymbol\theta,d\psi)',r'\pi_J(d\boldsymbol\theta^{(t)}\mid\psi^{(t-1)})'],shape='A full exact update of all local parameters conditional on the old hyperparameter, then a hyperparameter update conditional on the new local block. It is not a random-scan or Metropolis-within-Gibbs approximation; its state dimension increases with J.')
add('D11','mixing times',r'''
Throughout Section 4 we denote by $(\boldsymbol\theta^{(t)},\psi^{(t)})_{t\geq1}$ the Markov chain with operator $P_J$, and by $t_{mix}^{(J)}$ the associated mixing times, i.e.
\[
t_{mix}^{(J)}(\epsilon,\mu)=\inf\{t\geq0:\|\mu P_J^t-\pi_J\|_{TV}<\epsilon\}.
\]
''',[11],'Section 4 — mixing time from a specified start',{'D10':'The power P_J^t and stationary target refer to the exact hierarchical Gibbs kernel.'},phrases=['mixing times'],symbols=[r't_{mix}^{(J)}(\epsilon,\mu)',r'\|\mu P_J^t-\pi_J\|_{TV}<\epsilon'],shape='The first discrete iteration whose total variation error from the specified initial law is strictly below epsilon. The displayed t>=0 is interpreted as a discrete iteration count, and the empty infimum is infinity. It is not a supremum over warm starts.')
add('D12','worst-case mixing times',r'''
\[
t_{mix}^{(J)}(\epsilon,M)=\sup_{\mu\in\mathcal N(\pi_J,M)}t_{mix}^{(J)}(\epsilon,\mu).
\]
''',[11],'Section 4 — worst-case warm-start mixing time',{'D11':'The quantity maximized is the specified-start hierarchical mixing time.','D3':'The maximization ranges over the measure-domination class N(pi_J,M).'},context='and the associated worst-case mixing times for $P_n$ targeting $\pi_n$ are',phrases=[],symbols=[r't_{mix}^{(J)}(\epsilon,M)',r'\mu\in\mathcal N(\pi_J,M)'],shape='The worst mixing time over all M-warm initial laws for the same hierarchical target. The original naming context occurs with the general n-indexed formula on page 5; page 11 specializes the definition to J.')
members['D12']['naming_context'][0]['evidence']=[dict(page=5,location='Section 2.1 — original terminology for (6)')]
add('D13','marginal likelihood',r'''
We denote the marginal likelihood of the model, obtained by integrating out the group specific parameter $\theta$, as
\[
g(y\mid\psi)=\int_{\mathbb R^\ell}f(y\mid\theta)p(\theta\mid\psi)\,d\theta,\tag{16}
\]
''',[12],'Section 4.2 — marginal likelihood (16)',{'D9':'The integral uses the hierarchical observation likelihood and local conditional prior.'},phrases=['marginal likelihood'],symbols=[r'g(y\mid\psi)',r'\int_{\mathbb R^\ell}'],shape='One-group marginal sampling density after integrating its local parameter, not the joint posterior or the marginal likelihood after integrating the global prior.')
add('D14','prior density',r'''
There exists $\psi^*\in\mathbb R^D$ such that $Y_j\overset{\mathrm{iid}}\sim Q_{\psi^*}$ for $j=1,2,\ldots$, where $Q_{\psi^*}$ admits density $g(y\mid\psi^*)$. Moreover the map $\psi\to g(\cdot\mid\psi)$ is one-to-one and the map $\psi\to\sqrt{g(x\mid\psi)}$ is continuously differentiable for every $x$. Finally, the prior density $p_0$ is continuous and strictly positive in a neighborhood of $\psi^*$.
''',[12],'(B1)',{'D13':'The data law and identifiability/regularity concern the one-group marginal density g.','D9':'The positive continuous p_0 is the global prior of the hierarchical model.'},kind='assumption',phrases=['prior density','(B1)'],symbols=[r'\sqrt{g(x\mid\psi)}',r'Q_{\psi^*}'],shape='The full B1 assumption, retaining its correctly specified iid data law, marginal identifiability, square-root density regularity and local global-prior positivity together. The source keyword identifies one component but the complete assumption remains intact.')
members['D14']['application_context']=[dict(text=r'''Below we denote the product measures associated to $Q_{\psi^*}$ by $Q_{\psi^*}^{(J)}$ and $Q_{\psi^*}^{(\infty)}$.''',evidence=[dict(page=12,location='Before Theorem 4.2 — data product measures')])]
add('D15','sequence of tests',r'''
There exist a compact neighborhood $\Psi$ of $\psi^*$ and a sequence of tests $u_j:\mathbb R^{mJ}\to[0,1]$ such that $\int_{\mathbb R^{mJ}}u_j(y_1,\ldots,y_J)\prod_{j=1}^Jg(y_j\mid\psi^*)\,dy_{1:J}\to0$ and
\[
\sup_{\psi\notin\Psi}\int_{\mathbb R^{mJ}}[1-u_j(y_1,\ldots,y_J)]\prod_{j=1}^Jg(y_j\mid\psi)\,dy_{1:J}\to0,\qquad\text{as }J\to\infty.
\]
''',[12],'(B2)',{'D13':'Both test-error integrals use the product of one-group marginal densities.','D6':'The tests use the paper’s measurable [0,1]-valued randomized-test convention.'},kind='assumption',phrases=['sequence of tests','(B2)'],symbols=[r'\sup_{\psi\notin\Psi}',r'u_j:\mathbb R^{mJ}\to[0,1]'],shape='Uniform testing outside one compact neighborhood, with the source’s lower-case j on u_j and upper-case J sample dimension retained. The dy notation is printed even though the allowed likelihood dominating measure may be counting measure.')
add('D16','Fisher Information matrix',r'''
and its Fisher Information matrix as
\[
[\mathcal I(\psi)]_{d,d'}=E[\{\partial_{\psi_d}\log g(Y\mid\psi)\}\{\partial_{\psi_{d'}}\log g(Y\mid\psi)\}],\qquad d,d'=1,\ldots,D.
\]
''',[12],'Section 4.2 — marginal Fisher information',{'D13':'The score derivatives are of the group-marginal density g.'},phrases=['Fisher Information matrix'],symbols=[r'[\mathcal I(\psi)]',r'\partial_{\psi_d}\log g(Y\mid\psi)'],shape='The source score second-moment matrix for the marginal group model. The displayed expectation has no parameter subscript; its usual Fisher-information interpretation is under the candidate law g(.;psi), with the true value obtained at psi*. No new formula is inserted into the f-model Theorem 3.1.')
add('D17','Fisher Information matrix',r'''
The Fisher Information matrix $\mathcal I(\psi)$ is non-singular and continuous w.r.t. $\psi$.
''',[12],'(B3)',{'D16':'B3 constrains the marginal information matrix defined immediately above it.'},kind='assumption',phrases=['Fisher Information matrix','(B3)'],symbols=[r'\mathcal I(\psi)'],shape='Nonsingularity and continuity of the marginal Fisher information. This condition is kept separately from the definition of the matrix and from the f-model hypothesis in Theorem 3.1.')
add('D18','maximum marginal likelihood estimator',r'''
Indeed, assume that the maximum marginal likelihood estimator $\widehat\psi_J=\operatorname{argmax}\prod_{j=1}^Jg(Y_j\mid\psi)$, with $g$ as in (16), is well-defined.
''',[22],'Section 6 — marginal maximum likelihood initializer',{'D13':'The maximized product is formed from the group-marginal densities in (16).'},kind='condition',phrases=['maximum marginal likelihood estimator'],symbols=[r'\widehat\psi_J',r'\prod_{j=1}^Jg(Y_j\mid\psi)'],shape='The exact marginal maximum-likelihood estimate used to center the feasible start. The source omits a subscript on argmax and assumes it is well defined; existence, uniqueness and a measurable choice are not proved by this definition.')
add('D19','feasible start',r'''
Let $\mu_J\in\mathcal P(\mathbb R^{lJ+D})$ be given by
\[
\mu_J(B)=\int_B\operatorname{Unif}(\widehat\psi_J,c/\sqrt J)(d\psi)\prod_{j=1}^Jp(\theta_j\mid Y_j,\psi)\,d\boldsymbol\theta,\qquad B\subset\mathbb R^{lJ+D}\tag{35}
\]
where $c>0$ is a fixed constant and $\operatorname{Unif}(\psi,r)$ denotes the uniform distribution over the closed ball of center $\psi$ and radius $r>0$.
''',[22],'Section 6 — feasible initialization (35)',{'D18':'The uniform hyperparameter ball is centered at the marginal maximum likelihood estimator.','D9':'The product uses the group-specific posterior conditionals from the hierarchical model.'},context='Since starting from $\mu\in\mathcal N(\pi_J,M)$ with small $M$ (e.g. not increasing with $J$) may be in principle infeasible, it is of interest to provide an explicit example of a starting distribution that can be implemented in practice, a so-called feasible start, where the associated value of $M$ can be controlled.',phrases=[],symbols=[r'\mu_J(B)',r'\operatorname{Unif}(\widehat\psi_J,c/\sqrt J)'],shape='Draw the hyperparameter uniformly in a shrinking closed ball around the marginal MLE, then independently draw each local parameter from its exact conditional posterior. The radius constant c is fixed. The printed lower-case l in the joint dimension is retained. No deterministic M-warm guarantee is built into this definition.')
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print(f'Saved {len(interfaces)} source interfaces.')
