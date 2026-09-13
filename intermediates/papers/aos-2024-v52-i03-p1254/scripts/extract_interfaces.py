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


add('D1','empirical spectral distribution',r'''
Suppose $\mathbf A_n$ is an $n\times n$ Hermitian matrix. Then the empirical spectral distribution (ESD) of $\mathbf A_n$ is defined by
\[
F^{\mathbf A_n}(x)=\frac1n\sum_{j=1}^n I(\lambda_j\le x).
\]
''',[3],'Section 2.1 — empirical spectral distribution',symbols=[r'F^{\mathbf A_n}(x)'],shape='Empirical distribution of all eigenvalues with multiplicity. n is the generic matrix dimension here; the Gram matrix later has dimension p.')

add('D2','Limit Spectral Distribution',r'''
In the asymptotic scenario where $n$ tends to infinity, if the limit of $F^{\mathbf A_n}(x)$ exists, it is denoted as the Limit Spectral Distribution (LSD). This represents the distribution that emerges as a result of this convergence in the context of spectral analysis.
''',[3],'Section 2.1 — Limit Spectral Distribution',{'D1':'The limit is of the empirical spectral distribution.'},phrases=['Limit Spectral Distribution'],shape='Source introductory limit definition; the specific convergence mode used in Theorem 2.1 is separately defined in Definitions 2.1 and 2.2.')

add('D3','Stieltjes transform',r'''
The Stieltjes transform of $F^{\mathbf A}(x)$ is given by
\[
m_{F^{\mathbf A}}(z)=\int\frac1{x-z}\,dF^{\mathbf A}(x)=\frac1n\operatorname{tr}(\mathbf A-z\mathbf I_n)^{-1},\qquad z\in\mathbb C^+.
\]
''',[3],'Section 2.1 — Stieltjes transform',{'D1':'The displayed matrix example integrates the empirical spectral distribution.'},symbols=[r'm_{F^{\mathbf A}}(z)'],shape='Stieltjes convention (x-z)^-1, positive imaginary part on the upper half-plane. The integral definition is used for the limiting law as well.')

add('D4','population',r'''
Consider the random vector $\mathbf y=\boldsymbol\Sigma_n^{1/2}\mathbf x$, where $\mathbf x$ represents a $p$-dimensional random vector whose entries are independent and identically distributed (i.i.d.) random variables with zero mean and unit variance. In this context, $\mathbf y$ typically serves as a model for a $p$-dimensional population with covariance matrix $\Sigma_n$.
''',[3],'Section 2.1 — complete population model',kind='source_passage',symbols=[r'\mathbf y=\boldsymbol\Sigma_n^{1/2}\mathbf x'],shape='Centered linear population model with independent standardized coordinates before multiplication by the covariance square root. Coordinate independence does not extend to y; Sigma typography varies in the source.')

add('D5','incomplete population',r'''
To incorporate missing at random mechanisms, we introduce the random vector $\mathbf d=(d_1,\ldots,d_p)^T$, where each $d_j$ is an independent Bernoulli random variable $B(1,p_j)$, for $j=1,\ldots,p$. Consequently, we consider the Hadamard product of the random vector $\mathbf z=\mathbf d\circ\mathbf y$ as the population with missing probability. This population is referred to as the incomplete population, distinguishing it from the complete population $\mathbf y$. To conduct statistical inference, we draw a sample of $n$ observations from the incomplete population, denoted as $\mathbf z_1,\mathbf z_2,\ldots,\mathbf z_n$.
''',[3],'Section 2.1 — incomplete population',{'D4':'The masked vector is the original complete population y.'},kind='source_passage',symbols=[r'\mathbf z=\mathbf d\circ\mathbf y'],shape='Independent Bernoulli observation indicators with coordinate probabilities p_j. Independence from data is a separate Assumption B; p_j is an observation probability despite the source wording missing probability.')

