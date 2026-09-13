"""Transcribe statement prerequisites from the inspected pinned preprint, without supplements."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
interfaces=[];members={};edges={}
def add(lid,term,body,pages,heading,deps=None,*,kind='definition',symbols=(),phrases=(),context=None,note=None,shape):
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,
        statement_original=body.strip(),relation='exact',depends_on=list(deps or {}),
        evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=list(symbols),highlight_phrases=list(phrases))
    if note:m['variant_note']=note
    terms=term if isinstance(term,list) else [term];keywords=[]
    for t in terms:
        key=dict(paper_id=PID,local_id=lid,source_text=t,label=t[0].upper()+t[1:],kind='term')
        if t not in body:
            assert context and t in context,(lid,t)
            m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])];key['context_id']=lid+'/name'
        keywords.append(key)
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=' · '.join(k['label'] for k in keywords),
        lean_role='hypothesis' if kind in ('condition','assumption') else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}
add('D1','covariates',r'''
We consider an iid sample of $n$ observations of $Z=(X,A,Y)$ from distribution $\mathbb P$, where $X\in[0,1]^d$ denotes covariates, $A\in\{0,1\}$ a treatment or policy indicator, and $Y\in\mathbb R$ an outcome of interest. We let $F$ denote the distribution function of the covariate $X$ (with density $f$ as needed),
''',[4],'Section 2 — observed data and covariate distribution',kind='source_passage',phrases=['covariates'],symbols=[r'Z=(X,A,Y)',r'X\in[0,1]^d'],shape='Independent identically distributed observed triples with a bounded covariate domain, binary treatment and real outcome; F and f concern only the covariates. The underlying true law is printed as blackboard P, while a generic model law is written P; F is the separate covariate distribution.')
add('D2',['propensity score','marginal','treatment-specific outcome regressions'],r'''
\[
\pi(x)=\mathbb P(A=1\mid X=x)
\]
\[
\eta(x)=\mathbb E(Y\mid X=x)
\]
\[
\mu_a(x)=\mathbb E(Y\mid X=x,A=a)
\]
denote the propensity score, marginal, and treatment-specific outcome regressions, respectively. We sometimes omit arguments from functions to ease notation, e.g., note that $\tau=(\eta-\mu_0)/\pi$.
''',[4],'Section 2 — propensity and outcome regression functions',{'D1':'The conditional functions are defined under the law of the observed covariates, treatment and outcome.'},phrases=['propensity score','treatment-specific outcome regressions'],symbols=[r'\pi(x)',r'\mu_a(x)',r'\eta(x)'],shape='The three original conditional-function definitions, kept with their source terminology. The theorems impose smoothness on the control regression mu_0, not the marginal regression eta. The final displayed identity for tau requires division by pi; its zero-propensity convention is not supplied.')
add('D3','CATE',r'''
Our goal is to study estimation of the CATE $\tau(x)=\mu_1(x)-\mu_0(x)$ at a point $x_0\in(0,1)^d$, with error quantified by mean absolute error
\[
\mathbb E|\widehat\tau(x_0)-\tau(x_0)|.
\]
''',[4],'Section 2 — pointwise CATE and absolute error',{'D2':'The target is the difference between the two treatment-specific regressions.'},phrases=['CATE','mean absolute error'],symbols=[r'\tau(x)=\mu_1(x)-\mu_0(x)',r'x_0\in(0,1)^d'],shape='An interior-point observed regression contrast and its mean absolute estimation error. The causal potential-outcome interpretation has additional identifying assumptions in Section 1, saved separately; it is not needed to define the observed-data statistical target.')
add('D4','Hölder class',r'''
We say a function is $s$-smooth if it belongs to a Hölder class with index $s$; this essentially means it has $s-1$ bounded derivatives, and the highest order derivative is continuous. To be more precise, let $\lfloor s\rfloor$ denote the largest integer strictly smaller than $s$, and let $D^\alpha=\frac{\partial^\alpha}{\partial x_1^{\alpha_1}\ldots\partial x_d^{\alpha_d}}$ denote the partial derivative operator. Then the Hölder class with index $s$ contains all functions $g:\mathcal X\to\mathbb R$ that are $\lfloor s\rfloor$ times continuously differentiable, with derivatives up to order $\lfloor s\rfloor$ bounded, i.e.,
\[
|D^\alpha g(x)|\leq C<\infty
\]
for all $\alpha=(\alpha_1,\ldots,\alpha_d)$ with $\sum_j\alpha_j\leq\lfloor s\rfloor$ and for all $x\in\mathcal X$, and with $\lfloor s\rfloor$-order derivatives satisyfing the Lipschitz condition
\[
|D^\beta g(x)-D^\beta g(x')|\leq C\|x-x'\|^{s-\lfloor s\rfloor}
\]
for some $C<\infty$, for all $\beta=(\beta_1,\ldots,\beta_d)$ with $\sum_j\beta_j=\lfloor s\rfloor$, and for all $x,x'\in\mathcal X$, where for a vector $v\in\mathbb R^d$ we let $\|v\|$ denote the Euclidean norm. Sometimes Hölder classes are referenced by both the smoothness $s$ and constant $C$, but we focus our discussion on the smoothness $s$ and omit the constant, which is assumed finite and independent of $n$.
''',[4],'Section 2 — Hölder smoothness convention',phrases=['Hölder class'],symbols=[r'\lfloor s\rfloor',r'|D^\alpha g(x)|\leq C<\infty'],shape='Hölder differentiability with the source’s strict floor: at integer s, the top derivative order is s-1 and the remaining exponent is one. Alpha and beta are multi-indices inside this definition, distinct from the scalar smoothness indices in the theorems. The Hölder radius is fixed independently of n; no numerical radius is invented.')
add('D5','Legendre polynomial series',r'''
Let $K_h(x)=\frac1{h^d}\mathbb 1(\|x-x_0\|\leq h/2)$. For each covariate $x_j$, $j=1,\ldots,d$, define $\rho(x_j)=\{\rho_0(x_j),\rho_1(x_j),\ldots,\rho_{\lfloor\gamma\rfloor}(x_j)\}^{\mathsf T}$ as the first $(\lfloor\gamma\rfloor+1)$ terms of the Legendre polynomial series (shifted to be orthonormal on $[0,1]$),
\[
\rho_m(x_j)=\sum_{\ell=0}^m(-1)^{\ell+m}\sqrt{2m+1}\binom m\ell\binom{m+\ell}\ell x_j^\ell.
\]
Define $\rho(x)$ to be the corresponding tensor product of all interactions of $\rho(x_1),\ldots,\rho(x_d)$ up to order $\lfloor\gamma\rfloor$, which has length $q=\binom{d+\lfloor\gamma\rfloor}{\lfloor\gamma\rfloor}$ and is orthonormal on $[0,1]^d$, and finally define $\rho_h(x)=\rho(1/2+(x-x_0)/h)$.
''',[15],'Definition 2 — kernel and localized Legendre construction',{'D4':'The polynomial order uses the source’s largest-integer-strictly-below convention for gamma.'},phrases=['Legendre polynomial series'],symbols=[r'K_h(x)',r'\rho_m(x_j)',r'\rho_h(x)'],shape='The explicit shifted Legendre formula, total-degree interaction basis of fixed dimension q, and affine localization with the printed indicator kernel. The source defines the norm as Euclidean, although later text describes a cube. No sup-norm substitution or complete tensor-product dimension is made.')
add('D6','localized basis terms',r'''
\[
b_{hk}(x)=b\{1/2+(x-x_0)/h\}\mathbb 1(\|x-x_0\|\leq h/2)
\]
for $b:\mathbb R^d\mapsto\mathbb R^k$ a basis of dimension $k$.
''',[16],'Definition 2 — localized correction basis',context='In this sense, these localized basis terms spend all their approximation power locally rather than globally away from x0.',phrases=[],symbols=[r'b_{hk}(x)',r'\mathbb 1(\|x-x_0\|\leq h/2)'],shape='A k-dimensional input basis evaluated on affinely stretched covariates and restricted by the printed local indicator. It is distinct from the fixed-dimensional Legendre basis rho; k grows with the sample size. The declaration of b occurs immediately after the intervening estimated Gram formula in Definition 2.')
members['D6']['naming_context'][0]['evidence']=[dict(page=17,location='Section 4.1 — explanation of localized basis terms')]
add('D7','nuisance estimators',r'''
\[
\widehat\Omega=\int_{v\in[0,1]^d}b(v)b(v)^{\mathsf T}\,d\widehat F(x_0+h(v-1/2))
\]
for $b:\mathbb R^d\mapsto\mathbb R^k$ a basis of dimension $k$. The nuisance estimators $(\widehat F,\widehat\pi,\widehat\mu_0)$ are constructed from a separate training sample $D^n$, independent of that on which $\mathbb U_n$ operates.
''',[16],'Definition 2 — nuisance inputs and estimated basis matrix',{'D1':'F-hat estimates the distribution of the observed covariates.','D2':'Pi-hat and mu_0-hat estimate the propensity score and control regression.','D6':'The matrix uses the k-dimensional correction basis b, not the Legendre basis.','D10':'The affine measure argument is the estimated counterpart of the stretched F-star measure defined in Section 4.2.'},phrases=['nuisance estimators'],symbols=[r'\widehat\Omega',r'D^n',r'(\widehat F,\widehat\pi,\widehat\mu_0)'],shape='Independently trained nuisance functions and the matrix obtained by integrating basis outer products against the affinely transformed estimated covariate distribution. The source formula supplies no explicit h^-d measure normalization or failure rule for a singular estimated matrix. Remark 8 says an ordinary empirical F-hat need not be invertible with the chosen k.')
add('D8','Higher-Order Local Polynomial R-Learner',r'''
The proposed estimator is then defined as
\[
\widehat\tau(x_0)=\rho_h(x_0)^{\mathsf T}\widehat Q^{-1}\widehat R\tag{3}
\]
where $\widehat Q$ is a $q\times q$ matrix and $\widehat R$ a $q$-vector given by
\[
\widehat Q=\mathbb P_n\{\rho_h(X)K_h(X)\widehat\varphi_{a1}(Z)\rho_h(X)^{\mathsf T}\}
+\mathbb U_n\{\rho_h(X_1)K_h(X_1)\widehat\varphi_{a2}(Z_1,Z_2)K_h(X_2)\rho_h(X_1)^{\mathsf T}\}
\]
\[
\widehat R=\mathbb P_n\{\rho_h(X_1)K_h(X_1)\widehat\varphi_{y1}(Z_1)\}
+\mathbb U_n\{\rho_h(X_1)K_h(X_1)\widehat\varphi_{y2}(Z_1,Z_2)K_h(X_2)\},
\]
respectively, and
\[
\widehat\varphi_{a1}(Z)=A\{A-\widehat\pi(X)\}
\]
\[
\widehat\varphi_{y1}(Z)=\{Y-\widehat\mu_0(X)\}\{A-\widehat\pi(X)\}
\]
\[
\widehat\varphi_{a2}(Z_1,Z_2)=-\{A_1-\widehat\pi(X_1)\}b_{hk}(X_1)^{\mathsf T}\widehat\Omega^{-1}b_{hk}(X_2)A_2
\]
\[
\widehat\varphi_{y2}(Z_1,Z_2)=-\{A_1-\widehat\pi(X_1)\}b_{hk}(X_1)^{\mathsf T}\widehat\Omega^{-1}b_{hk}(X_2)\{Y_2-\widehat\mu_0(X_2)\}
\]
''',[15,16],'Definition 2 (Higher-Order Local Polynomial R-Learner)',{'D5':'The output and both empirical terms use the localized Legendre vector and the kernel K_h.','D6':'Both second-order corrections use the stretched and restricted basis b_hk.','D7':'The residual functions and inverse estimated basis matrix use the independently trained nuisance inputs.','D1':'The empirical and ordered-pair U-statistic averages act on iid observed triples; their normalizations are given in Section 2.'},context='Definition 2 (Higher-Order Local Polynomial R-Learner).',phrases=['Definition 2'],symbols=[r'\widehat\tau(x_0)',r'\widehat\varphi_{a2}',r'\widehat\varphi_{y2}',r'\widehat Q'],shape='The full printed estimator aggregation and four correction kernels. P_n is normalized by n and U_n by n(n-1), over ordered distinct pairs. The Q-hat correction literally ends in rho_h(X_1)^T; the later bias expression (9) uses X_2 instead. That mismatch is not repaired. The first-order a-kernel contains raw A times its residual, not a squared residual.')
add('D9','locally weighted projection parameter',r'''
In addition, our proposed estimator can be viewed as estimating a locally weighted projection parameter $\tau_h(x_0)=\rho_h(x_0)^{\mathsf T}\theta$, with coefficients given by
\[
\operatorname*{argmin}_\beta\mathbb E\left[K_h(x)\pi(x)\{1-\pi(x)\}\{\tau(x)-\beta^{\mathsf T}\rho_h(x)\}^2\right]=Q^{-1}R\tag{4}
\]
for
\[
Q=\int\rho_h(x)K_h(x)\pi(x)\{1-\pi(x)\}\rho_h(x)^{\mathsf T}\,dF(x)
\]
\[
R=\int\rho_h(x)K_h(x)\pi(x)\{1-\pi(x)\}\tau(x)\,dF(x).
\]
''',[16],'Section 4.1 — weighted projection and population matrices, equation (4)',{'D1':'The matrix and vector integrate with respect to the population covariate law F.','D2':'The projection weights use the population propensity pi and its complement.','D3':'The projected function is the observed-data CATE tau.','D5':'The projection is onto the localized finite Legendre vector with the same K_h weights.'},phrases=['locally weighted projection parameter'],symbols=[r'Q^{-1}R',r'Q=\int',r'\tau_h(x_0)'],shape='The population weighted least-squares coefficients, with a q-by-q matrix Q distinct from the k-by-k correction-basis matrix Omega. The theorem refers directly to Q’s eigenvalues and its estimated inverse; it does not assume the CATE equals a polynomial exactly.')
add('D10','distribution',r'''
for $dF^*(v)=dF(x_0+h(v-1/2))$ the distribution in $B_h(x_0)$, the $h$-ball around $x_0$, mapped to $[0,1]^d$.
''',[18],'Section 4.2 — transformed local covariate measure',{'D1':'The transformed measure comes from the original covariate distribution F.'},phrases=['distribution'],symbols=[r'dF^*(v)=dF(x_0+h(v-1/2))',r'B_h(x_0)'],shape='Literal local transformed-measure notation used in the approximation norm and density-ratio conditions. The text calls it a distribution but does not state whether restriction is normalized, nor insert h^-d. Ball versus cube language and the h versus h/2 radius conventions remain unresolved.')
add('D11','linear projection',r'''
where $\Pi_b g=\operatorname*{argmin}_{\ell=\theta^{\mathsf T}b}\int(g-\ell)^2\,dF^*$ is the usual linear projection of $g$ on $b$,
''',[18],'Section 4.2 — basis projection in the transformed measure',{'D6':'The approximation space is the span of the k-dimensional correction basis b.','D10':'The projection is in the norm induced by F-star.'},phrases=['linear projection'],symbols=[r'\Pi_b g',r'\operatorname*{argmin}_{\ell=\theta^{\mathsf T}b}'],shape='The population projection onto the correction-basis span under F-star. Its main-text coordinate expression uses Omega inverse; Omega is thereby identified as the population basis Gram matrix, without adding an estimated nuisance dependency to this population projection. The source does not separately display Omega=integral bb^T dF-star.')
members['D11']['application_context']=[dict(text=r'''where we define
\[
\Pi_b g^*(u)=b(u)^{\mathsf T}\Omega^{-1}\int b(v)g^*(v)\,dF^*(v)
\]
as the $F^*$-weighted linear projection of $g^*$ on the basis $b$,''',evidence=[dict(page=20,location='Section 4.2 — coordinate definition of the same projection and population Omega')])]
add('D12','Hölder approximation properties',r'''
Here we rely on the basis $b(x)$ having optimal Hölder approximation properties, In particular, we assume the approximation error of projections in $L_2$ norm satisfies
\[
\|(I-\Pi_b)g\|_{F^*}\lesssim k^{-s/d}\quad\text{for any }s\text{-smooth function }g\tag{6}
\]
''',[18],'Section 4.2 — Hölder approximating condition (6)',{'D4':'The smoothness class is the original Hölder class, with its fixed radius and strict-floor convention.','D11':'The residual uses the population basis projection under the transformed covariate measure.'},kind='condition',phrases=['Hölder approximation properties'],symbols=[r'\|(I-\Pi_b)g\|_{F^*}',r'k^{-s/d}'],shape='The stated L2 projection approximation rate for smooth functions. Here s is a generic smoothness order, not restricted to the average (alpha+beta)/2 used in the theorem rates. Uniform constants over basis dimension, bandwidth and the relevant fixed-radius Hölder classes are necessary interpretations of the asymptotic inequality; the source does not numerically specify them.')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source interfaces.')


if __name__ == "__main__":
    main()
