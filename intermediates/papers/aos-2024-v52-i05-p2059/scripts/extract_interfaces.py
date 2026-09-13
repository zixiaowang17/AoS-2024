"""Preserve original main-text source entries for the two-Theorem census."""
import json
from save_inventory import ROOT,PID
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,boundary,heading,kind='definition',context=None,context_page=None,phrases=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=phrases or [])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=boundary,semantic_boundary=boundary,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'linear regression model',r'''Consider a linear regression model
\[
y_i=x_i\beta+\mathbf z_i^\top\theta+\epsilon_i,\ i=1,\ldots,n
\]
(1)
with features $x_i\in\mathbb R$ and $\mathbf z_i\in\mathbb R^p$, and random errors $\varepsilon_i$ independent of $(x_i,\mathbf z_i)$.''',[2],[],[r'x_i\beta',r'\mathbf z_i^\top\theta'],'Original linear model, target coefficient beta, nuisance theta and error-feature independence. No Gaussian or iid error assumption is inserted.','Section 1 — Model (1)',kind='source_passage')
add(2,'exchangeable',r'''The noise variables $\varepsilon_1,\ldots,\varepsilon_n$ are exchangeable with in law.''',[2],[1],[], 'Standing joint exchangeability assumption. Preserve the printed wording with in law; exchangeability is not replaced by independence or Gaussianity.','Assumption 1.1',kind='assumption',phrases=['exchangeable'])
add(3,'permutation',r'''Let $x\in\mathbb R^n$ be the target feature, and $Z$ the observation matrix with rows $\mathbf z_1,\ldots,\mathbf z_n$. Define $[n]$ as the vector $(1,\ldots,n)$ and $\pi$ as a permutation of $[n]$. Denote $x_\pi$ and $Z_\pi$ as the row-permuted versions of $x$ and $Z$ respectively.''',[4],[1],[r'x_\pi',r'Z_\pi'],'Original row action and vector convention for [n]. Identity and composition conventions are preserved in auxiliary passages A1-A2, with the same prerequisites.','Section 2.1 — Row permutations')
add(4,'projection matrix',r'''Here, $H^*$ denotes the projection matrix onto the column space of its argument $*$. For instance, $H^{z_\pi z}$ represents the projection matrix onto the column space of $(Z_\pi,Z)$, $H^{x z z_\pi}$ onto that of $(x,Z,Z_\pi)$, etc.''',[4,6],[3],[r'H^*',r'H^{z_\pi z}'],'Projection onto the specified column space. H carries superscripts. No full-column-rank restriction or matrix-inverse formula is supplied or invented.','Section 2.1 — Projection convention')
add(5,'transferability',r'''For any permutations $\pi_1,\pi_2,\sigma$ of $[n]$, the function $T(.,.;x,Z,\varepsilon)$ satisfies
\[
T(\pi_1,\pi_2;x,Z,\varepsilon_\sigma)=T(\pi_1\circ\sigma^{-1},\pi_2\circ\sigma^{-1};x,Z,\varepsilon).
\]''',[9],[3],[r'\varepsilon_\sigma',r'\pi_1\circ\sigma^{-1}',r'\pi_2\circ\sigma^{-1}'],'Generic transferability condition for every triple of permutations. The inverse is composed on the right; no restriction to the PALMRT residual statistic.','Condition 3.1',kind='condition',context=r'''The crucial distinction between $T^{\mathrm{PALMRT}}(...)$ and $T^{\mathrm{FL}}(...)$ or $T^{\mathrm{PERM}}(...)$ lies in the transferability of permutations from the noise parameter $\varepsilon$ to its permutation arguments.''',context_page=8)
add(6,'p-value',r'''Set $\omega_b=\frac12\mathbb 1\{T_{b0}=T_{0b}\}+\mathbb 1\{T_{b0}>T_{0b}\}$.

Construct p-value for $H_0:\beta=0$ as $p_{val}\leftarrow\frac{1+\sum_{b=1}^B\omega_b}{B+1}$.''',[6],[1],[r'\omega_b',r'p_{val}'],'Algorithm 1 steps 5 and 7, with supplied paired statistics. Theorem 3.3 replaces the algorithm statistic-construction step by its own generic T. This entry does not require projections or the PALMRT RSS formula.','Algorithm 1 — Steps 5 and 7')
add(7,'original and permuted statistics',r'''\[
T_{original}=\|(I-H^{x_\pi z z_\pi})y\|_2^2,\qquad T_{perm}=\|(I-H^{x z z_\pi})y\|_2^2.
\]
(3)
We adopt eq. (3) to construct the original and permuted statistics for any given permutation.''',[6],[3,4],[r'T_{original}',r'T_{perm}'],'Concrete residual-statistic pair from (3). Preserve the source assignment of original to the x_pi model and permuted to the x model; the earlier F-statistic versions use different formulas.','Section 2.1 — Statistics (3)')
add(8,'test statistics',r'''In conjunction with the PALMRT $p$-value, a confidence interval for $\beta$ can be constructed by inverting the test. Define $(T_{0b}(\beta),T_{b0}(\beta))$ as the test statistics from replacing $y$ by $(y-x\beta)$ in Algorithm 2 when constructing $(T_{0b},T_{b0})$. Define $f(\beta)$ as $f(\beta)=\frac{1+\sum_{b=1}^B\omega_b(\beta)}{B+1}$, where $\omega_b(\beta)=\mathbb 1\{T_{0b}(\beta)<T_{b0}(\beta)\}+\frac12\mathbb 1\{T_{0b}(\beta)=T_{b0}(\beta)\}$.''',[11],[6,7],[r'T_{0b}(\beta)',r'T_{b0}(\beta)',r'f(\beta)'],'Test inversion uses residualized response y-x beta with the PALMRT pair and p-value recipe. The printed Algorithm 2 reference is retained; the actual pair-construction location is Algorithm 1 and (3), recorded as a source-reference discrepancy rather than a circular dependency.','Section 4 — Test inversion',kind='source_passage')
add(9,'confidence interval',r'''Set $\mathrm{CI}_\alpha=[\beta_{min},\beta_{max}]$ where $\beta_{min}=\inf\{\beta:f(\beta)>\alpha\}$ and $\beta_{max}=\sup\{\beta:f(\beta)>\alpha\}$. Then, we have $\min_\beta\mathbb P[\beta\in\mathrm{CI}_\alpha]>1-2\alpha$, for all $\alpha>0$.''',[11],[8],[r'\mathrm{CI}_\alpha',r'\inf\{\beta:f(\beta)>\alpha\}',r'\sup\{\beta:f(\beta)>\alpha\}'],'Original Corollary 4.1 interval definition and guarantee, retained as a source passage, not added to the Theorem inventory. The interval is the closed hull of the inversion set; no connectedness is assumed.','Corollary 4.1',kind='source_passage',context=r'''By taking the infimum and supremum of this set, we obtain a confidence interval $\mathrm{CI}_\alpha$ with worst-case guarantee at least as strong as direct inversion.''')
add(10,'critical values',r'''Let $t_1<\ldots<t_M$ denote the ordered values of $M$ unique elements in $\cup_{b\in A_1}\{s_b,u_b\}$, and let $(m_l^s,m_l^u)$ represent the sizes of $\#\{b:s_b=t_l\}$ and $\#\{b:u_b=t_l\}$, respectively. As we increase $\beta$ in $f_{A_1}(\beta)$, the function value can only change when we first hit $\{t_l\}_{l=1}^M$, or when $\beta$ slightly increases from these critical values represented. We represent the concept of increasing slightly from these critical values by $\{t_l^+\}_{l=1}^M$, where $t_l^+$ indicates being infinitesimally larger than $t_l$. Using these new quantities introduced, we can re-express $f_{A_1}(t_1)=\frac12(m_1^s-m_1^u)$ and identify induction relations for the function values as we increase $\beta$ to surpass the critical values $t_l$, described as follows:
\[
f_{A_1}(t_{l+1})=f_{A_1}(t_l^+)+\frac12(m_{l+1}^s-m_{l+1}^u),\qquad f_{A_1}(t_l^+)=f_{A_1}(t_l)+\frac12(m_l^s-m_l^u).
\]
(7)''',[12],[3,4,8],[r't_l^+',r'm_l^s',r'm_l^u'],'Critical values and multiplicity sweep. Original coefficient, root, partition and f_A1 formulas are archived in A4-A6; their row-permutation/projection prerequisites are expanded here. Printed formula inconsistencies remain unresolved, not corrected by this census.','Section 4 — Critical values and (7)')
add(11,'Exact CI construction for PALMRT',r'''1: procedure $\mathrm{CI}(y,x,Z,B,\alpha)$ — Confidence interval at coverage level $1-\alpha$.
2: Calculate the $B\times4$ matrix $(c_{b1},c_{b2},c_{b3},c_{b4})_{b=1}^B$ as defined in Lemma 4.3.
3: Calculate $\gamma$, $\{t_l\}_{l=1}^M$, $(m_l^s,m_l^u)_{l=1}^M$.
4: if $\gamma<0$ then
5: $\mathrm{CI}_\alpha=(-\infty,\infty)$.
6: else
7: Set and record $f_{A_1}(t_1)=\frac12(m_1^s-m_1^u)$.
8: for $l=2,\ldots,M$ do
9: Calculate and record $f_{A_1}(t_{l-1}^+)$ and $f_{A_1}(t_l)$ as in eq. (7).
10: end for
11: if $\max(f_{A_1}(.))\leq\gamma$ then
12: $\mathrm{CI}_\alpha=\emptyset$.
13: else
14: $\beta_{min}=\min\{t_l:f_{A_1}(t_l)\vee f_{A_1}(t_l^+)>\gamma\}$.
15: $\beta_{max}=\max\{t_l:f_{A_1}(t_l)\vee f_{A_1}(t_{l-1}^+)>\gamma\}$.
16: $\mathrm{CI}_\alpha=[\beta_{min},\beta_{max}]$.
17: end if
18: end if
19: end procedure''',[13],[3,4,10],[r'\gamma<0',r'\mathrm{CI}_\alpha',r'f_{A_1}(t_l^+)'],'All Algorithm 2 instructions, including the printed 1-alpha comment, empty/whole-line branches and both endpoint rules. Coefficients and gamma are retained in A4-A5. No missing-index, empty-critical-set or formula repair is added.','Algorithm 2 — Exact CI construction for PALMRT',context='Algorithm 2 Exact CI construction for PALMRT')
for i in [2,5]:interfaces[i-1]['lean_role']='predicate'
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
