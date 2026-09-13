"""Preserve original amplification, model, divergence and assumption definitions."""
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
add(1,'total variation (TV) distance',r'''\[
\|P-Q\|_{\mathrm{TV}}=\frac12\int|dP-dQ|.
\]''',[7],[],[r'\|P-Q\|_{\mathrm{TV}}'],'Original probability-measure TV normalization, one half of the L1 difference. Common domination is implicit; do not use the doubled variation norm.','Section 3 — Total variation distance',context='For probability measures $P,Q$ defined on the same probability space, the total variation (TV) distance, Hellinger distance, Kullback–Leibler (KL) divergence, and the chi-squared divergence are defined as follows:')
add(2,'Hellinger distance',r'''\[
H(P,Q)=\left(\frac12\int(\sqrt{dP}-\sqrt{dQ})^2\right)^{1/2}.
\]''',[7],[],[r'H(P,Q)'],'Original normalized Hellinger distance. Assumption4 uses its square, retaining the factor one half.','Section 3 — Hellinger distance',context='the total variation (TV) distance, Hellinger distance, Kullback–Leibler (KL) divergence, and the chi-squared divergence are defined as follows:')
add(3,'chi-squared divergence',r'''\[
\chi^2(P\|Q)=\int\frac{(dP-dQ)^2}{dQ}.
\]''',[7],[],[r'\chi^2(P\|Q)'],'Original asymmetric chi-squared divergence, denominator Q. Infinite values when domination fails and zero-density conventions are implicit. Definition5.1 uses estimator first and truth second.','Section 3 — Chi-squared divergence',context='the total variation (TV) distance, Hellinger distance, Kullback–Leibler (KL) divergence, and the chi-squared divergence are defined as follows:')
add(4,'sample amplification procedure',r'''Let $\mathcal P$ be a class of probability distributions over a domain $\mathcal X$. We say that $\mathcal P$ admits an $(n,n+m,\varepsilon)$ sample amplification procedure if there exists a (possibly randomized) map $T_{\mathcal P,n,m,\varepsilon}:\mathcal X^n\to\mathcal X^{n+m}$ such that
\[
\sup_{P\in\mathcal P}\|P^{\otimes n}\circ T_{\mathcal P,n,m,\varepsilon}^{-1}-P^{\otimes(n+m)}\|_{\mathrm{TV}}\le\varepsilon.\tag{1}
\]''',[1],[1],[r'T_{\mathcal P,n,m,\varepsilon}',r'P^{\otimes(n+m)}'],'Original existential uniform-TV amplification property. Map may be randomized; no requirement to retain input samples or produce conditionally independent outputs. Randomized-map notation is interpreted by a Markov kernel, not deterministic pushforward alone.','Definition 1.1 (Sample Amplification)')
add(5,'minimax error of sample amplification',r'''For a given distribution class $\mathcal P$ and sample sizes $n$ and $m$, the minimax error of sample amplification is defined as
\[
\varepsilon^\star(\mathcal P,n,m)\triangleq\inf_T\sup_{P\in\mathcal P}\|P^{\otimes(n+m)}-P^{\otimes n}\circ T^{-1}\|_{\mathrm{TV}},\tag{4}
\]
where the infimum is over all (possibly randomized) measurable mappings $T:\mathcal X^n\to\mathcal X^{n+m}$.''',[7],[1],[r'\varepsilon^\star(\mathcal P,n,m)'],'Original minimax amplification error: infimum over a single parameter-independent kernel, then supremum over the class. Its infimum need not be attained under the stated generality.','Section 3 — Minimax amplification error (4)')
add(6,'maximum size of sample amplification',r'''For a given error level $\varepsilon$, the maximum size of sample amplification is the largest $m$ such that there exists an $(n,n+m,\varepsilon)$ sample amplification, i.e.
\[
m^\star(\mathcal P,n,\varepsilon)\triangleq\max\{m\in\mathbb N:\varepsilon^\star(\mathcal P,n,m)\le\varepsilon\}.\tag{5}
\]
For the ease of presentation, we often choose $\varepsilon$ to be a small constant (say $0.1$) and abbreviate the above quantity as $m^\star(\mathcal P,n)$; we remark that all our results work for a generic $\varepsilon\in(0,1)$.''',[7,8],[4,5],[r'm^\star(\mathcal P,n,\varepsilon)',r'm^\star(\mathcal P,n)'],'Original maximal additional sample size and small-error abbreviation. Empty/unbounded feasible sets and equality when the infimum is unattained remain unstated conventions.','Section 3 — Maximum amplification size (5)')
add(7,'sufficient statistics',r'''We first recall the definition of sufficient statistics: in a statistical model $\mathcal M=(\mathcal X,(P_\theta)_{\theta\in\Theta})$ and $X\sim P_\theta$, a statistic $T=T(X)\in\mathcal T$ is sufficient if and only if both $\theta-X-T$ and $\theta-T-X$ are Markov chains.''',[9],[],[r'\theta-X-T',r'\theta-T-X'],'Original sufficiency definition by both Markov chains. For a nonrandom parameter, the statement requires a parameter-uniform conditional kernel interpretation; regular conditional probability existence is not guaranteed on arbitrary measurable spaces.','Section 4.1 — Sufficient statistics')
add(8,'Sample amplification via sufficiency',r'''1. Input: samples $X_1,\ldots,X_n$, a given transformation $f$ between sufficient statistics
2. Compute the sufficient statistic $T_n=T_n(X_1,\ldots,X_n)$.
3. Apply $f$ to the sufficient statistic and compute $\widehat T_{n+m}=f(T_n)$.
4. Generate $(\widehat X_1,\ldots,\widehat X_{n+m})\sim P_{X^{n+m}\mid T_{n+m}}(\cdot\mid\widehat T_{n+m})$.
5. Output: amplified samples $(\widehat X_1,\ldots,\widehat X_{n+m})$.''',[9],[7],[r'\widehat T_{n+m}=f(T_n)',r'P_{X^{n+m}\mid T_{n+m}}'],'Complete general conditional-generation algorithm. Sufficiency makes the kernel independent of the unknown parameter. Values of the kernel at null conditioning events and common versions across parameters remain measure-theoretic requirements.','Algorithm 1 — Sample amplification via sufficiency',context='Algorithm 1 Sample amplification via sufficiency')
add(9,'exponential family',r'''The exponential family $(\mathcal X,(P_\theta)_{\theta\in\Theta})$ of probability measures is determined by
\[
dP_\theta(x)=\exp(\theta^\top T(x)-A(\theta))\,d\mu(x),
\]
where $\theta\in\Theta$ is the natural parameter with $\Theta=\{\theta\in\mathbb R^d:A(\theta)<\infty\}$, $T(x)$ is the sufficient statistic, $A(\theta)$ is the log-partition function, and $\mu$ is the base measure.''',[11],[7],[r'\exp(\theta^\top T(x)-A(\theta))',r'\Theta=\{\theta\in\mathbb R^d:A(\theta)<\infty\}'],'Original natural exponential-family definition, with full finite-log-partition domain. Openness, Hessian invertibility and boundary differentiation are not added to the original definition.','Definition 4.3 (Exponential family)')
add(10,'Continuity',r'''The parameter set $\Theta$ has a non-empty interior. Under each $\theta\in\Theta$, the probability distribution $\mathcal L(T(X))$ is absolutely continuous with respect to the Lebesgue measure.''',[12],[9],[r'\mathcal L(T(X))'],'Original nonempty-interior and absolutely continuous statistic condition. It is not merely continuity of the parameter map or of the observations.','Assumption 1 (Continuity)',kind='assumption',context='Assumption 1 (Continuity).',phrases=['Assumption 1'])
add(11,'Moment condition',r'''For a given integer $k>0$, it holds that
\[
\sup_{\theta\in\Theta}\mathbb E_\theta\left[\left\|(\nabla^2A(\theta))^{-1/2}(T(X)-\nabla A(\theta))\right\|_2^k\right]<\infty.
\]
We call it the moment condition $M_k$.''',[12],[9],[r'(\nabla^2A(\theta))^{-1/2}',r'M_k'],'Original standardized k-th moment bound uniform in theta. Theorem4.5 uses k=3;4.6 imposes k=10 on each one-dimensional component. A uniform bound across a growing number of components is not expressly quantified.','Assumption 2 (Moment condition Mk)',kind='assumption',context='Assumption 2 (Moment condition $M_k$).',phrases=['Assumption 2'])
add(12,'sample average',r'''Let $X_1,\ldots,X_n$ be i.i.d. samples drawn from $P_\theta$ taking a general form in Definition 4.3, then it is clear that the sample average
\[
T_n(X^n)\triangleq\frac1n\sum_{i=1}^nT(X_i)
\]
is a sufficient statistic by the factorization theorem. We will apply the general Algorithm 1 with an identity map between sufficient statistics, i.e. $\widehat T_{n+m}=T_n$.''',[12],[7,8,9],[r'T_n(X^n)',r'\widehat T_{n+m}=T_n'],'Original average sufficient statistic and identity-map choice for the exponential-family amplification upper bounds. T_n denotes a statistic as well as its value on a random sample.','Section 4.3 — Sample average and identity map')
add(13,'product exponential family',r'''First, to avoid the unknown dependence on $d$, we additionally assume a product exponential family, i.e. $P_\theta(dx)=\prod_{i=1}^dp_{\theta_i}(dx_i)$, where each $p_{\theta_i}(x_i)$ is a one-dimensional exponential family.''',[13],[9,15],[r'P_\theta(dx)=\prod_{i=1}^dp_{\theta_i}(dx_i)'],'Original product of one-dimensional exponential families. Keep it separate from the general product distribution class and from Assumptions1/2 imposed componentwise only in4.6.','Section 4.3 — Product exponential family',kind='source_passage')
add(14,'estimation error',r'''For a class of distributions $\mathcal P$ and sample size $n$, the $\chi^2$-estimation error $r_{\chi^2}(\mathcal P,n)$ is defined to be the minimax estimation error under the expected $\chi^2$-divergence:
\[
r_{\chi^2}(\mathcal P,n)\triangleq\inf_{\widehat P_n}\sup_{P\in\mathcal P}\mathbb E_P[\chi^2(\widehat P_n,P)],
\]
where the infimum is taken over all possible distribution estimators $\widehat P_n$ based on $n$ samples.''',[14],[3],[r'r_{\chi^2}(\mathcal P,n)',r'\chi^2(\widehat P_n,P)'],'Original expected chi-squared minimax estimation risk with estimator-first divergence orientation. Distribution estimators are not required to belong to the model class.','Definition 5.1 (Chi-squared estimation error)')
add(15,'product structure',r'''When the distribution class $\mathcal P$ has a product structure $\mathcal P=\prod_{j=1}^d\mathcal P_j$, the next theorem shows a better relationship between the amplification error and the learning error.

$P_\theta=\prod_{j=1}^dp_{\theta_j}$ be a product model with $(\theta_1,\ldots,\theta_d)\in\prod_{j=1}^d\Theta_j$.''',[15,19],[],[r'\mathcal P=\prod_{j=1}^d\mathcal P_j',r'P_\theta=\prod_{j=1}^dp_{\theta_j}'],'Original unrestricted Cartesian product of coordinate families, with its parameterized notation excerpted from6.4. No exponential-family, continuity or common-parameter restriction is inherent.','Section 5.1 and Theorem 6.4 — Product model',kind='source_passage')
add(16,'Gaussian location model',r'''Consider the observations $X_1,\ldots,X_n$ from the Gaussian location model $P_\theta=\mathcal N(\theta,\Sigma)$ with an unknown mean $\theta\in\mathbb R^d$ and a known covariance $\Sigma\in\mathbb R^{d\times d}$.''',[10],[],[r'P_\theta=\mathcal N(\theta,\Sigma)'],'Original unknown-mean, known-covariance family. Positive definiteness is not explicitly stated; the exact formula in6.2 needs care for singular covariance.','Example 4.1 — Gaussian location model',kind='source_passage')
add(17,'identity map',r'''To amplify to $n+m$ samples, note that the sample mean vector is a sufficient statistic here, with
\[
T_n(X_1,\ldots,X_n)=\frac1n\sum_{i=1}^nX_i\sim\mathcal N(\theta,\Sigma/n).
\]
Now consider the identity map between sufficient statistics $\widehat T_{n+m}=T_n$ used with algorithm 1. The amplified samples $(\widehat X_1,\ldots,\widehat X_{n+m})$ are drawn from $\mathcal N(0,\Sigma)$ conditioned on the event that $T_{n+m}(\widehat X^{n+m})=\widehat T_{n+m}=T_n(X^n)$.''',[10],[7,8,16],[r'\widehat T_{n+m}=T_n',r'\mathcal N(\theta,\Sigma/n)'],'Original Gaussian identity-statistic procedure. Source shorthand says samples drawn from N(0,Sigma) conditioned on their mean; the product sampling convention is supplied by the general algorithm and Example4.2. Do not require the amplified sample to contain the originals.','Example 4.1 — Identity-map amplification')
add(18,'Linear independence',r'''The components of sufficient statistic $T(x)$ are linearly independent, i.e. $a^\top T(x)=0$ for $\mu$-almost all $x\in\mathcal X$ implies $a=0$.''',[18],[9],[r'a^\top T(x)=0',r'a=0'],'Original linear independence modulo zero, not affine independence modulo constants. Assumption1 gives additional nondegeneracy in the theorem; do not silently rewrite Assumption3 as minimality.','Assumption 3 (Linear independence)',kind='assumption',context='Assumption 3 (Linear independence).',phrases=['Assumption 3'])
add(19,'Assumption 4',r'''Let $\mathcal P$ possess the product structure as in Theorem 6.4. For each $j\in[d]$, there exists two points $\theta_{j,+},\theta_{j,-}\in\Theta_j$ such that $1/(10n)\le H^2(p_{\theta_{j,+}},p_{\theta_{j,-}})\le1/(5n)$.''',[20],[2,15],[r'H^2(p_{\theta_{j,+}},p_{\theta_{j,-}})',r'1/(10n)'],'Original two-point Hellinger condition for the given sample size n. Its reference to6.4 imports product structure, not that theorem’s two separate TV bounds. It does not require continuity of the full parameter map.','Assumption 4',kind='assumption',context='Assumption 4.',phrases=['Assumption 4'])
add(20,'discrete distributions',r'''Consider the following class $\mathcal P_{d,t}$ of discrete distributions:
\[
\mathcal P_{d,t}=\left\{(p_0,\ldots,p_d):p_i\ge0,\sum_{i=0}^dp_i=1,p_0=t\right\},
\]
where it is the same as the class of all discrete distributions over $d+1$ points, except that the learner has the perfect knowledge of $p_0=t$ for some known $t\in[1/(2\sqrt d),1/2]$.''',[21],[],[r'\mathcal P_{d,t}',r'p_0=t'],'Original finite alphabet class with one known mass and all other masses unknown. There is no positivity restriction on the other masses.','Section 7.1 — Discrete distribution class')
add(21,'low-rank covariance estimation model',r'''Consider a low-rank covariance estimation model: $X_1,\ldots,X_n\sim\mathcal N(0,\Sigma)$, where $\Sigma\in\mathbb R^{p\times p}$ could be written as $\Sigma=UU^\top$ with $U\in\mathbb R^{p\times d}$ and $U^\top U=I_d$. In other words, the covariance matrix $\Sigma$ is isotropic on some $d$-dimensional subspace.''',[21],[],[r'\Sigma=UU^\top',r'U^\top U=I_d'],'Original unknown projection-covariance Gaussian model with ambient dimension p and intrinsic dimension d. This is distinct from the known-covariance unknown-mean family of6.2. All nonzero covariance eigenvalues equal1.','Section 7.2 — Low-rank covariance model',kind='source_passage')
add(22,'densities',r'''Let $\mathcal P$ be the class of all $L$-Lipschitz densities supported on $[0,1]$, i.e. the density $f$ satisfies $|f(x)-f(y)|\le L|x-y|$ for all $x,y\in[0,1]$.''',[22],[],[r'|f(x)-f(y)|\le L|x-y|'],'Original univariate Lipschitz density class; probability normalization is inherent in density. No positive lower bound is imposed in this base class.','Section 7.3 — Lipschitz densities')
add(23,'densities lower bounded',r'''For $c\in(0,1)$, also let $\mathcal P_c\subseteq\mathcal P$ be the subclass of densities lower bounded by $c$ everywhere, i.e. $f(x)\ge c$ for all $x\in[0,1]$.''',[22],[22],[r'\mathcal P_c\subseteq\mathcal P',r'f(x)\ge c'],'Original subclass of the same Lipschitz densities, with fixed positive pointwise lower bound. Do not merge its stronger condition into the base class.','Section 7.3 — Densities with a positive lower bound')
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D11']['highlight_symbols'] = ['\\left\\|(\\nabla^2A(\\theta))^{-1/2}(T(X)-\\nabla A(\\theta))\\right\\|_2^k', 'M_k']

def main():
    review=json.loads((REVIEW_ROOT/'inventory-review.json').read_text());assert review['status']=='complete' and review['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==review['inventory_sha256']
    assert len(interfaces)==len(members)==23
    for x in interfaces:
        m=x['members'][0];assert set(m['depends_on'])<=set(members)
        assert any(v in m['statement_original']+' '+m['local_label'] for v in m['highlight_symbols']+m['highlight_phrases'])
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved23 original source entries; full census review remains pending.')
if __name__=='__main__':main()
