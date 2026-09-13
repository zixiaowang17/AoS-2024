"""Preserve original graphon definitions, models and estimator constructions."""
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
add(1,'sampling process',r'''The sampling process of $A$ is determined as follows: conditioning on $(\xi_1,\ldots,\xi_n)$, for all $1\le i<j\le n$,
\[
A_{ij}=A_{ji}\sim\operatorname{Bern}(M_{ij}),
\]
Conditioning on $(\xi_1,\ldots,\xi_n)$, $A_{ij}$’s are mutually independent across all $1\le i<j\le n$, and we adopt the convention that $A_{ii}=M_{ii}=0$ for all $i\in[n]$.''',[2],[],[r'A_{ij}=A_{ji}\sim\operatorname{Bern}(M_{ij})'],'Conditional independent Bernoulli upper-triangular edges with symmetry and zero diagonal. In fixed-M minimax statements this is the conditional observation kernel with M supplied, without requiring a latent graphon distribution. The separate graphon entry preserves Mij=f(xi_i,xi_j).','Section 1 — Bernoulli sampling in (1)')
add(2,'graphon',r'''Here the sequence $\{\xi_i\}$ are i.i.d. random variables sampled from an unknown distribution $\mathbb P_\xi$ supported on $[0,1]$. A common choice for $\mathbb P_\xi$ is the uniform distribution on $[0,1]$. In this paper, we allow $\mathbb P_\xi$ to be arbitrary so that the model (1) can be studied to its full generality.
The function $f:[0,1]\times[0,1]\mapsto[0,1]$, which is assumed to be symmetric, is called graphon.
$(M_f)_{ij}:=f(\xi_i,\xi_j)$.''',[2],[1],[r'\mathbb P_\xi',r'(M_f)_{ij}:=f(\xi_i,\xi_j)'],'Symmetric bounded graphon sampled at iid latent positions with arbitrary distribution on [0,1]. T4 supremizes over that distribution; the other finite-matrix statements do not assume a particular latent graphon law. Graphon target values matter only off diagonal in the loss.','Section 1 — Graphon, latent positions and target matrix')
add(3,'empirical loss',r'''consider estimating $f$ under the empirical loss:
\[
\ell(\widehat M,M_f):=\frac1{\binom n2}\sum_{1\le i<j\le n}(\widehat M_{ij}-(M_f)_{ij})^2,
\]
(2)
where $\widehat M\in\mathbb R^{n\times n}$''',[2],[],[r'\ell(\widehat M,M_f)',r'\binom n2'],'Off-diagonal mean squared matrix discrepancy, used with either an arbitrary target M or graphon target Mf. This arithmetic loss does not itself require the target to have a latent-position representation. The Mf definition is preserved separately. No diagonal or factor-of-two penalty is added.','Section 1 — Empirical loss (2)')
add(4,'polynomials',r'''Let $\mathbb R[Y]_{\le D}$ denote the space of polynomials $g:\mathbb R^N\to\mathbb R$ of degree at most $D$ of $Y$.''',[7],[],[r'\mathbb R[Y]_{\le D}'],'Real scalar polynomials of total degree at most D in observed coordinates. The binary prior in the surrounding Proposition1 is not a prerequisite of this algebraic class.','Section 2.1 — Polynomial estimator class')
add(5,'polynomial',r'''Here the notation $\widehat M\in\mathbb R[A]_{\le D}^{n\times n}$ means that for all $(i,j)\in[n]\times[n]$, $\widehat M_{ij}$ is a polynomial of $A$ with degree no more than $D$.''',[4],[4],[r'\mathbb R[A]_{\le D}^{n\times n}'],'Entrywise degree-bounded real matrix estimators based on A; no range, symmetry or diagonal constraints are imposed on the estimates in the displayed class. Arbitrary coefficients may depend on fixed model parameters.','Theorem 1 — Matrix polynomial convention',kind='theorem_excerpt')
add(6,'parameter space',r'''We first define the parameter space of interest in SBM,
\[
\mathcal M_k=\left\{M=(M_{ij})\in[0,1]^{n\times n}:M_{ii}=0\text{ for }i\in[n],\ M_{ij}=M_{ji}=Q_{z_iz_j}\text{ for }i\ne j,\text{ for some }Q=Q^\top\in[0,1]^{k\times k},z\in[k]^n\right\}.
\]
(10)''',[8],[],[r'\mathcal M_k',r'Q_{z_iz_j}'],'General symmetric k-class connectivity matrices with zero diagonal. Labels need not use every class and cluster sizes need not be balanced; Q has freely varying entries.','Section 3 — SBM parameter space (10)')
add(7,'special class of SBM models',r'''we introduce a special class of SBM models considered in the community detection literature, denoted by $\mathcal M_{k,p,q}$ $(0\le q<p\le1)$, whose definition is given by
\[
\mathcal M_{k,p,q}=\left\{M=(M_{ij})\in[0,1]^{n\times n}:M_{ii}=0\text{ for }i\in[n],\ M_{ij}=M_{ji}=p\mathbf1(z_i=z_j)+q\mathbf1(z_i\ne z_j)\text{ for }i\ne j\text{ for some }z\in[k]^n\right\}.
\]
(13)''',[9],[],[r'\mathcal M_{k,p,q}',r'p\mathbf1(z_i=z_j)+q\mathbf1(z_i\ne z_j)'],'Two homogeneous connectivity levels with p>q and arbitrary class assignments. Endpoint cases q=0 or p=1 require care in ratio-based SNR statements; no finite convention for division by zero is inserted.','Section 3 — Homogeneous SBM (13)')
add(8,'prior distribution',r'''We consider the following natural prior distribution $\mathbb P_{\mathrm{SBM}(p,q)}$ supported on $\mathcal M_{k,p,q}$. In particular, $M\sim\mathbb P_{\mathrm{SBM}(p,q)}$ can be generated as follows: first, sample $z\in[k]^n$ according to $z_i\overset{\mathrm{i.i.d.}}\sim\operatorname{Unif}\{1,\ldots,k\}$ for all $i\in[n]$; then let $M_{ij}=p\mathbf1(z_i=z_j)+q\mathbf1(z_i\ne z_j)$ for all $1\le i<j\le n$ and $M_{ii}=0$ for all $i\in[n]$.''',[10],[7],[r'\mathbb P_{\mathrm{SBM}(p,q)}',r'z_i\overset{\mathrm{i.i.d.}}\sim\operatorname{Unif}\{1,\ldots,k\}'],'Uniform iid labels induce random and possibly empty communities. This prior is on M; the joint risk also integrates the Bernoulli observation kernel. It is not a uniform distribution on balanced partitions or on distinct matrices.','Section 3 — SBM prior')
add(9,'Low-degree Polynomial Algorithm for SBM Graphon Estimation',r'''1: Input: $A,p,q,k,r,t_1$ and $t_2$.
2: (Fill the diagonal and transform the data) Let $\Lambda\in\mathbb R^{n\times n}$ be a diagonal matrix with i.i.d. $\operatorname{Bern}(p)$ entries on its diagonal and they are independent of $A$; let $\widetilde A=A+\Lambda-q\mathbf1_n\mathbf1_n^\top$.
3: (Power iteration) Generate an independent random matrix $B\in\mathbb R^{p\times r}$ with i.i.d. $N(0,1)$ entries; compute $\widetilde A^{t_1}B$.
4: (Gradient descent) Run $t_2$ iterations of gradient descent (GD) with zero initialization on the objective $\min_{W\in\mathbb R^{r\times n}}\|\widetilde A^{t_1}BW-\widetilde A\|_F^2$, i.e., for $l=0$ to $t_2-1$, compute
\[
W_{l+1}=W_l-\eta B^\top\widetilde A^{t_1}(\widetilde A^{t_1}BW_l-\widetilde A)\quad\text{with }W_0=0.
\]
5: Output: $\widehat M=\widetilde A^{t_1}BW_{t_2}+q\mathbf1_n\mathbf1_n^\top$.''',[12],[],[r'\widetilde A=A+\Lambda-q\mathbf1_n\mathbf1_n^\top',r'W_{l+1}',r'\widehat M=\widetilde A^{t_1}BW_{t_2}'],'Randomized estimator using observed A and independent Bernoulli diagonal/Gaussian sketch. Preserve the printed p-by-r sketch dimension and flag the required n-by-r correction separately. T3 supplies the prior, tuning and sample-size regime; no low-SNR lower-bound premise is imported into the algorithm.','Algorithm 1',context='Algorithm 1 Low-degree Polynomial Algorithm for SBM Graphon Estimation',context_page=12)
add(10,'Hölder norm',r'''Since graphons are symmetric functions, we only need to consider functions on $\mathcal D=\{(x,y)\in[0,1]\times[0,1]:x\ge y\}$. Define the derivative operator by
\[
\nabla_{jk}f(x,y)=\frac{\partial^{j+k}}{(\partial x)^j(\partial y)^k}f(x,y),
\]
and we adopt the convention $\nabla_{00}f(x,y)=f(x,y)$. Given a $\gamma>0$, the Hölder norm of $f$ is defined as
\[
\|f\|_{\mathcal H_\gamma}=\max_{j+k\le\lfloor\gamma\rfloor}\sup_{(x,y)\in\mathcal D}|\nabla_{jk}f(x,y)|+\max_{j+k=\lfloor\gamma\rfloor}\sup_{(x,y)\ne(x',y')\in\mathcal D}\frac{|\nabla_{jk}f(x,y)-\nabla_{jk}f(x',y')|}{(|x-x'|+|y-y'|)^{\gamma-\lfloor\gamma\rfloor}},
\]''',[13],[],[r'\|f\|_{\mathcal H_\gamma}',r'\nabla_{jk}',r'\gamma-\lfloor\gamma\rfloor'],'Printed floor-order derivatives on the lower triangle with l1 coordinate distance and exponent gamma-floor(gamma). At integer gamma this exponent is zero; do not replace it with a Lipschitz derivative convention. Boundary derivatives require the source’s intended smoothness interpretation.','Section 4 — Hölder norm')
add(11,'Hölder class',r'''the Hölder class with smoothness parameter $\gamma>0$ and radius $L>0$ is defined as
\[
\mathcal H_\gamma(L)=\{\|f\|_{\mathcal H_\gamma}\le L:f(x,y)=f(y,x)\text{ for }x\ge y\}.
\]''',[13],[10],[r'\mathcal H_\gamma(L)'],'Symmetric functions with the paper’s particular Hölder norm bounded by L; preserve the printed set-builder shorthand. This class alone does not impose the probability range.','Section 4 — Hölder class')
add(12,'smooth graphon',r'''Finally, the class of smooth graphon of interest is
\[
\mathcal F_\gamma(L)=\{0\le f\le1:f\in\mathcal H_\gamma(L)\}.
\]''',[13],[11],[r'\mathcal F_\gamma(L)'],'Hölder class restricted to probability-valued symmetric functions. T4 further restricts gamma>0.5 and independently quantifies over the latent distribution.','Section 4 — Smooth graphon class')
add(13,'membership matrix',r'''For any $M\in\mathcal M_{k,p,q}$ with $p>q$, there exists a unique $z\in[k]^n$ such that
\[
M_{ij}=p\mathbf1(z_i=z_j)+q\mathbf1(z_i\ne z_j).
\]
We write such $z$ as $z_M$ to emphasize its dependence on $M$. The membership matrix $Z_M$ is defined by: for $i\in[n]$, $(Z_M)_{ii}=0$, for all $i\ne j$,
\[
(Z_M)_{ij}=\mathbf1((z_M)_i=(z_M)_j)=\frac{M_{ij}-q}{p-q}.
\]
(23)''',[15],[7],[r'Z_M',r'\frac{M_{ij}-q}{p-q}'],'Off-diagonal co-membership is well defined despite the source’s incorrect claim of unique numeric labels: label permutations leave M unchanged. The target has zero diagonal and is distinct from an n-by-k one-hot membership matrix.','Section 5 — Membership matrix (23)')
add(14,'loss function',r'''under the following loss function,
\[
\ell(\widehat Z,Z)=\frac1{\binom n2}\sum_{1\le i<j\le n}(\widehat Z_{ij}-Z_{ij})^2.
\]''',[15],[],[r'\ell(\widehat Z,Z)'],'Mean squared off-diagonal co-membership loss. Preserve this source occurrence separately from graphon loss and rectangular loss; it is not label Hamming distance or permutation-optimized misclassification.','Section 5 — Community detection loss')
add(15,'class of probability matrices',r'''Given any $0<\rho<1$, the class of probability matrices is defined as
\[
\mathcal M_{k,\rho}=\left\{M=(M_{ij})\in[0,\rho]^{n\times n}:M_{ii}=0\text{ for }i\in[n],\ M_{ij}=M_{ji}=Q_{z_iz_j}\text{ for }i\ne j,\text{ for some }z\in[k]^n,Q=Q^\top\in[0,\rho]^{k\times k}\right\}.
\]
(26)''',[17],[],[r'\mathcal M_{k,\rho}',r'[0,\rho]^{k\times k}'],'Symmetric k-class matrices bounded by rho, without class-size restrictions. Sparse means a bound on probabilities; T6 adds rho≥c k²/n and its own parameter regime.','Section 6.1 — Sparse SBM class (26)')
add(16,'additive Gaussian noise',r'''We observe $Y=M+E$, where $M\in\mathcal M_{k_1,k_2}$ and $E$ has i.i.d. $N(0,1)$ entries.''',[18],[17],[r'Y=M+E',r'N(0,1)'],'Rectangular Gaussian observation model with unit noise variance. For the prior risk the noise is independent of the signal; the paper does not separately spell out that independence in this sentence.','Section 6.2 — Gaussian observation model',context='Section 6.2 considers the estimation problem under a biclustering structure with additive Gaussian noise, which can be regarded as an extension of the SBM to rectangular matrices.',context_page=17)
add(17,'biclustering structure',r'''Define the following parameter space of rectangular matrices with biclustering structure,
\[
\mathcal M_{k_1,k_2}=\left\{M\in\mathbb R^{n_1\times n_2}:M_{ij}=Q_{z_iz_j}\text{ for some }Q\in\mathbb R^{k_1\times k_2},z_1\in[k_1]^{n_1},z_2\in[k_2]^{n_2}\right\}.
\]''',[18],[],[r'\mathcal M_{k_1,k_2}',r'Q_{z_iz_j}'],'Rectangular block-constant signal with separate row and column labels. The displayed subscripts zi,zj abbreviate the row/column vectors z1,z2; no symmetry, boundedness or missing diagonal is imposed.','Section 6.2 — Biclustering parameter space')
add(18,'biclustering structure',r'''consider a subset of $\mathcal M_{k_1,k_2}$, denoted by $\mathcal M_{k_1,k_2,\lambda}$, whose definition is given by
\[
\mathcal M_{k_1,k_2,\lambda}=\left\{M\in\mathbb R^{n_1\times n_2}:M_{ij}=Q_{z_iz_j}\text{ for some }z_1\in[k_1]^{n_1},z_2\in[k_2]^{n_2},\ Q\in\mathbb R^{k_1\times k_2}\text{ such that }Q_{ii}=\lambda\text{ for all }i\in[k_1\wedge k_2]\text{ and }Q_{ij}=0\text{ otherwise}\right\}.
\]''',[18],[],[r'\mathcal M_{k_1,k_2,\lambda}',r'Q_{ii}=\lambda'],'Diagonal block-level signal of height lambda, with zero off-diagonal block levels. The following prior uses only min(k1,k2) labels on both sides even if the class permits additional labels.','Section 6.2 — Biclustering subset',context='Define the following parameter space of rectangular matrices with biclustering structure,',context_page=18)
add(19,'prior distribution',r'''We also consider a prior distribution $\mathbb P_{\mathrm{BC}(\lambda)}$ supported on $\mathcal M_{k_1,k_2,\lambda}$. The sampling process $M\sim\mathbb P_{\mathrm{BC}(\lambda)}$ is given as follows: first, generate $z_1\in[k_1]^n$, $z_2\in[k_2]^n$ such that $(z_1)_i,(z_2)_j\overset{\mathrm{i.i.d.}}\sim\operatorname{Unif}\{1,\ldots,k_1\wedge k_2\}$ independently for all $i\in[n_1]$ and $j\in[n_2]$; then let $M_{ij}=\lambda\mathbf1((z_1)_i=(z_2)_j)$.''',[18],[18],[r'\mathbb P_{\mathrm{BC}(\lambda)}',r'\operatorname{Unif}\{1,\ldots,k_1\wedge k_2\}'],'Independent row/column labels uniform over the shared min(k1,k2) labels. Preserve the printed n-length vector typo while retaining the explicitly stated n1/n2 coordinate ranges. The prior is on M; Gaussian noise supplies the joint law.','Section 6.2 — Biclustering prior')
add(20,'loss of interest',r'''the loss of interest is $\ell(\widehat M,M)=\frac1{n_1n_2}\sum_{i\in[n_1],j\in[n_2]}(\widehat M_{ij}-M_{ij})^2$.''',[18],[],[r'\frac1{n_1n_2}'],'Squared loss on every entry of the rectangular matrix, with n1*n2 normalization. It includes all coordinates, unlike the graphon and co-membership losses.','Section 6.2 — Rectangular estimation loss')
add(21,'low-degree polynomial algorithms',r'''$\widehat M\in\mathbb R[Y]_{\le D}^{n_1\times n_2}$''',[18],[4],[r'\mathbb R[Y]_{\le D}^{n_1\times n_2}'],'Rectangular matrix of degree-D scalar polynomials in Gaussian observations Y. Same scalar polynomial definition as Section2.1, instantiated to n1*n2 coordinates; no binary observation premise.','Theorem 7 — Rectangular polynomial class',kind='theorem_excerpt',context='The following result gives a lower bound for the class of low-degree polynomial algorithms.',context_page=18)
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D10']['highlight_symbols'] = ['\\|f\\|_{\\mathcal H_\\gamma}', '\\nabla_{jk}', "(|x-x'|+|y-y'|)^{\\gamma-\\lfloor\\gamma\\rfloor}"]

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
