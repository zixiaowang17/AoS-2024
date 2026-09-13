"""Original main-text passages; mathematical typos are preserved, not repaired."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
interfaces=[];members={};edges={}
def add(lid,term,body,pages,heading,deps=None,*,context=None,kind='definition',role='definition',symbols=(),phrases=(),note=None,shape):
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_kind=kind,source_heading=heading,
        statement_original=body.strip(),relation='exact',depends_on=list(deps or {}),
        evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=list(symbols),highlight_phrases=list(phrases))
    key=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if context:
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])];key['context_id']=lid+'/name'
    assert term in (context or body),(lid,term)
    if note:m['variant_note']=note
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=key['label'],lean_role=role,type_shape=shape,
        semantic_boundary=shape,members=[m],source_keywords=[key],central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}

add('D1','random sample',r'''Suppose that we draw a random sample, $\{(\mathbf{x}_i,\mathbf{y}_i):i=1,\ldots,n\}$, from the joint distribution of $(\mathbf{x},\mathbf{y})$, where $\mathbf{x}_i=(X_{i,1},\ldots,X_{i,p})^{\mathrm{T}}$ and $\mathbf{y}_i=(Y_{i,1},\ldots,Y_{i,q})^{\mathrm{T}}$. To avoid ties among the observations, we merely consider continuous random vectors in the sequel.''',[4],
    'Section 2.1 — random sample and continuous observations',kind='source_passage',phrases=['random sample','continuous random vectors'],shape='Random sample of paired p- and q-dimensional observations; the section assumes continuous random vectors to exclude ties.')
add('D2','U-statistic',r'''Let $h:(\mathbb{R}^1\times\mathbb{R}^1)^d\to\mathbb{R}^1$ be a fixed kernel of order $d\geq2$, which is symmetric and invariant to permutations of all arguments. For any pair of distinctive indices $k\in\{1,\ldots,p\}$ and $l\in\{1,\ldots,q\}$, a standard U-statistic induced by the kernel $h$ takes the form
\[
\widehat U_h^{(kl)}=\{C(n,d)\}^{-1}\sum_{1\leq i_1\leq\cdots\leq i_d\leq n}h\{(X_{i_1,k},Y_{i_1,l}),\ldots,(X_{i_d,k},Y_{i_d,l})\},
\]
where $C(n,d)$ denotes the number of all combinations of $d$ distinct elements from $\{1,\ldots,n\}$.''',[4],
    'Section 2.1 — symmetric kernel and U-statistic',{'D1':'Each argument is an observation of a coordinate pair from the random sample.'},phrases=['U-statistic'],symbols=[r'\widehat U_h^{(kl)}'],
    note='The displayed sum has non-strict index inequalities, while the following text says distinct elements. Both are preserved.',shape='Coordinate-pair U-statistic with the printed non-strict sum and distinct-combination normalization; the discrepancy is unresolved.')
add('D3','Hoeffding’s D',r'''(a) The kernel $h^{(D)}$ for Hoeffding’s $D$ is defined as
\[
\begin{aligned}
h^{(D)}(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{5,kl})={}&\frac{1}{480}\sum_{(i_1,\ldots,i_5)\in\mathcal P_5}\psi(X_{i_1,k},X_{i_2,k},X_{i_5,k})\\
&\psi(X_{i_3,k},X_{i_4,k},X_{i_5,k})\psi(Y_{i_1,l},Y_{i_2,l},Y_{i_5,l})\psi(Y_{i_3,l},Y_{i_4,l},Y_{i_5,l}).
\end{aligned}
\]''',[4],'Definition 1(a) — Hoeffding’s D',{'D1':'The kernel uses the observed coordinate-pair notation z_i,kl.'},context='(a) The kernel $h^{(D)}$ for Hoeffding’s D is defined as',symbols=[r'h^{(D)}'],shape='Order-five symmetric permutation-average kernel; psi and permutation notation are archived as local auxiliary definitions.')
add('D4','Blum-Kiefer-Rosenblatt’s R',r'''(b) The kernel $h^{(R)}$ for Blum-Kiefer-Rosenblatt’s $R$ is defined as
\[
\begin{aligned}
h^{(R)}(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{6,kl})={}&\frac{1}{2880}\sum_{(i_1,\ldots,i_6)\in\mathcal P_6}\psi(X_{i_1,k},X_{i_2,k},X_{i_5,k})\\
&\psi(X_{i_3,k},X_{i_4,k},X_{i_5,k})\psi(Y_{i_1,l},Y_{i_2,l},Y_{i_6,l})\psi(Y_{i_3,l},Y_{i_4,l},Y_{i_6,l}).
\end{aligned}
\]''',[4],'Definition 1(b) — Blum-Kiefer-Rosenblatt’s R',{'D1':'The kernel uses the observed coordinate-pair notation z_i,kl.'},context='(b) The kernel $h^{(R)}$ for Blum-Kiefer-Rosenblatt’s R is defined as',symbols=[r'h^{(R)}'],shape='Order-six symmetric permutation-average kernel; retain the separate fifth X and sixth Y reference observations.')
add('D5','Bergsma-Dassios-Yanagimoto’s τ∗',r'''(c) The kernel $h^{(\tau^*)}$ for Bergsma-Dassios-Yanagimoto’s $\tau^*$ is defined as
\[
\begin{aligned}
h^{(\tau^*)}(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{4,kl})={}&\frac{1}{24}\sum_{(i_1,\ldots,i_4)\in\mathcal P_4}\omega(X_{i_1,k},X_{i_2,k},X_{i_3,k},,X_{i_4,k})\\
&\omega(Y_{i_1,l},Y_{i_2,l},Y_{i_3,l},Y_{i_4,l}).
\end{aligned}
\]''',[4],'Definition 1(c) — Bergsma-Dassios-Yanagimoto’s τ∗',{'D1':'The kernel uses the observed coordinate-pair notation z_i,kl.'},context='(c) The kernel $h^{(\\tau^*)}$ for Bergsma-Dassios-Yanagimoto’s τ∗ is defined as',symbols=[r'h^{(\tau^*)}'],note='The extra comma in the X arguments and the source omega definition are preserved; no corrected standard kernel is substituted.',shape='Order-four symmetric permutation-average kernel using the original omega formula in local auxiliary definitions.')
add('D6','projections',r'''Let $h_c(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{c,kl})=E\{h(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{d,kl})\mid\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{c,kl}\}$ be the projections of $h$ onto the lower dimensional spaces, $\widetilde h=h-E\{h(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{d,kl})\}$ and $\widetilde h_c=h_c-E\{h(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{d,kl})\}$ for $c=1,\ldots,d$. Let
\[
g_h^{(c)}(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{c,kl})=\widetilde h_c-\sum_{j=1}^{c-1}\sum_{1\leq i_1<\cdots<i_j\leq c}g_h^{(j)}(\mathbf{z}_{i_1,kl},\ldots,\mathbf{z}_{i_j,kl}),\tag{2}
\]
where $g_h^{(1)}(\mathbf{z}_{1,kl})=\widetilde h_1(\mathbf{z}_{1,kl})$.''',[4,5],
    'Section 2.1 — projections and recursive centered components, equation (2)',{'D2':'The projections refer to the symmetric fixed kernel h and its order d.'},phrases=['projections'],symbols=[r'g_h^{(c)}'],shape='Conditional projections, centered projections and recursive Hoeffding components; preserve the printed omission of arguments on tilde h_c.')
add('D7','finite adjustment factor',r'''where $d$ is the order of kernel, and $\Delta_h$ is a finite adjustment factor,
\[
d=\begin{cases}5,&\text{if }h=h^{(D)},\\6,&\text{if }h=h^{(R)},\\4,&\text{if }h=h^{(\tau^*)}.\end{cases}
\quad\text{and}\quad
\Delta_h=\begin{cases}40,&\text{if }h=h^{(D)},\\60,&\text{if }h=h^{(R)},\\2/3,&\text{if }h=h^{(\tau^*)}.\end{cases}
\]''',[5],'Section 2.2 — kernel orders and finite adjustment factors',{
 'D3':'The D branch has order five and factor forty.','D4':'The R branch has order six and factor sixty.','D5':'The tau-star branch has order four and factor two-thirds.'},phrases=['finite adjustment factor'],symbols=[r'\Delta_h'],shape='Three case-dependent kernel orders and multipliers. The cases are alternatives, not simultaneous assumptions on one kernel.')
add('D8','test statistic',r'''To test $H_0$ in (1), we consider the test statistic which aggregates pairwise the U-statistics $\widehat U_h^{(kl)}$ to form
\[
\widehat T_h^{\natural}=\Delta_h\{C(d,2)\}^{-1}\{C(n,2)\}^{1/2}\sum_{k=1}^p\sum_{l=1}^q\widehat U_h^{(kl)},\tag{4}
\]''',[5],'Section 2.2 — aggregate test statistic, equation (4)',{
 'D2':'The aggregate sums each coordinate-pair U-statistic.','D7':'Its scaling uses the selected kernel order and Delta-h.'},phrases=['test statistic'],symbols=[r'\widehat T_h^{\natural}'],shape='Unnormalized aggregate statistic (4); its intended use for H0 does not restrict the statistic to independent data.')
add('D9','variance',r'''We now provide an estimate for the variance of $\widehat T_h^{\natural}$. Let
\[
\begin{aligned}
A_1^{(k)}(u,v)&=F_{X_k}^{2}(u)+F_{X_k}^{2}(v)-2\max\{F_{X_k}(u),F_{X_k}(v)\}+2/3,k=1,\ldots,p\\
A_2^{(l)}(u,v)&=F_{Y_l}^{2}(u)+F_{Y_l}^{2}(v)-2\max\{F_{Y_l}(u),F_{Y_l}(v)\}+2/3,l=1,\ldots,q,
\end{aligned}
\]
where $F_{X_k}(u)=\operatorname{pr}(X_k\leq u)$ and $F_{Y_l}(v)=\operatorname{pr}(Y_l\leq v)$.''',[5],'Section 2.2 — marginal kernels for the variance',{'D1':'The functions use the marginal cdfs of the sampled coordinates.'},phrases=['variance'],symbols=[r'A_1^{(k)}',r'A_2^{(l)}'],note='The author gives these auxiliary functions only symbolic names. The entry retains the adjacent source term variance, without asserting that A_1 or A_2 is itself a variance.',shape='Two cdf-based marginal kernels used in the variance calculation; their formulas do not require the null hypothesis.')
add('D10','variance term',r'''By Hoeffding decomposition, we have, under $H_0$,
\[
\Delta_h\{C(d,2)\}^{-1}\widehat U_h^{(kl)}=\{C(n,2)\}^{-1}\sum_{1\leq i<j\leq n}A_1^{(k)}(X_{ik},X_{jk})A_2^{(l)}(Y_{il},Y_{jl})+\widehat R_h^{(kl)},
\]
where $\widehat R_h^{(kl)}$ is a remainder term. It follows that $\widehat T_h^{\natural}=\widehat J^{(1)}+\widehat J_h^{(2)}$, where
\[
\widehat J^{(1)}=\{C(n,2)\}^{-1/2}\sum_{1\leq i<j\leq n}\sum_{k=1}^p\sum_{l=1}^q A_1^{(k)}(X_{ik},X_{jk})A_2^{(l)}(Y_{il},Y_{jl}),\quad\text{and}
\]
\[
\widehat J_h^{(2)}=\{C(n,2)\}^{1/2}\sum_{k=1}^p\sum_{l=1}^q\widehat R_h^{(kl)}.
\]
If both $p$ and $q$ are fixed, by the standard U-statistic theory, $\widehat J^{(1)}$ plays a dominating role in determining the asymptotic null distributions of our proposed rank-based indices. It motivates us to anticipate that this phenomenon remains to be true in high dimensional settings. In Lemma 1 of the Supplement, we show that, under $H_0$, $\widehat J^{(1)}$ remains to be a leading term and $\widehat J_h^{(2)}$ is asymptotically negligible even when $\max(p,q)\to\infty$. Therefore, under $H_0$, the variance of $\widehat T_h^{\natural}$, denoted as $S^2$, is dominated by
\[
\begin{aligned}
\operatorname{var}\{\widehat J^{(1)}\}={}&\left[\sum_{k_1=1}^p\sum_{k_2=1}^p E\{A_1^{(k_1)}(X_{1k_1},X_{2k_1})A_1^{(k_2)}(X_{1k_2},X_{2k_2})\}\right]\\
&\left[\sum_{l_1=1}^q\sum_{l_2=1}^q E\{A_2^{(l_1)}(Y_{1l_1},Y_{2l_1})A_2^{(l_2)}(Y_{1l_2},Y_{2l_2})\}\right].\tag{5}
\end{aligned}
\]
By the definition of $\widehat J^{(1)}$, the variance term, $S^2$, does not depend on $h$ under $H_0$ in an asymptotic sense.''',[5,6],'Section 2.2 — null variance term and leading-term variance, equation (5)',{
 'D8':'The source describes S squared as the variance of the aggregate statistic.','D9':'The leading-term expression uses the two marginal kernels.','D18':'The decomposition and product variance are stated under independence H0.'},phrases=['variance term'],symbols=[r'S^2'],kind='source_passage',note='The passage distinguishes the full statistic variance from its dominating leading-term variance, then reuses S squared. No exact equality between those two finite-sample variances is silently asserted.',shape='Original null-variance passage, preserving its asymptotic qualification and unresolved reuse of S squared; excludes the supplement proof.')
add('D11','unbiased estimate',r'''Under $H_0$, the unbiased estimate of $S^2$ is defined as follows,
\[
\widehat S^2=\left\{\sum_{k_1=1}^p\sum_{k_2=1}^p\widehat S_1^{(k_1k_2)}\right\}\left\{\sum_{l_1=1}^q\sum_{l_2=1}^q\widehat S_2^{(l_1l_2)}\right\},\tag{6}
\]
where
\[
\begin{aligned}
\widehat S_1^{(k_1k_2)}={}&\{n(n-1)(n-2)(n-3)(n-4)(n-5)\}^{-1}\\
&\sum_{(i_1,\ldots,i_6)}^n\psi(X_{i_1k_1},X_{i_3k_1},X_{i_4k_1})\psi(X_{i_2k_1},X_{i_5k_1},X_{i_6k_1})\\
&\psi(X_{i_1k_2},X_{i_3k_2},X_{i_4k_2})\psi(X_{i_2k_2},X_{i_5k_2},X_{i_6k_2}),\quad\text{and}\\
\widehat S_2^{(l_1l_2)}={}&\{n(n-1)(n-2)(n-3)(n-4)(n-5)\}^{-1}\\
&\sum_{(i_1,\ldots,i_6)}^n\psi(Y_{i_1l_1},Y_{i_3l_1},Y_{i_4l_1})\psi(Y_{i_2l_1},Y_{i_5l_1},Y_{i_6l_1})\\
&\psi(Y_{i_1l_2},Y_{i_3l_2},Y_{i_4l_2})\psi(Y_{i_2l_2},Y_{i_5l_2},Y_{i_6l_2}).
\end{aligned}
\]
In the above displays, the summations are taken over all possible permutations of distinctive indices.''',[6],'Section 2.2 — unbiased estimate, equation (6)',{
 'D1':'The formula is evaluated on the sampled coordinates.','D10':'The source identifies its target as the null variance term S squared.'},phrases=['unbiased estimate'],symbols=[r'\widehat S^2'],shape='Product of coordinate sums of six-distinct-index estimators; retain the signed expression and do not impose an unprinted nonnegativity correction.')
add('D12','normalized test statistic',r'''With $\widehat S$ defined in (6), the normalized test statistic has the form of
\[
\widehat T_h=\widehat T_h^{\natural}/\widehat S.
\]''',[6],'Section 2.2 — normalized test statistic',{'D8':'The numerator is the aggregate statistic (4).','D11':'The denominator is the square root of the estimate in (6), with the source convention retained.'},phrases=['normalized test statistic'],symbols=[r'\widehat T_h'],shape='Studentized aggregate statistic with the printed S-hat denominator; no zero/negative estimate convention is supplied.')
add('D13','Asymptotic analysis under the null',r'''Define
\[
V_1(\mathbf{x}_1,\mathbf{x}_2)=\sum_{k=1}^p A_1^{(k)}(X_{1k},X_{2k}),\quad\text{and}\quad V_2(\mathbf{y}_1,\mathbf{y}_2)=\sum_{l=1}^q A_2^{(l)}(Y_{1l},Y_{2l}).
\]''',[7],'Section 2.3 — coordinate sums V1 and V2',{'D9':'Each V is the sum of its corresponding marginal cdf kernel.'},context='Asymptotic analysis under the null',symbols=[r'V_1(\mathbf{x}_1,\mathbf{x}_2)',r'V_2(\mathbf{y}_1,\mathbf{y}_2)'],note='V1 and V2 have no individual natural-language name in the source; the section heading is retained as the indexing term.',shape='Coordinate sums used in the null moment condition; these functions themselves are defined without imposing independence between x and y.')
add('D14','Assumption 1',r'''Assume that, as $p\to\infty$,
\[
E\{V_1(\mathbf{x}_1,\mathbf{x}_2)^4\}/[nE^2\{V_1(\mathbf{x}_1,\mathbf{x}_2)^2\}]\to0,
\]
\[
E\{V_1(\mathbf{x}_1,\mathbf{x}_2)V_1(\mathbf{x}_2,\mathbf{x}_3)V_1(\mathbf{x}_3,\mathbf{x}_4)V_1(\mathbf{x}_4,\mathbf{x}_1)\}/E^2\{V_1(\mathbf{x}_1,\mathbf{x}_2)^2\}\to0;
\]
and in parallel, assume that, as $q\to\infty$,
\[
E\{V_2(\mathbf{y}_1,\mathbf{y}_2)^4\}/[nE^2\{V_2(\mathbf{y}_1,\mathbf{y}_2)^2\}]\to0,
\]
\[
E\{V_2(\mathbf{y}_1,\mathbf{y}_2)V_2(\mathbf{y}_2,\mathbf{y}_3)V_2(\mathbf{y}_3,\mathbf{y}_4)V_2(\mathbf{y}_4,\mathbf{y}_1)\}/E^2\{V_2(\mathbf{y}_1,\mathbf{y}_2)^2\}\to0.
\]''',[7],'Assumption 1',{'D13':'The four limits use the coordinate sums V1 and V2.'},context='Assumption 1',kind='assumption',role='hypothesis',phrases=['Assumption 1'],shape='Two moment-ratio limits in the p-divergent regime and two parallel limits in the q-divergent regime. Do not require both dimensions to diverge.')
add('D15','normal approximation',r'''Let $\mathbf{z}_i=(\mathbf{x}_i^{\mathrm T},\mathbf{y}_i^{\mathrm T})^{\mathrm T}$, for $i=1,\ldots,n$. Define $V(\mathbf{z}_1,\mathbf{z}_2)=V_1(\mathbf{x}_1,\mathbf{x}_2)V_2(\mathbf{y}_1,\mathbf{y}_2)$. The following theorem provides an explicit uniform bound on the error of normal approximation to the null distribution of $\widehat T_h$.''',[9],'Section 2.3 — product kernel V for normal approximation',{'D13':'V is the product of the two coordinate-sum functions.'},phrases=['normal approximation'],symbols=[r'V(\mathbf{z}_1,\mathbf{z}_2)'],note='The source defines V symbolically; its adjacent phrase normal approximation is retained for indexing.',shape='Product of the two marginal coordinate sums, on paired observations; its source correspondence is the fourth-moment bound in Theorem 3.')
add('D16','local alternatives',r'''Define
\[
\theta_h^{(kl)}=E\{h(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{d,kl})\},
\]
\[
\zeta_h^{(c)}=\operatorname{var}\left\{\sum_{k=1}^p\sum_{l=1}^q h_c(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{c,kl})\right\},\quad\text{and}
\]
\[
\widehat M_h^{(c)}=\sum_{1\leq i_1<\cdots<i_c\leq n}G_h^{(c)}(\mathbf{z}_{i_1,kl},\ldots,\mathbf{z}_{i_c,kl}),
\]
for $c=1,\ldots,d$, where
\[
G_h^{(c)}(\mathbf{z}_1,\ldots,\mathbf{z}_c)=\sum_{k=1}^p\sum_{l=1}^q g_h^{(c)}(\mathbf{z}_{1,kl},\ldots,\mathbf{z}_{c,kl}).
\]''',[10],'Section 2.4 — expectation and projection sums under local alternatives',{'D6':'The definitions use h, h_c and the recursive g_h components.'},context='Asymptotic analysis under local alternatives',symbols=[r'\theta_h^{(kl)}',r'\zeta_h^{(c)}',r'G_h^{(c)}'],shape='Original bundled expectation and projection-sum definitions; retain the printed kl subscripts in the M-hat display even though G_h is next defined on full vectors.')
add('D17','class of local alternatives',r'''To explore the power performance of our proposed test, we consider local alternatives where some $X_k$s and $Y_l$s are dependent. When $\max(p,q)\to\infty$ and $n\to\infty$, we assume that the class of local alternatives satisfy
\[
\zeta_h^{(c)}=o\{n^{c-2}S_h^2\},\quad c\in\{1,3,\ldots,d\},\tag{8}
\]
\[
E\{G_h^{(2)}(\mathbf{z}_1,\mathbf{z}_2)G_h^{(2)}(\mathbf{z}_2,\mathbf{z}_3)G_h^{(2)}(\mathbf{z}_3,\mathbf{z}_4)G_h^{(2)}(\mathbf{z}_4,\mathbf{z}_1)\}=o(S_h^4),\tag{9}
\]
\[
E[\{G_h^{(2)}(\mathbf{z}_1,\mathbf{z}_2)\}^4]=o(nS_h^4),\tag{10}
\]
where
\[
S_h^2=\operatorname{var}\left\{\sum_{k=1}^p\sum_{l=1}^q h_2(\mathbf{z}_{1,kl},\mathbf{z}_{2,kl})\right\}=\Delta_h^{-2}S^2.
\]''',[10],'Section 2.4 — conditions (8)-(10) and variance scale',{
 'D16':'The conditions use the projection variances zeta_h and sums G_h.','D6':'S_h is the variance of the sum of second conditional projections.','D7':'The displayed relation to S uses the adjustment factor Delta-h.'},kind='condition',role='hypothesis',phrases=['class of local alternatives'],symbols=[r'S_h^2',r'G_h^{(2)}'],note='The scale S is specified here through S_h. The independent-null product formula (5) is not substituted under dependence.',shape='Local-alternative negligibility and moment conditions with their own variance scale; no contamination model or independence null is imposed.')
add('D18','independent',r'''Let $\mathbf{x}=(X_1,\ldots,X_p)^{\mathrm T}\in\mathbb R^p$ and $\mathbf{y}=(Y_1,\ldots,Y_q)^{\mathrm T}\in\mathbb R^q$ be two random vectors with possibly different dimensions. We aim to test
\[
H_0:\mathbf{x}\text{ and }\mathbf{y}\text{ are independent, versus, }H_1:\text{ otherwise},\tag{1}
\]
under the asymptotic regime where either the dimension of $\mathbf{x}$, or that of $\mathbf{y}$, or both, diverge to infinity as the sample size $n$ grows.''',[1],'Section 1 — independence null, equation (1)',kind='condition',role='hypothesis',phrases=['independent'],symbols=[r'H_0'],shape='Independence between the two vectors, permitting dependence within either vector and unequal dimensions.')

def main():
    for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('interface-draft.json',interfaces)]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved 18 original source entries.')
if __name__=='__main__':main()
