"""Preserve original tensor-model, algorithm, rate and lower-bound source passages."""
import json,hashlib
from save_inventory import ROOT,PID,STATEMENTS
REVIEW_ROOT=ROOT
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
add(1,'Tensor factor model',r'''Again, we consider as in (1.2)
\[
\mathcal X_t=\mathcal F_t\times_1 A_1\times_2\ldots\times_K A_K+\mathcal E_t.
\]
Without loss of generality, assume that $A_k$ is of rank $r_k$. $A_k$ is not necessarily orthonormal, which is different from the classical Tucker decomposition (Tucker, 1966).''',[6],[2],[r'\mathcal X_t=\mathcal F_t\times_1 A_1\times_2\ldots\times_K A_K+\mathcal E_t'],'Original model with deterministic full-column-rank loadings and latent tensor series. Dimensions, signal M_t and core/noise independence are archived as auxiliary source context. The lower-bound model separately binds orthonormal loadings and scalar lambda.','Section 2.2 — Tensor factor model',kind='source_passage',context='2.2. Tensor factor model.')
add(2,'mode product',r'''Here the $k$-mode product of $\mathcal X\in\mathbb R^{d_1\times d_2\times\cdots\times d_K}$ with a matrix $U\in\mathbb R^{d'_k\times d_k}$, denoted as $\mathcal X\times_k U$, is an order $K$-tensor of size $d_1\times\cdots\times d_{k-1}\times d'_k\times d_{k+1}\times\cdots\times d_K$ such that
\[
(\mathcal X\times_k U)_{i_1,\ldots,i_{k-1},j,i_{k+1},\ldots,i_K}=\sum_{i_k=1}^{d_k}\mathcal X_{i_1,i_2,\ldots,i_K}U_{j,i_k}.
\]''',[2],[],[r'\mathcal X\times_k U'],'Modewise contraction replaces only the kth tensor dimension; the matrix acts from the left along that index.','Section 1 — k-mode product',context='Here the $k$-mode product of $\mathcal X$')
add(3,'unfolding',r'''The mode-$k$ unfolding (or matricization) is defined as $\operatorname{mat}_k(\mathcal A)$, which maps a tensor $\mathcal A$ to a matrix $\operatorname{mat}_k(\mathcal A)\in\mathbb R^{m_k\times m_{-k}}$ where $m_{-k}=\prod_{j\ne k}^K m_j$. For example, if $\mathcal A\in\mathbb R^{m_1\times m_2\times m_3}$, then
\[
(\operatorname{mat}_1(\mathcal A))_{i,(j+m_2(k-1))}=(\operatorname{mat}_2(\mathcal A))_{j,(k+m_3(i-1))}=(\operatorname{mat}_3(\mathcal A))_{k,(i+m_1(j-1))}=\mathcal A_{ijk}.
\]''',[5],[],[r'\operatorname{mat}_k(\mathcal A)'],'Preserve the explicit cyclic column-order example; do not substitute a different matricization convention.','Section 2.1 — Mode-k unfolding')
add(4,'tensor product',r'''For any two tensors $\mathcal A\in\mathbb R^{m_1\times m_2\times\cdots\times m_K}$, $\mathcal B\in\mathbb R^{r_1\times r_2\times\cdots\times r_N}$, denote the tensor product $\otimes$ as $\mathcal A\otimes\mathcal B\in\mathbb R^{m_1\times\cdots\times m_K\times r_1\times\cdots\times r_N}$, such that
\[
(\mathcal A\otimes\mathcal B)_{i_1,\ldots,i_K,j_1,\ldots,j_N}=(\mathcal A)_{i_1,\ldots,i_K}(\mathcal B)_{j_1,\ldots,j_N}.
\]''',[5],[],[r'\mathcal A\otimes\mathcal B'],'Full outer tensor product, distinct from the matrix Kronecker product denoted by odot in the source.','Section 2.1 — Tensor product')
add(5,'matrix spectral norm',r'''The matrix spectral norm is denoted as $\|A\|_{\mathrm S}=\sigma_1(A)$.''',[5],[],[r'\|A\|_{\mathrm S}',r'\|\widehat P_k-P_k\|_{\mathrm S}',r'\|\widehat P_k^{(m)}-P_k\|_{\mathrm S}'],'Largest singular value, including projection errors. Singular value ordering is ambient source context; squared and unsquared losses remain distinct in T3.4/T3.5.','Section 2.1 — Matrix spectral norm')
add(6,'Hilbert Schmidt norm',r'''For tensor $\mathcal A\in\mathbb R^{m_1\times m_2\times\cdots\times m_K}$, the Hilbert Schmidt norm is defined as
\[
\|\mathcal A\|_{\mathrm{HS}}=\sqrt{\sum_{i_1=1}^{m_1}\cdots\sum_{i_K=1}^{m_K}(\mathcal A)^2_{i_1,\ldots,i_K}}.
\]
For a matrix, the Hilbert Schmidt norm is just the Frobenius norm.''',[5],[],[r'\|\mathcal A\|_{\mathrm{HS}}'],'Entrywise Euclidean tensor norm, used to normalize the two matrix arguments of the source order-four operator norm.','Section 2.1 — Hilbert Schmidt norm')
add(7,'tensor operator norm',r'''Define the tensor operator norm for an order-4 tensor $\mathcal A\in\mathbb R^{m_1\times m_2\times m_3\times m_4}$,
\[
\|\mathcal A\|_{\mathrm{op}}=\max\left\{\sum_{i_1,i_2,i_3,i_4}u_{i_1,i_2}\cdot u_{i_3,i_4}\cdot(\mathcal A)_{i_1,i_2,i_3,i_4}:\|U_1\|_{\mathrm{HS}}=\|U_2\|_{\mathrm{HS}}=1\right\},
\]
where $U_1=(u_{i_1,i_2})\in\mathbb R^{m_1\times m_2}$ and $U_2=(u_{i_3,i_4})\in\mathbb R^{m_3\times m_4}$.''',[5],[6],[r'\|\mathcal A\|_{\mathrm{op}}'],'Bilinear contraction against two unit-HS matrices, not the injective tensor norm over four independent vectors. The source reuses u for the entries of both matrices; preserve its notation.','Section 2.1 — Tensor operator norm')
add(8,'orthogonal projection',r'''Denote the orthogonal projection to the column space of $A_k$ as
\[
P_k=P_{A_k}=A_k(A_k^\top A_k)^{-1}A_k^\top=U_kU_k^\top,
\]
(2.2)
where $U_k$ is the left singular matrix in the SVD $A_k=U_k\Lambda_kV_k^\top$. We use $P_k$ to represent the factor loading space of $A_k$.''',[6],[1],[r'P_k=P_{A_k}',r'U_kU_k^\top'],'Projection onto the full-column-rank loading matrix. The lower-bound theorems explicitly bind P_k=U_k U_k^T for their own orthonormal U, so do not import the whole general model by that equality alone.','Section 2.2 — Orthogonal projection (2.2)')
add(9,'lagged sample cross product',r'''\[
\widehat\Sigma_h=\widehat\Sigma_h(\mathcal X_{1:T})=\sum_{t=h+1}^T\frac{\mathcal X_{t-h}\otimes\mathcal X_t}{T-h}\in\mathbb R^{d_1\times\cdots\times d_K\times d_1\times\cdots\times d_K}
\]
(2.3)
is an order-$2K$ tensor.''',[6],[4],[r'\widehat\Sigma_h(\mathcal X_{1:T})'],'Uncentered lagged outer-product average; no mean subtraction is inserted. The formula defines an operator on the supplied tensor series, independent of a particular factor model.','Section 2.2 — Lagged sample cross product (2.3)',context='our estimator is based on the tensor version of the lagged sample cross product')
add(10,'TOPUP',r'''Let $\widehat\Sigma_h$ be the sample autocovariance of the data $\mathcal X_{1:T}=(\mathcal X_1,\ldots,\mathcal X_T)$ as in (2.3). Define
\[
\mathrm{TOPUP}_k=\left(\operatorname{mat}_k(\widehat\Sigma_h),\ h=1,\ldots,h_0\right),
\]
(2.4)
as a $d_k\times(dd_{-k}h_0)$ matrix, where $d=\prod_{k=1}^K d_k$, $d_{-k}=d/d_k$ and $h_0$ is a predetermined positive integer.''',[7],[3,9],[r'\mathrm{TOPUP}_k'],'Horizontal lag concatenation of mode-k unfoldings of the full order-2K sample product; h0 is positive and predetermined. The truncated-SVD estimator is a separate source passage.','Section 2.3 — TOPUP matrix (2.4)',context='The TOPUP method performs SVD of (2.4) to obtain the truncated left singular matrices')
add(11,'left singular matrix',r'''where $\mathrm{LSVD}_m$ stands for the left singular matrix composed of the first $m$ left singular vectors corresponding to the largest $m$ singular values.''',[7],[],[r'\mathrm{LSVD}_m'],'Truncated left singular-vector operator with the printed descending-value convention; tie selection is not specified.','Section 2.3 — LSVD operator')
add(12,'TIPUP',r'''Similar to (2.4), define a $d_k\times(d_kh_0)$ matrix as
\[
\mathrm{TIPUP}_k=\left(\sum_{t=h+1}^T\frac{\operatorname{mat}_k(\mathcal X_{t-h})\operatorname{mat}_k^\top(\mathcal X_t)}{T-h},\ h=1,\ldots,h_0\right),
\]
(2.7)
which replaces the tensor product by the inner product through (2.3) in (2.4).''',[7],[3],[r'\mathrm{TIPUP}_k'],'Matrix-valued lagged cross product; its comparison with TOPUP describes construction but does not require evaluating the outer-product operator. No mean subtraction is inserted.','Section 2.3 — TIPUP matrix (2.7)',context='The TIPUP method performs SVD:')
add(13,'generic iterative algorithm',r'''1: Input: $\mathcal X_t\in\mathbb R^{d_1\times\cdots\times d_K}$ for $t=1,\ldots,T$, $r_k$ for all $k=1,..,K$, the tolerance parameter $\epsilon>0$, the maximum number of iterations $J$, and the $\widehat U_k$-INIT and $\widehat U_k$-ITER operators.

2: Let $j=0$, initiate via applying $\widehat U_k$-INIT on $\{\mathcal X_{1:T}\}$, for $k=1,\ldots,K$, to obtain
\[
\widehat U_k^{(0)}=\widehat U_k\text{-}\mathrm{INIT}_k(\mathcal X_{1:T},r_k).
\]
3: repeat

4: Let $j=j+1$. At the $j$-th iteration, for $k=1,\ldots,K$, given previous estimates $(\widehat U_{k+1}^{(j-1)},\ldots,\widehat U_K^{(j-1)})$ and $(\widehat U_1^{(j)},\ldots,\widehat U_{k-1}^{(j)})$, sequentially calculate,
\[
\mathcal Z_{t,k}^{(j)}=\mathcal X_t\times_1(\widehat U_1^{(j)})^\top\times_2\cdots\times_{k-1}(\widehat U_{k-1}^{(j)})^\top\times_{k+1}(\widehat U_{k+1}^{(j-1)})^\top\times_{k+2}\cdots\times_K(\widehat U_K^{(j-1)})^\top,
\]
for $t=1,\ldots,T$. Perform $\widehat U_k$-ITER on the new tensor time series $\mathcal Z_{1:T,k}^{(j)}=(\mathcal Z_{1,k}^{(j)},\ldots,\mathcal Z_{T,k}^{(j)})$.
\[
\widehat U_k^{(j)}=\widehat U_k\text{-}\mathrm{ITER}_k(\mathcal Z_{1:T,k}^{(j)},r_k).
\]
5: until $j=J$ or
\[
\max_{1\le k\le K}\|\widehat U_k^{(j)}(\widehat U_k^{(j)})^\top-\widehat U_k^{(j-1)}(\widehat U_k^{(j-1)})^\top\|_{\mathrm S}\le\epsilon,
\]
6: Estimate and output:
\[
\widehat U_k^{\mathrm{iFinal}}=\widehat U_k^{(j)},\quad k=1,\ldots,K,
\]
\[
\widehat P_k^{\mathrm{iFinal}}=\widehat U_k^{\mathrm{iFinal}}(\widehat U_k^{\mathrm{iFinal}})^\top,\quad k=1,\ldots,K,
\]
\[
\widehat{\mathcal F}_t^{\mathrm{iFinal}}=\mathcal X_t\times_{k=1}^K(\widehat U_k^{\mathrm{iFinal}})^\top,\quad t=1,\ldots,T,
\]
\[
\widehat{\mathcal E}_t^{\mathrm{iFinal}}=\mathcal X_t-\mathcal X_t\times_1\widehat P_1^{\mathrm{iFinal}}\times_2\cdots\times_K\widehat P_K^{\mathrm{iFinal}},\quad t=1,\ldots,T.
\]''',[8],[2,5],[r'\mathcal Z_{t,k}^{(j)}',r'\widehat U_k^{(j)}'],'Sequential sweep uses current-iteration factors for modes below k and previous-iteration factors above k. Preserve INIT_k/ITER_k repeated k subscripts as printed. Generic operators are inputs; no branch is implicitly selected. All stopping and output lines are retained.','Algorithm 1 — A generic iterative algorithm',kind='source_passage',context='Algorithm 1 A generic iterative algorithm')
add(14,'iTOPUP',r'''When we use the $\widehat U_k$-TOPUP operator (2.5) for both $\widehat U_k$-INIT and $\widehat U_k$-ITER in Algorithm 1, it will be called iTOPUP procedure.''',[7],[13,35],[], 'TOPUP supplies both initialization and each iteration. No TIPUP initialization is silently substituted.','Section 2.3 — iTOPUP procedure',phrases=['iTOPUP'])
add(15,'iTIPUP',r'''Similarly, iTIPUP uses $\widehat U_k$-TIPUP operator (2.8) for both $\widehat U_k$-INIT and $\widehat U_k$-ITER.''',[7],[13,36],[],'TIPUP supplies both initialization and iteration. This is distinct from the mixed procedure.','Section 2.3 — iTIPUP procedure',phrases=['iTIPUP'])
add(16,'TIPUP-iTOPUP',r'''Besides these two versions, we may also use $\widehat U_k$-TIPUP for $\widehat U_k$-INIT and $\widehat U_k$-TOPUP for $\widehat U_k$-ITER, named as TIPUP-iTOPUP.''',[7,8],[13,35,36],[],'TIPUP initializer and TOPUP iterations, as consumed by T3.3. Do not merge this with either unmixed procedure or the reversed TOPUP-iTIPUP branch.','Section 2.3 — TIPUP-iTOPUP procedure',phrases=['TIPUP-iTOPUP'])
add(17,'Notation',r'''Let $\overline{\mathbb E}[\cdot]=\mathbb E[\cdot\mid\{\mathcal F_1,\ldots,\mathcal F_T\}]$.''',[9],[1],[r'\overline{\mathbb E}'],'Conditional expectation given the finite observed factor-process block; not ordinary expectation or expectation over a deterministic signal. Assumption 1 also names conditioning on the whole factor process, which remains a source distinction.','Section 3.1 — Conditional expectation notation',context='3.1. Notation.')
add(18,'error process',r'''The error process $\mathcal E_t$ are independent Gaussian tensors conditionally on the factor process $\{\mathcal F_t,t\in\mathbb Z\}$. In addition, there exists some constant $\sigma>0$, such that
\[
\overline{\mathbb E}(u^\top\operatorname{vec}(\mathcal E_t))^2\le\sigma^2\|u\|_2^2,\quad u\in\mathbb R^d.
\]''',[10],[1,17],[r'\mathcal E_t',r'\overline{\mathbb E}(u^\top\operatorname{vec}(\mathcal E_t))^2'],'Assumption 1 preserves conditional temporal independence, Gaussianity and a uniform second-moment bound. It does not demand independent tensor entries or identity covariance. Core/noise independence is separately in the model prose; no extra stationary factor assumption is added.','Assumption 1',kind='assumption',phrases=['Assumption 1'])
add(19,'order-4 tensors',r'''\[
\Theta_{k,h}=\sum_{t=h+1}^T\frac{\operatorname{mat}_k(\mathcal M_{t-h})\otimes\operatorname{mat}_k(\mathcal M_t)}{T-h}\in\mathbb R^{d_k\times d_{-k}\times d_k\times d_{-k}},
\]
(3.1)''',[9],[1,3,4],[r'\Theta_{k,h}',r'\Theta_{k,0}'],'Signal outer-product tensor with the source mode ordering; h=0 is used in the error rates. The signal M_t and dimension products are archived in auxiliary context.','Section 3.1 — Signal outer-product tensor (3.1)',context='Define order-4 tensors')
add(20,'noiseless version',r'''\[
\Theta^*_{k,h}=\sum_{t=h+1}^T\frac{\operatorname{mat}_k(\mathcal M_{t-h})\operatorname{mat}_k^\top(\mathcal M_t)}{T-h}\in\mathbb R^{d_k\times d_k},
\]
(3.3)''',[9],[1,3],[r'\Theta^*_{k,h}',r'\Theta^*_{k,0}'],'Signal matrix cross product, distinct from the outer-product tensor Theta. The naming context describes the lag-concatenated family of these matrices.','Section 3.1 — Signal inner-product matrix (3.3)',context=r'The noiseless version of (2.7) is',context_page=10)
add(21,'signal strength',r'''Let $\tau_{k,m}$ be the $m$-th singular value of the noiseless version of the $\mathrm{TOPUP}_k$ matrix,
\[
\tau_{k,m}=\sigma_m\left(\overline{\mathbb E}[\mathrm{TOPUP}_k]\right)=\sigma_m\left(\operatorname{mat}_1(\Theta_{k,1:h_0})\right)=\sigma_m\left(\operatorname{mat}_1(\Phi_{k,1:h_0}^{(cano)})\right).
\]
The signal strength for iTOPUP can be characterized as
\[
\lambda_k=\sqrt{h_0^{-1/2}\tau_{k,r_k}}.
\]
(3.5)''',[10],[3,10,17,19,33],[r'\lambda_k',r'\tau_{k,r_k}'],'Square root of h0^(-1/2) times the rkth singular value, not the singular value itself. Preserve all three equal source representations; lag concatenation is auxiliary notation.','Section 3.1 — iTOPUP signal strength (3.5)')
add(22,'signal strength',r'''Similarly, let
\[
\tau^*_{k,m}=\sigma_m(\overline{\mathbb E}(\mathrm{TIPUP}_k))=\sigma_m\left(\Theta^*_{k,1:h_0}\right)=\sigma_m\left(\Phi_k^{*(cano)}{}_{,1:h_0}\right).
\]
The signal strength for iTIPUP can be characterized as
\[
\lambda_k^*=\sqrt{h_0^{-1/2}\tau^*_{k,r_k}}.
\]
(3.6)''',[10],[12,17,20,34],[r'\lambda_k^*',r'\tau^*_{k,r_k}'],'Starred signal strength from TIPUP, potentially affected by signal cancellation. It is not identified with the unstarred strength.','Section 3.1 — iTIPUP signal strength (3.6)')
# Equivalent subscript placement is normalized consistently without changing the indexed object.
members['D22']['statement_original']=members['D22']['statement_original'].replace(r'\Phi_k^{*(cano)}{}_{,1:h_0}',r'\Phi_{k,1:h_0}^{*(cano)}')
add(23,'risk',r'''\[
R_k^{(0)}=\lambda_k^{-2}\sigma T^{-1/2}\left\{\sqrt{d_kd_{-k}r_{-k}}\|\Theta^*_{k,0}\|_{\mathrm S}^{1/2}+\left(\sqrt{d_k}+\sqrt{d_{-k}r}\right)\|\Theta_{k,0}\|_{\mathrm{op}}^{1/2}+\sigma\sqrt{d_k}d_{-k}+\sigma d_k\sqrt{d_{-k}}T^{-1/2}\right\},
\]
(3.7)
where $d_{-k}=\prod_{j\ne k}d_j$ and $r_{-k}=\prod_{j\ne k}r_j$.''',[10],[5,7,19,20,21],[r'R_k^{(0)}'],'Initial TOPUP risk-bound expression with unreduced ambient dimensions. The preceding citation is justification of a bound, not an extra theorem-statement assumption.','Section 3.2 — TOPUP initial rate (3.7)',context=r'the risk $\overline{\mathbb E}[\|\widehat U_k^{(0)}\widehat U_k^{(0)\top}-U_kU_k^\top\|_{\mathrm S}]$ of the TOPUP estimator for $U_k$, the initialization of iTOPUP, is no larger than a constant times')
add(24,'TOPUP',r'''Define
\[
\mathscr R_{k2}=\lambda_k^{-2}\sigma T^{-1/2}\left\{\sqrt{r_k}r_{-k}\|\Theta^*_{k,0}\|_{\mathrm S}^{1/2}+\left(\sqrt{d_k}+\sqrt{rr_{-k}}\right)\|\Theta_{k,0}\|_{\mathrm{op}}^{1/2}+\sigma(\sqrt{d_k}+\sqrt{rr_{-k}})+\sigma\sqrt{d_k}rT^{-1/2}\right\},
\]
(3.8)
\[
R_k^{(TOPUP)}=\mathscr R_{k2}+(R_k^{(0)})^2.
\]
(3.9)''',[11],[5,7,19,20,21,23],[r'\mathscr R_{k2}',r'R_k^{(TOPUP)}'],'Sharper bound’s defining expressions excerpted from Proposition 3.1. Its asymptotic small-initial-error premise belongs to the proposition guarantee, not to these definitions or automatically to T3.1.','Proposition 3.1 — Rate definitions (3.8)–(3.9)',kind='source_passage',context='provides a sharper bound for the TOPUP estimator as follows.',context_page=10)
add(25,'rate',r'''\[
R_k^{(ideal)}=\mathscr R_{k2}+\mathscr R_{k1}^2,
\]
(3.10)
by replacing all $d_j$ in $R_k^{(0)}$ with $r_j$, $j\ne k$, where
\[
\mathscr R_{k1}=\lambda_k^{-2}\sigma T^{-1/2}\left\{\sqrt{d_k}r_{-k}\|\Theta^*_{k,0}\|_{\mathrm S}^{1/2}+\left(\sqrt{d_k}+\sqrt{r_{-k}r}\right)\|\Theta_{k,0}\|_{\mathrm{op}}^{1/2}+\sigma\sqrt{d_k}r_{-k}+\sigma d_k\sqrt{r_{-k}}T^{-1/2}\right\}.
\]''',[11],[5,7,19,20,21,23,24],[r'R_k^{(ideal)}',r'\mathscr R_{k1}'],'Ideal TOPUP error expression; preserve the squared Rcal_k1 term and Rcal_k2, rather than using the unsquared starred expression. R0 is explicitly used to describe the dimension substitution.','Section 3.2 — Ideal TOPUP rate (3.10)',context='this would reduce the rate given in (3.7) and (3.9) to')
add(26,'additional error term',r'''However, because the iteration uses the estimated $U_j,j\ne k$, of total dimension $d^*_{-k}=\sum_{j\ne k}d_jr_j$, our analysis also involves the following additional error term,
\[
R_k^{(add)}=\lambda_k^{-2}\sigma^2T^{-1}\left(d^*_{-k}+\sqrt{d^*_{-k}d_kr_{-k}}\right).
\]
(3.11)''',[11],[8,21],[r'R_k^{(add)}',r'd^*_{-k}=\sum_{j\ne k}d_jr_j'],'Extra TOPUP iteration cost with dstar a sum of dj rj, not their product. The Uj reference identifies loading subspaces; it does not invoke an algorithmic risk theorem.','Section 3.2 — Additional TOPUP error (3.11)')
add(27,'TIPUP risk',r'''\[
\overline{\mathbb E}[\|\widehat P_k^{(TIPUP)}-P_k\|_{\mathrm S}]\lesssim R_k^{*(0)}=(\lambda_k^*)^{-2}\sigma T^{-1/2}\sqrt{d_k}\left(\|\Theta^*_{k,0}\|_{\mathrm S}^{1/2}+\sigma\sqrt{d_{-k}}\right)
\]
(3.16)
with $d_{-k}=\prod_{j\ne k}d_j$''',[12],[5,8,17,20,22,36],[r'R_k^{*(0)}'],'Preserve the full displayed risk inequality containing the rate definition. The initial TIPUP projection is defined through its truncated-SVD operator; the cited bound is not imported as a new assumption.','Section 3.2 — Initial TIPUP risk (3.16)',kind='source_passage',context='the TIPUP risk in the estimation of $P_k$ is bounded by')
add(28,'ideal rate',r'''\[
R_k^{*(ideal)}=(\lambda_k^*)^{-2}\sigma T^{-1/2}\sqrt{d_k}\left(\|\Theta^*_{k,0}\|_{\mathrm S}^{1/2}+\sigma\sqrt{r_{-k}}\right)
\]
(3.17)''',[12],[5,20,22],[r'R_k^{*(ideal)}'],'Starred ideal expression replaces d_-k by r_-k inside the noise term, with no squared rate correction.','Section 3.2 — Ideal TIPUP rate (3.17)',context='the aim of iTIPUP is to achieve the ideal rate')
add(29,'additional error term',r'''\[
R_k^{*(add)}=\sqrt{d^*_{-k}/d_k}R_k^{*(ideal)}.
\]
(3.18)''',[13],[28],[r'R_k^{*(add)}'],'Starred extra cost is a multiplicative dimension factor times the starred ideal rate. The dstar definition is separately archived so this does not depend on the unstarred Radd rate.','Section 3.2 — Additional TIPUP error (3.18)',context='our error bound for iTIPUP involves the additional error term')
add(30,'Hypergraphic Planted Clique',r'''An $m$-hypergraph $G=(V(G),E(G))$ is a natural extension of regular graph, where $V(G)=[N]$ and each hyper-edge is represented by an unordered group of $m$ different vertices $i_j\in V(G)$ $(j=1,\ldots,m)$, denoted as $e=(i_1,\ldots,i_m)\in E(G)$. Given a $m$-hypergraph its adjacency tensor $\mathcal A\in\{0,1\}^{N\times N\times\cdots\times N}$ is defined as
\[
\mathcal A_{i_1,\ldots,i_m}=\begin{cases}1,&\text{if }e=(i_1,\ldots,i_m)\in E(G);\\0,&\text{otherwise}.\end{cases}
\]
We denote by $\mathcal G_m(N,1/2)$ the Erdős–Rényi $m$-hypergraph on $N$ vertices where each hyper-edge $e$ is drawn independently with probability $1/2$, by $C=C(N,\kappa)$ a random clique of size $\kappa$ where the $\kappa$ members are uniformly sampled from $[N]$ and $E(C)$ is composed of all $e=(i_1,\ldots,i_m)$ with $i_j\in C$, and by $\mathcal G_m(N,1/2,\kappa)$ the random graph generated by first sampling independently $\mathcal G_m(N,1/2)$ and $C=C(N,\kappa)$ and then adding all the edges in $E(C)$ to the set of edges in $\mathcal G_m(N,1/2)$. The Hypergraphic Planted Clique (HPC) detection problem of parameter $(N,\kappa,m)$ refers to testing the following hypotheses:
\[
H_0^G:\mathcal A\sim \mathcal G_m(N,1/2)\qquad\text{v.s.}\qquad H_1^G:\mathcal A\sim \mathcal G_m(N,1/2,\kappa).
\]
(3.32)''',[21],[],[r'\mathcal G_m(N,1/2,\kappa)',r'H_0^G',r'H_1^G'],'Independent unordered hyperedges, distinct vertices and a uniformly planted clique. The symmetric adjacency tensor does not have iid ordered entries.','Section 3.6 — Hypergraphic Planted Clique detection')
add(31,'HPC detection',r'''Consider the HPC detection problem (3.32) and suppose $m\ge2$ is a fixed integer. If
\[
\limsup_{N\to\infty}\frac{\log\kappa}{\log N}\le\frac12-\delta,\quad\text{for any }\delta>0,
\]
(3.33)
for any sequence of polynomial-time tests $\{\psi\}_N:\mathcal A\to\{0,1\}$,
\[
\limsup_{N\to\infty}\left(\mathbb P_{H_0^G}(\psi(\mathcal A)=1)+\mathbb P_{H_1^G}(\psi(\mathcal A)=0)\right)>1/2.
\]''',[22],[30],[r'\mathbb P_{H_0^G}',r'\frac{\log\kappa}{\log N}'],'Source computational hardness hypothesis with limsup and strict risk threshold. Preserve its printed any-delta wording; T3.4 calls the hypothesis for some delta in (0,1/2).','Hypothesis I — HPC detection',kind='assumption',phrases=['Hypothesis I'])
add(32,'probability space',r'''For simplicity, we especially consider the factor model (1.2) with each individual series of $\mathcal F_t$ being mean 0 and independent,
\[
\mathcal X_t=\lambda\mathcal F_t\times_1 U_1\times_2\ldots\times_K U_K+\mathcal E_t,
\]
(3.34)
where $U_k\in\mathbb R^{d_k\times r_k}$, $U_k^\top U_k=I$ for $1\le k\le K$, and $0<c_1\le\sigma_{\min}(\mathbb E\operatorname{vec}(\mathcal F_t)\operatorname{vec}^\top(\mathcal F_t))\le\sigma_{\max}(\mathbb E\operatorname{vec}(\mathcal F_t)\operatorname{vec}^\top(\mathcal F_t))\le c_2<\infty$. The probability space we consider in this section is
\[
\mathscr P(T,d_1,\ldots,d_K,\lambda)=\big\{\mathcal X_1,\ldots,\mathcal X_T:\mathcal X_t\text{ has form (3.34) with independent series }\mathcal F_{t,i_1,\ldots,i_K},
\]
\[
\frac1{T-1}\sum_{t=2}^T\mathbb E\mathcal F_{t,i_1,\ldots,i_K}\mathcal F_{t-1,i_1,\ldots,i_K}=c_0>0,\ \text{and }\{\mathcal F_t\}_{t=1}^T\text{ independent of }\{\mathcal E_t\}_{t=1}^T,
\]
\[
\mathcal E_{t,j_1,\ldots,j_K}\overset{\mathrm{i.i.d.}}\sim N(0,\sigma^2),\ \text{for all }1\le t\le T,1\le i_k\le r_k,1\le j_k\le d_k,1\le k\le K\big\}.
\]
(3.35)''',[22],[2], [r'\mathscr P(T,d_1,\ldots,d_K,\lambda)',r'c_0>0'],'Original lower-bound distribution class and its immediate model conditions. Independent factor component series may be serially dependent; the positive lag-one moment rules out temporal independence with zero means. The iid Gaussian entry condition is explicit here and is not a replacement for general Assumption 1. The notation sigma_min means smallest nontrivial singular value by the source convention; preserve that ambiguity.','Section 3.6 — Lower-bound model and probability space (3.34)–(3.35)',kind='source_passage')
add(33,'canonical version',r'''\[
\Phi_{k,h}^{(cano)}=\sum_{t=h+1}^T\frac{\operatorname{mat}_k(\mathcal M_{t-h}\times_{k=1}^K U_k^\top)\otimes\operatorname{mat}_k(\mathcal M_t\times_{k=1}^K U_k^\top)}{T-h}\in\mathbb R^{r_k\times r_{-k}\times r_k\times r_{-k}},
\]
with $U_k$ from the SVD $A_k=U_k\Lambda_kV_k^\top$. We view $\Phi_{k,h}^{(cano)}$ as the canonical version of the auto-covariance of the factor process.''',[9],[1,2,3,4,8],[r'\Phi_{k,h}^{(cano)}'],'Canonical signal outer-product representation using orthonormal loading coordinates. The reused k as a mode-product index is retained. It is distinct from the raw factor Phi unless loadings have been absorbed.','Section 3.1 — Canonical outer-product tensor')
add(34,'canonical factor version',r'''\[
\Phi_{k,h}^{*(cano)}=U_k^\top\Theta^*_{k,h}U_k=\sum_{t=h+1}^T\frac{\operatorname{mat}_k(\mathcal M_{t-h}\times_{k=1}^K U_k^\top)\operatorname{mat}_k^\top(\mathcal M_t\times_{k=1}^K U_k^\top)}{T-h}\in\mathbb R^{r_k\times r_k}.
\]''',[9,10],[1,2,3,8,20],[r'\Phi_{k,h}^{*(cano)}'],'Preserve both printed equal representations of the canonical inner-product matrix. The equality uses the signal lying in all loading spaces; it must not be extended to arbitrary noisy data tensors.','Section 3.1 — Canonical inner-product matrix',context=r'and its canonical factor version is $\Phi_{k,1:h_0}^{*(cano)}=(\Phi_{k,h}^{*(cano)},h=1,\ldots,h_0)$',context_page=10)
add(35,'TOPUP method',r'''The TOPUP method performs SVD of (2.4) to obtain the truncated left singular matrices
\[
\widehat U_k\text{-}\mathrm{TOPUP}(\mathcal X_{1:T},m)=\mathrm{LSVD}_m\left(\operatorname{mat}_k(\widehat\Sigma_h(\mathcal X_{1:T})),\ h=1,\ldots,h_0\right),
\]
(2.5)''',[7],[3,9,10,11],[r'\widehat U_k\text{-}\mathrm{TOPUP}(\mathcal X_{1:T},m)'],'Truncated-SVD TOPUP operator with lag-matrix construction referenced explicitly by (2.4); the requested m is an input, specialized to rk in Algorithm 1.','Section 2.3 — TOPUP estimator (2.5)')
add(36,'TIPUP method',r'''The TIPUP method performs SVD:
\[
\widehat U_k\text{-}\mathrm{TIPUP}(\mathcal X_{1:T},m)=\mathrm{LSVD}_m\left(\sum_{t=h+1}^T\frac{\operatorname{mat}_k(\mathcal X_{t-h})\operatorname{mat}_k^\top(\mathcal X_t)}{T-h},\ h=1,\ldots,h_0\right),
\]
(2.8)
for $k=1,\ldots,K$. Again, $\widehat U_k$-TIPUP is treated as an operator.''',[7],[3,11],[r'\widehat U_k\text{-}\mathrm{TIPUP}(\mathcal X_{1:T},m)'],'Original self-contained inner-product/SVD operator; its full formula is recorded without requiring the separate matrix name TOPUP or a model-specific signal.','Section 2.3 — TIPUP estimator (2.8)')

