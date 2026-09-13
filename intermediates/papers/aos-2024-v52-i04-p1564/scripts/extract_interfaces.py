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

add('D1','Sparse sequence model',r'''
For some $\theta=(\theta_1,\ldots,\theta_n)$ consider observing independent data $X=(X_1,\ldots,X_n)$ satisfying, for a family of density functions $(f_a:a\in\mathbb R)$,
\[
X_i\sim f_{\theta_i},\qquad i=1,\ldots,n.\tag{1}
\]
We write $P_\theta$ for the law of $X$ with parameter $\theta$ in (1) and $E_\theta$ for the corresponding expectation. Write $F_a(x)=\int_{-\infty}^x f_a(t)\,dt$ and $\overline F_a(x)=1-F_a(x)$ for the distribution function and the tail function, respectively.
''',[4],'Section 1.2 — sparse sequence model (1)',kind='source_passage',context='Sparse sequence model',symbols=[r'X_i\sim f_{\theta_i}',r'\overline F_a(x)=1-F_a(x)'],shape='Independent coordinates with a real-indexed density family. P_theta is the joint law; no common location or scale family is imposed at this level. Two original excerpts surround the separate sparsity convention.')
add('D2','sparse asymptotic setting',r'''
The vector $\theta$ is assumed to be sparse; that is, to belong to the set
\[
\ell_0[s_n]=\{\theta\in\mathbb R^n,\|\theta\|_0\le s_n\},\qquad
\|\theta\|_0:=\#\{1\le i\le n:\theta_i\ne0\},\tag{2}
\]
consisting of vectors that have at most $s_n$ nonzero coordinates, where $0\le s_n\le n$; throughout the paper we consider the sparse asymptotic setting where
\[
n\to\infty,\ s_n\to\infty\text{ and }n/s_n\to\infty.\tag{3}
\]
''',[4],'Section 1.2 — sparsity and asymptotics (2)–(3)',kind='source_passage',symbols=[r'\ell_0[s_n]',r'n\to\infty,\ s_n\to\infty'],shape='At-most-s_n support class and global sequence regime. Specific parameter classes may require exactly s_n nonzero coordinates. Polynomial sparsity is a separate extra condition.')
add('D3','multiple testing procedure',r'''
A multiple testing procedure is formally defined as a measurable function of the data $\varphi:x\in\mathbb R^n\mapsto(\varphi_i(x))_{1\le i\le n}\in\{0,1\}^n$, where, by convention, $\varphi_i(X)=1$ corresponds to rejecting the null $H_{0,i}$. As such, the procedure will depend on $n$, and with some slight abuse of terminology, when dealing with asymptotics in terms of $n$, a sequence of such procedures is sometimes simply referred to as a ‘procedure’ for short.
''',[5],'Section 1.3 — multiple testing procedure',symbols=[r'\varphi:x\in\mathbb R^n\mapsto(\varphi_i(x))_{1\le i\le n}\in\{0,1\}^n'],shape='Measurable binary decision vector, or sequence thereof. Null H_0,i means theta_i=0. The theorem infima are not restricted to threshold rules unless explicitly stated.')
add('D4','false discovery rate',r'''
For any $\theta\in\mathbb R^n$ and any procedure $\varphi$, the false discovery rate (FDR) and the false discovery proportion (FDP) of $\varphi$ at the parameter $\theta$ are respectively defined as
\[
\operatorname{FDR}(\theta,\varphi)=E_\theta[\operatorname{FDP}(\theta,\varphi)],\qquad
\operatorname{FDP}(\theta,\varphi)=\frac{\sum_{i=1}^n\mathbf1\{\theta_i=0\}\varphi_i(X)}{1\vee\sum_{i=1}^n\varphi_i(X)}.\tag{5}
\]
''',[5],'Section 1.3 — FDR and FDP (5)',{'D3':'The numerator and denominator count rejections by the binary testing procedure.','D1':'Expectation is under the joint law P_theta of the observations.'},symbols=[r'\operatorname{FDR}(\theta,\varphi)',r'1\vee\sum_{i=1}^n\varphi_i(X)'],shape='Expectation of the random false-discovery fraction, not a ratio of expectations. The denominator is truncated below by one.')
add('D5','false negative rate',r'''
The false negative rate (FNR) at $\theta$ is here defined as (see, e.g., [5])
\[
\operatorname{FNR}(\theta,\varphi)=E_\theta\left[\frac{\sum_{i=1}^n\mathbf1\{\theta_i\ne0\}(1-\varphi_i(X))}{1\vee\sum_{i=1}^n\mathbf1\{\theta_i\ne0\}}\right].\tag{6}
\]
''',[5],'Section 1.3 — FNR (6)',{'D3':'The numerator counts missed nonnull coordinates of the testing procedure.','D1':'The expectation uses P_theta.'},symbols=[r'\operatorname{FNR}(\theta,\varphi)',r'1\vee\sum_{i=1}^n\mathbf1\{\theta_i\ne0\}'],shape='Expected missed-signal fraction, divided by the true support size truncated below by one. This differs from a false-omission proportion among accepted hypotheses.')
add('D6','combined risk',r'''
The (multiple testing) combined risk at $\theta\in\mathbb R^n$ of a procedure $\varphi$ is the sum
\[
\mathfrak R(\theta,\varphi)=\operatorname{FDR}(\theta,\varphi)+\operatorname{FNR}(\theta,\varphi).
\]
''',[5],'Section 1.3 — combined multiple testing risk',{'D4':'The first summand is the false discovery rate.','D5':'The second summand is the false negative rate.'},symbols=[r'\mathfrak R(\theta,\varphi)'],shape='Sum of the two risks with their different denominators. Do not replace it by Hamming risk or by FNR alone.')
add('D7','minimax multiple testing risk',r'''
To investigate questions of optimality, a natural benchmark is the minimax multiple testing risk, defined as
\[
\mathfrak R(\Theta)=\inf_\varphi\sup_{\theta\in\Theta}\mathfrak R(\theta,\varphi),\tag{7}
\]
where the infimum is over all multiple testing procedures and the parameter set $\Theta$ is some appropriate subset of $\ell_0[s_n]$.
''',[5],'Section 1.4 — minimax risk (7)',{'D6':'The minimax functional uses the combined testing risk.','D2':'The parameter set is a subset of the sparse class.'},symbols=[r'\mathfrak R(\Theta)=\inf_\varphi\sup_{\theta\in\Theta}\mathfrak R(\theta,\varphi)'],shape='Infimum over all measurable procedures, followed by worst-case parameter risk. FNR-only and classification minimax expressions are separately bound in their theorem statements.')
add('D8','Gaussian location model',r'''
The prototypical example to have in mind is the Gaussian location model, under which $f_a$ is the density of the distribution $\mathcal N(a,1)$, so that
\[
X_i=\theta_i+\varepsilon_i,\qquad\varepsilon_i\overset{\mathrm{iid}}\sim\mathcal N(0,1),\qquad i=1,\ldots,n.\tag{4}
\]
''',[4],'Example 1 — Gaussian location model',{'D1':'This specifies the density family and independent noise in the sequence model.'},kind='source_passage',symbols=[r'X_i=\theta_i+\varepsilon_i',r'\mathcal N(0,1)'],shape='Independent standard-variance Gaussian location noise. It is a particular model, not an additional condition on all general-noise results.')
add('D9','beta-min type condition',r'''
To evaluate the minimax risk, we define a class of configurations for $\theta$ that measures how the alternatives are separated from the null hypothesis: for a given $a\in\mathbb R$, set
\[
\Theta=\Theta(a,s_n)=\{\theta\in\ell_0[s_n]:|\theta_i|\ge a\text{ for }i\in S_\theta,\ |S_\theta|=s_n\},\tag{9}
\]
where $S_\theta=\{i:\theta_i\ne0\}$ denotes the support of $\theta$ (recall $\ell_0[s_n]$ is defined by (2)). This choice corresponds to a so-called beta-min type condition, meaning that all intensities of nonzero coefficients are required to be above a certain value $a>0$.

We identify here a sharp formulation for this boundary, by considering for $b\in\mathbb R$,
\[
\Theta_b=\Theta(a_b,s_n),\qquad a_b=\sqrt{2\log(n/s_n)}+b,\tag{10}
\]
with $\Theta(a,s_n)$ as in (9).
''',[9],'Section 2 — beta-min parameter class (9)–(10)',{'D2':'The class has exactly s_n nonzero entries within the at-most-s_n sparse class.'},symbols=[r'\Theta(a,s_n)',r'\Theta_b=\Theta(a_b,s_n)',r'a_b=\sqrt{2\log(n/s_n)}+b'],shape='Two original excerpts defining the beta-min class and its boundary parametrization. The initial domain a in R and later prose a>0 are both retained. Theorem 7 uses a separately archived union over support sizes without changing a_b.')
add('D10','polynomial sparsity assumption',r'''
Some will require an additional polynomial sparsity assumption: for some unknown $c<1$,
\[
s_n\lesssim n^c.\tag{12}
\]
''',[11],'Section 2.3 — polynomial sparsity (12)',kind='condition',symbols=[r's_n\lesssim n^c'],shape='Extra polynomial upper bound with an unknown exponent below one, distinct from s_n/n tending to zero. Branch applicability is recorded per theorem.')
add('D11','Benjamini–Hochberg procedure',r'''
First, probably the most widely used multiple testing procedure is the so-called Benjamini–Hochberg procedure, introduced in [9]. For some level $\alpha$, it is given by $\varphi_\alpha^{BH}=(\mathbf1\{|X_i|\ge\widehat t\})_{1\le i\le n}$ where the threshold $\widehat t=\widehat t(\alpha)$ is defined as a specific intersection point between the empirical upper-tail distribution function of the $X_i$'s and a quantile curve of the noise distributions (see Section S-7 for details).
''',[7],'Section 1.6 — BH procedure description',{'D3':'The threshold rule defines a binary multiple testing procedure.','D1':'Its threshold compares empirical observations to the null noise distribution.'},kind='source_passage',symbols=[r'\varphi_\alpha^{BH}',r'\widehat t=\widehat t(\alpha)'],shape='Main-text description only. Exact threshold/intersection conventions and formula S-18 are deferred to the excluded supplement and remain unresolved; do not substitute a textbook convention.')
add('D12','empirical Bayes calibration',r'''
The second procedure uses Bayesian $\ell$-values (often also called local FDR values) with an empirical Bayes calibration. For a particular spike-and-slab prior $\Pi_w$ on $\mathbb R^n$ (see Section S-8 for details), we consider the empirical Bayes $\ell$-value procedure defined by thresholding posterior probabilities of null hypotheses at some specified level $t\in(0,1)$, i.e., $\varphi_t^{\widehat\ell}=(\mathbf1\{\Pi_{\widehat w}(\theta_i=0\mid X)<t\})_{1\le i\le n}$, where $\widehat w$ is the marginal maximum likelihood estimator for $w$, as in [36, 35].
''',[7],'Section 1.6 — empirical Bayes null-probability thresholding',{'D3':'Posterior thresholding supplies the binary testing decisions.','D1':'The posterior and marginal likelihood depend on the observation model.'},kind='source_passage',symbols=[r'\varphi_t^{\widehat\ell}',r'\Pi_{\widehat w}(\theta_i=0\mid X)<t'],shape='Retain the strict posterior-probability threshold. The particular slab, prior weights and marginal-likelihood optimization domain are not given in this main-text passage; S-29 remains a supplement-only reference.')
add('D13','sparsity-preserving',r'''
We say that a multiple-testing procedure $\varphi=\varphi(X)\in\{0,1\}^n$ (or strictly, a sequence of such procedures, indexed by $n$), is sparsity-preserving over $\Theta=(\Theta_n)_n$ (with $\Theta_n\subset\ell_0[s_n]$) up to a multiplicative factor $A=(A_n)_n$ if, as $n\to\infty$,
\[
\sup_{\theta\in\Theta_n}P_\theta\left[\sum_{i=1}^n\varphi_i(X)>A_ns_n\right]=o(1).\tag{14}
\]
We denote by $\mathcal S_A(\Theta)=\mathcal S_A((s_n)_n,\Theta)$ the set of all such procedure sequences.
''',[12],'Definition 1',{'D3':'The event counts rejections by a procedure sequence.','D2':'The parameter sets are contained in the sparse classes with sizes s_n.','D1':'The overshoot probability is evaluated under P_theta.'},symbols=[r'\mathcal S_A(\Theta)',r'\sum_{i=1}^n\varphi_i(X)>A_ns_n'],shape='Uniform high-probability control of rejection count up to the factor A_n. It is neither a deterministic rejection cap nor an expected-count bound.')
add('D14','Assumption 1',r'''
There exists a constant $L$ such that each $F_a$ is $L$-Lipschitz. There exist sequences of positive numbers $a_n^*\to\infty$, $\delta_n\to0$ such that
\[
(n/s_n)\overline F_0(a_n^*-\delta_n)\to\infty,\tag{16}
\]
\[
(n/s_n)\overline F_0(a_n^*)\to0.\tag{17}
\]
The density $f_0$ is continuous and positive on $\mathbb R$. Further assume one of
''',[13],'Assumption 1 — common conditions (16)–(17)',{'D1':'The common Lipschitz condition and null tail refer to the density family and its distribution functions.','D2':'The null tail scaling uses the sparse sequence regime.'},kind='assumption',context='Assumption 1.',symbols=[r'(n/s_n)\overline F_0(a_n^*-\delta_n)',r'(n/s_n)\overline F_0(a_n^*)'],shape='Common part of Assumption 1; one of separately preserved branches A or B is required, not both. The Lipschitz constant is common to every F_a, and the threshold sequences are positive.')
add('D15','Assumption 1A',r'''
A. $f_{-a}(-x)=f_a(x)$ for $a,x\in\mathbb R$, $\overline F_a(x)$ is increasing in $a\in\mathbb R$ and, for $a>0$,
\[
f_a(x)/f_0(x)\text{ is increasing in }x\in\mathbb R.\tag{18}
\]
''',[13],'Assumption 1A',{'D14':'Branch A is paired with the common Lipschitz, null-density and tail conditions.'},kind='assumption',context='Under Assumption 1A,',context_pages=[15],symbols=[r'f_{-a}(-x)=f_a(x)',r'f_a(x)/f_0(x)'],shape='Location-type reflection and stochastic/likelihood-ratio monotonicity branch. The likelihood-ratio requirement is for a>0 and all real x; no strictness is added to increasing.')
add('D16','Assumption 1B',r'''
B. $f_a(-x)=f_a(x)$ for all $a,x\in\mathbb R$, $\overline F_a(x)$ is increasing in $a>0$ for $x>0$, and for $a\ne0$
\[
f_a(x)/f_0(x)\text{ is increasing in }x>0.\tag{19}
\]
''',[13],'Assumption 1B',{'D14':'Branch B shares the common Lipschitz, null-density and tail conditions.'},kind='assumption',context='Under Assumption 1B,',context_pages=[15],symbols=[r'f_a(-x)=f_a(x)',r'f_a(x)/f_0(x)'],shape='Even-in-observation densities and positive-half-line monotonicity. The source does not explicitly impose f_{-a}=f_a in this branch; do not silently insert parameter-sign invariance.')
add('D17','Subbotin',r'''
Assumption 1A holds with $a_n^*=(\zeta\log(n/s_n))^{1/\zeta}$ for the Subbotin (generalised Gaussian) location model, with $f_a$ denoting the law of $X=a+\varepsilon$, $\varepsilon\sim\phi_\zeta$,
\[
\phi_\zeta(x)=L_\zeta^{-1}e^{-|x|^\zeta/\zeta},\qquad\zeta>1;\tag{20}
\]
see Lemma S-1. In particular, this model includes standard Gaussian noise as the case $\zeta=2$, while the excluded case $\zeta=1$ would correspond to Laplace noise. In this setting we will write $\overline\Phi_\zeta(x)=\int_x^\infty\phi_\zeta(t)\,dt$ and $\Phi_\zeta=1-\overline\Phi_\zeta$. Note that when we write $a_n^*$ in reference to the Subbotin model, we will mean the value $(\zeta\log(n/s_n))^{1/\zeta}$ except where specified otherwise.
''',[14],'Example 2 — Subbotin location model',{'D1':'The example specifies the location density family.','D2':'The default threshold convention uses n/s_n in the sparse regime.'},kind='source_passage',symbols=[r'\phi_\zeta(x)=L_\zeta^{-1}e^{-|x|^\zeta/\zeta}',r'\zeta>1'],shape='Original model definition and threshold convention. Its assertion that Assumption 1A holds is a source claim, not an extra assumption needed to state Theorem 8. L_zeta is the density normalizer; Laplace noise is excluded.')
add('D18','more general parameter set',r'''
In this section, we also consider a more general parameter set, with different signal strengths. For a vector $\boldsymbol a=(a_1,\ldots,a_{s_n})$ (implicitly indexed by $n$) with $a_j>0$ for $1\le j\le s_n$, define
\[
\Theta(\boldsymbol a,s_n)=\{\theta\in\ell_0[s_n]:\exists i_1,\ldots,i_{s_n}\text{ all distinct},\ |\theta_{i_j}|\ge a_j,\ 1\le j\le s_n\}.\tag{21}
\]
''',[14],'Section 3.1 — heterogeneous-strength parameter set (21)',{'D2':'The vector belongs to the at-most-s_n sparse class, while positivity of all a_j forces exactly s_n nonzero entries.'},symbols=[r'\Theta(\boldsymbol a,s_n)',r'|\theta_{i_j}|\ge a_j'],shape='Existential matching of positive lower strengths to distinct signal coordinates. Positions and signs remain unknown; strengths need not be equal or in source order.')
add('D19','measure of the (lack of) signal strength',r'''
A key quantity is
\[
\Lambda_n(\boldsymbol a)=s_n^{-1}\sum_{j=1}^{s_n}F_{a_j}(a_n^*);\tag{22}
\]
this can be seen roughly as a measure of the (lack of) signal strength for the parameter set $\Theta(\boldsymbol a,s_n)$. In a slight abuse of notation, if $\theta$ is a vector whose non-zero entries have absolute values $a_1,\ldots,a_{s_n}$ and recalling the notation $S_\theta=\{i:\theta_i\ne0\}$, we also write
\[
\Lambda_n(\theta)=s_n^{-1}\sum_{i\in S_\theta}F_{|\theta_i|}(a_n^*).\tag{23}
\]
''',[14],'Section 3.1 — average signal-strength quantity (22)–(23)',{'D1':'The quantity averages distribution-function values F_a, not upper tails.','D14':'The evaluation threshold a_n^* is the sequence specified by Assumption 1.','D18':'The vector form uses the heterogeneous positive-strength coordinates.'},symbols=[r'\Lambda_n(\boldsymbol a)',r'\Lambda_n(\theta)',r'F_{|\theta_i|}(a_n^*)'],shape='The average uses CDFs at the critical threshold. Branch A risk is Lambda; branch B risk is 2 Lambda-1. Preserve the parameter-sign convention and do not silently make the two branches equivalent.')
add('D20','condition on the level',r'''
Let us introduce the following condition on the level $\alpha=\alpha_n$ of the BH procedure:
\[
\frac{3n\overline F_0(a_n^*)}{s_n(1-\Lambda_n(\theta))}\le\alpha_n\le\min\left\{1,\frac{n\overline F_0(a_n^*-\delta_n)}{s_n}\right\}\qquad\text{for }n\text{ large enough}.\tag{24}
\]
''',[16],'Section 3.2 — BH level condition (24)',{'D11':'The condition restricts the level of the BH procedure.','D19':'The lower bound depends on the signal vector through one minus Lambda.','D14':'Both bounds use the null-tail threshold and its delta perturbation.'},kind='condition',symbols=[r'\frac{3n\overline F_0(a_n^*)}{s_n(1-\Lambda_n(\theta))}'],shape='Theta-dependent interval for the level. Theorem 5 uniform/o(1) assertions require careful source-scope notes; the printed interval alone permits nonvanishing levels. Preserve the branch-B replacement convention separately.')
add('D21','classification (Hamming) loss',r'''
The classification (Hamming) loss in terms of classes $\{0\}$ and $\mathbb R\setminus\{0\}$ is defined by
\[
\mathrm L_{\mathrm C}(\theta,\varphi)=\sum_{i=1}^n\left(\mathbf1\{\theta_i=0\}\mathbf1\{\varphi_i\ne0\}+\mathbf1\{\theta_i\ne0\}\mathbf1\{\varphi_i=0\}\right).\tag{30}
\]
''',[22],'Section 5.2 — classification loss (30)',{'D3':'The loss counts both kinds of classification errors by the binary testing procedure.'},symbols=[r'\mathrm L_{\mathrm C}(\theta,\varphi)'],shape='Unnormalized Hamming count. Theorem 7 divides its expectation by s_n; Theorems 8 and 9 divide by n^(1-beta). It is not the combined testing risk.')
add('D22','parameter space of large signals',r'''
Let us first formally introduce an appropriate parameter space of large signals. For some $\beta\in(0,1)$, $\zeta>1$, and $r>\beta$, for fixed $0<a<b$, define
\[
\Theta(r,\beta)=\bigcup_{s_n\in[an^{1-\beta},bn^{1-\beta}]}\{\theta\in\ell_0[s_n]:|S_\theta|=s_n,\ |\theta_i|\ge M(r)\text{ for all }i\in S_\theta\},\tag{32}
\]
\[
M=M(r)=(\zeta r\log n)^{1/\zeta}.\tag{33}
\]
''',[23],'Section 6 — large-signal parameter space (32)–(33)',{'D2':'The union ranges over support sizes proportional to n^(1-beta), with exact support size inside each component.'},symbols=[r'\Theta(r,\beta)',r'M=M(r)=(\zeta r\log n)^{1/\zeta}'],shape='Unknown support size within a fixed proportional range and coordinatewise lower amplitude. The constants a,b here are unrelated to the earlier boundary offset b or strength vector. Signals may have unequal magnitudes.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source interface passages; theorem linkage and full review remain pending.')
if __name__=='__main__':main()
