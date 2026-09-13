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


add('D1','linear parabolic SPDE',r'''
Suppose that $X=(X(t))_{0\le t\le T}$ solves the linear parabolic SPDE
\[
dX(t)=A_\vartheta X(t)dt+dW(t),\qquad0\le t\le T,\tag{1.1}
\]
on an open, bounded and smooth domain $\Lambda\subset\mathbb R^d$ with some initial value $X_0$, a space-time white noise $dW$ and a second order elliptic operator
\[
A_\vartheta=\sum_{i=1}^p\vartheta_i A_i+A_0\tag{1.2}
\]
satisfying zero Dirichlet boundary conditions. The $A_i$ are known differential operators of differential order $n_i\in\{0,1,2\}$ and we aim at recovering the unknown parameter $\vartheta\in\mathbb R^p$.
''',[1],'Introduction — model (1.1)-(1.2)',kind='source_passage',symbols=[r'A_\vartheta',r'\Lambda'],shape='Linear parameter family with fixed known operators and nuisance operator A_0, additive space-time white noise and zero Dirichlet boundary. The initial value is specified separately.')

add('D2','differential order',r'''
Let $\vartheta\in\Theta\subset\mathbb R^p$ be an unknown parameter. For $i=0,\ldots,p$, suppose that the operators in (1.2) are of the form $A_i=\nabla\cdot a^{(i)}\nabla+\nabla\cdot b^{(i)}+c^{(i)}$ for symmetric $a^{(i)}\in\mathbb R^{d\times d}$, $b^{(i)}\in\mathbb R^d$ and $c^{(i)}\in\mathbb R$, where for each $i=1,\ldots,p$ only one of the coefficients $a^{(i)},b^{(i)},c^{(i)}$ is non-vanishing. For each $A_i$, the formal adjoint is $A_i^*=\nabla\cdot a^{(i)}\nabla-\nabla\cdot b^{(i)}+c^{(i)}$, and its differential order $n_i=\operatorname{ord}(A_i)\in\{0,1,2\}$ is the number of non-vanishing derivatives. With $a_\vartheta=\sum_{i=1}^p\vartheta_i a^{(i)}+a^{(0)}$, $b_\vartheta=\sum_{i=1}^p\vartheta_i b^{(i)}+b^{(0)}$ and $c_\vartheta=\sum_{i=1}^p\vartheta_i c^{(i)}+c^{(0)}$, (1.2) gives
\[
A_\vartheta=\nabla\cdot a_\vartheta\nabla+\nabla\cdot b_\vartheta+c_\vartheta.
\]
''',[3],'Section 2.1 — operators, adjoints and differential orders',{'D1':'This specifies the parameter-linear operator family (1.2).'},symbols=[r'n_i=\operatorname{ord}(A_i)',r'A_i^*',r'a_\vartheta'],shape='Constant-coefficient operators homogeneous in differential order for i>=1. A_0 may mix orders. The formal transport adjoint has the opposite sign.')

add('D3','analytic semigroup',r'''
We suppose that $a_\vartheta$ is positive definite for all $\vartheta\in\Theta$. Then $A_\vartheta$ is a strongly elliptic operator and generates with domain $H_0^1(\Lambda)\cap H^2(\Lambda)$ an analytic semigroup $(S_\vartheta(t))_{t\ge0}$ on $L^2(\Lambda)$ [46]. Considered with the same domain, the adjoint $A_\vartheta^*=\sum_{i=1}^p\vartheta_i A_i^*+A_0^*$ generates the adjoint semigroup $(S_\vartheta^*(t))_{t\ge0}$ [62, Section 2.5.3].
''',[3],'Section 2.1 — ellipticity and semigroups',{'D2':'The semigroup generator and positive diffusion matrix are the preceding parameter family.'},kind='condition',symbols=[r'S_\vartheta(t)',r'a_\vartheta'],shape='Pointwise-in-parameter positive definiteness with Dirichlet H2 domain; no uniform parameter-space ellipticity constant or stationarity is added.')

