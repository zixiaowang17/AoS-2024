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
        lean_role='hypothesis' if kind=='condition' else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}

add('D1','i.i.d. sample',r'''
Suppose $X_1,\ldots,X_n$, $X_i=(X_{i1},\ldots,X_{id})$ is an i.i.d. sample of $d$-variate observations with joint cumulative distribution function (cdf) $F$ and continuous marginal cdf's $F_1,\ldots,F_d$. A generic random variable with c.d.f. $F$ will be denoted by $X=(X_1,\ldots,X_d)^\top$.
''',[1],'Section 1 — sampling model',kind='source_passage',phrases=['i.i.d. sample','continuous marginal'],shape='An iid d-variate sample with continuous one-dimensional marginal distribution functions; X without a sample index denotes a generic vector.')
add('D2','independence copula',r'''
where $C$ is the unique copula associated with $X$ and where $\Pi_d$ denotes the $d$-dimensional independence copula defined as
\[
\Pi_d(u)=\prod_{j=1}^du_j,\qquad u=(u_1,\ldots,u_d)^\top\in[0,1]^d.
\]
''',[2],'Section 1 — independence copula',phrases=['independence copula'],symbols=[r'\Pi_d'],shape='Product copula on the unit cube; lower-dimensional versions and its marginal probability measure are used in the hypotheses and integrals.')
add('D3','marginal copula',r'''
where $I_d(k)$ denotes the set of all $A\subset\{1,\ldots,d\}$ of cardinality $k$ and where $C_A$ denotes the $|A|$-dimensional marginal copula of $C$ belonging to the sub-vector $X_A=(X_j)_{j\in A}$.
''',[2],'Section 1 — marginal copula and index sets',phrases=['marginal copula'],symbols=[r'C_A'],shape='Coordinate marginal of a supplied copula, indexed by a subset A of cardinality k. The general evaluation convention G_A(u)=G(u^A) is archived as an auxiliary passage.')
add('D4','hypothesis',r'''
The hypothesis in (1.3) may easily be extended to $k\in\{3,\ldots,d\}$:
\[
H_k:C_A=\Pi_k\text{ for all }A\inI_d(k),\tag{1.4}
\]
i.e., $X$ is $k$-wise dependent. With a slight abuse of notation, $H$ in (1.2) may be written as $H=\bigcap_{k=2}^dH_k$ with $H_2\subset H_3\subset\cdots\subset H_d$.
''',[2],'Section 1 — hypothesis H_k, equation (1.4)',{'D2':'Equation (1.4) compares every k-dimensional marginal with the independence copula Pi_k.','D3':'The quantification is over all coordinate marginal copulas C_A with |A|=k.'},kind='condition',phrases=['hypothesis'],symbols=[r'H_k',r'H_5',r'H_{4m-3}'],note='The words k-wise dependent and the displayed direction of the inclusions are preserved from the source. They conflict with the independence equation; no silent correction is made.',shape='The printed condition C_A=Pi_k for every k-coordinate subset. Theorem 3.1 uses k=5 and k=4m-3 in separate regimes, not just k=2 or k=m.')
add('D5',['pseudo-observations','(max-)rank'],r'''
where the inequality is understood componentwise and where $\widehat U_i=(\widehat U_{i1},\ldots,\widehat U_{id})^\top$ denotes observable pseudo-observations from $C$ defined as
\[
\widehat U_{ip}=\frac{R_{ip}}{n+1},\qquad R_{ip}=\sum_{j=1}^n\mathbf1_{\{X_{jp}\leq X_{ip}\}},\qquad p=1,\ldots,d.
\]
Note that $R_{ip}$ is the (max-)rank of $X_{ip}$ among $X_{1p},\ldots,X_{np}$.
''',[3],'Section 2 — pseudo-observations and ranks',phrases=['pseudo-observations','(max-)rank'],symbols=[r'R_{ip}',r'\widehat U_{ip}'],shape='Coordinatewise max-ranks using weak inequalities, divided by n+1. These are sample constructions; their formulas do not require an independence null.')
add('D6','empirical copula process',r'''
In the interest of improved efficiency, Genest and Rémillard (2004), p. 347, propose to use the previous definition with a version of the empirical copula process that is centered under the null hypothesis $C=\Pi$, namely
\[
\mathbb C^M_{n,A}=\frac1{\sqrt n}\sum_{i=1}^n\prod_{p\in A}\left(\mathbf1_{\{\widehat U_{ip}\leq u_p\}}-U_n(u_p)\right),
\]
where $U_n=U_n(t)=\min\{\lfloor(n+1)t\rfloor/n,1\}$ denotes the cdf of a random variable that is uniformly distributed on $\{1/(n+1),\ldots,n/(n+1)\}$.
''',[4],'Section 2 — empirical copula process centered under the null',{'D5':'The centered product process is evaluated using rank-based pseudo-observations U-hat_ip.'},phrases=['empirical copula process'],symbols=[r'\mathbb C^M_{n,A}',r'U_n'],shape='Centered product process with finite-grid cdf U_n, rather than centering each factor by u_p. The formula defines a process even away from the null; being centered is a null property.')
add('D7','Cramér-von-Mises statistics',r'''
The respective Cramér-von-Mises statistics may then be calculated explicitly, and one obtains:
\[
S^M_{n,A}=\int_{[0,1]^{|A|}}\{\mathbb C^M_{n,A}(u)\}^2\,d\Pi_A((u_j)_{j\in A})=\frac1n\sum_{i,j=1}^n\prod_{p\in A}I^{(p)}_{i,j},\tag{2.1}
\]
where
\[
I^{(p)}_{i,j}=\frac{2n+1}{6n}+\frac{R_{ip}(R_{ip}-1)}{2n(n+1)}+\frac{R_{jp}(R_{jp}-1)}{2n(n+1)}-\frac{\max(R_{ip},R_{jp})}{n+1}.
\]
''',[4],'Section 2 — Cramér-von-Mises statistics, equation (2.1)',{'D6':'The integral squares the process with finite-grid centering U_n.','D2':'The integration measure is the independence copula measure.','D3':'Pi_A is the coordinate marginal of the product copula for the subset A.','D5':'The equivalent finite-sample formula uses the max-ranks R_ip and R_jp.'},phrases=['Cramér-von-Mises statistics'],symbols=[r'S^M_{n,A}',r'I^{(p)}_{i,j}'],shape='Squared integrated centered product process, with its exact all-pairs rank formula including diagonal terms. The differently centered bar-S statistic is not substituted.')
add('D8',['expectation','variance'],r'''
For the purpose of aggregating over various index sets $A$, it is helpful to calculate expectation and variance of $S^M_{n,A}$. For $A\subset\{2,\ldots,d\}$ such that $|A|=k\in\{2,\ldots d\}$, let
\[
\mu_n(k):=\mathbb E_{H_k}\left[S^M_{n,A}\right],\qquad\sigma_n^2(k):=\operatorname{Var}_{H_k}(S^M_{n,A}),\tag{2.2}
\]
where $\mathbb E_{H_k}$ denotes expectation under $H_k$.
''',[4],'Section 2 — null expectation and variance, equation (2.2)',{'D7':'The moments are of the centered Cramer-von-Mises statistic S^M_n,A.','D4':'The expectation and variance are taken under the k-wise independence hypothesis H_k.'},phrases=['expectation','variance'],symbols=[r'\mu_n(k)',r'\sigma_n^2(k)'],note='The source writes A as a subset of {2,...,d} here, despite using {1,...,d} elsewhere. This transcription preserves that discrepancy.',shape='Finite-sample mean and variance under H_k of the selected subset statistic. These are not empirical sample moments or moments under an arbitrary alternative.')
add('D9','aggregation',r'''
More precisely, for some given $k\in\{2,\ldots,m\}$, we consider the following aggregation over all sets $A\subset\{1,\ldots,d\}$ with $|A|=k$:
\[
T_n(k)=\sum_{\substack{A\subset\{1,\ldots,d\}\\|A|=k}}S^M_{n,A}.\tag{3.1}
\]
''',[5],'Section 3 — aggregation, equation (3.1)',{'D7':'T_n(k) sums the S^M_n,A statistics over every k-element coordinate subset.'},phrases=['aggregation'],symbols=[r'T_n(k)',r'T_n(2)',r'T_n(m)'],shape='Unweighted sum of the subset Cramer-von-Mises statistics over all k-element subsets, for fixed k between 2 and m. This is not the further normalized sum in Corollary 3.2.')
add('D10','scaling sequences',r'''
Recalling $\mu_n(k)$ and $\sigma_n^2(k)$ from (2.2) (with explicit formulas provided in Lemma 2.1), this motivates the introduction of the following scaling sequences:
\[
\nu_n(k)=\binom dk\cdot\mu_n(k)=\binom dk\cdot\left\{\left[\frac16-\frac1{6n}\right]^k+(n-1)\left(\frac{-1}{6n}\right)^k\right\},
\]
and
\[
\bar\delta_n(k)=\sqrt{\sigma_n^2(k)\cdot\binom dk},\qquad\delta_n(k)=\sqrt{\frac2{90^k}\cdot\binom dk}.\tag{3.2}
\]
''',[5],'Section 3 — scaling sequences, equation (3.2)',{'D8':'The centering nu_n and finite-sample scale bar-delta_n use the null mean and variance from equation (2.2); delta_n instead uses the displayed limiting-variance constant.'},phrases=['scaling sequences'],symbols=[r'\nu_n',r'\delta_n',r'\bar\delta_n'],shape='The three printed centering/scaling sequences retain their distinct formulas. Finite-sample bar-delta and asymptotic delta are not equated, and the final theorem replacement is preserved as written.')
add('D11','martingale array',r'''
Let $d=d_n\to\infty$. Let $\eta^2$ be an a.s. finite r.v. and let $\{(S_{n,r},\mathcal F_{n,r}):1\leq r\leq d,n\geq1\}$ be a zero-mean, square integrable martingale array with differences $X_{n,r}=S_{n,r}-S_{n,r-1}$. If $\mathcal F_{n,r}\subset\mathcal F_{n+1,r}$ for all $1\leq r\leq d$ and $n\geq1$ and if
''',[20],'Theorem 6.5 — martingale array and filtration conditions',kind='theorem_excerpt',phrases=['martingale array'],symbols=[r'\mathcal F_{n,r}',r'X_{n,r}'],shape='Zero-mean square-integrable martingale triangular array with its difference sequence and cross-row filtration inclusion. This generic array does not inherit the paper-specific copula sampling model.')
interfaces[-1]['lean_role']='hypothesis'
add('D12','Lindeberg condition',r'''
\[
\forall\varepsilon>0:\quad\sum_{r=1}^d\mathbb E\left[X_{n,r}\mathbf1_{\{|X_{n,r}|>\varepsilon\}}\mid\mathcal F_{n,r-1}\right]\xrightarrow[n\to+\infty]{\mathbb P}0,\tag{6.24}
\]
''',[20],'Theorem 6.5 — Lindeberg condition, equation (6.24)',{'D11':'The condition uses the martingale differences X_n,r and their preceding filtration F_n,r-1 from the theorem setup.'},kind='theorem_excerpt',context='Moreover, the Lindeberg condition in (6.24) is a consequence of the Lyapunov condition:',phrases=['Lindeberg condition'],symbols=[r'\mathbf1_{\{|X_{n,r}|>\varepsilon\}}'],note='Equation (6.24) is printed with X_n,r to the first power, not squared. It is retained as printed and must not be identified with a corrected standard condition without a separate source decision.',shape='Printed conditional truncated first-moment convergence for every epsilon>0; fidelity record, not a silently repaired standard conditional Lindeberg predicate.')
interfaces[-1]['lean_role']='hypothesis'
add('D13','Lyapunov condition',r'''
\[
\sum_{r=1}^d\mathbb E\left[X_{n,r}^4\mid\mathcal F_{n,r-1}\right]\xrightarrow[n\to+\infty]{\mathbb P}0.\tag{6.26}
\]
''',[20],'Theorem 6.5 — Lyapunov condition, equation (6.26)',{'D11':'The fourth-moment sum is of the martingale differences conditional on the preceding array filtration.'},kind='theorem_excerpt',context='Moreover, the Lindeberg condition in (6.24) is a consequence of the Lyapunov condition:',phrases=['Lyapunov condition'],symbols=[r'X_{n,r}^4'],shape='Conditional fourth-moment sum converging in probability to zero, offered as a sufficient condition in the final theorem clause, not an additional simultaneous assumption.')
interfaces[-1]['lean_role']='hypothesis'

def main():
 for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('interface-draft.json',interfaces)]:
  (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(f'Saved {len(interfaces)} source interfaces.')
if __name__=='__main__':main()