add('D6','Gram matrix',r'''
Accordingly, letting $\mathbf d_j=(d_{1j},\ldots,d_{pj})^T$ and $\mathbb D_j=\operatorname{diag}(d_{1j},\ldots,d_{pj})$, we compute the corresponding Gram matrix as
\[
\mathbf S_n=\frac1n\sum_{j=1}^n\mathbf z_j\mathbf z_j^T=\frac1n\mathbf Z\mathbf Z^T=\frac1n\sum_{j=1}^n\mathbb D_j\mathbf y_j\mathbf y_j^T\mathbb D_j=\frac1n(\mathbf D_n\circ\boldsymbol\Sigma_n^{1/2}\mathbf X_n)(\mathbf D_n\circ\boldsymbol\Sigma_n^{1/2}\mathbf X_n)^T,
\]
where $\mathbf X_n=(\mathbf x_1,\ldots,\mathbf x_n)=(x_{jk})$ and $\mathbf D_n=(d_{jk})$.
''',[4],'Section 2.1 — Gram matrix',{'D5':'Columns z_j are observations of the incomplete population, with the complete y_j and latent x_j resolved there.'},symbols=[r'\mathbf S_n',r'\mathbb D_j'],shape='Sample Gram matrix divided by n, without pairwise missing-count renormalization or sample-mean subtraction. Bold D_n is the rectangular mask and blackboard D_j is a diagonal column mask.')

add('D7','auxiliary matrix',r'''
In the context of statistical applications, we introduce an auxiliary matrix $\Theta_n$. This auxiliary matrix is arbitrary, as long as it satisfies the specific assumptions outlined in our main results. The form of this matrix may vary case by case in statistical applications, depending on the particular problem under consideration.
''',[4],'Section 2.1 — auxiliary matrix',symbols=[r'\Theta_n'],shape='Auxiliary matrix parameter. Its conditions are stated separately in B and D; the introductory passage does not explicitly specify positive semidefiniteness or invertibility.')

add('D8','missing probability matrix',r'''
Define $\mathbb P=\mathrm E\mathbb D_1=\operatorname{diag}(p_1,\ldots,p_p)$ and
\[
\mathbb P^{(2)}=\mathrm E(\mathbb D_j-\mathbb P)^2=\mathbb P-\mathbb P^2,\qquad
\mathbb P^{(3)}=\mathrm E(\mathbb D_j-\mathbb P)^3=\mathbb P-3\mathbb P^2+2\mathbb P^3,
\]
\[
\mathbb P^{(4)}=\mathrm E(\mathbb D_j-\mathbb P)^4=\mathbb P-4\mathbb P^2+6\mathbb P^3-3\mathbb P^4,\qquad
\mathbb P^{(5)}=(\mathbb P^{(4)}-3(\mathbb P^{(2)})^2).
\]
''',[4],'Section 2.2 — diagonal probability and centered-moment matrices',{'D6':'The expectation uses the diagonal Bernoulli mask D_j defined with the Gram matrix.'},context=r'where $\mathbb P$ represents the missing probability matrix.',context_pages=[13],symbols=[r'\mathbb P^{(2)}',r'\mathbb P^{(5)}'],shape='Diagonal mask probability and centered moments. P^(5) is a fourth cumulant expression, not a fifth raw or centered moment. P_n in later statements is the dimension-indexed notation.')

add('D9','sub-Gaussian norm',r'''
Recall that a random variable $X$ is considered sub-Gaussian if there exists a constant $C$ such that:
\[
\mathrm E\exp(X^2/C^2)\le2.
\]
We define its sub-Gaussian norm as:
\[
\|X\|_g=\inf\{c>0:\mathrm E\exp(X^2/c^2)\le2\}.
\]
''',[4],'Section 2.2 — sub-Gaussian norm',symbols=[r'\|X\|_g'],shape='Exponential-square Orlicz norm with threshold 2; do not replace it by a tail parameter with different normalization.')

add('D10','independent and identically sub-Gaussian',r'''
Assumption A: The random variables $x_{jk},j,k=1,2,\ldots$ are independent and identically sub-Gaussian with zero mean, unit variance and sub-Gaussian norm $\|x\|_g$. Let $\mathrm E|x_{11}|^4=\nu_4$.
''',[4],'Assumption A',{'D9':'Assumption A uses the displayed sub-Gaussian norm.','D6':'The x_jk are the latent data entries in X_n.'},kind='assumption',symbols=[r'\nu_4'],phrases=['Assumption A'],shape='Uniform latent-coordinate distribution and fourth moment; preserve the printed wording identically sub-Gaussian, interpreted with the iid model paragraph, not as an assumption directly on masked correlated observations.')

