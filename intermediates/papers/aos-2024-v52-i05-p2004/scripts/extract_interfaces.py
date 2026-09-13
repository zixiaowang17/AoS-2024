"""Preserve original main-text source entries for the nine-Theorem census."""
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
add(1,'leave-one-column-out submatrix',r'''Consider two matrices
\[
Y=(y_1,\ldots,y_{n-1})\in\mathbb R^{p\times(n-1)}\text{ and }\hat Y=(y_1,\ldots,y_{n-1},y_n)\in\mathbb R^{p\times n},
\]
(1)
where $Y$ is a leave-one-column-out submatrix of $\hat Y$ with the last column removed.''',[1],[],[r'Y=(y_1,\ldots,y_{n-1})',r'y_n'],'Two arbitrary real matrices differing by their last column; no mixture model or randomness is assumed.','Section 1 — Matrices (1)',kind='source_passage')
add(2,'Singular Value Decomposition',r'''Consider two matrices as in (1) such that they are equal to each other except that $\hat Y$ has an extra last column. Let the Singular Value Decomposition (SVD) of these two matrices be
\[
Y=\sum_{i\in[p\wedge(n-1)]}\sigma_i u_iv_i^T\text{ and }\hat Y=\sum_{i\in[p\wedge n]}\hat\sigma_i\hat u_i\hat v_i^T,
\]
where $\sigma_1\geq\ldots\geq\sigma_{p\wedge(n-1)}$ and $\hat\sigma_1\geq\ldots\geq\hat\sigma_{p\wedge n}$. Consider any $r\in[p\wedge(n-1)]$. Define
\[
U_r:=(u_1,\ldots,u_r)\in\mathbb O^{p\times r}\text{ and }\hat U_r:=(\hat u_1,\ldots,\hat u_r)\in\mathbb O^{p\times r}
\]
to include the leading $r$ left singular vectors of $Y$ and $\hat Y$, respectively.''',[4],[1],[r'U_r',r'\hat U_r',r'\sigma_r'],'Ordered singular decompositions and their leading left-vector matrices in the arbitrary-matrix setup; sigma_{r+1} at the last allowed index has no explicit zero-extension convention in this passage.','Section 2.1 — Singular Value Decomposition')
add(3,'mixture model',r'''We consider a mixture model with $k$ centers $\theta_1^*,\theta_2^*,\ldots,\theta_k^*\in\mathbb R^p$ and a cluster assignment vector $z^*\in[k]^n$. The observations $X_1,X_2,\ldots,X_n\in\mathbb R^p$ are generated from
\[
X_i=\theta_{z_i^*}^*+\epsilon_i,
\]
(6)
where $\epsilon_1,\ldots,\epsilon_n\in\mathbb R^p$ are noises.''',[6],[],[r'X_i=\theta_{z_i^*}^*+\epsilon_i',r'z^*\in[k]^n'],'Fixed centers and assignments with arbitrary noise vectors. Independence and distributions are additional theorem hypotheses, not part of the general mixture model.','Section 2.2 — Mixture Models (6)',kind='source_passage')
add(4,'data matrix',r'''The data matrix $X:=(X_1,\ldots,X_n)\in\mathbb R^{p\times n}$ can be written equivalently in a matrix form
\[
X=P+E,
\]
(7)
where $P:=(\theta_{z_1^*}^*,\theta_{z_2^*}^*,\ldots,\theta_{z_n^*}^*)$ is the signal matrix and $E:=(\epsilon_1,\ldots,\epsilon_n)$ is the noise matrix.''',[6],[3],[r'X=P+E',r'E:=(\epsilon_1,\ldots,\epsilon_n)'],'Original matrix representation of the mixture observations, including the named signal and noise matrices. No probabilistic restriction is added.','Section 2.2 — Matrix form (7)')
add(5,'smallest cluster size',r'''Define $\beta:=\frac1{n/k}\min_{a\in[k]}|\{i:z_i^*=a\}|$ such that $\beta n/k$ is the smallest cluster size.''',[6],[3],[r'\beta',r'\beta n/k'],'Normalized minimum cluster size. The different powers of k and numerical bounds in each theorem remain distinct local hypotheses.','Section 2.2 — Smallest cluster size')
add(6,'leave-one-out counterparts',r'''We are interested in the left singular subspaces of $X$ and its leave-one-out counterparts. For each $i\in[n]$, define $X_{-i}$ to be a submatrix of $X$ with its $i$th column removed. That is,
\[
X_{-i}:=(X_1,\ldots,X_{i-1},X_{i+1},\ldots,X_n)\in\mathbb R^{p\times(n-1)}.
\]
(8)''',[6],[4],[r'X_{-i}'],'Remove each specified column from the mixture data matrix; not a change to the true assignments or noise law.','Section 2.2 — Leave-one-out matrices (8)')
add(7,'left singular vectors',r'''Let their SVDs be $X=\sum_{j\in[p\wedge n]}\hat\lambda_j\hat u_j\hat v_j^T$ and $X_{-i}=\sum_{j\in[p\wedge(n-1)]}\hat\lambda_{-i,j}\hat u_{-i,j}\hat v_{-i,j}^T$, where $\hat\lambda_1\geq\hat\lambda_2\geq\ldots\geq\hat\lambda_{p\wedge n}$ and $\hat\lambda_{-i,1}\geq\hat\lambda_{-i,2}\geq\ldots\geq\hat\lambda_{-i,p\wedge(n-1)}$. Note that the signal matrix $P$ is at most rank-$k$. Then for any $r\in[k]$, define
\[
\hat U_{1:r}:=(\hat u_1,\hat u_2,\ldots,\hat u_r)\in\mathbb O^{p\times r}\text{ and }\hat U_{-i,1:r}=(\hat u_{-i,1},\ldots,\hat u_{-i,r})\in\mathbb O^{p\times r}
\]
to include the leading $r$ left singular vectors of $X$ and $X_{-i}$, respectively.''',[7],[4,6],[r'\hat U_{1:r}',r'\hat U_{-i,1:r}',r'\hat U_{1:\kappa}',r'\hat U_{-i,1:\kappa}'],'Empirical full-data and leave-one-out singular-vector matrices. These are not the signal-matrix singular vectors. The k-based index domain is retained without silently extending a finite SVD.','Section 2.2 — Empirical singular vectors')
add(8,'singular values',r'''Let $\lambda_1\geq\lambda_2\geq\ldots\geq\lambda_{p\wedge n}$ be the singular values of $P$ and $\kappa$ be the rank of $P$ such that $\kappa\in[k]$, $\lambda_\kappa>0$, and $\lambda_{\kappa+1}=0$.''',[7],[4],[r'\lambda_\kappa',r'\kappa',r'\lambda_r'],'Population signal singular values and positive rank kappa, distinct from empirical hatted singular values. Kappa may be smaller than k.','Section 2.2 — Signal spectrum')
add(9,'Spectral Clustering',r'''Algorithm 1: Spectral Clustering

Input: Data matrix $X=(X_1,\ldots,X_n)\in\mathbb R^{p\times n}$, number of clusters $k$, number of singular vectors $r$

Output: Cluster assignment vector $\hat z\in[k]^n$

1 Perform SVD on $X$ to have
\[
X=\sum_{i=1}^{p\wedge n}\hat\lambda_i\hat u_i\hat v_i^T,
\]
where $\hat\lambda_1\geq\hat\lambda_2\geq\ldots\geq\hat\lambda_{p\wedge n}\geq0$ and $\{\hat u_i\}_{i=1}^{p\wedge n}\in\mathbb R^p,\{\hat v_i\}_{i=1}^{p\wedge n}\in\mathbb R^n$. Let $\hat U_{1:r}:=(\hat u_1,\ldots,\hat u_r)\in\mathbb R^{p\times r}$.

2 Perform $k$-means on the columns of $\hat U_{1:r}^TX$. That is,
\[
\left(\hat z,\{\hat c_j\}_{j\in[k]}\right)=\operatorname*{argmin}_{z\in[k]^n,\{c_j\}_{j\in[k]}\in\mathbb R^r}\sum_{i\in[n]}\|\hat U_{1:r}^TX_i-c_{z_i}\|^2.
\]
(14)''',[8],[4],[r'\hat z',r'\hat U_{1:r}^TX_i-c_{z_i}'],'Full two-step source algorithm with an exact global k-means minimizer. Theorems 3.1 and 3.3 choose r=kappa and r=k respectively. Approximate k-means in Discussion is not substituted.','Algorithm 1 — Spectral Clustering')
add(10,'misclustering error',r'''For any $z\in[k]^n$, its misclustering error is defined as
\[
\ell(z,z^*):=\min_{\phi\in\Phi}\frac1n\sum_{i\in[n]}\mathbb I\{z_i=\phi(z_i^*)\},
\]
where $\Phi:=\{\phi:\phi\text{ is a bijection from }[k]\text{ to }[k]\}$. The minimization of $\Phi$ is due to that the cluster assignment vector $z^*$ is identifiable only up to a permutation of the labels $[k]$.''',[9],[3],[r'\ell(z,z^*)',r'\ell(\hat z,z^*)',r'\ell(\tilde z,z^*)',r'\ell(\check z,z^*)'],'Preserve the printed equality inside the indicator. Equation (17) on the same page instead counts inequalities; this source discrepancy is separately flagged, not silently corrected.','Section 3.1 — Misclustering error')
add(11,'minimum distance among centers',r'''Define $\Delta$ to be the minimum distance among centers, i.e.,
\[
\Delta:=\min_{a,b\in[k]:a\ne b}\|\theta_a^*-\theta_b^*\|.
\]''',[9],[3],[r'\Delta'],'Minimum Euclidean distance between distinct cluster centers. The real-delta parameterization of the two-cluster model is retained separately with its sign issue.','Section 3.1 — Separation')
add(12,'sub-Gaussian',r'''For a random variable $X$, we say $X$ is sub-Gaussian with variance proxy $\sigma^2$ (denoted as $X\sim\mathrm{SG}(\sigma^2)$) if $\mathbb Ee^{tX}\leq\exp(\sigma^2t^2/2)$ for any $t\in\mathbb R$.''',[3],[],[r'\mathrm{SG}(\sigma^2)',r'\mathbb Ee^{tX}\leq\exp(\sigma^2t^2/2)'],'Scalar uncentered moment-generating-function bound for every real t; no subtraction of the mean is inserted. The variance proxy sigma squared is distinct from actual variance bar-sigma squared.','Notation — Scalar sub-Gaussian condition')
add(13,'sub-Gaussian random vector',r'''For a random vector $X\in\mathbb R^d$, we say $X$ is sub-Gaussian with variance proxy $\sigma^2$ (denoted as $X\sim\mathrm{SG}_d(\sigma^2)$) if $u^TX\sim\mathrm{SG}(\sigma^2)$ for any unit vector $u\in\mathbb R^d$.''',[3],[12],[r'\mathrm{SG}_d(\sigma^2)',r'\mathrm{SG}_p(\sigma^2)'],'Common scalar variance proxy in every unit direction, not coordinatewise independence. Theorem-specific independence across observations remains separate.','Notation — Vector sub-Gaussian condition',context=r'''Theorem 3.1 assumes that each noise $\epsilon_i$ is an independent sub-Gaussian random vector with zero mean and variance proxy $\sigma^2$ and establishes an exponential rate for the risk $\mathbb E\ell(\hat z,z^*)$.''',context_page=11)
add(14,'Spectral Clustering with Adaptive Dimension Reduction',r'''Algorithm 2: Spectral Clustering with Adaptive Dimension Reduction

Input: Data matrix $X=(X_1,\ldots,X_n)\in\mathbb R^{p\times n}$, number of clusters $k$, threshold $T$

Output: Clustering label vector $\tilde z\in[k]^n$

1 Perform SVD on $X$ same as Step 1 of Algorithm 1.

2 Let $\hat r$ be the largest index in $[k]$ such that the difference between two neighboring singular values is greater than $T$, i.e.,
\[
\hat r=\max\{a\in[k]:\hat\lambda_a-\hat\lambda_{a+1}\geq T\}.
\]
(23)
Let $\hat U_{1:\hat r}:=(\hat u_1,\ldots,\hat u_{\hat r})\in\mathbb R^{p\times\hat r}$.

3 Perform $k$-means on the columns of $\hat U_{1:\hat r}^TX$. That is,
\[
\left(\tilde z,\{\tilde c_j\}_{j=1}^k\right)=\operatorname*{argmin}_{z\in[k]^n,\{c_j\}_{j=1}^k\in\mathbb R^{\hat r}}\sum_{i\in[n]}\|\hat U_{1:\hat r}^TX_i-c_{z_i}\|^2.
\]
(24)''',[13],[4],[r'\tilde z',r'\hat r=\max\{a\in[k]:\hat\lambda_a-\hat\lambda_{a+1}\geq T\}'],'Full adaptive algorithm. Import only Step 1 of Algorithm 1 as auxiliary A3; not its fixed-r clustering output. Preserve largest-index choice and the printed non-strict gap threshold. No empty-set fallback is supplied in the source.','Algorithm 2 — Spectral Clustering with Adaptive Dimension Reduction')
add(15,'two-cluster symmetric mixture model',r'''Consider a mixture model (6) with two clusters such that
\[
\theta_1^*=-\theta_2^*=\delta\mathbf1_p,\text{ and }\{\epsilon_{i,j}\}_{i\in[n],j\in[p]}\overset{\mathrm{iid}}\sim F,
\]
(28)
for some $\delta\in\mathbb R$ and some distribution $F$, where $\{\epsilon_{i,j}\}_{j\in[p]}$ are entries of $\epsilon_i$ for each $i\in[n]$.''',[15,16],[3],[r'\theta_1^*=-\theta_2^*=\delta\mathbf1_p',r'\overset{\mathrm{iid}}\sim F'],'Two opposite constant-coordinate centers and iid noise entries across both samples and coordinates. The statement allows real delta; no positive sign is inserted.','Section 3.6 — Model (28)',kind='source_passage',context=r'''To answer this question, in this section we consider a two-cluster symmetric mixture model where the centers are proportional to $\mathbf1_p$ and the noises have i.i.d. entries.''',context_page=15)
add(16,'spectral estimator',r'''Define
\[
\left(\check z,\{\check c_j\}_{j=1}^2\right)=\operatorname*{argmin}_{z\in[2]^n,\{c_j\}_{j=1}^2\in\mathbb R}\sum_{i\in[n]}(\hat u_1^TX_i-c_{z_i})^2.
\]
(29)
The performance of the spectral estimator $\check z$ will be the focus in this section.''',[16],[4,15],[r'\check z',r'\hat u_1^TX_i-c_{z_i}'],'Two-means applied to the empirical leading singular-vector projection. It is not a sign estimator, and the true singular vector is not substituted for the empirical one. A3 retains the SVD convention used here.','Section 3.6 — Spectral estimator (29)')
add(17,'Fisher information',r'''Assume the distribution $F$ has a positive, continuously differentiable density $f$ with mean zero and finite Fisher information $\mathcal I:=\int(f'/f)^2f\,dx$. Assume $\Delta$ is a constant.''',[17],[11,15],[r'\mathcal I:=\int(f\prime/f)^2f\,dx'],'Original regularity assumptions and Fisher-information definition from Lemma 3.4, explicitly imported by Theorem 3.5. Delta is fixed in that lemma; it is not replaced by a growing-separation limit.','Lemma 3.4 — Assumptions',kind='condition')
# Select the exact printed-form LaTeX expression, including the prime, for D17.
members['D17']['highlight_symbols']=[r"\mathcal I:=\int(f'/f)^2f\,dx"]
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
