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
add('D1','two-stage',r'''
Consider a two-stage series of binary treatment assignments, denoted by $A_1$ and $A_2$, and an outcome of interest, $Y\in\mathbb R$. Alongside this, a set of possibly high-dimensional sequential pre-treatment covariates $\mathbf S_1\in\mathbb R^{d_1}$ and $\mathbf S_2\in\mathbb R^{d_2}$, possibly of different dimensions, are also observed. The potential or counterfactual outcomes, $Y(a)$, refer to the outcome that a participant would have experienced had they followed a particular treatment sequence, $a=(a_1,a_2)\in\{0,1\}^2$, which may differ from the treatment they were observed with.
''',[1,2],'Section 1 — two-stage treatment observations and potential outcomes',kind='source_passage',phrases=['two-stage'],symbols=[r'Y(a)',r'\mathbf S_1',r'\mathbf S_2'],shape='Two binary exposures, sequential real-vector covariates and real potential outcomes indexed by a treatment path; no causal independence is built into the observation space.')
add('D2','dynamic treatment effect',r'''
Our parameter of interest is the dynamic treatment effect (DTE) between two treatment paths, $a$ and $a'$, which is defined as follows:
\[
\theta:=E[Y(a)]-E[Y(a')]=\theta_a-\theta_{a'},\quad\text{with }\theta_a:=E[Y(a)].\tag{1.1}
\]
''',[2],'Section 1 — dynamic treatment effect, equation (1.1)',{'D1':'The expected outcomes are indexed by the two-stage treatment paths.'},phrases=['dynamic treatment effect'],symbols=[r'\theta'],shape='Difference of population mean potential outcomes for the specified two treatment paths.')
add('D3',['conditional means','working models'],r'''
In an MSM, the treatment assignment and the outcome of interest are modeled separately using propensity scores $\pi_a(\mathbf s_1)$ and $\rho_a(\mathbf s)$ together with the first-time and second-time conditional means, $\mu_a(\mathbf s_1):=E[Y(a)\mid\mathbf S_1=\mathbf s_1]$ and $\nu_a(\mathbf s):=E[Y(a)\mid\mathbf S=\mathbf s,A_1=a_1]$. Throughout this work, we use $\pi_a^*(\cdot)$ and $\rho_a^*(\cdot)$ as well as $\mu_a^*(\cdot)$ and $\nu_a^*(\cdot)$ to refer to the working models, i.e., the population-level approximations of the propensity scores and conditional means, respectively.
''',[2],'Section 1.1 — conditional means and general working-model notation',{'D1':'Conditional means use the potential outcomes and sequential covariates.','D4':'The working propensity models approximate the two defined conditional assignment probabilities.'},phrases=['conditional means','working models'],symbols=[r'\mu_a(\mathbf s_1)',r'\nu_a(\mathbf s)',r'\mu_a^*(\cdot)',r'\nu_a^*(\cdot)'],shape='General population conditional means and corresponding working functions; this passage imposes no linear or logistic form.')
add('D4','propensity scores',r'''
Here, the propensity scores are defined as $\pi_a(\mathbf s_1):=P[A_1=a_1\mid\mathbf S_1=\mathbf s_1]$ and $\rho_a(\mathbf s):=P[A_2=a_2\mid\mathbf S=\mathbf s,A_1=a_1]$.
''',[2],'Assumption 1 — propensity score definitions',{'D1':'The conditional probabilities refer to the two exposure assignments and covariates.'},phrases=['propensity scores'],symbols=[r'\pi_a(\mathbf s_1)',r'\rho_a(\mathbf s)'],shape='Two-stage assignment probabilities; the separate overlap assumption is not part of their defining equations.')
add('D5',['Sequential Ignorability','Consistency of potential outcomes','Overlap'],r'''
(a) (Sequential Ignorability) $Y(a_1,a_2)\mathrel{\perp\!\!\!\perp}A_1\mid\mathbf S_1$ and $Y(a_1,a_2)\mathrel{\perp\!\!\!\perp}A_2\mid\mathbf S,A_1=a_1$ where $\mathbf S=(\mathbf S_1^\top,\mathbf S_2^\top)^\top\in\mathbb R^d$ with $d:=d_1+d_2$. (b) (Consistency of potential outcomes) $Y=Y(A_1,A_2)$. (c) (Overlap) Let $c_0\in(0,1/2)$ be a positive constant, such that $P(c_0\leq\pi_a(\mathbf S_1)\leq1-c_0)=1$, and $P(c_0\leq\rho_a(\mathbf S)\leq1-c_0)=1$. Here, the propensity scores are defined as $\pi_a(\mathbf s_1):=P[A_1=a_1\mid\mathbf S_1=\mathbf s_1]$ and $\rho_a(\mathbf s):=P[A_2=a_2\mid\mathbf S=\mathbf s,A_1=a_1]$.
''',[2],'Assumption 1',{'D1':'The causal assumptions concern the two-stage potential outcomes.','D4':'Overlap bounds the true conditional assignment probabilities.'},kind='assumption',phrases=['Sequential Ignorability','Consistency of potential outcomes','Overlap','Assumption 1'],shape='All three printed causal conditions for two-stage trials, with almost-sure two-sided overlap and distinct first/second-stage conditioning.')
add('D6',['Orlicz norm','sub-Gaussian'],r'''
For any $\alpha>0$, let $\psi_\alpha(\cdot)$ denote the function given by $\psi_\alpha(x):=\exp(x^\alpha)-1$, $\forall x>0$. Then the $\psi_\alpha$-Orlicz norm $\|\cdot\|_{\psi_\alpha}$ of a random variable $X$ is defined as $\|X\|_{\psi_\alpha}:=\inf\{c>0:E[\psi_\alpha(|X|/c)]\leq1\}$. Two special cases of finite $\psi_\alpha$-Orlicz norm are given by $\psi_2(x)=\exp(x^2)-1$ and $\psi_1(x)=\exp(x)-1$, which correspond to sub-Gaussian and sub-exponential random variables, respectively.
''',[4],'Section 1.3 — Orlicz norms',phrases=['Orlicz norm','sub-Gaussian'],symbols=[r'\psi_2',r'\|\cdot\|_{\psi_\alpha}'],shape='Luxemburg exponential Orlicz norm with alpha-positive gauges and the sub-Gaussian special case; zero-input gauge extension is not explicitly stated.')
add('D7',['logistic function','link function'],r'''
Define $g(u)=\exp(u)/\{1+\exp(u)\}$ as the logistic function and $\phi(u)=\log(1+\exp(u))$ as the corresponding link function throughout.
''',[4,5],'Section 1.3 — logistic and link functions',phrases=['logistic function','link function'],symbols=[r'g(u)',r'\phi(u)'],shape='Real logistic response and softplus loss primitive, retaining the source term link function for phi.')
add('D8','independent and identically distributed',r'''
We observe a collection of independent and identically distributed (i.i.d.) samples $\mathcal D:=\{W_i\}_{i=1}^N=(Y_i,\mathbf S_{1i},A_{1i},\mathbf S_{2i},A_{2i})_{i=1}^N$, drawn from the same distribution as $(Y,\mathbf S_1,A_1,\mathbf S_2,A_2)$.
''',[5],'Section 2 — observed sample',{'D1':'The sample law is that of the two-stage observation.'},kind='source_passage',phrases=['independent and identically distributed'],symbols=[r'\mathcal D',r'W_i'],shape='N independent copies of the two-stage observed tuple; sample independence is separate from causal identifiability.')
add('D9','population minimizer',r'''
The population minimizer approximating $\pi_a(\mathbf s_1)$ is defined as $\pi_a^*(\mathbf s_1)=g(\mathbf v^\top\boldsymbol\gamma_a^*)$ with $\mathbf v=(1,\mathbf s_1^\top)^\top$, whereas that of approximating $\rho_a(\mathbf s)$ is $\rho_a^*(\mathbf s)=g(\mathbf u^\top\boldsymbol\delta_a^*)$ with $\mathbf u=(1,\mathbf s^\top)^\top$. Here
\[
\boldsymbol\gamma_a^*=\operatorname*{argmin}_{\boldsymbol\gamma\in\mathbb R^{d_1+1}}E[\phi(\mathbf V^\top\boldsymbol\gamma)-\mathbb 1_{\{A_1=a_1\}}\mathbf V^\top\boldsymbol\gamma],\quad\mathbf V=(1,\mathbf S_1^\top)^\top\in\mathbb R^{d_1+1}\ \text{and}\tag{2.1}
\]
\[
\boldsymbol\delta_a^*=\operatorname*{argmin}_{\boldsymbol\delta\in\mathbb R^{d+1}}E[\mathbb 1_{\{A_1=a_1\}}[\phi(\mathbf U^\top\boldsymbol\delta)-\mathbb 1_{\{A_2=a_2\}}\mathbf U^\top\boldsymbol\delta]],\quad\mathbf U=(1,\mathbf S)^\top\in\mathbb R^{d+1}.\tag{2.2}
\]
''',[5],'Section 2.1 — logistic working models, equations (2.1)-(2.2)',{'D7':'The objectives use phi and the response models use g.','D4':'The two minimizers approximate the defined first- and second-time propensity scores.'},phrases=['population minimizer'],symbols=[r'\pi_a^*(\mathbf s_1)',r'\rho_a^*(\mathbf s)',r'\boldsymbol\gamma_a^*',r'\boldsymbol\delta_a^*'],shape='Two distinct logistic population projections, one unconditional and one weighted by the first-stage treatment indicator; no model-correctness restriction is part of minimization.')
add('D10','best linear working model',r'''
The best linear working model for the second-time conditional mean $\nu_a(\cdot)=E[Y\mid\mathbf S,A_1=a_1,A_2=a_2]$ is denoted as
\[
\nu_a^*(\mathbf s)=\mathbf u^\top\boldsymbol\alpha_a^*,\qquad\boldsymbol\alpha_a^*:=\operatorname*{argmin}_{\boldsymbol\alpha\in\mathbb R^{d+1}}E[\mathbb 1_{\{A_1=a_1,A_2=a_2\}}(Y-\mathbf U^\top\boldsymbol\alpha)^2].\tag{2.5}
\]
''',[5],'Section 2.1 — second-time linear working model, equation (2.5)',{'D3':'This approximates the second-time conditional mean; its observed-outcome identification uses the separately asserted causal hypotheses.'},phrases=['best linear working model'],symbols=[r'\nu_a^*(\mathbf s)',r'\boldsymbol\alpha_a^*'],shape='Treatment-path-weighted least-squares projection of observed Y on the augmented full covariate vector; no logistic or DR projection is needed to define it.')
add('D11','DR imputed outcome',r'''
Recall that $\boldsymbol\delta_a^*$ and $\boldsymbol\alpha_a^*$ are defined in Equations (2.2) and (2.5), respectively. We propose the following DR imputed outcome
\[
Y^{DR}:=\mathbf U^\top\boldsymbol\alpha_a^*+\mathbb 1_{\{A_2=a_2\}}\frac{Y-\mathbf U^\top\boldsymbol\alpha_a^*}{g(\mathbf U^\top\boldsymbol\delta_a^*)}.
\]
''',[5],'Section 2.1 — population DR imputed outcome',{'D9':'The denominator uses the population second-stage logistic projection.','D10':'Both the baseline and residual use the second-time linear projection.'},phrases=['DR imputed outcome'],symbols=[r'Y^{DR}'],shape='Augmented inverse-propensity pseudo-outcome using population working parameters, not a claim that its conditional mean always equals the true mean.')
add('D12','linear working model',r'''
With this in mind, we consider a linear working model for the first-time conditional mean
\[
\mu_a^*(\mathbf s_1)=\mathbf v^\top\boldsymbol\beta_a^*,\qquad\boldsymbol\beta_a^*:=\operatorname*{argmin}_{\boldsymbol\beta\in\mathbb R^{d_1+1}}E[\mathbb 1_{\{A_1=a_1\}}(Y^{DR}-\mathbf V^\top\boldsymbol\beta)^2].\tag{2.9}
\]
''',[6],'Section 2.1 — first-time DR linear working model, equation (2.9)',{'D11':'The projection response is the population DR imputed outcome.','D3':'This is the S-DRL working approximation of the first-time conditional mean.'},phrases=['linear working model'],symbols=[r'\mu_a^*(\mathbf s_1)',r'\boldsymbol\beta_a^*'],shape='First-treatment-weighted linear projection of YDR; it is distinct from the nested projection even when the true first-time mean is linear.')
add('D13','best linear working model',r'''
Based on the best linear approximation $\nu_a^*(\mathbf s)=\mathbf u^\top\boldsymbol\alpha_a^*$, (2.5), of $\nu_a(\cdot)$, we introduce the following nested “best linear working model”:
\[
\mu_{a,NR}^*(\mathbf s_1)=\mathbf v^\top\boldsymbol\beta_{a,NR}^*,\qquad\boldsymbol\beta_{a,NR}^*:=\operatorname*{argmin}_{\boldsymbol\beta\in\mathbb R^{d_1+1}}E[\mathbb 1_{\{A_1=a_1\}}(\mathbf U^\top\boldsymbol\alpha_a^*-\mathbf V^\top\boldsymbol\beta)^2].\tag{2.14}
\]
Note that the two linear working models $\mu_{a,NR}^*(\cdot)$ and $\mu_a^*(\cdot)$ are not necessarily the same; see Section 2.3 for detailed comparisons.
''',[7],'Section 2.2 — nested first-time working model, equation (2.14)',{'D10':'The nested response is the second-time linear projection.','D3':'The nested model approximates the first-time conditional mean, with correctness imposed separately.'},phrases=['best linear working model'],symbols=[r'\mu_{a,NR}^*(\mathbf s_1)',r'\boldsymbol\beta_{a,NR}^*'],shape='Nested linear projection; its comparison with mu-star is contextual and does not make the DR projection a defining prerequisite.')
add('D14','regularization',r'''
With a subset of training data $\mathcal D_{\mathcal J}=\{W_i\}_{i\in\mathcal J}\subset\mathcal D$, where $\mathcal J\subset\{1,\ldots,N\}$, we define
\[
\widehat{\boldsymbol\gamma}_a:=\widehat{\boldsymbol\gamma}_a(\mathcal D_{\mathcal J})=\operatorname*{argmin}_{\boldsymbol\gamma\in\mathbb R^{d_1+1}}\frac1{|\mathcal J|}\sum_{i\in\mathcal J}[\phi(\mathbf V_i^\top\boldsymbol\gamma)-\mathbb 1_{\{A_{1i}=a_1\}}\mathbf V_i^\top\boldsymbol\gamma]+\lambda_\gamma\|\boldsymbol\gamma\|_1,\tag{2.3}
\]
\[
\widehat{\boldsymbol\delta}_a:=\widehat{\boldsymbol\delta}_a(\mathcal D_{\mathcal J})=\operatorname*{argmin}_{\boldsymbol\delta\in\mathbb R^{d+1}}\frac1{|\mathcal J|}\sum_{i\in\mathcal J}\mathbb 1_{\{A_{1i}=a_1\}}[\phi(\mathbf U_i^\top\boldsymbol\delta)-\mathbb 1_{\{A_{2i}=a_2\}}\mathbf U_i^\top\boldsymbol\delta]+\lambda_\delta\|\boldsymbol\delta\|_1,\tag{2.4}
\]
with tuning parameters $\lambda_\gamma,\lambda_\delta>0$.
''',[5],'Section 2.1 — regularized propensity estimates, equations (2.3)-(2.4)',{'D7':'The sample objectives use the softplus primitive phi.','D8':'Both estimators use a specified subset of the observed i.i.d. sample.'},context=r'Throughout this work, we focus on the $\ell_1$-regularization, albeit the theoretical developments apply more broadly.',symbols=[r'\widehat{\boldsymbol\gamma}_a',r'\widehat{\boldsymbol\delta}_a'],shape='Two l1-penalized logistic sample objectives, with first-stage filtering only in the second model; population targets and consistency assumptions are separate.')
add('D15','estimator',r'''
An estimator of (2.5) can be obtained similarly with $\lambda_\alpha>0$:
\[
\widehat{\boldsymbol\alpha}_a:=\widehat{\boldsymbol\alpha}_a(\mathcal D_{\mathcal J})=\operatorname*{argmin}_{\boldsymbol\alpha\in\mathbb R^{d+1}}\frac1{|\mathcal J|}\sum_{i\in\mathcal J}\mathbb 1_{\{A_{1i}=a_1,A_{2i}=a_2\}}(Y_i-\mathbf U_i^\top\boldsymbol\alpha)^2+\lambda_\alpha\|\boldsymbol\alpha\|_1.\tag{2.6}
\]
''',[5],'Section 2.1 — second-time outcome estimator, equation (2.6)',{'D8':'The regression objective uses the given training observations.'},phrases=['estimator'],symbols=[r'\widehat{\boldsymbol\alpha}_a'],shape='Treatment-path-filtered least-squares Lasso with normalization by the entire training subset size; all coordinates, including intercept, appear in the printed penalty.')
add('D16','DR estimate',r'''
To estimate the best linear slope $\boldsymbol\beta_a^*$ based on a subset of training data $\mathcal D_{\mathcal J}\subset\mathcal D$, we consider an additional sample splitting with $\mathcal D_{\mathcal J}=\mathcal D_{\mathcal J_1}\cup\mathcal D_{\mathcal J_2}$, where $\mathcal J_1$ and $\mathcal J_2$ are disjoint subsets of $\mathcal J$. Using the first half of the subsamples $\mathcal D_{\mathcal J_1}$, we first obtain the second-time nuisance estimates $\widetilde{\boldsymbol\delta}_a:=\widehat{\boldsymbol\delta}_a(\mathcal D_{\mathcal J_1})$ and $\widetilde{\boldsymbol\alpha}_a:=\widehat{\boldsymbol\alpha}_a(\mathcal D_{\mathcal J_1})$ as (2.4) and (2.6), respectively. Then, for each $i\in\mathcal J_2$, we construct a DR imputed outcome
\[
\widehat Y_i^{DR}:=\mathbf U_i^\top\widetilde{\boldsymbol\alpha}_a+\mathbb 1_{\{A_{2i}=a_2\}}\frac{Y_i-\mathbf U_i^\top\widetilde{\boldsymbol\alpha}_a}{g(\mathbf U_i^\top\widetilde{\boldsymbol\delta}_a)}.\tag{2.10}
\]
Based on the DR imputed outcomes $\widehat Y_{\mathcal J_2}^{DR}:=\{\widehat Y_i^{DR}\}_{i\in\mathcal J_2}$, we propose a DR estimate:
\[
\widehat{\boldsymbol\beta}_a:=\widehat{\boldsymbol\beta}_a(\mathcal D_{\mathcal J_2},\widehat Y_{\mathcal J_2}^{DR})=\operatorname*{argmin}_{\boldsymbol\beta\in\mathbb R^{d_1+1}}\frac1{|\mathcal J_2|}\sum_{i\in\mathcal J_2}\mathbb 1_{\{A_{1i}=a_1\}}(\widehat Y_i^{DR}-\mathbf V_i^\top\boldsymbol\beta)^2+\lambda_\beta\|\boldsymbol\beta\|_1,\tag{2.11}
\]
where $\lambda_\beta>0$. To regain full sample size efficiency, we can always swap the samples $\mathcal D_{\mathcal J_1}$ and $\mathcal D_{\mathcal J_2}$, repeat the procedure, and average the results.
''',[6],'Section 2.1 — DR imputation and fitted slope, equations (2.10)-(2.11)',{'D14':'One half-sample fits the second-stage propensity estimator.','D15':'The same half-sample fits the second-time outcome slope.','D7':'Imputation uses the logistic function evaluated at the fitted propensity slope.'},phrases=['DR estimate'],symbols=[r'\widehat Y_i^{DR}',r'\widehat{\boldsymbol\beta}_a'],shape='Split-sample pseudo-outcome and weighted Lasso fit, including the source swap-and-average instruction; population beta-star is an estimation target, not an input to the algorithm.')
add('D17','imputed Lasso estimate',r'''
We consider the following imputed Lasso estimate of $\boldsymbol\beta_{a,NR}^*$, defined as $\widehat{\boldsymbol\beta}_{a,NR}:=\widehat{\boldsymbol\beta}_{a,NR}(\mathcal D_{\mathcal J},\widehat{\boldsymbol\alpha}_a)$ with
\[
\widehat{\boldsymbol\beta}_{a,NR}:=\operatorname*{argmin}_{\boldsymbol\beta\in\mathbb R^{d_1+1}}\frac1{|\mathcal J|}\sum_{i\in\mathcal J}\mathbb 1_{\{A_{1i}=a_1\}}(\mathbf U_i^\top\widehat{\boldsymbol\alpha}_a-\mathbf V_i^\top\boldsymbol\beta)^2+\lambda_\beta\|\boldsymbol\beta\|_1.\tag{2.15}
\]
''',[7],'Section 2.2 — nested imputed Lasso estimate, equation (2.15)',{'D15':'The nested response uses the fitted second-time outcome slope.'},phrases=['imputed Lasso estimate'],symbols=[r'\widehat{\boldsymbol\beta}_{a,NR}'],shape='Nested first-treatment-weighted Lasso; no inner split or propensity correction is present in the printed objective.')
add('D18','DR score function',r'''
For each $c\in\{a,a'\}$ and for any $\boldsymbol\eta=(\boldsymbol\alpha,\boldsymbol\beta,\boldsymbol\gamma,\boldsymbol\delta)$, define the DR score function based on the DR representation (1.2):
\[
\psi_c(W;\boldsymbol\eta):=\mathbf V^\top\boldsymbol\beta+\mathbb 1_{\{A_1=c_1\}}\frac{\mathbf U^\top\boldsymbol\alpha-\mathbf V^\top\boldsymbol\beta}{g(\mathbf V^\top\boldsymbol\gamma)}+\mathbb 1_{\{A_1=c_1,A_2=c_2\}}\frac{Y-\mathbf U^\top\boldsymbol\alpha}{g(\mathbf V^\top\boldsymbol\gamma)g(\mathbf U^\top\boldsymbol\delta_c)}.\tag{2.12}
\]
''',[6],'Section 2.1 — parametric DR score, equation (2.12)',{'D7':'The two denominators use the logistic response.','D1':'The score evaluates the observed outcome and two-stage assignment indicators.'},phrases=['DR score function'],symbols=[r'\psi_c(W;\boldsymbol\eta)'],note='Equation (2.12) prints delta_c in the final denominator although the argument tuple binds delta without c. This source inconsistency is retained.',shape='Parametric score on an observation and four coefficient vectors, with a source subscript discrepancy; no estimator or population minimizer is an input prerequisite.')
add('D19','Sequential Double Robust Lasso',r'''
Require: Observations $\mathcal D:=\{W_i\}_{i=1}^N=(Y_i,\mathbf S_{1i},A_{1i},\mathbf S_{2i},A_{2i})_{i=1}^N$, treatment path $a$, and control $a'$.

1: For any $K\geq2$, let $\mathbb K=\{1,2,\ldots,K\}$. Randomly split $\mathcal I=\{1,\ldots,N\}$ into $K$ equal-sized $|\mathcal I_k|=n$. Define $\mathcal I_{-k}:=\mathcal I\setminus\mathcal I_k$, and further split $\mathcal I_{-k}$ into two equal-sized sets $\mathcal I_{-k,1}$ and $\mathcal I_{-k,2}$.

2: Let $\mathcal W_{-k}:=\{W_i\}_{i\in\mathcal I_{-k}}$ and $\mathcal W_{-k,j}:=\{W_i\}_{i\in\mathcal I_{-k,j}}$ for each $j\in\{1,2\}$.

3: for $k=1,2,\ldots,K$ do

4: for $c\in\{a,a'\}$ do

5: Using $\mathcal W_{-k}$, construct estimates $\widehat{\boldsymbol\gamma}_c$, $\widehat{\boldsymbol\delta}_c$, and $\widehat{\boldsymbol\alpha}_c$ through (2.3), (2.4), and (2.6), respectively.

6: Using $\mathcal W_{-k,1}$, construct estimates $\widetilde{\boldsymbol\delta}_c$ and $\widetilde{\boldsymbol\alpha}_c$ through (2.4) and (2.6), respectively.

7: For each $i\in\mathcal I_{-k,2}$, set $\widehat Y_i^{DR}$ as defined in (2.10) with $\widetilde{\boldsymbol\delta}_c$ and $\widetilde{\boldsymbol\alpha}_c$ from Step 6.

8: Compute $\widehat{\boldsymbol\beta}_{c,1}$ through (2.11) based on the training samples $\mathcal W_{-k,2}$.

9: Exchange $\mathcal W_{-k,1}$ and $\mathcal W_{-k,2}$, repeat Steps 6-8 and obtain $\widehat{\boldsymbol\beta}_{c,2}$ analogously. Compute
\[
\widehat{\boldsymbol\beta}_c=(\widehat{\boldsymbol\beta}_{c,1}+\widehat{\boldsymbol\beta}_{c,2})/2.\tag{2.7}
\]
10: end for

11: Let $\widehat{\boldsymbol\eta}_c=(\widehat{\boldsymbol\alpha}_c,\widehat{\boldsymbol\beta}_c,\widehat{\boldsymbol\gamma}_c,\widehat{\boldsymbol\delta}_c)$. Using the DR score (2.12), compute $\check\theta^{(k)}$ as
\[
\check\theta^{(k)}=|\mathcal I_k|^{-1}\sum_{i\in\mathcal I_k}[\psi_a(W_i;\widehat{\boldsymbol\eta}_a)-\psi_{a'}(W_i;\widehat{\boldsymbol\eta}_{a'})].
\]
12: end for

return The S-DRL estimator and the variance estimate
\[
\widehat\theta:=K^{-1}\sum_{k\in\mathbb K}\check\theta^{(k)},\qquad\widehat\sigma^2:=N^{-1}\sum_{k\in\mathbb K,i\in\mathcal I_k}[\psi_a(W_i;\widehat{\boldsymbol\eta}_a)-\psi_{a'}(W_i;\widehat{\boldsymbol\eta}_{a'})-\widehat\theta]^2.\tag{2.8}
\]
''',[6],'Algorithm 1 — Sequential Double Robust Lasso (S-DRL)',{'D14':'Steps 5-6 fit the penalized propensity models.','D15':'Steps 5-6 fit the second-time outcome slopes.','D16':'Steps 7-9 impute, fit and average the two first-time slopes.','D18':'Step 11 and both returned quantities evaluate the parametric score.'},kind='source_passage',context='Algorithm 1 Sequential Double Robust Lasso (S-DRL)',symbols=[r'\widehat\theta',r'\widehat\sigma^2',r'\widehat{\boldsymbol\beta}_c'],shape='Complete outer cross-fitting and inner split/swap algorithm, with both contrast and empirical variance outputs; equal fold and half-fold sizes are required by the printed procedure.')
add('D20','Dynamic Treatment Lasso',r'''
Require: Observations $\{W_i\}_{i=1}^N$, number of cross-fitting subsets $K\geq2$, treatment path $a$, and control $a'$.

1: For any $K\geq2$, let $\mathbb K=\{1,2,\ldots,K\}$. Randomly split $\mathcal I=\{1,\ldots,N\}$ into $K$ equal-sized $|\mathcal I_k|=n$ with $\mathcal I_{-k}=\mathcal I\setminus\mathcal I_k$ and $\mathcal W_{-k}=\{W_i\}_{i\in\mathcal I_{-k}}$.

2: for $k=1,2,\ldots,K$ do

3: for $c\in\{a,a'\}$ do

4: Using $\mathcal W_{-k}$, construct estimates $\widehat{\boldsymbol\gamma}_c$, $\widehat{\boldsymbol\delta}_c$, and $\widehat{\boldsymbol\alpha}_c$ through (2.3), (2.4), and (2.6), respectively.

5: Compute $\widehat{\boldsymbol\beta}_{c,NR}$ as (2.15) based on the training samples $\mathcal W_{-k}$ and the nuisance estimate $\widehat{\boldsymbol\alpha}_c$.

6: end for

7: Using the DR score (2.12) and let $\widehat{\boldsymbol\eta}_{c,NR}=(\widehat{\boldsymbol\alpha}_c,\widehat{\boldsymbol\beta}_{c,NR},\widehat{\boldsymbol\gamma}_c,\widehat{\boldsymbol\delta}_c)$, compute $\check\theta_{DTL}^{(k)}$ as
\[
\check\theta_{DTL}^{(k)}=|\mathcal I_k|^{-1}\sum_{i\in\mathcal I_k}[\psi_a(W_i;\widehat{\boldsymbol\eta}_{a,NR})-\psi_{a'}(W_i;\widehat{\boldsymbol\eta}_{a',NR})].
\]
8: end for

return The DTL estimator and the variance estimate
\[
\widehat\theta_{DTL}:=K^{-1}\sum_{k\in\mathbb K}\check\theta_{DTL}^{(k)},\qquad\widehat\sigma_{DTL}^2:=N^{-1}\sum_{k\in\mathbb K,i\in\mathcal I_k}[\psi_a(W_i;\widehat{\boldsymbol\eta}_{a,NR})-\psi_{a'}(W_i;\widehat{\boldsymbol\eta}_{a',NR})-\widehat\theta_{DTL}]^2.\tag{2.13}
\]
''',[7],'Algorithm 2 — Dynamic Treatment Lasso (DTL)',{'D14':'Step 4 fits the same propensity estimators as in Algorithm 1.','D15':'Step 4 fits the second-time outcome slope.','D17':'Step 5 uses the nested fitted response instead of DR imputation.','D18':'The returned contrast and variance use the parametric DR score.'},kind='source_passage',context='Algorithm 2 Dynamic Treatment Lasso (DTL)',symbols=[r'\widehat\theta_{DTL}',r'\widehat\sigma_{DTL}^2'],shape='Complete DTL outer cross-fitting algorithm, with no inner half-sample split; retain fold-local nuisance fits even though the printed notation suppresses k.')
residual=r'''Define $\zeta_a:=\mathbb 1_{\{A_1=a_1,A_2=a_2\}}(Y(a)-\nu_a^*(\mathbf S))$, $\varepsilon_a:=\mathbb 1_{\{A_1=a_1\}}(\nu_a^*(\mathbf S)-\mu_a^*(\mathbf S_1))$ and let $\zeta:=\zeta_a+\zeta_{a'}$, $\varepsilon:=\varepsilon_a+\varepsilon_{a'}$.'''
variance=r'''\[
\sigma^2:=E[\psi_a(W;\boldsymbol\eta_a^*)-\psi_{a'}(W;\boldsymbol\eta_{a'}^*)-\theta]^2,\tag{3.1}
\]
where $\psi_c(\cdot;\cdot)$ is defined in (2.12) and $\boldsymbol\eta_c^*:=(\boldsymbol\alpha_c^*,\boldsymbol\beta_c^*,\boldsymbol\gamma_c^*,\boldsymbol\delta_c^*)$.'''
tails=r'''Suppose that there exist positive constants $\sigma_\zeta<\infty$ and $\sigma_\varepsilon<\infty$, such that $\zeta$ and $\varepsilon$ are sub-Gaussian, with $\|\zeta\|_{\psi_2}\leq\sigma\sigma_\zeta$, $\|\varepsilon\|_{\psi_2}\leq\sigma\sigma_\varepsilon$, and'''
rescontext=r'A sufficient condition for Assumption 2 is $\|\zeta/\sqrt{E[\zeta^2]}\|_{\psi_2}\leq\sigma_\zeta$ and $\|\varepsilon/\sqrt{E[\varepsilon^2]}\|_{\psi_2}\leq\sigma_\varepsilon$, i.e., the “normalized” residuals have constant $\psi_2$-norms.'
for suffix,target in [('', 'D12'),('NR','D13')]:
 add('D21'+suffix,'residuals',residual,[10],'Assumption 2 — residual definitions'+(' (DTL application)' if suffix else ''),{'D10':'Zeta and epsilon use the population second-time linear projection.',target:'Epsilon uses the first-time working model of this application.'},context=rescontext,symbols=[r'\zeta_a',r'\varepsilon_a'],shape='Treatment-filtered residual sums over the two paths; only the defining fragment of Assumption 2, not its sub-Gaussian hypothesis.')
 add('D22'+suffix,'variance',variance,[10],'Assumption 2 — score second moment, equation (3.1)'+(' (DTL application)' if suffix else ''),{'D18':'Equation (3.1) squares the centered contrast of parametric scores.','D2':'The centering is the true DTE.','D9':'Eta-star includes both logistic population minimizers.','D10':'Eta-star includes the second-time outcome projection.',target:'Eta-star includes the application-specific first-time slope.'},context='return The S-DRL estimator and the variance estimate',symbols=[r'\sigma^2'],shape='Second moment about the true DTE of the population fitted score contrast; not automatically its variance under arbitrary misspecification.')
 members['D22'+suffix]['naming_context'][0]['evidence']=[dict(page=6,location='Algorithm 1 — variance estimate return label')]
 add('D23'+suffix,'sub-Gaussian',residual+'\n\n'+tails+'\n\n'+variance,[10],'Assumption 2'+(' — DTL application' if suffix else ''),{'D21'+suffix:'The tail bound is on the defined sums of residuals.','D22'+suffix:'Both Orlicz bounds are scaled by the population score second moment.','D6':'Sub-Gaussianity is expressed using the source psi2-Orlicz norm.'},kind='assumption',phrases=['sub-Gaussian','Assumption 2'],shape='Full Assumption 2, retaining residual definitions, score scale and fixed positive normalized tail constants.')
 if suffix:
  for lid in ['D21NR','D22NR','D23NR']:
   members[lid]['application_context']=[dict(text=r'Let Assumptions 1-4 hold with $\mu_a^*(\cdot)$ and $\boldsymbol\beta_a^*$ replaced by $\mu_{a,NR}^*(\cdot)$ and $\boldsymbol\beta_{a,NR}^*$.',evidence=[dict(page=11,location='Theorem 4 — explicit replacement instruction')]),dict(text=r'Let Assumptions 1-3 hold with $\mu_a^*(\cdot)$ and $\boldsymbol\beta_a^*$ replaced by $\mu_{a,NR}^*(\cdot)$ and $\boldsymbol\beta_{a,NR}^*$.',evidence=[dict(page=12,location='Theorem 5 — explicit replacement instruction')])]
   members[lid]['variant_note']='Theorem 4 and Theorem 5 explicitly substitute the nested first-time model and slope. The archived Assumption 2 wording is unchanged; its application-specific dependency path records the substitution.'