add('D11','independent',r'''
Assumption B: The matrices $\mathbf X_n$ and $\mathbf D_n$ are independent, and $\Theta_n$ is a nonrandom matrix.
''',[4],'Assumption B',{'D6':'X_n and D_n are the latent data and rectangular mask matrices.','D7':'Theta_n is the auxiliary matrix.'},kind='assumption',symbols=[r'\mathbf X_n',r'\mathbf D_n'],phrases=['Assumption B'],shape='Independence of full data and mask matrices, plus deterministic auxiliary matrix. The source model imposes more than a general conditional MAR mechanism.')

add('D12','convergence regime',r'''
Assumption C: The convergence regime is $y_n=p/n\to y\in(0,+\infty)$.
''',[4],'Assumption C',kind='assumption',symbols=[r'y_n=p/n'],phrases=['Assumption C'],shape='Joint dimension-sample sequence with strictly positive finite aspect ratio.')

add('D13','incomplete population spectral distribution',r'''
Assumption D: The spectral distribution $H_n$ of the matrix $\Psi_n=\boldsymbol\Theta_n^{1/2}\mathbf T_n\boldsymbol\Theta_n^{1/2}$ where $\mathbf T_n=\mathbb P\boldsymbol\Sigma_n\mathbb P+\mathbb P^{(2)}\circ\boldsymbol\Sigma_n$ weakly converges to a probability distribution $H$, as $p\to\infty$, referred as the incomplete population spectral distribution (IPSD). Let the spectral norm of the sequence $(\boldsymbol\Sigma_n\Theta_n)$ be uniformly bounded.
''',[4],'Assumption D',{'D1':'H_n is the empirical spectral distribution of Psi_n.','D4':'Sigma_n is the complete population covariance.','D7':'The transformed population matrix uses the auxiliary Theta_n.','D8':'T_n uses the observation probabilities and centered second-moment matrix.'},kind='assumption',symbols=[r'\Psi_n',r'\mathbf T_n',r'H_n'],phrases=['Assumption D'],shape='Weak IPSD convergence and uniform spectral bound; retain the displayed square-root product and the bound on Sigma_n Theta_n rather than replace them with bounds on each factor.')

add('D14','high probability',r'''
If for any $\ell>0$, $1-\mathrm P(A_n)=o(n^{-\ell})$ as $n\to\infty$, then we say $A_n$ occurs with high probability (w.h.p).
''',[3],'Notation — events with high probability',symbols=[r'1-\mathrm P(A_n)=o(n^{-\ell})'],shape='Event failure probability decays faster than every inverse polynomial. This is stronger than probability merely tending to one.')

add('D15','Convergence with high probability',r'''
We say that a sequence of random variables $x_n$ converges with high probability to $x$, denoted as $x_n\xrightarrow{\mathrm{w.h.p.}}x$, if for any $\epsilon>0$ and $\ell>0$,
\[
\mathrm P(|x_n-x|>\epsilon)=o(n^{-\ell}),\qquad n\to\infty.
\]
''',[6],'Definition 2.1 (Convergence with high probability)',context='Definition 2.1 (Convergence with high probability).',symbols=[r'\mathrm P(|x_n-x|>\epsilon)=o(n^{-\ell})'],shape='Scalar convergence at every fixed positive tolerance with superpolynomial tail bounds, not ordinary convergence in probability.')

add('D16','Convergence with high probability of ESD',r'''
Consider a sequence of random matrices $\mathbf A_n$ with empirical spectral distributions denoted by $F^{\mathbf A_n}$. Adopting the usual definition of Kolmogorov distance $\|F-G\|_\infty=\sup_x|F(x)-G(x)|$ for two distribution functions $F$ and $G$, we say that the sequence $F^{\mathbf A_n}$ converges with high probability to $F$, denoted as $F^{\mathbf A_n}\xrightarrow{\mathrm{w.h.p.}}F$, if
\[
\|F^{\mathbf A_n}-F\|_\infty\xrightarrow{\mathrm{w.h.p.}}0.
\]
''',[6],'Definition 2.2 (Convergence with high probability of ESD)',{'D1':'The random distributions are the ESDs.','D15':'The Kolmogorov distance converges in the strong probability sense of Definition 2.1.'},context='Definition 2.2 (Convergence with high probability of ESD).',symbols=[r'\|F^{\mathbf A_n}-F\|_\infty'],shape='High-probability convergence in uniform CDF distance; do not substitute only weak convergence of measures.')

