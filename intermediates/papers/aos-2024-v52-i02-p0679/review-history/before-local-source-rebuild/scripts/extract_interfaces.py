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
add('D1','patient history',r'''
We focus on the DTR estimation under a longitudinal setting where data are collected over time periods indexed by $t\in\{1,2\}$. Let $O_t\in\mathcal O_t\subset\mathbb R^{p_t}$ denote the $p_t$ dimensional vector of patient clinical variables collected at time $t$ and $p=\max(p_1,p_2)$. At a given time $t$, a binary treatment decision $A_t\in\{\pm1\}$ is made for the patient and a response to such treatment $Y_t\in\mathbb R$ is observed. Without loss of generality, we assume higher values of response $Y_t$ are desirable. Let us denote the distribution underlying the observed random vector $\mathcal D=(O_1,A_1,Y_1,O_2,A_2,Y_2)$ by $\mathbb P$. Suppose we sample $n$ i.i.d. observations from $\mathbb P$. The corresponding empirical distribution function will be denoted by $\mathbb P_n$. Since treatment decisions are often made based on all previous states including prior treatments and responses, we define the patient history by
\[
H_1=O_1,\text{ and }H_2=(O_1,Y_1,O_2,A_1),
\]
where $H_1$ and $H_2$ take values in sets $\mathcal H_1$ and $\mathcal H_2$, respectively.
''',[5,6],'Section 2 — longitudinal observations and histories',kind='source_passage',phrases=['patient history'],symbols=[r'\mathbb P_n',r'H_2=(O_1,Y_1,O_2,A_1)'],shape='Iid longitudinal records with two treatment stages, binary actions coded minus/plus one, stage-specific histories and their joint law/empirical law. Within-record variables are sequential, not independent.')
members['D1']['application_context']=[dict(text=r'''Our goal is to find the treatment regime $d=(d_1,d_2):\mathcal H_1\times\mathcal H_2\mapsto\{\pm1\}\times\{\pm1\}$ that maximizes the expected sum of rewards $Y_1(d)+Y_2(d)$,
\[
V(d_1,d_2)=\mathbb E_d[Y_1(d)+Y_2(d)],
\]
where $Y_t(d)$ is the potential outcome associated with time $t\in\{1,2\}$, and $\mathbb E_d$ is the expectation with respect to the data distribution under regime $d$.''',evidence=[dict(page=6,location='Section 2 — potential outcomes under a treatment regime')])]
add('D2','propensity scores',r'''
We denote by $\pi_1(a_1\mid H_1)$ and $\pi_2(a_2\mid H_2)$ the propensity scores $\mathbb P(A_1=a_1\mid H_1)$ and $\mathbb P(A_2=a_2\mid H_2)$, respectively.
''',[6],'Section 2 — propensity scores',{'D1':'These are the conditional treatment probabilities under the longitudinal observation law given each stage’s history.'},phrases=['propensity scores'],symbols=[r'\pi_1(a_1\mid H_1)',r'\pi_2(a_2\mid H_2)'],shape='Stage-specific treatment probabilities conditional on the respective histories. Later statistical rates assume these functions are known; an estimated-propensity extension is not silently included.')
add('D3','Positivity',r'''
There exists a constant $C_\pi\in(0,1)$ so that $\pi_t(A_t\mid H_t)>C_\pi$ for all $H_t$, $t=1,2$.
''',[6],'Assumption I — Positivity',{'D2':'The strict common lower bound applies to the conditional treatment propensities.'},kind='assumption',context='I. Positivity:',symbols=[r'C_\pi\in(0,1)',r'\pi_t(A_t\mid H_t)>C_\pi'],shape='Uniform strict lower propensity bound as printed at the realized treatment A_t. The source does not explicitly quantify every possible action in this formula; no stronger actionwise condition is inserted.')
add('D4','Consistency',r'''
The observed outcomes $Y_t$ and covariates $O_t$ agree with the potential outcomes and covariates under the treatments actually received. See Schulte et al. (2014); Robins (1994) for more details.
''',[6],'Assumption II — Consistency',{'D1':'This identifies observed longitudinal variables with their potential versions along the received treatment history.'},kind='assumption',context='II. Consistency:',phrases=['Consistency'],shape='Causal consistency of observations with potential outcomes and covariates under received treatments. The source states it in words and refers externally for details; it is not expanded into a different potential-outcome system.')
add('D5','Sequential ignorability',r'''
For each $t=1,2$, the treatment assignment $A_t$ is conditionally independent of the future potential outcomes $Y_t$ and future potential clinical profile $O_{t+1}$ given $H_t$. Here we take $O_3$ to be the empty set.
''',[6],'Assumption III — Sequential ignorability',{'D1':'The condition concerns treatment assignment, potential future variables and the appropriate observed history in the two-stage model.'},kind='assumption',context='III Sequential ignorability:',phrases=['Sequential ignorability'],symbols=[r'O_3'],shape='The exact conditional-independence statement printed for each stage, with O_3 empty. The passage uses Y_t without an intervention index when referring to future potential outcomes; the audit preserves this scope instead of supplying an expanded counterfactual array.')
add('D6','conditional treatment effects',r'''
The treatment effect contrasts are defined as follows:
\[
\mathcal T_1(H_1)=\mathbb E[Y_1+U_2^*(H_2)\mid A_1=1,H_1]-\mathbb E[Y_1+U_2^*(H_2)\mid A_1=-1,H_1],\tag{1}
\]
and
\[
\mathcal T_2(H_2)=\mathbb E[Y_1+Y_2\mid A_2=1,H_2]-\mathbb E[Y_1+Y_2\mid A_2=-1,H_2],\tag{2}
\]
where
\[
U_2^*(H_2)=\max_{a_2\in\{\pm1\}}\mathbb E[Y_2\mid H_2,A_2=a_2].\tag{3}
\]
''',[6],'Section 2 — treatment effect contrasts and continuation reward, equations (1)-(3)',{'D1':'The conditional rewards and stage histories come from the longitudinal model.'},context='We will also refer to them as the first stage and the second stage conditional treatment effects.',symbols=[r'\mathcal T_1(H_1)',r'\mathcal T_2(H_2)',r'U_2^*(H_2)'],shape='The two stage-specific reward contrasts and their explicitly defined optimal second-stage continuation reward. Assumption IV and subsequent definitions use U_2^* from this original block. Finiteness is imposed separately, without a circular dependency.')
members['D6']['naming_context'][0]['evidence']=[dict(page=7,location='Section 2 continuation — conditional treatment effects')]
add('D7','conditional expectations',r'''
For any $h_2\in\mathcal H_2$, and $a_2\in\{-1,1\}$, the conditional expectation $\mathbb E[|Y_1|+|Y_2|\mid H_2=h_2,A_2=a_2]<\infty$. For any $h_1\in\mathcal H_1$, and $a_1\in\{-1,1\}$, the conditional expectation $\mathbb E[Y_1+U_2^*(H_2)\mid H_1=h_1,A_1=a_1]<\infty$. Furthermore, $\mathbb E[|Y_1+Y_2|]<\infty$.
''',[7],'Assumption IV',{'D1':'The conditional and unconditional expectations are under the longitudinal observation law.','D6':'The first-stage condition includes the continuation reward U_2^* defined in (3).'},kind='assumption',context='For the blip functions or the conditional treatment effects to be well defined, we need the conditional expectations in (1) and (2) to be finite, which is not automatically guaranteed by Assumptions I-III.',phrases=['Assumption IV'],symbols=[r'\mathbb E[|Y_1+Y_2|]<\infty'],shape='Three distinct printed integrability requirements. The second conditional expression has no absolute value, and the last controls the absolute sum rather than the sum of absolute values. The exact source statements are retained.')
add('D8','optimal DTR',r'''
We define the optimal DTR $d^*$ to be the maximizer of $\mathbb E_d[Y_1(d)+Y_2(d)]$ over all possible regimes $d=(d_1,d_2)$ such that $d_1:\mathcal H_1\mapsto\{\pm1\}$ and $d_2:\mathcal H_2\mapsto\{\pm1\}$. Under Assumptions I-III, the optimal policy $d^*$ can be identified as follows (Zhao et al., 2015; Chakraborty and Moodie, 2013)
\[
d_2^*(H_2)=\operatorname*{argmax}_{a_2\in\{\pm1\}}\mathbb E[Y_2\mid H_2,A_2=a_2]
\]
\[
d_1^*(H_1)=\operatorname*{argmax}_{a_1\in\{\pm1\}}\mathbb E[Y_1+U_2^*(H_2)\mid H_1,A_1=a_1],\tag{4}
\]
where $U_2^*$ is as defined in (3).
''',[7],'Section 2 — optimal treatment regime, equation (4)',{'D1':'The optimization is over history-dependent treatment regimes and their potential rewards.','D6':'The first-stage optimal action uses the optimal continuation reward U_2^*.','D3':'The source identification formula is stated under positivity.','D4':'The same identification formula assumes consistency.','D5':'The identification formula assumes sequential ignorability.'},phrases=['optimal DTR'],symbols=[r'd_1^*(H_1)',r'd_2^*(H_2)'],shape='Optimal regimes and their backward conditional-mean characterization under the stated causal assumptions. Ties are discussed separately. This original definition does not identify an arbitrary chosen scalar action with the entire argmax set.')
members['D8']['application_context']=[dict(text=r'Consequently, to avoid confusion, we let $d_1^*=1$ and $d_2^*=1$ at both first and second stage decision boundaries.',evidence=[dict(page=7,location='Remark 1 — start of tie convention'),dict(page=8,location='Remark 1 — continuation')])]
add('D9','measurable',r'''
\[
\mathcal F=\{(f_1,f_2)\mid f_1:\mathcal H_1\mapsto\mathbb R,\ f_2:\mathcal H_2\mapsto\mathbb R\text{ are measurable}\},\tag{6}
\]
''',[8],'Section 2 — measurable policy-score class, equation (6)',{'D1':'The two functions have the appropriate stage-specific history spaces as their domains.'},phrases=['measurable'],symbols=[r'\mathcal F'],shape='Pairs of real-valued measurable policy-score functions, one on each history space. This class excludes the extended-valued surrogate maximizers introduced subsequently; zero scores are subject to separate source conventions.')
add('D10','value function',r'''
If $(f_1^*,f_2^*)$ is a maximizer of
\[
V(f_1,f_2)=\mathbb P\left[\frac{(Y_1+Y_2)\mathbb 1[A_1f_1(H_1)>0]\mathbb 1[A_2f_2(H_2)>0]}{\pi_1(A_1\mid H_1)\pi_2(A_2\mid H_2)}\right]\tag{5}
\]
over the class
\[
\mathcal F=\{(f_1,f_2)\mid f_1:\mathcal H_1\mapsto\mathbb R,\ f_2:\mathcal H_2\mapsto\mathbb R\text{ are measurable}\},\tag{6}
\]
then $\operatorname{sign}(f_1^*)$ and $\operatorname{sign}(f_2^*)$ yield the optimal rules $d_1^*$ and $d_2^*$, respectively (Zhao et al., 2015).
''',[8],'Section 2 — score-based value, equations (5)-(6)',{'D2':'The value uses inverse weighting by both treatment propensities.','D9':'The maximization is over the real-valued measurable policy-score class.','D8':'The source connects maximizing scores to the optimal decision rules.'},context='directly optimizing the original value function.',symbols=[r'V(f_1,f_2)',r'\mathbb 1[A_1f_1(H_1)>0]'],shape='Inverse-propensity weighted population reward with strictly positive signed-score indicators, together with the source maximizing-score correspondence. Scores equal to zero yield zero indicator contribution in the formula, which conflicts with some later sign/tie prose; no repair is made.')
members['D10']['naming_context'][0]['evidence']=[dict(page=17,location='Section 3.3 — original value-function terminology')]
add('D11','surrogate',r'''
We appeal to this very intuition and consider
\[
V_\psi(f_1,f_2)=\mathbb P\left[\frac{(Y_1+Y_2)\psi\big(A_1f_1(H_1),A_2f_2(H_2)\big)}{\pi_1(A_1\mid H_1)\pi_2(A_2\mid H_2)}\right],\tag{7}
\]
where $\psi$ is some bivariate function.
''',[8],'Section 2 — surrogate population value, equation (7)',{'D2':'The surrogate value uses the same two propensity factors as the original reward.','D9':'The arguments are pairs of measurable history-based score functions.'},context='using a suitable surrogate to the zero-one loss function.',symbols=[r'V_\psi(f_1,f_2)'],shape='Population inverse-propensity value with an arbitrary bivariate surrogate. Product structure, positivity, smoothness and Fisher consistency are separate assumptions, not part of this general definition.')
add('D12','decision rules',r'''
Suppose there exist functions $f_1:\mathcal H_1\mapsto[-\infty,\infty]$ and $f_2:\mathcal H_2\mapsto[-\infty,\infty]$ so that
\[
V_\psi(\widetilde f_1,\widetilde f_2)=\sup_{(f_1,f_2)\in\mathcal F}V_\psi(f_1,f_2)\tag{8}
\]
where $\mathcal F$ is as defined in (6). Note that $\widetilde f_1$ and $\widetilde f_2$ may not be unique. Each $(\widetilde f_1,\widetilde f_2)$ lead to the decision rules $\widetilde d_1(H_1)=\operatorname{sign}(\widetilde f_1(H_1))$ and $\widetilde d_2(H_2)=\operatorname{sign}(\widetilde f_2(H_2))$. If $\widetilde f(H_t)=0$, then $\widetilde d_t(H_t)$ can be either $+1$ or $-1$.
''',[8],'Section 2 — surrogate maximizers and induced rules, equation (8)',{'D11':'The scores attain the supremum of the surrogate population value.','D9':'The reference supremum is over the real-valued measurable class F, even though an attaining score may be extended-valued.'},phrases=['decision rules'],symbols=[r'\widetilde d_1(H_1)',r'\widetilde d_2(H_2)'],shape='Potentially extended-valued maximizing scores and the corresponding sign rules, allowing both actions at a zero score. The printed introductory binders f_1,f_2 do not have tildes while the equality does; this discrepancy is preserved. Existence is not imposed as a requirement in the sequential definition of Fisher consistency.')
add('D13','regret',r'''
Finally, we define excess risk in line with the excess risk in context of classification. Letting $V^*=V(f_1^*,f_2^*)$ and $V_\psi^*=V_\psi(\widetilde f_1,\widetilde f_2)$, we define the respective regret and $\psi$-regret of using $(f_1,f_2)$ by
\[
V^*-V(f_1,f_2)\qquad\text{and}\qquad V_\psi^*-V_\psi(f_1,f_2),
\]
respectively. Note that regret and the $\psi$-regret are always non-negative.
''',[8,9],'Section 2 — true and surrogate regrets',{'D10':'V* is the optimal original value and V is the value of the supplied scores.','D11':'V_psi is the surrogate value of the supplied scores.','D12':'The source names the optimal surrogate value through a potentially extended-valued maximizing pair; its defining equality is the supremum in (8).'},phrases=['regret'],symbols=[r'V^*',r'V_\psi^*'],shape='Differences between optimal and achieved population values. The source writes optima using maximizers, while Fisher consistency subsequently permits using their suprema without assuming a measurable maximizing pair. This distinction is recorded separately.')
add('D14','decision boundaries',r'''
next, defining the maps $\eta_1:\mathcal H_1\mapsto\mathbb R$ and $\eta_2:\mathcal H_2\mapsto\mathbb R$ by
\[
\eta_1(H_1)=\frac{\mathbb E[Y_1+U_2^*(H_2)\mid A_1=1,H_1]}{\mathbb E[Y_1+U_2^*(H_2)\mid A_1=1,H_1]+\mathbb E[Y_1+U_2^*(H_2)\mid A_1=-1,H_1]},\tag{9}
\]
\[
\eta_2(H_2)=\frac{\mathbb E[Y_1+Y_2\mid A_2=1,H_2]}{\mathbb E[Y_1+Y_2\mid A_2=1,H_2]+\mathbb E[Y_1+Y_2\mid A_2=-1,H_2]},\tag{10}
\]
we observe that $\eta_1$ and $\eta_2$ play the same role in DTR setting as the conditional probability $\eta$ in context of binary classification. To elaborate, from the definitions of $d_1^*$ and $d_2^*$ in (4), it follows that $d_t^*(H_t)=+1$ if $\eta_t(H_t)>1/2$, and $-1$ otherwise. Note also that the first stage and second stage decision boundaries can be represented by the sets $\{h_1:\eta_1(h_1)=1/2\}$ and $\{h_2:\eta_2(h_2)=1/2\}$.
''',[9],'Section 2 — reward-ratio maps and decision boundaries, equations (9)-(10)',{'D6':'The first ratio uses the optimal continuation reward U_2^* from (3), and both are formed from conditional stage rewards.','D8':'The source relates the ratios and their half-level sets to the optimal treatment rules.'},phrases=['decision boundaries'],symbols=[r'\eta_1(H_1)',r'\eta_2(H_2)'],shape='The source’s two reward-ratio maps and the decision boundaries they define at one half. The maps are not renamed conditional treatment probabilities. The printed minus-one tie rule here conflicts with the plus-one convention in Remark 1; both are retained.')
add('D16','Fisher consistent',r'''
The surrogate $\psi$ is called Fisher consistent if for all $\mathbb P$ satisfying Assumption I-IV, any $\{f_{1n},f_{2n}\}_{n\geq1}\subset\mathcal F$ that satisfies
\[
V_\psi(f_{1n},f_{2n})\to V_\psi^*,
\]
also satisfies
\[
V(f_{1n},f_{2n})\to V^*.
\]
''',[9],'Definition 1',{'D3':'The definition quantifies over laws satisfying positivity (I).','D4':'The same laws satisfy causal consistency (II).','D5':'The same laws satisfy sequential ignorability (III).','D7':'The same laws satisfy the integrability requirements (IV).','D9':'The sequences are pairs of real-valued measurable history scores in F.','D13':'The implication compares convergence to the optimal surrogate and original values.'},phrases=['Fisher consistent','Definition 1'],shape='Sequential Fisher consistency over every admissible law: every score sequence approaching the optimal surrogate value must approach the optimal true value. It is not merely existence of a sign-correct optimizer, and it does not assume the optimizer lies in F.')
members['D16']['application_context']=[dict(text=r'Note that Definition 1 does not require $\widetilde f_1$ and $\widetilde f_2$ to exist or be measurable.',evidence=[dict(page=9,location='After Definition 1 — no attainment requirement')])]
add('D17','closed',r'''
We say a function is closed if it is upper semicontinuous everywhere, or equivalently, if its superlevel sets are closed (pp. 78, Hiriart-Urruty and Lemaréchal, 2004).
''',[12],'Section 3.1 — closed concave function convention',phrases=['closed','upper semicontinuous'],shape='The source’s upper-semicontinuity convention for a closed concave function, including its superlevel-set characterization. It is not replaced by lower semicontinuity for convex minimization.')
add('D18','strictly concave',r'''
The function $h$ is strictly concave if for any $\lambda\in(0,1)$, and $x,y\in\operatorname{dom}(h)$,
\[
h(\lambda x+(1-\lambda)y)>\lambda h(x)+(1-\lambda)h(y).
\]
''',[12],'Section 3.1 — strict concavity convention',phrases=['strictly concave'],symbols=[r'\lambda\in(0,1)'],shape='The source strict-concavity formula. It omits the usual restriction x unequal to y; that omission is documented without modifying this original passage. Effective domain and extended-real conventions are archived separately.')
add('D19','smoothed 0–1 loss',r'''
$\phi$ is a strictly increasing function such that

1. $\phi(x)>0$ for all $x\in\mathbb R$.
2. For all $x\in\mathbb R$, $\phi(x)$ satisfies $\phi(x)+\phi(-x)=C_\phi$ where $C_\phi>0$ is a constant.
3. $\lim_{x\to\infty}\phi(x)=C_\phi$ and $\lim_{x\to-\infty}\phi(x)=0$.
''',[16,17],'Condition 2',kind='condition',context='The class specified by Condition 2 has been mentioned in various machine-learning problems, often presented in forms appropriate for a minimization problem. In certain instances, it is referred to as the smoothed 0–1 loss.',phrases=['Condition 2'],symbols=[r'\phi(x)+\phi(-x)=C_\phi'],shape='Strictly increasing positive univariate surrogate with constant reflected sum and specified limits. Condition 2 itself does not require differentiability or continuity. The bivariate product is imposed explicitly by Theorem 3 and as a later section convention.')
members['D19']['naming_context'][0]['evidence']=[dict(page=18,location='Section 3.3 — terminology for the Condition 2 class')]
add('D20','lower bound condition',r'''
\[
\left|\mathbb E[T(H_2,d_2^*(H_2))\mid H_1=h_1,A_1=1]-\mathbb E[T(H_2,d_2^*(H_2))\mid H_1=h_1,A_1=-1]\right|
>\mathbb E[T(H_2,-d_2^*(H_2))\mid H_1=h_1,A_1=1]+\mathbb E[T(H_2,-d_2^*(H_2))\mid H_1=h_1,A_1=-1],\tag{13}
\]
where we remind the readers that $T(H_2,a_2)=Y_1+\mathbb E[Y_2\mid H_2,A_2=a_2]$.
''',[14,15],'Section 3.2 — hinge-policy condition, equation (13)',{'D8':'The rewards are evaluated at the optimal second-stage action d_2^* and its opposite.','D1':'The defining T is the first reward plus the conditional second reward under the longitudinal observation law.'},kind='condition',context='Thus (13) can be interpreted as a lower bound condition, indicating the minimum strength required for the first stage conditional treatment effect.',symbols=[r'T(H_2,-d_2^*(H_2))',r'\tag{13}'],shape='Strict inequality comparing the absolute first-stage optimal-reward contrast with the sum of opposite-second-action rewards. T here is a reward function, distinct from the calligraphic treatment contrasts. Both conditional terms on the right are added, not differenced.')
members['D20']['naming_context'][0]['evidence']=[dict(page=15,location='Section 3.2 — interpretation of (13)')]
add('D21',['empirical','value function'],r'''
Define the empirical $\psi$-value function
\[
\widehat V_\psi(f_1,f_2)=\mathbb P_n\left[\frac{(Y_1+Y_2)\psi\big(A_1f_1(H_1),A_2f_2(H_2)\big)}{\pi_1(A_1\mid H_1)\pi_2(A_2\mid H_2)}\right]\tag{16}
\]
''',[20],'Section 4 — empirical surrogate value, equation (16)',{'D11':'The empirical value replaces the population expectation in the surrogate value by the empirical measure.','D1':'P_n is the empirical law of the n iid observed records.','D19':'The surrounding Section 4 convention fixes psi(x,y)=phi(x)phi(y) with phi satisfying Condition 2.'},phrases=['empirical'],symbols=[r'\widehat V_\psi(f_1,f_2)'],shape='Empirical inverse-propensity surrogate value, with the product-surrogate convention of Section 4. The known-propensity assumption used by the subsequent error rates is archived separately; no propensity estimation error is included here.')
members['D21']['application_context']=[dict(text=r'For the remainder of this paper except Supplement B, unless otherwise mentioned, $\phi$ will denote a univariate surrogate satisfying Condition 2, and $\psi$ will denote the bivariate surrogate $\psi(x,y)=\phi(x)\phi(y)$ where $\phi$ satisfies Condition 2.',evidence=[dict(page=20,location='Section 4 — product-surrogate convention')])]
add('D22','classifiers',r'''
We assume that $(\widehat f_{n,1},\widehat f_{n,2})\in\mathcal U_n=\mathcal U_{1n}\times\mathcal U_{2n}$, where $\mathcal U_{1n},\mathcal U_{2n}$ are classes of functions.
''',[25],'Section 6 — fitted classifiers and product class',{'D9':'The search classes are subclasses of the measurable score-pair class F, as specified in Section 4.'},context='In this section, we focus on the estimation error in (18), and provide sharp regret-bound for a selected set of classifiers by combining all sources of error.',symbols=[r'\mathcal U_n=\mathcal U_{1n}\times\mathcal U_{2n}',r'\widehat f_{n,1}'],shape='Data-dependent fitted score pair in a product of two function classes. The source does not require an exact empirical maximizer; its suboptimality is measured by Opt_n. General-class Theorems 5-7 do not assume neural-network or wavelet structure.')
members['D22']['application_context']=[dict(text=r'''Therefore, in practice, one may optimize $\widehat V_\psi(f_1,f_2)$ over a nested class
\[
\mathcal U_1\subset\ldots\subset\mathcal U_n\subset\mathcal F,
\]
where $\mathcal U_n$ is some rich class of classifiers, preferably a universal class (see Zhang et al., 2018a).''',evidence=[dict(page=20,location='Section 4 — nested search classes')])]
add('D23','optimization error',r'''
We define the optimization error as
\[
\mathit{Opt}_n=\sup_{(f_1,f_2)\in\mathcal U_n}\widehat V_\psi(f_1,f_2)-\widehat V_\psi(\widehat f_{n,1},\widehat f_{n,2}).
\]
''',[21],'Section 4.1 — empirical optimization gap',{'D21':'The gap is the supremum of the empirical surrogate value minus its value at the fitted scores.','D22':'Both the candidate supremum and the fitted pair belong to the search class U_n.'},phrases=['optimization error'],symbols=[r'\mathit{Opt}_n'],shape='Empirical optimization suboptimality retained as a random term in the regret bounds. It need not be zero and no particular optimizer or convergence theorem is assumed by its definition.')
add('D24','Outcomes',r'''
Outcomes $Y_1,Y_2$ satisfy $\max(Y_1,Y_2)\leq C_y$.
''',[22],'Assumption A',{'D1':'The bound concerns the two observed stage rewards.'},kind='assumption',phrases=['Outcomes','Assumption A'],symbols=[r'\max(Y_1,Y_2)\leq C_y'],shape='The printed common upper outcome bound, combined with the earlier positive lower outcome convention when applicable. This assumption is not rewritten as an absolute-value bound or imported into the early Fisher-consistency theorems.')
add('D25','Tsybakov small noise assumption',r'''
There exist a constant $C>0$, a small number $t_0\in(0,1)$, and positive reals $\alpha_1,\alpha_2$ such that
\[
P(0<|\eta_1(H_1)-1/2|\leq t)\leq Ct^{\alpha_1},
\]
\[
P(0<|\eta_2(H_2)-1/2|\leq t)\leq Ct^{\alpha_2}
\]
for all $t<t_0$.
''',[22],'Assumption B — Tsybakov small noise assumption',{'D14':'The two probabilities measure distances of the reward-ratio maps from their one-half decision boundaries.'},kind='assumption',context='Assumption B (Tsybakov small noise assumption).',phrases=['Assumption B'],symbols=[r'0<|\eta_1(H_1)-1/2|\leq t',r'0<|\eta_2(H_2)-1/2|\leq t'],shape='Two-stage small-noise condition excluding mass exactly at the boundary, with potentially distinct positive exponents. The paper later takes alpha=min(alpha_1,alpha_2). The printed t range omits an explicit positive lower bound, and that domain omission is recorded.')
add('D26','Strong separation',r'''
$\eta_1$ and $\eta_2$ are bounded away from zero on their respective domains.
''',[24],'Assumption C — Strong separation',{'D14':'The condition is stated for the two reward-ratio maps defined in (9)-(10).'},kind='assumption',context='Assumption C (Strong separation).',phrases=['Assumption C'],symbols=[r'\eta_1',r'\eta_2'],shape='The exact source condition bounds eta_1 and eta_2 away from zero, not their distance from one half. This conflicts with the surrounding description as separation from a treatment boundary; it is preserved without correction.')
add('D27','type A',r'''
We say a surrogate $\phi$ satisfying Condition 2 is of type A if there exists a constant $B_\phi>0$ and $\kappa\geq2$ such that $|\phi'(x)|<B_\phi(1+|x|)^{-\kappa}$ for all $x\neq0$.
''',[23],'Definition 2 — type A',{'D19':'A type-A surrogate first satisfies all parts of Condition 2, then the polynomial derivative bound.'},phrases=['type A','Definition 2'],symbols=[r'B_\phi(1+|x|)^{-\kappa}'],shape='Condition 2 plus a strict polynomial bound on the derivative away from zero, with kappa at least two. No differentiability at zero is required by the source.')
add('D28','type B',r'''
We say a surrogate $\phi$ satisfying Condition 2 is of type B if there exists a constant $B_\phi>0$ and $\kappa>0$ such that $|\phi'(x)|<B_\phi\exp(-\kappa|x|)$ for all $x\neq0$.
''',[23],'Definition 2 — type B',{'D19':'A type-B surrogate first satisfies Condition 2, then the exponential derivative bound.'},phrases=['type B','Definition 2'],symbols=[r'B_\phi\exp(-\kappa|x|)'],shape='Condition 2 plus a strict exponential bound on the derivative away from zero, with a positive kappa. This is kept distinct from the type-A condition and its different parameter range.')
add('D29','hinge loss',r'''
In this section, we demonstrate the Fisher inconsistency of the non-smooth loss function $\psi(x,y)=\min(x,y,1)$, which is a bivariate version of the univariate hinge loss $\min(x,1)$.
''',[14],'Section 3.2 — hinge surrogate',kind='source_passage',phrases=['hinge loss'],symbols=[r'\psi(x,y)=\min(x,y,1)'],shape='The particular bivariate minimum surrogate used in Theorem 2. The paper also prints shifted and sign-reversed hinge expressions elsewhere; those are not substituted for this exact function.')
add('D30','bracketing entropy',r'''
Given two functions $f_l$ and $f_u$, the bracket $[f_l,f_u]$ is the set of all function $f$ satisfying $f_l\leq f\leq f_u$. Suppose $\|\cdot\|$ is a norm on the function-space and $\epsilon>0$. Then $[f_l,f_u]$ is called an $\epsilon$-bracket if $\|f_u-f_l\|<\epsilon$. For a function-class $\mathcal G$, we define the bracketing entropy $N_{[\ ]}(\epsilon,\mathcal G,\|\cdot\|)$ to be the minimum number of $\epsilon$-brackets needed to cover $\mathcal G$.
''',[25],'Section 6.0.1 — bracketing number convention',phrases=['bracketing entropy'],symbols=[r'N_{[\ ]}(\epsilon,\mathcal G,\|\cdot\|)'],shape='The source calls the bracketing number an entropy. The definition counts brackets with strictly less than epsilon norm width; it does not take a logarithm. Its later bounds distinguish N from log N.')
add('D31','VC-type classes',r'''
\[
N_{[\ ]}(\epsilon,\mathcal U_{tn},\|\cdot\|_\infty)\lesssim\left(\frac{A_n}{\epsilon}\right)^{\rho_n},\qquad t=1,2\tag{21}
\]
where $A_n,\rho_n>0$.
''',[25],'Section 6.0.1 — sup-norm complexity condition, equation (21)',{'D30':'This condition bounds the number of sup-norm brackets, not its logarithm.','D22':'It applies separately to the two factors U_1n,U_2n of the search class.'},kind='condition',context='The $\mathcal U_n$’s that satisfy (21) are called VC-type classes (p. 41 Koltchinskii, 2011).',symbols=[r'\mathcal U_{tn}',r'\tag{21}'],shape='Polynomial sup-norm bracketing-number bounds for each stage’s score class. The source states no explicit epsilon range or uniformity convention for the implicit constant. Theorem 5 adds its own restrictions on A_n and rho_n.')
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed interfaces; extraction remains in progress.')