add('D24','sub-Gaussian vector',r'''
Let $\mathbf U$ be a sub-Gaussian vector such that $\|\mathbf x^\top\mathbf U\|_{\psi_2}\leq\sigma_u\|\mathbf x\|_2$ for $\mathbf x\in\mathbb R^{d+1}$ and $\sigma_u>0$. Let $\lambda_{\min}(E[\mathbf U\mathbf U^\top\mathbb 1_{\{A_1=a_1\}}])\geq\kappa_l$ for any $a_1\in\{0,1\}$, with $\kappa_l>0$.
''',[10],'Assumption 3',{'D6':'All linear projections are bounded in psi2-Orlicz norm.','D1':'U augments the full covariate vector with an intercept and the Gram bound is treatment-filtered.'},kind='assumption',phrases=['sub-Gaussian vector','Assumption 3'],shape='Sub-Gaussian augmented covariates and uniform positive treatment-weighted population Gram eigenvalue for both first-stage assignments.')
add('D25','overlap condition',r'''
Let $\pi_a^*(\cdot)$ and $\rho_a^*(\cdot)$ be such that $P(c_0\leq\pi_a^*(\mathbf S_1)\leq1-c_0)=1$, $P(c_0\leq\rho_a^*(\mathbf S)\leq1-c_0)=1$, for a fixed constant $c_0>0$.
''',[10],'Assumption 4',{'D3':'The bounds concern working propensity functions, which may be general functions in Section 3.3.'},kind='assumption',context='The following Assumption 4 is an overlap condition for the working propensity score models, which is additionally required only when model misspecification occurs.',symbols=[r'\pi_a^*(\mathbf S_1)',r'\rho_a^*(\mathbf S)'],phrases=['Assumption 4'],shape='Almost-sure fixed two-sided bounds on working propensity models; no linear/logistic specification is built into this condition.')
add('D26','general DR DTE estimator',r'''
For any $K\geq2$, randomly split $\mathcal I=\{1,\ldots,N\}$ into $K$ equal-sized parts with $|\mathcal I_k|=n=N/K$. For the sake of simplicity, we consider $n$ as an integer. Based on the training samples $\mathcal W_{-k}$, construct $\widehat\nu_{c,-k}(\cdot)$, $\widehat\mu_{c,-k}(\cdot)$, $\widehat\pi_{c,-k}(\cdot)$, and $\widehat\rho_{c,-k}(\cdot)$ as estimates of the nuisance functions $\nu_c(\cdot)$, $\mu_c(\cdot)$, $\pi_c(\cdot)$, and $\rho_c(\cdot)$, respectively. For each $c\in\{a,a'\}$, let
\[
\widehat\psi_{c,-k}(W):=\widehat\mu_{c,-k}(\mathbf S_1)+\mathbb 1_{\{A_1=c_1\}}\frac{\widehat\nu_{c,-k}(\mathbf S)-\widehat\mu_{c,-k}(\mathbf S_1)}{\widehat\pi_{c,-k}(\mathbf S_1)}+\mathbb 1_{\{A_1=c_1,A_2=c_2\}}\frac{Y-\widehat\nu_{c,-k}(\mathbf S)}{\widehat\pi_{c,-k}(\mathbf S_1)\widehat\rho_{c,-k}(\mathbf S)}.\tag{2.16}
\]
The general DR DTE estimator and the corresponding variance estimate are then defined with $\widehat\Delta_{-k}(\cdot)=\widehat\psi_{a,-k}(\cdot)-\widehat\psi_{a',-k}(\cdot)$ and $\mathbb K=\{1,\cdots,K\}$ as
\[
\widehat\theta_{gen}:=\frac1N\sum_{k\in\mathbb K,i\in\mathcal I_k}\widehat\Delta_{-k}(W_i),\qquad\widehat\sigma_{gen}^2:=\frac1N\sum_{k\in\mathbb K,i\in\mathcal I_k}[\widehat\Delta_{-k}(W_i)-\widehat\theta_{gen}]^2.\tag{2.17}
\]
''',[9],'Section 2.4 — general fitted DR score, estimator and variance',{'D8':'The cross-fitting partition acts on the observed sample.','D3':'The nuisance estimates target the general conditional means and propensity functions.'},phrases=['general DR DTE estimator'],symbols=[r'\widehat\theta_{gen}',r'\widehat\sigma_{gen}^2'],shape='Cross-fitted DR contrast and empirical variance for arbitrary supplied nuisance-fitting strategies; neither Algorithm 1 nor Algorithm 2 is prescribed.')
add('D27','DR score function',r'''
In this section, we provide a new consistency result of the general DR DTE estimator. Here we consider arbitrary working models $\pi_a^*(\cdot)$, $\rho_a^*(\cdot)$, $\mu_a^*(\cdot)$, and $\nu_a^*(\cdot)$, which may not follow the logistic or linear forms as before. For each $c\in\{a,a'\}$, define the corresponding DR score function as
\[
\psi_c^*(W):=\mu_c^*(\mathbf S_1)+\mathbb 1_{\{A_1=c_1\}}\frac{\nu_c^*(\mathbf S)-\mu_c^*(\mathbf S_1)}{\pi_c^*(\mathbf S_1)}+\mathbb 1_{\{A_1=c_1,A_2=c_2\}}\frac{Y-\nu_c^*(\mathbf S)}{\pi_c^*(\mathbf S_1)\rho_c^*(\mathbf S)},\tag{3.5}
\]
with
\[
\sigma^2:=E[\psi_a^*(W)-\psi_{a'}^*(W)-\theta]^2.\tag{3.6}
\]
''',[12],'Section 3.3 — general population DR score and second moment',{'D3':'Equation (3.5) uses arbitrary working nuisance functions.','D2':'Equation (3.6) centers their score contrast at the true DTE.'},phrases=['DR score function'],symbols=[r'\psi_c^*(W)',r'\sigma^2'],shape='General-function score and its second moment about the DTE, distinct from the parametric score definition and its coefficient targets.')
add('D28','residuals',residual,[10],'Assumption 2 — residual definitions used in Section 3.3',{'D3':'Section 3.3 allows arbitrary working means in the same residual formulas.'},context=rescontext,symbols=[r'\zeta_a',r'\varepsilon_a'],note='Assumption 5 refers to the residual definitions in Assumption 2, not to its sub-Gaussian restriction. Section 3.3 explicitly replaces the parametric working functions by arbitrary working models.',shape='The residual formulas interpreted with the general Section 3.3 working functions; no parametric projections or sub-Gaussian hypotheses are imported.')
members['D28']['application_context']=[dict(text=r'Here we consider arbitrary working models $\pi_a^*(\cdot)$, $\rho_a^*(\cdot)$, $\mu_a^*(\cdot)$, and $\nu_a^*(\cdot)$, which may not follow the logistic or linear forms as before.',evidence=[dict(page=12,location='Section 3.3 — scope of working models')])]
add('D29','centered conditional effect',r'''
where $\xi:=\mu_a(\mathbf S_1)-\mu_{a'}(\mathbf S_1)-\theta$ denotes the centered conditional effect at the first exposure.
''',[10],'Discussion after Assumption 3 — centered conditional effect',{'D3':'Xi uses the true first-time conditional means.','D2':'Xi is centered at their population DTE.'},phrases=['centered conditional effect'],symbols=[r'\xi'],shape='True first-time conditional DTE minus its population mean; the surrounding sufficient-condition discussion is not an extra hypothesis.')
add('D30',['overlap condition','conditional second moments'],r'''
For positive sequences $a_N=o(\sigma)$, $b_N=o(\sigma)$, $c_N=o(1)$, and $d_N=o(1)$, let $E[\widehat\nu_a(\mathbf S)-\nu_a^*(\mathbf S)]^2=O_p(a_N^2)$, $E[\widehat\mu_a(\mathbf S_1)-\mu_a^*(\mathbf S_1)]^2=O_p(b_N^2)$, $E[\widehat\pi_a(\mathbf S_1)-\pi_a^*(\mathbf S_1)]^2=O_p(c_N^2)$, and $E[\widehat\rho_a(\mathbf S)-\rho_a^*(\mathbf S)]^2=O_p(d_N^2)$. Moreover, for $c_0\in(0,1/2)$, $P(c_0\leq\widehat\pi_a(\mathbf S_1)\leq1-c_0)=1$ and $P(c_0\leq\widehat\rho_a(\mathbf S)\leq1-c_0)=1$ with probability approaching one. For $\zeta$ and $\varepsilon$ defined in Assumption 2, $\max\{E|\zeta|^q/[E|\zeta|^2]^{q/2},E|\varepsilon|^q/[E|\varepsilon|^2]^{q/2},E|\xi|^q/[E|\xi|^2]^{q/2}\}\leq C$, $P(E[\zeta^2\mid\mathbf S]\leq CE[\zeta^2])=1$, and $P(E[\varepsilon^2\mid\mathbf S_1]\leq CE[\varepsilon^2])=1$, for constants $C>0$ and $q>2$.
''',[13],'Assumption 5',{'D26':'The estimated nuisance functions come from the general cross-fitting procedure.','D27':'The rate scales use the general score second moment sigma.','D28':'The moment conditions use the named residual definitions only.','D29':'The third normalized q-th moment is that of the centered true conditional effect.'},kind='assumption',context=r'Note that Assumption 5 allows for $\rho_a^*(\cdot)$ to differ from $\rho_a(\cdot)$ while requiring a overlap condition consistent with the existing literature; see, e.g., Chernozhukov et al. (2018). The max condition, satisfied by sub-Gaussian random variables, controls the tails of $\zeta$, $\varepsilon$, and $\xi$. The last two conditions of Assumption 5 aim to ensure the interpretability of the results by bounding the “normalized” conditional second moments.',phrases=['Assumption 5'],symbols=[r'a_N',r'b_N',r'c_N',r'd_N'],shape='Four prediction rates, fitted-overlap event and normalized residual/conditional moments; fresh-covariate expectations conditional on fitted functions, not training-sample averages.')
add('D31','imputed-Lasso estimator',r'''
Let $\mathcal S:=(Y_i^*,\mathbf X_i)_{i=1}^M$ be i.i.d. observations and let $(Y^*,\mathbf X)$ be an independent copy with $Y^*\in\mathbb R$ and $\mathbf X\in\mathbb R^d$. Suppose that there exists, possibly random, $\widehat Y_i\in\mathbb R$. Note that for some, and possibly all observations, outcomes $Y^*$ are imputed, i.e., estimated using $\widehat Y_i$. The true population slope is defined as $\boldsymbol\beta^*=\operatorname*{argmin}_{\boldsymbol\beta\in\mathbb R^d}E[Y^*-\mathbf X^\top\boldsymbol\beta]^2$. Then its estimator is
\[
\widehat{\boldsymbol\beta}:=\operatorname*{argmin}_{\boldsymbol\beta\in\mathbb R^d}\left\{M^{-1}\sum_{i=1}^M[\widehat Y_i-\mathbf X_i^\top\boldsymbol\beta]^2+\lambda_M\|\boldsymbol\beta\|_1\right\},\tag{4.1}
\]
for $\lambda_M>0$. The following result delineates properties of such imputed-Lasso estimator, $\widehat{\boldsymbol\beta}$.
''',[14,15],'Section 4.1 — general imputed Lasso, equation (4.1)',phrases=['imputed-Lasso estimator'],symbols=[r'\boldsymbol\beta^*',r'\widehat{\boldsymbol\beta}'],shape='Separate generic regression experiment with potentially dependent imputed responses, population projection and l1-penalized estimator; no treatment-model assumptions apply.')
add('D32','multi-stage',r'''
Consider $T\geq2$ exposure times and suppose that we observe i.i.d. samples $\{W_{T,i}\}_{i=1}^N=(\mathbf S_{1i},A_{1i},\ldots,\mathbf S_{Ti},A_{Ti},Y)_{i=1}^N$. Let $W_T:=(\mathbf S_1,A_1,\ldots,\mathbf S_T,A_T,Y)$ be an independent copy of $W_{T,i}$. For each $t\leq T$, let $\mathbf S_t\in\mathbb R^{d_t}$ and $A_t\in\{0,1\}$ denote the covariate vector and the treatment assignment at the $t$-th exposure time, respectively. Let $Y\in\mathbb R$ denote the observed outcome variable at the final stage. Denote $\bar{\mathbf S}_t:=(\mathbf S_1,\ldots,\mathbf S_t)$ and $\bar A_t:=(A_1,\ldots,A_t)$ for any $1\leq t\leq T$. Let $Y(\bar a_T)$ be the counterfactual outcome corresponding to the treatment path $\bar a_T=(a_1,\ldots,a_T)\in\{0,1\}^T$.
''',[17],'Section 5 — multi-stage observations, histories and potential outcomes',kind='source_passage',context='The objective of this section is to expand upon the methodology of sequential doubly robust estimation by considering its application in multi-stage settings.',phrases=['counterfactual outcome'],symbols=[r'W_T',r'\bar{\mathbf S}_t',r'\bar A_t'],shape='T-stage observation law, histories and potential outcomes; retains the printed unindexed Y in the sample tuple rather than silently adding i.')
add('D33',['conditional mean','propensity score'],r'''
We define the conditional mean and propensity score functions as
\[
\mu_t(\bar{\mathbf s}_t,\bar a_T):=E[Y(\bar a_T)\mid\bar{\mathbf S}_t=\bar{\mathbf s}_t,\bar A_{t-1}=\bar a_{t-1}],\quad\text{for }1\leq t\leq T+1,\tag{5.1}
\]
\[
\pi_t(\bar{\mathbf s}_t,\bar a_t):=P[A_t=a_t\mid\bar{\mathbf S}_t=\bar{\mathbf s}_t,\bar A_{t-1}=\bar a_{t-1}],\quad\text{for }1\leq t\leq T,\tag{5.2}
\]
where for the sake of simplicity, we denote with $\bar A_0=\bar a_0=\varnothing$ and $\bar{\mathbf S}_{T+1}:=(\mathbf S_1,\ldots,\mathbf S_T,Y)$. For each $1\leq t\leq T$, we denote $\mu_t^*(\bar{\mathbf s}_t,\bar a_T)$ and $\pi_t^*(\bar{\mathbf s}_t,\bar a_t)$ as the working models for the conditional mean and propensity score, respectively. Additionally, with $\bar{\mathbf S}_0=\bar{\mathbf s}_0=\varnothing$, we set $\mu_0(\bar{\mathbf s}_0,\bar a_T):=E[Y(\bar a_T)\mid\bar{\mathbf S}_0=\bar{\mathbf s}_0]=\theta_{\bar a_T}$ and $\mu_{T+1}^*(\bar{\mathbf s}_{T+1},\bar a_T):=s_{T+1}$. Note that, under the Assumption 6(b) below, we have $\mu_{T+1}^*(\bar{\mathbf S}_{T+1},\bar a_T)=\mu_{T+1}(\bar{\mathbf S}_{T+1},\bar a_T)=Y$.
''',[17],'Section 5 — multi-stage nuisance functions and terminal conventions',{'D32':'Conditional functions are indexed by multi-stage histories and treatment paths.'},phrases=['conditional mean','propensity score'],symbols=[r'\mu_t',r'\pi_t',r'\mu_{T+1}^*'],shape='General multi-stage conditional means and propensities, with empty stage-zero histories and terminal outcome convention; the terminal identity is explicitly conditional on consistency, not a reason to import the whole Assumption 6 into the definition.')
add('D34',['Sequential Ignorability','Consistency of potential outcomes','Overlap'],r'''
(a) (Sequential Ignorability) $Y(\bar a_T)\mathrel{\perp\!\!\!\perp}A_t\mid\bar{\mathbf S}_t,\bar A_{t-1}=\bar a_{t-1}$ for each $1\leq t\leq T$. (b) (Consistency of potential outcomes) $Y=Y(\bar A_T)$. (c) (Overlap) Let $c_0\in(0,1/2)$ be a positive constant, such that $P(c_0\leq\pi_t(\bar{\mathbf s}_t,\bar a_t)\leq1-c_0)=1$ for each $1\leq t\leq T$.
''',[17],'Assumption 6',{'D32':'The assumptions concern the multi-stage potential outcomes and histories.','D33':'Overlap is imposed on each true stage propensity.'},kind='assumption',phrases=['Sequential Ignorability','Consistency of potential outcomes','Overlap','Assumption 6'],shape='Multi-stage sequential causal assumptions; the source writes lower-case s-bar inside the overlap probability and that wording is retained.')
# Theorem 9 points to the averaged fit (2.7); archive its exact source instruction
# with the component-fit passage rather than importing the entire DTE algorithm.
members['D16']['statement_original']+=r'''

Exchange $\mathcal W_{-k,1}$ and $\mathcal W_{-k,2}$, repeat Steps 6-8 and obtain $\widehat{\boldsymbol\beta}_{c,2}$ analogously. Compute
\[
\widehat{\boldsymbol\beta}_c=(\widehat{\boldsymbol\beta}_{c,1}+\widehat{\boldsymbol\beta}_{c,2})/2.\tag{2.7}
\]
'''
members['D16']['excerpt_selection']='Equations (2.10)-(2.11) and their complete sample-splitting prose, followed by Algorithm 1 Step 9 specifying the averaged coefficient; both occur on page 6.'
def rename(lid,terms,context,page):
 x=next(x for x in interfaces if x['members'][0]['local_id']==lid);m=members[lid]
 m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=page,location=m['source_heading']+' — naming prose')])]
 x['source_keywords']=[]
 for term in terms:
  k=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
  if term not in m['statement_original']:
   assert term in context,(lid,term);k['context_id']=lid+'/name'
  x['source_keywords'].append(k)
 x['name']=' · '.join(k['label'] for k in x['source_keywords'])
