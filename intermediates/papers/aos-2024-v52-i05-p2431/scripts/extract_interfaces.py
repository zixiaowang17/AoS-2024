"""Preserve the original multi-layer graph model definitions without changing source definitions."""
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
add(1,'multi-layer SBM',r'''A multi-layer SBM with $K$ common communities generates independent Bernoulli random variables
\[
A_t(i,j)\overset{\mathrm{indep.}}\sim\operatorname{Bernoulli}(B_t(\sigma_i,\sigma_j)),\qquad1\le i<j\le n,\quad1\le t\le T,
\]
(1)
where $\sigma=(\sigma(i):i\in[n])\in[K]^n$ is a community membership vector, with $\sigma(i)\in[K]$ denoting the membership of node $i$, and $B_t\in[0,1]^{K\times K}$ is a symmetric matrix specifying the edge probability between the communities in the $t$th layer.
The observed data are $T$ symmetric binary adjacency matrices $A=(A_t:t\in[T])$.''',[3,4],[],[r'A_t(i,j)',r'B_t(\sigma_i,\sigma_j)'],'Conditional independent undirected loop-free edge observations for fixed community memberships and layer probability matrices. The special mixture in Definition1 randomizes those latent parameters, so its marginal edges are not independent.','Section 2 — Multi-layer stochastic block model (1)')
add(2,'balanced membership vectors',r'''we focus on the case $K=2$ and assume both $n$ and $T$ are even. Let $\mathcal S_n=\{\sigma\in\{0,1\}^n:\sum_{i\in[n]}\sigma(i)=n/2\}$ be the set of all balanced membership vectors $\sigma$ on $n$ nodes.''',[4],[],[r'\mathcal S_n',r'\sum_{i\in[n]}\sigma(i)=n/2'],'Exactly balanced binary assignments, with even n and T. The source uses the analogous S_T for exactly balanced layer identities. Do not replace these uniform balanced priors by independent Bernoulli labels.','Section 2 — Balanced binary memberships')
add(3,'network density',r'''Let $\rho\in(0,2/3)$ be a overall network density parameter. Define
\[
B^{(0)}=\begin{bmatrix}\frac32\rho&\frac12\rho\\\frac12\rho&\frac32\rho\end{bmatrix},\qquad B^{(1)}=\begin{bmatrix}\frac12\rho&\frac32\rho\\\frac32\rho&\frac12\rho\end{bmatrix}.
\]
(2)''',[4],[],[r'B^{(0)}',r'B^{(1)}',r'\rho\in(0,2/3)'],'Fixed assortative and disassortative two-block matrices with edge probabilities rho/2 and3rho/2. The strict density range puts every probability inside (0,1). These are the specific alternatives used in the theorems, not arbitrary layer matrices.','Section 2 — Layer probability matrices (2)')
add(4,'balanced two-community model',r'''The balanced two-community model $P_{1,n}=P_1(n,T,\rho)$:
(a) $\sigma\sim\operatorname{Uniform}(\mathcal S_n)$;
(b) $\tau\sim\operatorname{Uniform}(\mathcal S_T)$;
(c) $B_t=B^{(\tau_t)}$ for each $t\in[T]$, with $B^{(0)},B^{(1)}$ given in (2);
(d) Generate $A$ according to (1).
In the rest of this paper, we will use $P_{1,n}$ to denote the joint distribution of $(A,\sigma,\tau)$.''',[4,5],[1,2,3],[r'P_{1,n}',r'\sigma\sim\operatorname{Uniform}(\mathcal S_n)',r'\tau\sim\operatorname{Uniform}(\mathcal S_T)'],'Balanced latent-node and latent-layer mixture with both layer types. The source subsequently uses P1,n for the full joint law and for the observation marginal in testing/divergence formulas; this overloading is recorded explicitly. Separate prior draws are naturally read as independent, though that word is not printed in the list.','Definition 1(1) — Balanced two-community model')
add(5,'null model',r'''The null model $P_{0,n}=P_0(n,T,\rho)$:
\[
A_t(i,j)\overset{\mathrm{indep.}}\sim\operatorname{Bernoulli}(\rho)
\]
for all $1\le i<j\le n$, $t\in[T]$.''',[4],[],[r'P_{0,n}',r'\operatorname{Bernoulli}(\rho)'],'Independent Bernoulli-rho edge observations under the null, without community or layer labels. Its sample space for testing is the observed graph tensor; latent labels are not observed in either testing hypothesis.','Definition 1(2) — Null model')
add(6,'normalized Hamming distance',r'''\[
\ell_n(\widehat\sigma,\sigma)=n^{-1}\min\{d_{\mathrm{Ham}}(\widehat\sigma,\sigma),d_{\mathrm{Ham}}(\widehat\sigma,1-\sigma)\}
\]
is the normalized Hamming distance between $\widehat\sigma$ and $\sigma$ up to label permutation.''',[5],[],[r'\ell_n(\widehat\sigma,\sigma)',r'1-\sigma'],'Fraction of mislabeled nodes minimized over the global binary label swap. Recovery means this loss tends to zero in probability, not exact equality of all labels or merely nontrivial overlap.','Definition 2(1) — Hamming loss up to permutation')
add(7,'recoverable',r'''For a sequence $(T_n,\rho_n)_{n=1}^\infty$, we say the corresponding MLSBM sequence $P_{1,n}$ defined in Definition 1 is recoverable if there exists a sequence of estimators $\widehat\sigma(A)\in\mathcal S_n$ such that
\[
P_{1,n}(\ell_n(\widehat\sigma,\sigma)\ge\epsilon)\to0
\]
for any positive constant $\epsilon$,''',[5],[2,4,6],[r'\widehat\sigma(A)\in\mathcal S_n',r'P_{1,n}(\ell_n'],'Existence of estimators based only on A, taking balanced labels and achieving vanishing permutation-invariant Hamming fraction under the latent joint mixture law. This is not a uniform-over-all-fixed-label minimax statement. Computational restriction is separate.','Definition 2(1) — Recoverable model sequence')
add(8,'distinguishable',r'''For a sequence $(T_n,\rho_n)_{n=1}^\infty$, we say the corresponding MLSBM sequence $(P_{1,n})$ defined in Definition 1 is distinguishable from $P_{0,n}$ if there exists a sequence of $\widehat\psi:\widehat\psi(A)\in\{0,1\}$ such that
\[
P_{1,n}(\widehat\psi(A)=0)+P_{0,n}(\widehat\psi(A)=1)\to0.
\]''',[5],[4,5],[r'\widehat\psi(A)',r'P_{1,n}(\widehat\psi(A)=0)+P_{0,n}(\widehat\psi(A)=1)'],'Strong detection by an A-measurable binary test with vanishing sum of type-I and type-II error probabilities. Negation means no such sequence, not necessarily total variation tending to zero or impossibility of weak detection.','Definition 2(2) — Distinguishable model sequence')
add(9,'Asymptotic regime',r'''When $n\to\infty$, we have $T_n\to\infty$, $\rho_n\to0$, $\rho_n^{-1}=o(n^2)$.''',[6],[],[r'T_n\to\infty',r'\rho_n^{-1}=o(n^2)'],'Diverging layers and vanishing density, but expected edges per layer do not vanish through a density smaller than n^−2. The source labels this Assumption1; do not replace rho_n^−1=o(n²) by a bound on n*T_n*rho_n.','Assumption 1 (Asymptotic regime of (T_n, rho_n))',kind='assumption',context='Assumption 1 (Asymptotic regime of $(T_n,\rho_n)$)',context_page=6)
add(10,'Low-degree polynomial conjecture',r'''Let $P_{0,n}$ and $P_{1,n}$ be two sequences of MLSBM defined in Definition 1 with parameters $(T_n,\rho_n)$ satisfying the asymptotic regime specified in Assumption 1. If every polynomial $\psi$ of degree at most $D_n=\log^{1.01}(n)$ with $E_{P_{0,n}}\psi^2=1$ and $E_{P_{0,n}}\psi=0$ satisfies $E_{P_{1,n}}\psi=O(1)$ uniformly, then $P_{1,n}$ is not distinguishable from $P_{0,n}$ by any polynomial-time algorithm.
Here the polynomial is viewed as a multivariate polynomial with input vector $A\in\mathbb R^{\binom n2\times T_n}$.''',[7],[4,5,8,9,14],[r'D_n=\log^{1.01}(n)',r'E_{P_{0,n}}\psi^2=1',r'E_{P_{0,n}}\psi=0'],'Full conjectured implication, including uniformity over normalized centered low-degree polynomials and the data input. It is an assumed conjecture in the computational lower bounds, not a proven theorem or an unconditional complexity lower bound.','Conjecture 3.2 (Low-degree polynomial conjecture: Conjecture 2.2.4 in [20])',kind='source_passage',context='Conjecture 3.2 (Low-degree polynomial conjecture: Conjecture 2.2.4 in [20])',context_page=7)
add(11,'conditional distribution',r'''For $\tau\in\mathcal S_{T_n}$, let $P_{1,\tau,n}$ be the corresponding conditional distribution of $(A,\sigma)$ under $P_{1,n}$ given $\tau$. For $\tau\in\mathcal S_{T_n}$, $\sigma\in\mathcal S_n$, $P_{\sigma,\tau}$ denotes the distribution of $A$ given $(\sigma,\tau)$.''',[10],[2,4],[r'P_{1,\tau,n}',r'P_{\sigma,\tau}'],'Known-layer-identity conditional mixture and fixed-label graph law. Theorem4.1 explicitly sums P1,tau,n(A), hence uses its A marginal even though the preceding definition names the joint law of (A,sigma). Keep this distinction rather than comparing different sample spaces.','Section 4.1 — Conditional alternative laws')
add(12,'divergence',r'''Recall that for two distributions $P,Q$ on the same sample space $\mathcal X$ with probability mass function $q(x)$ and $p(x)$ respectively, their $\chi^2$-divergence is
\[
d_{\chi^2}(Q,P)=E_{X\sim P}\left(\frac{q(X)}{p(X)}-1\right)^2=\sum_{x\in\mathcal X}\frac{q^2(x)}{p(x)}-1.
\]''',[10],[],[r'd_{\chi^2}(Q,P)',r'\frac{q^2(x)}{p(x)}'],'Directed chi-square divergence with null/reference mass in the denominator. The prose reverses the p/q assignment relative to the standard formula; preserve both and flag it. For these graph models P0 has full support, so the A-marginal ratios exist.','Section 4.1 — Chi-square divergence')
add(13,'maximum likelihood estimate',r'''We consider a variant of the maximum likelihood estimate (MLE) specialized to the MLSBM in Definition 1. Given data $A\in\{0,1\}^{\binom n2\times T_n}$, we estimate $\sigma$ and $\tau$ together by maximizing the blockwise edge count:
\[
(\widehat\sigma_{\mathrm{mle}},\widehat\tau_{\mathrm{mle}})=\operatorname{arg}\max_{\sigma\in\mathcal S_n,\tau\in\mathcal S_{T_n}}\sum_{(i,j,t):2\mid\sigma(i)+\sigma(j)+\tau(t)}A_t(i,j).
\]
(4)''',[11],[2],[r'\widehat\sigma_{\mathrm{mle}}',r'2\mid\sigma(i)+\sigma(j)+\tau(t)'],'Joint balanced-label maximization of observed edge counts for even-parity triples, where 1≤i<j≤n and1≤t≤T_n are the ambient observation indices. Only the sigma component is asserted to have vanishing Hamming loss. No efficient algorithm or tie-breaking convention is specified.','Section 4.2 — Joint maximum-likelihood variant (4)')
add(14,'polynomial-time',r'''Here the notion of “polynomial-time” means polynomial in $n$,''',[8],[],[], 'Runtime convention stated in the lower-bound discussion, measured in the node count. For fixed monomial layer growth the input size is polynomial in n; under the actual negative-logarithm lower-bound condition it is also polynomial. The following explanatory sentence prints a different log sign and is retained separately as a source issue.','Section 3 — Polynomial-time convention',phrases=['polynomial-time'])
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D13']['highlight_symbols'] = ['\\widehat\\sigma_{\\mathrm{mle}}', '\\sum_{(i,j,t):2\\mid\\sigma(i)+\\sigma(j)+\\tau(t)}']

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
