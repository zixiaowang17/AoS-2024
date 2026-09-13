"""Rebuild original main-text passages and local dependencies for this paper.

The saved data is manually transcribed; source audit is a separate stage.
"""
import json
from pathlib import Path
from save_inventory import PID, claims

ROOT = Path(__file__).resolve().parents[1]
interfaces, members, edges = [], {}, {}


def add(lid, term, body, pages, heading, deps=None, *, kind='definition',
        symbols=(), phrases=(), context=None, context_pages=None, shape):
    evidence = [dict(page=p, location=heading) for p in pages]
    member = dict(paper_id=PID, local_id=lid, local_label=heading,
        source_heading=heading, source_kind=kind, statement_original=body.strip(),
        relation='exact', depends_on=list(deps or {}), evidence=evidence,
        highlight_symbols=list(symbols), highlight_phrases=list(phrases))
    keyword = dict(paper_id=PID, local_id=lid, source_text=term,
                   label=term[0].upper()+term[1:], kind='term')
    if term not in body:
        assert context and term in context, (lid, term)
        member['naming_context'] = [dict(context_id=lid+'/name', text=context,
            evidence=[dict(page=p, location=heading+' — naming context') for p in (context_pages or pages)])]
        keyword['context_id'] = lid+'/name'
    interfaces.append(dict(interface_id=PID+'/'+lid, rank_group='all', name=keyword['label'],
        lean_role='hypothesis' if kind in ('condition', 'assumption') else 'definition',
        type_shape=shape, semantic_boundary=shape, members=[member], source_keywords=[keyword],
        central_claim_uses=[], dependencies=[], theorem_explanations={}))
    members[lid] = member
    edges[lid] = deps or {}


