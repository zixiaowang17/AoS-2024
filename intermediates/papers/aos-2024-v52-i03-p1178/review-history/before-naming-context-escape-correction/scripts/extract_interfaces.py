"""Extract original missing-data classification prerequisites, main text only."""
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
add('D1','dimension',r'''
For $\omega\in\{0,1\}^d$, we write $d_\omega:=\|\omega\|_1$ for the number of 1s in $\omega$, which will refer to as the dimension of $\omega$. For $\omega=(\omega_1,\ldots,\omega_d)^\mathrm T,\omega'=(\omega'_1,\ldots,\omega'_d)^\mathrm T\in\{0,1\}^d$, we write $\omega\preceq\omega'$ if $\omega_j\le\omega'_j$ for all $j\in[d]$, $\omega\prec\omega'$ if $\omega_j\le\omega'_j$ for all $j\in[d]$ and $\omega\ne\omega'$, $\omega\wedge\omega':=(\omega_1\wedge\omega'_1,\ldots,\omega_d\wedge\omega'_d)^\mathrm T$, and $\omega\vee\omega':=(\omega_1\vee\omega'_1,\ldots,\omega_d\vee\omega'_d)^\mathrm T$.
''',[3],'Section 1 — pattern dimension and partial order',symbols=[r'd_\omega:=\|\omega\|_1',r"\omega\preceq\omega'"],shape='Binary patterns with Hamming weight, componentwise partial order and strict order requiring at least one strict component. The printed phrase which will refer to is retained. Scalar minima/maxima in componentwise meet/join are standard.')
add('D2','entrywise product',r'''
For $x\in\mathbb R^d$ and $\omega\in\{0,1\}^d$, we write $x^\omega:=x\odot\omega+\mathbf0_d\odot(\mathbf1_d-\omega)\in\mathbb R^d$, and $\odot$ denotes the entrywise product.
''',[3],'Section 1 — masking by an observation pattern',symbols=[r'x^\omega',r'\odot'],shape='Masking preserves ambient dimension d and replaces unselected coordinates with zero. This is not a vector in R^{d_omega}; the observation mask remains available to distinguish observed zeros from missing entries.')
add('D3','marginal distribution',r'''
Let $\mathcal Q$ denote the class of all distributions on $\mathbb R^d\times\{0,1\}\times\{0,1\}^d$. Then, for $Q\in\mathcal Q$, suppose that $(X,Y,O)\sim Q$, and recall that $X$ denotes the feature vector taking values in $\mathbb R^d$, $Y$ denotes its class label (either 0 or 1) and $O$ denotes an observation indicator in $\{0,1\}^d$. We write $P\equiv P_Q$ for the marginal distribution of $(X,Y)$,
''',[3,4],'Section 2 — joint and test-pair distributions',symbols=[r'P\equiv P_Q',r'(X,Y,O)\sim Q'],shape='Joint distribution includes the binary label and mask; P_Q is the unconditional test-pair marginal. It is not the conditional complete-case distribution.')
add('D4','regression function',r'''
write $\eta:\mathbb R^d\to[0,1]$ for the regression function given by $\eta(x):=\mathbb P_P(Y=1\mid X=x)$, and let $\mu$ denote the marginal distribution of $X$ on $\mathbb R^d$.
''',[4],'Section 2 — regression function and feature marginal',{'D3':'The regression and feature marginal belong to the test-pair law P_Q.'},symbols=[r'\eta(x)',r'\mu'],shape='Conditional class-one probability and feature marginal under P_Q. Pointwise conditional probabilities require versions; the source states later assumptions at all support points without an additional version convention.')
add('D5','training data',r'''
For $n\in\mathbb N$ and $Q\in\mathcal Q$, let $(X_1,Y_1,O_1),\ldots,(X_n,Y_n,O_n)$ be independent and identically distributed triples from $Q$. In our missing data problem, we only observe those entries of $X_i$ for which the corresponding entry of $O_i$ is 1. In other words, our training data is $D_n:=\big((X_1^{O_1},Y_1,O_1),\ldots,(X_n^{O_n},Y_n,O_n)\big)$ and we are presented with the task of assigning a fully observed test point $X$ to either class 0 or class 1.
''',[4],'Section 2 — incomplete training sample and complete test point',{'D3':'The iid triples have common law Q and the test pair has marginal P_Q.','D2':'Only the masked feature vector and its mask are observed in each training record.'},symbols=[r'D_n',r'X_1^{O_1}'],shape='IID masked training records with every label observed, and a fully observed test point from P_Q. The printed footnote discussing partially observed test points is separate contextual material, not a change to the experiment.')
add('D6','data-dependent classifier',r'''
A data-dependent classifier $\widehat C$ is a measurable function from $\mathbb R^d\times(\mathbb R^d\times\{0,1\}\times\{0,1\}^d)^n$ to $\{0,1\}$, and we let $\mathcal C_n$ denote the set of all such data-dependent classifiers. Throughout this paper the latter $n$ arguments of $\widehat C(x,D_n)$ will always be $D_n$ and thus will often be omitted; we will simply write $\widehat C(x)$.
''',[4],'Section 2 — class of measurable classification rules',{'D5':'The classifier is evaluated on the observed masked training data D_n.'},symbols=[r'\mathcal C_n',r'\widehat C(x,D_n)'],shape='All measurable binary classifiers using the observed training records and a complete test feature vector. This class is distinct from the specific HAM procedure and from the oracle used in the minimax proof.')
add('D7','test error',r'''
The performance of $\widehat C\in\mathcal C_n$ will be measured by its test error
\[
L_P(\widehat C):=\mathbb P_P\{\widehat C(X)\ne Y\mid D_n\}=\int_{\mathbb R^d\times\{0,1\}}\mathbb1_{\{\widehat C(x)\ne y\}}\,dP(x,y),
\]
''',[4],'Section 2 — conditional test error',{'D3':'The loss is integrated against the unconditional test-pair distribution P.','D5':'The probability is conditional on the observed training data.','D6':'The prediction is made by a data-dependent measurable binary rule.'},symbols=[r'L_P(\widehat C)'],shape='Random test error conditional on training data, obtained by integrating the fixed fitted rule over an independent test pair. The later outer expectation also conditions on the observed mask sequence.')
add('D8','Bayes classifier',r'''
which is minimised by the Bayes classifier $C^{\mathrm{Bayes}}(x)=\mathbb1_{\{\eta(x)\ge1/2\}}$.
''',[4],'Section 2 — Bayes decision rule',{'D4':'The Bayes rule thresholds the regression function eta.'},symbols=[r'C^{\mathrm{Bayes}}(x)'],shape='Bayes rule with class one selected at an exact tie eta=1/2. Its excess-loss contribution at a tie is zero.')
add('D9','excess test error',r'''
Therefore our main results will concern the (nonnegative) excess test error
\[
\mathcal E_P(\widehat C):=L_P(\widehat C)-L_P(C^{\mathrm{Bayes}})=\int_{\mathbb R^d}\mathbb1_{\{\widehat C(x)\ne C^{\mathrm{Bayes}}(x)\}}|2\eta(x)-1|\,d\mu(x).\tag{2}
\]
''',[4],'Section 2 — excess test error (2)',{'D7':'Excess error subtracts the Bayes error from the fitted-rule test error.','D8':'The comparison rule is the original Bayes classifier.','D4':'The weighted disagreement integral uses eta and the feature marginal mu.'},symbols=[r'\mathcal E_P(\widehat C)'],shape='Nonnegative excess error under the unconditional feature marginal. Theorem expectations average this random training-dependent quantity conditionally on all masks.')
add('D10','missingness mechanism',r'''
For $\mathcal O\subseteq\{0,1\}^d$, let $\mathcal Q_{\mathrm{Miss}}(\mathcal O)\subseteq\mathcal Q$ denote the class of distributions for which $\mathbb P_Q(O=o)>0$ for all $o\in\mathcal O$, and
\[
\mathbb P_Q(Y=1\mid X^\omega=x^\omega)=\mathbb P_Q(Y=1\mid X^\omega=x^\omega,O=o)\tag{3}
\]
for all $x\in\operatorname{supp}(\mu)$, $\omega\in\{0,1\}^d$ and $o\in\mathcal O$ with $\omega\preceq o$.
''',[4],'Definition 1',{'D3':'The missingness mechanism is a condition on the joint law Q.','D4':'The pointwise condition is required on the feature marginal support.','D2':'Both conditional probabilities use the masked features.','D1':'The condition applies to every pattern omega observed within o.'},context='More formally, we employ the following general assumption on the missingness mechanism.',symbols=[r'\mathcal Q_{\mathrm{Miss}}(\mathcal O)',r'\mathbb P_Q(O=o)>0'],shape='Positive probabilities for every conditioned-on pattern in O and equality of all available-subvector regression probabilities. O need not be the entire support of the mask law. This is not replaced by MCAR, MAR or coordinate independence.')
add('D11','anova decomposition',r'''
More precisely, these functions may be defined recursively for $x\in\mathbb R^d$ as follows:
\[
f_{\mathbf0_d}(x):=\mathbb E_P\{\eta(X)\}-\frac12\equiv\mathbb P_P(Y=1)-\frac12\tag{4}
\]
\[
f_\omega(x):=\mathbb E_P\left\{\eta(X)-\frac12-\sum_{\omega'\prec\omega}f_{\omega'}(X)\mid X^\omega=x^\omega\right\}\quad\text{for }\omega\in\{0,1\}^d\text{ with }d_\omega\ge1.\tag{5}
\]
This is known as an anova decomposition (Efron and Stein, 1981), and indeed Proposition S3 in Section S1.2 confirms that
\[
\eta(\cdot)=\frac12+\sum_{\omega\in\{0,1\}^d}f_\omega(\cdot).\tag{6}
\]
''',[5],'Section 2 — recursive anova decomposition (4)–(6)',{'D4':'The decomposition uses conditional expectations of eta under P.','D2':'Conditioning is on the masked subvector.','D1':'The recursive subtraction ranges over strict predecessors of the pattern.'},symbols=[r'f_{\mathbf0_d}(x)',r'f_\omega(x)',r'\eta(\cdot)=\frac12'],shape='Recursive conditional-expectation definition with a centered constant component and all strict-predecessor terms inside the expectation. The displayed reconstruction is retained. Supplementary Proposition S3 is not read; no independent-coordinate assumption or different Hoeffding decomposition is substituted.')
add('D12','distribution',r'''
For $Q\in\mathcal Q_{\mathrm{Miss}}(\mathcal O)$ and $\omega\in\{0,1\}^d$, we write $\mu_\omega$ to denote the distribution of $X^\omega$ when $(X,Y,O)\sim Q$, i.e. the distribution on $\mathbb R^d$ given by $\mu_\omega(A)=\mu\big(\{x\in\mathbb R^d:x^\omega\in A\}\big)$ for measurable $A\subseteq\mathbb R^d$.
''',[6],'Section 2 — unconditional masked-feature distribution',{'D10':'The defining paragraph works with Q in the original missingness class.','D4':'The measure is the pushforward of the feature marginal mu.','D2':'Its pushforward map zeros the unselected coordinates.'},symbols=[r'\mu_\omega(A)'],shape='Distribution of the masked feature vector as a probability measure on R^d, even for lower-dimensional patterns. Unconditional test-feature measure, distinct from its conditional training counterpart.')
add('D13','distribution',r'''
Moreover, for $o\in\mathcal O$ and $\omega\preceq o$, we write $\mu_{\omega\mid o}$ to denote the distribution of $X^\omega\mid\{O=o\}$ when $(X,Y,O)\sim Q$, i.e. the distribution on $\mathbb R^d$ given by $\mu_{\omega\mid o}(A)=\mathbb P_Q(X^\omega\in A\mid O=o)$, for measurable $A\subseteq\mathbb R^d$.
''',[6],'Section 2 — conditional masked-feature distribution',{'D10':'Positive mask probabilities come from Q in the missingness class.','D2':'The conditional random vector is masked by omega.','D1':'The conditional mask must contain omega.'},symbols=[r'\mu_{\omega\mid o}(A)'],shape='Conditional training-feature law given an available mask o. It can differ from the unconditional test-feature pushforward, which is why the tail conditions compare distinct measures.')
add('D14','signal strength',r'''
For $Q\in\mathcal Q_{\mathrm{Miss}}(\mathcal O)$ and $\omega\in\{0,1\}^d$, define
\[
\sigma_\omega^2:=\min_{o\in\mathcal O:o\succeq\omega}\mathbb E_Q\{f_\omega^2(X)\mid O=o\}.\tag{7}
\]
''',[6,7],'Section 2 — conditional interaction signal (7)',{'D10':'Q belongs to the missingness class so each relevant conditioning mask has positive probability.','D11':'The squared quantity is the original anova component.','D1':'The minimum ranges over masks containing omega.'},context='The intuition is that this provides a natural measure of the signal strength, and that, with enough data, we are able to detect which patterns $\omega$ belong to $\Omega_\star$.',symbols=[r'\sigma_\omega^2'],shape='Minimum conditional second moment over compatible masks in O, not a centered conditional variance. Empty compatible-mask minima are not explicitly assigned a convention in the main text.')
add('D15','antichains',r'''
Let $\mathcal I(\{0,1\}^d):=\{\Omega\subset\{0,1\}^d:\text{if }\omega,\omega'\in\Omega\text{ and }\omega\preceq\omega',\text{ then }\omega=\omega'\}$ be the set of antichains in $\{0,1\}^d$, i.e. the set of subsets $\Omega\subseteq\{0,1\}^d$ for which any two distinct elements of $\Omega$ are incomparable.
''',[6],'Section 2 — antichains of observation patterns',{'D1':'Incomparability is with respect to the componentwise pattern order.'},symbols=[r'\mathcal I(\{0,1\}^d)'],shape='Antichains in the Boolean pattern lattice. Theorem parameters exclude the empty antichain and the singleton zero pattern, not every antichain containing other lower-dimensional patterns.')
add('D16','orderings of subsets',r'''
Further, for $\Omega\in\mathcal I(\{0,1\}^d)$, let $L(\Omega):=\{\omega\in\{0,1\}^d:\text{there exists }\omega'\in\Omega\text{ such that }\omega\prec\omega'\}$ denote the elements of $\{0,1\}^d$ that precede the elements of $\Omega$, and write $U(\Omega):=\{0,1\}^d\setminus\{\Omega\cup L(\Omega)\}$.
''',[6],'Section 2 — strict predecessors and remaining patterns',{'D15':'The domain is an antichain of patterns.','D1':'L is formed by strict predecessors in the Boolean order.'},symbols=[r'L(\Omega)',r'U(\Omega)'],context='To make a precise statement of our main condition, which asks that $f_\\omega$ is zero for certain values of $\\omega$, we will also make use of some basic notation concerning orderings of subsets of $\\{0,1\\}^d$.',shape='L is the strict lower closure; U is the complement of Omega union L, including incomparable patterns as well as upper patterns. The source braces around the removed union are retained as grouping notation; U is not redefined as just the upper closure.')
add('D17','regression decomposition',r'''
For $\Omega_\star\in\mathcal I(\{0,1\}^d)$, $c_{\mathrm E}\in[0,1/4]$ and $\mathcal O\subseteq\{0,1\}^d$, let
\[
\mathcal Q_{\mathrm E}(\Omega_\star,c_{\mathrm E},\mathcal O):=\left\{Q\in\mathcal Q_{\mathrm{Miss}}(\mathcal O):\sigma_\omega^2\ge c_{\mathrm E}\text{ for all }\omega\in\Omega_\star,\ f_\omega\equiv0\text{ for all }\omega\in U(\Omega_\star)\right\}.
\]
''',[6],'Definition 2',{'D10':'The class is a subclass of the original missingness laws.','D14':'Its nonzero-component restriction is a conditional signal lower bound.','D11':'All patterns in U have identically zero original components.','D15':'Omega_star is an antichain.','D16':'U determines which components must vanish.'},context='Indeed, our next definition specifies which of the $f_\omega$ functions may contribute to the regression decomposition and which are identically zero.',symbols=[r'\mathcal Q_{\mathrm E}(\Omega_\star,c_{\mathrm E},\mathcal O)',r'\sigma_\omega^2\ge c_{\mathrm E}'],shape='Missingness class with interaction support restricted to Omega_star and its predecessors, plus conditional signal lower bounds only on Omega_star. With c_E=0 the signal restriction is redundant; lower-order components need not all be nonzero.')
add('D18','lower density',r'''
For a probability distribution $\nu$ on $\mathbb R^d$ and $s\in[0,d]$ let $\rho_{\nu,s}:\mathbb R^d\to[0,1]$ denote the lower density (Reeve et al., 2021) given by
\[
\rho_{\nu,s}(x):=\inf_{r\in(0,1)}\frac{\nu\big(B_r(x)\big)}{r^s}.\tag{8}
\]
''',[7],'Section 2 — lower density (8)',symbols=[r'\rho_{\nu,s}(x)'],shape='Infimum of open Euclidean ball probabilities divided by r^s for radii strictly between zero and one. The scale exponent s can be less than ambient dimension d; no Lebesgue density or uniformly positive lower bound is required.')
add('D19','tail parameters',r'''
Fix $\boldsymbol\gamma=(\gamma_1,\ldots,\gamma_d)^\mathrm T\in[0,\infty)^d$, $C_{\mathrm L}\ge1$ and $\mathcal O\subseteq\{0,1\}^d$. For $\omega=(\omega_1,\ldots,\omega_d)^\mathrm T\in\{0,1\}^d\setminus\{\mathbf0_d\}$, let $\gamma_\omega:=\min\{\gamma_j:\omega_j=1\}$.
''',[7],'Definition 3 — patternwise tail parameter',symbols=[r'\gamma_\omega:=\min'],context='In Section S1.1, we study specific instances of our examples above and in particular characterise which tail parameters we can choose in the class $\mathcal Q_{\mathrm L}(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)$.',shape='Minimum coordinate tail exponent over the selected coordinates of a nonzero pattern. Gamma is a vector, gamma_omega a scalar. No nonzero-pattern positivity follows from the bare [0,infinity)^d domain.')
add('D20','marginal feature distributions',r'''
Let $\mathcal Q_{\mathrm L}(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)$ denote the subclass of $\mathcal Q_{\mathrm{Miss}}(\mathcal O)$ for which
\[
\mu_\omega\left(\left\{x\in\mathbb R^d:\min_{o\in\mathcal O:\omega\preceq o}\rho_{\mu_{\omega\mid o},d_\omega}(x)<\xi\right\}\right)\le C_{\mathrm L}\cdot\xi^{\gamma_\omega}\tag{9}
\]
for all $\xi>0$ and all $\omega\in\{0,1\}^d\setminus\{\mathbf0_d\}$.
''',[7],'Definition 3 — lower-density tail condition',{'D10':'The distribution class retains the original missingness restrictions.','D12':'The outer measure is the unconditional masked test-feature distribution.','D13':'The lower density is calculated for each conditional training-feature distribution.','D18':'The small-density event uses the lower density at exponent d_omega.','D19':'The decay exponent is the minimum selected-coordinate gamma.','D1':'Compatible masks and pattern dimension use the original order and Hamming weight.'},context='Our next condition concerns the regularity of the marginal feature distributions.',symbols=[r'\mathcal Q_{\mathrm L}(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)',r'\rho_{\mu_{\omega\mid o},d_\omega}(x)<\xi'],shape='Controls small conditional lower densities under the unconditional test-feature measure, for all nonzero patterns and every positive threshold. Strict inequality, compatible-mask minimum and distinct inner/outer measures are retained.')
add('D21','smoothness',r'''
Fix $\boldsymbol\beta=(\beta_1,\ldots,\beta_d)^\mathrm T\in(0,1]^d$ and $C_{\mathrm S}\ge1$. For $\omega=(\omega_1,\ldots,\omega_d)^\mathrm T\in\{0,1\}^d\setminus\{\mathbf0_d\}$, let $\beta_\omega:=\min\{\beta_j:\omega_j=1\}$.
''',[8],'Definition 4 — patternwise smoothness exponent',symbols=[r'\beta_\omega:=\min'],context='The remaining conditions on our class of distributions concern the smoothness of the functions $f_\omega$, which contribute to the decomposition in (6), and a standard margin assumption on the regression function $\eta$.',shape='Positive smoothness exponent at most one, obtained by minimizing over selected coordinates of a nonzero pattern. Bold beta denotes the coordinate vector.')
add('D22','smoothness',r'''
Let $\mathcal P_{\mathrm S}(\boldsymbol\beta,C_{\mathrm S})$ denote the class of distributions for which
\[
|f_\omega(x_1)-f_\omega(x_2)|\le C_{\mathrm S}\cdot\|x_1^\omega-x_2^\omega\|_2^{\beta_\omega}\tag{10}
\]
for all $x_1,x_2\in\operatorname{supp}(\mu)$ and all $\omega\in\{0,1\}^d\setminus\{\mathbf0_d\}$.
''',[8],'Definition 4 — componentwise smoothness class',{'D11':'Smoothness is imposed on each original anova component.','D21':'Its exponent is the minimum selected-coordinate beta.','D2':'The distance is between the masked feature vectors.','D4':'The point pair lies in the unconditional feature support.'},context='The remaining conditions on our class of distributions concern the smoothness of the functions $f_\omega$, which contribute to the decomposition in (6), and a standard margin assumption on the regression function $\eta$.',symbols=[r'\mathcal P_{\mathrm S}(\boldsymbol\beta,C_{\mathrm S})',r'\|x_1^\omega-x_2^\omega\|_2^{\beta_\omega}'],shape='Supportwise Holder condition with Euclidean distance in selected coordinates for every nonzero component. It is a condition on P, not on the mask law, and is not replaced by a single global smoothness assumption on eta.')
add('D23','margin condition',r'''
Fix $\alpha\in[0,\infty)$ and $C_{\mathrm M}\ge1$. Let $\mathcal P_{\mathrm M}(\alpha,C_{\mathrm M})$ denote the class of distributions for which
\[
\mu\big(\{x\in\mathbb R^d:|\eta(x)-1/2|<t\}\big)\le C_{\mathrm M}\cdot t^\alpha
\]
for all $t>0$.
''',[8],'Definition 5',{'D4':'The margin event uses eta and the unconditional feature marginal mu.'},context='Our final definition is the standard margin condition (e.g. Polonik, 1995; Mammen and Tsybakov, 1999).',symbols=[r'\mathcal P_{\mathrm M}(\alpha,C_{\mathrm M})',r'|\eta(x)-1/2|<t'],shape='Strict small-margin event includes exact ties eta=1/2. The condition holds for every positive t, and alpha=0 is allowed. Do not insert the common alternative event 0<|eta-1/2|<=t.')
add('D24','class of distributions',r'''
More precisely, for $\Omega_\star\in\mathcal I(\{0,1\}^d)\setminus\{\{\mathbf0_d\},\emptyset\}$, $c_{\mathrm E}\in[0,1/4]$, $\boldsymbol\gamma\in[0,\infty)^d$, $C_{\mathrm L}>1$, $\boldsymbol\beta\in(0,1]^d$, $C_{\mathrm S}\ge1$, $\alpha\in[0,\infty)$, $C_{\mathrm M}\ge1$ and $\mathcal O\subseteq\{0,1\}^d$, we write
\[
\begin{aligned}
\mathcal Q'_{\mathrm{Miss}}&\equiv\mathcal Q'_{\mathrm{Miss}}(\Omega_\star,c_{\mathrm E},\boldsymbol\gamma,C_{\mathrm L},\boldsymbol\beta,C_{\mathrm S},\alpha,C_{\mathrm M},\mathcal O)\\
&:=\mathcal Q_{\mathrm E}(\Omega_\star,c_{\mathrm E},\mathcal O)\cap\mathcal Q_{\mathrm L}(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)\cap\{Q\in\mathcal Q:P\equiv P_Q\in\mathcal P_{\mathrm S}(\boldsymbol\beta,C_{\mathrm S})\cap\mathcal P_{\mathrm M}(\alpha,C_{\mathrm M})\}.\tag{11}
\end{aligned}
\]
''',[8],'Section 2 — minimax distribution class (11)',{'D17':'The intersection includes the interaction support and signal class.','D20':'It includes the unconditional-measure lower-density tail class.','D22':'The test marginal must satisfy componentwise smoothness.','D23':'The test marginal must satisfy the margin restriction.','D15':'The active pattern set is a nontrivial antichain.','D3':'P_Q is the marginal of the joint distribution.'},context='In Theorem 1 below we provide our main minimax result, in which the class of distributions of interest is the intersection of the classes given in Definitions 1 to 5.',symbols=[r"\mathcal Q'_{\mathrm{Miss}}"],shape='Intersection class for the minimax theorem. Includes missingness through its component classes, and P-level smoothness/margin conditions through P_Q. This is the prime class, not the stronger plus class used by HAM.')
add('D25','available cases',r'''
To that end, for fixed $o_1,\ldots,o_n\in\mathcal O$, let $n_\omega:=\sum_{i=1}^n\mathbb1_{\{\omega\preceq o_i\}}$ denote the number of available cases for the observation pattern $\omega\in\{0,1\}^d$,
''',[8],'Section 2 — available-case counts at fixed masks',{'D1':'A case is available when its mask contains omega.'},symbols=[r'n_\omega:=\sum_{i=1}^n'],shape='Deterministic count after conditioning on the mask sequence; not n times a mask probability and not the count of exact mask matches. A containing mask may contribute to several patterns.')
add('D26','observation patterns',r'''
and define $\mathcal N:=\{\omega\in\{0,1\}^d:n_\omega>0\}$ to be the set of observation patterns for which we have training data.
''',[8],'Section 2 — patterns with at least one available case',{'D25':'Availability is determined by the fixed-mask counts n_omega.'},symbols=[r'\mathcal N:='],shape='Downward-closed set of all patterns supported by at least one observed mask, distinct from O, the allowed conditioning masks. It always contains the zero pattern for positive n. Its complement is taken in the Boolean pattern universe.')
add('D27','log',r'''Finally, for $x\in\mathbb R$, we write $\log_+(x):=\log(x\vee e)$.''',[3],'Section 1 — lower-truncated logarithm',symbols=[r'\log_+(x)'],shape='Logarithm truncated below at one by taking max(x,e). It is not log(1+x) or max(log(x),0).')
add('D28','Hard-thresholding Anova Missing data classifier',r'''
1: Input: Data $D_n=((X_1^{o_1},Y_1,o_1),\ldots,(X_n^{o_n},Y_n,o_n))\in(\mathbb R^d\times\{0,1\}\times\{0,1\}^d)^n$, $\boldsymbol\gamma\in[0,\infty)^d$, $\boldsymbol\beta\in(0,1]^d$, $\alpha\in[0,\infty)$, and a test point $x_0\in\mathbb R^d$

2: $\widehat f_{\mathbf0}(\cdot):=\frac1n\sum_{i=1}^nY_i-\frac12$

3: for $d'=1,\ldots,d$ do

4: for $\omega\in\mathcal N$ such that $d_\omega=d'$ do

5: $k_\omega:=1+\lfloor n_\omega^{\frac{2\beta_\omega\gamma_\omega}{\gamma_\omega(2\beta_\omega+d_\omega)+\alpha\beta_\omega}}\rfloor$; $\tau_\omega:=2^{-4}\cdot n_\omega^{-\frac{\beta_\omega\gamma_\omega}{2[\gamma_\omega(2\beta_\omega+d_\omega)+\alpha\beta_\omega]}}$; $N_\omega:=\{i\in[n]:\omega\preceq o_i\}$

6: for $x\in\{X_i^{o_i}:i\in N_\omega\}\cup\{x_0\}$ do

7: Let $(X_{(1)_\omega}^\omega(x),Y_{(1)_\omega}(x)),\ldots,(X_{(n_\omega)}^\omega(x),Y_{(n_\omega)_\omega}(x))$ be a reordering of the pairs $\{(X_i^{o_i},Y_i):i\in N_\omega\}$ such that $\|X_{(1)_\omega}^\omega(x)-x^\omega\|\le\cdots\le\|X_{(n_\omega)_\omega}^\omega(x)-x^\omega\|$

8: $\widehat f_\omega(x):=\frac1{k_\omega}\sum_{j=1}^{k_\omega}Y_{(j)_\omega}(x)-\frac12-\sum_{\omega'\prec\omega}\widehat f_{\omega'}(x)$

9: end for

10: $\widehat\sigma_\omega^2:=\frac1{n_\omega}\sum_{i\in N_\omega}\widehat f_\omega^2(X_i^\omega)$

11: end for

12: end for

13: $\widehat\Omega=\emptyset$

14: for $d'=d,d-1,\ldots,1$ do

15: for $\omega\in\mathcal N$ with $d_\omega=d'$, $U(\{\omega\})\cap\widehat\Omega=\emptyset$ do

16: if $\widehat\sigma_\omega^2\ge\tau_\omega$ then $\widehat\Omega=\widehat\Omega\cup\{\omega\}$

17: end if

18: end for

19: end for

20: $\widehat\eta(x_0):=\frac12+\sum_{\omega\in\widehat\Omega\cup L(\widehat\Omega)}\widehat f_\omega(x_0)$

21: Output: $\widehat C_{\mathrm{HAM}}(x_0):=\mathbb1_{\{\widehat\eta(x_0)\ge1/2\}}$
''',[11],'Algorithm 1 — Hard-thresholding Anova Missing data classifier',{'D5':'The input is the observed masked training data.','D2':'The nearest-neighbor distance and evaluations use projected feature vectors.','D1':'Pattern dimension and predecessor order determine the loops and recursive subtraction.','D19':'The chosen neighborhood size and threshold use gamma_omega.','D21':'Those tuning quantities also use beta_omega.','D25':'The formulas use available-case counts n_omega.','D26':'The loops run over patterns with data.','D16':'The selection loop uses U and the reconstruction uses L.'},context=r'Algorithm 1 The Hard-thresholding Anova Missing data classifier $\widehat C_{\mathrm{HAM}}$.',symbols=[r'\widehat C_{\mathrm{HAM}}(x_0)',r'\widehat\sigma_\omega^2',r'U(\{\omega\})\cap\widehat\Omega=\emptyset'],shape='All 21 printed lines, preserving both dimension-order loops, nearest-neighbor residual estimates, empirical signal, threshold, antichain selection and final half-threshold. The original algorithm contains neighbor-count, projection and selection ambiguities recorded separately; no corrected implementation is substituted.',note='The literal U({omega}) condition can reject incomparable patterns as well as predecessors of an already selected pattern, unlike the accompanying prose. Also k_omega=2 when n_omega=1, exceeding the available sample, with no printed cap. Preserve both issues for downstream formalization.')
add('D29','marginal feature distributions',r'''
Fix $\boldsymbol\gamma=(\gamma_1,\ldots,\gamma_d)^\mathrm T\in[0,\infty)^d$, $C_{\mathrm L}\ge1$ and $\mathcal O\subseteq\{0,1\}^d$. Then let $\mathcal Q_{\mathrm L}^+(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)$ denote the class of distributions for which (9) holds and
\[
\max_{\widetilde o\in\mathcal O:\omega\preceq\widetilde o}\mu_{\omega\mid\widetilde o}\left(\left\{x\in\mathbb R^d:\min_{o\in\mathcal O:\omega\preceq o}\rho_{\mu_{\omega\mid o},d_\omega}(x)<\xi\right\}\right)\le C_{\mathrm L}\cdot\xi^{\gamma_\omega}
\]
for all $\xi>0$ and all $\omega\in\{0,1\}^d\setminus\{\mathbf0_d\}$.
''',[11],'Definition 3+',{'D20':'The strengthened condition explicitly retains (9).','D13':'The extra outer measure ranges over conditional training-feature laws.','D18':'The inner event uses conditional lower densities.','D19':'The exponent is the same patternwise gamma.','D1':'Both mask ranges must contain omega and density dimension is d_omega.'},context='we will require a slightly stronger assumption on the properties of the marginal feature distributions in our class, namely we ask for control of the $\mu_{\omega\mid o}$ tails.',symbols=[r'\mathcal Q_{\mathrm L}^+(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)',r'\mu_{\omega\mid\widetilde o}'],shape='Strengthens (9) by controlling the same small-lower-density event under every compatible conditional feature measure, as well as under the original unconditional measure. Not equivalent to the original tail class.')
add('D30','class of distributions',r'''
Now, to state our main theoretical result about Algorithm 1, we will write $\mathcal Q^+_{\mathrm{Miss}}\equiv\mathcal Q^+_{\mathrm{Miss}}(\Omega_\star,c_{\mathrm E},\boldsymbol\gamma,C_{\mathrm L},\boldsymbol\beta,C_{\mathrm S},\alpha,C_{\mathrm M},\mathcal O)$ for the class of distributions that arises when we replace $\mathcal Q_{\mathrm L}(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)$ in the class $\mathcal Q'_{\mathrm{Miss}}$ in (11) with $\mathcal Q_{\mathrm L}^+(\boldsymbol\gamma,C_{\mathrm L},\mathcal O)$.
''',[11],'Section 3 — distribution class for the HAM guarantee',{'D24':'The original intersection structure and other constituent conditions come from (11).','D29':'The tail constituent is replaced by Definition 3+.'},symbols=[r'\mathcal Q^+_{\mathrm{Miss}}'],shape='HAM distribution class with the stronger conditional-measure tail control. Theorem 2 permits C_L=1 whereas the introductory parameter range for (11) says C_L>1; the constituent tail definitions allow C_L>=1, and the source extension is recorded without altering its text.')

def main():
    for lid,m in members.items():
        assert all(d in members for d in m['depends_on']),(lid,'unknown dependency')
        assert any(s in m['statement_original']+' '+m['local_label'] for s in m['highlight_symbols']+m['highlight_phrases']),(lid,'missing own-source highlight')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source passages and their local dependencies; source audit remains pending.')

if __name__ == "__main__":
    main()