rename('D9',['propensities','population minimizer'],r'We focus on the high-dimensional scenario, and consider linear (working) models for the conditional means $\mu_a(\cdot)$ and $\nu_a(\cdot)$, along with logistic (working) models for the propensities $\pi_a(\cdot)$ and $\rho_a(\cdot)$.',5)
rename('D10',['second-time conditional mean','best linear working model'],'The best linear working model for the second-time conditional mean',5)
rename('D12',['first-time conditional mean','linear working model'],'With this in mind, we consider a linear working model for the first-time conditional mean',6)
rename('D13',['nested','best linear working model'],'we introduce the following nested “best linear working model”:',7)
rename('D14',['regularization','propensities'],r'We focus on the high-dimensional scenario, and consider linear (working) models for the conditional means $\mu_a(\cdot)$ and $\nu_a(\cdot)$, along with logistic (working) models for the propensities $\pi_a(\cdot)$ and $\rho_a(\cdot)$. Throughout this work, we focus on the $\ell_1$-regularization, albeit the theoretical developments apply more broadly.',5)
members['D14']['naming_context'][0]['excerpt_selection']='Two original sentences from the same Section 2.1 paragraph and its following regularization paragraph; intervening formulas and feature-map discussion are omitted.'
rename('D15',['second-time conditional mean','estimator'],'The best linear working model for the second-time conditional mean',5)
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(interfaces),'source-backed interfaces.')


if __name__ == '__main__':
    main()
