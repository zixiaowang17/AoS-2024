"""Preserve original main-text source entries for the seven-Theorem census."""
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
add(1,'Markov kernels',r'''Let $\mathfrak P(\mathcal Z)=\mathfrak P(\mathcal Z,\mathcal G)$ be the set of all probability measures on $(\mathcal Z,\mathcal G)$ and $\mathfrak P(\mathcal X\to\mathcal Z)$ be the set of all Markov kernels $Q:\mathcal G\times\mathcal X\to[0,1]$ from $(\mathcal X,\mathcal F)$ to $(\mathcal Z,\mathcal G)$. Note that we can always think of a Markov kernel $Q\in\mathfrak P(\mathcal X\to\mathcal Z)$ as a linear mapping from $\mathfrak P(\mathcal X)$ to $\mathfrak P(\mathcal Z)$ by defining $P\mapsto QP$ as $[QP](dz):=\int_{\mathcal X}Q(dz\mid x)P(dx)$. In the same sense we can also consider compositions $[QR](dz\mid x)=\int_{\mathcal Z'}Q(dz\mid z')R(dz'\mid x)$ of Markov kernels $R\in\mathfrak P(\mathcal X\to\mathcal Z')$ and $Q\in\mathfrak P(\mathcal Z'\to\mathcal Z)$. For $P\in\mathfrak P(\mathcal X)$, we easily see that $Q[RP]=[QR]P$ and thus it is allowed to just write $QRP$. For a statistical model $\mathcal P\subseteq\mathfrak P(\mathcal X)$ we also write $Q\mathcal P=\{QP:P\in\mathcal P\}$ for the model obtained by applying $Q$ to all original probability measures in $\mathcal P$. Notice that any measurable function $T:\mathcal X\to\mathcal Z$ can also be represented as a (degenerate) Markov kernel $R_T\in\mathfrak P(\mathcal X\to\mathcal Z)$ by defining $R_T(dz\mid x)$ to be the Dirac measure $\delta_{T(x)}$ at $T(x)$. Hence, we sometimes write $T\mathcal P:=R_T\mathcal P$ which is easily seen to coincide with the push-forward model $\{PT^{-1}:P\in\mathcal P\}$, since $[R_TP](A)=\int_{\mathcal X}\delta_{T(x)}(A)P(dx)=\int_{\mathcal X}\mathbf1_{T^{-1}(A)}(x)P(dx)=PT^{-1}(A)$. Similarly, we can also make sense of the composition of a Markov kernel $Q\in\mathfrak P(\mathcal Z'\to\mathcal Z)$ and the measurable function $T:\mathcal X\to\mathcal Z'$, by setting $[QT](dz\mid x):=[QR_T](dz\mid x)=Q(dz\mid T(x))$.''',[4],[],[r'[QP](dz)',r'Q\mathcal P',r'[QT](dz\mid x)'],'Kernel action on probability measures, kernel composition and deterministic push-forward convention. Blackletter P denotes probability laws/kernels; calligraphic P denotes a statistical model.','Section 1.2 — Markov kernels and their action')
add(2,'privacy mechanism',r'''First, we define the set of marginal $\alpha$-differentially private channels by
\[
\mathcal Q_\alpha(\mathcal X\to\mathcal Z):=\{Q\in\mathfrak P(\mathcal X\to\mathcal Z):Q(A\mid x)\le e^\alpha Q(A\mid x'),\ \forall A\in\mathcal G,\forall x,x'\in\mathcal X\}.
\]
(1.4)
When searching for an optimal privacy mechanism, we want to impose no a priori restrictions on the space $(\mathcal Z,\mathcal G)$ from which the sanitized observations are drawn. Thus, we also consider the union over all possible measurable output spaces
\[
\mathcal Q_\alpha:=\mathcal Q_\alpha(\mathcal X):=\bigcup_{(\mathcal Z,\mathcal G)}\mathcal Q_\alpha(\mathcal X\to\mathcal Z).
\]
(1.5)''',[4,5],[1],[r'\mathcal Q_\alpha(\mathcal X\to\mathcal Z)',r'\mathcal Q_\alpha(\mathcal X)'],'Marginal local privacy for every input pair and every measurable output event. The unrestricted-output union is a class; the author specifies the real-valued supremum interpretation in footnote 1, retained in A2.','Section 1.2.1 — Marginal privacy (1.4)–(1.5)')
# Use the source term with its mathematical qualifier kept in the original passage.
add(3,'sequentially interactive',r'''A Markov kernel $Q^{(n)}\in\mathfrak P(\mathcal X^n\to\mathcal Z^{(n)})$ is said to be sequentially interactive if the following condition is satisfied: For every $i=1,\ldots,n$, there exists a Markov kernel $Q_i\in\mathfrak P(\mathcal X\times\mathcal Z^{(i-1)}\to\mathcal Z_i)$, such that for all $x_1,\ldots,x_n\in\mathcal X$,
\[
Q^{(n)}(dz_{1:n}\mid x_1,\ldots,x_n)=Q_{z_{1:n-1}}(dz_n\mid x_n)Q_{z_{1:n-2}}(dz_{n-1}\mid x_{n-1})\cdots Q_\varnothing(dz_1\mid x_1),
\]
(1.6)
where $Q_{z_{1:i-1}}(dz_i\mid x_i):=Q_i(dz_i\mid x_i,z_{1:i-1})$, $z_{1:0}=\varnothing$ and $z_{1:i}=(z_1,\ldots,z_i)^T\in\mathcal Z^{(i)}$. Here, the idea is that individual $i$ can only use $X_i$ and previous $Z_j$, $j<i$, in its local privacy mechanism, thus leading to the sequential structure in the above definition. If, in addition, for all $i\in[n]$ and for all $z_{1:i-1}\in\mathcal Z^{(i-1)}$ we have $Q_{z_{1:i-1}}\in\mathcal Q_\alpha(\mathcal X\to\mathcal Z_i)$, then, by the usual approximation of integrands by simple functions, it is easy to see that $Q$ in (1.6) is $\alpha$-differentially private (i.e., satisfies (1.3)), in which case we call it $\alpha$-sequentially interactive.''',[5],[1,2],[r'Q_{z_{1:i-1}}',r'Q^{(n)}'],'History-dependent marginal channels use only the current raw input and preceding sanitized outputs. Local privacy is imposed at every history, not only almost surely. Empty-product notation is retained in A1.','Section 1.2.1 — Sequentially interactive mechanism (1.6)')
add(4,'non-interactive mechanisms',r'''An important subclass of sequentially interactive mechanisms are the so called non-interactive mechanisms $Q\in\mathfrak P(\mathcal X^n\to\mathcal Z^{(n)})$ that are of product form
\[
Q(dz_{1:n}\mid x_1,\ldots,x_n)=\bigotimes_{i=1}^nQ_i(dz_i\mid x_i),\qquad\forall x_1,\ldots,x_n\in\mathcal X,
\]
(1.7)
for some marginal kernels $Q_i\in\mathfrak P(\mathcal X\to\mathcal Z_i)$. Clearly, a non-interactive mechanism $Q$ satisfies (1.3) if, and only if, for all $i=1,\ldots,n$, $Q_i\in\mathcal Q_\alpha$. In that case it is also called $\alpha$-non-interactive.''',[5],[1,2],[r'\bigotimes_{i=1}^nQ_i',r'\mathcal Q_\alpha'],'Product privacy mechanism, allowing different marginal kernels for different individuals. Fixed-Q MLEs specialize this definition to a common channel. The subclass comparison does not require another sequential construction to define the product.','Section 1.2.1 — Non-interactive mechanism (1.7)')
add(5,'Differentiability in Quadratic Mean',r'''A model $\mathcal P=(P_\theta)_{\theta\in\Theta}$ with $\Theta\subseteq\mathbb R^p$, sample space $(\mathcal X,\mathcal F)$ and ($\sigma$-finite) dominating measure $\mu$ is called differentiable in quadratic mean (DQM) at the point $\theta\in\Theta$, if $\theta$ is an interior point of $\Theta$ and the $\mu$-densities $p_\theta=\frac{dP_\theta}{d\mu}$ satisfy
\[
\Psi_\theta(h):=\int_{\mathcal X}\left(\sqrt{p_{\theta+h}(x)}-\sqrt{p_\theta(x)}-\frac12h^Ts_\theta(x)\sqrt{p_\theta(x)}\right)^2\mu(dx)=o(\|h\|^2)
\]
as $h\to0$, for some measurable vector valued function $s_\theta:\mathcal X\to\mathbb R^p$. The function $s_\theta$ is called the score at $\theta$.''',[9],[],[r'\Psi_\theta(h)',r's_\theta',r'o(\|h\|^2)'],'DQM at a specified interior parameter under a sigma-finite dominating measure. The all-parameter convention is retained in A3 and explicitly in C1. No nonsingularity assumption is part of this definition.','Definition 1 (Differentiability in Quadratic Mean)',context='DEFINITION 1 (Differentiability in Quadratic Mean).')
add(6,'Fisher information matrix',r'''We also recall that if the model $\mathcal P$ is DQM at $\theta$, then the score satisfies $\mathbb E_\theta[s_\theta]=0$ and the Fisher information matrix $I_\theta(\mathcal P):=\mathbb E_\theta[s_\theta s_\theta^T]\in\mathbb R^{p\times p}$ exists and is finite (see van der Vaart, 2007, Theorem 7.2).''',[9],[5],[r'I_\theta(\mathcal P)',r'\mathbb E_\theta[s_\theta s_\theta^T]'],'Score second-moment information for a DQM model, including singular matrices. Applied to a private model through the kernel-action convention; it is scalar only in the explicitly scalar theorems.','Section 3.1 — Fisher information',kind='source_passage')
add(7,'Local Asymptotic Mixed Normality',r'''Fix a parameter space $\Theta\subseteq\mathbb R^p$ and a sequence $(\delta_n)_{n\in\mathbb N}$ of positive definite $p\times p$ matrices with $\|\delta_n\|\to0$ as $n\to\infty$. We say the sequence of statistical experiments $\mathcal E_n=(\Omega_n,\mathcal A_n,\{R_{n,\theta}:\theta\in\Theta\})$ satisfies the LAMN condition at $\theta\in\Theta$, if $\theta$ is an interior point of $\Theta$ and the following two conditions hold:
1. There exists a sequence $(\Delta_{n,\theta})_{n\in\mathbb N}$ of random vectors $\Delta_{n,\theta}:\Omega_n\to\mathbb R^p$ and a sequence $(\Sigma_{n,\theta})_{n\in\mathbb N}$ of random nonnegative-definite matrices $\Sigma_{n,\theta}:\Omega_n\to\mathbb R^{p\times p}$, such that
\[
\Lambda_n(\theta+\delta_nh,\theta)-\left(h^T\Delta_{n,\theta}-\frac12h^T\Sigma_{n,\theta}h\right)
\]
converges to zero in $R_{n,\theta}$ probability for every $h\in\mathbb R^p$.
2. We have
\[
\begin{pmatrix}\Delta_{n,\theta}\\\Sigma_{n,\theta}\end{pmatrix}\overset{R_{n,\theta}}{\rightsquigarrow}\begin{pmatrix}\Sigma_\theta^{1/2}\Delta\\\Sigma_\theta\end{pmatrix},
\]
where $\Delta\sim\mathcal N(0,J_p)$ is independent of $\Sigma_\theta$.''',[10],[],[r'\Sigma_\theta^{1/2}\Delta',r'\Lambda_n(\theta+\delta_nh,\theta)','LAMN'],'Mixed-normal local likelihood expansion with joint weak convergence and independent standard Gaussian factor. Nonnegative-definite information may be singular. Log-likelihood ratio uses the absolutely continuous part, retained in A4.','Definition 2 (Local Asymptotic Mixed Normality)',context='DEFINITION 2 (Local Asymptotic Mixed Normality).')
add(8,'Maximum Likelihood',r'''Fix a (marginal) channel $Q\in\mathcal Q_\alpha(\mathcal X)$, pick $\nu(dz):=Q(dz\mid x^*)$ and $q(z\mid x)$ as in Lemma D.2 and write $q_\theta(z)=\int_{\mathcal X}q(z\mid x)p_\theta(x)\mu(dx)$ for $\nu$-densities of the model $Q\mathcal P$. In particular, we have $q_\theta(z)\in[e^{-\alpha},e^\alpha]$. The log-likelihood of the observed (non-interactively) sanitized data $Z_1,\ldots,Z_n$ is given by
\[
\theta\mapsto\ell_n(\theta):=\ell_n(\theta;z_1,\ldots,z_n):=\sum_{i=1}^n\log q_\theta(z_i),
\]
and we define the corresponding non-interactive $\alpha$-private MLE $\widehat\theta_n$ to be a measurable maximizer.''',[14],[1,2,4],[r'q_\theta(z)',r'\ell_n(\theta)',r'\widehat\theta_n'],'Fixed-channel private maximum likelihood estimator in a dominated model. Its density construction refers to an appendix lemma; preserve the main-text formula and reference without reading the appendix or claiming existence of a maximizer.','Section 4.1.1 — Non-interactive private MLE',context='4.1.1. Maximum Likelihood.')
add(9,'truncation operation',r'''We can turn this into a non-interactive $\alpha$-private procedure by considering the truncation operation $\Pi_\tau(y):=y\mathbf1_{\{\|y\|_1\le\tau\}}$, $y\in\mathbb R^p$.''',[15],[],[r'\Pi_\tau(y)',r'y\mathbf1_{\{\|y\|_1\le\tau\}}'],'Hard truncation to zero outside an l1 ball. This is not clipping to its boundary. g, its expectation map, inverse and Laplace noise are locally bound by Theorem 4.3.','Section 4.1.2 — Truncation operation')
add(10,'DQM',r'''The model $(\mathcal X,\mathcal F,\mathcal P)$ is DQM at every $\theta\in\Theta\subseteq\mathbb R^p$ with score $s_\theta$ and dominating measure $\mu$.''',[16],[5],[r's_\theta'], 'All-parameter DQM with common dominating measure, preserving the separately labeled C1 assumption. No positive information condition is added.','Condition (C1)',kind='assumption',phrases=['Condition (C1)'])
add(11,'measurability condition',r'''The mappings $(x,\theta)\mapsto p_\theta(x):\mathcal X\times\Theta\to\mathbb R_+$ and $(x,\theta)\mapsto s_\theta(x):\mathcal X\times\Theta\to\mathbb R^p$ are measurable.''',[16],[5],[r'(x,\theta)\mapsto p_\theta(x)',r'(x,\theta)\mapsto s_\theta(x)'],'Joint measurability of density and score versions in data and parameter. Distinct from pointwise-in-parameter DQM and continuity into a function space.','Condition (C2)',kind='assumption',context='The measurability condition (C2) will be used to construct a measurable discretization of the original model and to show that the Fisher-Information of the discretized model and a maximizer thereof are appropriately measurable.',phrases=['Condition (C2)'])
add(12,'regularity',r'''The mapping $\theta\mapsto s_\theta\sqrt{p_\theta}:\Theta\to L^2(\mu,\|\cdot\|_2)$ is continuous.''',[16],[5],[r'\theta\mapsto s_\theta\sqrt{p_\theta}'],'Continuity of the score times square-root density in L2. Keep C3 separately; the adjacent comparison with a stronger notion of regularity does not add positive-definite information to C3.','Condition (C3)',kind='assumption',context=r'Conditions (C1) and (C3) together with positive definiteness of $I_\theta(\mathcal P)$ for all $\theta\in\Theta$, correspond exactly to what Bickel et al. (1993) call regularity of the parametric model $\mathcal P$.',phrases=['Condition (C3)'])
add(13,'consistent quantizer',r'''Suppose Condition (C1) holds and let $\dot p_\theta(x):=s_\theta(x)p_\theta(x)\in\mathbb R^p$. A sequence of measurable mappings $(x,\theta)\mapsto T_m(x,\theta):\mathcal X\times\Theta\to\mathbb N$, $m\in\mathbb N$, is called a consistent quantizer of the model $\mathcal P$, if there exists another sequence of measurable mappings $k_m:\Theta\to\mathbb N$, such that the following hold true:
a) For all $m\in\mathbb N$, $\theta\in\Theta$ and $x\in\mathcal X$ we have $T_m(x,\theta)\in[k_m(\theta)]:=\{1,\ldots,k_m(\theta)\}$.
b) Define the following quantities: $T_{m,\theta}(x):=T_m(x,\theta)$, $B_j:=B_{j,m}(\theta):=T_{m,\theta}^{-1}(\{j\})$, $J:=J_m(\theta):=\{l\in[k_m(\theta)]:0<\mu(B_{l,m}(\theta))<\infty\}$, $K:=K_{J,m}(\theta):=\bigcup_{j\in J}B_{j,m}(\theta)$,
\[
\bar p_\theta(x):=\sum_{j\in J}\frac{\int_{B_j}p_\theta(y)\mu(dy)}{\mu(B_j)}\mathbf1_{B_j}(x),\quad\text{and}\quad\overline{\dot p}_\theta(x):=\sum_{j\in J}\frac{\int_{B_j}\dot p_\theta(y)\mu(dy)}{\mu(B_j)}\mathbf1_{B_j}(x)\in\mathbb R^p.
\]
We then have $\Delta_m(\theta_m)\to0$ as $m\to\infty$, for every sequence $(\theta_m)_{m\in\mathbb N}$ in $\Theta$ whose limit is also in $\Theta$, and where
\[
\Delta_m(\theta):=\left[\left\|(p_\theta-\bar p_\theta)\mathbf1_{K(\theta)}\right\|_{L^1(\mu)}+\left\|\|\dot p_\theta-\overline{\dot p}_\theta\|_{\ell_2}\mathbf1_{K(\theta)}\right\|_{L^1(\mu)}+\sqrt{P_\theta(K(\theta)^c)}\right].
\]
(4.4)''',[17,18],[10],[r'T_m(x,\theta)',r'\Delta_m(\theta)',r'0<\mu(B_{l,m}(\theta))<\infty'],'Parameter-dependent finite quantization with density and score-density histogram approximation along every convergent parameter sequence. Finite positive cell masses and square-root tail term are essential.','Definition 3 — Consistent quantizer')
add(14,'column stochastic matrices',r'''Define the set $\mathcal M_\alpha(\ell,k)$ consisting of all $\ell\times k$ column stochastic matrices $Q$ (i.e., $Q_{ij}\ge0$ and $\sum_{i=1}^{\ell}Q_{ij}=1$) with the following property: Two elements $Q_{ij}$ and $Q_{ij'}$ of any given row $i$ of $Q$ satisfy $e^{-\alpha}Q_{ij'}\le Q_{ij}\le e^\alpha Q_{ij'}$.''',[18],[],[r'\mathcal M_\alpha(\ell,k)',r'\sum_{i=1}^{\ell}Q_{ij}=1'],'Finite channel matrix domain, with output rows and input columns. Column sums equal one; privacy comparisons run across a fixed row. These are the privacy-constrained matrices, not all stochastic matrices.','Lemma 4.5 — Matrix domain',kind='definition')
add(15,'two-step estimation procedure',r'''We begin by describing the complete locally private two-step estimation procedure: Given are private data $X_1,\ldots,X_n\overset{\mathrm{iid}}{\sim}P_\theta$, $\theta\in\Theta\subseteq\mathbb R$, from a regular statistical model $\mathcal P=\{P_\theta:\theta\in\Theta\}$ on sample space $\mathcal X\subseteq\mathbb R^d$ dominated by $\mu$.
1. Fix a preliminary privacy mechanism $Q_0\in\mathcal Q_\alpha(\mathcal X)$, such that $Q_0\mathcal P$ is identifiable.
2. Consider a non-interactive $\alpha$-private preliminary estimator $\widetilde\theta_{n_1}$ based on sanitized versions $Z_1,\ldots,Z_{n_1}$ of $X_1,\ldots,X_{n_1}$ generated from $Q_0$, which is consistent for $\theta$ (cf. Subsection 4.1), that is, which satisfies
\[
[Q_0P_\theta]^{n_1}(|\widetilde\theta_{n_1}-\theta|>\varepsilon)\xrightarrow[n_1\to\infty]{}0,\qquad\forall\varepsilon>0,\forall\theta\in\Theta.
\]
3. Fix a consistent quantizer $(T_m)_{m\in\mathbb N}$ as in Definition 3 with associated sequence $(k_m)_{m\in\mathbb N}$ and set $\widehat T_{n_1}(x):=T_{n_1}(x,\widetilde\theta_{n_1})$ and $\widehat k_{n_1}:=k_{n_1}(\widetilde\theta_{n_1})$.
4. Let $\widehat Q_{n_1}$ be a measurable maximizer
\[
\widehat Q_{n_1}\in\operatorname*{arg\,max}_{Q\in\mathcal M_\alpha(\widehat k_{n_1},\widehat k_{n_1})}I_{\widetilde\theta_{n_1}}(Q\widehat T_{n_1}\mathcal P)
\]
(4.8)
(cf. Lemma 4.6 with $\theta=\widetilde\theta_{n_1}$ and Lemma 4.5).
5. Generate $Z_{n_1+1},\ldots,Z_n$ non-interactively from $X_{n_1+1},\ldots,X_n$ using the mechanism $\widehat Q_{n_1}\widehat T_{n_1}$. More precisely, individual $i\in\{n_1+1,\ldots,n\}$ computes $Y_i=\widehat T_{n_1}(X_i)$ and generates $Z_i\in\{1,\ldots,\widehat k_{n_1}\}$ from $\widehat Q_{n_1}(dz\mid Y_i)$ (equivalently, from the discrete distribution given by the vector $[\widehat Q_{n_1}]_{\cdot,Y_i}\in\mathbb R^{\widehat k_{n_1}}$).
6. Let $\widehat\theta_{n_2}$ be an MLE in the model $[\widehat Q_{n_1}\widehat T_{n_1}\mathcal P]^{n_2}$, that is, a measurable maximizer (where it exists, and defined arbitrarily otherwise) of the conditional log-likelihood
\[
\theta\mapsto\ell_{n_2}(\theta):=\ell_{n_2}(\theta;z_{n_1+1},\ldots,z_n\mid\widetilde\theta_{n_1}):=\frac1{n_2}\sum_{i=n_1+1}^n\log\widehat q_\theta(z_i),\qquad z_i\in\{1,\ldots,\widehat k_{n_1}\},
\]
over $\Theta$, where $n_2=n-n_1$,
\[
\widehat q(z\mid x):=[\widehat Q_{n_1}]_{z,\widehat T_{n_1}(x)}=\sum_{j=1}^{\widehat k_{n_1}}[\widehat Q_{n_1}]_{z,j}\cdot\mathbf1_{\widehat T_{n_1}^{-1}(\{j\})}(x)
\]
and
\[
\widehat q_\theta(z):=\int_{\mathcal X}\widehat q(z\mid x)p_\theta(x)\mu(dx)=\sum_{j=1}^{\widehat k_{n_1}}[\widehat Q_{n_1}]_{z,j}\cdot P_\theta(\widehat T_{n_1}^{-1}(\{j\})).
\]''',[21,22],[1,2,4,5,6,13,14],[r'\widehat\theta_{n_2}',r'\widehat q_\theta(z)',r'\widetilde\theta_{n_1}',r'\widehat Q_{n_1}'],'Complete six-step scalar procedure including an identifiable preliminary channel, a consistent preliminary estimator, adaptive quantization and maximization, second-group conditional likelihood and arbitrary fallback. Final consistency is a separate hypothesis of Theorem 4.12.','Section 4.3 — Two-step estimation procedure')
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D7']['highlight_symbols'] = ['\\Sigma_\\theta^{1/2}\\Delta', '\\Lambda_n(\\theta+\\delta_nh,\\theta)']
members['D7']['highlight_phrases'] = ['LAMN']

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
