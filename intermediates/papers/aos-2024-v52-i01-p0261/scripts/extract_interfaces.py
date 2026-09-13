"""Transcribe statement prerequisites from the inspected published PDF, without supplements."""
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
        lean_role='hypothesis' if kind=='condition' else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}

add('D1','Fourier coefficients',r'''
The mean value of $f$ over the circle is invariant to rotations, and is easily estimated by averaging across samples. Thus, let us assume for simplicity and without loss of generality that $f$ has known mean 0. Passing to the Fourier domain, we assume that $f$ is bandlimited to $K$ Fourier frequencies, that is, $f$ admits the Fourier sequence representation
\[
f(t)=\sum_{k=1}^K\theta_{k,1}f_{k,1}(t)+\theta_{k,2}f_{k,2}(t),\quad f_{k,1}(t)=\frac1{\sqrt\pi}\cos kt,\ f_{k,2}(t)=\frac1{\sqrt\pi}\sin kt,
\]
where $\{f_{k,1},f_{k,2}:k=1,\ldots,K\}$ are orthonormal Fourier basis functions over $[-\pi,\pi)$, and
\[
\theta=(\theta_{1,1},\theta_{1,2},\ldots,\theta_{K,1},\theta_{K,2})\in\mathbb R^{2K}
\]
are the Fourier coefficients of $f$. We assume implicitly throughout the paper that $K\geq2$, and we are interested in applications with potentially large values of this bandlimit $K$.
''',[5],'Section 2 — Fourier coefficients and bandlimit',phrases=['Fourier coefficients'],shape='Mean-zero real bandlimited signal represented by 2K real coefficients in the printed orthonormal trigonometric basis; K>=2 throughout.')
add('D2','Fourier magnitudes and phases',r'''
Importantly, due to the choice of Fourier basis, the $2K$-dimensional space of such bandlimited functions is closed under rotations of the circle. The rotation $f\mapsto f_\alpha$ induces a map from the Fourier coefficients of $f$ to those of $f_\alpha$, which we denote as $\theta\mapsto g(\alpha)\cdot\theta$ for an orthogonal matrix $g(\alpha)\in\mathbb R^{2K\times2K}$. Explicitly, this map $\theta\mapsto g(\alpha)\cdot\theta$ is given separately for each Fourier frequency $k=1,\ldots,K$ by
\[
\begin{pmatrix}\theta_{k,1}\\\theta_{k,2}\end{pmatrix}\mapsto\begin{pmatrix}\cos k\alpha&-\sin k\alpha\\\sin k\alpha&\cos k\alpha\end{pmatrix}\begin{pmatrix}\theta_{k,1}\\\theta_{k,2}\end{pmatrix},\tag{3}
\]
and $g(\alpha)$ is the block-diagonal matrix with these $2\times2$ blocks. Equivalently, writing
\[
(\theta_{k,1},\theta_{k,2})=(r_k\cos\phi_k,r_k\sin\phi_k),
\]
where $r_k>0$ is the magnitude and $\phi_k\in\mathcal A$ is the phase (identified modulo $2\pi$), this map is given for each $k=1,\ldots,K$ by
\[
(r_k,\phi_k)\mapsto(r_k,\phi_k+k\alpha).\tag{4}
\]
''',[5],'Section 2 — rotations, Fourier magnitudes and phases, equations (3)-(4)',{'D1':'The block rotation acts on the real Fourier coefficient pairs.'},context='We may express and bound the loss (6) in terms of the Fourier magnitudes and phases.',symbols=[r'r_k',r'g(\alpha)'],shape='Source polar representation and block-diagonal rotation action; r_k>0 is printed for the polar coordinates, and phases are modulo 2pi.')
members['D2']['naming_context'][0]['evidence']=[dict(page=6,location='Section 3.1, sentence preceding Proposition 3.1')]
add('D3','Fourier sequence space',r'''
The samples $f_\alpha(t)\,\mathrm dt+\sigma\,\mathrm dW(t)$ represented in this Fourier sequence space take the form
\[
y^{(m)}=g(\alpha^{(m)})\cdot\theta+\sigma\varepsilon^{(m)}\in\mathbb R^{2K}\quad\text{for }m=1,\ldots,N,\tag{5}
\]
where $\alpha^{(1)},\ldots,\alpha^{(N)}\overset{\mathrm{i.i.d.}}{\sim}\operatorname{Unif}([-\pi,\pi))$, $\varepsilon^{(1)},\ldots,\varepsilon^{(N)}\overset{\mathrm{i.i.d.}}{\sim}\mathcal N(0,I_{2K})$, and these are independent.
''',[5],'Section 2 — observation model in Fourier sequence space, equation (5)',{'D1':'Each observed vector has 2K Fourier coefficients.','D2':'The signal mean is rotated by the block action g(alpha).'},kind='source_passage',phrases=['Fourier sequence space'],symbols=[r'y^{(m)}'],shape='N independent Gaussian observations with independent latent uniform rotations and fixed known sigma>0, as specified by the surrounding Section 2 convention.')
add('D4','loss',r'''
Writing $\widehat\theta\in\mathbb R^{2K}$ for the Fourier coefficients of the estimated function $\widehat f$ (which should likewise be bandlimited to $K$ Fourier frequencies), the loss (1) is equivalent to
\[
L(\widehat\theta,\theta)=\min_{\alpha\in\mathcal A}\|\widehat\theta-g(\alpha)\cdot\theta\|^2.\tag{6}
\]
''',[5],'Section 2 — rotation-invariant loss, equation (6)',{'D1':'Both estimated and true coefficients are in the same bandlimited coefficient space.','D2':'The loss minimizes over the circular rotation action.'},phrases=['loss'],symbols=[r'L(\widehat\theta,\theta)'],shape='Squared Euclidean error minimized over one shared rotation alpha across all frequencies; not independent phase alignment per coordinate.')
add('D5','power law decay rate',r'''
In the remainder of this paper, we will consider the problem in this sequence form. We reserve the notation $\theta^*$ for the Fourier coefficients of the true unknown function. Fixing constants $\beta\in[0,\frac12)$ and $\underline c,\overline c>0$, we consider a parameter space of “generic” Fourier coefficient vectors with power law decay rate $\beta$, given by
\[
\Theta_\beta=\{\theta^*\in\mathbb R^{2K}:\underline c k^{-\beta}\leq r_k(\theta^*)\leq\overline c k^{-\beta}\text{ for all }k=1,\ldots,K\}.\tag{7}
\]
Here, “generic” refers to the quantitative lower bound for each value $r_k(\theta^*)$ that matches the assumed upper bound up to a constant factor.
''',[5],'Section 2 — generic Fourier coefficient class, equation (7)',{'D1':'The parameter is the true 2K-dimensional Fourier coefficient vector.','D2':'The two-sided decay bounds restrict every Fourier magnitude.'},phrases=['power law decay rate'],symbols=[r'\Theta_\beta'],shape='Two-sided per-frequency power-law magnitude class with fixed positive constants and beta in [0,1/2); preserve the lower bound and unrestricted phases.')
add('D6','estimators',r'''
In both statements, $\mathbb E_{\theta^*}$ is the expectation over $N$ samples $y^{(1)},\ldots,y^{(N)}$ from the model (5) with true parameter $\theta^*$. The infimum $\inf_{\widehat\theta}$ is over all estimators $\widehat\theta$ based on these samples, and $\asymp$ denotes upper and lower bounds up to constant multiplicative factors that depend only on $\beta$, $\underline c$, $\overline c$, $c_0$.
''',[6],'Conventions following Theorems 2.1 and 2.2',{'D3':'The estimator and expectation use the N-sample observation law (5).'},kind='source_passage',phrases=['estimators'],symbols=[r'\mathbb E_{\theta^*}'],shape='Minimax estimator class and uniformity of comparison constants for Theorems 2.1-2.2. Do not replace all estimators by either constructive upper-bound procedure.')
add('D7','Complex representation',r'''
It will be notationally and conceptually convenient to pass between $\theta\in\mathbb R^{2K}$ and a complex representation by $\widetilde\theta\in\mathbb C^K$. We use throughout
\[
\operatorname{Arg}z\in[-\pi,\pi)\tag{11}
\]
for the principal complex argument of $z\in\mathbb C$. Recalling the $k$th Fourier coefficient pair $(\theta_{k,1},\theta_{k,2})=(r_k\cos\phi_k,r_k\sin\phi_k)$, we set
\[
\widetilde\theta_k=\theta_{k,1}+i\theta_{k,2}=r_ke^{i\phi_k}\in\mathbb C.\tag{12}
\]
For $\theta,\theta'\in\mathbb R^{2K}$, note that
\[
\langle\theta,\theta'\rangle=\sum_{k=1}^K\theta_{k,1}\theta'_{k,1}+\theta_{k,2}\theta'_{k,2}=\sum_{k=1}^K\operatorname{Re}\widetilde\theta_k\overline{\widetilde\theta'_k}=\frac{\langle\widetilde\theta,\widetilde\theta'\rangle+\langle\widetilde\theta',\widetilde\theta\rangle}{2},\tag{13}
\]
where the left-hand side is the real inner product and the right-hand side is the complex inner product $\langle u,v\rangle=\sum_k u_k\overline{v_k}$.

Similarly, we may represent the sample $y^{(m)}\in\mathbb R^{2K}$ from (5) by $\widetilde y^{(m)}\in\mathbb C^K$ where
\[
\widetilde y_k^{(m)}=y_{k,1}^{(m)}+iy_{k,2}^{(m)}\in\mathbb C.
\]
Then, recalling the form of rotational action (4), we have
\[
\widetilde y_k^{(m)}=r_ke^{i(\phi_k+k\alpha^{(m)})}+\sigma\widetilde\varepsilon_k^{(m)}\in\mathbb C,\tag{14}
\]
where $\widetilde\varepsilon_k^{(m)}=\varepsilon_{k,1}^{(m)}+i\varepsilon_{k,2}^{(m)}\sim\mathcal N_{\mathbb C}(0,2)$ is complex Gaussian noise, independent across both frequencies $k=1,\ldots,K$ and samples $m=1,\ldots,N$.
''',[7],'Section 3.2 — Complex representation',{'D2':'Complex coordinates use the Fourier magnitude/phase and rotation formula.','D3':'The complex samples are formed from the real observation law.'},context='Complex representation.',symbols=[r'\widetilde y_k^{(m)}',r'\operatorname{Arg}z'],shape='Real-to-complex representation with principal arguments in [-pi,pi) and complex noise variance 2; real and imaginary components each have variance one.')
add('D8','circular distance',r'''
For $\phi,\phi'\in\mathcal A=[-\pi,\pi)$, we define the circular distance
\[
|\phi-\phi'|_{\mathcal A}=\min_{j\in\mathbb Z}|\phi-\phi'+2\pi j|.\tag{8}
\]
''',[6],'Section 3.1 — circular distance, equation (8)',phrases=['circular distance'],symbols=[r'\mathcal A=[-\pi,\pi)'],shape='Distance modulo 2pi. The optimization pilot uses this circular discrepancy, whereas the final phase least squares uses real arithmetic.')
add('D9','method-of-moments procedures',r'''
This motivates the following class of method-of-moments procedures:

1. For each $k=1,\ldots,K$, estimate $r_k$ by
\[
\widehat r_k=\left(\frac1N\sum_{m=1}^N|\widetilde y_k^{(m)}|^2-2\sigma^2\right)_+^{1/2}.\tag{16}
\]
2. For each $(k,l)\in\mathcal I$, compute
\[
\widehat B_{k,l}=\frac1N\sum_{m=1}^N\widetilde y_{k+l}^{(m)}\cdot\overline{\widetilde y_k^{(m)}}\cdot\overline{\widetilde y_l^{(m)}},\tag{17}
\]
and choose a version of its complex argument $\widehat\Phi_{k,l}$ in $\mathbb R$ such that $\widehat\Phi_{k,l}-\operatorname{Arg}\widehat B_{k,l}=0\mod 2\pi$.

3. Estimate $\phi=(\phi_k:k=1,\ldots,K)$ by the least-squares estimator
\[
\widehat\phi=\arg\min_{\phi\in\mathbb R^K}\sum_{(k,l)\in\mathcal I}\big(\widehat\Phi_{k,l}-(\phi_{k+l}-\phi_k-\phi_l)\big)^2.\tag{18}
\]
Then estimate $\theta$ by $\widehat\theta=(\widehat r_k\cos\widehat\phi_k,\widehat r_k\sin\widehat\phi_k)_{k=1}^K$.

Here, (18) is defined using the squared difference over $\mathbb R$ rather than over the periodic domain $\mathcal A$. Hence, the final estimate $\widehat\theta$ depends on the specific choice of argument $\widehat\Phi_{k,l}$ in Step 2, which we have left ambiguous above.
''',[8],'Section 4 — method-of-moments procedures, equations (16)-(18)',{'D7':'The empirical magnitude and bispectrum use complex observations and their principal arguments.','D2':'The fitted magnitudes and phases reconstruct the real Fourier coefficient pairs.'},phrases=['method-of-moments procedures'],symbols=[r'\widehat B_{k,l}',r'\widehat\phi'],shape='Full three-step procedure with unspecified argument lift supplied by a separate oracle or optimization rule. Index set I={(k,l):1<=k,l<=K,k+l<=K} is retained as a local auxiliary.')
add('D10','oracle procedure',r'''
Let us identify each entry of the true Fourier phase vector as a real value $\phi_k\in[-\pi,\pi)$, and set
\[
\Phi_{k,l}=\phi_{k+l}-\phi_k-\phi_l\in\mathbb R.\tag{20}
\]
We emphasize that this arithmetic is carried out in $\mathbb R$, not modulo $2\pi$. We consider an oracle version of the above method-of-moments procedure, where $\widehat\Phi^{\mathrm{oracle}}_{k,l}\in[\Phi_{k,l}-\pi,\Phi_{k,l}+\pi)$ is chosen in Step 2 as the unique version of the complex argument of $\widehat B_{k,l}$ that belongs to this range. Recalling the complex representation of $\theta$ in (12) and defining
\[
B_{k,l}=\widetilde\theta_{k+l}\cdot\overline{\widetilde\theta_k}\cdot\overline{\widetilde\theta_l}=r_{k+l}r_kr_le^{i(\phi_{k+l}-\phi_k-\phi_l)}\in\mathbb C,\tag{21}
\]
note that this means, for the principal argument specified in (11),
\[
\widehat\Phi^{\mathrm{oracle}}_{k,l}-\Phi_{k,l}=\operatorname{Arg}(\widehat B_{k,l}/B_{k,l})\in[-\pi,\pi).\tag{22}
\]
We will write $\widehat\Phi^{\mathrm{oracle}}=\widehat\Phi^{\mathrm{oracle}}(\phi)$ if we wish to make explicit the dependence of this definition on the phase vector $\phi$ of the true signal. We denote by $\widehat\phi^{\mathrm{oracle}}$ the resulting least-squares estimate of $\phi$ in (18), and by $\widehat\theta^{\mathrm{oracle}}$ the corresponding estimate of $\theta$.
''',[9],'Section 4.1 — The oracle procedure',{'D9':'The oracle supplies the argument versions in Step 2 and uses the same least-squares reconstruction.','D7':'Its centered argument formula uses the complex bispectrum and principal argument.','D2':'The lift is centered on real representatives of the true Fourier phases.'},context='The oracle procedure.',symbols=[r'\widehat\theta^{\mathrm{oracle}}',r'\widehat\Phi^{\mathrm{oracle}}'],shape='Oracle-specific argument lift using true phases, including the complete definition of the true bispectrum. Do not identify it with an observable estimator.')
add('D11','Mimicking the oracle',r'''
We now consider the method-of-moments procedure where the choice of $\widehat\Phi_{k,l}$ in Step 2 is determined instead by the following method: Compute a “pilot” estimate of $\phi$ as any minimizer of the $\ell_\infty$-type objective
\[
\widetilde\phi=\arg\min_{\phi\in\mathcal A^K}\max_{(k,l)\in\mathcal I}|\operatorname{Arg}\widehat B_{k,l}-(\phi_{k+l}-\phi_k-\phi_l)|_{\mathcal A},\tag{31}
\]
where a minimizer exists because $\mathcal A$ is compact under $|\cdot|_{\mathcal A}$. Identify each entry $\widetilde\phi_k\in[-\pi,\pi)$ of this estimate as a real value, and set $\widetilde\Phi_{k,l}=\widetilde\phi_{k+l}-\widetilde\phi_k-\widetilde\phi_l$ where arithmetic is again carried out in $\mathbb R$, not modulo $2\pi$. Then choose $\widehat\Phi^{\mathrm{opt}}_{k,l}\in[\widetilde\Phi_{k,l}-\pi,\widetilde\Phi_{k,l}+\pi)$ as the unique version of complex argument of $\widehat B_{k,l}$ belonging to this range. Let $\widehat\phi^{\mathrm{opt}}$ be the resulting least-squares estimate of $\phi$ in (18), and let $\widehat\theta^{\mathrm{opt}}$ be the corresponding estimate of $\theta$.
''',[12],'Section 4.2 — Mimicking the oracle',{'D9':'The pilot selects Step 2 argument lifts, followed by the original real least-squares reconstruction.','D8':'The pilot minimizes maximum circular discrepancies on A^K.','D7':'The observed bispectrum enters by its principal complex argument.'},context='Mimicking the oracle.',symbols=[r'\widetilde\phi',r'\widehat\theta^{\mathrm{opt}}'],shape='Data-dependent circular l-infinity pilot followed by real argument lifting and least squares; do not import oracle phases or its proof-only stability lemmas.')
add('D12','maximum likelihood estimator',r'''
Define the log-likelihood function
\[
l(\theta,y)=\log p_\theta(y):=\log\left[\frac1{2\pi}\int_{-\pi}^{\pi}\left(\frac1{\sqrt{2\pi\sigma^2}}\right)^{2K}\exp\left(-\frac{\|y-g(\alpha)\cdot\theta\|^2}{2\sigma^2}\right)\,\mathrm d\alpha\right],\tag{35}
\]
where $p_\theta(y)$ denotes the Gaussian mixture density that marginalizes over the unknown rotation. Then the MLE is given by
\[
\widehat\theta^{\mathrm{MLE}}=\arg\min_{\theta\in\mathbb R^{2K}}R_N(\theta),\quad R_N(\theta)=-\frac1N\sum_{m=1}^Nl(\theta,y^{(m)}),
\]
where $R_N(\theta)$ denotes the negative empirical log-likelihood.
''',[14],'Section 5 — Maximum likelihood estimator, equation (35)',{'D3':'The likelihood is the Gaussian mixture density of the observation model, with the independent sample log-likelihood summed over m.','D2':'The latent rotation acts through g(alpha).'},context='Motivated by this observation, and by the more common use of likelihood-based approaches in practice [31, 34], in this section we analyze the maximum likelihood estimator (MLE) in the setting of Theorem 2.2.',symbols=[r'\widehat\theta^{\mathrm{MLE}}',r'R_N(\theta)'],shape='Unconstrained likelihood minimization over all real 2K-vectors after marginalizing latent uniform rotations, not a minimization over Theta_beta or a proof-aligned rotation.')
add('D13','Fourier magnitudes',r'''
There exists a constant $c_{\mathrm{gen}}>0$ such that for any $B\subseteq\{1,\ldots,K\}$ with $|B|\geq K/2$,
\[
\sum_{k\in B}r_k(\theta^*)^2\geq c_{\mathrm{gen}}\|\theta^*\|^2.
\]
''',[15],'Assumption 5.1',{'D2':'The assumption constrains the total squared Fourier magnitude in every subset containing at least half the frequencies.'},kind='condition',context=r'For the results of this section, we isolate the following general condition for the Fourier magnitudes of $\theta^*$. ',phrases=['Assumption 5.1'],symbols=[r'c_{\mathrm{gen}}'],shape='Uniform lower bound on energy in every subset of at least K/2 frequencies. Do not replace this assumption by the stronger two-sided power-law class.')
members['D13']['source_kind']='assumption'

def main():
    for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('interface-draft.json',interfaces)]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source interfaces.')
if __name__=='__main__':main()