# Theorems consume these rate definitions, not the preceding proposition/risk guarantees.
full24=members['D24']['statement_original']
r2,rtopup=full24.split('(3.8)',1)
add(37,'TOPUP',r2.strip()+'\n(3.8)',[11],[5,7,19,20,21],[r'\mathscr R_{k2}'],'Auxiliary Rcal_k2 term from Proposition 3.1; retain its full defining expression without importing the proposition conclusion or the separately defined R_TOPUP.','Proposition 3.1 — Auxiliary rate (3.8)',kind='source_passage',context='provides a sharper bound for the TOPUP estimator as follows.',context_page=10)
members['D24']['statement_original']=rtopup.strip()
members['D24']['depends_on']=['D23','D37']
members['D24']['highlight_symbols']=[r'R_k^{(TOPUP)}']
members['D24']['local_label']=members['D24']['source_heading']='Proposition 3.1 — TOPUP rate (3.9)'
members['D25']['depends_on']=[x if x!='D24' else 'D37' for x in members['D25']['depends_on']]
m=members['D27'];m['statement_original']=r'\['+'\n'+m['statement_original'].split(r'\lesssim ',1)[1]
m['depends_on']=['D5','D20','D22']
x=next(x for x in interfaces if x['members'][0]['local_id']=='D27')
x['semantic_boundary']=x['type_shape']='Starred initial rate definition from the right-hand side of (3.16). The full risk assertion is auxiliary source context; its estimator does not become a rate-definition dependency.'
m=members['D26'];intro,formula=m['statement_original'].split(r'\[',1)
m['statement_original']=r'$d^*_{-k}=\sum_{j\ne k}d_jr_j$'+'\n'+r'\['+formula
m['depends_on']=['D21'];m['naming_context']=[dict(context_id='D26/name',text=intro.strip(),evidence=m['evidence'])]
x=next(x for x in interfaces if x['members'][0]['local_id']=='D26');x['source_keywords'][0]['context_id']='D26/name'

def main():
    review=json.loads((REVIEW_ROOT/'inventory-review.json').read_text())
    assert review['status']=='complete' and review['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==review['inventory_sha256']
    for m in members.values():
        assert all(x in members for x in m['depends_on'])
        for x in m['highlight_symbols']: assert x in m['statement_original'] or any(x in t for t in STATEMENTS),(m['local_id'],x)
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