add('D17','finite-dimensional approximation of the LSD',r'''
Let $F^{y,H}$ represent the distribution $F$, and let $F^{y_n,H_n}$ be obtained by replacing $y$ and $H$ with $y_n$ and $H_n$, respectively. We denote $m_n^0(z)$ as $m_{F^{y_n,H_n}}(z)$, which satisfies the equation (2.1). In other words, we have
\[
\underline m_n^0(z)=\frac1{y_n\int\frac{t}{t\underline m_n^0(z)+1}\,dH_n(t)-z}\tag{2.2}
\]
and
\[
z=-\frac1{\underline m_n^0}+y\int\frac{t}{t\underline m_n^0+1}\,dH_n(t).\tag{2.3}
\]
Here, $-z\underline m_n^0(z)=1-y_n-y_nzm_n^0(z)$.
''',[7],'After Theorem 2.1 — finite spectral approximation and companion transform',{'D13':'The population law H and finite H_n come from Assumption D.','D12':'The aspect ratios y and y_n come from Assumption C.','D3':'m_n^0 is the Stieltjes transform of the finite-parameter law.','D2':'F denotes the limiting spectral distribution characterized in Theorem 2.1.'},context=r'Here, $F^{\mathbf S_n\Theta_n}(x)-F^{c_n,H_n}(x)$ provides a measure of the deviation from the finite-dimensional approximation of the LSD.',context_pages=[10],symbols=[r'F^{y_n,H_n}',r'\underline m_n^0(z)'],shape='Original finite-parameter laws and companion transform relationship. Equation (2.3) prints y, whereas (2.2) uses y_n; c,c_n elsewhere are unresolved aliases. The limiting companion transform in Theorem 2.3 is not separately defined in this paragraph.')

add('D18','LSS',r'''
Let us consider the LSS of $\mathbf S_n\Theta_n$ associated with a test function $f$. This statistic is given by the integral:
\[
L_n(f,\mathbf S_n\Theta_n)=\int f(x)\,dF^{\mathbf S_n\Theta_n}(x).
\]
Consequently, the centralized LSS can be expressed as follows:
\[
L^c(f,\mathbf S_n\Theta_n)=\int f(x)\,d[F^{\mathbf S_n\Theta_n}(x)-F^{c_n,H_n}(x)].
\]
''',[10],'Section 2.6 — LSS and centralized LSS displays',{'D6':'The statistic uses the original Gram matrix S_n.','D7':'The spectral argument multiplies S_n by auxiliary Theta_n.','D1':'The first integral is against an ESD.','D17':'The centering is the finite-parameter spectral law, printed with c_n instead of y_n.'},symbols=[r'L^c(f,\mathbf S_n\Theta_n)'],shape='Two exact source passages with intervening explanatory prose omitted. The normalized ESD integral and its centralized version have no p multiplier in the source; the CLT scale is not silently repaired.')

add('D19','terms that are independent of the kurtosis',r'''
\[
\begin{aligned}
\mathcal I_2(\mathbf A,\mathbf B,\Sigma_n,\mathbb P)
={}&4\operatorname{tr}[\mathbb P^{(2)}(\mathbf A\circ\mathbf B)\mathbb P^{(2)}(\boldsymbol\Sigma_n\circ\boldsymbol\Sigma_n)]+2\operatorname{tr}[(\mathbf A\circ\mathbb P^{(2)})\boldsymbol\Sigma_n(\mathbf B\circ\mathbb P^{(2)})\boldsymbol\Sigma_n]\\
&+6\operatorname{tr}(\mathbb P^{(3)}\circ\mathbf A\circ\boldsymbol\Sigma_n\circ(\mathbf B\mathbb P\boldsymbol\Sigma_n))+2\operatorname{tr}((\mathbb P^{(2)}\circ\mathbf A)\boldsymbol\Sigma_n\mathbb P\mathbf B\mathbb P\boldsymbol\Sigma_n)\\
&+2\operatorname{tr}((\mathbb P^{(2)}\circ\mathbf B)\boldsymbol\Sigma_n\mathbb P\mathbf A\mathbb P\boldsymbol\Sigma_n)+3\operatorname{tr}[\mathbb P^{(3)}\circ\mathbf B\circ\boldsymbol\Sigma_n\circ(\mathbf A\mathbb P\boldsymbol\Sigma_n+\mathbf A^T\mathbb P\boldsymbol\Sigma_n)]\\
&+3\operatorname{tr}[\mathbf A\circ\boldsymbol\Sigma_n\circ\mathbf B\circ\boldsymbol\Sigma_n\circ\mathbb P^{(5)}]+4\operatorname{tr}[\mathbb P^{(2)}\circ(\mathbf A\mathbb P\boldsymbol\Sigma_n+\mathbf A^T\mathbb P\boldsymbol\Sigma_n)\circ(\mathbf B\mathbb P\boldsymbol\Sigma_n)],
\end{aligned}
\]
''',[5],'Lemma 2.1 — definition of the functional I₂',{'D4':'The functional uses the complete population covariance.','D8':'The functional uses the diagonal probability, centered moments and fourth cumulant.'},context='where the terms that are independent of the kurtosis of the underlying distribution are given by',symbols=[r'\mathcal I_2'],shape='The I_2 functional displayed inside Lemma 2.1, consumed by the CLT and a_P,Sigma. A is any nonrandom p-by-p matrix and B is nonrandom symmetric in the lemma; the lemma conclusion and proof are not additional inventoried theorems.')