add('D1','image measure',r'''
For a statistic $T=t(X^n)$, we write $\mathbf P^T$ for the image measure of $\mathbf P$ under $t$, that is, $\mathbf P^T\{T\in B\}=\mathbf P\{t(X^n)\in B\}$.
''',[3],'Section 2.1 — image measure',symbols=[r'\mathbf P^T'],shape='Pushforward law of a measurable statistic. Superscripts V_n and M_n in theorems use this convention.')
add('D2','marginal distribution',r'''
Furthermore, for a prior distribution $\boldsymbol\Pi$ on $\Theta$, we write $\boldsymbol\Pi^\theta\mathbf P_\theta$ for the marginal distribution that assigns probability $\boldsymbol\Pi^\theta\mathbf P_\theta\{X\in B\}=\int\mathbf P_\theta\{X\in B\}d\boldsymbol\Pi(\theta)$ to any measurable set $B$.
''',[3],'Section 2.1 — marginal distribution under a prior',symbols=[r'\boldsymbol\Pi^\theta\mathbf P_\theta'],shape='Probability mixture over a parameter; in the theorems the parameter space is G and the superscript g binds the mixture index. It is not a group action on measures.')
add('D3','Kullback-Leibler',r'''
The Kullback-Leibler (KL) divergence between $\mathbf Q$ and $\mathbf P$ is denoted by $\operatorname{KL}(\mathbf Q,\mathbf P)=\mathbf E^{\mathbf Q}[\ln(dQ/dP)]$ (Kullback and Leibler, 1951).
''',[3,4],'Section 2.1 — Kullback-Leibler divergence',symbols=[r'\operatorname{KL}(\mathbf Q,\mathbf P)',r'dQ/dP'],shape='Ordered relative entropy with Q as expectation law. The printed Radon-Nikodym numerator and denominator omit bold font; infinite-divergence conventions are not spelled out here.')
add('D4','action',r'''
If $G$ acts on $\mathcal X$, then we denote the action of $G$ on $\mathcal X$ by $(g,x)\mapsto gx$ for $g\in G$ and $x\in\mathcal X$, and extend the action to $\mathcal X^n$ component-wise; that is, $(g,x^n)\mapsto gX^n:=(gx_1,\ldots,gx_n)$ for $g\in G$ and $x^n\in\mathcal X^n$. We write $gB=\{gb:b\in B\}$ for the left translate of a subset $B\subseteq\mathcal X$ by $g$. If $G$ acts on $\Theta$, the notation is completely analogous.
''',[4],'Section 2.1 — group action and left translates',symbols=[r'gX^n:=(gx_1,\ldots,gx_n)',r'gB=\{gb:b\in B\}'],shape='Componentwise group action and set translate. The source switches from the input x^n to capital X^n in the displayed abbreviation; preserve that typography.')
add('D5','acts freely',r'''
Recall that $G$ acts freely on a set $\mathcal Z$ if anytime that $gz=z$ for some $g\in G$ and $z\in\mathcal Z$, then $g$ is the identity element of the group $G$.
''',[4],'Section 2.2 — free action',{'D4':'Freeness is a property of the group action.'},symbols=[r'gz=z'],shape='Trivial stabilizers. This is a separate condition from model invariance and is not inherited by Theorem 4 through Assumption 1 Part 3.')
add('D6','Group invariance',r'''
A probabilistic model $\mathcal P=\{\mathbf P_\theta:\theta\in\Theta\}$ on $\mathcal X$ is said to be invariant under the action of $G$ if the distribution $\mathbf P_\theta$ satisfies
\[
\mathbf P_\theta\{X\in B\}=\mathbf P_{g\theta}\{X\in gB\}\tag{3}
\]
for any $g\in G$, measurable $B\subseteq\mathcal X$, and $\theta\in\Theta$.
''',[4],'Section 2.2 — invariant probabilistic model (3)',{'D4':'The equality transports both the parameter and the observation set by the group action.'},context='Group invariance.',symbols=[r'\mathbf P_{g\theta}\{X\in gB\}'],shape='Equivariance of the family of distributions. The same original definition applies to each reparameterized group-indexed hypothesis.')
add('D7','maximally invariant',r'''
Furthermore, a function $m(x)$ is said to be invariant under the action of $G$ if $m(gx)=m(x)$ for all $x\in\mathcal X$ and $g\in G$; in other words, $m$ is constant on the orbits of $G$. Moreover, $m$ is said to be maximally invariant if it indexes the orbits of $\mathcal X$ under the action of $G$; that is, $m(x)=m(x')$ for $x,x'\in\mathcal X$ if and only if there exists a $g\in G$ such that $x=gx'$. A statistic is called (maximally) invariant if the corresponding function is.
''',[4],'Section 2.2 — invariant and maximally invariant statistics',{'D4':'The equivalence relation is given by group orbits.'},symbols=[r"m(x)=m(x')",r"x=gx'"],shape='The statistic identifies precisely the group orbits. Theorem 1 does not require its arbitrary statistic V_n to be invariant.')
add('D8','hypothesis testing problem',r'''
\[
\mathcal H_0:X^n\sim\mathbf P_g,\ g\in G,\quad\text{vs.}\quad\mathcal H_1:X^n\sim\mathbf Q_g,\ g\in G.\tag{4}
\]
To make notation more succinct, we use $\mathcal Q=\{\mathbf Q_g\}_{g\in G}$ to denote the alternative hypothesis and $\mathcal P=\{\mathbf P_g\}_{g\in G}$ for the null.
''',[4],'Section 2.2 — group-indexed testing problem (4)',{'D6':'These are the null and alternative group models with the invariance property (3).'},context='for the hypothesis testing problem (4).',context_pages=[10],symbols=[r'\mathcal H_0',r'\mathcal H_1'],shape='Fixed two group-indexed model families. The source obtains this representation from two parameter orbits; later theorems operate directly on the families, without adding the reparameterization proof as a condition.')
add('D9','amenability',r'''
A group $G$ is amenable if there exists a sequence of almost-right-invariant probability distributions, that is, a sequence $\boldsymbol\Pi_1,\boldsymbol\Pi_2,\ldots$ such that, for any measurable set $B\subseteq G$ and $g\in G$
\[
\lim_{k\to\infty}|\boldsymbol\Pi_k\{H\in B\}-\boldsymbol\Pi_k\{H\in Bg\}|=0.
\]
''',[5],'Section 2.2 — amenability by probability distributions',context='One of the crucial assumptions underlying their result is the amenability of',symbols=[r'\boldsymbol\Pi_k\{H\in Bg\}'],shape='Original sequence-based, pointwise-in-B-and-g formulation. The later compact-set characterization is retained as auxiliary context, not silently substituted here. H is a dummy random group element.')
add('D10','e-statistics',r'''
We now define e-statistics, our measure of evidence against the null hypothesis. The family of e-statistics comprises all nonnegative real statistics whose expected value is bounded by one under all elements of the null, that is, all statistics $T_n=t_n(X^n)$ such that $T_n\ge0$ and
\[
\sup_{g\in G}\mathbf E_g^{\mathbf P}[T_n]\le1.\tag{7}
\]
''',[6],'Section 2.3 — e-statistics (7)',{'D8':'The uniform expectation bound is under the null family P_g in (4).'},symbols=[r'T_n\ge0',r'\sup_{g\in G}\mathbf E_g^{\mathbf P}[T_n]\le1'],shape='Nonnegative real measurable statistic, with null expectation at most one uniformly over the nuisance group. It need not be invariant or a martingale.')
add('D11','GROW',r'''
Should it exist, an e-statistic $T_n^*$ is GROW if it maximizes the worst-case expected logarithmic value under the alternative hypothesis, that is, if it maximizes
\[
T_n\mapsto\inf_{g\in G}\mathbf E_g^{\mathbf Q}[\ln T_n]\tag{8}
\]
over all e-statistics.
''',[6,7],'Section 2.4 — GROW criterion (8)',{'D10':'The optimization ranges over all null-valid e-statistics.','D8':'The worst-case expectation ranges over the alternative family Q_g.'},symbols=[r'\inf_{g\in G}\mathbf E_g^{\mathbf Q}[\ln T_n]'],shape='Absolute worst-case logarithmic growth optimization. A maximum is not assumed to exist merely by naming the criterion.')
add('D12','relatively GROW',r'''
We say that an e-statistic $T_n^*$ is relatively GROW if it maximizes the gain in expected logarithmic value relative to an oracle that is given the particular distribution in the alternative hypothesis from which data are generated, that is, if $T_n^*$ maximizes, over all e-statistics,
\[
T_n\mapsto\inf_{g\in G}\left\{\mathbf E_g^{\mathbf Q}[\ln T_n]-\sup_{T_n'\text{ e-stat.}}\mathbf E_g^{\mathbf Q}[\ln T_n']\right\}.\tag{10}
\]
''',[7],'Section 2.4 — relative GROW criterion (10)',{'D10':'Both the outer candidate and oracle competitors are e-statistics for the same null.','D8':'The oracle is indexed by the alternative distribution Q_g.'},symbols=[],phrases=['relatively GROW'],shape='Alternative-specific oracle log-growth subtraction before taking the infimum over g. Theorem 4 proves equivalence to GROW under its stated conditions, not by definition.')
add('D13','Polish',r'''
As topological spaces, $G$ and $\mathcal X^n$ are Polish—separable, completely metrizable and locally compact.
''',[9],'Assumption 1 — Part 1',kind='assumption',symbols=[],phrases=['Polish','locally compact'],shape='The full printed topological requirement. Locally compact is retained as an extra property; the source dash does not change the usual meaning of Polish.')
add('D15','proper',r'''
In (1), an action is proper if the map $G\times\mathcal X^n\to\mathcal X^n\times\mathcal X^n$ defined by $(g,x^n)\mapsto(gx^n,x^n)$ is proper, that is, the inverse of any compact set is compact.
''',[4],'Section 2.2 — proper action',{'D4':'The defining map uses the action on the sample space.'},symbols=[r'(g,x^n)\mapsto(gx^n,x^n)'],shape='Properness of the action map through inverse images of compact sets; source spelling inverse means preimage here.')
add('D14','free, continuous and proper',r'''
The action of $G$ on $\mathcal X^n$ is free, continuous and proper.
''',[9],'Assumption 1 — Part 2',{'D4':'The condition applies to the componentwise sample-space action.','D5':'Free has the trivial-stabilizer definition in Section 2.2.','D15':'Proper has the compact-preimage definition in Section 2.2.'},kind='assumption',phrases=['free, continuous and proper'],shape='All three stated action properties, grouped as the original numbered assumption clause. Continuity is the usual topological continuity.')
add('D16','relatively left invariant',r'''
The models $\{\mathbf P_g\}_{g\in G}$ and $\{\mathbf Q_g\}_{g\in G}$ are invariant and have densities with respect to a common measure $\mu$ on $\mathcal X^n$ that is relatively left invariant with some multiplier $\chi$—$\mu\{gB\}=\chi(g)\mu\{B\}$ for any measurable set $B\subseteq\mathcal X^n$ and $g\in G$. All densities have a single common support.
''',[9],'Assumption 1 — Part 3',{'D8':'The two density families are the hypotheses in (4).','D6':'The assumption explicitly requires invariance of both models.','D4':'Relative invariance uses the left translate gB.'},kind='assumption',symbols=[r'\mu\{gB\}=\chi(g)\mu\{B\}'],phrases=['single common support'],shape='Invariant dominated models, relative left invariance of the common measure and one common support. Theorem 4 invokes only this part; other parts and amenability are not prerequisites of this clause.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
