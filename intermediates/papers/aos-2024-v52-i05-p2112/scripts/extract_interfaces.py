"""Preserve original main-text source entries for the four-Theorem census."""
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
add(1,'unit complex numbers',r'''Let $z_1^*,\ldots,z_n^*\in\mathbb C_1$ where $\mathbb C_1:=\{x\in\mathbb C:|z|=1\}$, the set of all unit complex numbers. Then each $z_j^*$ can be written equivalently as $e^{i\theta_j^*}$ for some phase (or angle) $\theta_j^*\in[0,2\pi)$.''',[1],[],[r'\mathbb C_1'],'Original unit-circle convention. The source binds x but writes |z|=1; preserve this typographical mismatch and use the accompanying unit-complex-number description to explain its role.','Section 1 — Unit complex numbers')
add(2,'phase synchronization problem',r'''For each $1\leq j<k\leq n$, the observation $X_{jk}\in\mathbb C$ is missing at random. Let $A_{jk}\in\{0,1\}$ and $X_{jk}$ satisfy
\[
X_{jk}:=\begin{cases}z_j^*\overline{z_k^*}+\sigma W_{jk},&\text{if }A_{jk}=1,\\0,&\text{if }A_{jk}=0,\end{cases}
\]
(1)
where $A_{jk}\sim\operatorname{Bernoulli}(p)$ and $W_{jk}\sim\mathcal{CN}(0,1)$. That is, each $X_{jk}$ is missing with probability $1-p$ and is denoted as $0$. If it is not missing, it is equal to $z_j^*\overline{z_k^*}$ with an additive noise $\sigma W_{jk}$ where $W_{jk}$ follows the standard complex Gaussian distribution: $\operatorname{Re}(W_{jk}),\operatorname{Im}(W_{jk})\sim\mathcal N(0,1/2)$ independently. Each $A_{jk}$ is the indicator of whether $X_{jk}$ is observed or not. We assume all random variables $\{A_{jk}\}_{1\leq j<k\leq n}$, $\{W_{j,k}\}_{1\leq j<k\leq n}$ are independent of each other. The goal is to estimate the phase vector $z^*:=(z_1^*,\ldots,z_n^*)\in\mathbb C_1^n$ from $\{A_{jk}\}_{1\leq j<k\leq n}$ and $\{X_{jk}\}_{1\leq j<k\leq n}$.''',[1],[1],[r'z_j^*\overline{z_k^*}',r'\mathcal N(0,1/2)',r'A_{jk}'],'Masked complex observations with independent upper-triangle Bernoulli masks and circular complex noise. The Hermitian completion and zero diagonal are retained in A1. Conjugation is essential; lower-triangle noises are not independent additional draws.','Section 1 — Phase model (1)',kind='source_passage',context='We consider the phase synchronization problem with additive Gaussian noises and incomplete data [2, 5, 39, 18].')
add(3,'spectral estimator',r'''Let $u\in\mathbb C^n$ be the leading eigenvector of $X$. Then the spectral estimator $\widehat z\in\mathbb C_1^n$ is defined as
\[
\widehat z_j:=\begin{cases}\dfrac{u_j}{|u_j|},&\text{if }u_j\ne0,\\1,&\text{if }u_j=0,\end{cases}
\]
(4)
for each $j\in[n]$, where each $u_j$ is normalized so that $\widehat z_j\in\mathbb C_1$.''',[2],[1,2],[r'\widehat z_j',r'\dfrac{u_j}{|u_j|}',r'u_j=0'],'Leading data-matrix eigenvector followed by coordinatewise phase normalization. Retain the explicit value 1 on a zero coordinate; no population-eigenvector approximation is required to define this estimator.','Section 1 — Spectral estimator (4)')
add(4,'loss',r'''The performance of the spectral estimator can be quantified by a normalized squared $\ell_2$ loss
\[
\ell(\widehat z,z^*):=\min_{a\in\mathbb C_1}\frac1n\sum_{j=1}^n|\widehat z_j-z_j^*a|^2,
\]
(5)
where the minimum over $\mathbb C_1$ is due to the fact that $z_1^*,\ldots,z_n^*$ are identifiable only up to a phase.''',[2],[1],[r'\ell(\widehat z,z^*)',r'\min_{a\in\mathbb C_1}',r'\sum_{j=1}^n'],'Average squared phase loss minimized over one global unit-complex alignment, not a separate phase for each coordinate. The arguments are bound inputs, so computing the estimator is not part of the loss definition.','Section 1 — Loss (5)')
add(5,'orthogonal matrices',r'''Let $d>0$ be an integer. Define
\[
O(d):=\{U\in\mathbb R^{d\times d}:UU^T=U^TU=I_d\}
\]
(11)
to include all orthogonal matrices in $\mathbb R^{d\times d}$.''',[4],[],[r'O(d)',r'UU^T=U^TU=I_d'],'Real orthogonal group including both determinant signs. Theorems 2 and 4 further restrict d; the definition itself is for any positive integer d.','Section 1 — Orthogonal group (11)')
add(6,'orthogonal group synchronization',r'''Let $d>0$ be an integer. Recall the definition of $O(d)$ in (11) and that $Z_1^*,\ldots,Z_n^*\in O(d)$. For each $1\leq j<k\leq n$, the observation $\mathcal X_{jk}\in\mathbb R^{d\times d}$ is given by
\[
\mathcal X_{jk}:=\begin{cases}Z_j^*Z_k^{*T}+\sigma\mathcal W_{jk},&\text{if }A_{jk}=1,\\0,&\text{if }A_{jk}=0,\end{cases}
\]
(20)
where $A_{jk}\sim\operatorname{Bernoulli}(p)$ and $\mathcal W_{jk}\sim\mathcal{MN}(0,I_d,I_d)$, i.e., the standard matrix Gaussian distribution. We assume $\{A_{jk}\}_{1\leq j<k\leq n}$, $\{\mathcal W_{j,k}\}_{1\leq j<k\leq n}$ are all independent of each other. Similar to the phase synchronization problem, the observations are missing at random with additive Gaussian noises. The goal is to recover $Z_1^*,\ldots,Z_n^*$ from $\{\mathcal X_{jk}\}_{1\leq j<k\leq n}$ and $\{A_{j,k}\}_{1\leq j<k\leq n}$.''',[10],[5],[r'Z_j^*Z_k^{*T}',r'\mathcal{MN}(0,I_d,I_d)'],'Real matrix observations with independent upper-triangle masks and matrix-normal noise. Transpose completion, zero blocks and the block-masked matrix formula are retained in A2; the matrix-Gaussian density convention is A3.','Section 3 — Orthogonal model (20)',kind='source_passage',context='This is known as the orthogonal group synchronization (or $O(d)$ synchronization).',context_page=4)
add(7,'polar decomposition',r'''The mapping $\mathcal P:\mathbb R^{d\times d}\to O(d)$ is from the polar decomposition and is defined as follows. For any matrix $B\in\mathbb R^{d\times d}$ that is full-rank, it admits a singular value decomposition (SVD): $B=MDV^T$ with $M,V\in O(d)$ and $D$ a diagonal matrix. Then its polar decomposition is $B=(MV^T)(VDV^T)$ and $\mathcal P(B):=MV^T$ is defined as its first factor.''',[10],[5],[r'\mathcal P(B):=MV^T',r'B=(MV^T)(VDV^T)'],'Orthogonal polar factor on full-rank square matrices. Although the displayed map domain is all square matrices, the definition supplies this case only; the estimator separately assigns the identity on singular blocks.','Section 3 — Polar factor')
add(8,'spectral estimator',r'''Let $\lambda_1\geq\ldots\geq\lambda_d$ be the largest $d$ eigenvalues of $\mathcal X$ and $u_1,\ldots,u_d\in\mathbb R^{nd}$ be their corresponding eigenvectors. Denote $U:=(u_1,\ldots,u_d)\in\mathbb R^{nd\times d}$ as the eigenspace that includes the top $d$ eigenvectors of $\mathcal X$. For each $j\in[n]$, denote $U_j\in\mathbb R^{d\times d}$ as its $j$th submatrix. Then the spectral estimator $\widehat Z_j\in O(d)$ is defined as
\[
\widehat Z_j:=\begin{cases}\mathcal P(U_j),&\text{if }\det(U_j)\ne0,\\I_d,&\text{if }\det(U_j)=0,\end{cases}
\]
(13)
for each $j\in[n]$.''',[4],[5,6,7],[r'\widehat Z_j',r'\mathcal P(U_j)',r'\det(U_j)=0'],'Top-d eigenspace represented by its eigenvector columns, followed by block polar normalization with explicit identity fallback for singular blocks. The source does not print an eigenspace tie-selection rule; first-order approximations are proof objects, not estimator inputs.','Section 1 — Orthogonal spectral estimator (13)')
add(9,'loss function',r'''The loss function is defined analogously to (5) as
\[
\ell^{od}(\widehat Z,Z^*):=\min_{O\in O(d)}\frac1n\|\widehat Z_j-Z_j^*O\|_F^2.
\]''',[11],[5],[r'\ell^{od}(\widehat Z,Z^*)',r'\widehat Z_j-Z_j^*O'],'Original printed orthogonal loss. It contains a free block index j and no sum, despite being described as analogous to (5). Preserve this ambiguity; do not silently add a sum or replace the blocks by stacked matrices.','Section 3 — Orthogonal loss')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