add('D4','process',r'''
With an $\mathcal F_0$-measurable initial value $X_0$ and a cylindrical Wiener process $W$ on $L^2(\Lambda)$ define a process $X=(X(t))_{0\le t\le T}$ by
\[
X(t)=S_\vartheta(t)X_0+\int_0^t S_\vartheta(t-t')\,dW(t'),\qquad0\le t\le T.\tag{2.1}
\]
Due to the low spatial regularity of $W$ this process is understood as a random element with values in $L^2(\Lambda)\subset\mathcal H_1$ almost surely for a larger Hilbert space $\mathcal H_1$ with an embedding $\iota:L^2(\Lambda)\to\mathcal H_1$ such that $\int_0^t\|\iota S_\vartheta(t')\|_{\mathrm{HS}(L^2(\Lambda),\mathcal H_1)}^2dt'<\infty$ [24, Remark 6.6]. Such an embedding always exists.
''',[4],'Section 2.1 — stochastic convolution (2.1)',{'D3':'The convolution and propagated initial value use the elliptic semigroup.'},symbols=[r'X(t)=S_\vartheta(t)X_0',r'\mathcal H_1'],shape='Mild process with potentially rough cylindrical forcing, realized in a larger Hilbert space. The printed assertion about values in L2 subset H1 is preserved, without inferring actual L2-valued paths in all dimensions.')

add('D5','dual pairings',r'''
According to [4, Proposition 2.1] and [40, Lemma 2.4.2] this allows us to extend the dual pairings $\langle X(t),z\rangle_{\mathcal H_1\times\mathcal H_1'}$ to a real-valued Gaussian process $(\langle X(t),z\rangle)_{0\le t\le T,z\in L^2(\Lambda)}$ by
\[
\langle X(t),z\rangle=\langle S_\vartheta(t)X_0,z\rangle+\int_0^t\langle S_\vartheta^*(t-t')z,dW(t')\rangle\tag{2.2}
\]
(the notation $\langle X(t),z\rangle$ is used for convenience and indicates that the process does not depend on the embedding space $\mathcal H_1$).
''',[4],'Section 2.1 — generalized observations (2.2)',{'D4':'The generalized observation pairs the original mild process with an L2 test function.','D3':'The stochastic integral uses the adjoint semigroup.'},symbols=[r'\langle X(t),z\rangle'],shape='Generalized observation rather than an assumed pathwise L2 inner product. The Gaussian description may need conditions on X0; the original F0-measurability assumption alone is not strengthened.')

add('D6','scale and shift operation',r'''
Introduce for $z\in L^2(\mathbb R^d)$ the scale and shift operation
\[
z_{\delta,x}(y)=\delta^{-d/2}z(\delta^{-1}(y-x)),\qquad x,y\in\Lambda,\quad\delta>0.\tag{2.4}
\]
''',[4],'Section 2.2 — scale and shift (2.4)',{'D1':'The shift and evaluation points lie in the original spatial domain.'},symbols=[r'z_{\delta,x}(y)'],shape='L2-preserving spatial scaling, with restricted evaluation on Lambda. It is not an L1-normalized kernel.')

add('D7','point spread function',r'''
Suppose that $K\in H^2(\mathbb R^d)$ is an (unscaled) point spread function with compact support (see Section 5 for concrete examples). Consider locations $x_1,\ldots,x_M\in\Lambda$, $M\in\mathbb N$, and a resolution level $\delta>0$, which is small enough to ensure that the point spread functions $K_{\delta,x_k}$ are supported on $\Lambda$.
''',[4],'Section 2.2 — point spread function and locations',{'D6':'Each local kernel is obtained by the original scale-and-shift operation.'},kind='condition',symbols=[r'K\in H^2(\mathbb R^d)',r'K_{\delta,x_k}'],shape='Compactly supported H2 kernel and shifted supports inside Lambda. Disjointness and a fixed interior compact set are separate assumptions.')

