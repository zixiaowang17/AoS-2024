"""Preserve graph laws, signed tree counts and randomized color-coding definitions."""
import json
from save_inventory import ROOT,PID,STATEMENTS
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
add(1,'correlated Erdős–Rényi graph model',r'''a popular statistical model for graph matching is the correlated Erdős–Rényi graph model, denoted by $\mathcal G(n,q,\rho)$, in which the observed graphs are two instances of the Erdős–Rényi graph $\mathcal G(n,q)$ whose edges are correlated through a hidden vertex correspondence. Specifically, let $\pi$ be a latent uniform random permutation on $[n]\triangleq\{1,\ldots,n\}$. Denote the observed graphs by $G_1$ and $G_2$ and their adjacency matrices by $A=(A_{ij})$ and $B=(B_{ij})$ respectively. Conditioned on the permutation $\pi$, the pairs of edges $\{(A_{ij},B_{\pi(i)\pi(j)}):1\le i<j\le n\}$ are i.i.d. pairs of Bernoulli random variables with parameter $q\in(0,1)$ and correlation coefficient $\rho$.''',[2],[],[r'\mathcal G(n,q,\rho)',r'(A_{ij},B_{\pi(i)\pi(j)})'],'Uniform latent permutation mixture of edge-correlated Bernoulli graphs. Independence is across aligned edge pairs conditional on pi, not between the two graphs under the mixture alternative. The graphs are simple, undirected and loop-free. Feasibility of negative rho is stated in the same-page footnote, preserved separately.','Section 1 — Correlated Erdős–Rényi graph model')
add(2,'hypothesis testing problem',r'''we formulate the problem of detecting network correlation as a hypothesis testing problem, where
- Under the null hypothesis $H_0$, $G_1$ and $G_2$ are independently generated from the Erdős–Rényi graph model $\mathcal G(n,q)$;
- Under the alternative hypothesis, $H_1$, $G_1$ and $G_2$ are generated from the correlated Erdős–Rényi graph model $\mathcal G(n,q,\rho)$.
Note that under both $H_0$ and $H_1$, the graphs $G_1$ and $G_2$ are marginally distributed as $\mathcal G(n,q)$.
where $\mathcal Q$ and $\mathcal P$ denote the joint distribution of $G_1$ and $G_2$ under $H_0$ and $H_1$, respectively.''',[3],[1],[r'\mathcal Q',r'\mathcal P',r'H_0',r'H_1'],'Null and alternative observation laws on the graph pair, with common Bernoulli edge marginals. The final sentence is excerpted after(1). Pi is latent rather than an observed argument of P. The randomized approximation uses independent coloring randomness in addition to these data laws; this extension is implicit in the source and recorded separately.','Section 1.1 — Null and alternative graph laws',kind='source_passage')
add(3,'isomorphism class',r'''For any graph $H$, let $V(H)$ denote the vertex set of $H$ and $E(H)$ denote the edge set of $H$. Two graphs $H$ and $H'$ are isomorphic, denoted by $H\cong H'$, if there exists a bijection $\pi:V(H)\to V(H')$ such that $(\pi(u),\pi(v))\in E(H')$ if and only if $(u,v)\in E(H)$. Denote by $[H]$ the isomorphism class of $H$; it is customary to refer to these isomorphic classes as unlabeled graphs. Let $\operatorname{aut}(H)$ be the number of automorphisms of $H$ (graph isomorphisms to itself). We say $H$ is a subgraph of $G$, denoted by $H\subset G$, if $V(H)\subset V(G)$ and $E(H)\subset E(G)$.''',[4,5],[],[r'[H]',r'\operatorname{aut}(H)',r'H\cong H\prime'],'Graph isomorphism classes and their automorphism counts, preserving the distinction between a labeled copy and an unlabeled tree. Subgraphs here are edge-induced with no isolated vertices by the page8 standing convention, not vertex-induced subgraphs. The printed subset symbol is not converted into proper-subgraph inclusion.','Section 1.3 — Graph isomorphism and automorphisms')
members['D3']['highlight_symbols']=[r'[H]',r'\operatorname{aut}(H)',r"H\cong H'"]
add(4,'centered version',r'''Specifically, denote by $A$ and $B$ the adjacency matrices of $G_1$ and $G_2$ respectively, and by $\overline A=A-\mathbb E[A]$ and $\overline B=B-\mathbb E[B]$ their centered version.''',[5],[2],[r'\overline A=A-\mathbb E[A]',r'\overline B=B-\mathbb E[B]'],'Entrywise edge centering by the common Bernoulli marginal q under either graph law. Counts are evaluated on these signed weighted matrices, not on uncentered graph counts minus their expectation. q is supplied; the source does not insert a plug-in edge-probability estimator.','Section 2.1 — Centered adjacency matrices')
add(5,'unlabeled trees',r'''Let $\mathcal T$ denote the set of unlabeled trees with $K$ edges.''',[5],[3],[r'\mathcal T',r'K'],'All non-isomorphic unrooted trees with exactly K edges, hence K+1 vertices. K diverges under(7); it is not the number of vertices or a selected subfamily. No rooted-tree counting constant is substituted.','Section 2.1 — Tree family')
add(6,'subgraph count',r'''for any weighted adjacency matrix $M$ on vertex set $[n]$, we define
\[
W_H(M)\triangleq\sum_{S\cong H}\prod_{(i,j)\in S}M_{ij},
\]
(5)
where the sum is over subgraphs of $K_n$ that are isomorphic to $H$. When $M$ is the unweighted adjacency matrix of a graph $G$, $W_H(M)$ reduces to the subgraph count $\operatorname{sub}(H,G)$. Thus $W_H(M)$ can be viewed as a natural generalization of the subgraph count to weighted graphs.''',[6],[3],[r'W_H(M)',r'\sum_{S\cong H}'],'Sum over distinct edge-set copies of H in the complete graph, multiplying one matrix entry per edge. It is not a sum over all labeled injections with their automorphism multiplicity and not an induced-subgraph count. Real weights may be negative.','Section 2.1 — Weighted subgraph count (5)')
add(7,'scaling factor',r'''Here
\[
\beta=\left(\frac{\rho}{q(1-q)}\right)^K\frac{(n-K-1)!}{n!}
\]
(4)
is a scaling factor introduced for ease of analysis,''',[6],[],[r'\beta',r'\frac{(n-K-1)!}{n!}'],'Normalization uses the correlation parameter, Bernoulli edge variance and K+1-vertex embedding factorial. Its sign follows rho^K; the theorem’s expected statistic and threshold use rho^(2K). Requires integer0≤K≤n−1, satisfied eventually by(7). These parameters retain their meanings under the standing graph experiment.','Section 2.1 — Scaling factor (4)')
add(8,'test statistic',r'''Define
\[
f_{\mathcal T}(A,B)\triangleq\sum_{[H]\in\mathcal T}f_H(A,B),\qquad\text{where }f_H(A,B)\triangleq\beta\operatorname{aut}(H)W_H(\overline A)W_H(\overline B).
\]
(3)''',[5],[3,4,5,6,7],[r'f_{\mathcal T}(A,B)',r'\beta\operatorname{aut}(H)W_H(\overline A)W_H(\overline B)'],'Exact signed-tree test statistic. Each tree class occurs once, with its automorphism weight and the product of weighted counts in the two centered adjacency matrices. This is distinct from covariance of raw unsigned counts, the likelihood-ratio projection used to analyze it and its randomized approximation.','Section 2.1 — Signed-tree test statistic (3)',context='and our test statistic is determined by the number of their copies in the observed graphs.')
add(9,"Otter's constant",r'''A celebrated result of Otter [Ott48] is that the number of unlabeled trees grows exponentially with
\[
\lim_{K\to\infty}|\mathcal T|^{1/K}=1/\alpha,
\]
(6)
where $\alpha\approx0.33833$ is Otter's constant.''',[6],[5],[r'\lim_{K\to\infty}|\mathcal T|^{1/K}=1/\alpha',r'\alpha'],'Reciprocal exponential growth constant for unrooted unlabeled trees by edge count. The rounded decimal is descriptive, not the exact threshold. The strict rho-squared comparison has no claim at equality and no uniformity near the boundary is stated.','Section 2.1 — Otter constant (6)')
add(10,'sufficient condition',r'''Suppose
\[
n\min\{q,1-q\}\ge n^{-o(1)},\qquad\rho^2>\alpha,\qquad\omega(1)\le K\le\frac{\log n}{16\log\log n\vee2\log\left(\frac1{n\min\{q,1-q\}}\right)},
\]
(7)
where $\alpha\approx0.33833$ is Otter's constant.''',[6],[9],[r'n\min\{q,1-q\}\ge n^{-o(1)}',r'\omega(1)\le K'],'Condition(7) is bound inside Theorem1 and explicitly referenced by Theorem2. Preserve minimum in edge sparsity, maximum in the denominator, diverging integer K and the strict correlation threshold. The max notation is defined on page5. No additional rate uniformity in rho is invented.','Theorem 1 — Condition (7)',kind='theorem_excerpt',context=r'we arrive at the following sufficient condition for the statistic $f_{\mathcal T}(A,B)$ to achieve consistent detection.')
add(11,'threshold',r'''where the threshold is chosen as
\[
\tau=C\mathbb E_{\mathcal P}[f_{\mathcal T}(A,B)]=C\rho^{2K}|\mathcal T|
\]
for any fixed constant $0<C<1$.''',[6],[2,5,8],[r'\tau=C\mathbb E_{\mathcal P}[f_{\mathcal T}(A,B)]',r'C\rho^{2K}|\mathcal T|'],'Threshold defined within Theorem1 and inherited by Theorem2’s reference to(8). C is any fixed constant strictly between0 and1; the expectation is that of the exact statistic under the alternative, not a data-estimated or null-quantile threshold.','Theorem 1 — Threshold in (8)',kind='theorem_excerpt')
add(12,'random coloring',r'''Specifically, given $M$ as a weighted adjacency matrix of a graph on $[n]$, we generate a random coloring $\mu:[n]\to[K+1]$ that assigns a color to each vertex of $M$ from the color set $[K+1]$ independently and uniformly at random. Given any $V\subset[n]$, let $\chi_\mu(V)$ indicate that $\mu(V)$ is colorful, i.e., $\mu(x)\ne\mu(y)$ for any distinct $x,y\in V$. In particular, if $|V|=K+1$, then $\chi_\mu(V)=1$ with probability
\[
r\triangleq\frac{(K+1)!}{(K+1)^{K+1}}.
\]
(29)''',[15],[],[r'\mu:[n]\to[K+1]',r'\chi_\mu(V)',r'\frac{(K+1)!}{(K+1)^{K+1}}'],'Independent uniform vertex coloring into K+1 colors, with colorful-set indicator and exact success probability. This is algorithmic randomness independent of the supplied weighted host graph; the source conditional expectation confirms that interpretation. K counts edges of a query tree.','Section 4 — Random coloring and colorful probability (29)')
add(13,'colorful subgraphs',r'''For any graph $H$ with $K+1$ vertices, we define
\[
X_H(M,\mu)\triangleq\sum_{S\cong H}\chi_\mu(V(S))\prod_{(i,j)\in E(S)}M_{ij}.
\]
(30)''',[15],[3,12],[r'X_H(M,\mu)',r'\chi_\mu(V(S))'],'Weighted count restricted to copies with all vertices differently colored. The source formula permits any query graph with K+1 vertices; tree structure is imposed by the family used in the test and by its efficient computation. Negative centered edge weights are retained.','Section 4 — Colorful weighted count (30)',context='counts the so-called colorful subgraphs (vertices having distinct colors) that are isomorphic to the query graph.')
add(14,'approximate test statistic',r'''To further obtain an accurate approximation of $W_H(M)$, we average over multiple copies of $X_H(M,\mu)$ by generating $t$ independent random colorings, where
\[
t\triangleq\lceil1/r\rceil.
\]
Next, we plug in the averaged subgraph count to approximately compute $f_{\mathcal T}(A,B)$. Specifically, we generate $2t$ random colorings $\{\mu_i\}_{i=1}^t$ and $\{\nu_j\}_{j=1}^t$ which are independent copies of $\mu$ that map $[n]$ to $[K+1]$. Then, we define
\[
Y_{\mathcal T}(A,B)\triangleq\sum_{[H]\in\mathcal T}\operatorname{aut}(H)\left(\frac1t\sum_{i=1}^tX_H(\overline A,\mu_i)\right)\left(\frac1t\sum_{j=1}^tX_H(\overline B,\nu_j)\right)
\]
(31)
and
\[
\widetilde f_{\mathcal T}(A,B)\triangleq\frac{\beta}{r^2}Y_{\mathcal T}(A,B).
\]
(32)''',[15],[3,4,5,7,12,13],[r'\widetilde f_{\mathcal T}(A,B)',r't\triangleq\lceil1/r\rceil',r'\frac{\beta}{r^2}'],'Product of two independent coloring averages, with the same coloring arrays reused across all tree classes; normalize by beta/r². It is not the average of paired same-color products and does not use only one family of colors for both graphs. W_H and f_T in the motivating prose are comparisons, not extra prerequisites of the explicit formula.','Section 4 — Color-coding approximation (31)–(32)',context=r'we conclude that the approximate test statistic $\widetilde f_{\mathcal T}$ succeeds under the same condition as the original test statistic $f_{\mathcal T}$',context_page=16)
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
