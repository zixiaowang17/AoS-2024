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
add('D1','Bayesian two-groups model',r'''
For $i=1,\ldots,m$, let $H_i=0$ if the $i$th hypothesis is null and $H_i=1$ otherwise, and consider the simple Bayesian two-groups model
\[
p_i\mid H_i=h\overset{\mathrm{ind}}{\sim}f_h,\quad\text{with}\quad H_i\overset{\mathrm{iid}}{\sim}\operatorname{Bern}(1-\pi_0),\quad\text{for }i=1,\ldots,m,\tag{1}
\]
where $f_0$ and $f_1$ are densities (null and alternative, respectively) supported on the unit interval $[0,1]$, and the null proportion is $\pi_0\in[0,1]$. We will assume throughout that $f_0=\mathbf1_{[0,1]}$, the uniform density. Let $f:=\pi_0+(1-\pi_0)f_1$ denote the common mixture density of the $p$-values in model (1), and let $F(t):=\int_0^t f(u)\,du$ denote the corresponding cumulative distribution function (cdf).
''',[2],'Introduction — Bayesian two-groups model, equation (1)',kind='source_passage',phrases=['Bayesian two-groups model'],symbols=[r'H_i=0',r'f:=\pi_0+(1-\pi_0)f_1'],shape='Independent conditional p-values with iid Bernoulli non-null indicators, uniform null and a common alternative density. Expectations in the Bayesian census average both indicators and p-values. The alternative shape restriction is separate.')
add('D2','local false discovery rate',r'''
The lfdr is then defined as the posterior probability that $H_i=0$, conditional on the observed $p$-value $p_i$:
\[
\operatorname{lfdr}(t):=\mathbb P\{H_i=0\mid p_i=t\}=\frac{\pi_0}{f(t)}.\tag{2}
\]
''',[2],'Introduction — local false discovery rate, equation (2)',{'D1':'The posterior and mixture density belong to model (1) with a uniform null.'},context='The likelihood that an individual discovery is a false lead is called its local false discovery rate (lfdr, Efron et al., 2001).',symbols=[r'\operatorname{lfdr}(t)',r'\frac{\pi_0}{f(t)}'],shape='Null posterior probability, represented by the mixture-density ratio. It is the probability that the null is true, despite the reversed wording in the abstract. Values at zero-density points and a density version require conventions not supplied by the formula.')
add('D3','alternative density',r'''
We will usually work under the additional assumption that $f_1(t)$ is non-increasing in $t$, or equivalently that $\operatorname{lfdr}(t)$ is non-decreasing, so that smaller $p$-values represent stronger evidence against the null.
''',[2,3],'Introduction — monotonicity of the alternative density',{'D1':'f_1 is the alternative density in model (1).','D2':'The source also states the corresponding monotonicity of lfdr.'},kind='condition',context='Furthermore, if the alternative density $f_1$ is non-increasing, then we have',phrases=['non-increasing'],symbols=[r'f_1(t)'],shape='Monotonicity condition on the alternative, with the source lfdr equivalence. Theorem 1 uses it only for its final max-lfdr clause, not for the preceding exact last-rejection identity.')
members['D3']['naming_context'][0]['evidence']=[dict(page=8,location='Theorem 1 — additional alternative-density condition')]
add('D4','max-lfdr',r'''
We represent a generic multiple testing method as a function $\mathcal R(p_1,\ldots,p_m)$ returning an index set $\mathcal R\subseteq\{1,\ldots,m\}$, where hypothesis $i$ is rejected if and only if $i\in\mathcal R$. We say the procedure’s max-lfdr is
\[
\operatorname{max\text{-}lfdr}(\mathcal R):=\mathbb E\left[\max_{i\in\mathcal R}\operatorname{lfdr}(p_i)\right],\tag{3}
\]
defining the maximum as zero if no rejections are made.
''',[3],'Introduction — maximum local false discovery rate, equation (3)',{'D2':'The criterion averages the maximum of the individual null posterior probabilities.'},phrases=['max-lfdr'],symbols=[r'\operatorname{max\text{-}lfdr}(\mathcal R)'],shape='Expectation of the largest lfdr among a data-dependent rejection set, with maximum zero for an empty set. This is not the random maximum alone and is not ordinary FDR. Monotonicity is needed for its last-rejection characterization, not for its definition.')
add('D5','support line (SL) procedure',r'''
In addition to the max-lfdr criterion, we also introduce a simple multiple testing procedure, the support line (SL) procedure, and show that it provably controls the max-lfdr under mild assumptions. Define the $p$-value order statistics $p_{(1)}\leq\cdots\leq p_{(m)}$, and let $p_{(0)}=0$ by convention. Then our procedure rejects $p$-values up to the last minimizer
\[
R_\ell:=\operatorname*{argmin}_{k=0,\ldots,m}\ p_{(k)}-\frac{\ell k}{m}.\tag{4}
\]
That is, we reject $\mathcal R_\ell:=\{i:p_i\leq\tau_\ell\}$, for the threshold $\tau_\ell=p_{(R_\ell)}$.
''',[3],'Introduction — support-line rule and threshold, equation (4)',phrases=['support line (SL) procedure','last minimizer'],symbols=[r'R_\ell',r'\tau_\ell=p_{(R_\ell)}'],shape='Last minimizing index of the line-adjusted order statistics, its p-value threshold, and the induced rejection set. The last-minimizer tie rule and p_(0)=0 are explicit. It is a deterministic procedure on the p-values, without a model or monotonicity prerequisite merely to compute it.')
add('D6','weighted classification loss',r'''
To formalize our analysis above, define the per-instance weighted classification loss:
\[
L_\omega(H,\mathcal R):=\frac{(1+\omega)V-R}{m},\tag{5}
\]
where $R=|\mathcal R|$ denotes the number of rejections and $V=\sum_{i\in\mathcal R}(1-H_i)$ denotes the number of false discoveries. This loss can be derived, up to additive and multiplicative constants, by viewing each of the $m$ hypotheses as a binary classification problem, where we incur a cost $c_1$ for each type I error or false discovery ($i\in\mathcal R$, but $H_i=0$), and cost $c_2$ from each type II error or false non-discovery ($i\notin\mathcal R$, but $H_i=1$). If the total number of non-nulls is $m_1=\sum_i H_i$, then there are $m_1-(R-V)$ false non-discoveries, so the total loss over all $m$ instances is
\[
c_1V+c_2(m_1-(R-V))=c_2m\cdot L_\omega(H,\mathcal R)+c_2m_1,
\]
where $\omega=c_1/c_2$ is the ratio between the two misclassification costs. $L_\omega$ as defined in (5) is normalized so that rejecting nothing incurs zero loss, and each true discovery has value $1/m$.
''',[4],'Section 1.1 — per-instance weighted classification loss, equation (5)',phrases=['weighted classification loss'],symbols=[r'L_\omega(H,\mathcal R)',r'\omega=c_1/c_2'],shape='Normalized loss on a truth-label vector and a rejection set, allowing negative values for beneficial rejections. It does not require independent random truth labels to be defined; the Bayesian model enters when averaging risk.')
add('D7','oracle procedure',r'''
Under the two-groups model (1), Sun and Cai (2007, Theorem 2) show that the corresponding Bayes risk $\mathbb E L_\omega(H,\mathcal R)$ is minimized by the oracle procedure
\[
\mathcal R^*:=\{i:\operatorname{lfdr}(p_i)\leq\alpha\},\quad\text{where}\quad\alpha=\frac1{1+\omega}.\tag{6}
\]
''',[5],'Section 1.1 — oracle decision rule, equation (6)',{'D2':'The oracle thresholds the individual null posterior probabilities.','D6':'Its threshold is fixed by the cost ratio of the weighted classification loss.'},phrases=['oracle procedure'],symbols=[r'\mathcal R^*',r'\alpha=\frac1{1+\omega}'],shape='Oracle rejection rule at the cost-determined lfdr threshold. The external Bayes-optimality attribution is preserved but not read or used as a new census theorem.')
members['D7']['application_context']=[dict(text=r'''If $f_1$ is non-increasing, then the oracle procedure reduces to thresholding $p$-values at a fixed threshold
\[
\mathcal R^*=\{i:p_i\leq\tau^*\},\quad\text{for}\quad\tau^*:=\max\{t\in[0,1]:\operatorname{lfdr}(t)\leq\alpha\},\tag{7}
\]
with $\tau^*=0$ if no such threshold exists.''',evidence=[dict(page=5,location='Equation (7) — monotone case and empty-set convention')])]
add('D8','estimator of the null proportion',r'''
First, we use the estimator of the null proportion $\pi_0$, defined as
\[
\widehat\pi_0^\lambda:=\frac{1+\#\{i:p_i>\lambda\}}{(1-\lambda)m},\tag{12}
\]
''',[10],'Section 2.2 — null-proportion estimator, equation (12)',phrases=['estimator of the null proportion'],symbols=[r'\widehat\pi_0^\lambda',r'1+\#\{i:p_i>\lambda\}'],shape='Finite-sample null-proportion estimate with a plus-one numerator and a fixed lambda in (0,1). No clipping at one is specified. Theorem 6 quantifies a general estimator and does not require this particular construction.')
add('D9','modified version of our SL procedure',r'''
Fix $\lambda\in(0,1)$, and define a modified version of our SL procedure that only examines order statistics below $\lambda$:
\[
R_\ell^\lambda:=\operatorname*{argmin}_{k\geq0:\ p_{(k)}\leq\lambda}\ \widehat\pi_0^\lambda p_{(k)}-\frac{\ell k}{m},\tag{13}
\]
and $\mathcal R_\ell^\lambda=\{i:\ p_i\leq p_{(R_\ell^\lambda)}\}$.
''',[10],'Theorem 4 — constrained SL procedure, equation (13)',{'D8':'The objective uses the particular null-proportion estimator (12).','D5':'This is the stated modification of the SL procedure, retaining its order-statistic and last-minimizer conventions.'},kind='theorem_excerpt',phrases=['modified version of our SL procedure'],symbols=[r'R_\ell^\lambda',r'p_{(k)}\leq\lambda'],shape='Lambda-constrained SL rule with the estimated null proportion in the objective. The source says below lambda but the displayed constraint is weak <=, which is retained. This is distinct from unconstrained SL at a general estimated level.')
add('D10',['regret','excess risk'],r'''
A fundamental result of Sun and Cai (2007) is that the oracle (6) minimizes the weighted classification risk over all procedures, thus representing a benchmark against which we can compare methods that are feasible without a priori knowledge of the lfdr. In the empirical Bayes literature (see, e.g., Efron, 2019), the price of our ignorance of the model parameters is measured by the regret, or excess risk, given by the optimality gap
\[
\operatorname{Regret}_m(\mathcal R):=\mathbb E\left[L_\omega(H,\mathcal R)-L_\omega(H,\mathcal R^*)\right].\tag{16}
\]
''',[11],'Section 3 — empirical Bayes regret, equation (16)',{'D6':'The excess risk compares the normalized weighted losses.','D7':'The comparator is the oracle rejection rule (6).','D1':'The preceding paragraph specifies expectation over both truth labels and p-values under model (1).'},phrases=['regret','excess risk'],symbols=[r'\operatorname{Regret}_m(\mathcal R)'],shape='Unconditional expected excess weighted loss relative to the oracle, averaging the same data used by a procedure. It is not the fixed-threshold population regret evaluated independently at a random threshold.')
members['D10']['application_context']=[dict(text=r'In this section, we study our procedure’s empirical Bayes regret under the weighted classification risk $\mathbb E[L_\omega(H,\mathcal R)]$, where the expectation is taken over $H_1,\ldots,H_m$ and $p_1,\ldots,p_m$ according to (1), and $L_\omega$ is defined as in (5). Throughout this section we will be considering a sequence of problems with $m\to\infty$.',evidence=[dict(page=11,location='Section 3 — expectation and asymptotic regime')])]
add('D11','Chernoff’s distribution',r'''
All three are given in terms of Chernoff’s distribution (Chernoff, 1964), which is defined as the distribution of the maximizer $Z$ of a standard two-sided Brownian motion $W=(W(t))_{t\in\mathbb R}$ with parabolic drift:
\[
Z=\operatorname*{argmax}_{t\in\mathbb R}W(t)-t^2.\tag{22}
\]
''',[15],'Section 3.3 — Chernoff distribution, equation (22)',phrases=['Chernoff’s distribution'],symbols=[r'W(t)-t^2'],shape='Distribution of the location of the maximum of standard two-sided Brownian motion minus t squared, with the exact unit drift normalization. This is not the maximum value; its variance is quoted as approximately 0.26 in the theorem statements.')
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed interfaces; theorem connections remain to be finalized.')