add('D8','Local measurements',r'''
\[
(X_\delta)_k=X_{\delta,k}=(\langle X(t),K_{\delta,x_k}\rangle)_{0\le t\le T},
\]
''',[4],'Section 2.2 — local observation process',{'D5':'The observation is the generalized pairing with the process.','D7':'The test functions are the original localized kernels.'},context=r'Local measurements of $X$ at the locations $x_1,\ldots,x_M$ at resolution $\delta$ correspond to the continuously observed processes',symbols=[r'X_{\delta,k}'],shape='M continuously observed local projections over [0,T], not discrete time samples and not independent processes. The full source channel notation is separated from the derivative channels.')

add('D9','continuously observed processes',r'''
\[
(X_\delta^{A_0})_k=X_{\delta,k}^{A_0}=(\langle X(t),A_0^*K_{\delta,x_k}\rangle)_{0\le t\le T},
\]
\[
(X_\delta^A)_{ik}=X_{\delta,k}^{A_i}=(\langle X(t),A_i^*K_{\delta,x_k}\rangle)_{0\le t\le T}.
\]
''',[4],'Section 2.2 — derivative observation channels',{'D5':'The derivative channels are generalized pairings with X.','D7':'The operators act on the same shifted point spread functions.','D2':'The derivative channels use the formal adjoints of the known operators.'},context=r'Local measurements of $X$ at the locations $x_1,\ldots,x_M$ at resolution $\delta$ correspond to the continuously observed processes',symbols=[r'X_{\delta,k}^{A_i}',r'X_\delta^{A_0}'],shape='Known operator channels, including the A0 nuisance channel. For the lower-bound extension instantiate these at Delta and divergence in b; the adjoint sign is retained.')

add('D10','observed Fisher information',r'''
\[
\mathcal I_\delta=\sum_{k=1}^M\int_0^T X_{\delta,k}^A(t)X_{\delta,k}^A(t)^\top\,dt.\tag{2.7}
\]
''',[5],'Section 2.2 — observed Fisher information (2.7)',{'D9':'The integrand is the outer product of the p derivative-channel vector at each location.'},context='with observed Fisher information',symbols=[r'\mathcal I_\delta'],shape='p-by-p random integrated outer-product matrix, without a kernel-variance divisor in this convention. Invertibility is supplied by H(i), not built into the definition.')

add('D11','augmented MLE',r'''
\[
\widehat\vartheta_\delta=\mathcal I_\delta^{-1}\sum_{k=1}^M\left(\int_0^T X_{\delta,k}^A(t)dX_{\delta,k}(t)-\int_0^T X_{\delta,k}^A(t)X_{\delta,k}^{A_0}(t)dt\right),\tag{2.6}
\]
which we call augmented MLE generalising [2, Section 4.1],
''',[5],'Section 2.2 — augmented MLE (2.6)',{'D10':'The estimator inverts the observed information matrix.','D8':'The stochastic integral is against each local observation.','D9':'It uses the derivative-channel vector and subtracts the known A0 contribution.'},symbols=[r'\widehat\vartheta_\delta'],shape='Original explicit estimator with the known nuisance-operator correction. It is derived from a modified likelihood, not asserted to be the exact likelihood maximizer for independent local diffusions.')

add('D12','scaling coefficients',r'''
We define a diagonal matrix of scaling coefficients $\rho_\delta\in\mathbb R^{p\times p}$,
\[
(\rho_\delta)_{ii}=M^{-1/2}\delta^{n_i-1},\tag{2.10}
\]
''',[6],'Section 2.3 — rate matrix (2.10)',{'D2':'The powers depend on each operator differential order.','D7':'M counts the local measurement locations.'},symbols=[r'(\rho_\delta)_{ii}'],shape='Diagonal rate scaling. The global asymptotic convention permits non-decreasing M(delta), and the information-normalized CLT is distinct from consistency of each parameter.')

