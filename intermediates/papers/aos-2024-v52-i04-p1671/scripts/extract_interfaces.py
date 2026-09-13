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

add('D1','Distributed Group Differential Privacy',r'''
In a distributed system, assume that the entire dataset is stored in machines $\mathcal H_1,\ldots,\mathcal H_m$. A randomized algorithm $\mathcal A:\mathcal X^N\to\Theta$ is $(\epsilon,\delta)$-distributed group differentially private ($( \epsilon,\delta)$-DGDP) if for any pair of datasets $\mathbb X\in\mathcal X^N$ and $\mathbb X'\in\mathcal X^N$, whose elements are the same except for one local machine, the following holds
\[
\mathbb P\{\mathcal A(\mathbb X)\in U\}\le e^\epsilon\cdot\mathbb P\{\mathcal A(\mathbb X')\in U\}+\delta,
\]
for every measurable subset $U\subseteq\Theta$.
''',[2],'Definition 1 (Distributed Group Differential Privacy)',context='Distributed Group Differential Privacy',
symbols=[r'\mathcal A:\mathcal X^N\to\Theta'],phrases=['distributed group differentially private'],
shape='Privacy predicate for replacement of an entire local-machine dataset; measurable output events, not record-level adjacency.')
add('D2','sign matrix',r'''
First, we formally introduce the Majority Vote procedure. Let $\boldsymbol Q_j^c$ be the sign vector obtained by the local machine $\mathcal H_j$ based on $\{\boldsymbol X_i,i\in\mathcal H_j\}$ (where $1\le j\le m$). The server then has a $p\times m$ sign matrix $\mathbb Q=(Q_{l,j})=(\boldsymbol Q_1^c,\ldots,\boldsymbol Q_m^c)$ where each $Q_{l,j}$ takes a value of $\{1,-1,0\}$, representing positive, negative and null, respectively. Here $\boldsymbol Q_j^c=(Q_{1,j},\ldots,Q_{p,j})^{\mathrm T}$ denotes each column vector received from the $j$-th local machine (where $1\le j\le m$). For each coordinate $1\le l\le p$, we consider the Majority Vote with the row vector $\boldsymbol Q_l^r=(Q_{l,1},\ldots,Q_{l,m})$.
''',[7],'Section 2.1 — sign matrix',symbols=[r'\mathbb Q=(Q_{l,j})',r'\boldsymbol Q_l^r'],shape='Ternary p by m matrix of arbitrary local signs; rows index coordinates, columns index machines. Vote counts are preserved as auxiliary definitions.')
add('D3','Majority Vote',r'''
Then $N_l^++N_l^-+N_l^0=m$ always holds, and the Majority Vote of $\boldsymbol Q_l^r$ can be equivalently computed as
\[
\operatorname{MajVote}\{\boldsymbol Q_l^r\}=
\begin{cases}
1&\text{if }N_l^+\ge N_l^0+N_l^-+1,\\
-1&\text{if }N_l^-\ge N_l^0+N_l^++1,\\
0&\text{otherwise}.
\end{cases}
\]
Let $\overline{\boldsymbol Q}$ be the resulting vector of $\mathbb Q$ by the Majority Vote, that is,
\[
\overline{\boldsymbol Q}=(\operatorname{MajVote}\{\boldsymbol Q_l^r\},1\le l\le p)^{\mathrm T}.\tag{2}
\]
''',[7],'Section 2.1 — Majority Vote (2)',{'D2':'The majority operation acts on each ternary row of the sign matrix; its three vote counts are defined in (1).'},symbols=[r'\operatorname{MajVote}\{\boldsymbol Q_l^r\}',r'\overline{\boldsymbol Q}'],shape='Strict majority for either nonzero sign; all other cases return zero, including ties. This is not plurality over three labels.')
add('D4','support',r'''
Let $\overline S$ be the support for $\overline{\boldsymbol Q}$ and $\overline s=|\overline S|$.
''',[12],'Section 2.4 — support of the majority vector',{'D3':'The support and its cardinality belong to the non-private majority vector in (2).'},symbols=[r'\overline s=|\overline S|'],shape='Support size of the realized majority vector, distinct from the population support size s used later.')
add('D5','stability level',r'''
Recall the definitions of $\{N_l^+,N_l^+,N_l^0\}$ given in (1). To solve the questions addressed at the end of the previous section, for each row $\boldsymbol Q_l^r$ where $1\le l\le p$, we define the stability level of dataset $\boldsymbol Q_l^r$ with respect to the $\operatorname{MajVote}(\cdot)$ function as the minimal number of elements in $\boldsymbol Q_l^r$ which need to be flipped to change the value of $\operatorname{MajVote}\{\boldsymbol Q_l^r\}$. This can also be explicitly computed as:
\[
f^S(\boldsymbol Q_l^r)=
\begin{cases}
N_l^+-N_l^0-N_l^-&\text{if }\operatorname{MajVote}\{\boldsymbol Q_l^r\}=1,\\
N_l^--N_l^0-N_l^+&\text{if }\operatorname{MajVote}\{\boldsymbol Q_l^r\}=-1,\\
-\min\{N_l^++N_l^0-N_l^-,N_l^-+N_l^0-N_l^+\}&\text{if }\operatorname{MajVote}\{\boldsymbol Q_l^r\}=0.
\end{cases}\tag{4}
\]
Note that we assign the stability $f^S(\boldsymbol Q_l^r)$ with a minus sign for $\operatorname{MajVote}\{\boldsymbol Q_l^r\}=0$ because we only want to select the nonzero elements.
''',[10],'Section 2.3 — stability level (4)',{'D3':'The score branches according to the majority result and uses the corresponding vote margins.'},symbols=[r'f^S(\boldsymbol Q_l^r)'],shape='Signed peeling score exactly as printed. Its null branch is nonpositive, and its formula is not literally the minimal integer number of coordinate flips described in the prose.')
add('D6','utility function',r'''
\[
\begin{cases}
f_l(\boldsymbol Q_l^r,1)=N_l^+-N_l^0-N_l^-,\\
f_l(\boldsymbol Q_l^r,-1)=N_l^--N_l^0-N_l^+,\\
f_l(\boldsymbol Q_l^r,0)=\min\{N_l^++N_l^0-N_l^-,N_l^-+N_l^0-N_l^+\}.
\end{cases}\tag{5}
\]
''',[11],'Section 2.3 — utility function (5)',{'D2':'Each utility value is calculated from the positive, negative and null counts of row l, defined in (1).'},context='utility function:',symbols=[r'f_l(\boldsymbol Q_l^r,0)',r'f_l(\boldsymbol Q_l^r,1)'],shape='Three utilities for the exponential sign draw. The null utility has the opposite sign from the null branch of the peeling score; Theorem 2 uses this utility evaluated at the majority sign.')
add('D7','Laplace distribution',r'''
Here, $\operatorname{Lap}(b)$ denotes the Laplace distribution with the density function $\frac1{2b}\exp(-|x|/b)$ for $x\in(-\infty,\infty)$, and the scale parameter $b>0$.
''',[8],'Section 2.2 — Laplace distribution',symbols=[r'\operatorname{Lap}(b)'],shape='Centered real Laplace distribution with positive scale; the density is a definition, while the adjacent privacy lemma is not a theorem-inventory item or statement dependency.')
add('D8','Peeling',r'''
Input: The set of signs $\mathbb Q=\{\boldsymbol Q_1^c,...,\boldsymbol Q_m^c\}$; the number of selections $\widetilde s$; privacy level $(\epsilon,\delta)$; initial $\widetilde S=\varnothing$.

1: for $1\le l\le p$ do

2: Compute the stability level $f^S(\boldsymbol Q_l^r)$ based on (4).

3: end for

4: for $1\le t\le\widetilde s$ do

5: Generate $g_{t,1},\ldots,g_{t,p}\sim\operatorname{Lap}(4\sqrt{2\widetilde s\log(1/\delta)}/\epsilon)$;

6: Add $l^*=\operatorname{argmax}_{l\in[p]\setminus\widetilde S}f^S(\boldsymbol Q_l^r)+g_{t,l}$ to $\widetilde S$.

7: end for

Output: Return the sets $\widetilde S$.
''',[10],'Algorithm 1 — Peeling',{'D2':'Algorithm 1 takes the local ternary sign columns as its input.','D5':'Its selection score is the signed stability level (4).','D7':'At every selection step it draws the stated Laplace noise.'},context='Peeling',symbols=[r'g_{t,1}',r'f^S(\boldsymbol Q_l^r)'],shape='Sequential selection without replacement. Each round uses noise scale 4 sqrt(2 s_tilde log(1/delta))/epsilon. Independence and tie handling are implicit implementation conventions, not added original text.')
add('D9','Differentially Private Majority Vote for Sign Recovery',r'''
Input: The set of signs $\mathbb Q=\{\boldsymbol Q_1^c,...,\boldsymbol Q_m^c\}$; the number of selections $\widetilde s$; privacy level $(\epsilon,\delta)$.

1: Apply $\operatorname{Peeling}(\mathbb Q,\widetilde s,\epsilon/2,\delta/2)$ to select the index set $\widetilde S=\{l_1,l_2,\ldots,l_{\widetilde s}\}$.

2: for $l\in\widetilde S$ do

3: Compute the quantities $f_l(\boldsymbol Q_l^r,1)$, $f_l(\boldsymbol Q_l^r,-1)$, $f_l(\boldsymbol Q_l^r,0)$ based on (5).

4: Generate the random sign $\widehat Q_l$ according to the following distribution
\[
\begin{cases}
\mathbb P(\widehat Q_l=1)=\frac{P_l^+}{P_l^++P_l^-+P_l^0},\\
\mathbb P(\widehat Q_l=0)=\frac{P_l^0}{P_l^++P_l^-+P_l^0},\\
\mathbb P(\widehat Q_l=-1)=\frac{P_l^-}{P_l^++P_l^-+P_l^0},
\end{cases}
\quad\text{where}\quad
\begin{cases}
P_l^+=\exp\{\epsilon'f_l(\boldsymbol Q_l^r,1)/4\},\\
P_l^0=\exp\{\epsilon'f_l(\boldsymbol Q_l^r,0)/4\},\\
P_l^-=\exp\{\epsilon'f_l(\boldsymbol Q_l^r,-1)/4\}.
\end{cases}
\]
and $\epsilon'=\epsilon/(4\sqrt{2\widetilde s\log(2/\delta)})$.

5: end for

Output: Return the sets $\widehat S=\{l|l\in\widetilde S,\widehat Q_l\ne0\}$ and $\widehat{\boldsymbol Q}=\{\widehat Q_l|l\in\widehat S\}$.
''',[11],'Algorithm 2 — Differentially Private Majority Vote for Sign Recovery',{'D2':'DPVote receives the matrix of local ternary signs.','D8':'It first runs Peeling with half of both privacy parameters.','D6':'The sign probabilities use the three utilities in (5), with the printed epsilon-prime and divisor four.'},context='Differentially Private Majority Vote for Sign Recovery',symbols=[r'\operatorname{Peeling}(\mathbb Q,\widetilde s,\epsilon/2,\delta/2)',r'\epsilon/(4\sqrt{2\widetilde s\log(2/\delta)})'],shape='Randomized sparse output from Algorithm 2. Preserve its pair/set output notation; identifying it with a full p-vector requires the implicit zero extension and coordinate indexing recorded separately.')
add('D10','quantization function',r'''
To present our method more clearly, we define the quantization function $\mathcal Q_\lambda(\cdot)$ as follows:
\[
\mathcal Q_\lambda(x)=\operatorname{sgn}\{\underbrace{\operatorname{sgn}(x)\cdot(|x|-\lambda)_+}_{\text{shrinkage operator}}\}=
\begin{cases}
\operatorname{sgn}(x)&\text{if }|x|>\lambda,\\
0&\text{if }|x|\le\lambda.
\end{cases}\tag{7}
\]
Here $\lambda$ is the threshold parameter. When $x$ is a vector, $\mathcal Q_\lambda(x)$ performs the aforementioned operation in a coordinated manner. In particular, when $\lambda=0$, the function $\mathcal Q_0(\cdot)$ is the same as sign function $\operatorname{sgn}(\cdot)$.
''',[13],'Section 3.1 — quantization function (7)',symbols=[r'\mathcal Q_\lambda(x)'],shape='Coordinatewise ternary thresholding, with equality to the threshold mapped to zero. The positive-part identity is interpreted for nonnegative threshold.')
add('D11','Differentially private Majority Vote (DPVote) for sparse mean',r'''
Input: Dataset $\mathbb X=\{\boldsymbol X_1,\ldots,\boldsymbol X_N\}$ stored in $m$ local machines (where $j=1,\ldots,m$), the universal thresholding parameter $\lambda_N$, number of selections $\widetilde s$, privacy level $(\epsilon,\delta)$.

1: for $j=1,\ldots,m$ do

2: Compute the local sample mean $\overline{\boldsymbol X}_j=n_j^{-1}\sum_{i\in\mathcal H_j}\boldsymbol X_i$ on the $j$-th machine and obtain the sign vector $\boldsymbol Q_j=\mathcal Q_{\lambda_N}(\overline{\boldsymbol X}_j)$. Send $\boldsymbol Q_j$ to the server.

3: end for

4: Apply DPVote
\[
\widehat{\boldsymbol Q}(\mathbb X)=\operatorname{DPVote}(\{\boldsymbol Q_j\}_{1\le j\le m},\widetilde s,\epsilon,\delta).\tag{8}
\]

Output: The sign vector $\widehat{\boldsymbol Q}(\mathbb X)$.
''',[13],'Algorithm 3 — Differentially private Majority Vote (DPVote) for sparse mean',{'D10':'Each local sample mean is converted to signs by quantization at lambda_N.','D9':'The server applies the Algorithm 2 DPVote mechanism to those local signs.'},context='Differentially private Majority Vote (DPVote) for sparse mean.',symbols=[r'\mathcal Q_{\lambda_N}(\overline{\boldsymbol X}_j)'],shape='Distributed sample-mean sign estimator, preserving unequal n_j and the shared threshold. Original Algorithm 2 sparse-output versus full-vector convention remains explicit.')
add('D12','distribution space',r'''
To discuss the theoretical properties of our method, we introduce the distribution space $\mathcal P$ for the population $\boldsymbol X$:
\[
\mathcal P(\boldsymbol\theta^*,C)=\left\{\mathbb P\left|\mathbb E_{\mathbb P}[\boldsymbol X]=\boldsymbol\theta^*,\max_{1\le l\le p}\mathbb E_{\mathbb P}[|X_l-\theta_l^*|^3]\le C\right.\right\},\tag{10}
\]
where $C>0$ is a constant.
''',[15],'Section 3.2 — distribution space for the mean vector (10)',symbols=[r'\mathcal P(\boldsymbol\theta^*,C)'],shape='Probability laws with prescribed mean and uniformly bounded coordinatewise third absolute centered moments. Coordinate independence and a variance lower bound are not imposed in this passage.')
add('D13','local estimator',r'''
Let
\[
\widehat{\boldsymbol\theta}_j(\lambda)=\operatorname{argmin}_{\boldsymbol\theta\in\mathbb R^p}\frac1{2n_j}\sum_{i\in\mathcal H_j}(Y_i-\boldsymbol X_i^{\mathrm T}\boldsymbol\theta)^2+\lambda|\boldsymbol\theta|_1.\tag{14}
\]
''',[16],'Section 4.1 — local estimator (14)',context=r'In particular, we let $\lambda_j$ be the smallest number such that the local estimator $\widehat{\boldsymbol\theta}_j(\lambda_j)$ having at most $\widetilde s$ nonzero elements and no less than a universal constant $\lambda_N$ in (18).',
symbols=[r'\widehat{\boldsymbol\theta}_j(\lambda)'],shape='Lasso objective with factor 1/(2 n_j). A measurable choice of minimizer is implicit; uniqueness is not guaranteed by the displayed definition.')
add('D14','regularization parameter',r'''
We need to choose a problem-specific regularization parameter $\lambda_j$ for each local machine. In particular, we let $\lambda_j$ be the smallest number such that the local estimator $\widehat{\boldsymbol\theta}_j(\lambda_j)$ having at most $\widetilde s$ nonzero elements and no less than a universal constant $\lambda_N$ in (18). More precisely, we let
\[
\lambda_j=\min\left\{\lambda\left|\,|\widehat{\boldsymbol\theta}_j(\lambda)|_0\le\widetilde s,\ \lambda\ge\lambda_N\right.\right\}.\tag{15}
\]
''',[16],'Section 4.1 — local regularization parameter (15)',{'D13':'The parameter is selected using the support size of the local Lasso minimizer in (14).'},symbols=[r'\lambda_j=\min'],shape='Data-dependent smallest penalty meeting the support cap and universal lower bound. The lower bound lambda_N is supplied by the theorem, not a recursive dependency on Algorithm 4. Nonempty feasible set alone does not prove attainment of this minimum.')
add('D15','Differentially private Majority Vote for sparse linear regression',r'''
Input: Data on local machines $\{(\boldsymbol X_i,Y_i)|i\in\mathcal H_j\}$ for $j=1,\ldots,m$, the universal regularization parameter $\lambda_N$ in (18) and $\lambda_j$ in (15), privacy level $(\epsilon,\delta)$.

1: for $j=1,\ldots,m$ do

2: Let $\widehat{\boldsymbol\theta}_j=\widehat{\boldsymbol\theta}_j(\lambda_j)$ in (14), and obtain the sign vector $\boldsymbol Q_j=\operatorname{sgn}(\widehat{\boldsymbol\theta}_j)$. Send $\boldsymbol Q_j$ to the server.

3: end for

4: Apply DPVote
\[
\widehat{\boldsymbol Q}(\mathbb X)=\operatorname{DPVote}(\{\boldsymbol Q_j\}_{1\le j\le m},\widetilde s,\epsilon,\delta).\tag{16}
\]

Output: The sign vector $\widehat{\boldsymbol Q}(\mathbb X)$.
''',[17],'Algorithm 4 — Differentially private Majority Vote for sparse linear regression (DPVote Lasso)',{'D13':'Local signs are signs of the Lasso minimizer in (14).','D14':'Each local penalty is chosen by the data-dependent rule (15).','D9':'The server uses the same Algorithm 2 DPVote mechanism on these signs.'},context='Differentially private Majority Vote for sparse linear regression (DPVote Lasso)',symbols=[r'\operatorname{sgn}(\widehat{\boldsymbol\theta}_j)'],shape='Model-specific Lasso sign wrapper. The selection count is consumed in (16) although not listed in the printed input line. No privacy property is inferred as a theorem-statement dependency from the algorithm name.')
add('D16','distribution space',r'''
For linear regression, we consider the following distribution space
\[
\mathcal P_{X,Y}(\boldsymbol\theta^*,\rho,\eta_1,C_1,\eta_2,C_2)=
\left\{\mathbb P\ \middle|\ \begin{aligned}
&\rho\le\Lambda_{\min}(\boldsymbol\Sigma)\le\Lambda_{\max}(\boldsymbol\Sigma)\le\rho^{-1},\\
&\sup_{|\boldsymbol v|_2=1}\mathbb E_{\mathbb P}\{\exp(\eta_1|\boldsymbol v^{\mathrm T}\boldsymbol X|^2)\}\le C_1,\\
&z=Y-\boldsymbol X^{\mathrm T}\boldsymbol\theta^*,\ z\perp\boldsymbol X,\ \mathbb E_{\mathbb P}\{\exp(\eta_2|z|^2)\}\le C_2
\end{aligned}\right\},\tag{17}
\]
where $\rho,C_1,C_2,\eta_1,\eta_2$ are positive constants.
''',[17],'Section 4.2 — distribution space for linear regression (17)',symbols=[r'\mathcal P_{X,Y}(\boldsymbol\theta^*,\rho,\eta_1,C_1,\eta_2,C_2)'],shape='Joint law with spectral bounds and uniform exponential square moments of projections and independent residual. Sigma is defined in Theorem 4(c) as the uncentered second moment; no zero-mean assumption is silently added.')

for lid,term,label,context in [
    ('D12','Mean Vector','Mean vector','Theory of Mean Vector Sign Selection'),
    ('D16','linear regression','Linear regression',None)]:
    x=next(x for x in interfaces if x['members'][0]['local_id']==lid)
    keyword=dict(paper_id=PID,local_id=lid,source_text=term,label=label,kind='term')
    if context:
        cid=lid+'/model-name'
        members[lid].setdefault('naming_context',[]).append(dict(context_id=cid,text=context,evidence=members[lid]['evidence']))
        keyword['context_id']=cid
    x['source_keywords'].append(keyword)
    x['name']=' · '.join(k['label'] for k in x['source_keywords'])

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source interfaces; full source audit pending.')
if __name__=='__main__':main()
