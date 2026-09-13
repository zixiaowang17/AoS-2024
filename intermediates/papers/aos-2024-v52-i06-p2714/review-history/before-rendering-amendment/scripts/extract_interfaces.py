"""Preserve original SKS, MAP and marginal source definitions and assumptions."""
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
add(1,'parametric family of distributions',r'''We denote with $\{X_i\}_{i=1}^n$, $n\in\mathbb N$, a sequence of random variables with unknown true distribution $P_0^n$. Moreover, let $\mathcal P_\Theta=\{P_\theta^n,\theta\in\Theta\}$, with $\Theta\subseteq\mathbb R^d$, be a parametric family of distributions. In the following, we assume that there exists a common $\sigma$–finite measure $\mu^n$ which dominates $P_0^n$ as well as all measures $P_\theta^n$, and we denote by $p_0^n$ and $p_\theta^n$ the corresponding density functions.''',[5],[],[r'\mathcal P_\Theta',r'P_0^n',r'p_\theta^n'],'Dominated statistical experiment indexed by n. No iid or correct-specification condition is imposed.','Section 1.1 — Statistical experiment',kind='source_passage')
add(2,'Kullback–Leibler projection',r'''The Kullback–Leibler projection $P_{\theta_*}^n$ of $P_0^n$ on $\mathcal P_\Theta$ is defined as $P_{\theta_*}^n=\operatorname{argmin}_{P_\theta^n\in\mathcal P_\Theta}\operatorname{KL}(P_0^n\|P_\theta^n)$ where $\operatorname{KL}(P_0^n\|P_\theta^n)$ denotes the Kullback–Leibler divergence between $P_0^n$ and $P_\theta^n$.''',[5],[1],[r'P_{\theta_*}^n',r'\operatorname{KL}(P_0^n\|P_\theta^n)'],'Original model projection. Existence, parameter-level uniqueness and possible dependence of the minimizing parameter on n remain separate from this notation.','Section 1.1 — Kullback–Leibler projection')
add(3,'log–likelihood',r'''The log–likelihood of the, possibly misspecified, model is $\ell(\theta)=\ell(\theta,X^n)=\log p_\theta^n(X^n)$.''',[5],[1],[r'\ell(\theta,X^n)',r'\log p_\theta^n(X^n)'],'Log-likelihood for the supplied statistical experiment; misspecification is allowed.','Section 1.1 — Log-likelihood')
add(4,'Prior and posterior distributions',r'''Prior and posterior distributions are denoted by $\Pi(\cdot)$ and $\Pi_n(\cdot)$, whereas the corresponding densities are indicated with $\pi(\cdot)$ and $\pi_n(\cdot)$, respectively.''',[5],[3],[r'\Pi_n(\cdot)',r'\pi_n(\cdot)',r'\pi(\cdot)'],'Original prior/posterior notation. The posterior is for the stated model likelihood and prior; its usual Bayes construction and subsequent coordinate pushforwards are ambient interpretation, not added source formulas.','Section 1.1 — Prior and posterior distributions')
add(5,'derivatives',r'''Leveraging the above notation, the score vector evaluated at $\theta_*$ is defined as
\[
\ell_{\theta_*}^{(1)}=[\ell_s^{(1)}(\theta)]|_{\theta=\theta_*}=[(\partial/\partial\theta_s)\ell(\theta)]|_{\theta=\theta_*}\in\mathbb R^d,
\]
whereas, the second, third and fourth order derivatives of $\ell(\theta)$, still evaluated at $\theta_*$, are
\[
\ell_{\theta_*}^{(2)}=[\ell_{st}^{(2)}(\theta)]|_{\theta=\theta_*}=[\partial/(\partial\theta_s\partial\theta_t)\ell(\theta)]|_{\theta=\theta_*}\in\mathbb R^{d\times d},
\]
\[
\ell_{\theta_*}^{(3)}=[\ell_{stl}^{(3)}(\theta)]|_{\theta=\theta_*}=[\partial/(\partial\theta_s\partial\theta_t\partial\theta_l)\ell(\theta)]|_{\theta=\theta_*}\in\mathbb R^{d\times d\times d},
\]
\[
\ell_{\theta_*}^{(4)}=[\ell_{stlk}^{(4)}(\theta)]|_{\theta=\theta_*}=[\partial/(\partial\theta_s\partial\theta_t\partial\theta_l\partial\theta_k)\ell(\theta)]|_{\theta=\theta_*}\in\mathbb R^{d\times d\times d\times d},
\]
where all the indexes in the above definitions and in the subsequent ones go from $1$ to $d$.''',[5],[2,3],[r'\ell_{stl}^{(3)}(\theta)',r'\ell_{stlk}^{(4)}(\theta)'],'Source derivative arrays and their original evaluation convention; later the evaluation point is the MAP. Preserve the printed single partial numerator rather than silently changing notation. These arrays are distinct from the abstract expansion coefficients in Assumption2.','Section 1.1 — Log-likelihood derivatives')
add(6,'Fisher information',r'''$J_{\theta_*}=[j_{st}]=-[\ell_{\theta_*,st}^{(2)}]\in\mathbb R^{d\times d}$''',[6],[5],[r'J_{\theta_*}',r'j_{st}'],'Observed information is the negative likelihood Hessian. The same notation evaluated at the MAP is used in Eq22; it is not the full posterior Hessian. Expected Fisher information is separate auxiliary context.','Section 1.1 — Observed Fisher information',context='The observed and expected Fisher information are denoted by')
add(7,'derivatives of the log–prior density',r'''In addition,
\[
\log\pi_{\theta_*}^{(1)}=[\log\pi(\theta)_s^{(1)}]|_{\theta=\theta_*}=[\partial/(\partial\theta_s)\log\pi(\theta)]|_{\theta=\theta_*}\in\mathbb R^d,
\]
\[
\log\pi_{\theta_*}^{(2)}=[\log\pi(\theta)_{st}^{(2)}]|_{\theta=\theta_*}=[\partial/(\partial\theta_s\partial\theta_t)\log\pi(\theta)]|_{\theta=\theta_*}\in\mathbb R^{d\times d},
\]
represent the first two derivatives of the log–prior density, evaluated at $\theta_*$.''',[6],[2,4],[r'\log\pi_{\theta_*}^{(2)}',r'\log\pi(\theta)_{st}^{(2)}'],'Original log-prior derivatives. Assumption10 bounds these at generic local points; Assumption3 instead introduces its own abstract first-order coefficient and does not require this differentiability definition.','Section 1.1 — Log-prior derivatives')
add(8,'norming rate',r'''Let $\delta_n\to0$ be a generic norming rate governing the posterior contraction toward $\theta_*$. Consistent with standard Bernstein–von Mises type theory (see e.g., Van der Vaart, 2000; Kleijn and van der Vaart, 2012), consider the re–parametrization $h=\delta_n^{-1}(\theta-\theta_*)\in\mathbb R^d$.''',[6],[2],[r'\delta_n\to0',r'h=\delta_n^{-1}(\theta-\theta_*)'],'General norming sequence and local coordinate. It is not automatically n^{-1/2}; MAP centering is separately recorded.','Section 2 — Norming rate and reparametrization')
add(9,'univariate cumulative distribution function',r'''Moreover, let $F(\cdot):\mathbb R\to[0,1]$ denote any univariate cumulative distribution function which satisfies $F(-x)=1-F(x)$ and $F(x)=1/2+\eta x+O(x^2)$, $x\to0$, for some $\eta\in\mathbb R$.''',[6],[],[r'F(-x)=1-F(x)',r'F(x)=1/2+\eta x+O(x^2)'],'Original admissible skewing CDF. Eta is printed in R although later polynomials divide by eta; preserve that unresolved zero-slope case.','Section 2 — Skewing CDF')
add(10,'SKS approximating densities',r'''Then, the class of SKS approximating densities $p_{\mathrm{SKS}}^n(h)$ we derive and study has the general form
\[
p_{\mathrm{SKS}}^n(h)=2\phi_d(h;\xi,\Omega)w(h-\xi)=2\phi_d(h;\xi,\Omega)F(\alpha_\eta(h-\xi)),\tag{1}
\]
with $P_{\mathrm{SKS}}^n(S)=\int_Sp_{\mathrm{SKS}}^n(h)\,\mathrm dh$ denoting the associated cumulative distribution function. In (1), $\phi_d(\cdot;\xi,\Omega)$ is the density of a $d$–variate Gaussian with mean vector $\xi$ and covariance matrix $\Omega$, while the function $w(h-\xi)\in(0,1)$ is responsible for inducing skewness, and takes the form $w(h-\xi)=F(\alpha_\eta(h-\xi))$, where $\alpha_\eta(\cdot):\mathbb R^d\to\mathbb R$ denotes a third order odd polynomial depending on the parameter that regulates the expansion of $F(\cdot)$, i.e., $\eta$.''',[6,7],[9],[r'p_{\mathrm{SKS}}^n(h)',r'\alpha_\eta(h-\xi)'],'Generic Gaussian-times-skewing density, with parameters supplied in Theorem2.1. Preserve the source open interval for w and measure/cdf wording. No regular-parametric derivative formulas are imported by the generic definition.','Section 2 — SKS density (1)')
add(11,'Kullback–Leibler projection',r'''The Kullback–Leibler projection $\theta_*\in\Theta$ is unique.''',[9],[2],[r'\theta_*\in\Theta'],'Original uniqueness assumption on the projection parameter. It is not redefined as a correctly specified truth.','Assumption 1',kind='assumption',phrases=['Assumption 1'])
add(12,'random vectors',r'''There exists a sequence of $d$-dimensional random vectors $\Delta_{\theta_*}^n=O_{P_0^n}(1)$, a sequence of $d\times d$ random matrices $V_{\theta_*}^n=[v_{st}^n]$ with $v_{st}^n=O_{P_0^n}(1)$, and also a sequence of $d\times d\times d$ random arrays $a_{\theta_*}^{(3),n}=[a_{\theta_*,stl}^{(3),n}]$ with $a_{\theta_*,stl}^{(3),n}=O_{P_0^n}(1)$, so that
\[
\log\frac{p_{\theta_*+\delta_nh}^n}{p_{\theta_*}^n}(X^n)-h_sv_{st}^n\Delta_{\theta_*,t}^n+\frac12v_{st}^nh_sh_t-\frac{\delta_n}6a_{\theta_*,stl}^{(3),n}h_sh_th_l=r_{n,1}(h),
\]
with $r_{n,1}:=\sup_{h\in K_n}|r_{n,1}(h)|=O_{P_0^n}(\delta_n^2M_n^{c_1})$, for some positive constant $c_1>0$, where $K_n=\{\|\theta-\theta_*\|\le M_n\delta_n\}$. In addition, there are two positive constants $\eta_1^*$ and $\eta_2^*$ such that the event $A_{n,0}=\{\lambda_{\mathrm{MIN}}(V_{\theta_*}^n)>\eta_1^*\}\cap\{\lambda_{\mathrm{MAX}}(V_{\theta_*}^n)<\eta_2^*\}$, holds with $P_0^nA_{n,0}=1-o(1)$.''',[9],[1,2,8,14],[r'\Delta_{\theta_*}^n',r'V_{\theta_*}^n',r'a_{\theta_*,stl}^{(3),n}',r'r_{n,1}(h)'],'Full abstract third-order local likelihood expansion, coefficient bounds, remainder and eigenvalue event. Preserve its K_n coordinate mismatch; do not identify the coefficients with actual derivatives or require Assumptions5–6.','Assumption 2',kind='assumption',phrases=['Assumption 2'])
add(13,'vector',r'''There exists a $d$–dimensional vector $\log\pi^{(1)}=[\log\pi_s^{(1)}]$ such that
\[
\log\pi(\theta_*+\delta_nh)/\pi(\theta_*)-\delta_nh_s\log\pi_s^{(1)}=r_{n,2}(h),
\]
with $\log\pi_s^{(1)}=O(1)$ and $r_{n,2}:=\sup_{h\in K_n}|r_{n,2}(h)|=O(\delta_n^2M_n^{c_2})$ for some constant $c_2>0$.''',[9],[2,4,8,14],[r'\log\pi^{(1)}',r'r_{n,2}(h)'],'Full prior expansion with its abstract vector coefficient and deterministic remainder. Preserve printed log/ratio scope; smoothness via Assumption7 is sufficient background, not a dependency of this assumption.','Assumption 3',kind='assumption',phrases=['Assumption 3'])
add(14,'notation',r'''For convenience, let us introduce the notation $M_n=\sqrt{c_0\log\delta_n^{-1}}$, with $c_0>0$ a constant to be specified later.

$K_n=\{\|\theta-\theta_*\|\le M_n\delta_n\}$.''',[9],[8],[r'M_n=\sqrt{c_0\log\delta_n^{-1}}',r'K_n=\{\|\theta-\theta_*\|\le M_n\delta_n\}'],'Original logarithmic radius notation and set definition excerpted from Assumption2. This shared definition is separate from the likelihood-expansion hypothesis so Assumption3 does not inherit that hypothesis.','Section 2.2 and Assumption 2 — Local radius and set',kind='source_passage')
add(15,'posterior distribution',r'''It holds $\lim_{\delta_n\to0}P_0^n\{\Pi_n(\|\theta-\theta_*\|>M_n\delta_n)<\delta_n^2\}=1$.''',[9],[2,4,8,14],[r'\Pi_n(\|\theta-\theta_*\|>M_n\delta_n)'],'Original posterior tail probability condition at the generic norming rate. Preserve probability-of-posterior-probability nesting and the strict inequalities.','Assumption 4',kind='assumption',context='Together with Assumption 4, it guarantees that asymptotically the posterior distribution concentrates in the region where the two expansions in Assumptions 2–3 hold with negligible remainders.',context_page=10,phrases=['Assumption 4'])
add(16,'log–prior density',r'''The log–prior density $\log\pi(\theta)$ is two times continuously differentiable in a neighborhood of $\theta_*$, and $0<\pi(\theta_*)<\infty$.''',[15],[2,4],[r'\log\pi(\theta)',r'0<\pi(\theta_*)<\infty'],'Twice continuously differentiable local log prior with positive finite density at the projection. Distinct from the abstract Assumption3 expansion.','Assumption 7',kind='assumption',phrases=['Assumption 7'])
add(17,'log–likelihood ratio',r'''For every sequence $M_n\to\infty$ there exists a constant $c_5>0$ such that $\lim_{n\to\infty}P_0^n\{\sup_{\|\theta-\theta_*\|>M_n/\sqrt n}\{(\ell(\theta)-\ell(\theta_*))/n\}<-c_5M_n^2/n\}=1$.''',[15],[2,3],[r'\sup_{\|\theta-\theta_*\|>M_n/\sqrt n}',r'-c_5M_n^2/n'],'Uniform likelihood separation beyond every diverging-radius root-n neighborhood. M_n here is a quantified arbitrary sequence, not a dependency on the specific general-theorem radius.','Assumption 8',kind='assumption',context='Assumption 8 which allows precise control on the behavior of the log–likelihood ratio outside the set $K_n$.',context_page=18,phrases=['Assumption 8'])
add(18,'MAP',r'''$\widehat\theta=\operatorname{argmax}_{\theta\in\Theta}\{\ell(\theta)+\log\pi(\theta)\}$''',[21],[3,4],[r'\widehat\theta=\operatorname{argmax}'],'Original posterior-mode estimator. Selection/existence and the interior first-order condition are not automatic for a constrained argmax.','Section 4.1 — MAP estimator',context='where the unknown $\theta_*$ is replaced by the MAP')
add(19,'rescaled parameter',r'''the rescaled parameter $\widehat h=\sqrt n(\theta-\widehat\theta)\in\mathbb R^d$''',[21],[18],[r'\widehat h=\sqrt n(\theta-\widehat\theta)'],'Root-n coordinate centered at the MAP, distinct from the general pseudo-true-parameter rescaling.','Section 4.1 — Rescaled parameter')
add(20,'precision matrix',r'''$\widehat\Omega=(\widehat V^n)^{-1}$ with $\widehat V^n=[\widehat v_{st}^n]=[j_{\widehat\theta,st}/n]\in\mathbb R^{d\times d}$''',[21],[6,18],[r'\widehat\Omega=(\widehat V^n)^{-1}',r'j_{\widehat\theta,st}/n'],'MAP-evaluated likelihood precision and its inverse. Keep this definition separate from Assumption10 positivity/boundedness so no artificial dependency cycle is created.','Section 4.1 — Gaussian covariance and precision',context='in the expression for the precision matrix of the Gaussian density factor in (22) the additional term including the third order derivative disappears.')
add(21,'skew–modal approximation',r'''\[
\widehat p_{\mathrm{SKS}}^n(\widehat h)=2\phi_d(\widehat h;0,\widehat\Omega)\widehat w(\widehat h)=2\phi_d(\widehat h;0,\widehat\Omega)F(\widehat\alpha_\eta(\widehat h)),\tag{22}
\]
where $\widehat\Omega=(\widehat V^n)^{-1}$ with $\widehat V^n=[\widehat v_{st}^n]=[j_{\widehat\theta,st}/n]\in\mathbb R^{d\times d}$, while the skewing function entering the univariate cdf $F(\cdot)$ is defined as $\widehat\alpha_\eta(\widehat h)=\{1/(12\eta\sqrt n)\}(\ell_{\widehat\theta,stl}^{(3)}/n)\widehat h_s\widehat h_t\widehat h_l\in\mathbb R$.''',[21],[5,9,18,19,20],[r'\widehat p_{\mathrm{SKS}}^n(\widehat h)',r'\widehat\alpha_\eta(\widehat h)'],'Complete joint skew-modal density, its likelihood covariance and cubic skewing factor. This is not the derivative-at-the-projection density in Eq2.','Section 4.1 — Skew-modal approximation (22)',context='For this reason, such a solution is referred to as skew–modal approximation.')
add(22,'event',r'''For every $M_n\to\infty$, the event $\widehat A_{n,0}=\{\|\widehat\theta-\theta_*\|\le M_n\sqrt d/\sqrt n\}$ satisfies $P_0^n(\widehat A_{n,0})>1-\widehat\epsilon_{n,0}$ for some sequence $\{\widehat\epsilon_{n,0}\}_{n=1}^\infty$ converging to zero.''',[21],[2,18],[r'\widehat A_{n,0}',r'M_n\sqrt d/\sqrt n'],'MAP proximity event for every diverging sequence. Keep sqrt(d), strict probability bound and the separate vanishing error sequence.','Assumption 9',kind='assumption',phrases=['Assumption 9'])
add(23,'spectral norm',r'''There exist two positive constants $\bar\eta_1$, $\bar\eta_2$ such that the event $\widehat A_{n,1}=\{\lambda_{\mathrm{MIN}}(\widehat\Omega^{-1})>\bar\eta_1\}\cap\{\lambda_{\mathrm{MAX}}(\widehat\Omega^{-1})<\bar\eta_2\}$ holds with a probability $P_0^n(\widehat A_{n,1})>1-\widehat\epsilon_{n,1}$ for a suitable sequence $\{\widehat\epsilon_{n,1}\}_{n=1}^\infty$ converging to zero as $n\to\infty$. Moreover, there exist positive constants $\delta>0$ and $L_3>0$, $L_4>0$, $L_{\pi,2}>0$ such that, for $B_\delta(\widehat\theta):=\{\theta\in\Theta:\|\widehat\theta-\theta\|<\delta\}$, the joint event $\widehat A_{n,2}=\{\sup_{\theta\in B_\delta(\widehat\theta)}\|\log\pi^{(2)}(\theta)\|<L_{\pi,2}\}\cap\{\sup_{\theta\in B_\delta(\widehat\theta)}\|\ell^{(3)}(\theta)/n\|<L_3\}\cap\{\sup_{\theta\in B_\delta(\widehat\theta)}\|\ell^{(4)}(\theta)/n\|<L_4\}$, holds with a probability $P_0^n(\widehat A_{n,2})>1-\widehat\epsilon_{n,2}$, for some suitable sequence $\{\widehat\epsilon_{n,2}\}_{n=1}^\infty$ converging to zero, where $\|\cdot\|$ represents the spectral norm.''',[21],[5,7,18,20],[r'\widehat A_{n,1}',r'\widehat A_{n,2}',r'B_\delta(\widehat\theta)'],'Full local spectral regularity assumption: two eigenvalue bounds and a separate joint event controlling prior Hessian and likelihood third/fourth derivatives on a random-center fixed-radius ball. Tensor spectral convention remains as named by the source.','Assumption 10',kind='assumption',phrases=['Assumption 10'])
add(24,'set containing the indexes',r'''To address the above goal, denote with $C\subseteq\{1,\ldots,d\}$ the set containing the indexes for the elements of $\theta$ on which we are interested in. Let $d_C$ be the cardinality of $C$, and $\bar C=C^c$ the complement of $C$. Finally, write $\widehat h=(\widehat h_C,\widehat h_{\bar C})$.''',[23],[19],[r'C\subseteq\{1,\ldots,d\}',r'\widehat h=(\widehat h_C,\widehat h_{\bar C})'],'Original coordinate subset, its complement and block coordinate. It is independent of Gaussian covariance; empty/full subsets require the usual zero-dimensional conventions, not supplied explicitly.','Section 4.2 — Marginal coordinate set')
add(25,'Gaussian',r'''Accordingly, the corresponding matrix $\widehat\Omega=(J_{\widehat\theta}/n)^{-1}$ can be partitioned in two diagonal blocks $\widehat\Omega_{CC}$, $\widehat\Omega_{\bar C\bar C}$, and an off–diagonal one $\widehat\Omega_{\bar CC}$.

The second order term in the above expression is proportional to the kernel of a Gaussian and, therefore, can be decomposed as
\[
\exp(-j_{\widehat\theta,st}\widehat h_s\widehat h_t/(2n))\propto\phi_d(\widehat h;0,\widehat\Omega)=\phi_{d_C}(\widehat h_C;0,\widehat\Omega_{CC})\phi_{d-d_C}(\widehat h_{\bar C};\Lambda_C\widehat h_C,\bar\Omega),
\]
where $\Lambda_C=\widehat\Omega_{\bar CC}\widehat\Omega_{CC}^{-1}$ and $\bar\Omega=\widehat\Omega_{\bar C\bar C}-\widehat\Omega_{\bar CC}\widehat\Omega_{CC}^{-1}\widehat\Omega_{C\bar C}$.''',[23,24],[20,24],[r'\Lambda_C',r'\bar\Omega',r'\widehat\Omega_{CC}'],'Original covariance blocks and Gaussian conditional factorization. This uses the MAP likelihood covariance, not the theoretical covariance in Theorem2.1. The intervening posterior Taylor-expansion sentence is not part of this archived definition.','Section 4.2 — Gaussian block factorization',kind='source_passage')
add(26,'summation',r'''\[
\nu_{1,s}^n=3\ell_{\widehat\theta,srv}^{(3)}\bar\Omega_{rv}+3\ell_{\widehat\theta,rvk}^{(3)}\bar\Omega_{rv}\Lambda_{C,ks},
\]
\[
\nu_{3,stl}^n=\ell_{\widehat\theta,stl}^{(3)}+3\ell_{\widehat\theta,str}^{(3)}\Lambda_{C,rl}+3\ell_{\widehat\theta,srv}^{(3)}\Lambda_{C,rt}\Lambda_{C,vl}+\ell_{\widehat\theta,rvk}^{(3)}\Lambda_{C,rs}\Lambda_{C,vt}\Lambda_{C,kl},\tag{29}
\]
the summation in (28) can be written as $\nu_{1,s}^n\widehat h_s+\nu_{3,stl}^n\widehat h_s\widehat h_t\widehat h_l$, with $s,t,l\in C$.''',[24],[5,18,24,25],[r'\nu_{1,s}^n',r'\nu_{3,stl}^n'],'Original coefficients of the contracted marginal cubic expectation. Indices r,v,k range over the complement, as specified before Eq29; s,t,l range over C. Preserve factors3 and all distinct contractions.','Section 4.2 — Marginal coefficients (29)')
add(27,'odd polynomial',r'''\[
\alpha_{\eta,C}(\widehat h_C)=\{1/(12\eta\sqrt n)\}(1/n)(\nu_{1,s}^n\widehat h_s+\nu_{3,stl}^n\widehat h_s\widehat h_t\widehat h_l).\tag{30}
\]''',[24],[9,24,26],[r'\alpha_{\eta,C}(\widehat h_C)'],'Original marginal odd polynomial, with both linear and cubic terms and n^{-3/2} scaling. It is not simply the joint cubic restricted to the selected coordinates.','Section 4.2 — Marginal odd polynomial (30)',context='Note that $\alpha_{\eta,C}(\widehat h_C)$ in (30) is an odd polynomial of $\widehat h_C$')
add(28,'posterior marginal density',r'''As a result, the posterior marginal density of $\widehat h_C$ can be approximated by
\[
\widehat p_{\mathrm{SKS},C}^n(\widehat h_C)=2\phi_{d_C}(\widehat h_C;0,\widehat\Omega_{CC})w_C(\widehat h_C)=2\phi_{d_C}(\widehat h_C;0,\widehat\Omega_{CC})F(\alpha_{\eta,C}(\widehat h_C)).\tag{31}
\]''',[24],[9,24,25,27],[r'\widehat p_{\mathrm{SKS},C}^n(\widehat h_C)'],'Separate marginal skew-modal approximation, using F of the conditional mean polynomial. It is generally not the exact marginal of the joint skew-modal density.','Section 4.2 — Marginal skew-modal approximation (31)',kind='source_passage')
add(29,'target marginal posterior density',r'''$\pi_{n,C}(\widehat h_C)=\int\pi_n(\widehat h)\,\mathrm d\widehat h_{\bar C}$.''',[25],[4,19,24],[r'\pi_{n,C}(\widehat h_C)'],'True rescaled posterior marginal obtained by integrating out complementary coordinates. Its definition requires no Gaussian covariance or approximating density.','Section 4.2 — Target marginal posterior',context='the above solution preserves the same theoretical accuracy guarantees in approximating the target marginal posterior density')
# The paper gives these assumptions numbered headings, without descriptive titles.
for n,number,page in [(11,1,9),(12,2,9),(13,3,9),(15,4,9),(16,7,15),(17,8,15),(22,9,21),(23,10,21)]:
    lid='D'+str(n);m=members[lid];context_id=lid+'/heading'
    m.setdefault('naming_context',[]).append(dict(context_id=context_id,text='ASSUMPTION '+str(number)+'.',evidence=[dict(page=page,location='Printed small-cap assumption heading')]))
    x=next(x for x in interfaces if x['members'][0]['local_id']==lid)
    x['source_keywords']=[dict(paper_id=PID,local_id=lid,source_text='ASSUMPTION '+str(number),label='Assumption '+str(number),kind='term',context_id=context_id)]
    x['name']='Assumption '+str(number)
def main():
    review=json.loads((REVIEW_ROOT/'inventory-review.json').read_text())
    assert review['status']=='complete' and review['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==review['inventory_sha256']
    assert len(interfaces)==len(members)==29
    for x in interfaces:
        a=x['members'][0];own=a['statement_original']+' '+a['local_label'];assert any(v in own for v in a['highlight_symbols']+a['highlight_phrases'])
        assert set(a['depends_on'])<=set(members)
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved29 original source entries; full census review remains pending.')
if __name__=='__main__':main()