add('D13','linearly independent',r'''
The functions $A_iK$ are linearly independent for all $i=1,\ldots,p$.
''',[6],'Assumption H(i)',{'D2':'H(i) applies to the known differential operators.','D7':'The functions are obtained by applying the operators to the unscaled point spread function.'},kind='assumption',symbols=[r'A_iK'],shape='Linear independence of unscaled operator-applied kernels. The printed clause uses A_i, not A_i-star; do not change it.')

add('D14','differential order',r'''
$n_i>1-d/2$ for all $i=1,\ldots,p$.
''',[6],'Assumption H(ii)',{'D2':'n_i is the original differential order.'},kind='assumption',context=r'For each $A_i$, the formal adjoint is $A_i^*=\nabla\cdot a^{(i)}\nabla-\nabla\cdot b^{(i)}+c^{(i)}$, and its differential order $n_i=\operatorname{ord}(A_i)\in\{0,1,2\}$ is the number of non-vanishing derivatives.',context_pages=[3],symbols=[r'n_i>1-d/2'],shape='Strict order-dimension restriction. The boundary-case extension in Section 5 is not inserted into Theorem 2.3.')

add('D15','locations',r'''
The locations $x_k$, $k=1,\ldots,M$, belong to a fixed compact set $\mathcal J\subset\Lambda$, which is independent of $\delta$ and $M$. There exists $\delta'>0$ such that $\operatorname{supp}(K_{\delta,x_k})\cap\operatorname{supp}(K_{\delta,x_l})=\varnothing$ for $k\ne l$ and all $\delta\le\delta'$.
''',[6],'Assumption H(iii)',{'D7':'The condition restricts the original local kernel supports and locations.'},kind='assumption',symbols=[r'\mathcal J'],phrases=['fixed compact set'],shape='Uniform interior compact set and eventual pairwise support disjointness. Independent driving noises do not imply independent observed processes.')

add('D16','initial value',r'''
$\sup_{x\in\mathcal J}\int_0^T\mathbb E[\langle X_0,S_\vartheta^*(t)A_i^*K_{\delta,x}\rangle^2]dt=o(\delta^{2-2n_i})$ for all $i=1,\ldots,p$.
''',[6],'Assumption H(iv)',{'D4':'X0 is the initial value of the mild solution.','D3':'The initial signal is propagated by the adjoint semigroup.','D2':'The adjoint operator and differential order enter the bound.','D6':'The initial signal is tested against the scaled kernel.','D15':'The supremum is over the fixed compact location set.'},kind='assumption',context='The next lemma shows that Assumption H(iv) on the initial value is satisfied in most relevant situations.',symbols=[r'X_0',r'o(\delta^{2-2n_i})'],shape='Uniform little-o negligibility of the propagated initial condition, with expectation and squared pairing. Gaussianity of X0 is not an extra stated condition.')

add('D17','fractional operator',r'''
To this extent, consider the positive operator $-\nabla\cdot a_\vartheta\nabla$ with domain $H^2(\mathbb R^d)$. Its spectral calculus induces for each $s\in\mathbb R$ the fractional operator $(-\nabla\cdot a_\vartheta\nabla)^s$, which acts in the Fourier domain as the multiplication operator with multiplier $\xi\mapsto(-\xi^\top a_\vartheta\xi)^s$, cf. [37] or [18, Chapter VI.5]. By positive definiteness of $a_\vartheta$, this means $(-\nabla\cdot a_\vartheta\nabla)^sz\in L^2(\mathbb R^d)$ as soon as $\xi\mapsto|\xi|^{2s}\mathcal Fz(\xi)\in L^2(\mathbb R^d)$ with the Fourier transform $\mathcal Fz$.
''',[6],'Section 2.3 — whole-space fractional operator',{'D2':'The fractional principal part uses the diffusion matrix a_theta.','D3':'Its positive definiteness is imposed in the setup.'},symbols=[r'(-\nabla\cdot a_\vartheta\nabla)^s'],shape='Whole-space fractional principal part, distinct from the Dirichlet generator. The printed negative Fourier multiplier conflicts with the positive-operator description; preserve and flag it rather than repair it.')

