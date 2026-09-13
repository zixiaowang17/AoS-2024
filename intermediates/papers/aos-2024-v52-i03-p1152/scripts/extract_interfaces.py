"""Extract the source-reviewed published spectral-EL prerequisites; appendices remain excluded."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID='aos-2024-v52-i03-p1152'
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
add('D1','weakly stationary real-valued stochastic process',r'''
Consider a weakly stationary real-valued stochastic process $\{X_t\}_{t\in\mathbb Z}$ with absolutely summable autocovariances and a corresponding spectral density $f:[-\pi,\pi]\to[0,\infty)$. Let $\theta\in\Theta\subseteq\mathbb R^p$ denote a spectral parameter of interest.
''',[5],'Section 3 — spectral process and parameter framework',kind='assumption',symbols=[r'\{X_t\}_{t\in\mathbb Z}',r'f:[-\pi,\pi]\to[0,\infty)'],shape='Real weakly stationary process with absolutely summable autocovariances, its spectral density and a finite-dimensional spectral parameter. The later fourth-order stationarity and mixing conditions strengthen this common framework; strict stationarity, linearity and zero mean are not imposed here.')
add('D2','spectral estimating functions',r'''
Denote a vector of spectral estimating functions as
\[
G_\theta(\lambda)\equiv(g_{1,\theta}(\lambda),\ldots,g_{p,\theta}(\lambda))^\intercal:[-\pi,\pi]\times\Theta\mapsto\mathbb R^p\tag{1}
\]
(to be integrated with respect to $f(\lambda)$, $\lambda\in[-\pi,\pi]$)
''',[5],'Section 3 — spectral estimating functions (1)',symbols=[r'G_\theta(\lambda)',r'g_{p,\theta}(\lambda)'],shape='Parameter-indexed vector of p frequency-domain estimating functions on [-pi,pi]. Theta is the parameter domain in the section setup. No bounded-variation or differentiability condition is part of this bare definition; those are recorded separately.')
add('D3','parametric vector of spectral moments',r'''
and let
\[
\mathcal M_\theta\equiv(m_1(\theta),\ldots,m_p(\theta))^\intercal:\Theta\mapsto\mathbb R^p
\]
denote a corresponding parametric vector of spectral moments.
''',[5],'Section 3 — spectral moment vector',symbols=[r'\mathcal M_\theta'],shape='General parameter-dependent spectral moment vector, using script M. It need not be the zero vector or equal theta. Its relationship to the estimating functions and true density is a separate moment condition.')
add('D4','spectral moment condition',r'''
As linked through the spectral density $f$, we then assume that $G_\theta$ and $\mathcal M_\theta$ satisfy the spectral moment condition
\[
\int_{-\pi}^\pi G_\theta(\lambda)f(\lambda)d\lambda=\mathcal M_\theta\tag{2}
\]
at the true value $\theta_0$ of the parameter.
''',[5],'Section 3 — spectral moment condition (2)',{'D1':'The moment is integrated against the true process spectral density f.','D2':'The integrand is the vector of spectral estimating functions.','D3':'The right-hand side is the general parametric moment vector.'},kind='assumption',symbols=[r'\int_{-\pi}^\pi G_\theta(\lambda)f(\lambda)d\lambda=\mathcal M_\theta'],shape='Equality required at the true parameter theta0, not an identity at every candidate theta. The moment vector may be nonzero, allowing more than normalized ratio parameters.')
add('D5','periodogram',r'''
Suppose data are available from an observed time stretch $X_1,\ldots,X_n$ of length $n$, and denote the periodogram as $I_n(\lambda)=(2\pi n)^{-1}\left|\sum_{t=1}^n X_t\exp(-\imath\lambda t)\right|^2$, where $\imath=\sqrt{-1}$ and $\lambda\in[-\pi,\pi]$.
''',[6],'Section 4.1 — full-data periodogram',{'D1':'The observed time stretch comes from the real-valued process in the common spectral framework.'},symbols=[r'I_n(\lambda)'],shape='Uncentered squared Fourier transform of the full observed stretch, normalized by 2*pi*n. The imaginary unit is distinct from the block index i. The empirical sums later omit the zero Fourier frequency.')
add('D6','empirical spectral average',r'''
Using $I_n(\cdot)$ in place of $f(\cdot)$, a standard empirical spectral average for estimating a spectral mean $\int_{-\pi}^\pi G_\theta(\lambda)f(\lambda)d\lambda$ from (2) is given by
\[
T_n(\theta)\equiv\frac{2\pi}n\sum_{|j|=1}^{\lfloor n/2\rfloor}G_\theta(\lambda_{j,n})I_n(\lambda_{j,n}),\qquad\theta\in\Theta,\tag{5}
\]
in Riemann sum form, where $\lambda_{j,n}\equiv2\pi j/n$, $1\le|j|\le\lfloor n/2\rfloor$, denote discrete Fourier frequencies and summation over $|j|$ denotes inclusion of both positive/negative frequencies.
''',[6],'Section 4.1 — full-data empirical spectral average (5)',{'D2':'The Riemann sum weights the periodogram by G_theta.','D5':'It uses the full-data periodogram I_n.'},symbols=[r'T_n(\theta)',r'\lambda_{j,n}'],shape='Riemann sum over both signs of every nonzero Fourier frequency up to floor(n/2). For even n the printed range includes both -pi and pi. It is the full-data average, distinct from the nonoverlapping block averages used to form SEL.')
add('D7','nonoverlapping (NOL)',r'''
For a block length $b<n$, the data are divided into $N\equiv\lfloor n/b\rfloor$ nonoverlapping (NOL) blocks/subsamples of length $b$ as $(X_{1+(i-1)b},\ldots,X_{ib})$, $i=1,\ldots,N$. The periodogram from the $i$th subsample, denoted as
\[
I_{i,\mathrm{NOL}}(\lambda)\equiv\frac1{2\pi b}\left|\sum_{s=1}^b X_{(i-1)b+s}e^{-\imath\lambda s}\right|^2,\qquad\lambda\in[-\pi,\pi],
\]
''',[6],'Section 4.1 — nonoverlapping blocks and periodograms',{'D1':'The blocks partition the observed time stretch of the process, up to the unused remainder after N full blocks.'},symbols=[r'N\equiv\lfloor n/b\rfloor',r'I_{i,\mathrm{NOL}}(\lambda)'],shape='N=floor(n/b) disjoint length-b blocks with their own periodograms, normalized by 1/(2*pi*b). The original construction uses only N full blocks; it does not require b to divide n.')
add('D8','empirical spectral average',r'''
is used for a subsample-analog of the empirical spectral average $T_n(\theta)$, $\theta\in\Theta$, from (5) as
\[
T_{i,\mathrm{NOL}}(\theta)\equiv\frac{2\pi}b\sum_{|j|=1}^{\lfloor b/2\rfloor}G_\theta(\lambda_{j,b})I_{i,\mathrm{NOL}}(\lambda_{j,b}),\qquad i=1,\ldots,N,
\]
where $\lambda_{j,b}\equiv2\pi j/b$, $1\le|j|\le\lfloor b/2\rfloor$; thus, $I_{i,\mathrm{NOL}}$ and $b$ from blocks replace $I_n$ and $n$ in (5).
''',[7],'Section 4.1 — nonoverlapping subsample spectral averages',{'D2':'The block-periodogram Riemann sum uses G_theta.','D7':'The periodogram and count of blocks are the nonoverlapping construction.'},symbols=[r'T_{i,\mathrm{NOL}}(\theta)'],shape='Block-scale spectral averages over the nonoverlapping periods. Mention of full-data T_n describes the analogous construction; the numerical value of T_n is not required to compute these block averages.')
add('D9','SEL function',r'''
To assess the plausibility of a given value of the spectral parameter $\theta\in\Theta$, we then define a SEL function for $\theta$ as
\[
L_n(\theta)\equiv\sup\left\{\prod_{i=1}^N p_i\ \middle|\ p_i\ge0,\ \sum_{i=1}^N p_i=1,\ \sum_{i=1}^N p_iT_{i,\mathrm{NOL}}(\theta)=\mathcal M_\theta\right\},\tag{6}
\]
by assigning probabilities $p_i$ to the subsample statistics, $p_i\longmapsto T_{i,\mathrm{NOL}}(\theta)$, under a mean constraint $\mathcal M_\theta$.

When the conditioning set in (6) is empty, we may define $L_n(\theta)=0$.
''',[7],'Section 4.1 — SEL probability profiling (6)',{'D8':'The likelihood profiles weights on nonoverlapping subsample spectral averages.','D3':'The weighted-mean constraint equals the general spectral moment vector.'},symbols=[r'L_n(\theta)',r'\sum_{i=1}^N p_iT_{i,\mathrm{NOL}}(\theta)=\mathcal M_\theta'],shape='Supremum of the product of N probability weights under an estimating-equation constraint. The convention for an empty feasible set is explicitly zero. This profiles subsample spectral averages, not individual time observations or individual full-periodogram ordinates.')
add('D10','SEL log-ratio statistic',r'''
Analogous to parametric likelihood, we then consider a SEL log-ratio statistic as
\[
\ell_n(\theta)\equiv-2\log[N^N L_n(\theta)].\tag{7}
\]
''',[7],'Section 4.1 — SEL log-ratio (7)',{'D9':'The log-ratio uses the constrained SEL likelihood, normalized against the unconstrained product N^{-N}.'},symbols=[r'\ell_n(\theta)'],shape='Minus twice the log of N^N times the SEL function. When the likelihood is zero, the extended-real log-ratio is infinite under the usual convention; finite-valued convergence is a theorem conclusion, not imposed on every sample.')
add('D11','mixing coefficient',r'''
Recall that the $\alpha$-mixing coefficient of a time series $\{X_t\}$ is given, for integer $k\ge1$, by $\alpha(k)\equiv\sup_{m\in\mathbb Z}\{|\mathbb P(A\cap B)-\mathbb P(A)\mathbb P(B)|:A\in\mathcal F_{-\infty}^m,B\in\mathcal F_{m+k}^\infty\}$, where $\mathcal F_{-\infty}^m$ and $\mathcal F_{m+k}^\infty$ denote, respectively, $\sigma$-algebras generated by random variables $X_j$, $j\le m$ and $X_j$, $j\ge m+k$; see [3], Ch. 16.
''',[8],'Section 4.2 — alpha-mixing coefficient',symbols=[r'\alpha(k)',r'\mathcal F_{m+k}^\infty'],shape='Strong mixing coefficient uniformly over time origins and past/future events. The supremum over event pairs is encoded in the source set-builder expression inside sup_m. Strict stationarity is not required to define this coefficient.')
add('D12','4th-order stationary series',r'''
$\{X_t\}_{t\in\mathbb Z}$ is a real-valued, 4th-order stationary series such that, for some $\delta>0$, $\sup_{t\in\mathbb Z}\mathbb E|X_t|^{4+\delta}<\infty$ and $\sum_{k=1}^\infty k^2\alpha(k)^{\delta/(4+\delta)}<\infty$.
''',[8],'Assumption 1',{'D11':'The summability restriction uses the alpha-mixing coefficient defined immediately above.'},kind='assumption',symbols=[r'\sup_{t\in\mathbb Z}\mathbb E|X_t|^{4+\delta}',r'k^2\alpha(k)^{\delta/(4+\delta)}'],shape='Fourth-order stationarity, a uniform 4+delta moment and weighted strong-mixing summability using the same positive delta. Neither strict stationarity nor an eighth moment nor linear-process structure is imposed.')
add('D13','bounded variation',r'''
At the true parameter $\theta_0\in\Theta\subset\mathbb R^p$ value, each component $g_{j,\theta_0}(\cdot):[-\pi,\pi]\mapsto\mathbb R$ of $G_{\theta_0}(\cdot)$ is of bounded variation, for $j=1,\ldots,p$.
''',[8],'Assumption 2',{'D2':'Bounded variation is required for each component of the spectral estimating vector at theta0.'},kind='assumption',symbols=[r'g_{j,\theta_0}(\cdot)',r'G_{\theta_0}(\cdot)'],phrases=['bounded variation'],shape='Componentwise bounded variation in frequency at the true parameter only. The assumption does not impose a uniform variation bound over a neighborhood of all theta, nor differentiability in frequency.')
add('D14','4th-order cumulant density',r'''
and $f_4(\lambda_1,\lambda_2,\lambda_3)\equiv(2\pi)^{-3}\sum_{h_1,h_2,h_3\in\mathbb Z}\operatorname{cum}(X_0,X_{h_1},X_{h_2},X_{h_3})e^{-\imath(\lambda_1h_1+\lambda_2h_2+\lambda_3h_3)}$ denotes the 4th-order cumulant density of the process.
''',[8],'Assumption 3 — fourth-order cumulant density definition',{'D1':'The cumulants are those of the real-valued time process in the spectral setup.'},symbols=[r'f_4(\lambda_1,\lambda_2,\lambda_3)'],shape='Triple Fourier series of fourth-order cumulants with factor (2*pi)^{-3} and negative imaginary exponent. The standard cumulant notion is ambient; Assumption 1 supplies the moments in theorem applications. No Gaussian or independent-innovation simplification is inserted.')
add('D15','positive definite',r'''
The $p\times p$ matrix $V_{\theta_0}\equiv V_{\theta_0,1}+V_{\theta_0,2}$ is positive definite, where
\[
\begin{aligned}
V_{\theta_0,1}&\equiv2\pi\int_{-\pi}^\pi G_{\theta_0}(\lambda)(G_{\theta_0}(\lambda)+G_{\theta_0}(-\lambda))^\intercal f(\lambda)^2d\lambda,\\
V_{\theta_0,2}&\equiv2\pi\int_{-\pi}^\pi\int_{-\pi}^\pi G_{\theta_0}(\lambda_1)G_{\theta_0}(\lambda_2)^\intercal f_4(\lambda_1,\lambda_2,-\lambda_2)d\lambda_1d\lambda_2,
\end{aligned}\tag{9}
\]
''',[8],'Assumption 3 — spectral covariance nonsingularity',{'D1':'The first contribution uses the squared process spectral density.','D2':'Both covariance contributions use the vector G at the true parameter.','D14':'The second contribution uses the fourth-order cumulant density at (lambda1,lambda2,-lambda2).'},kind='assumption',symbols=[r'V_{\theta_0}',r'V_{\theta_0,2}'],phrases=['positive definite'],shape='Positive definiteness of the sum V_theta0, not separate positive definiteness of its two contributions. Both terms and the reflected-frequency vector are retained. The second contribution need not vanish for the allowed nonlinear processes.')
add('D16','spectral M-estimator',r'''
Based on $T_n(\theta)$ and the spectral moment condition (2), we define a spectral M-estimator $\widehat\theta_n$ as the solution to
\[
T_n(\theta)=\mathcal M_\theta.\tag{11}
\]
''',[10],'Section 5.1 — spectral M-estimator (11)',{'D6':'The estimating equation uses the full-data spectral average.','D3':'Its right-hand side is the parameter-dependent spectral moment vector.'},symbols=[r'\widehat\theta_n',r'T_n(\theta)=\mathcal M_\theta'],shape='Root of the full-periodogram estimating equation. Theorem 2 asserts existence of a consistent asymptotically normal solution sequence, not uniqueness or those properties for every root.')
add('D17','regularity conditions',r'''
suppose the following regularity conditions in a neighborhood of $\theta_0$ satisfying (2): (i) partial derivatives $\partial G_\theta(\cdot)/\partial\theta$, $\partial^2G_\theta(\cdot)/\partial\theta\partial\theta^\intercal$, $\partial\mathcal M_\theta/\partial\theta$ and $\partial^2\mathcal M_\theta/\partial\theta\partial\theta^\intercal$ exist; (ii) each component $\partial g_{i,\theta_0}(\cdot)/\partial\theta_j$ of $\partial G_{\theta_0}(\cdot)/\partial\theta$ is Riemann integrable for $i,j=1,\ldots,p$; (iii) $\|\partial\mathcal M_\theta/\partial\theta\|$, $\|\partial^2\mathcal M_\theta/\partial\theta\partial\theta^\intercal\|$ are bounded, and $\|\partial G_\theta(\cdot)/\partial\theta\|$, $\|\partial^2G_\theta(\cdot)/\partial\theta\partial\theta^\intercal\|$ are bounded by a Riemann integrable function $H(\cdot):[-\pi,\pi]\mapsto\mathbb R^+$; and (iv) $D_{\theta_0}\equiv\int_{-\pi}^\pi[\partial G_{\theta_0}(\lambda)/\partial\theta]f(\lambda)d\lambda-\partial\mathcal M_{\theta_0}/\partial\theta$ is nonsingular.
''',[10],'Theorem 2 — regularity conditions (i)–(iv)',{'D2':'The derivatives are of the spectral estimating functions.','D3':'The bounded derivatives and subtraction in D_theta0 involve the general moment vector.','D1':'The Jacobian integral is weighted by the process spectral density.','D4':'The neighborhood is around a true parameter satisfying moment condition (2).'},kind='condition',symbols=[r'D_{\theta_0}',r'H(\cdot):[-\pi,\pi]\mapsto\mathbb R^+'],shape='All four neighborhood regularity conditions, including parameter derivatives through order two, componentwise Riemann integrability at theta0, integrable derivative envelopes, and nonsingularity of the moment-equation Jacobian. These supplement, rather than replace, Assumptions 1–3.')
add('D18','OL block',r'''
where $I_{i,\mathrm{OL}}(\lambda)\equiv(2\pi/b)|\sum_{s=1}^b X_{s-1+i}e^{-\imath\lambda s}|^2$ denotes the periodogram from the $i$th OL block $(X_i,\ldots,X_{i+b-1})$, $i=1,\ldots,n-b+1$.
''',[12],'Section 5.2 — overlapping blocks and their printed periodogram',{'D1':'The overlapping windows are taken from the observed process.'},symbols=[r'I_{i,\mathrm{OL}}(\lambda)'],shape='All n-b+1 consecutive length-b overlapping blocks. The printed periodogram prefactor is 2*pi/b, unlike the NOL prefactor 1/(2*pi*b). Preserve the original formula and flag its normalization mismatch.',note='PDF 12 literally prints (2π/b) before the squared Fourier sum; PDF 6 uses 1/(2πb) for the nonoverlapping periodogram. The factor differs by 4π². No silent correction or claim that the two normalizations agree is made.')
add('D19','subsample statistics',r'''
\[
T_{i,\mathrm{OL}}(\widehat\theta_n)\equiv\frac{2\pi}b\sum_{|j|=1}^{\lfloor b/2\rfloor}G_{\widehat\theta_n}(\lambda_{j,b})I_{i,\mathrm{OL}}(\lambda_{j,b}),
\]
''',[12],'Section 5.2 — overlapping subsample spectral average',{'D2':'The overlapping-periodogram sum is weighted by the spectral estimating functions at its argument.','D18':'It uses the overlapping block periodogram and its printed normalization.'},symbols=[r'T_{i,\mathrm{OL}}(\widehat\theta_n)'],context=r'Using the spectral M-estimator $\widehat\theta_n$ in place of the true parameter $\theta_0$ (Section 5.1), define a collection of overlapping (OL) subsample statistics from the data $X_1,\ldots,X_n$ as',shape='Overlapping-block spectral-average function, first displayed at the fitted parameter. Section 7 explicitly reuses the same block statistic as a function of every theta; that function itself does not require fitting theta. The evaluated collection is recorded separately.')
members['D19']['application_context']=[dict(text=r'For given value of $\theta$, we then create a collection of overlapping (OL) periodogram sub-averages $\{T_{i,\mathrm{OL}}(\theta),\theta\in\Theta\}_{i=1}^{n-b+1}$, noting that the $i$th OL data block $(X_i,\ldots,X_{i+b-1})$ of length $b$ determines $T_{i,\mathrm{OL}}(\theta)$ as a function of $\theta$.',evidence=[dict(page=19,location='Section 7 — block statistic as a function of theta')])]
add('D20','overlapping (OL) subsample statistics',r'''
Using the spectral M-estimator $\widehat\theta_n$ in place of the true parameter $\theta_0$ (Section 5.1), define a collection of overlapping (OL) subsample statistics from the data $X_1,\ldots,X_n$ as
\[
\mathcal C_{\mathrm{OL}}\equiv\{T_{i,\mathrm{OL}}(\widehat\theta_n):i=1,\ldots,n-b+1\},
\]
''',[12],'Section 5.2 — fitted overlapping-block collection',{'D19':'The collection consists of the overlapping spectral-average statistics.','D16':'Each statistic is evaluated at the spectral M-estimator.'},symbols=[r'\mathcal C_{\mathrm{OL}}'],shape='Empirical collection indexed by all overlapping windows and evaluated at the full-data fitted parameter. Repeated values retain their block multiplicities when sampled; the braces do not justify deduplicating the empirical collection.')
add('D21','i.i.d. draws',r'''
We then take $N$ i.i.d. draws from the OL collection $\mathcal C_{\mathrm{OL}}$, as $\{T_{i,\mathrm{OL}}^*(\widehat\theta_n)\}_{i=1}^N$, to serve as bootstrap counterparts to $\{T_{i,\mathrm{NOL}}(\theta_0)\}_{i=1}^N$,
''',[12],'Section 5.2 — resampling the fitted overlapping collection',{'D20':'The draws are from the fitted overlapping-block collection.','D7':'The number of independent draws is the count N=floor(n/b) of nonoverlapping blocks.'},symbols=[r'\{T_{i,\mathrm{OL}}^*(\widehat\theta_n)\}_{i=1}^N'],shape='N conditionally independent draws from the empirical overlapping collection, retaining block multiplicities. Uses the same block length as SEL. The sampled objects are spectral averages, not a reconstructed time series.')
add('D22','bootstrap analog',r'''
and define the bootstrap analog of the SEL ratio $\ell_n(\theta_0)=-2\log[N^N L_n(\theta_0)]$ as $\ell_n^*(\widehat\theta_n)=-2\log[N^N L_n^*(\widehat\theta_n)]$ for
\[
L_n^*(\widehat\theta_n)=\sup\left\{\prod_{i=1}^N p_i:p_i\ge0,\ \sum_{i=1}^N p_i=1,\ \sum_{i=1}^N p_iT_{i,\mathrm{OL}}^*(\widehat\theta_n)=\mathcal M_{\widehat\theta_n}\right\}.
\]
The above bootstrap likelihood $L_n^*(\widehat\theta_n)$ uses the spectral moment $\mathcal M_{\widehat\theta_n}=T_n(\widehat\theta_n)$, based on (11) and the spectral M-estimator $\widehat\theta_n$, in analog to the moment $\mathcal M_{\theta_0}$ defining the SEL function $L_n(\theta_0)$ from (6) at $\theta_0$.
''',[12],'Section 5.2 — bootstrap SEL likelihood and log-ratio',{'D21':'The probability weights are assigned to the resampled overlapping spectral averages.','D3':'The mean constraint uses the moment vector evaluated at the fitted parameter.','D16':'The fit and its estimating equation determine the bootstrap moment target.'},symbols=[r'\ell_n^*(\widehat\theta_n)',r'L_n^*(\widehat\theta_n)'],shape='Bootstrap likelihood and log-ratio with fitted moment target. The original baseline ratio is recalled for comparison; its random numerical value is not an input into the explicitly defined bootstrap objective. Stars on likelihood/statistic are superscripts, whereas the bootstrap probability in Theorems has subscript star.')
add('D23','smooth function parameter',r'''
The SEL function $L_n(\theta)$ for $\theta$ leads to a natural SEL function and log-ratio for a value of the smooth function parameter $\vartheta=h(\theta)$ as
\[
L_n(\vartheta)\equiv\max\{L_n(\theta):h(\theta)=\vartheta\},\qquad\ell_n(\vartheta)\equiv-2\log[N^N L_n(\vartheta)].
\]
''',[19],'Section 7 — SEL profiling for a smooth function parameter',{'D9':'The profile maximizes the original SEL function over the fiber of h.'},symbols=[r'L_n(\vartheta)',r'\ell_n(\vartheta)'],shape='Profile likelihood and log-ratio for h(theta), using the original max rather than replacing it by sup. Theorem 4 specifies h:R^p→R^s; its Jacobian rank supplies chi-square degrees of freedom. Section 7 states s<=p and theta in R^p, consistently with the theorem.')
add('D24','estimator',r'''
To approximate the distribution of $\ell_n(\vartheta_0)$ with the SELB procedure, we initially compute an estimator $\widehat\vartheta_n\equiv h(\widehat\theta_n)$ using the smooth function $h(\cdot)$ of a spectral M-estimator $\widehat\theta_n$ for $\theta$ from (11), where $\widehat\vartheta_n$ then plays the role of the true parameter $\vartheta_0$ in the bootstrap.
''',[19],'Section 7 — fitted smooth function parameter',{'D16':'The smooth function is applied to the full-data spectral M-estimator.'},symbols=[r'\widehat\vartheta_n\equiv h(\widehat\theta_n)'],shape='Plug-in smooth function of the spectral M-estimator. The function h is a theorem-local input, and no extra profile optimization defines this fitted target.')
add('D25','OL block statistics',r'''
For given value of $\theta$, we then create a collection of overlapping (OL) periodogram sub-averages $\{T_{i,\mathrm{OL}}(\theta),\theta\in\Theta\}_{i=1}^{n-b+1}$, noting that the $i$th OL data block $(X_i,\ldots,X_{i+b-1})$ of length $b$ determines $T_{i,\mathrm{OL}}(\theta)$ as a function of $\theta$. By independently resampling $N\equiv\lfloor n/b\rfloor$ OL block statistics from this collection, we obtain a bootstrap version $\{T_{i,\mathrm{OL}}^*(\theta),\theta\in\Theta\}_{i=1}^N$ of the nonoverlapping (NOL) periodogram sub-averages $\{T_{i,\mathrm{NOL}}(\theta),\theta\in\Theta\}_{i=1}^N$ that build $L_n(\theta)$. This produces a bootstrap rendition $L_n^*(\theta)$ of $L_n(\theta)$, $\theta\in\Theta$,
''',[19],'Section 7 — resampling entire block-statistic functions',{'D19':'Each resampled object is the overlapping statistic as a function of theta, explicitly reusing the earlier construction.','D7':'The resampling count is N=floor(n/b).','D9':'The SEL objective is applied to the resampled block-statistic functions to define the likelihood process.'},symbols=[r'\{T_{i,\mathrm{OL}}^*(\theta),\theta\in\Theta\}_{i=1}^N'],shape='Resample whole theta-indexed block-statistic functions with shared block indices across theta, then form the SEL likelihood process. This is not independent resampling afresh at every theta and does not depend on the single fitted-parameter collection in Section 5.2.')
add('D26','bootstrap analogs',r'''
and then bootstrap analogs
\[
L_n^*(\widehat\vartheta_n)\equiv\max\{L_n^*(\theta):h(\theta)=\widehat\vartheta_n\},\qquad\ell_n^*(\widehat\vartheta_n)\equiv-2\log[N^N L_n^*(\widehat\vartheta_n)],
\]
of the SEL function $L_n(\vartheta_0)$ and log-ratio $\ell_n(\vartheta_0)$ at the true value $\vartheta_0$ of the spectral parameter.
''',[19],'Section 7 — bootstrap smooth-function profile likelihood and log-ratio',{'D25':'The profile uses the bootstrap likelihood process over the whole parameter domain.','D24':'Its constraint equals the fitted smooth function parameter.'},symbols=[r'L_n^*(\widehat\vartheta_n)',r'\ell_n^*(\widehat\vartheta_n)'],shape='Bootstrap profile maximum over the h-fiber at the fitted smooth parameter, with the same N^N log-ratio normalization. It uses function-valued resampling so all candidate theta values share one bootstrap experiment.')

def main():
    for lid,m in members.items():
        assert all(d in members for d in m['depends_on']),(lid,'unknown dependency')
        assert any(s in m['statement_original']+' '+m['local_label'] for s in m['highlight_symbols']+m['highlight_phrases']),(lid,'missing own-source highlight')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source passages and their local dependencies; source audit remains pending.')

if __name__=="__main__":main()
