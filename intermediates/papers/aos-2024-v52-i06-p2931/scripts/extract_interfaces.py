"""Preserve original federated-learning models, estimators and assumption source passages."""
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
add(1,'risk function',r'''A typical federated learning (FL) setting involves $K$ clients, and we define $f_k(\cdot;\boldsymbol\xi^k)$ as the loss function specific to the $k$th client and $F_k(\boldsymbol\theta)=\mathbb E_{P_k}(f_k(\boldsymbol\theta;\boldsymbol\xi^k))$ as the corresponding risk function, where $\boldsymbol\xi^k$ is drawn from an unknown distribution $P_k$. We do not assume $\{P_k\}_{k=1}^K$ being identical to accommodate heterogeneity across the clients’ local data distributions. We write $\mathbb E_{P_k}(\cdot)$ as $\mathbb E(\cdot)$ for simplicity.''',[3],[],[r'F_k(\boldsymbol\theta)=\mathbb E_{P_k}(f_k(\boldsymbol\theta;\boldsymbol\xi^k))'],'Original client-specific loss and population expectation under heterogeneous distributions.','Section 2 — Client losses and risks',kind='source_passage')
add(2,'weights',r'''$\{w_k\}_{k=1}^K$ is a set of positive pre-specified weights such that $\sum_{k=1}^Kw_k=1$.

This work assumes that there exist positive constants $b_1$ and $b_2$ such that $b_1\le w_kK\le b_2$ for $1\le k\le K$.''',[3],[],[r'\sum_{k=1}^Kw_k=1',r'b_1\le w_kK\le b_2'],'Original positive balanced client weights, summing to one. Equal weights are an example, not compulsory.','Section 2 — Weight conditions',kind='condition')
add(3,'federated risk function',r'''Define the federated risk function
\[
F(\boldsymbol\theta)=\sum_{k=1}^Kw_kF_k(\boldsymbol\theta),\tag{1}
\]
where $\boldsymbol\theta\in\mathbb R^d$ is the parameter of interest''',[3],[1,2],[r'F(\boldsymbol\theta)='],'Original weighted population risk; not an empirical sample objective.','Section 2 — Federated risk (1)')
add(4,'parameter',r'''The purpose of the FL is to estimate the parameter $\boldsymbol\theta_K^*$ defined as
\[
\boldsymbol\theta_K^*=\operatorname*{argmin}_{\boldsymbol\theta\in\boldsymbol\Phi}F(\boldsymbol\theta),\tag{2}
\]
where the subscript $K$ reflects the dependence on the number of clients and $\boldsymbol\Phi$ is the parameter space.''',[3],[3,5],[r'\boldsymbol\theta_K^*'],'Original federated-risk minimizer, indexed by the potentially growing client count. Do not silently assume it is constant in K.','Section 2 — Target parameter (2)')
add(5,'parameter space',r'''We assume that the parameter space $\boldsymbol\Phi$ is convex and closed, and denote $R_d:=\sup_{\boldsymbol\theta,\boldsymbol\theta'}\|\boldsymbol\theta-\boldsymbol\theta'\|_2<\infty$ as the diameter of $\boldsymbol\Phi$ when it is bounded.''',[4],[],[r'\boldsymbol\Phi',r'R_d'],'Original closed convex parameter space, with finite diameter only in the bounded case.','Section 2 — Parameter space',kind='condition')
add(6,'metric projection operator',r'''By $\mathbb M_{\boldsymbol\Phi}$, we denote the metric projection operator onto the parameter space $\boldsymbol\Phi$, that is, $\mathbb M_{\boldsymbol\Phi}(\boldsymbol x)=\operatorname*{argmin}_{\boldsymbol x'\in\boldsymbol\Phi}\|\boldsymbol x-\boldsymbol x'\|_2$. Note that the metric projection operator is a nonexpanding operator, that is,
\[
\|\mathbb M_{\boldsymbol\Phi}(\boldsymbol x)-\mathbb M_{\boldsymbol\Phi}(\boldsymbol x')\|_2\le\|\boldsymbol x-\boldsymbol x'\|_2\quad\forall\boldsymbol x,\boldsymbol x'\in\mathbb R^d.
\]
We define similarily the matrix form of the metric projection operator $\mathbb M_{\boldsymbol\Phi}$, that is, for $\boldsymbol X=(\boldsymbol x_1,\boldsymbol x_2,\ldots,\boldsymbol x_K)\in\mathbb R^{d\times K}$, $\mathbb M_{\boldsymbol\Phi}(\boldsymbol X)=(\mathbb M_{\boldsymbol\Phi}(\boldsymbol x_1),\mathbb M_{\boldsymbol\Phi}(\boldsymbol x_2),\ldots,\mathbb M_{\boldsymbol\Phi}(\boldsymbol x_K))$.''',[4],[5],[r'\mathbb M_{\boldsymbol\Phi}'],'Original Euclidean projection and its columnwise matrix extension.','Section 2 — Metric projection')
add(7,'spectral and Frobenius norms',r'''Throughout the paper, we use $\|\boldsymbol A\|_2=\sup_{\boldsymbol x\ne0}\|\boldsymbol A\boldsymbol x\|_2/\|\boldsymbol x\|_2$ and $\|\boldsymbol A\|_F=\sqrt{\operatorname{tr}(\boldsymbol A^T\boldsymbol A)}$ to denote the spectral and Frobenius norms of the matrix $\boldsymbol A\in\mathbb R^{K\times K}$, respectively, where $\operatorname{tr}$ is the trace operator. We use $\boldsymbol A\succeq\boldsymbol B$ to show that for symmetric matrices $\boldsymbol A$ and $\boldsymbol B$, $\boldsymbol A-\boldsymbol B$ is semi-positive definite.''',[4],[],[r'\|\boldsymbol A\|_F',r'\|\boldsymbol A\|_2'],'Original matrix norm and PSD-order conventions; vector norms remain Euclidean and later rectangular matrices use the corresponding Frobenius expression.','Section 2 — Matrix norms and order')
add(8,'identity matrix',r'''We denote the $d$-dimensional vector of ones as $\boldsymbol1_d$, and the identity matrix and $d^{-1}\boldsymbol1_d\boldsymbol1_d^T$ by $\boldsymbol I$ and $\boldsymbol J$, respectively.''',[4],[],[r'd^{-1}\boldsymbol1_d\boldsymbol1_d^T',r'\boldsymbol J'],'Original identity/averaging notation as printed. Its d-dimensional J conflicts with right-centering K client columns later; the separate source note records this mismatch.','Section 2 — Identity and averaging matrices')
add(9,'connection matrix',r'''The connection network of the participating clients in the FL system is defined by an undirected graph $G=(V,E)$ where $V=\{v_k\}_{k=1}^K$ represents the set of clients and $E$ specifies the edge set such that $(i,j)\in E$ if and only if clients $i$ and $j$ are connected. We assume that there is a self-loop for each client (node) such that $(i,i)\in E$ for $1\le i\le K$. Let $\boldsymbol C=(c_{ij})\in\mathbb R^{K\times K}$ be a symmetric connection matrix defined on $G=(V,E)$, where $c_{ij}$ is a nonnegative constant that specifies the contribution of the $j$th data block to the estimation at node $i$. It is required that $c_{ij}>0$ if and only if $(i,j)\in E$ and $\sum_{j=1}^Kc_{ij}=1$ for all $i$.''',[4],[],[r'\boldsymbol C=(c_{ij})',r'\sum_{j=1}^Kc_{ij}=1'],'Original nonnegative symmetric row-stochastic client matrix supported exactly on an undirected graph with self-loops. The Metropolis–Hastings rule is an optional example.','Section 2.1 — Connection network and matrix')
add(10,'Assumption 2.1',r'''The $K$-dimensional connection matrix $\boldsymbol C$ satisfies $\boldsymbol C\boldsymbol1=\boldsymbol1$ and $\boldsymbol C^T=\boldsymbol C$ whose largest eigenvalue is $1$ and the absolute values of other eigenvalues are strictly less than $1$, namely $\max\{|\lambda_k(\boldsymbol C)|\mid k=2,3,\ldots,K\}\le\rho<\lambda_1(\boldsymbol C)=1$ for some $0\le\rho<1$, where $\lambda_k(\boldsymbol C)$ denotes the $k$th largest eigenvalue of $\boldsymbol C$.''',[6],[9],[r'\max\{|\lambda_k(\boldsymbol C)|',r'0\le\rho<1'],'Original uniform network spectral contraction; negative eigenvalues are controlled in absolute value and rho=0 is allowed.','Assumption 2.1',kind='assumption',context='Assumption 2.1.',phrases=['Assumption 2.1'])
add(11,'Assumption 2.2',r'''The step sizes $\{\eta_t\}_{t\ge1}$ in the DFL algorithm satisfy $\eta_t=D(t+\gamma)^{-\alpha}$ for some positive constants $D$, $\gamma$, and $1/2<\alpha\le1$.''',[7],[],[r'\eta_t=D(t+\gamma)^{-\alpha}',r'1/2<\alpha\le1'],'Original positive shifted polynomial step-size family, including alpha=1.','Assumption 2.2',kind='assumption',context='Assumption 2.2.',phrases=['Assumption 2.2'])
add(12,'weighted stochastic gradient matrix',r'''Let the local parameter estimate conducted on the $k$th data block at the $t$th step of the algorithm be $\hat{\boldsymbol\theta}_t^k$, the corresponding matrix of estimates of all clients be $\hat{\boldsymbol\Theta}_t=(\hat{\boldsymbol\theta}_t^1,\hat{\boldsymbol\theta}_t^2,\ldots,\hat{\boldsymbol\theta}_t^K)\in\mathbb R^{d\times K}$, the step size be $\eta_t$ and the weighted stochastic gradient matrix be
\[
\hat{\boldsymbol G}_t=K\left(w_1\nabla f_1(\hat{\boldsymbol\theta}_{t-1}^1;\boldsymbol\xi_t^1),w_2\nabla f_2(\hat{\boldsymbol\theta}_{t-1}^2;\boldsymbol\xi_t^2),\ldots,w_K\nabla f_K(\hat{\boldsymbol\theta}_{t-1}^K;\boldsymbol\xi_t^K)\right).\tag{6}
\]''',[5],[1,2],[r'\hat{\boldsymbol G}_t=K',r'\hat{\boldsymbol\Theta}_t'],'Original local-state and weighted gradient matrices. The factor K is part of the update, not an unweighted gradient convention.','Section 2.2 — Estimate and gradient matrices (6)')
add(13,'DFL algorithm',r'''Here for each $k$, $\{\boldsymbol\xi_t^k\}_{t\ge1}$ are drawn independently and sequentially at each step $t$ from the distribution $P_k$. The DFL algorithm (summarized as Algorithm 1 in the SM) proceeds as follows. At $t=0$, all the local estimates are initialized as $\hat{\boldsymbol\theta}_0\in\mathbb R^d$. For $t=1,2,\ldots,T$ and some positive integer $\tau$, if $t$ is divisible by $\tau$, there is a synchronization of the computation results among neighboring nodes according to $\boldsymbol C$, and the parameter estimates are updated as $\hat{\boldsymbol\Theta}_t=\mathbb M_{\boldsymbol\Phi}((\hat{\boldsymbol\Theta}_{t-1}-\eta_t\hat{\boldsymbol G}_t)\boldsymbol C)$; otherwise we update the parameter estimates locally and in parallel by $\hat{\boldsymbol\Theta}_t=\mathbb M_{\boldsymbol\Phi}(\hat{\boldsymbol\Theta}_{t-1}-\eta_t\hat{\boldsymbol G}_t)$.''',[5],[6,9,11,12],[r'\mathbb M_{\boldsymbol\Phi}((\hat{\boldsymbol\Theta}_{t-1}-\eta_t\hat{\boldsymbol G}_t)\boldsymbol C)',r'\hat{\boldsymbol\Theta}_t'],'Original projected decentralized SGD with shared initialization and synchronization every tau steps. All steps are available in the main text; no supplementary algorithm is imported.','Section 2.2 — DFL algorithm')
add(14,'spatial averaging',r'''The first one is the spatial averaging across the $K$ clients at each step:
\[
\hat{\bar{\boldsymbol\theta}}_t=K^{-1}\sum_{k=1}^K\hat{\boldsymbol\theta}_t^k;
\]''',[5],[13],[r'\hat{\bar{\boldsymbol\theta}}_t'],'Original unweighted client average at a single time.','Section 2.2 — Spatial averaging')
add(15,'temporal averaging',r'''the second type is the temporal averaging within a client $k$ for $1\le t\le T$:
\[
\hat{\bar{\boldsymbol\theta}}_T^k=T^{-1}\sum_{t=1}^T\hat{\boldsymbol\theta}_t^k;
\]''',[5],[13],[r'\hat{\bar{\boldsymbol\theta}}_T^k'],'Original time average of one client trajectory; not a spatial average.','Section 2.2 — Temporal averaging')
add(16,'spatial-temporal averaging',r'''and the last type is the spatial-temporal averaging
\[
\hat{\bar{\bar{\boldsymbol\theta}}}_T=(TK)^{-1}\sum_{t=1}^T\sum_{k=1}^K\hat{\boldsymbol\theta}_t^k.
\]''',[5],[14,15],[r'\hat{\bar{\bar{\boldsymbol\theta}}}_T'],'Original PR average of all client/time iterates, unweighted despite weighted local gradient updates.','Section 2.2 — Spatial-temporal PR averaging')
add(17,'Assumption 3.1',r'''There exists nonnegative constants $L_\xi$ and $\sigma^2$, and a positive integer $v$ such that the gradient noise $\boldsymbol\epsilon_k(\boldsymbol\theta;\boldsymbol\xi^k)=\nabla f_k(\boldsymbol\theta;\boldsymbol\xi^k)-\nabla F_k(\boldsymbol\theta)$ satisfies $\mathbb E(\|\boldsymbol\epsilon_k(\boldsymbol\theta;\boldsymbol\xi^k)\|_2^{2s})\le\sigma^{2s}+L_\xi\|\nabla F_k(\boldsymbol\theta)\|_2^{2s}$ for all positive integers $s\le v$, $\boldsymbol\theta\in\boldsymbol\Phi$, and $k=1,2,\ldots,K$.''',[7],[1,5],[r'\boldsymbol\epsilon_k(\boldsymbol\theta;\boldsymbol\xi^k)',r's\le v'],'Original gradient-dependent noise-moment family. Theorems 1–4/6 select v=1; Theorem 5 selects v=2.','Assumption 3.1',kind='assumption',context='Assumption 3.1.',phrases=['Assumption 3.1'])
add(18,'Assumption 3.2',r'''For $k=1,2,\ldots,K$, the objective function $F_k(\cdot)$ is differentiable, convex and $L$-smooth with a positive constant $L$ such that for any $\boldsymbol\theta_1,\boldsymbol\theta_2\in\boldsymbol\Phi$,
\[
0\le F_k(\boldsymbol\theta_1)-F_k(\boldsymbol\theta_2)-\langle\nabla F_k(\boldsymbol\theta_2),\boldsymbol\theta_1-\boldsymbol\theta_2\rangle\le\frac L2\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2^2.\tag{11}
\]''',[7],[1,5,7],[r'\frac L2\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2^2'],'Original population convexity/smoothness sandwich, not stochastic mean-square gradient smoothness.','Assumption 3.2',kind='assumption',context='Assumption 3.2.',phrases=['Assumption 3.2'])
add(19,'Assumption 3.3',r'''There exist nonnegative constants $\kappa$ and $B$ such that $\sum_{k=1}^Kw_k\|\nabla F(\boldsymbol\theta)-\nabla F_k(\boldsymbol\theta)\|_2^2\le\kappa^2$ for any $\boldsymbol\theta\in\boldsymbol\Phi$, and $\|\nabla F_k(\boldsymbol\theta_K^*)\|_2\le B$ for all $1\le k\le K$.''',[8],[1,2,3,4,7],[r'\|\nabla F(\boldsymbol\theta)-\nabla F_k(\boldsymbol\theta)\|_2^2',r'\|\nabla F_k(\boldsymbol\theta_K^*)\|_2\le B'],'Original weighted inter-client gradient heterogeneity and uniform target-gradient bound.','Assumption 3.3',kind='assumption',context='Assumption 3.3.',phrases=['Assumption 3.3'])
add(20,'constants',r'''Under Assumptions 2.1–2.2, 3.1 with $v=1$, and Assumptions 3.2–3.3, there exist two positive constants $B_{\mathrm{MSE}}$ and $B_{\mathrm{CE}}$ such that for all $1\le t\le T$ and $K\ge1$, the following hold regardless of the parameter space $\boldsymbol\Phi$ is bounded by a diameter $R_d<\infty$ or is $\mathbb R^d$:
\[
\mathbb E\left(\|\hat{\bar{\boldsymbol\theta}}_t-\boldsymbol\theta_K^*\|_2^2\right)<B_{\mathrm{MSE}}\quad\text{and}\quad K^{-1}\mathbb E\left(\|\hat{\boldsymbol\Theta}_t(\boldsymbol I-\boldsymbol J)\|_F^2\right)<B_{\mathrm{CE}}.\tag{12}
\]''',[8],[4,8,10,11,13,14,17,18,19,21],[r'B_{\mathrm{MSE}}',r'B_{\mathrm{CE}}'],'Original main-text lemma fixes the two constants explicitly consumed by Theorem 1. Retain as source context, not an additional inventoried Theorem.','Lemma 1 — Uniform bound constants',kind='source_passage')
add(21,'consensus error',r'''First, we establish an upper bound of the consensus error $K^{-1}\sum_{k=1}^K\mathbb E(\|\hat{\boldsymbol\theta}_t^k-\hat{\bar{\boldsymbol\theta}}_t\|_2^2)$ of the DFL algorithm, characterizing the deviation of the local estimators $\{\hat{\boldsymbol\theta}_t^k\}_{k=1}^K$ to their average $\hat{\bar{\boldsymbol\theta}}_t$.''',[7],[7,13,14],[r'K^{-1}\sum_{k=1}^K\mathbb E(\|\hat{\boldsymbol\theta}_t^k-\hat{\bar{\boldsymbol\theta}}_t\|_2^2)'],'Original average squared disagreement, represented by right-centering with J in the theorem. The printed J dimension issue is retained separately.','Section 3 — Consensus error')
add(22,'Assumption 3.4',r'''For all $k=1,2,\ldots,K$, $F_k(\cdot)$ is differentiable and (strongly-)convex, and let $\mu$ be the corresponding largest nonnegative constant such that for any $\boldsymbol\theta_1,\boldsymbol\theta_2\in\mathbb R^d$
\[
\frac\mu2\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2^2\le F_k(\boldsymbol\theta_1)-F_k(\boldsymbol\theta_2)-\langle\nabla F_k(\boldsymbol\theta_2),\boldsymbol\theta_1-\boldsymbol\theta_2\rangle.\tag{14}
\]
If $\mu>0$, the parameter space $\boldsymbol\Phi$ is allowed to be unbounded, for instance, $\mathbb R^d$. If $\mu=0$, $\boldsymbol\Phi$ is required to be bounded with $R_d=\sup_{\boldsymbol\theta_1,\boldsymbol\theta_2\in\boldsymbol\Phi}\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2<\infty$, and the federated objective function $F(\cdot)=\sum_{k=1}^Kw_kF_k(\cdot)$ satisfies a generalized self-concordance property. The latter means that there exist positive constants $\mu_*$ and $B_G$ such that:

(i) $F(\cdot)$ is three-times differentiable, and $\nabla^2F(\boldsymbol\theta_K^*)\succeq\mu_*\boldsymbol I$;

(ii) for any $\boldsymbol\theta_1,\boldsymbol\theta_2\in\boldsymbol\Phi$, $\varphi^{\prime\prime\prime}(t)\le B_G\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2\varphi''(u)$, where $\varphi:u\mapsto F(\boldsymbol\theta_1+u(\boldsymbol\theta_2-\boldsymbol\theta_1))$ for $u\in\mathbb R$;

(iii) $\|\nabla F(\boldsymbol\theta)\|_2\le B_G$ for all $\boldsymbol\theta\in\boldsymbol\Phi$.''',[9,10],[1,3,4,5,7],[r'\frac\mu2',r'\nabla^2F(\boldsymbol\theta_K^*)\succeq\mu_*\boldsymbol I'],'Complete original alternative curvature assumptions. Preserve the printed t/u third-derivative condition and its unresolved quantifier/absolute-value conventions.','Assumption 3.4',kind='assumption',context='Assumption 3.4.',phrases=['Assumption 3.4'])
add(23,'MSE bounds',r'''\[
\mu_{R_d}=\begin{cases}
\left(\frac\mu{2L}+\frac12\right)\mu&\text{if }\mu>0\text{ and}\\
\mu_*^2\left(2L\left(4+\frac{16B_G^2R_d^2}{9}\right)\right)^{-1}&\text{if }\mu=0,
\end{cases}\tag{17}
\]
where $\mu$ and $L$ are defined in (14) and Assumption 3.2, respectively. It also need constants $\mu_*$ and $B_G$ defined in Assumption 3.4 (i) and (ii), respectively.''',[10],[5,18,22],[r'\mu_{R_d}',r'\frac{16B_G^2R_d^2}{9}'],'Original derived curvature constant with separate positive-mu and generalized-self-concordance formulas; not the alternative tilde-mu constant in the later remark.','Section 3.2 — Curvature constant (17)',context='MSE bounds of the DFL sequence.',context_page=9)
add(24,'Assumption 4.1',r'''For $k=1,2,\ldots,K$, the objective function $f_k(\cdot;\cdot)$ is $L$-average smooth with a positive constant $L_a$ such that for any $\boldsymbol\theta_1,\boldsymbol\theta_2\in\boldsymbol\Phi$,
\[
\mathbb E\left(\|\nabla f_k(\boldsymbol\theta_1;\boldsymbol\xi^k)-\nabla f_k(\boldsymbol\theta_2;\boldsymbol\xi^k)\|_2^2\right)\le L_a\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2^2.\tag{20}
\]''',[11],[1,5,7],[r'L_a\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2^2'],'Original mean-square stochastic-gradient smoothness with coefficient L_a, not its square.','Assumption 4.1',kind='assumption',context='Assumption 4.1.',phrases=['Assumption 4.1'])
add(25,'Assumption 4.2',r'''There exist positive constants $\ell_{\mathrm{cov}}$, $\delta$ and $C_e$ such that for all $k=1,2,\ldots,K$, $\boldsymbol S_k=\mathbb E(\boldsymbol\epsilon_k(\boldsymbol\theta_K^*;\boldsymbol\xi^k)\boldsymbol\epsilon_k(\boldsymbol\theta_K^*;\boldsymbol\xi^k)^T)$ satisfies $\boldsymbol S_k\succeq\ell_{\mathrm{cov}}\boldsymbol I$ and $\mathbb E(\|\boldsymbol\epsilon(\boldsymbol\theta_K^*;\boldsymbol\xi^k)\|_2^{2+\delta})<C_e$ for all $K\ge1$, where $\boldsymbol\epsilon(\boldsymbol\theta)=\sqrt K\sum_{k=1}^Kw_k\boldsymbol\epsilon_k(\boldsymbol\theta;\boldsymbol\xi^k)$.''',[12],[2,4,7,17],[r'\boldsymbol S_k\succeq\ell_{\mathrm{cov}}\boldsymbol I',r'\boldsymbol\epsilon(\boldsymbol\theta)=\sqrt K'],'Original client nondegeneracy and aggregated higher-moment condition. Preserve the source mismatch between epsilon(theta) and epsilon(theta;xi^k).','Assumption 4.2',kind='assumption',context='Assumption 4.2.',phrases=['Assumption 4.2'])
add(26,'Assumption 4.3',r'''The federated risk function $F(\boldsymbol\theta)=\sum_{k=1}^Kw_kF_k(\boldsymbol\theta)$ is second-order differentiable with respect to $\boldsymbol\theta\in\boldsymbol\Phi$, and the Hessian matrix $\nabla^2F(\boldsymbol\theta)$ is Lipschitz continuous at $\boldsymbol\theta_K^*$ in the sense that there exists a positive constant $L_H$ such that $\|\nabla^2F(\boldsymbol\theta)-\nabla^2F(\boldsymbol\theta_K^*)\|_2\le L_H\|\boldsymbol\theta-\boldsymbol\theta_K^*\|_2$ for all $\boldsymbol\theta\in\boldsymbol\Phi$ and $K\ge1$.''',[12],[3,4,5,7],[r'\|\nabla^2F(\boldsymbol\theta)-\nabla^2F(\boldsymbol\theta_K^*)\|_2'],'Original population-Hessian regularity, allowing losses themselves not to be twice differentiable.','Assumption 4.3',kind='assumption',context='Assumption 4.3.',phrases=['Assumption 4.3'])
add(27,'population Hessian matrix',r'''where $\boldsymbol H=\nabla^2F(\boldsymbol\theta_K^*)$ is the population Hessian matrix''',[12],[3,4],[r'\boldsymbol H=\nabla^2F(\boldsymbol\theta_K^*)'],'Original Hessian of the aggregate risk at its K-dependent minimizer.','Theorem 3 — Population Hessian',kind='theorem_excerpt')
add(28,'covariance matrix',r'''$\boldsymbol S=\mathbb E(\boldsymbol\epsilon(\boldsymbol\theta_K^*)\boldsymbol\epsilon(\boldsymbol\theta_K^*)^T)$ is the covariance matrix of the aggregated gradient noise, and $\boldsymbol\epsilon(\boldsymbol\theta)$ is defined in Assumption 4.2.''',[12],[25],[r'\boldsymbol S=\mathbb E(\boldsymbol\epsilon(\boldsymbol\theta_K^*)\boldsymbol\epsilon(\boldsymbol\theta_K^*)^T)'],'Original covariance of the square-root-K weighted aggregate noise, not the single-client covariance.','Theorem 3 — Aggregated noise covariance',kind='theorem_excerpt')
add(29,'covariance matrix',r'''\[
\begin{aligned}
\hat{\boldsymbol S}_k={}&\frac1T\sum_{t=0}^{T-1}\nabla f_k(\hat{\boldsymbol\theta}_t^k;\boldsymbol\xi_t^k)\nabla f_k(\hat{\boldsymbol\theta}_t^k;\boldsymbol\xi_t^k)^T\\
&-\frac1{T^2}\left(\sum_{t=0}^{T-1}\nabla f_k(\hat{\boldsymbol\theta}_t^k;\boldsymbol\xi_t^k)\right)\left(\sum_{t=0}^{T-1}\nabla f_k(\hat{\boldsymbol\theta}_t^k;\boldsymbol\xi_t^k)\right)^T.
\end{aligned}\tag{22}
\]''',[13],[1,13],[r'\hat{\boldsymbol S}_k',r'\frac1{T^2}'],'Original centered local gradient-covariance estimate. Preserve the printed t=0 through T-1 data/iterate indexing; no shift is silently supplied.','Section 4.2 — Local covariance estimate (22)',context='One-pass estimation of covariance matrix.',context_page=12)
add(30,'estimator',r'''Then, an estimator of $\boldsymbol S$ can be constructed as
\[
\hat{\boldsymbol S}=K\sum_{k=1}^Kw_k^2\hat{\boldsymbol S}_k.\tag{23}
\]''',[13],[2,28,29],[r'\hat{\boldsymbol S}='],'Original squared-weight aggregation of the centered client covariance estimates.','Section 4.2 — Aggregated covariance estimator (23)')
add(31,'plug-in estimator',r'''When the local objective functions $\{f_k(\cdot;\cdot)\}$ are smooth namely second-order differentiable with respect to $\boldsymbol\theta$, we propose a plug-in estimator as follows. Let $a(\cdot):\mathbb N_+\to\mathbb N_+$ be a nondecreasing function, then the estimators of $\boldsymbol H_k=\nabla^2F_k(\boldsymbol\theta_K^*)$ and $\boldsymbol H$ can be defined as
\[
\hat{\boldsymbol H}_k=\frac1{a(T)}\sum_{s=0}^{a(T)-1}\nabla^2f_k(\hat{\bar{\boldsymbol\theta}}_{T-s-1}^k;\boldsymbol\xi_{T-s}^k)\quad\text{and}\quad\hat{\boldsymbol H}=\sum_{k=1}^Kw_k\hat{\boldsymbol H}_k,\tag{24}
\]
respectively.''',[13],[1,2,15,27],[r'\hat{\boldsymbol H}_k',r'\hat{\boldsymbol H}='],'Original trailing-window Hessian estimator evaluated at client temporal averages. Window bounds and the initial temporal average require source-domain notes.','Section 4.3 — Hessian plug-in estimator (24)')
add(32,'Assumption 4.4',r'''For all $k=1,2,\ldots,K$, we assume that the objective function $f_k(\boldsymbol\theta;\boldsymbol\xi)$ is second-order differentiable with respect to $\boldsymbol\theta\in\boldsymbol\Phi$, and there exists positive constants $\ell_H$ and $H$, such that
\[
\sqrt{\mathbb E\left(\|\nabla^2f_k(\boldsymbol\theta;\boldsymbol\xi^k)-\nabla^2f_k(\boldsymbol\theta_K^*;\boldsymbol\xi^k)\|_2^2\right)}\le\ell_H\|\boldsymbol\theta-\boldsymbol\theta_K^*\|_2
\]
and $\mathbb E(\|\nabla^2f_k(\boldsymbol\theta_K^*;\boldsymbol\xi^k)-\nabla^2F_k(\boldsymbol\theta_K^*)\|_2^2)\le H^2$, where $\boldsymbol\theta\in\boldsymbol\Phi$ and $\boldsymbol\theta_K^*$ is the true value defined in (2).''',[13],[1,4,5,7],[r'\ell_H\|\boldsymbol\theta-\boldsymbol\theta_K^*\|_2'],'Original mean-square stochastic-Hessian regularity and variance bound. The scalar H bound is distinct from the population Hessian matrix bold H.','Assumption 4.4',kind='assumption',context='Assumption 4.4.',phrases=['Assumption 4.4'])
add(33,'confidence region',r'''\[
\hat{\boldsymbol\Sigma}=\hat{\boldsymbol H}^{-1}\hat{\boldsymbol S}\hat{\boldsymbol H}^{-1}.
\]
This theorem is readily useful for the construction of the $1-\beta$ confidence region for $\boldsymbol\theta_K^*$
\[
\{\boldsymbol\theta\mid TK(\hat{\bar{\bar{\boldsymbol\theta}}}_T-\boldsymbol\theta)^T\hat{\boldsymbol\Sigma}^{-1}(\hat{\bar{\bar{\boldsymbol\theta}}}_T-\boldsymbol\theta)\le\chi^2_{d,\beta}\}.\tag{26}
\]''',[14],[16,30,31],[r'\hat{\boldsymbol\Sigma}',r'\chi^2_{d,\beta}'],'Original sandwich estimate and its Wald region. Chi-square upper-tail quantile is bound in the theorem; do not reinterpret as a lower beta-quantile.','Theorem 4 and Section 4.3 — Sandwich confidence region',kind='theorem_excerpt')
add(34,'normalizing constants',r'''\[
C(T,\alpha)=\begin{cases}T^{\alpha-1}&\text{if }\frac12<\alpha<1,\\(\log(T))^{-1}&\text{if }\alpha=1.\end{cases}\tag{29}
\]''',[14],[11],[r'C(T,\alpha)'],'Original regression normalization with distinct polynomial and logarithmic regimes.','Section 5 — Regression normalization (29)',context='which are shown by their respective normalizing constants.',context_page=15)
add(35,'thresholding version',r'''Specifically, for a small $\delta>0$, let the $\boldsymbol\Psi\boldsymbol D\boldsymbol\Psi^T$ be the eigenvalue decomposition of $\boldsymbol V_1$, where $\boldsymbol D=(D_{ij})$ is a nonnegative diagonal matrix. The thresholding version $\tilde{\boldsymbol V}_1$ is
\[
\tilde{\boldsymbol V}_1=\boldsymbol\Psi\tilde{\boldsymbol D}\boldsymbol\Psi^T,\qquad(\tilde D_{jj})=\min\left\{\max\{(D_{jj}),\delta\},\frac1\delta\right\},\tag{30}
\]''',[15],[],[r'\min\left\{\max\{(D_{jj}),\delta\},\frac1\delta\right\}'],'Original spectral clipping rule illustrated for a PSD matrix V_1, then expressly reused for V. Preserve small fixed delta and its unspecified relation to limiting eigenvalues.','Section 5 — Spectral thresholding (30)')
add(36,'constants',r'''First, given a positive constant $\zeta\in(0,1/2)$, we define $r_i(T)$ for $i=1,2,3$ such that $\sum_{i=1}^3r_i(T)=T$. Specifically,
\[
r_1(T)=\begin{cases}\frac T{C_1}&\text{for }\alpha<1,\\\frac{T^{1-\zeta}}{C_2}&\text{for }\alpha=1,\end{cases}\qquad r_2(T)=\frac T{C_3},\quad\text{and}\quad r_3(T)=\frac T{C_4},\tag{31}
\]
where $C_j>1$ for $1\le j\le4$ are constants.''',[15],[11],[r'\sum_{i=1}^3r_i(T)=T',r'r_1(T)'],'Original three-segment allocation, including the incompatible fixed-constant sum condition when alpha=1 and the unstated integer rounding.','Section 5 — Regression time segments (31)')
add(37,'regression-based estimator',r'''Then, the regression-based estimator $\hat{\boldsymbol H}^{\mathrm{reg}}$ for the aggregated Hessian matrix $\boldsymbol H$ is $\hat{\boldsymbol H}^{\mathrm{reg}}=\boldsymbol Z\boldsymbol V^{-1}$, where
\[
\boldsymbol Z=B(T-r_3(T),r_1(T),\alpha)K\sum_{k=1}^Kw_k\boldsymbol Z_k,\qquad\boldsymbol V=B(T,r_1(T),\alpha)\sum_{k=1}^K\boldsymbol V_k.
\]
\[
\boldsymbol Z_k=\sum_{t=r_1(T)+1}^{T-r_3(T)}\left(\nabla f_k(\hat{\boldsymbol\theta}_{t-1}^k;\boldsymbol\xi_t^k)-\left(\frac1{r_3(T)}\sum_{s=T-r_3(T)+1}^T\nabla f_k(\hat{\boldsymbol\theta}_{s-1}^k;\boldsymbol\xi_s^k)\right)\right)(\hat{\boldsymbol\theta}_{t-1}^k-\hat{\bar{\bar{\boldsymbol\theta}}}_{T-1})^T,
\]
\[
\boldsymbol V_k=\sum_{t=r_1(T)+1}^T(\hat{\boldsymbol\theta}_{t-1}^k-\hat{\bar{\bar{\boldsymbol\theta}}}_{T-1})(\hat{\boldsymbol\theta}_{t-1}^k-\hat{\bar{\bar{\boldsymbol\theta}}}_{T-1})^T
\]
and $B(T_1,T_2,\alpha)=(C(T_1,\alpha)^{-1}-C(T_2,\alpha)^{-1})^{-1}$, where $C(T,\alpha)$ is defined in (29).''',[15],[1,2,13,16,27,34,36],[r'\hat{\boldsymbol H}^{\mathrm{reg}}=\boldsymbol Z\boldsymbol V^{-1}',r'B(T_1,T_2,\alpha)'],'Original centered multi-client regression Hessian estimate with separate gradient-centering time segment and unequal Z/V normalizations.','Section 5 — Regression Hessian estimator')
add(38,'thresholding version',r'''Denote $\tilde{\boldsymbol H}^{\mathrm{reg}}=\boldsymbol Z(\tilde{\boldsymbol V})^{-1}$, where $\tilde{\boldsymbol V}$ is the thresholding version of $\boldsymbol V$ according to (30).''',[15],[35,37],[r'\tilde{\boldsymbol H}^{\mathrm{reg}}=\boldsymbol Z(\tilde{\boldsymbol V})^{-1}'],'Original thresholded regression Hessian estimator, the target of Theorem 5. It is not the smooth plug-in Hessian estimator in (24).','Section 5 — Thresholded regression Hessian')
add(39,'one-step estimator',r'''Given the preliminary estimator $\hat{\bar{\bar{\boldsymbol\theta}}}_T$ with $\alpha=1$, the one-step estimator is
\[
\hat{\bar{\bar{\boldsymbol\theta}}}^{\mathrm{os}}_T=\hat{\bar{\bar{\boldsymbol\theta}}}_T-(\hat{\boldsymbol H})^{-1}\frac1T\sum_{t=1}^T\sum_{k=1}^Kw_k\nabla f_k(\hat{\boldsymbol\theta}_{t-1}^k;\boldsymbol\xi_t^k),\tag{33}
\]
where $\hat{\boldsymbol H}$ is an estimator of $\boldsymbol H$ given in (24).''',[16],[1,2,13,16,31],[r'\hat{\bar{\bar{\boldsymbol\theta}}}^{\mathrm{os}}_T',r'\nabla f_k(\hat{\boldsymbol\theta}_{t-1}^k;\boldsymbol\xi_t^k)'],'Original correction of the alpha=1 PR average using stored local stochastic gradients and the specified smooth Hessian estimator. Do not substitute a gradient at the final PR average.','Section 6 — One-step estimator (33)')
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D23']['highlight_symbols'] = ['\\mu_{R_d}', '\\left(2L\\left(4+\\frac{16B_G^2R_d^2}{9}\\right)\\right)^{-1}']

def main():
    r=json.loads((REVIEW_ROOT/'inventory-review.json').read_text());assert r['status']=='complete' and r['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==r['inventory_sha256']
    assert len(interfaces)==len(members)==39
    for x in interfaces:
        m=x['members'][0];assert set(m['depends_on'])<=set(members)
        assert any(v in m['statement_original']+' '+m['local_label'] for v in m['highlight_symbols']+m['highlight_phrases'])
        for ctx in m.get('naming_context',[]):assert not any(ord(ch)<32 and ch!='\n' for ch in ctx['text'])
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved 39 original source entries; full review remains pending.')
if __name__=='__main__':main()
