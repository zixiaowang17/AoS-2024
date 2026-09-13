"""Preserve original main-text source entries for the nine-occurrence census."""
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
add(1,'Hölder space',r'''For $\eta>0$, $\mathcal X,\mathcal Y$ two subsets of Euclidean spaces and $f=(f_1,\ldots,f_p)\in C^{\lfloor\eta\rfloor}(\mathcal X,\mathcal Y)$ the set of $\lfloor\eta\rfloor:=\max\{k\in\mathbb N_0\mid k\le\eta\}$ times differentiable functions, denote $\partial^\nu f_i=\frac{\partial^{|\nu|}f_i}{\partial x_1^{\nu_1}\ldots\partial x_d^{\nu_d}}$ the partial differential operator for any multi-index $\nu=(\nu_1,\ldots,\nu_d)\in\mathbb N_0^d$ with $|\nu|:=\nu_1+\ldots+\nu_d\le\lfloor\eta\rfloor$. Write $\|f_i\|_{\eta-\lfloor\eta\rfloor}=\sup_{x\ne y}\frac{f_i(x)-f_i(y)}{\min\{1,\|x-y\|^{\eta-\lfloor\eta\rfloor}\}}$ and let
\[
\mathcal H_K^\eta(\mathcal X,\mathcal Y)=\left\{f\in C^{\lfloor\eta\rfloor}(\mathcal X,\mathcal Y)\ \middle|\ \max_i\sum_{|\nu|\le\lfloor\eta\rfloor}\|\partial^\nu f_i\|_{L^\infty(\mathcal X,\mathcal Y)}+\sum_{|\nu|=\lfloor\eta\rfloor}\|\partial^\nu f_i\|_{\eta-\lfloor\eta\rfloor}\le K\right\}
\]
denote the ball of radius $K$ of the Hölder space $\mathcal H^\eta(\mathcal X,\mathcal Y)$, the set of functions $f:\mathcal X\to\mathcal Y$ of regularity $\eta$. To lighten the notation we will write $\mathcal H_1^\gamma$ instead of $\mathcal H_1^\gamma(\mathbb R^p,\mathbb R)$ and $\mathcal H_K^{\beta+1}$ instead of $\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ when the context is clear.''',[4],[],[r'\mathcal H_K^\eta',r'\mathcal H_1^\gamma',r'\mathcal H_K^{\beta+1}'],'Original coordinatewise Hölder ball with the author floor convention and bounded-increment quotient. Preserve the printed placement of max_i and both derivative sums; do not silently impose a different integer-smoothness convention.','Section 2.1 — Hölder space')
add(2,'push forward measure',r'''For a uniform random variable $U\sim\mathcal U([0,1]^d)$ on the $d$-dimensional unit cube and $g\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$, we denote by $g_{\#U}$ the push forward measure of $U$ by $g$, i.e. $\forall f\in\mathcal H_1^0(\mathbb R^p,\mathbb R)$,
\[
\int_{\mathbb R^p}f(x)dg_{\#U}(x):=\int_{[0,1]^d}f(g(u))d\lambda^d(u),
\]
with $\lambda^d$ being the $d$-dimensional Lebesgue measure.''',[4],[1],[r'g_{\#U}',r'\int_{[0,1]^d}f(g(u))d\lambda^d(u)'],'Push-forward of the uniform latent variable, using torus-periodic maps on cube representatives. The source displays H^0 test functions although its preceding Hölder definition starts at eta>0; retain this convention as a source issue.','Section 2.1 — Push forward measure')
add(3,'Integral Probability Metric',r'''Given a known easy-to-sample distribution $\nu$ on a latent space $\mathcal Z$, the generator $\mathcal G\ni g:\mathcal Z\to\mathbb R^p$ approximates $\mu$ by trying to minimize over $\mathcal G$ a certain Integral Probability Metric (IPM) (Müller, 1997):
\[
d_{\mathcal D}(\mu,g_\#\nu):=\sup_{D\in\mathcal D}\mathbb E_\mu[D(X)]-\mathbb E_\nu[D(g(Z))],
\]
(1.1)
where $g_\#\nu$ stands for the pushforward measure of $\nu$ by $g$.''',[2],[],[r'd_{\mathcal D}',r'\sup_{D\in\mathcal D}'],'General discriminator discrepancy for a supplied latent distribution. The author does not put an absolute value in the supremum or assume symmetry of arbitrary D here; it need not be a metric for arbitrary discriminator classes. The general pushforward convention is supplied in this passage.','Section 1 — Integral Probability Metric (1.1)')
add(4,'Hölder Integral Probability Metric',r'''The distance we use to measure discrepancy between two probability measures $\mu,\nu$ on $\mathbb R^p$ is the Hölder Integral Probability Metric (Müller, 1997):
\[
d_{\mathcal H_1^\gamma}(\mu,\nu):=\sup_{D\in\mathcal H_1^\gamma}\mathbb E_{X\sim\mu,Y\sim\nu}[D(X)-D(Y)].
\]
(2.1)''',[5],[1],[r'd_{\mathcal H_1^\gamma}',r'\sup_{D\in\mathcal H_1^\gamma}'],'Unit Hölder-ball IPM. Gamma=1 is comparable to W1 on the stated compact supports, not declared identical to W1; the equivalence constants are retained separately.','Section 2.1 — Hölder Integral Probability Metric (2.1)')
add(5,'GAN estimator',r'''As the Wasserstein GAN (Arjovsky et al., 2017) approach has been proven to be easily implementable and provide state-of-the-art results in various field, we focus in this paper on the GAN estimator
\[
\widehat g\in\operatorname*{arg\,min}_{g\in\mathcal G}\sup_{D\in\mathcal D}\frac1n\sum_{i=1}^nD(X_i)-D(g(U_i))
\]
(1.3)
for $U_i\sim\mathcal U([0,1]^d)$ i.i.d., $\mathcal G\subset\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ and $\mathcal D\subset\mathcal H_1^\gamma(\mathbb R^p,\mathbb R)$ with $\gamma\in[1,\beta+1]$. The estimator $\widehat g$ is to be understood as an empirical approximation of the solution of (1.2) based on the data $X_1,\ldots,X_n$. The probability measure $\widehat g_{\#U}$ is then naturally our estimator of the target $g^\star_{\#U}$.''',[3],[1,2],[r'\widehat g',r'\operatorname*{arg\,min}_{g\in\mathcal G}',r'D(g(U_i))'],'Empirical generator/discriminator optimization over supplied classes and uniform latent sample. Preserve the source summation typography and exact argmin without inventing a measurable selection or approximate optimizer. Later specified generator classes are instantiated by the theorem, not baked into this generic estimator.','Section 1 — GAN estimator (1.3)')
add(6,'general low dimensional model',r'''There exists $g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ such that the target measure $\mu$ verifies $\mu=g^\star_{\#U}$.''',[5],[1,2],[r'g^\star\in\mathcal H_K^{\beta+1}',r'\mu=g^\star_{\#U}'],'Model 1: general smooth torus pushforward, allowing atoms and irregular image support. No manifold or density regularity condition is added.','Model 1',kind='assumption',context='2.2.1. A (too) general low dimensional model.')
add(7,'reach',r'''For a $d$-dimensional submanifold $\mathcal M$ of $\mathbb R^p$ and $\epsilon>0$, we denote by $\mathcal M^\epsilon:=\{x\in\mathbb R^p\mid d(x,\mathcal M)<\epsilon\}$ the set of points such that their distance to the manifold $d(x,\mathcal M):=\inf_{y\in\mathcal M}\|x-y\|$, is less than $\epsilon$. The reach $r_{\mathcal M}$ (Federer, 1959) of $\mathcal M$ corresponds to the largest $\epsilon\ge0$ such that its orthogonal projection $\pi_{\mathcal M}$ is well defined from $\mathcal M^\epsilon$ to $\mathcal M$.''',[4],[],[r'r_{\mathcal M}',r'\pi_{\mathcal M}',r'\mathcal M^\epsilon'],'Reach via uniqueness of the orthogonal projection on the open tubular neighborhood. Ambient distance is the Euclidean infimum.','Section 2.1 — Reach')
add(8,'manifold regularity condition',r'''Let $g\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$.
i) The map $g$ is said to verify the $K$-manifold regularity condition if it is injective and its image $\mathcal M_g$ is a $d$-dimensional submanifold with reach $r_g$ larger than $K^{-1}$.''',[6],[1,7],[r'\mathcal M_g',r'r_g',r'K^{-1}'],'Part (i) of Definition 2.1. Injectivity, smooth manifold image and strict reach bound. It does not by itself impose the separate lower singular-value condition in part (ii).','Definition 2.1(i) — Manifold regularity condition')
add(9,'density regularity condition',r'''Let $g\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$.
ii) The map $g$ is said to verify the $K$-density regularity condition if the differential of $g$ verifies
\[
\inf_{u\in[0,1]^d}\lambda_{\min}((\nabla g(u))^\top\nabla g(u))^{1/2}\ge K^{-1}.
\]''',[6,7],[1],[r'\lambda_{\min}((\nabla g(u))^\top\nabla g(u))^{1/2}',r'K^{-1}'],'Part (ii) of Definition 2.1, sharing its opening binder. Uniform lower bound on the smallest differential singular value. Theorem 5.1 formal version applies this only to g-star; its overview applies it to both maps.','Definition 2.1(ii) — Density regularity condition')
add(10,'non-degenerate manifold model',r'''There exists $g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ that verifies the $K$-manifold and $K$-density regularity conditions such that the target measure $\mu$ verifies $\mu=g^\star_{\#U}$.''',[7],[1,2,8,9],[r'g^\star',r'\mu=g^\star_{\#U}'],'Model 3: torus pushforward with both distinct regularity requirements. Its stated topology and nonempty-model restriction d<p are retained as supporting context.','Model 3',kind='assumption',context='2.2.3. A non-degenerate manifold model.',context_page=6)
add(11,'approximation error',r'''The approximation error of the class $\mathcal G$ is defined as
\[
\Delta_{\mathcal G}:=\inf_{g\in\mathcal G}d_{\mathcal H_1^\gamma}(g_{\#U},g^\star_{\#U}).
\]
(3.1)''',[10],[2,4],[r'\Delta_{\mathcal G}',r'\inf_{g\in\mathcal G}'],'Generator approximation error at the supplied target, class and IPM regularity. Theorem 5.4 uses its Section-5 regularity; no extra Model-1 generator construction is imported.','Section 3.1.1 — Generator approximation error (3.1)')
add(12,'approximation error',r'''On the other hand, the approximation error of the class $\mathcal D$ is defined as
\[
\Delta_{\mathcal D}:=\sup_{g\in\mathcal G}\{d_{\mathcal H_1^\gamma}(g_{\#U},g^\star_{\#U})-d_{\mathcal D}(g_{\#U},g^\star_{\#U})\}.
\]
(3.2)''',[10],[2,3,4],[r'\Delta_{\mathcal D}',r'\sup_{g\in\mathcal G}'],'Uniform discriminator discrepancy relative to the Hölder IPM. Distinct from the candidate-dependent Besov discrepancy in Theorem 5.4.','Section 3.1.1 — Discriminator approximation error (3.2)')
add(13,'covering number',r'''Let us now define the notion of covering number which is the other feature of $\mathcal G$ and $\mathcal D$ that intervenes in the bound on the objective. For $\epsilon>0$, a minimal $\epsilon$-covering $\mathcal F_\epsilon$ of a class of functions $\mathcal F$ is defined as:
\[
\mathcal F_\epsilon:=\operatorname*{arg\,min}\{|A|\mid\forall f\in\mathcal F,\exists f_\epsilon\in A,\|f-f_\epsilon\|_\infty\le\epsilon\}.
\]
(3.3)
The covering numbers $|\mathcal G_\epsilon|$ and $|\mathcal D_\epsilon|$ characterise the sizes of the classes of functions.''',[10],[],[r'\mathcal F_\epsilon',r'\|f-f_\epsilon\|_\infty\le\epsilon'],'Supremum-norm minimal coverings. The source uses argmin as a selected cover and does not specify a tie-selection or require centers to lie in F. Preserve the notation without interpreting the cardinality of a set of all minimizers.','Section 3.1.1 — Covering number (3.3)')
add(14,'wavelet basis',r'''Let $\psi,\varphi\in\mathcal H^{\lfloor\beta\rfloor+3}(\mathbb R,\mathbb R)$ be a compactly supported scaling and wavelet function respectively (see (Daubechies, 1988) on Daubechies wavelets). For ease of notation, the functions $\psi,\varphi$ will be written $\psi_0,\psi_1$ respectively. Then for $j\in\mathbb N_0,l\in\{1,\ldots,2^p-1\},w\in\mathbb Z^p$, the family of functions
\[
\psi_{0w}(x)=\prod_{i=1}^p\psi_0(x_i-w_i),\quad\psi_{jlw}(x)=2^{jp/2}\prod_{i=1}^p\psi_{l_i}(2^jx_i-w_i)
\]
form an orthonormal basis of $L^2(\mathbb R^p,\mathbb R)$ (with $l_i$ the $i$th digit of the base-2-decomposition of $l$).
One can construct a wavelet basis on $L^2(\mathbb T^d)$ by using the periodised scaling and wavelet functions on $[0,1]/\mathbb Z$:
\[
\varphi_j^{\mathrm{per}}(s)=2^{j/2}\sum_{k\in\mathbb Z}\varphi(2^j(s-k))\quad\text{and}\quad\psi_j^{\mathrm{per}}(s)=2^{j/2}\sum_{k\in\mathbb Z}\psi(2^j(s-k)).
\]
(3.7)
Note that it is a well known fact that $\sum_{k\in\mathbb Z}\varphi(s-k)=1$ (Section 4.3.4 in Giné and Nickl (2015)). For ease of notation, $\varphi_j^{\mathrm{per}}$ and $\psi_j^{\mathrm{per}}$ will be written $\psi_{j0}^{\mathrm{per}},\psi_{j1}^{\mathrm{per}}$. Then
\[
\left(1,\left\{\psi_{jlz}^{\mathrm{per}}=\prod_{i=1}^d\psi_{jl_i}^{\mathrm{per}}(\cdot-2^{-j}z_i)\ \middle|\ j\in\mathbb N_0,l\in\{1,\ldots,2^d\},z\in\{0,\ldots,2^j-1\}^d\right\}\right),
\]
is a wavelet basis of $L^2(\mathbb T^d)$.''',[12,13],[1],[r'\psi_{jlw}',r'\psi_{jlz}^{\mathrm{per}}'],'Original Euclidean and periodized basis formulas, kept as separate paragraphs. The source reverses the scaling/wavelet phi/psi convention and prints the periodized l range through 2^d. Preserve both discrepancies and the constant mode; do not invent corrected indices.','Section 3.2.1 — Euclidean and periodised wavelet bases',kind='source_passage')
add(15,'Besov space',r'''Let $q_1,q_2\ge1,s>0$ and $b\ge0$ such that $\lfloor\beta\rfloor+3>s$. The Besov space $\mathcal B_{q_1,q_2}^{s,b}(\mathbb R^p,\mathbb R)$ consists of functions $f:\mathbb R^p\to\mathbb R$ that admit a wavelet expansion in $L^2$:
\[
f(x)=\sum_{w\in\mathbb Z^p}\alpha_f(w)\psi_{0w}(x)+\sum_{j=0}^\infty\sum_{l=1}^{2^p-1}\sum_{w\in\mathbb Z^p}\alpha_f(j,l,w)\psi_{jlw}(x),
\]
equipped with the norm
\[
\|f\|_{\mathcal B_{q_1,q_2}^{s,b}}=\left(\left(\sum_{w\in\mathbb Z^p}|\alpha_f(w)|^{q_1}\right)^{q_2/q_1}+\sum_{j=0}^\infty2^{jq_2(s+p/2-p/q_1)}(1+j)^{bq_2}\sum_{l=1}^{2^p-1}\left(\sum_{w\in\mathbb Z^p}|\alpha_f(j,l,w)|^{q_1}\right)^{q_2/q_1}\right)^{1/q_2}.
\]
Note that for $b=0$, $\mathcal B_{q_1,q_2}^{s,0}(\mathbb R^p,\mathbb R)$ coincides with the classical Besov space $\mathcal B_{q_1,q_2}^s(\mathbb R^p,\mathbb R)$ (Giné and Nickl, 2015). The Besov spaces can be generalized for any $s\in\mathbb R$ as a subspace of the space of tempered distribution $\mathcal S'(\mathbb R^p)$. Indeed for $f\in\mathcal S'(\mathbb R^p)$ and $C>0$, writing $\alpha_f(j,l,w)=\langle f,\psi_{jlw}\rangle$, the Besov space for $s\in\mathbb R$ is defined as
\[
\mathcal B_{q_1,q_2}^{s,b}(\mathbb R^p,\mathbb R,C)=\{f\in\mathcal S'(\mathbb R^p)\mid\|f\|_{\mathcal B_{q_1,q_2}^{s,b}}\le C\}.
\]''',[12],[14],[r'\mathcal B_{q_1,q_2}^{s,b}',r'(1+j)^{bq_2}',r'\alpha_f(j,l,w)'],'Original weighted wavelet Besov norm and radius-C convention. Later use of q1=q2=infinity and periodic/vector versions invokes conventional modifications not explicitly expanded here; supporting main-text context is retained separately.','Section 3.2.1 — Besov space')
add(16,'class of function',r'''Fix $L>0$ and let be $\widehat\varphi:\mathbb R\to\mathbb R$ such that
\[
\|\varphi-\widehat\varphi\|_{\mathcal H^{\lfloor\beta\rfloor+2}}\le CL^{-1},
\]
(3.10)
for $\varphi$ the Daubechies scaling function. The existence of a neural network (either with tanh or ReQU activation) $\widehat\varphi$ satisfying (3.10) is guaranteed by Lemmas A.1 and A.2 in Section A.2.1. We also detail in this section how to compute $\widehat\psi_{jlz}^{\mathrm{per}}$ (A.10), the approximation by neural networks of the periodised Daubechies wavelet $\psi_{jlz}^{\mathrm{per}}$ using $\widehat\varphi$. Define the class of function $\widehat{\mathcal F}_{\mathrm{per}}^{\eta,\delta}$ by
\[
\widehat{\mathcal F}_{\mathrm{per}}^{\eta,\delta}=\left\{f\in L^2(\mathbb T^d,\mathbb R^p)\ \middle|\ f_i=\sum_{j=0}^{\log_2(\delta^{-1})}\sum_{l=1}^{2^d}\sum_{z\in\{0,\ldots,2^j-1\}^d}\widehat\alpha(j,l,w)_i\widehat\psi_{jlz}^{\mathrm{per}}\ \text{with }|\widehat\alpha(j,l,z)_i|\le C_\eta K2^{-j(\eta+d/2)},\forall i\in\{1,\ldots,p\}\right\},
\]
(3.11)
for $C_\eta$ the constant such that $\|\cdot\|_{\mathcal B_{\infty,\infty}^\eta}\le C_\eta\|\cdot\|_{\mathcal H^\eta}$. The class $\widehat{\mathcal F}_{\mathrm{per}}^{\eta,\delta}$ is an approximation of the class $\mathcal F_{\mathrm{per}}^{\eta,\delta}$ defined in (3.8) using the tanh (or ReQU) neural network approximation $\widehat\psi_{jlz}^{\mathrm{per}}$ (A.10) of the periodised wavelet (3.7).''',[14,15],[1,14,15],[r'\widehat{\mathcal F}_{\mathrm{per}}^{\eta,\delta}',r'\widehat\psi_{jlz}^{\mathrm{per}}',r'\widehat\alpha(j,l,w)_i'],'Periodic neural wavelet class with original coefficient bound and precision. The formula prints w in the sum but z in the bound and omits an explicit constant mode. Hat-wavelet implementation (A.10) is appendix-only; retain the reference without inventing its construction.','Section 3.2.2 — Periodic network class (3.10)–(3.11)')
add(17,'generator class',r'''Fix the approximation of the scaling function in (3.10) to be at precision $L^{-1}=n^{-1}$ and take as the generator class
\[
\mathcal G:=\widehat{\mathcal F}_{\mathrm{per}}^{\beta+1,n^{-\frac1{2\beta+d}}}.
\]
(4.1)''',[15],[16],[r'\mathcal G',r'L^{-1}=n^{-1}',r'n^{-\frac1{2\beta+d}}'],'Model-1 generator class at the printed n-dependent resolution and wavelet precision. Preserve the class as written without adding an unprinted Hölder-ball intersection.','Section 4.1 — Generator class (4.1)')
add(18,'discriminator class',r'''Let us take as the discriminator class
\[
\mathcal D:=\{D^\star_{g,g'}\mid g,g'\in\mathcal G_{1/n}\},
\]
(4.2)
with $D^\star_{g,g'}\in\operatorname*{arg\,max}_{D\in\mathcal H_1^\gamma}\mathbb E[D(g(U))-D(g'(u))]$. The class of discriminators is constructed specifically to well approximate the IPMs between the measures $g_{\#U}$ with $g\in\mathcal G$, without being too massive. This class $\mathcal D$ is not really computable in practice, but we use it here to illustrate that we can bypass the problems risen by the lack of regularity of the target measure $g^\star_{\#U}$, at the cost of the tractability of the method.''',[16],[1,2,13,17],[r'\mathcal G_{1/n}',r'\operatorname*{arg\,max}_{D\in\mathcal H_1^\gamma}'],'Model-1 theoretical optimal discriminators between net generators. The source prints lowercase u in its second evaluation, although the expectation uses U elsewhere; preserve that mismatch. No discriminator optimizer or net tie-breaking is invented.','Section 4.1 — Discriminator class (4.2)')
add(19,'class of generators',r'''In order to apply Theorem 5.1 to the GAN estimator $\widehat g$, we need it to verify the manifold regularity condition of Definition 2.1. We define in the Appendix Section E.1, the $\chi$-numerical regularity condition that implies the manifold regularity condition. In a nutshell, it is an easy to compute condition that ensures that if two points are far in the torus, then their images by $\widehat g$ are not too close. We choose
\[
\mathcal G:=\{g\in\widehat{\mathcal F}_{\mathrm{per}}^{\beta+1,n^{-\frac1{2\beta+d}}}\mid g\text{ verifies the }\chi\text{-numerical regularity condition}\}
\]
(5.1)
to be the class of generators.''',[22],[16],[r'\chi',r'\mathcal G',r'n^{-\frac1{2\beta+d}}'],'Manifold generator class restricted by the explicitly appendix-defined numerical condition. Its full condition and choice of chi are unresolved within main-text-only scope. The claimed implication to manifold regularity is not substituted for the actual constraint or used as a definition-body edge.','Section 5.2 — Generator class (5.1)',kind='source_passage')
add(20,'class of function',r'''Let $\widehat\varphi,\widehat\psi$ be the approximations by neural networks of the scaling and wavelet Daubechies function from (A.4) and (A.5) at precision $L^{-1}=n^{-1}$. For ease of notation $\widehat\varphi,\widehat\psi$ will be written $\widehat\psi_0,\widehat\psi_1$ respectively and define the multi-dimensional approximation of the wavelet as
\[
\widehat\psi_{0w}(x)=\prod_{i=1}^p\widehat\psi_0(x_i-w_i),\quad\widehat\psi_{jlw}(x)=2^{pj/2}\prod_{i=1}^p\widehat\psi_{l_i}(2^jx_i-w_i).
\]
Using these approximated wavelets, Define the class of function $\widehat{\mathcal F}$ by
\[
\widehat{\mathcal F}^{\eta,\delta}:=\left\{\sum_{j=0}^{\log_2(\delta^{-1})}\sum_{l=1}^{2^p}\sum_{w\in\{-K2^j,\ldots,K2^j\}^p}\widehat\alpha(j,l,w)\widehat\psi_{jlw}\ \middle|\ |\widehat\alpha(j,l,w)|\le C_\eta K2^{-j(\eta+p/2)}\right\}.
\]
(4.3)''',[17],[1,14,15],[r'\widehat{\mathcal F}^{\eta,\delta}',r'\widehat\psi_{jlw}',r'C_\eta K2^{-j(\eta+p/2)}'],'Nonperiodic neural wavelet class, distinct from the periodic generator class. C_eta is the inherited Hölder/Besov norm constant. Hat-function construction is appendix-only; the sum endpoints and index sets are retained as printed, without inventing a constant/coarse mode or rounding rule.','Section 4.2 — Network class (4.3)')
add(21,'class of discriminators',r'''Define
\[
\widetilde\beta+1:=(\beta+1)\wedge d/2,
\]
(5.2)
write $\widetilde\delta_n:=n^{-\frac1{2\widetilde\beta+d}}$, and choose
\[
\mathcal D:=\widehat{\mathcal F}^{\widetilde\beta+1,\widetilde\delta_n}
\]
(5.3)
to be the class of discriminators.''',[22],[20],[r'\widetilde\beta+1',r'\widetilde\delta_n',r'\mathcal D'],'Manifold discriminator regularity cap and sample-dependent resolution. This redefines tilde-beta relative to the full-dimensional section. For d=1 the displayed denominator 2 tilde-beta+d is zero; retain the source without adding a dimension restriction.','Section 5.2 — Discriminator class (5.2)–(5.3)')
add(22,'covering number',r'''For $\epsilon\in(0,1)$, let
\[
|(\mathcal D_{\mathcal G})_\epsilon|:=\sup_{g\in\mathcal G}|(\{D\circ g\mid D\in\mathcal D\})_\epsilon|,
\]
be the largest $\epsilon$-covering number of the class $\{D\circ g\mid D\in\mathcal D\}$ among $g\in\mathcal G$.''',[22],[13,19,21],[r'|(\mathcal D_{\mathcal G})_\epsilon|',r'\{D\circ g\mid D\in\mathcal D\}'],'Supremum of covering numbers for each fixed-generator composition class, not the covering number of a union over all generators. The surrounding section fixes G and D in (5.1),(5.3).','Section 5.2 — Composed discriminator covering number')
add(23,'discrimination error',r'''For $g\in\mathcal G$, define
\[
D_g^\star\in\operatorname*{arg\,max}_{D\in\mathcal B_{\infty,\infty}^{\widetilde\beta+1}(C)}\mathbb E[D(g(U))-D(g^\star(U))]
\]
and
\[
\overline D_g\in\operatorname*{arg\,min}_{D\in\mathcal D}\|D-D_g^\star\|_{\mathcal B_{\infty,\infty}^0},
\]
as the optimal discriminator within $\mathcal B_{\infty,\infty}^{\widetilde\beta+1}$ and its approximation by $\mathcal D$. Let us write
\[
\Delta_{\mathcal D}^g:=\mathbb E[D_g^\star(g(U))-D_g^\star(g^\star(U))-(\overline D_g(g(U))-\overline D_g(g^\star(U)))]
\]
for the discrimination error between $g_{\#U}$ and $g^\star_{\#U}$ of the class $\mathcal D$ compared to the class $\mathcal B_{\infty,\infty}^{\widetilde\beta+1}(C)$.''',[22,23],[2,15,19,21],[r'\Delta_{\mathcal D}^g',r'D_g^\star',r'\overline D_g'],'Candidate-specific discrepancy using a Besov-optimal discriminator and its B^0 approximation. At the random fitted generator Theorem 5.4 takes its expectation; it is distinct from the uniform Delta_D in (3.2). Preserve optimizer existence/selection as stated.','Section 5.2 — Candidate discrimination error')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
