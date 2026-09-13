"""Restore nine complete original Theorems from the registered local arXiv v2.

This preserves the reviewed transcription; running it is not a new source review.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1845'
SHA='8f13d1bece5dac9408eb42ab31169cae838e25fef36717ef9376604dccd585d4'
URL='https://arxiv.org/pdf/2203.10418v2'
NUMBERS=['3.3','3.5','3.6','3.7','4.1','4.2','4.3','4.5','4.6']
TITLES=['High probability bounds for Huber ReLU-DNN estimation',r'Optimal rate for adaptive Huber estimator under $\mathcal H(d,l,\mathcal P)$ and asymmetric noise',r'Optimal rate for least squares estimator under $\mathcal H(d,l,\mathcal P)$',r'Optimal rate under $\mathcal H(d,l,\mathcal P)$ and symmetric noise',r'A generic lower bound on the $L_2$ error',r'A generic lower bound on the $L_2$ error of least squares estimator','Neural network approximation error, lower bound',None,None]
PAGES=[[11,12],[14],[15],[15,16],[18],[19],[20],[23,24],[24,25]]
STATEMENTS=[r'''Assume Conditions 1 and 2 hold with $p\geq2$. Write $\mathcal F_n=\mathcal F_n(d,\bar L,\bar N,M)$ with $\bar N,\bar L,n\in\{3,4,\ldots,\}$, and let $\tau\in[c_1,\infty]$. For any $\omega,D\geq1$, define $\delta_{n,\tau}=\delta_b\vee\delta_a\vee\delta_s$, where
\[
\delta_b=\frac{v_p}{\tau^{p-1}},\quad
\delta_a=\inf_{f\in\mathcal F_n}\|f-f_0\|_2,\quad
\delta_s=\sqrt{V_n\{v_2+\min\{\tau,\omega v_p^{1/p}V_n^{-1/p}\}\}}
\]
(3.11)
and $V_n=n^{-1}(\bar N\bar L)^2\log(\bar N\bar L)\log n$. Let $\mathcal S_{n,\tau}(\delta)$ be the set of approximate empirical risk minimizers with optimization error $\delta$, that is, $\mathcal S_{n,\tau}(\delta)=\{f\in\mathcal F_n:\widehat{\mathcal R}_\tau(f)\leq\inf_{g\in\mathcal F_n}\widehat{\mathcal R}_\tau(g)+\delta^2\}$. Then, there exists some universal constant $c_2>0$ independent of $(\bar N,\bar L,n,\tau,\omega,D,v_p,v_2)$, $f_0$ and the distribution of $(X,\varepsilon)$ such that, for any $\delta_{\mathrm{opt}}>0$,
\[
\mathbb P\left\{\sup_{f\in\mathcal S_{n,\tau}(\delta_{\mathrm{opt}})}\|f-f_0\|_2\geq c_2(D\delta_{n,\tau}+\delta_{\mathrm{opt}})\right\}
\lesssim\begin{cases}
e^{-nV_nD^2/c_2}&\text{if }\tau\leq\omega D^2(v_p/V_n)^{1/p}\\
e^{-nV_n/c_2}+\omega^{1-p}D^{-2p}&\text{if }\tau>\omega D^2(v_p/V_n)^{1/p}.
\end{cases}
\]
(3.12)''',r'''Assume Conditions 1 holds, $v_2\asymp1$ and $v_p^{1/((2p-1)p)}\lesssim(\log n)^{C'}$ for some constant $C'>0$. Let $\beta^*,d^*$ and $\gamma^*$ be as in (2.6), and $L,N\geq3$ be such that
\[
LN\asymp\left(\frac{n}{\log^6 n}\right)^{\frac{\nu^*}{2(2\gamma^*+\nu^*)}}\quad\text{with }\nu^*=1-\frac1{2p-1}.
\]
(3.14)
Consider the neural network class $\mathcal F_n=\mathcal F_n(d,\bar L,\bar N,M)$ with depth and width
\[
\bar L=c_3\lceil L\log L\rceil\quad\text{and}\quad\bar N=c_4\lceil N\log N\rceil,
\]
(3.15)
where $c_3$–$c_4$ are the positive constants from Proposition 3.4. Moreover, let $\delta_{n,\mathrm{AH}}$ and $\tau_n$ be such that
\[
\delta_{n,\mathrm{AH}}\asymp\left(\frac{\log^6 n}{n}\right)^{\frac{\gamma^*\nu^*}{2\gamma^*+\nu^*}}v_p^{\frac1{2p-1}}\quad\text{and}\quad
\tau_n\asymp\left(\frac{n}{\log^6 n}\right)^{\frac{2\gamma^*(1-\nu^*)}{2\gamma^*+\nu^*}}v_p^{\frac2{2p-1}}.
\]
(3.16)
Provided that $n$ is sufficiently large, we have for any $D\geq1$ that
\[
\sup_{\substack{f_0\in\mathcal H(d,l,\mathcal P),\\\mathbb E[\varepsilon\mid X]=0,\mathbb E[|\varepsilon|^p\mid X]\leq v_p}}
\mathbb P\left\{\sup_{f\in\mathcal S_{n,\tau_n}(\delta_{n,\mathrm{AH}})}\|f-f_0\|_2\geq c_6D\delta_{n,\mathrm{AH}}\right\}
\lesssim\exp\left\{-D^2n^{\frac{\nu^*}{2\gamma^*+\nu^*}}(\log n)^{\frac{8\gamma^*-2\nu^*}{2\gamma^*+\nu^*}}/c_6\right\},
\]
where $c_6>0$ is a universal constant independent of $(n,D,p,v_p)$.''',r'''Assume Condition 1 holds and $v_2\asymp1$. Let $\beta^*,d^*$ and $\gamma^*$ be as in (2.6), and $N,L\geq3$ satisfying $(NL)\asymp\{n/\log^6(n)\}^{\nu^\dagger/(4\gamma^*+2\nu^\dagger)}$ for $\nu^\dagger=1-1/p$. Consider the approximate least squares estimates with optimization error bounded by $\delta_{n,\mathrm{LS}}^2$, where $\delta_{n,\mathrm{LS}}\asymp\{\log^6(n)/n\}^{\gamma^*\nu^\dagger/(2\gamma^*+\nu^\dagger)}v_p^{1/(2p)}$ and the depth and width of the network class $\mathcal F_n=\mathcal F_n(d,\bar L,\bar N,M)$ satisfy (3.15). Then, for all sufficiently large $n$, the following bound
\[
\sup_{\substack{f_0\in\mathcal H(d,l,\mathcal P)\\\mathbb E[\varepsilon\mid X]=0,\mathbb E[|\varepsilon|^p\mid X]\leq v_p}}
\mathbb P\left\{\sup_{f\in\mathcal S_{n,\infty}(\delta_{n,\mathrm{LS}})}\|f-f_0\|_2\geq c_7D\delta_{n,\mathrm{LS}}\right\}\leq c_7D^{-2p}
\]
holds for any $D\geq1$, where $c_7$ is a universal constant independent of $(n,D,p,v_p)$.''',r'''Assume Conditions 1 and 3 hold. Consider the function class $\mathcal F_n=\mathcal F_n(d,\bar L,\bar N,M)$, where the depth $\bar L$ and width $\bar N$ satisfies (3.15) with $L,N\geq3$ satisfying $LN\asymp\{n/\log^6(n)\}^{1/(4\gamma^*+2)}$. Furthermore, let $c_1\leq\tau\lesssim1$ and $\delta_{n,\mathrm H}\asymp\{(\log n)^6/n\}^{\frac{\gamma^*}{2\gamma^*+1}}$. Then, for all sufficiently enough $n$ and arbitrary $D\geq1$, it holds
\[
\sup_{f_0\in\mathcal H(l,d,\mathcal P)}\mathbb P\left\{\sup_{f\in\mathcal S(\delta_{n,\mathrm H})}\|f-f_0\|_2\geq c_8D\delta_{n,\mathrm H}\right\}
\lesssim\exp\left\{-n^{\frac1{2\gamma^*+1}}(\log n)^{\frac{12\gamma^*}{2\gamma^*+1}}D^2/c_8\right\},
\]
where $c_8$ is a universal constant independent of $n,D$.''',r'''Let $\mathcal F_0\subseteq\{f:\mathbb R^d\to[-1,1]\}$ be a function class with intrinsic dimension-adjusted smoothness upper bounded by some $\alpha>0$. Suppose $0\in\mathcal F_0$. Define the family of data generating processes as
\[
\mathcal U(d,p,\mathcal F)=\{(X,f_0,\varepsilon):X\sim\operatorname{Uniform}([0,1]^d),f_0\in\mathcal F,\mathbb E[\varepsilon\mid X]=0,\mathbb E[|\varepsilon|^p\mid X]\leq1\}.
\]
(4.2)
Let $\mathcal S^{\mathrm{HN}}_{n,\tau}(\delta)$ be the set of all approximate Huber ReLU-DNN estimates with given robustification parameter $\tau$, depth $\bar L$ and width $\bar N$, i.e.,
\[
\begin{aligned}
\mathcal S^{\mathrm{HN}}_{n,\tau}(\delta)=\bigg\{\widetilde f_n\in\mathcal F_n(d,\bar L,\bar N,1):{}&\widehat{\mathcal R}_\tau(\widetilde f_n)\leq\min\Big\{\widehat{\mathcal R}_\tau(f_{0,\tau}),\inf_{f\in\mathcal F_n(d,\bar L,\bar N,1)}\widehat{\mathcal R}_\tau(f)+c_9\delta^2\Big\}\\
&\text{or }\widehat{\mathcal R}_\tau(\widetilde f_n)\leq\inf_{f\in\mathcal F_n(d,\bar L,\bar N,1)}\widehat{\mathcal R}_\tau(f)+n^{-100}\bigg\}
\end{aligned}
\]
(4.3)
for some universal constant $c_9>0$ (independent of $\bar N,\bar L,n$ and $\tau$). Then, there exists universal positive constants $c_{10}$–$c_{12}$ independent of $n,\bar L,\bar N,\tau$ such that the following statements hold.

(1) For any $n\geq3$, $\bar N,\bar L\geq c_{11}$ and $\tau\geq c_{12}$,
\[
\sup_{(X,f_0,\varepsilon)\in\mathcal U(d,p,\mathcal F_0)}\mathbb P\{\exists\widehat f_n\in\mathcal S^{\mathrm{HN}}_{n,\tau}(\delta_n)\text{ s.t. }\|\widehat f_n-f_0\|_2\geq\delta_n\}\geq1-\frac{c_{10}}{\log n},
\]
where
\[
\delta_n\asymp\frac1{(\bar N\bar L)^{2\alpha}\log^{5\alpha}(\bar N\bar L)}
\bigvee\left[1\bigwedge\frac{\bar N\bar L}{\sqrt n\log n}\left\{\sqrt\tau\wedge\left(\frac{\sqrt n\log n}{\bar N\bar L}\right)^{1/p}\right\}\right]
\bigvee\frac1{\tau^{p-1}\log^2(n)}.
\]
(4.4)
(2) There exists $\delta_{n,*}\asymp n^{-\frac{\alpha\nu^*}{2\alpha+\nu^*}}(\log n)^{-\frac{\alpha(3\nu^*+4)}{2\alpha+\nu^*}}$ such that
\[
\liminf_{n\to\infty}\inf_{\bar N,\bar L\geq c_{11},\tau\geq c_{12}}\sup_{(X,f_0,\varepsilon)\in\mathcal U(d,p,\mathcal F_0)}\mathbb P\{\exists\widehat f_n\in\mathcal S^{\mathrm{HN}}_{n,\tau}(\delta_{n,*})\text{ s.t. }\|\widehat f_n-f_0\|_2\geq\delta_{n,*}\}=1.
\]''',r'''Let $\mathcal F_0$, $\mathcal U(d,p,\mathcal F)$ and $\mathcal S^{\mathrm{HN}}_{n,\tau}(\delta)$ be as in Theorem 4.1. The following two statements hold.

(1) For any $n\geq3$, $\bar N,\bar L\geq c_{11}$,
\[
\sup_{(X,f_0,\varepsilon)\in\mathcal U(d,p,\mathcal F_0)}\mathbb P\{\exists\widehat f_n\in\mathcal S^{\mathrm{HN}}_{n,\infty}(\delta_n)\text{ s.t. }\|\widehat f_n-f_0\|_2\geq\delta_n\}\geq1-\frac{c_{10}}{\log n},
\]
where $\delta_n\asymp\frac1{(\bar N\bar L)^{2\alpha}\log^{5\alpha}(\bar N\bar L)}\vee\{(\frac{\bar N\bar L}{\sqrt n\log n})^{1-1/p}\wedge1\}$.

(2) There exists $\delta_{n,*}\asymp n^{-\frac{\alpha\nu^\dagger}{2\alpha+\nu^\dagger}}(\log n)^{-\frac{7\alpha\nu^\dagger}{2\alpha+\nu^\dagger}}$ such that
\[
\liminf_{n\to\infty}\inf_{\bar N,\bar L\geq c_{11}}\sup_{(X,f_0,\varepsilon)\in\mathcal U(d,p,\mathcal F_0)}\mathbb P\{\exists\widehat f_n\in\mathcal S^{\mathrm{HN}}_{n,\infty}(\delta_{n,*})\text{ s.t. }\|\widehat f_n-f_0\|_2\geq\delta_{n,*}\}=1,
\]
(4.5)''',r'''Suppose $\bar L,\bar N\geq3$ are arbitrarily given integers. Let $\mathcal F_0\subseteq\{f:\mathbb R^d\to[-1,1]\}$ be a function class with intrinsic dimension-adjusted smoothness upper bounded by $\alpha$. Let $\mathcal F_n=\mathcal F_n(d,\bar L,\bar N,1)$ be the neural network class of interest. Then, there exists some constant $c_{13}>0$ independent of $\bar N$ and $\bar L$ such that
\[
\sup_{f_0\in\mathcal F_0}\inf_{f\in\mathcal F_n}\|f-f_0\|_2\geq c_{13}\{(\bar N\bar L)^2\log^5(\bar N\bar L)\}^{-\alpha},
\]
where $\|\cdot\|_2=\|\cdot\|_{L_2(\mathbb P_X)}$ with $\mathbb P_X$ denoting the uniform distribution on $[0,1]^d$.''',r'''For any given $N,L\in\mathbb N^+$, let $K=\lfloor N^{1/d}\rfloor^2\lfloor L^{1/d}\rfloor^2$, and $\{y_\alpha\}_{\alpha\in\mathcal A}\subseteq[0,1]$ be an arbitrary set of values indexed by $\mathcal A=\{1,\ldots,K\}^d$. For any tolerance parameter $\Delta\in(0,1/(3K)]$, and precision parameter $\epsilon\in(0,1)$, let
\[
Q_\alpha(\Delta)=\left\{x=(x_1,\cdots,x_d):(\alpha_i-1)/K\leq x_i\leq\alpha_i/K-\mathbf1_{\{\alpha_i<K\}}\Delta\right\}.
\]
(4.8)
Then, there exist a deep ReLU neural network $f_1^\dagger$ with depth $(5L+7)(\lceil\log_2(1/\epsilon)\rceil+2)$ and width $(4N+3)d\vee(8N+10)$, and a deep ReLU neural network $f_2^\dagger$ with depth $9L+12$ and width $(4N+3)d\vee(8N+6)(\lceil\log_2(1/\epsilon)\rceil+1)$ such that
\[
|f_s^\dagger(x)-y_\alpha|\leq\epsilon\text{ for all }x\in Q_\alpha(\Delta),\quad s=1,2.
\]
(4.9)
Moreover, if $y_\alpha=\sum_{i=0}^r2^{-i}\theta_i$ for $(\theta_1,\ldots,\theta_r)\in\{0,1\}^r$ with $r\leq\lceil\log_2(1/\epsilon)\rceil$, we have $f_s^\dagger(x)=y_\alpha$ instead of $|f_s^\dagger(x)-y_\alpha|\leq\epsilon$ in (4.9). In this case, the term $\lceil\log_2(1/\epsilon)\rceil+1)$ in the width and depth can further be reduced to $r$ if all the $y_\alpha$ can be written as the above form.''',r'''Given any integers $N,L\geq1$, let $K=\lfloor N^{1/d}\rfloor^2\lfloor L^{1/d}\rfloor^2$. For any $\Delta_1\in(0,1/(3K)]$, $\Delta_2>0$, suppose $(x_\alpha,y_\alpha)_{\alpha\in\widetilde{\mathcal A}}$ is a set of arbitrary points indexed by $\widetilde{\mathcal A}\subseteq\{1,\cdots,K\}^d$. Each element $(x_\alpha,y_\alpha)$ satisfies $x_\alpha\in Q_\alpha(\Delta_1)$ defined by (4.8) and $y_i\in\{-1,1\}$. Then there exist some constants $c_{22}$–$c_{25}$ independent of $N,L,\Delta_1,\Delta_2$ such that for any $u\in[-1,1]$, we can find a deep ReLU neural network $f_1^\dagger$ with depth $c_{22}L\log_2(1/\Delta_2)$ and width $c_{23}N$ and a deep ReLU neural network $f_2^\dagger$ with depth $c_{24}L$, $c_{25}N\log_2(1/\Delta_2)$ satisfying
\[
f_s^\dagger(x_\alpha)=y_\alpha\text{ for all }\alpha\in\widetilde{\mathcal A},\quad s=1,2,
\]
and
\[
f_s^\dagger(x)=u\text{ if }x\in Q,\text{ and }\|x-x_\alpha\|_\infty\geq\Delta_2\text{ for all }\alpha\in\widetilde{\mathcal A},\quad s=1,2,
\]
where $Q=\bigcup_{\alpha\in\{1,\cdots,K\}^d}Q_\alpha(\Delta_1)$.''']
def inventory():
    claims=[]
    for i,(num,title,s,pages) in enumerate(zip(NUMBERS,TITLES,STATEMENTS,PAGES),1):
        label='Theorem '+num+((' ('+title+')') if title else '')
        claims.append(dict(claim_id=PID+'/T'+num,paper_id=PID,claim_kind='theorem',label=label,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+num+'; complete original statement, including continuation where present') for p in pages]))
    paper=dict(paper_id=PID,title='How do noise tails impact on deep ReLU networks?',authors=['Jianqing Fan','Yihong Gu','Wen-Xin Zhou'],version='arXiv:2203.10418v2; arXiv stamp 30 Dec 2022',pdf_pages=79,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=27,main_text_boundary=dict(location='Main text ends in Section 5 Conclusion on PDF page 27, before References at y=208.450. Retained page-27 evidence is clipped at y=207.5. References and appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerated actual bold Theorem headings across all main-text pages; visually compared all nine complete statements and their continuations. Excluded diagram labels, citations, Propositions, Lemmas, Remarks and appendices.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v2 only; no source replacement, web search or appendix-body reading.',normalization_policy='Original wording, formulas, branches, quantifiers and source irregularities retained. Normalize PDF line wrapping and mathematical typesetting only; no repaired or expanded hypotheses.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved nine complete original main-text Theorems; independent inventory review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
