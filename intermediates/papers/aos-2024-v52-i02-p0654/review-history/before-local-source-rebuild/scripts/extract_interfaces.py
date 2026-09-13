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
add('D1','target mean function',r'''
Let $X^{[t]}:[0,1]\to\mathbb R$ be a target random function and each target subject $i\in\{1,\ldots,n^{[t]}\}$ has an an independent copy $X_i^{[t]}$ (called curve) of $X^{[t]}$. We have noisy observations of these curves at discrete locations:
\[
Y_{ij}^{[t]}=X_i^{[t]}(T_{ij}^{[t]})+\varepsilon_{ij}^{[t]},\qquad(j=1,\ldots,m_i^{[t]}\text{ and }i=1,\ldots,n^{[t]}),\tag{1}
\]
where $T_{ij}^{[t]}$ are target design points, and $\varepsilon_{ij}^{[t]}$ are an independent random noises. Based on the target sample $\mathcal D^{[t]}:=\{(T_{ij}^{[t]},Y_{ij}^{[t]}):j=1,\ldots,m_i^{[t]},i=1,\ldots,n^{[t]}\}$, our primary objective is to estimate the target mean function $f^{[t]}(\cdot):=\mathbb E(X^{[t]}(\cdot))$.
''',[2],'Section 1.1 — target observations and mean, equation (1)',kind='source_passage',phrases=['target mean function'],symbols=[r'f^{[t]}',r'\mathcal D^{[t]}'],shape='Independent subject curves with noisy discrete observations and pointwise target mean. Within-curve values need not be independent. The statement does not impose smoothness on the sample curves; it restricts their mean separately.')
add('D2','source samples',r'''
In the transfer learning setup, we also have $K$ source samples $\mathcal D^{[s,1]},\ldots,\mathcal D^{[s,K]}$ in addition to the target sample $\mathcal D^{[t]}$. These source samples are generated similarly. That is, for each source index $k\in\{1,\ldots,K\}$, there is a random function $X^{[s,k]}:[0,1]\to\mathbb R$ with its source mean function $f^{[s,k]}(\cdot):=\mathbb E(X^{[s,k]}(\cdot))$ and we observe
\[
Y_{ij}^{[s,k]}=X_i^{[s,k]}(T_{ij}^{[s,k]})+\varepsilon_{ij}^{[s,k]},\qquad(j=1,\ldots,m_i^{[s,k]},i=1,\ldots,n^{[s,k]},\text{ and }k=1,\ldots,K),\tag{2}
\]
where the curves $X_i^{[s,k]}$ are an independent copies of $X^{[s,k]}$, $T_{ij}^{[s,k]}$ are source design points, and $\varepsilon_{ij}^{[s,k]}$ are an independent random noises. The estimator for the target mean function $f^{[t]}$ now can utilize the source samples $\mathcal D^{[s,1]},\ldots,\mathcal D^{[s,K]}$ as well as the target sample $\mathcal D^{[t]}$.
''',[2],'Section 1.1 — source observation model, equation (2)',{'D1':'The source observations supplement the target observations whose mean f^[t] is estimated.'},kind='source_passage',phrases=['source samples'],symbols=[r'\mathcal D^{[s,1]}',r'f^{[s,k]}'],shape='K source populations with independent subject copies within each population. Source means can differ from one another and the target. Independence across populations is imposed in the statistical model, not inferred from this display alone.')
add('D3','Hölder smoothness',r'''
Let us denote by $\mathcal H_\alpha(L,M)$ the class of bounded functions with Hölder smoothness $\alpha>0$. To be more specific, $f\in\mathcal H_\alpha(L,M)$ if and only if $f:[0,1]\to\mathbb R$ is bounded as $\|f\|_{\mathcal L^\infty}\leq M$ and $\alpha^*$-times continuously differentiable such that
\[
|f^{(\alpha^*)}(t_1)-f^{(\alpha^*)}(t_2)|\leq L|t_1-t_2|^{\alpha-\alpha^*},\qquad\text{for any }t_1,t_2\in[0,1],
\]
where $\alpha^*:=\omega(\alpha)$ denotes the largest integer strictly smaller than $\alpha$.
''',[2],'Section 1.1 — bounded Hölder class',phrases=['Hölder smoothness'],symbols=[r'\mathcal H_\alpha(L,M)',r'\omega(\alpha)'],shape='Bounded Hölder class with derivative order equal to the largest integer strictly below alpha. At integer alpha this is alpha-1, not alpha. Only the displayed derivative difference and the function supremum are bounded.')
add('D4','mean and difference functions',r'''
We assume
\[
f^{[t]},f^{[s,k]}\in\mathcal H_{\alpha_m}(L_m,M_m),\qquad
\delta^{[s,k]}:=f^{[t]}-f^{[s,k]}\in\mathcal H_{\alpha_\delta}(L_\delta,M_\delta),\qquad(k=1,\ldots,K)\tag{3}
\]
with two smoothness parameters $\alpha_m,\alpha_\delta>0$ and constants $L_m,M_m,L_\delta,M_\delta>0$.
''',[2,3],'Section 1.1 — mean and difference regularity, equation (3)',{'D3':'Both supplied mean functions and their differences lie in the corresponding bounded Hölder classes.'},kind='condition',context='The mean and difference functions of measures in $\mathcal P$ satisfy Equation (3) and the measures themselves also satisfy the uniform sub-Gaussian condition (Assumption 1).',symbols=[r'\delta^{[s,k]}',r'\mathcal H_{\alpha_m}(L_m,M_m)',r'\mathcal H_{\alpha_\delta}(L_\delta,M_\delta)'],shape='A condition on given target and source means, with a separate smoothness class for their differences. No ordering between alpha_m and alpha_delta is assumed. In the conventional no-source specialization only the target mean restriction is operative; no source data are required by this predicate.')
members['D4']['naming_context'][0]['evidence']=[dict(page=5,location='Section 2 — model class')]
add('D6','uniformly sub-Gaussian variables',r'''
The random functions and noises are uniformly sub-Gaussian variables with a positive variance proxy $\tau^2$. As per Wainwright [36], we assume that for every $u>0$, the following holds: for any given $x\in[0,1]$ and $k=1,\ldots,K$,
\[
\left.\begin{gathered}
\mathbb P\big(|X_1^{[t]}(x)-f^{[t]}(x)|\geq u\big)\vee\mathbb P\big(|X_1^{[s,k]}(x)-f^{[s,k]}(x)|\geq u\big)\\
\mathbb P\big(|\varepsilon_{11}^{[t]}|\geq u\big)\vee\mathbb P\big(|\varepsilon_{11}^{[s,k]}|\geq u\big)
\end{gathered}\right\}\leq2e^{-u^2/2\tau^2}
\]
''',[5,6],'Assumption 1',kind='assumption',phrases=['uniformly sub-Gaussian variables','Assumption 1'],symbols=[r'\tau^2'],shape='Uniform pointwise tail bounds for supplied centered random functions and for uncentered noises, using one positive proxy. This is not a supremum-norm tail bound. Target terms apply in the no-source specialization. The formula does not explicitly impose zero-mean errors or independence of design points from curves.')
model=r'''
To describe the optimality of functional mean estimation, we consider a statistical model denoted by $\mathcal P$ which is a collection of certain probability measures. The mean and difference functions of measures in $\mathcal P$ satisfy Equation (3) and the measures themselves also satisfy the uniform sub-Gaussian condition (Assumption 1). Finally, the collection of target and source samples, $\{\mathcal D^{[t]},\mathcal D^{[s,1]},\ldots,\mathcal D^{[s,K]}\}$, is assumed to be independent. We continue to employ the same assumptions in Section 3 where we argue the optimality under an independent design.
'''
add('D7','statistical model',model,[5],'Section 2 — statistical model',{'D1':'The laws generate target observations with mean f^[t].','D2':'The full transfer model also generates K source populations.','D4':'The model explicitly requires the mean and difference restrictions in Equation (3).','D6':'The model explicitly imposes the uniform tail bounds in Assumption 1.'},kind='source_passage',phrases=['statistical model'],symbols=[r'\mathcal P'],shape='Class of laws satisfying the observation models, mean/difference smoothness, uniform pointwise tails and independence of target and source samples. The sampling design is specified separately for each section; the class itself is not tied to common design.')
add('D8','common design',r'''
While the results presented in this section are valid for randomly selected common design points, for the sake of clarity in our exposition, we simplify by assuming that these design points are deterministic. Additionally, we adopt the convention, without loss of generality, that the common design points are arranged in ascending order. To summarize, a common design is characterized by two collections of common design points, $\{T_j^{[t]}:j=1,\ldots,m_t\}$ and $\{T_j^{[s]}:j=1,\ldots,m_s\}$, such that $T_{j_1}^{[t]}\leq T_{j_2}^{[t]}$ and $T_{j_1}^{[s]}\leq T_{j_2}^{[s]}$ for any $j_1\leq j_2$ as well as the following holds:
\[
T_{ij}^{[t]}=T_j^{[t]}\quad\text{for all }j=1,\ldots,m_t\text{ and }i=1,\ldots,n_t,
\]
\[
T_{ij}^{[s,k]}=T_j^{[s]}\quad\text{for all }j=1,\ldots,m_s,i=1,\ldots,n_s\text{ and }k=1,\ldots,K.
\]
''',[5],'Section 2 — common design',kind='condition',phrases=['common design'],symbols=[r'T_j^{[t]}',r'T_j^{[s]}'],shape='Ordered deterministic designs shared across target subjects and across all source populations. The target grid need not equal the source grid. Upper gap bounds are separate theorem hypotheses; they are not required by the lower-bound statement.')
add('D9','independent design',r'''
This section investigates the setting in which the design points of both the target and source samples are randomly drawn from the domain $[0,1]$. Consider two probability distributions on $[0,1]$, referred to as $\eta_t$ and $\eta_s$, for target and sample design points, respectively. We make the following assumptions:
\[
\big(T_{ij}^{[t]}:j=1,\ldots,m_t,i=1,\ldots,n_t\big)\overset{\mathrm{i.i.d.}}\sim\eta_t,
\]
\[
\big(T_{ij}^{[s,k]}:j=1,\ldots,m_s,i=1,\ldots,n_s,k=1,\ldots,K\big)\overset{\mathrm{i.i.d.}}\sim\eta_s.
\]
''',[12],'Section 3 — independent design',kind='condition',context='3. Transfer learning for functional mean estimation under an independent design.',symbols=[r'\eta_t',r'\eta_s'],shape='Iid target designs and iid source designs, the latter sharing one law across K groups. The positive lower and upper density bounds occur in Theorems 3.1/3.2, not in this section definition or the lower-bound statement.')
add('D17',['statistical model','conventional setup'],model,[5],'Sections 2.1 and 3.1 — conventional restriction of the statistical model',{'D1':'The conventional experiment observes only the target sample and estimates its mean.','D4':'Equation (3) supplies the target Hölder restriction; source/difference clauses belong to the full model and do not require source observations in this specialization.','D6':'The target random-function and error terms in Assumption 1 supply the conventional experiment’s tail restrictions.'},kind='source_passage',context='THEOREM 2.1 (The minimax risk under conventional setup and common design).',symbols=[r'\mathcal P'],note='The paper reuses the symbol for its conventional no-source setting. The complete original model paragraph is preserved; the no-source application context determines this restricted experiment.',shape='Conventional target-only specialization of the paper’s law class. The main text explicitly sets n_s=0. The full paragraph is quoted unchanged; source observations, transfer algorithms and positive-source sample constraints are not imported.')
members['D17']['naming_context'][0]['evidence']=[dict(page=6,location='Theorem 2.1 heading')]
members['D17']['application_context']=[dict(text='This involves estimating the target mean function $f^{[t]}$ when no source samples are available, i.e. $n_s=0$.',evidence=[dict(page=6,location='Section 2.1 — conventional setup')]),dict(text='We again aim to estimate the target mean function $f^{[t]}$ when we have no source samples available ($n_s=0$).',evidence=[dict(page=12,location='Section 3.1 — conventional setup')])]
add('D10','Randomized local polynomial regression with thresholding',r'''
Require: A collection $\mathcal D=\{(T_{ij},Y_{ij}):j=1,\ldots,m,i=1,\ldots,n\}$ of observations, a bandwidth $b\in1/\mathbb Z^+$, a degree $d\in\mathbb Z^+$ of polynomial, and a threshold $M>0$.

1. Partition the domain $[0,1]$ into $b^{-1}$-many intervals of length $b$. We denote those intervals by $I_r$ $(r=1,\ldots,b^{-1})$ from left to right.
2. Let us denote by $\mathcal D^{(i)}:=\{(T_{ij},Y_{ij}):j=1,\ldots,m\}$ the collection of observations from the same subject $i\in\{1,\ldots,n\}$. For index $r=1,\ldots,b^{-1}$, we take randomized collection $\mathcal D_r:=\{(\mathbb T_{i,r},\mathbb Y_{i,r}):i=1,\ldots,n\}$ of observations where $(\mathbb T_{i,r},\mathbb Y_{i,r})$ is randomly chosen from the following process:
3. if the collection $\mathcal D$ comes from common design then
4. Consider any $(1/m)$-packing and $(1/2m)$-covering sub-collection $\widetilde{\mathcal D}^{(i)}$ of $\mathcal D^{(i)}$ where the distance between observations is computed based on design points. The random $(\mathbb T_{i,r},\mathbb Y_{i,r})$ is now uniformly chosen from $\{(T,Y)\in\widetilde{\mathcal D}^{(i)}:T\in I_r\}$.
5. else if the collection $\mathcal D$ comes from independent design then
6. The random $(\mathbb T_{i,r},\mathbb Y_{i,r})$ is uniformly chosen from $\{(T,Y)\in\mathcal D^{(i)}:T\in I_r\}$.
7. end if
8. Implement the polynomial regression of degree $d$ on each collection $\mathcal D_r$ $(r=1,\ldots,b^{-1})$ of observations. In other words, we are enough to compute for each $r=1,\ldots,b^{-1}$,
\[
(\check a_{r,0},\check a_{r,1},\ldots,\check a_{r,d}):=\operatorname*{argmin}_{(a_0,a_1,\ldots,a_d)\in\mathbb R^{d+1}}\sum_{(T,Y)\in\mathcal D_r}\left[Y-\sum_{s=0}^da_s\left(\frac{T-(q-1)b}{b}\right)^s\right]^2.
\]
If the solution is not available, simply take $(\check a_{r,0},\check a_{r,1},\ldots,\check a_{r,d})=0$.
9. Compute the local polynomial regression estimator $\check f:[0,1]\to\mathbb R$ by
\[
\check f(x):=\sum_{r=1}^{b^{-1}}\sum_{s=0}^d\check a_{r,s}\left(\frac{x-(r-1)b}{b}\right)^s\mathbb 1(x\in I_r)\qquad(0\leq x\leq1).
\]
10. Output the final estimator $\widehat f:[0,1]\to\mathbb R$ through thresholding:
\[
\widehat f:=\begin{cases}\check f&\text{if }\|\check f\|_{\mathcal L^\infty(I_r)}\leq M,\\0&\text{otherwise},\end{cases}\qquad\text{on each }I_r\ (r=1,\ldots,b^{-1}).
\]
''',[7],'Algorithm 1 — Randomized local polynomial regression with thresholding',context=r'Algorithm 1 Randomized local polynomial regression with thresholding $\mathcal A(\mathcal D,b,d,M)$',symbols=[r'\mathcal D_r',r'\widetilde{\mathcal D}^{(i)}'],shape='Randomized per-subject reduction within each interval, local least squares and intervalwise discard-to-zero thresholding. The design type selects one of two branches; neither branch imposes the other design’s assumptions. The printed free q, possible empty selection sets and unstated choices among least-squares minimizers are retained and flagged.')
add('D11','conventional learning algorithm',r'''
We will now present the optimal algorithm $\mathcal A_{\mathrm{CL}}(b_t,d_t,M_t)$ for estimating the mean function under the conventional setup and common design. This algorithm is essentially the same as algorithm $\mathcal A$ with the following four inputs: the target sample $\mathcal D^{[t]}$, a bandwidth $b_t\in1/\mathbb Z^+$, a degree $d_t\in\mathbb Z^+$ of local polynomial and a threshold $M_t>0$.
''',[7],'Section 2.1 — conventional learning algorithm',{'D1':'The input is the target observation sample.','D10':'The conventional estimator is Algorithm 1 applied to that sample with its chosen bandwidth, degree and threshold.'},context=r'The output $\widehat f_{\mathrm{CL}}^{[t]}$ of the conventional learning algorithm $\mathcal A_{\mathrm{CL}}$',symbols=[r'\mathcal A_{\mathrm{CL}}(b_t,d_t,M_t)'],shape='Algorithm 1 with target data only. Both upper-bound theorems use it with their own design-specific parameters. Its occurrence in proofs of conventional minimax attainability is not a dependency of those minimax statements.')
add('D12','Transfer learning for mean function',r'''
Require: Two bandwidths $b_s,b_\delta\in1/\mathbb Z^+$, two degrees $d_s,d_\delta\in\mathbb Z^+$ of polynomial, and two thresholds $M_s,M_\delta>0$.

1. Execute $\mathcal A(\mathcal D^{[s]},b_s,d_s,M_s)$ with the combined source sample $\mathcal D^{[s]}:=\bigcup_{k=1}^K\mathcal D^{[s,k]}$. The result of this algorithm is denoted as $\widehat f^{[s]}$.
2. Compute a new sample $\mathcal D^{[\delta]}:=\{(T_{ij}^{[t]},Y_{ij}^{[t]}-\widehat f^{[s]}(T_{ij}^{[t]})):j=1,\ldots,m_t,i=1,\ldots,n_t\}$.
3. Execute $\mathcal A(\mathcal D^{[\delta]},b_\delta,d_\delta,M_\delta)$. The output of this algorithm is denoted by $\widehat\delta^{[s]}$.
4. Output our final estimator $\widehat f^{[t]}:=\widehat f^{[s]}+\widehat\delta^{[s]}$.
''',[8],'Algorithm 2 — Transfer learning for mean function',{'D2':'The first call pools the K source observation samples.','D1':'The second call uses target responses after subtracting the estimated source mean.','D10':'Both stages use the randomized local polynomial algorithm with separate bandwidths, degrees and thresholds.'},context=r'Algorithm 2 Transfer learning for mean function $\mathcal A_{\mathrm{TL}}(b_s,b_\delta,d_s,d_\delta,M_s,M_\delta)$',symbols=[r'\mathcal D^{[\delta]}',r'\widehat\delta^{[s]}'],shape='Two-stage estimator: pooled source fit, then a target residual fit, then addition. The source populations are not required to share one mean. Subject identities across source groups must remain distinct in the combined sample.')
add('D14','Adaptive transfer learning for mean function under a common design',r'''
1. Randomly partition the target sample $\mathcal D^{[t]}$ into two sub-samples, denoted as $\mathcal D_{\mathrm{train}}^{[t]}$ and $\mathcal D_{\mathrm{test}}^{[t]}$, based on subjects. Specifically, perform a random split of the index set $\{1,\ldots,2n_t\}$ into two partitions, $\mathcal I_{\mathrm{train}}^{[t]}$ and $\mathcal I_{\mathrm{test}}^{[t]}$ such that $|\mathcal I_{\mathrm{train}}^{[t]}|=|\mathcal I_{\mathrm{test}}^{[t]}|=n_t$. We define:
\[
\mathcal D_{\mathrm{train}}^{[t]}:=\{(T_j^{[t]},Y_{ij}^{[t]}):i\in\mathcal I_{\mathrm{train}}^{[t]},j=1,\ldots,m_t\},
\]
\[
\mathcal D_{\mathrm{test}}^{[t]}:=\{(T_j^{[t]},Y_{ij}^{[t]}):i\in\mathcal I_{\mathrm{test}}^{[t]},j=1,\ldots,m_t\}.
\]
2. Execute both $\mathcal A_{\mathrm{CL}}(b_t,d_t,M_t)$ and $\mathcal A_{\mathrm{TL}}(b_s,b_\delta,d_s,d_\delta,M_s,M_\delta)$ following the same specifications as outlined in Theorem 2.2, with the only distinction being that the target sample is provided as $\mathcal D_{\mathrm{train}}^{[t]}$, not $\mathcal D^{[t]}$. The outputs are denoted as $\widehat f_{\mathrm{CL}}^{[t]}$ and $\widehat f_{\mathrm{TL}}^{[t]}$, respectively.
3. Output the following estimator $\widehat g_*^{[t]}$. If a tie occurs, use any randomization to break it.
\[
\widehat g_*^{[t]}:=\operatorname*{argmin}_{\widehat g^{[t]}\in\{\widehat f_{\mathrm{CL}}^{[t]},\widehat f_{\mathrm{TL}}^{[t]}\}}\sum_{i\in\mathcal I_{\mathrm{test}}^{[t]}}\sum_{j=1}^{m_t}\big(Y_{ij}^{[t]}-\widehat g^{[t]}(T_j^{[t]})\big)^2(\Delta T_j^{[t]}),
\]
where $T_0^{[t]}:=0$, $T_{m_t+1}^{[t]}:=1$ and $\Delta T_j^{[t]}:=T_j^{[t]}-T_{j-1}^{[t]}$ for each $j=1,\ldots,m_t+1$.
''',[11],'Algorithm 3 — Adaptive transfer learning for mean function under a common design',{'D8':'The validation loss uses the ordered common target grid and its adjacent spacings.','D11':'One candidate fits the conventional estimator on target training subjects.','D12':'The other candidate uses source data and target training subjects in the transfer estimator.'},context=r'Algorithm 3 Adaptive transfer learning for mean function under a common design $\mathcal A_{\mathrm{ALC}}$',symbols=[r'\widehat g_*^{[t]}',r'\Delta T_j^{[t]}'],shape='Subject-level half split, two candidate fits and spacing-weighted test loss. Theorem 2.2 supplies the base-estimator parameters; its oracle rate comparison is replaced by this empirical comparison. The final averaging over repetitions belongs to Theorem 2.4.')
members['D14']['application_context']=[dict(text='It is further assumed for brevity that the target sample $\mathcal D^{[t]}$ contains $2n_t$ subjects, which does not affect the rate of convergence.',evidence=[dict(page=11,location='Section 2.3 — sample-size convention')])]
add('D16','Adaptive transfer learning for mean function under an independent design',r'''
1. Initialize $\widehat{\mathcal G}^{[t]}=\varnothing$, the collection of candidate estimators.
2. Randomly partition the target sample $\mathcal D^{[t]}$ into two sub-samples, denoted as $\mathcal D_{\mathrm{train}}^{[t]}$ and $\mathcal D_{\mathrm{test}}^{[t]}$, based on subjects. Specifically, perform a random split of the index set $\{1,\ldots,2n_t\}$ into two partitions, $\mathcal I_{\mathrm{train}}^{[t]}$ and $\mathcal I_{\mathrm{test}}^{[t]}$ such that $|\mathcal I_{\mathrm{train}}^{[t]}|=|\mathcal I_{\mathrm{test}}^{[t]}|=n_t$. We define:
\[
\mathcal D_{\mathrm{train}}^{[t]}:=\{(T_{ij}^{[t]},Y_{ij}^{[t]}):i\in\mathcal I_{\mathrm{train}}^{[t]},j=1,\ldots,m_t\},
\]
\[
\mathcal D_{\mathrm{test}}^{[t]}:=\{(T_{ij}^{[t]},Y_{ij}^{[t]}):i\in\mathcal I_{\mathrm{test}}^{[t]},j=1,\ldots,m_t\}.
\]
3. Pick any constants $B_t\geq C_t$ and $d_t\geq\omega(\alpha_m)$.
4. Take a threshold $M_t=\log n_t$.
5. for $b_t\in\{2^r\leq m_tn_t:r\in\mathbb Z^+\}$ do
6. Execute $\mathcal A_{\mathrm{CL}}(b_t,d_t,M_t)$ as if target sample is given as $\mathcal D_{\mathrm{train}}^{[t]}$, not $\mathcal D^{[t]}$.
7. Add the algorithm’s output to the collection $\widehat{\mathcal G}^{[t]}$.
8. end for
9. Pick any constants $B_s\geq C_s$, $B_\delta\geq C_t$, $d_s\geq\omega(\alpha_m)$ and $d_\delta\geq\omega(\alpha_\delta)$.
10. Take thresholds $M_s=\log n_s$ and $M_s=\log n_tn_s$.
11. for $(b_s,b_\delta)\in\{2^r\leq Km_sn_s:r\in\mathbb Z^+\}\times\{2^r\leq m_tn_t:r\in\mathbb Z^+\}$ do
12. Execute $\mathcal A_{\mathrm{TL}}(b_s,b_\delta,d_s,d_\delta,M_s,M_\delta)$ as if target sample is given as $\mathcal D_{\mathrm{train}}^{[t]}$, not $\mathcal D^{[t]}$.
13. Add the algorithm’s output to the collection $\widehat{\mathcal G}^{[t]}$.
14. end for
15. Output the following estimator $\widehat g_*^{[t]}$. If a tie occurs, use any randomization to break it.
\[
\widehat g_*^{[t]}:=\operatorname*{argmin}_{\widehat g^{[t]}\in\widehat{\mathcal G}^{[t]}}\sum_{(T,Y)\in\mathcal D_{\mathrm{test}}^{[t]}}\big(Y-\widehat g^{[t]}(T)\big)^2.
\]
''',[17],'Algorithm 4 — Adaptive transfer learning for mean function under an independent design',{'D9':'The algorithm is specified for the independent design, with individual T_ij values in the split samples.','D3':'The degree conditions use omega(alpha), the strict-integer derivative-order convention of the Hölder class.','D11':'The candidate collection contains conventional fits at the printed candidate bandwidths.','D12':'The candidate collection also contains transfer fits at pairs of printed candidate bandwidths.'},context=r'Algorithm 4 Adaptive transfer learning for mean function under an independent design $\mathcal A_{\mathrm{ALI}}$',symbols=[r'\widehat{\mathcal G}^{[t]}',r'\widehat g_*^{[t]}'],shape='Subject-level half split, multiple bandwidth candidates and unweighted empirical test-loss selection. The source prints positive dyadic bandwidths outside Algorithm 1’s domain, lower-density constants instead of the upper ones, and duplicate M_s assignments. These are preserved, not repaired. Repetition averaging is specified in Theorem 3.4.')
members['D16']['application_context']=[dict(text='It is further assumed for brevity that the target sample $\mathcal D^{[t]}$ contains $2n_t$ subjects, which does not affect the rate of convergence.',evidence=[dict(page=16,location='Section 3.3 — sample-size convention')])]
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed interfaces; extraction remains in progress.')