add('D20','terms that are dependent on the kurtosis',r'''
\[
\begin{aligned}
\mathcal{II}(\mathbf A,\mathbf B,\Sigma_n,\mathbb P)
={}&\operatorname{tr}[(\boldsymbol\Sigma_n^{1/2}(\mathbb P\mathbf A\mathbb P+\mathbb P^{(2)}\circ\mathbf A)\boldsymbol\Sigma_n^{1/2})\circ(\boldsymbol\Sigma_n^{1/2}(\mathbb P\mathbf B\mathbb P+\mathbb P^{(2)}\circ\mathbf B)\boldsymbol\Sigma_n^{1/2})]\\
&+2\operatorname{tr}[\mathbb P^{(2)}(\mathbf A\circ\mathbf B)\mathbb P^{(2)}(\boldsymbol\Sigma_n^{1/2}\circ\boldsymbol\Sigma_n^{1/2})^2]+\operatorname{tr}[\mathbb P^{(5)}\circ\mathbf A\circ\mathbf B\circ(\boldsymbol\Sigma_n^{1/2}\circ\boldsymbol\Sigma_n^{1/2})^2]\\
&+2\operatorname{tr}[(\boldsymbol\Sigma_n^{1/2}\circ\boldsymbol\Sigma_n^{1/2}\circ\boldsymbol\Sigma_n^{1/2})(\mathbf A\circ\mathbb P^{(3)})\mathbf B\mathbb P\boldsymbol\Sigma_n^{1/2}]\\
&+\operatorname{tr}[(\boldsymbol\Sigma_n^{1/2}\circ\boldsymbol\Sigma_n^{1/2}\circ\boldsymbol\Sigma_n^{1/2})(\mathbf B\circ\mathbb P^{(3)})(\mathbf A+\mathbf A^T)\mathbb P\boldsymbol\Sigma_n^{1/2}]\\
&+2\operatorname{tr}[(\boldsymbol\Sigma_n^{1/2}\circ\boldsymbol\Sigma_n^{1/2})\mathbb P^{(2)}((\mathbf A\mathbb P\boldsymbol\Sigma_n^{1/2}+\mathbf A^T\mathbb P\boldsymbol\Sigma_n^{1/2})\circ(\mathbf B\mathbb P\boldsymbol\Sigma_n^{1/2}))].
\end{aligned}
\]
''',[5,6],'Lemma 2.1 — definition of the functional II, continued on page 6',{'D4':'The functional uses the complete covariance and its square root.','D8':'The functional uses the diagonal mask moments and fourth cumulant.'},context='while the terms that are dependent on the kurtosis of the underlying distribution are expressed as',context_pages=[5],symbols=[r'\mathcal{II}'],shape='Full six-term trace functional across the page boundary. Ordinary matrix products and Hadamard products are distinct; the outer factor nu_4-3 belongs to the CLT and is not absorbed into this definition.')