add('D18','negative self-adjoint closed operator',r'''
Suppose that $A$ is an (unbounded) negative self-adjoint closed operator on a Hilbert space $(\mathcal H,\|\cdot\|_{\mathcal H})$ with domain $\mathcal D(A)\subset\mathcal H$ such that $Ae_j=-\lambda_j e_j$ for a non-decreasing sequence $(\lambda_j)_{j\ge1}$ of positive real numbers with $0<\lambda_1\le\lambda_2\le\cdots$ and an orthonormal basis $(e_j)_{j\ge1}$ of $\mathcal H$, and such that $A$ generates a strongly continuous semigroup $(S(t))_{t\ge0}$ on $\mathcal H$ [18].
''',[7],'Section 3 — general spectral generator setup',kind='condition',symbols=[r'Ae_j=-\lambda_j e_j',r'\mathcal D(A)'],shape='General negative self-adjoint generator with a positive spectral gap and orthonormal eigenbasis. It is not assumed to be the potentially nonsymmetric SPDE generator A_theta.')

add('D19','stationary stochastic convolution',r'''
With a cylindrical Wiener process $W$, consider the stationary stochastic convolution
\[
X(t)=\int_{-\infty}^t S(t-t')dW(t'),\qquad t\ge0.\tag{3.1}
\]
As discussed after (2.1) the process $X=(X(t))_{0\le t\le T}$ is understood as a random element with values in $\mathcal H\subset\mathcal H_1$ almost surely for some larger Hilbert space $\mathcal H_1$.
''',[7],'Section 3 — general stationary convolution (3.1)',{'D18':'The semigroup is generated by the general negative self-adjoint operator.'},symbols=[r'X(t)=\int_{-\infty}^t',r'\mathcal H_1'],shape='Stationary convolution from minus infinity, realized in a larger Hilbert space. No arbitrary initial condition or non-self-adjoint transport generator is imported.')

add('D20','RKHS',r'''
Let us introduce some background on the RKHS of a centred Gaussian random variable $Z$, defined on a separable Hilbert space $\mathcal Z$. Its covariance operator $C_Z$ is necessarily positive self-adjoint and trace-class. This means, by the spectral theorem, there exist strictly positive eigenvalues $(\sigma_j^2)_{j\ge1}$ and an associated orthonormal system of eigenvectors $(u_j)_{j\ge1}$ such that $C_Z=\sum_{j\ge1}\sigma_j^2(u_j\otimes u_j)$. Associate with $Z$ (or rather with the induced centred Gaussian measure) the so-called kernel or RKHS $(H_Z,\|\cdot\|_Z)$, where
\[
H_Z=\{h\in\mathcal Z:\|h\|_Z<\infty\},\qquad\|h\|_Z^2=\sum_{j\ge1}\frac{\langle u_j,h\rangle_{\mathcal Z}^2}{\sigma_j^2}\tag{6.8}
\]
(see, e.g., [38, Example 4.2] and also [38, Chapters 4.1 and 4.3] and [22, Chapter 3.6] for other characterizations of the RKHS of a Gaussian measure or process). Alternatively, we have $H_Z=C_Z^{1/2}\mathcal Z$ and $\|h\|_Z=\|C_Z^{-1/2}h\|_{\mathcal Z}$ for $h\in H_Z$.
''',[18],'Section 6.2 — RKHS definition (6.8)',symbols=[r'H_Z',r'C_Z^{1/2}\mathcal Z'],shape='Source covariance-eigenbasis definition and alternative range characterization. With a nontrivial covariance kernel the displayed finite-norm set needs a support convention; this is recorded without editing the original.')

