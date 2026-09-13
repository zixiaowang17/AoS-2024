"""Preserve all twelve Theorems, including those in the numbered main Proofs section."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0519', 'title': 'Consistent inference for diffusions from low frequency measurements', 'version': 'arXiv:2210.13008v3', 'source_url': 'https://arxiv.org/pdf/2210.13008v3', 'pdf_pages': 34, 'pdf_sha256': '2fac61e70c2fa85e1da196dc4b3bc1d96c50114dba0000536b8d06a3d947c47a'}
claims=[]
def claim(n,page,body):claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n),source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=page,location='Theorem '+str(n))]))
claim(1,3,r'''
Suppose positive diffusion coefficients $f_1,f_2\in C^2(\mathcal O)$ are bounded away from zero on $\mathcal O$ and such that $f_1=f_2$ near $\partial\mathcal O$. Then if $P_{D,f_1}=P_{D,f_2}$ coincide as bounded linear operators on $L^2(\mathcal O)$ for some $D>0$, we must have $f_1=f_2$ on $\mathcal O$.
''')
claim(2,4,r'''
Let $D>0$ and consider data $X_0,X_D,\ldots,X_{ND}$ generated from the diffusion (2) in a bounded smooth convex domain $\mathcal O$. Assume the ground truth $f_0>1/4$ is sufficiently regular in a Sobolev sense and equals $1/2$ near $\partial\mathcal O$. Assign an appropriate Gaussian process prior $\Pi$ to $(\theta(x):x\in\mathcal O)$, form $f_\theta=(1+e^\theta)/4$, and consider the random field
\[
(\overline f_N\equiv f_{\overline\theta_N}(x):x\in\mathcal O),\quad\overline\theta_N=E^\Pi[\theta\mid X_0,X_D,\ldots,X_{ND}],
\]
arising from the posterior mean function. Then the posterior inference for the transition operators $P_{t,f_0},t>0$, as well as for $f_0$ is consistent, that is, as $N\to\infty$ and in $\mathbb P_{f_0}$-probability,
\[
\|P_{t,\overline f_N}-P_{t,f_0}\|_{L^2\to L^2}\to0,\quad\text{and }\|\overline f_N-f_0\|_{L^2}\to0,
\]
where $\|\cdot\|_{L^2\to L^2}$ denotes the operator norm on $L^2=L^2(\mathcal O)$.
''')
claim(3,6,r'''
Consider data $X_0,X_D,\ldots,X_{ND}$, at fixed observation distance $D>0$, from the reflected diffusion model (2) on a bounded convex domain $\mathcal O\subset\mathbb R^d$ with smooth boundary, started at $X_0\sim Unif(\mathcal O)$, with $f_0\in C^2\cap H^s,s>2d-1$, such that $\inf_{x\in\mathcal O}f_0(x)\geq f_{min}>0$, $U\geq\|f_0\|_{H^s}+\|f_0\|_{C^2}$. Then the estimator $\widehat P_J$ from (63) with choice $J_N\simeq N^{d/(2s+2+d)}$ satisfies,
\[
\|\widehat P_J-P_{D,f_0}\|_{L^2\to L^2}=O_{\mathbb P_{f_0}}\left(N^{-(s+1)/(2s+2+d)}\right),\quad N\to\infty,\tag{5}
\]
with constants $C=C(s,D,U,d,\mathcal O,f_{min})>0$ in the $O_{\mathbb P_{f_0}}$ notation.
''')
claim(4,6,r'''
In the setting of Theorem 3, there exists a bounded convex domain $\mathcal O\subset\mathbb R^d$ with smooth boundary and a constant $c=c(s,D,U,d,f_{min})>0$ such that
\[
\liminf_{N\to\infty}\inf_{\widetilde P_N}\sup_{f:\|f\|_{H^s(\mathcal O)}\leq U,\,f\geq f_{min}>0}\mathbb P_f\left(\|\widetilde P_N-P_{D,f}\|_{H^2\to H^2}>cN^{-(s-1)/(2s+2+d)}\right)>1/4,\tag{7}
\]
where the infimum extends over all estimators $\widetilde P_N$ of $P_{D,f}$ (i.e., measurable functions of the $X_0,X_D,\ldots,X_{ND}$ taking values in the space of bounded linear operators on $L^2$).
''')
claim(5,7,r'''
Let $\mathcal O$ be a bounded convex domain in $\mathbb R^d,d\in\mathbb N$, with smooth boundary. Let $f,f_0$ be bounded from below by a constant $f_{min}>0$, suppose $f=f_0$ on $\mathcal O\setminus\mathcal O_0$ for some compact subset $\mathcal O_0$ of $\mathcal O$ and that $\|f\|_{C^2}+\|f_0\|_{C^2}\leq U$ for some $U$. Then there exists a positive constant depending on $D,d,\mathcal O_0,\mathcal O,U,f_{min}$ such that
\[
\|f-f_0\|_{L^2(\mathcal O)}\leq C\left(\log\frac1{\|P_{D,f}-P_{D,f_0}\|_{L^2\to L^2}}\right)^{-2/3}.\tag{8}
\]
In particular if $P_{D,f}=P_{D,f_0}$ co-incide as linear operators on $L^2(\mathcal O)$ for some $D>0$, we must have $f=f_0$ on $\mathcal O$.
''')
claim(6,7,r'''
In addition to the hypotheses of Theorem 5, assume also $\|f\|_{H^s}+\|f_0\|_{H^s}\leq U$ for some $s>d$ and that
\[
\inf_{x\in\mathcal O_0}\frac12\Delta E_{1,f_0,\iota}(x)+\mu|\nabla E_{1,f_0,\iota}(x)|_{\mathbb R^d}^2\geq c_0>0,\tag{10}
\]
for some $\mu,c_0>0$ and some vector $\iota$. Then we have
\[
\|f-f_0\|_{L^2}\leq\overline C\|P_{D,f}-P_{D,f_0}\|_{H^2\to H^2}\tag{11}
\]
for a constant $\overline C=\overline C(U,D,\mu,c_0,\iota,\mathcal O_0,\mathcal O,f_{min},d)$.
''')
claim(7,8,r'''
Under the hypotheses of Theorem 6 we have
\[
\|P_{t,f}-P_{t,f_0}\|_{HS}\leq C'\|P_{D,f}-P_{D,f_0}\|_{L^2\to L^2}^{\gamma},\quad\text{any }0<t<D,\tag{14}
\]
where $0<\gamma<1$ is as in (12) and where $C'=C(D,t,s,U,\mu,c_0,\iota,\mathcal O,\mathcal O_0,f_{min},d)$.
''')
claim(8,9,r'''
A) Consider domains $\mathcal O_{m,w}$ for $w\geq2$. Then we can choose $m$ large enough such that the Laplacian $-\Delta=-\mathcal L_1$ on $\mathcal O_{m,w}$ has a simple eigenvalue $0<\lambda_{1,1,m}<\lambda_{2,1,m}$ and the corresponding eigenfunction $e_{1,1,m}$ satisfies (10) for any compact subset $\mathcal O_0$ of $\mathcal O_{(w)}$, with constant $\mu,c_0$ depending on $\mathcal O_0,d,w,m$.

B) The conclusions in A) remain valid if we replace $\mathcal L_1$ by $\mathcal L_{f_0}$ for any $f_0$ that satisfies $\|f_0\|_{H^s(\mathcal O_{m,w})}\leq U,s>d$, as well as $\|f_0-1\|_\infty<\kappa$ for some $\kappa$ small enough, with constants now depending also on $\kappa,U$.
''')
claim(9,12,r'''
Consider discrete data $X_0,X_D,\ldots,X_{ND}$, at fixed observation distance $D>0$, from the reflected diffusion model (2) on a bounded convex domain $\mathcal O\subset\mathbb R^d$ with smooth boundary, started at $X_0\sim Unif(\mathcal O)$. Assume $f_0\in H^s,s>\max(2+d/2,2d-1)$, satisfies $\inf_{x\in\mathcal O}f_0(x)>1/4$ and $f_0=1/2$ on $\mathcal O\setminus\mathcal O_{00}$. Let $\Pi(\cdot\mid X_0,X_D,\ldots,X_{ND})$ be the posterior distribution (16) resulting from the prior $\Pi$ for $f$ from (17) with $K\simeq N^{d/(2s+2+d)}$ and the given $s$. Then there exists $M$ depending on $D,\mathcal O,\mathcal O_{00},s,d$ and $U\geq\|f_0\|_{H^s}$ such that
\[
\Pi\left(f:\|P_{D,f}-P_{D,f_0}\|_{L^2\to L^2}\geq MN^{-(s+1)/(2s+2+d)}\mid X_0,X_D,\ldots,X_{ND}\right)\xrightarrow[N\to\infty]{\mathbb P_{f_0}}0.\tag{18}
\]
''')
claim(10,12,r'''
Consider the setting of Theorem 9. Then there exists a sequence $\eta_N\to0$ such that as $N\to\infty$,
\[
\Pi\left(f:\|f-f_0\|_{L^2(\mathcal O)}\geq\eta_N\mid X_0,X_D,\ldots,X_{ND}\right)\to^{\mathbb P_{f_0}}0,\tag{20}
\]
as well as, for any $t>0$,
\[
\Pi\left(f:\|P_{t,f}-P_{t,f_0}\|_{HS}\geq\eta_N\mid X_0,X_D,\ldots,X_{ND}\right)\to^{\mathbb P_{f_0}}0.\tag{21}
\]
Specifically we can take $\eta_N=O((\log N)^{-\delta'})$ for some $\delta'>0$. Moreover, if in addition (10) holds for $f_0$, then we can take $\eta_N=O(N^{-(s-1)/(2s+2+d)})$.
''')
claim(11,17,r'''
Let $f,f_0$ satisfy the conditions of Proposition 2B) for some $s>d$. Suppose $f=f_0$ outside of a compact subset $\mathcal O_0\subset\mathcal O$. Then for any $D>0$ there exist positive constants $C_0,C_1$ depending on $D,\mathcal O,\mathcal O_0,s,d,U,f_{min}$ such that
\[
KL(f,f_0)\leq C_0\|P_{D,f_0}-P_{D,f}\|_{HS}^2\leq C_1\|f-f_0\|_{(H_c^1)^*}^2.\tag{45}
\]
''')
claim(12,25,r'''
Let $\Pi=\Pi_N$ be a sequence of priors on $\mathcal F$ and suppose for $f_0\in\mathcal F$, some sequence $\delta_N\to0$ such that $\sqrt N\delta_N\to\infty$ and constant $A>0$ we have
\[
\Pi_N(B_{\delta_N})\geq e^{-AN\delta_N^2}.\tag{75}
\]
Suppose further for a sequence of subsets $\mathcal F_N\subset\mathcal F$ and constant $B>A+2$ we have
\[
\Pi_N(\mathcal F\setminus\mathcal F_N)\leq e^{-BN\delta_N^2}\tag{76}
\]
and that there exists tests $\Psi_N=\Psi(X_0,\ldots,X_{ND})$ and a sequence $\overline\delta_N\to0$ such that
\[
E_{f_0}\Psi_N\to_{N\to\infty}0,\qquad\sup_{f\in\mathcal F_N,d(f,f_0)>\overline\delta_N}E_f[1-\Psi_N]\leq e^{-BN\delta_N^2},\tag{77}
\]
where $d$ is some distance function on $\mathcal F$. Then we have for $0<b<B-A-2$ that
\[
\Pi\left(\mathcal F_N\cap\{f:d(f,f_0)\leq\overline\delta_N\}\mid X_0,\ldots,X_{ND}\right)=1-O_{\mathbb P_{f_0}}(e^{-bN\delta_N^2}).\tag{78}
\]
''')
def main():
    repo = Path(__file__).resolve().parents[5]
    source = Path(subprocess.check_output([sys.executable, str(repo/'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=34,main_text_boundary=dict(location='The PDF consists of Sections 1-3 followed by references ending on page 34. Section 3 Proofs is part of the numbered main text and contains Theorems 11 and 12. There are no attached appendices or supplementary sections in this version.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,c['claim_id']
            assert depth==0,c['claim_id']
    p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)

if __name__ == '__main__':
    main()
