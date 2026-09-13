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


add('D2','probability distributions',r'''
In this paper, we assume a stylized model whereby the rows $\boldsymbol\Lambda,\boldsymbol\Theta$ are mutually independent (and independent of $\boldsymbol Z$) with $(\boldsymbol\Lambda_i)_{i\le n}\overset{\mathrm{iid}}\sim\mu_\Lambda$ and $(\boldsymbol\Theta_j)_{j\le d}\overset{\mathrm{iid}}\sim\mu_\Theta$. Here, $\mu_\Lambda$ and $\mu_\Theta$ are fixed probability distributions on $\mathbb R^r$. We will be concerned with the problem of determining the Bayes optimal estimation error under the idealized setting in which the distributions $\mu_\Lambda,\mu_\Theta$ and the signal-to-noise ratio $s_n$ are known to the statistician.
''',[3],'Introduction — fixed independent factor distributions',kind='source_passage',symbols=[r'\mu_\Lambda',r'\mu_\Theta'],phrases=['mutually independent'],shape='Fixed known row priors for the two factors, with mutual independence and independence of the Gaussian noise. The prior laws do not change with n,d; rank is fixed.')
add('D1','spiked model',r'''
In the spiked model, we observe a matrix $\boldsymbol A\in\mathbb R^{n\times d}$ which is given by the sum of a low-rank signal and random noise
\[
\boldsymbol A=s_n\boldsymbol\Lambda\boldsymbol\Theta^{\mathsf T}+\boldsymbol Z.\tag{1}
\]
Here, $\boldsymbol\Lambda\in\mathbb R^{n\times r}$, $\boldsymbol\Theta\in\mathbb R^{d\times r}$ are factors which we would like to estimate and $\boldsymbol Z$ is a noise matrix with i.i.d. entries $Z_{ij}\sim\mathsf N(0,1)$. Finally, $s_n\in\mathbb R_{>0}$ is a signal-to-noise ratio which we also assume to be known. We will consider high-dimensional asymptotics whereby $d,n\to\infty$ with $r$ fixed. In what follows, we will denote by $\boldsymbol a_1,\ldots,\boldsymbol a_n$ the rows of $\boldsymbol A$.
''',[3],'Spiked model — equation (1)',{'D2':'The model is specialized in the same introduction to fixed independent factor-row priors, independent of Z.'},kind='source_passage',symbols=[r'\boldsymbol A=s_n\boldsymbol\Lambda\boldsymbol\Theta^{\mathsf T}+\boldsymbol Z'],shape='Rectangular additive Gaussian observation with known positive signal scale and fixed rank. Neither the strong nor weak normalization is part of the generic model.')
add('D3','strong signal regime',r'''
We first consider the strong signal regime in which we set $s_n=1/\sqrt n$, and therefore we have
\[
\boldsymbol A=\frac1{\sqrt n}\boldsymbol\Lambda\boldsymbol\Theta^{\mathsf T}+\boldsymbol Z\in\mathbb R^{n\times d}.\tag{4}
\]
''',[7],'Strong signal regime — equation (4)',{'D1':'Equation (4) fixes s_n=1/sqrt(n) in the spiked model (1).'},kind='source_passage',symbols=[r's_n=1/\sqrt n',r'\frac1{\sqrt n}\boldsymbol\Lambda\boldsymbol\Theta^{\mathsf T}'],shape='Exact strong-signal normalization, under the fixed-prior model. Its theorems take n,d to infinity with d/n to infinity.')
add('D4','weak signal regime',r'''
In this section, we consider the weak signal regime where $s_n=1/\sqrt[4]{nd}$. Thus the model of interest is
\[
\boldsymbol A=\frac1{\sqrt[4]{nd}}\boldsymbol\Lambda\boldsymbol\Theta^{\mathsf T}+\boldsymbol Z\in\mathbb R^{n\times d}.\tag{9}
\]
For convenience, we define $r_n:=\sqrt[4]{d/n}$. By assumption, we see that $r_n\to\infty$ as $n,d\to\infty$.
''',[8],'Weak signal regime — equation (9)',{'D1':'Equation (9) fixes the scale of model (1) to (nd)^(-1/4).'},kind='source_passage',symbols=[r's_n=1/\sqrt[4]{nd}',r'r_n:=\sqrt[4]{d/n}'],shape='Exact weak-signal normalization and aspect-ratio scale. Do not use the strong-signal observation when interpreting its risks.')
add('D5','second moments',r'''
We define $\boldsymbol Q_\Lambda:=\mathbb E_{\Lambda_0\sim\mu_\Lambda}[\boldsymbol\Lambda_0\boldsymbol\Lambda_0^{\mathsf T}]\in S_r^+$ and $\boldsymbol Q_\Theta:=\mathbb E_{\Theta_0\sim\mu_\Theta}[\boldsymbol\Theta_0\boldsymbol\Theta_0^{\mathsf T}]\in S_r^+$. Before we proceed, we establish the following conventions for the distributions $\mu_\Lambda,\mu_\Theta$.
''',[7],'Second-moment matrices before Remark 3.1',context='Assume $\mu_\Lambda,\mu_\Theta$ have finite non-singular second moments',symbols=[r'\boldsymbol Q_\Lambda',r'\boldsymbol Q_\Theta'],shape='Uncentered second-moment matrices. They are not covariances unless the corresponding mean vanishes; in particular the factor Lambda in the clustering example has nonzero mean.')
add('D6','invertible',r'''
Without loss of generality we can and will assume that both $\boldsymbol Q_\Lambda$ and $\boldsymbol Q_\Theta$ are invertible. Furthermore, we can assume that $\boldsymbol Q_\Theta=q_\Theta\boldsymbol I_r$ for some $q_\Theta\in\mathbb R_{>0}$.
''',[7],'Remark 3.1 — second-moment normalization',{'D5':'The conditions refer to the two second-moment matrices defined immediately above.'},kind='condition',symbols=[r'\boldsymbol Q_\Theta=q_\Theta\boldsymbol I_r'],phrases=['invertible'],shape='Positive-definite second moments and isotropic Theta second moment, after the described reparameterization. Finite moment existence is retained from the model/theorem conventions.')
add('D7','spectral estimator',r'''
Denote by $\widehat{\boldsymbol\Lambda}_s\in\mathbb R^{n\times r}$ the matrix whose columns are the top $r$ eigenvectors of $\boldsymbol A\boldsymbol A^{\mathsf T}$, normalized so that $\widehat{\boldsymbol\Lambda}_s^{\mathsf T}\widehat{\boldsymbol\Lambda}_s/n=\boldsymbol I_r$.
''',[7],'Section 3.1 — spectral estimator',{'D3':'The matrix A is observed under the strong signal experiment in this section.'},context='We will show that a simple spectral estimator provides a consistent estimate up to a rotation in the $r$-dimensional Euclidean space.',symbols=[r'\widehat{\boldsymbol\Lambda}_s',r'\widehat{\boldsymbol\Lambda}_s^{\mathsf T}\widehat{\boldsymbol\Lambda}_s/n=\boldsymbol I_r'],shape='Top-r eigenvectors with squared column norm n. It estimates a column space; the source does not choose signs or a unique basis at repeated eigenvalues.')
add('D8','estimation loss',r'''
Denote by $\boldsymbol P,\widehat{\boldsymbol P}\in\mathcal O(n)$ the projection matrices onto the column spaces of $\boldsymbol\Lambda$ and $\widehat{\boldsymbol\Lambda}_s$, respectively. We use the following distance between the two subspaces as estimation loss
\[
L^{\sin}(\widehat{\boldsymbol\Lambda}_s,\boldsymbol\Lambda):=\|\boldsymbol P(\boldsymbol I-\widehat{\boldsymbol P})\|_{\mathrm{op}}=\|\widehat{\boldsymbol P}(\boldsymbol I-\boldsymbol P)\|_{\mathrm{op}}=\sin\alpha(\widehat{\boldsymbol\Lambda}_s,\boldsymbol\Lambda),\tag{5}
\]
where $\alpha(\widehat{\boldsymbol\Lambda}_s,\boldsymbol\Lambda)$ is the principal angle between the two column spaces.
''',[7],'Section 3.1 — subspace estimation loss (5)',{'D7':'The estimated column space is that of the specified spectral estimator.'},symbols=[r'L^{\sin}',r'\|\boldsymbol P(\boldsymbol I-\widehat{\boldsymbol P})\|_{\mathrm{op}}'],shape='Operator-norm distance between column-space projectors. The source incorrectly places projection matrices in the orthogonal group O(n); preserve the original passage and flag it separately. The largest-angle convention and finite-sample rank degeneracy are not explicitly qualified.')
add('D9','identifiability conditions',r'''
Let $\boldsymbol\Lambda_0\sim\mu_\Lambda$. If we further assume that there does not exist $\boldsymbol\Omega\in\mathcal O(r)$, such that $\boldsymbol\Omega\ne\boldsymbol I_r$ and $\boldsymbol\Omega\boldsymbol\Lambda_0\overset d=\boldsymbol\Lambda_0$,
''',[7],'Theorem 3.1 — identifiability hypothesis in claim 3',kind='theorem_excerpt',context=r'According to Theorem 3.1, $\boldsymbol\Lambda$ can be estimated consistently under identifiability conditions.',context_pages=[8],symbols=[r'\boldsymbol\Omega\ne\boldsymbol I_r',r'\boldsymbol\Omega\boldsymbol\Lambda_0\overset d=\boldsymbol\Lambda_0'],shape='No nonidentity orthogonal symmetry of the Lambda-row distribution. This is a distributional identifiability hypothesis, not merely full rank or nonzero mean. Claim 2 has its own higher-moment condition.')
add('D10','GOE',r'''
$\operatorname{GOE}(n)$ denotes the distribution of a symmetric matrix with independent entries on or above the diagonal $(W_{ij})_{i\le j}$ such that $W_{ii}\sim\mathsf N(0,2/n)$ and $W_{ij}\sim\mathsf N(0,1/n)$ for $i<j$.
''',[5],'Introduction — GOE normalization',symbols=[r'\operatorname{GOE}(n)',r'W_{ii}\sim\mathsf N(0,2/n)',r'W_{ij}\sim\mathsf N(0,1/n)'],shape='Real symmetric Gaussian noise with diagonal variance 2/n and off-diagonal variance 1/n. This normalization differs from an unscaled GOE convention.')
add('D11','symmetric spiked model',r'''
Under this model we observe $\boldsymbol Y\in\mathbb R^{n\times n}$ given by
\[
\boldsymbol Y=\frac{q_\Theta}{n}\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}+\boldsymbol W,\tag{10}
\]
where $\boldsymbol W\overset d=\operatorname{GOE}(n)$, and $\boldsymbol\Lambda_i\overset{\mathrm{iid}}\sim\mu_\Lambda$, independent of each other. We view $q_\Theta>0$ as a signal-to-noise ratio parameter.
''',[9],'Symmetric spiked model — equation (10)',{'D10':'The observation noise has the GOE distribution with the normalization defined on page 5.'},kind='source_passage',context='estimation under model (9) is equivalent to estimation under a symmetric spiked model.',symbols=[r'\boldsymbol Y=\frac{q_\Theta}{n}\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}+\boldsymbol W'],shape='Symmetric Gaussian experiment involving the Lambda prior only. q_Theta is the signal parameter here; no Theta factor or asymmetry assumptions are part of this stand-alone experiment.')
add('D12','Bayesian MMSE',r'''
We denote the Bayesian MMSE of model (10) by
\[
\operatorname{MMSE}_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta):=\min_{\widehat{\boldsymbol M}(\cdot)}\frac1{n^2}\mathbb E\left[\left\|\widehat{\boldsymbol M}(\boldsymbol Y)-\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}\right\|_F^2\right].\tag{11}
\]
Note that the Bayesian MMSE is achieved by the posterior expectation $\widehat{\boldsymbol M}(\boldsymbol Y)=\mathbb E[\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}\mid\boldsymbol Y]$.
''',[9],'Bayesian MMSE — symmetric model (11)',{'D11':'The risk and posterior expectation are under the symmetric experiment (10).'},symbols=[r'\operatorname{MMSE}_n^{\mathrm{symm}}',r'\frac1{n^2}'],shape='Optimal Frobenius squared risk for Lambda Lambda^T, normalized by n^2, using Y. The printed definition uses a minimum, whereas the asymmetric definition uses an infimum.')
add('D13','normalized mutual information',r'''
We also define the normalized mutual information
\[
\mathrm I_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta):=\frac1n\mathbb E\log\frac{d\mathbb P_{\boldsymbol\Lambda,\boldsymbol Y}}{d(\mathbb P_{\boldsymbol\Lambda}\times\mathbb P_{\boldsymbol Y})}(\boldsymbol\Lambda,\boldsymbol Y).\tag{12}
\]
''',[9],'Normalized mutual information — symmetric model (12)',{'D11':'The joint and marginal laws are those of Lambda and Y in (10).'},symbols=[r'\mathrm I_n^{\mathrm{symm}}'],shape='Mutual information between the latent Lambda matrix and Y, normalized by n. It is not information per matrix entry and is not defined between Y and the pair of both factors.')
add('D14','free energy functional',r'''
For $s>0$ and $\boldsymbol Q\in S_r^+$, we define the free energy functional $\mathcal F(s,\boldsymbol Q)$ and its maximizer $\boldsymbol Q^*(s)\in S_r^+$ via
\[
\mathcal F(s,\boldsymbol Q):=-\frac s4\|\boldsymbol Q\|_F^2+\mathbb E\left\{\log\left(\int\exp\left(\sqrt s\boldsymbol z^{\mathsf T}\boldsymbol Q^{1/2}\boldsymbol\lambda+s\boldsymbol\lambda^{\mathsf T}\boldsymbol Q\boldsymbol\Lambda_0-\frac s2\boldsymbol\lambda^{\mathsf T}\boldsymbol Q\boldsymbol\lambda\right)\mu_\Lambda(d\boldsymbol\lambda)\right)\right\}.\tag{13}
\]
''',[9],'Free energy functional — equation (13)',symbols=[r'\mathcal F(s,\boldsymbol Q)',r'\sqrt s\boldsymbol z^{\mathsf T}\boldsymbol Q^{1/2}\boldsymbol\lambda'],shape='Functional of a positive semidefinite r-by-r matrix, with independent Lambda_0~mu_Lambda and standard Gaussian z; this expectation convention is recorded as adjacent source context. No asymmetric Theta-prior assumption is required to define it.')
add('D15','maximizer',r'''
\[
\boldsymbol Q^*(s)\in\operatorname*{argmax}_{\boldsymbol Q\in S_r^+}\mathcal F(s,\boldsymbol Q).\tag{14}
\]
''',[9],'Free energy maximizer — equation (14)',{'D14':'The maximizer is taken over the positive semidefinite domain of the free energy functional (13).'},context=members['D14']['statement_original'],symbols=[r'\boldsymbol Q^*(s)'],shape='Any maximizing matrix, not a stated unique optimizer. Theorem 4.1 leaves s unbound in its MMSE formula; retain that literal source notation.')
add('D16','matrix mean square error',r'''
For simplicity, we will restrict ourselves to studying the matrix mean square error:
\[
\operatorname{MMSE}_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta):=\inf_{\widehat{\boldsymbol M}(\cdot)}\frac1{n^2}\mathbb E\left[\left\|\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}-\widehat{\boldsymbol M}(\boldsymbol A)\right\|_F^2\right],\tag{15}
\]
where the infimum is taken over all estimators (measurable functions) $\widehat{\boldsymbol M}:\boldsymbol A\mapsto\widehat{\boldsymbol M}(\boldsymbol A)\in\mathbb R^{n\times n}$. Of course $\operatorname{MMSE}_n^{\mathrm{asym}}$ depends on the distributions $\mu_\Lambda,\mu_\Theta$.
''',[10],'Matrix mean square error — asymmetric model (15)',{'D4':'The input A is observed in the weak signal model (9).'},symbols=[r'\operatorname{MMSE}_n^{\mathrm{asym}}'],shape='Infimum over measurable estimators of the Lambda Gram matrix from A, normalized by n^2. Definition does not impose the additional sub-Gaussian/third-moment hypothesis later used to prove comparison theorems.')
add('D17','sub-Gaussian',r'''
We assume $\mathbb E[\boldsymbol\Theta_0]=\boldsymbol0_r$, $\mathbb E[\boldsymbol\Theta_0\otimes\boldsymbol\Theta_0\otimes\boldsymbol\Theta_0]=\boldsymbol0_{r\times r\times r}$, where $\otimes$ denotes the tensor product. Furthermore, we assume that $\mu_\Theta,\mu_\Lambda$ are sub-Gaussian.
''',[10],'Assumption 4.1',kind='assumption',symbols=[r'\mathbb E[\boldsymbol\Theta_0]',r'\boldsymbol\Theta_0\otimes\boldsymbol\Theta_0\otimes\boldsymbol\Theta_0'],phrases=['sub-Gaussian'],shape='Original combined assumption: zero first and full third tensor moments of Theta, plus sub-Gaussian laws for both factors. It does not require zero mean or zero third moment of Lambda. No sub-Gaussian norm convention is defined in main text.')
add('D18','mutual information per coordinate',r'''
Define the mutual information per coordinate in asymmetric model of Eqs. (9), via
\[
\mathrm I_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta):=\frac1n\mathbb E\log\frac{d\mathbb P_{\boldsymbol\Lambda,\boldsymbol A}}{d(\mathbb P_{\boldsymbol\Lambda}\times\mathbb P_{\boldsymbol A})}(\boldsymbol\Lambda,\boldsymbol A).\tag{16}
\]
''',[10],'Theorem 4.3 — mutual information definition (16)',{'D4':'The joint and marginal laws involve Lambda and the weak-signal observation A.'},kind='theorem_excerpt',symbols=[r'\mathrm I_n^{\mathrm{asym}}'],shape='Mutual information between Lambda and A normalized by n. Conditions referenced from Theorem 4.3 by later theorems do not import its mutual-information conclusion as a definition dependency.')
add('D19','modified model',r'''
Further, consider a modified model in which the statistician observes $(\boldsymbol A,\boldsymbol Y'(\varepsilon))$, where $\boldsymbol A$ is given by Eq. (9), and
\[
\boldsymbol Y'(\varepsilon):=\frac{\sqrt\varepsilon}{n}\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}+\boldsymbol W',\qquad\boldsymbol W'\sim\operatorname{GOE}(n).
\]
Here, we assume $\boldsymbol W'$ is independent of everything else.
''',[11],'Theorem 4.4 — modified observation model',{'D4':'A retains the weak-signal model (9).','D10':'The independent auxiliary symmetric noise W-prime uses the same GOE normalization.'},kind='theorem_excerpt',symbols=[r"\boldsymbol Y'(\varepsilon)",r'\frac{\sqrt\varepsilon}{n}'],shape='Additional symmetric observation at signal sqrt(epsilon), with independent noise and the same latent Lambda. It does not replace A. Epsilon tends to zero only after the dimension limit in the theorem.')
add('D20','matrix mean square error',r'''
Denote by $\operatorname{MMSE}_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta;\varepsilon)$ the corresponding matrix mean square error.
''',[11],'Theorem 4.4 — matrix error with additional observation',{'D19':'The statistician may use both A and Y-prime(epsilon).','D16':'Corresponding matrix mean square error retains the Lambda Gram target, squared Frobenius loss and n^-2 normalization of (15).'},kind='theorem_excerpt',symbols=[r'\operatorname{MMSE}_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta;\varepsilon)'],shape='Bayesian Gram-matrix risk using the augmented observation. The source defines it by correspondence, without printing a second full infimum formula.')
add('D21','global maximum',r'''
For the case $r=1$, define $Y=\sqrt\gamma\Lambda_0+G$ with $G\sim\mathsf N(0,1)$ independent of $\Lambda_0\sim\mu_\Lambda$, and define $\mathsf I(\gamma)=\mathbb E\log\frac{dp_{Y\mid\Lambda_0}}{dp_Y}(Y,\Lambda_0)$. Let
\[
\Psi(\gamma,s)=\frac{s^2}4+\frac{\gamma^2}{4s}-\frac\gamma2+\mathsf I(\gamma).
\]
Assume that the global maximum of $\gamma\mapsto\Psi(\gamma,q_\Theta)$ over $(0,\infty)$ is also the first stationary point of the same function.
''',[12],'Theorem 4.5 — alternative (c)',kind='theorem_excerpt',symbols=[r'\Psi(\gamma,s)',r'\mathsf I(\gamma)'],phrases=['global maximum','first stationary point'],shape='Original rank-one scalar-channel alternative. The printed positive quadratic plus nonnegative mutual information is unbounded above for fixed positive s, conflicting with an attained global maximum on (0,infinity). Record this source problem without changing maximum to minimum or altering signs.')
add('D22','Gaussian mixture model',r'''
We next consider the case of $k\ge2$ clusters with approximately orthogonal centers. We denote by $\{\boldsymbol\Theta_{\cdot i}/\sqrt[4]{nd}:i\in[k]\}\subseteq\mathbb R^d$ the cluster centers. Let $\boldsymbol\Theta\in\mathbb R^{d\times k}$ with the $i$-th column given by $\boldsymbol\Theta_{\cdot i}$. For $j\in[d]$, we let $\boldsymbol\Theta_j\in\mathbb R^k$ be the $j$-th row of $\boldsymbol\Theta$. We assume $\boldsymbol\Theta_j\overset{\mathrm{iid}}\sim\mu_\Theta$, where $\mu_\Theta$ is sub-Gaussian with vanishing first and third moments and diagonal covariance: $\operatorname{Cov}(\boldsymbol\Theta_1)=q_\Theta\boldsymbol I_k$.

Let $\boldsymbol e_j$ be the $j$-th standard basis vector in $\mathbb R^k$. We encode the data point labels by setting $\boldsymbol\Lambda_i=\boldsymbol e_j$ if and only if the $i$-th sample belongs to the $j$-th cluster, and consider the case of equal proportions, so that $(\boldsymbol\Lambda_i)_{i\le n}\overset{\mathrm{iid}}\sim\operatorname{Unif}(\{\boldsymbol e_1,\cdots,\boldsymbol e_k\})$.

As before, we let $\boldsymbol A\in\mathbb R^{n\times d}$ be the matrix whose rows are i.i.d. samples $\boldsymbol a_i$ from the Gaussian mixture model with centers $\{\boldsymbol\Theta_{\cdot i}/\sqrt[4]{nd}:i\in[k]\}$. With these definitions, the matrix $\boldsymbol A$ is distributed according to model (9).
''',[14],'Section 5.2 — equal-weight mixture with orthogonal centers',{'D4':'The source explicitly identifies the data distribution with weak-signal model (9), with r=k and the stated label prior.'},kind='source_passage',symbols=[r'\operatorname{Cov}(\boldsymbol\Theta_1)=q_\Theta\boldsymbol I_k',r'\operatorname{Unif}(\{\boldsymbol e_1,\cdots,\boldsymbol e_k\})'],shape='Random center rows and uniform one-hot labels, with known component covariance equal to the identity after preprocessing. Centers are approximately orthogonal under their random-row law; exact finite-sample orthogonality is not assumed in the theorem.')
add('D23','overlap',r'''
We will measure estimation accuracy using the overlap
\[
\operatorname{Overlap}_n:=\max_{\pi\in \mathfrak S_k}\frac1n\sum_{i=1}^n\mathbb{1}\{\widehat{\boldsymbol\Lambda}_i=\boldsymbol\Lambda_i^\pi\}.
\]
Here, $\mathfrak S_k$ denotes the group of permutations over $k$ elements, and $\boldsymbol\Lambda_i^\pi$ denotes the action of this group on the cluster label encodings of the $i$-th sample. (We will work with slightly different encodings for the cases $k=2$ and $k\ge3$ below.)
''',[13],'Clustering — overlap modulo label permutations',symbols=[r'\operatorname{Overlap}_n',r'\max_{\pi\in \mathfrak S_k}'],shape='Maximum matching fraction over one global permutation of label names. Theorem 5.1 uses one-hot labels, not the signed encoding of Proposition 5.1.')
add('D24','threshold',r'''
Recall the function $\mathcal F(s,\boldsymbol Q)$ is defined in Eq. (13), where we take $\mu_\Lambda=\sum_{i=1}^k\delta_{\boldsymbol e_i}/k$. We let $\boldsymbol Q_0:=\boldsymbol1_k\boldsymbol1_k^{\mathsf T}/k^2$ and define the threshold
\[
q_\Theta^{\mathrm{info}}(k):=\inf\left\{q_\Theta\ge0:\sup_{\boldsymbol Q\in S_k^+}\mathcal F(q_\Theta^2,\boldsymbol Q)>\mathcal F(q_\Theta^2,\boldsymbol Q_0)\right\}.\tag{26}
\]
''',[14],'Information threshold — equation (26)',{'D14':'The threshold compares free energies (13) at s=q_Theta^2 for the stated uniform one-hot prior.'},symbols=[r'q_\Theta^{\mathrm{info}}(k)',r'\boldsymbol Q_0:=\boldsymbol1_k\boldsymbol1_k^{\mathsf T}/k^2'],shape='Infimum over a strict free-energy improvement over the uninformative outer-product matrix Q0. Q0 is the outer product of the prior mean, not the second-moment matrix I_k/k. The theorem makes no claim at equality to the threshold.')

add('D25','second moments',r"""
In addition, we require without loss of generality $\boldsymbol Q_\Theta=q_\Theta\boldsymbol I_r$, cf. Remark 3.1.
""",[10],'Theorem 4.3 — Theta second-moment normalization',{'D5':'Q_Theta is the uncentered second-moment matrix defined on page 7.'},kind='theorem_excerpt',context='Assume $\mu_\Lambda,\mu_\Theta$ have finite non-singular second moments',context_pages=[7],symbols=[r'\boldsymbol Q_\Theta=q_\Theta\boldsymbol I_r'],shape='The explicitly selected Theta normalization in Theorem 4.3. Keep it separate from the full Remark 3.1 conditions used in the strong-signal results and Theorem 4.2; do not add a Lambda invertibility requirement solely from this citation.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