add('D21','Gaussian process',r'''
Next, as in (2.3), consider the Gaussian process $(\langle X(t),z\rangle_{\mathcal H})_{t\ge0,z\in\mathcal H}$, where the ‘inner product’ here corresponds to
\[
\langle X(t),z\rangle_{\mathcal H}=\int_{-\infty}^t\langle S(t-t')z,dW(t')\rangle_{\mathcal H},
\]
''',[7],'Section 3 — generalized stationary observations',{'D19':'The pairing is the generalized observation of the stationary convolution.','D18':'The same semigroup acts on the test vector in the general Hilbert space.'},symbols=[r'\langle X(t),z\rangle_{\mathcal H}'],shape='Generalized Gaussian pairing for all test vectors in H, not an assumption that the cylindrical solution has an ordinary H inner product pathwise.')

add('D22','stationary solution',r'''
Suppose that $\mathbb P_\vartheta$ corresponds to the law of the stationary solution $X$ to the SPDE (1.1) and assume that the following conditions hold:
''',[8],'Assumption L — stationary law',{'D1':'The stationary law is that of the original spatial SPDE.'},kind='assumption',symbols=[r'\mathbb P_\vartheta'],shape='Stationary law for the lower-bound submodels. This is separate from the arbitrary initial condition allowed in the CLT and from the self-adjoint general-Hilbert-space RKHS setup.')

add('D23','kernel function',r'''
The kernel function satisfies $K=\Delta^2\widetilde K$ with $\widetilde K\in C_c^\infty(\mathbb R^d)$.
''',[8],'Assumption L(i)',kind='assumption',symbols=[r'K=\Delta^2\widetilde K'],shape='Smooth compactly supported iterated-Laplacian kernel. In Theorem 4.3 this requirement is applied separately to K, Delta K and (nabla dot b)K.')

add('D24','parameter classes',r'''
The models are $A_\vartheta=\vartheta_1\Delta+\vartheta_2(\nabla\cdot b)+\vartheta_3$ for $\vartheta\in\mathbb R^3$, a fixed unit vector $b\in\mathbb R^d$, and where $\vartheta$ lies in one of the parameter classes
\[
\Theta_1=\{\vartheta=(\vartheta_1,0,0):\vartheta_1\ge1\},
\]
\[
\Theta_2=\{\vartheta=(1,\vartheta_2,0):\vartheta_2\in[0,1]\},
\]
\[
\Theta_3=\{\vartheta=(1,0,\vartheta_3):\vartheta_3\le0\}.
\]
The parameter classes $\Theta_i$ correspond to the cases of estimating the diffusivity $\vartheta_1$, transport coefficient $\vartheta_2$ and reaction coefficient $\vartheta_3$ in front of operators $A_i$ with differential orders $n_1=2$, $n_2=1$, $n_3=0$.
''',[8,9],'Assumption L(ii) and following differential-order identification',{'D1':'These are three one-dimensional submodels of the original SPDE family.'},kind='assumption',symbols=[r'\Theta_1',r'\Theta_2',r'\Theta_3'],shape='One-sided submodels about (1,0,0), with the other coefficients fixed. The explanatory sentence on page 9 is archived after the original clause; intervening L(iii) is stored separately.')

add('D25','δ-separated points',r'''
Let $x_1,\ldots,x_M$ be δ-separated points in $\Lambda$, that is, $|x_k-x_l|>\delta$ for all $1\le k\ne l\le M$. Moreover, suppose that $\operatorname{supp}(K_{\delta,x_k})\subset\Lambda$ for all $k=1,\ldots,M$ and $\operatorname{supp}(K_{\delta,x_k})\cap\operatorname{supp}(K_{\delta,x_l})=\varnothing$ for all $1\le k\ne l\le M$.
''',[9],'Assumption L(iii)',{'D6':'The support conditions use the original scaled kernels.'},kind='assumption',symbols=[r'|x_k-x_l|>\delta'],shape='Strict delta separation plus disjoint kernel supports inside Lambda. This does not impose the fixed interior compact set of H(iii). For Theorem 4.3 check each of the three kernel choices.')


def main():
    for lid,m in members.items():
        assert all(d in members for d in m['depends_on']),lid
        assert any(s in m['statement_original']+' '+m['local_label'] for s in m['highlight_symbols']+m['highlight_phrases']),lid
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages; full source audit remains pending.')

if __name__=='__main__':main()
