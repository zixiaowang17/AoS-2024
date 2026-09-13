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
add('D1','data model',r'''
Consider a supervised learning scenario where we are given i.i.d data $\{(\boldsymbol x_i,y_i)\}_{i\leq n}$ generated according to the following distribution:
\[
y_i=\langle\boldsymbol x_i,\boldsymbol\beta\rangle+\xi_i,\quad\text{with}\quad\boldsymbol x_i\sim_{\mathrm{iid}}N(0,\boldsymbol I_d),\quad\xi_i\sim N(0,\tau^2).\tag{2.1}
\]
The (linear) dependence between $(\boldsymbol x_i,y_i)$ is unknown and the goal is to fit a model to this data which can be then used to predict labels for the unlabeled examples at test time.
''',[4],'Section 2 — data model, equation (2.1)',kind='source_passage',context=r'Recall the data model (2.1).',symbols=[r'y_i=\langle\boldsymbol x_i,\boldsymbol\beta\rangle+\xi_i',r'\tau^2'],shape='I.i.d. response/covariate pairs with standard Gaussian covariates and Gaussian additive residual marginals; the displayed source does not explicitly state independence of xi and the covariates.')
# The naming term comes from the explicit source reference, not invented prose.
members['D1']['naming_context'][0]['text']='Recall that in the data model (2.1),'
members['D1']['naming_context'][0]['evidence']=[dict(page=10,location='Paragraph after Assumption 1')]
add('D2','random features',r'''
We consider modeling the relation between label $y$ and feature vector $\boldsymbol x$ using the class of random features (RF) model, which can be described as
\[
\mathcal F_{\mathrm{RF}}(\boldsymbol W)=\left\{f(\boldsymbol x,\boldsymbol\theta,\boldsymbol W)=\sum_{\ell=1}^N\theta_\ell\sigma(\langle\boldsymbol w_\ell,\boldsymbol x\rangle):\boldsymbol\theta=(\theta_1,\cdots,\theta_N)\in\mathbb R^N\right\},\tag{2.2}
\]
where $\boldsymbol\theta$ is the parameter vector to be learned and $\boldsymbol W\in\mathbb R^{N\times d}$ is a fixed matrix whose rows $\boldsymbol w_\ell$ are chosen randomly and independently of data. For simplicity we assume the normalization $\|\boldsymbol w_\ell\|_{\ell_2}=1$. Namely, the vectors $\boldsymbol w_\ell$ are chosen uniformly at random from the unit sphere, $\boldsymbol w_\ell\sim\mathrm{Unif}(\mathbb S^{d-1})$, which implies that $\langle\boldsymbol w_\ell,\boldsymbol x_j\rangle$ is of order one. In addition, $\sigma:\mathbb R\mapsto\mathbb R$ is a nonlinear activation function.
Note that in random features model training is only done on $\boldsymbol\theta$ and not on $\boldsymbol W$.
''',[4],'Section 2 — random features model, equation (2.2)',phrases=['random features'],symbols=[r'\mathcal F_{\mathrm{RF}}(\boldsymbol W)',r'\boldsymbol W'],shape='Finite random-feature linear span with sphere-distributed first-layer rows independent of the data, held fixed during second-layer fitting; the activation is an argument here.')
members['D2']['application_context']=[dict(text=r'Before we outline the main steps of the proof, we note that since the rows of the matrix $\boldsymbol W\in\mathbb R^{N\times d}$ are generated i.i.d. according to $\boldsymbol w_\ell\sim\mathrm{Unif}(\mathbb S^{d-1})$, then the matrix norm of $\boldsymbol W$ is bounded with high probability and the rows of $\boldsymbol W$ are almost orthogonal.',evidence=[dict(page=15,location='Section 6 — row-independence specification')])]
add('D3','shifted ReLU activation',r'''
Recall the data distribution given in (2.1). Given $n$ i.i.d pairs $(\boldsymbol x_i,y_i)$ drawn from this distribution, we fit a random features model, defined as the function class (2.2), with the shifted ReLU activation:
\[
\sigma(x)=\max(x,0)-\frac1{\sqrt{2\pi}}.\tag{4.1}
\]
''',[10],'Section 4 — shifted ReLU activation, equation (4.1)',phrases=['shifted ReLU activation'],symbols=[r'\sigma(x)'],shape='The scalar shifted positive-part function, applied componentwise to feature vectors. It can be defined without a sampling law or a particular feature matrix.')
add('D4','Asymptotic setting',r'''
(a) Defining $\psi_{1,d}=N/d$ and $\psi_{2,d}=n/d$, we assume that the following limits exist:
\[
\lim_{d\to\infty}\psi_{1,d}=\psi_1,\qquad\lim_{d\to\infty}\psi_{2,d}=\psi_2,
\]
for some positive finite constants $\psi_1$ and $\psi_2$.

(b) We assume that the $\ell_2$ norm of the signal $\boldsymbol\beta$ converges, as $d\to\infty$. For the sake of normalization and without loss of generality, we assume $\lim_{d\to\infty}\|\boldsymbol\beta\|_{\ell_2}=1$.
''',[10],'Assumption 1 (Asymptotic setting.)',{'D1':'The signal beta is the coefficient vector of data model (2.1).'},kind='assumption',context='Assumption 1 (Asymptotic setting.)',phrases=['Assumption 1'],symbols=[r'\psi_{1,d}',r'\psi_{2,d}'],shape='Proportional feature/sample/input dimensions and signal norm tending to one; preserve both parts as the explicit hypothesis of Theorem 4.2.')
add('D5','Adversarial risk',r'''
For a predictive model $f$ and a loss of choice $\ell:\mathbb R\times\mathbb R\to\mathbb R_{\geq0}$, the adversarial risk of model $f$ is defined as:
\[
\mathrm{AR}(f):=\mathbb E\left[\max_{\|\boldsymbol\delta\|_{\ell_2}\leq\varepsilon_{\mathrm{test}}}\ell(f(\boldsymbol x+\boldsymbol\delta),y)\right],
\]
where the expectation is with respect to randomness of $(\boldsymbol x,y)$.

In particular, for a random features model $\boldsymbol\theta=(\theta_1,\cdots,\theta_N)^\top$ from $\mathcal F_{\mathrm{RF}}(\boldsymbol W)$, defined in (2.2), and with the choice of squared loss, the adversarial risk of $\boldsymbol\theta$ becomes:
\[
\mathrm{AR}(\boldsymbol\theta):=\mathbb E\left[\max_{\|\boldsymbol\delta\|_{\ell_2}\leq\varepsilon_{\mathrm{test}}}(y-\boldsymbol\theta^\top\sigma(\boldsymbol W(\boldsymbol x+\boldsymbol\delta)))^2\right].\tag{4.2}
\]
''',[10],'Definition 4.1 (Adversarial risk.)',{'D1':'The surrounding Section 4 fixes the test-pair distribution to data model (2.1).','D2':'The specialization evaluates the random features model for a given W and coefficient vector.','D3':'Section 4 specializes the feature map to shifted ReLU.'},context='Definition 4.1 (Adversarial risk.)',phrases=['adversarial risk'],symbols=[r'\mathrm{AR}(f)',r'\mathrm{AR}(\boldsymbol\theta)'],shape='Expected test loss after a pointwise maximizing Euclidean perturbation, with a separate test radius. Expectation is over the test pair for a fixed fitted model, not over its training data or W.')
add('D6','robust empirical risk minimization',r'''
A popular approach to adversarial training is by considering the following robust empirical risk minimization (robust-ERM) problem [58, 90]:
\[
\widehat{\boldsymbol\theta}^{\varepsilon}=\operatorname*{argmin}_{\boldsymbol\theta\in\mathbb R^N}\max_{\|\boldsymbol\delta_i\|_{\ell_2}\leq\varepsilon}\frac1{2n}\sum_{i=1}^n(y_i-\boldsymbol\theta^\top\sigma(\boldsymbol W(\boldsymbol x_i+\boldsymbol\delta_i)))^2.\tag{4.3}
\]
''',[10],'Section 4 — robust empirical risk minimization, equation (4.3)',{'D1':'The empirical objective uses n pairs from the data model.','D2':'The fitted coefficients range over the random features model with W fixed.','D3':'The section fixes the activation to shifted ReLU.'},phrases=['robust empirical risk minimization'],symbols=[r'\widehat{\boldsymbol\theta}^{\varepsilon}'],shape='Robust training minimization over all second-layer coefficients and separate bounded perturbations for each sample; training radius epsilon need not equal epsilon_test. No added ridge penalty.')
add('D7','Stieltjes transform',r'''
For $\psi_1\in(0,\infty)$, we define function $S(\cdot;\psi_1):\mathbb R_{<0}\to\mathbb R_{<0}$:
\[
S(z;\psi_1)=\frac{1-\psi_1-z-\sqrt{(1-\psi_1-z)^2-4\psi_1z}}{-2\psi_1z}.\tag{4.4}
\]
One may recognize that $S(z;\psi_1)$ is the Stieltjes transform of the Marchenko-Pastur distribution. We refer to Lemma F.2 (Appendix F) for more details.
''',[11],'Section 4 — Stieltjes transform formula, equation (4.4)',phrases=['Stieltjes transform'],symbols=[r'S(z;\psi_1)'],shape='Explicit real-valued transform on negative real z, with positive aspect ratio parameter and the source sign convention. The defining integral and other details in Appendix F are outside scope.')
add('D8',['matrix norm','almost orthogonal'],r'''
Before we outline the main steps of the proof, we note that since the rows of the matrix $\boldsymbol W\in\mathbb R^{N\times d}$ are generated i.i.d. according to $\boldsymbol w_\ell\sim\mathrm{Unif}(\mathbb S^{d-1})$, then the matrix norm of $\boldsymbol W$ is bounded with high probability and the rows of $\boldsymbol W$ are almost orthogonal. More precisely, we define the event
\[
\mathcal E_{\boldsymbol W}:=\left\{\|\boldsymbol W\|\leq\sqrt{\psi_{1,d}}+C,\ |\boldsymbol w_\ell^\top\boldsymbol w_k|\leq\log(d)/\sqrt d\ \forall\ell\ne k\right\},\tag{6.2}
\]
for a large enough constant $C$ (note that $N/d:=\psi_{1,d}$ – see Assumption 1).
''',[15],'Section 6 — random-weight event, equation (6.2)',{'D2':'The event restricts the sampled random-feature weight matrix and its rows.'},kind='condition',phrases=['matrix norm','almost orthogonal'],symbols=[r'\mathcal E_{\boldsymbol W}'],shape='Joint spectral-norm and pairwise row-correlation event. Its defining ratio N/d is finite-dimensional notation and does not require signal normalization from Assumption 1(b).')
add('D9','adversarial effects',r'''
Hence, this can be written as $\mathbb E[\eta_i(\boldsymbol\theta)^2]=\|\boldsymbol J\boldsymbol\theta\|_{\ell_2}^2$ with
\[
\boldsymbol J:=\left((\boldsymbol W\boldsymbol W^\top)\odot\mathbb E[\mathbb I(\boldsymbol W\boldsymbol x_i>0)\mathbb I(\boldsymbol W\boldsymbol x_i>0)^\top]\right)^{1/2}.
\]
Note that the $\boldsymbol J$ is well-defined since the matrix under the square root is positive semidefinite. (This follows from the observation that the expression (6.9) is positive for all $\boldsymbol\theta$.)
''',[17],'Section 6.2 — matrix of adversarial effects',{'D2':'The matrix uses the random-feature weight matrix W.','D1':'The expectation is over standard Gaussian covariates x_i, with W fixed.'},context='6.2. Concentration of the adversarial effects',symbols=[r'\boldsymbol J'],shape='Positive-semidefinite matrix square root of the Hadamard product of the weight Gram matrix with its Gaussian sign-indicator second moment; W is fixed inside the expectation.')
members['D9']['statement_original']+=r'''

Therefore, we obtain the following explicit formulation for $\boldsymbol J_{\boldsymbol W}$:
\[
\boldsymbol J=\left((\boldsymbol W\boldsymbol W^\top)\odot\left(\frac{\pi-\cos^{-1}(\boldsymbol W\boldsymbol W^\top)}{2\pi}\right)\right)^{1/2}.\tag{6.10}
\]
'''
members['D9']['excerpt_selection']='The original J definition and positive-semidefiniteness sentence, followed by its explicit formula (6.10); intervening jointly Gaussian covariance calculations are omitted.'
add('D10',['activation function','nonlinear component'],r'''
We begin with decomposing the nonlinear activation function $\sigma(z)$ as
\[
\sigma(z)=\mu_0+\mu_1z+\mu_2\sigma_\perp(z),\tag{6.13}
\]
where for $G\sim N(0,1)$,
\[
\mu_0:=\mathbb E[\sigma(G)],\qquad\mu_1=\mathbb E[G\sigma(G)],\qquad\mu_2:=\sqrt{\mathbb E[\sigma^2(G)]-\mu_0^2-\mu_1^2}.
\]
For the case of shifted ReLU activation, defined in (4.1), we have $\mu_0=0$, $\mu_1=\frac12$ and $\mu_2=\sqrt{\frac14-\frac1{2\pi}}$. Also, $\sigma_\perp(z)$ is the nonlinear component of the activation function which is orthogonal to the constant and linear components in the following sense: $\mathbb E[\sigma_\perp(G)]=0$ and $\mathbb E[G\sigma_\perp(G)]=0$.
''',[18],'Section 6.3 — activation decomposition, equation (6.13)',{'D3':'The recorded numerical coefficients specialize the moment decomposition to shifted ReLU.'},phrases=['activation function','nonlinear component'],symbols=[r'\mu_0',r'\mu_1',r'\mu_2',r'\sigma_\perp'],shape='Gaussian constant, linear and orthogonal residual decomposition of the activation, including the exact shifted-ReLU coefficients. The square root covers all three terms in the residual variance.')
add('D11','noisy linear model',r'''
This suggests to replace the variables $\sigma_\perp(\boldsymbol w_i^\top\boldsymbol x)$ by a set of i.i.d standard normal variables and consider the following noisy linear model
\[
\boldsymbol f:=\mu_0\boldsymbol 1+\mu_1\boldsymbol W\boldsymbol x+\mu_2\boldsymbol u,\tag{6.15}
\]
with $\boldsymbol f,\boldsymbol u\in\mathbb R^N$ and $\boldsymbol u\sim N(0,\boldsymbol I_N)$ is generated independently from $\boldsymbol x$.
''',[18],'Section 6.3 — noisy linear features, equation (6.15)',{'D10':'The feature coefficients are the Gaussian activation moments in (6.13).','D2':'The linear component uses the same random-feature weight matrix.','D1':'The original input is the standard Gaussian covariate in data model (2.1).'},phrases=['noisy linear model'],symbols=[r'\boldsymbol f',r'\boldsymbol u'],shape='Gaussian noisy linear surrogate features for the same covariate and W, using independent-from-x standard Gaussian perturbations; preserve the source independence wording.')
members['D11']['application_context']=[dict(text=r'where $\boldsymbol f_i$ are generated i.i.d. according to (6.15).',evidence=[dict(page=19,location='Immediately after equation (6.16)')])]
add('D12','asymptotic regime',r'''
Note that we consider the asymptotic regime where $n,d,N$ grow at the same scale, ($\lim N/d\to\psi_1$ and $\lim n/d\to\psi_2$ for some positive constants $\psi_1$ and $\psi_2$), the expression $d\to\infty$ implies that $n,N\to\infty$, as well.
''',[16],'Section 6 — proportional-growth convention',kind='condition',phrases=['asymptotic regime'],symbols=[r'd\to\infty'],shape='Section-wide proportional growth convention for the probability limits. The source repeats the positive aspect ratios here, but does not repeat signal normalization in Theorem 6.9.')
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed interfaces.')