add('D21','incomplete sample',r'''
We adopt the data model discussed in the previous section. Specifically, we draw an incomplete sample of $n$ observations from a centered $p$-dimensional population $\mathbf y=(y_1,\ldots,y_p)^T$. The missingness is governed by a missing probability matrix $\mathbb P$, which determines the probability of each component being observed. Similarly to Lounici [13], where the estimation of the covariance matrix is considered, we assume that the missing probabilities are known. For $1\le i\le p$ and $1\le j\le n$, we define $d_{ij}=1$ if the $i$th variate of the $j$th sample is observed, and $d_{ij}=0$ otherwise. Let $\mathbb D_j=\operatorname{diag}(d_{1j},\ldots,d_{pj})$. We compute the corresponding Gram matrix as follows:
\[
\hat{\mathbf S}_n=\frac1n\sum_{j=1}^n\mathbb D_j\mathbf y_j\mathbf y_j^T\mathbb D_j.
\]
''',[12],'Section 3.1 — incomplete sample with known observation probabilities',{'D5':'Section 3 explicitly adopts the incomplete population model from Section 2.','D8':'The given probability matrix is the diagonal matrix P.'},kind='source_passage',symbols=[r'\hat{\mathbf S}_n'],phrases=['missing probabilities are known'],shape='Known observation probabilities and raw second-moment matrix of the centered population. No estimated probabilities or empirical centering are substituted.')

add('D22','null and alternative hypotheses',r'''
We consider the null and alternative hypotheses for testing the equality of high-dimensional covariance matrices, denoted by $\boldsymbol\Sigma=\mathrm E\mathbf y\mathbf y^T$:
\[
H_0:\boldsymbol\Sigma=\boldsymbol\Sigma_0\quad\text{vs.}\quad H_1:\boldsymbol\Sigma\ne\boldsymbol\Sigma_0.
\]
Here, $\boldsymbol\Sigma_0$ represents the given covariance matrix against which we are testing the equality.
''',[12],'Section 3.1 — covariance null hypothesis',{'D21':'The covariance belongs to the centered population sampled in Section 3.'},kind='condition',symbols=[r'H_0',r'\boldsymbol\Sigma_0'],shape='Fixed given covariance null; no estimated null matrix and no composite equivalence up to scale.')

add('D23','limiting parameters',r'''
\[
a_{\mathbb P,\Sigma}=\lim_{n\to\infty}p^{-1}\mathcal I_2(\mathbf T_n^{-1},\mathbf T_n^{-1},\boldsymbol\Sigma_n,\mathbb P_n)+(\nu_4-3)\lim_{n\to\infty}p^{-1}\mathcal{II}(\mathbf T_n^{-1},\mathbf T_n^{-1},\boldsymbol\Sigma_n,\mathbb P_n).
\]
''',[12],'Corollary 2.1 — definition of a in the renormalized case',{'D13':'T_n is the incomplete-population covariance matrix in Assumption D.','D19':'The first term evaluates the original I_2 functional.','D20':'The second term evaluates the original II functional.','D10':'nu_4 is the latent-coordinate fourth moment in Assumption A.'},context='It is demonstrated that in this scenario, the limiting parameters in the general CLT manifest a more accessible form and offer computational simplicity.',symbols=[r'a_{\mathbb P,\Sigma}'],shape='Renormalized CLT scalar evaluated with inverse T_n and normalization p^-1. Existence of inverses and limits is used but not separately established by this definition. This scalar is not the general analytic function a(z).')

add('D24','test statistics',r'''
Specifically we define the matrix $\mathbf T_0=\mathbb P\boldsymbol\Sigma_0\mathbb P+\mathbb P^{(2)}\circ\boldsymbol\Sigma_0$, where $\mathbb P$ represents the missing probability matrix. We consider two test statistics,
\[
\mathcal T_F=\operatorname{tr}(\mathbf T_0^{-1}\hat{\mathbf S}_n-\mathbf I_p)^2,\qquad\mathcal T_L=\log\det\mathbf T_0^{-1}\hat{\mathbf S}_n.
\]
''',[13],'Section 3.2 — covariance test statistics',{'D22':'T_0 uses the fixed covariance Sigma_0 under the null.','D21':'The statistics use the observed Gram matrix hat S_n.','D8':'The normalization matrix uses P and P^(2).'},symbols=[r'\mathcal T_F',r'\mathcal T_L'],shape='Trace of the squared residual matrix and log determinant of the normalized observed Gram matrix. Source typesets tr(A)^2 without explicit brackets around the squared-matrix argument; retain its notation and record the standard intended reading separately. No inversion or log-domain convention is supplied.')


def main():
    for lid,member in members.items():
        assert all(d in members for d in member['depends_on']),lid
        own=member['statement_original']+' '+member['local_label']
        assert any(s in own for s in member['highlight_symbols']+member['highlight_phrases']),lid
        assert not any(ord(c)<32 and c!='\n' for c in member['statement_original']),lid
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages; full source audit remains pending.')

if __name__=='__main__': main()
