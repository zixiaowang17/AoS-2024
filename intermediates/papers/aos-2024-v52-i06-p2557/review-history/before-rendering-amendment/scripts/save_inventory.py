"""Reproduce all fourteen original main-text Theorem statements in source order."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2557'
SHA='e3655b1b7191064691ba36bf048e6d681c8b82fbb39ff47419e9a3cbdb9f9365'
URL='https://arxiv.org/pdf/2302.06025v3'
NUMBERS=[str(i) for i in range(1,15)]
PAGES=[6,7,8,10,11,11,12,15,22,24,27,28,28,29]
STATEMENTS=[r'''In a ridge bandit problem with the link function $f$ satisfying Assumption 1, for any $\kappa\in(0,1/4)$, the following upper bound holds for the burn-in cost:
\[
T^\star_{\mathrm{burn\text{-}in}}(f,d)\lesssim d^2\cdot\int_{1/\sqrt d}^{1/2}\frac{\mathrm d(x^2)}{\max_{1/\sqrt d\le y\le x}\min_{z\in[(1-\kappa)y,(1+\kappa)y]}[f'(z)]^2},
\]
with a hidden factor depending on $\kappa$. This upper bound is achieved by Algorithm 1 in Section 3.1.''',r'''Suppose $f$ is even or odd. In a ridge bandit problem with the link function $f$ satisfying Assumption 1, the following lower bound holds for the burn-in cost: whenever $T^\star_{\mathrm{burn\text{-}in}}(f,d)\le T$, then
\[
T^\star_{\mathrm{burn\text{-}in}}(f,d)\gtrsim d\cdot\int_{\sqrt{c\log(T)/d}}^{1/2}\frac{\mathrm d(x^2)}{(f(x))^2}.
\]
Here $c>0$ is an absolute constant independent of $(f,d)$.''',r'''Consider a ridge bandit problem with a link function $f$ satisfying Assumption 1. In what follows $\kappa\in(0,1/4)$ is any fixed constant, and $c_1,c_2>0$ are absolute constants independent of $(f,d,\varepsilon)$.

• For $\varepsilon\in[c_1/\sqrt d,1/2]$, the following upper bound holds on the learning trajectory:
\[
T^\star_{\mathrm{burn\text{-}in}}(f,d,\varepsilon)\lesssim d^2\cdot\int_{1/\sqrt d}^{\varepsilon}\frac{\mathrm d(x^2)}{\max_{1/\sqrt d\le y\le x}\min_{z\in[(1-\kappa)y,(1+\kappa)y]}[f'(z)]^2}.
\]

• In addition assume that $f$ is even or odd. Then for $\varepsilon\in[\sqrt{c_2\log(T)/d},1/2]$, the following lower bound holds on the learning trajectory: if $T^\star_{\mathrm{burn\text{-}in}}(f,d,\varepsilon)\le T$, then
\[
T^\star_{\mathrm{burn\text{-}in}}(f,d,\varepsilon)\gtrsim d\cdot\int_{\sqrt{c_2\log(T)/d}}^{\varepsilon}\frac{\mathrm d(x^2)}{(f(x))^2}.
\]''',r'''For every Lipschitz link function $f$ satisfying Assumption 1, there exists a tie-breaking rule for (El-UCB) such that for the Eluder-UCB algorithm, the following lower bound holds for its sample complexity $T^\star_{\mathrm{UCB}}$ of achieving inner product at least $\varepsilon$: whenever $T^\star_{\mathrm{UCB}}\le T$ and $\varepsilon\ge\sqrt{c\log(T)/d}$, it holds that
\[
T^\star_{\mathrm{UCB}}\gtrsim\frac d{g(\sqrt{c\log(T)/d})^2}.
\]
Here $c>0$ is an absolute constant independent of $(f,d,\varepsilon)$, and $g(x):=\max\{|f(x)|,|f(-x)|\}$.''',r'''For every Lipschitz link function $f$ satisfying Assumption 1, there exists improper online regression oracles satisfying (5) or proper offline regression oracles satisfying (6) such that: for any algorithm under the oracle model, its sample complexity $T^\star_{\mathrm{RO}}$ of achieving an inner product at least $\varepsilon$ satisfies that whenever $T^\star_{\mathrm{RO}}\le T$ and $\varepsilon\ge\sqrt{c\log(T)/d}$, then
\[
T^\star_{\mathrm{RO}}\gtrsim\frac d{g(\sqrt{c\log(T)/d})^2}.
\]
Here $c>0$ is an absolute constant independent of $(f,d,\varepsilon)$, and $g(x):=\max\{|f(x)|,|f(-x)|\}$.''',r'''Suppose the link function $f$ satisfies Assumption 2, and the learner is given an action $a_0$ with $\langle\theta^\star,a_0\rangle\ge1-3\gamma/4$. Then for every $\varepsilon<\gamma$, the output $\widehat\theta_T$ of Algorithm 4 in Section 3.2 satisfies $\mathbb E[\langle\widehat\theta_T,\theta^\star\rangle]\ge1-\varepsilon$ with
\[
T=O\left(\frac{d^2}{c_f^2\varepsilon}\right).
\]
Here the hidden constant depends only on $\gamma$. If in addition $f$ satisfies Assumption 1, Algorithm 4 in Section 3.2 over a time horizon $T$ achieves a cumulative regret
\[
\mathfrak R_T^\star(f,d)=O\left(\min\left\{\frac{C_f}{c_f}d\sqrt T,T\right\}\right).
\]''',r'''Suppose the link function $f$ satisfies Assumptions 2 and 3. Then for every $\varepsilon<1/2$, the following minimax lower bounds hold:
\[
T^\star(f,d,\varepsilon)\ge\frac{cd^2}{\varepsilon},\qquad\mathfrak R_T^\star(f,d)\ge c\min\{d\sqrt T,T\},
\]
where $c>0$ is an absolute constant depending only on $(\gamma,c_f,L)$.''',r'''Suppose the link function $f$ satisfies Assumption 1, and $g(x):=\max\{|f(x)|,|f(-x)|\}$. Given $c>0$, $\delta\in(0,1)$, let $\{\varepsilon_t\}_{t\ge1}$ be a sequence of positive reals defined recursively as follows:
\[
\varepsilon_1=\sqrt{\frac{c\log(1/\delta)}d},\qquad\varepsilon_{t+1}^2=\varepsilon_t^2+\frac cd g(\varepsilon_t)^2,\qquad\forall t\ge1.
\]
(8)
There exists a universal constant $c>0$ such that for any $\delta\in(0,1)$, if $\theta^\star$ is uniform distributed on $\mathbb S^{d-1}$, then for the above sequence $\{\varepsilon_t\}_{t\ge1}$ and all $t\ge1$, any learner satisfies that
\[
\mathbb P\left(\bigcap_{s\le t}\{|\langle\theta^\star,a_s\rangle|\le\varepsilon_s\}\right)\ge1-t\delta.
\]''',r'''Let $\delta\in(0,1/2)$. Suppose that $\kappa_1\in(0,(x_0^{-1}-1)/2)$, $\kappa_2\in(0,1/4)$, and
\[
d_0=\left\lceil\frac{(2\kappa_1+4)^2\kappa_2(2-\kappa_2)}{\kappa_1^2(1-\kappa_2)^2}\right\rceil+1,\qquad c_0=c\left(1+\frac{\kappa_1}4,1+\frac{\kappa_1}2,1-x_0^2,\frac{1-x_0}2\right),
\]
where the function $c(\cdot)$ appears in Lemma 6. Let $\{\varepsilon_i\}_{i\ge0}$ be a set of positive reals defined by
\[
\varepsilon_i=\begin{cases}
\frac12\min_{z\in[1/\sqrt d,(1+\kappa_1/2)/\sqrt d]}\left|f\left(z+\frac{c_1}{\sqrt d}\right)-f(z)\right|&\text{if }1\le i\le d_0,\\
\frac12\max_{c_2/\sqrt d\le y\le(1-\kappa_2)\sqrt{(i-1)/d}}\min_{z\in[(1-\kappa_1)y,(1+\kappa_1)y]}\left|f\left(z+\frac{c_1}{\sqrt d}\right)-f(z)\right|&\text{if }d_0+1\le i\le m,
\end{cases}
\]
where $c_1=\kappa_1\sqrt{1-(1-\kappa_2)^2}/4$, $c_2=(2\kappa_1+4)\sqrt{1-(1-\kappa_2)^2}/\kappa_1$ are numerical constants determined by $(\kappa_1,\kappa_2)$, and $m=\lceil x_0^2d\rceil$.
If $f$ is monotone on $[-1,1]$, then with probability at least $1-\delta$, Algorithm 1 outputs an action $a_0$ with $\langle\theta^\star,a_0\rangle\ge x_0$ using at most
\[
O\left(\log^2\left(\frac d\delta\right)\sum_{i=1}^m\frac1{\varepsilon_i^2}\right)
\]
queries, where the hidden constant depends only on $(x_0,\kappa_1,\kappa_2)$.''',r'''Consider the same setting of Theorem 9, and assume that $f$ is continuous and strictly increasing on $[-1,1]$. Then there is an algorithm without the knowledge of $f$ such that, with probability at least $1-\delta$, it outputs an action $a_0$ with $\langle\theta^\star,a_0\rangle\ge x_0$ using
\[
O\left(\log^3\left(\frac d\delta\right)\sum_{i=1}^m\frac1{\varepsilon_i^2}\right)
\]
queries, where the hidden constant depends only on $(x_0,\kappa_1,\kappa_2)$.''',r'''Let the link function $f$ satisfy Assumption 1 in the ridge bandit problem, and $\theta^\star\sim\operatorname{Unif}(\mathbb S^{d-1})$. Then any nonadaptive learner cannot find $\widehat\theta_T$ with $\mathbb E[\langle\theta^\star,\widehat\theta_T\rangle]>1/2$ if
\[
T<\max_{K\ge1}\frac{cd}{g(\sqrt{(\log K)/d})^2+K^{-1}},
\]
where $c>0$ is an absolute constant, and $g(x):=\max\{|f(x)|,|f(-x)|\}$.''',r'''Let the link function $f$ satisfy Assumption 1 in the ridge bandit problem. For every $K=\exp(o(d))$, there exists a finite action set $\mathcal A$ with $|\mathcal A|=K$ such that any learner cannot find $\widehat\theta_T$ with $\inf_{\theta^\star\in\mathbb S^{d-1}}\mathbb E_{\theta^\star}[\langle\theta^\star,\widehat\theta_T\rangle]\ge4/5$ if
\[
T<\frac c{g(\sqrt{(c'\log K)/d})^2+K^{-1}},
\]
where $c,c'>0$ are absolute constants, and $g(x):=\max\{|f(x)|,|f(-x)|\}$.''',r'''Suppose the link function $f$ satisfies the monotonicity condition in Assumption 1, and $f'(x)/f'(y)\le C$ as long as $1/c\le x/y\le c$ for some constants $c,C>1$. Then the following upper and lower bounds hold for the minimax regret over $\theta^\star\in\mathbb B^d$:
\[
\mathfrak R_T^\star(f,d)\lesssim\max_{r\in[0,1]}\min\left\{\frac{f(r)}{r^4}d^2\int_{r/\sqrt d}^{r/2}\frac{\mathrm d(x^2)}{\max_{r/\sqrt d\le y\le x}\min_{z\in[(1-\kappa)y,(1+\kappa)y]}[f'(z)]^2}+d\sqrt T,Tf(r)\right\},
\]
\[
\mathfrak R_T^\star(f,d)\gtrsim\max_{r\in[0,1]}\min\left\{\frac{f(r)}{r^2}d\int_{r/\sqrt d}^{r/2}\frac{\mathrm d(x^2)}{\max\{f(x)^2,f(-x)^2\}}+d\sqrt T,Tf(r)\right\},
\]
where $\kappa\in(0,1/4)$ is any fixed parameter, and the hidden factors depend only on $(c,C,\kappa)$.''',r'''For the linear bandit $f(x)=\operatorname{id}(x)=x$ with dimension $d$, it holds that
\[
T^\star_{\mathrm{burn\text{-}in}}(\operatorname{id},d)\gtrsim d^2.
\]''']
def inventory():
    cs=[]
    for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,PAGES),1):
        title=' (Weaker version of Theorem '+('9' if n=='1' else '8')+')' if n in ['1','2'] else ''
        cs.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+title,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement, including all conditions and conclusions')]))
    cs[-1]['evidence'][0]['before_main_text_end']=True
    paper=dict(paper_id=PID,title='Statistical Complexity and Optimal Algorithms for Non-linear Ridge Bandits',authors=['Nived Rajaraman','Yanjun Han','Jiantao Jiao','Kannan Ramchandran'],version='arXiv:2302.06025v3, marked 10 Jan 2024; title-page date January 11, 2024',pdf_pages=55,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Section4.4 ends on PDFpage29 with the discussion of sums of ridge functions. AppendixA, Auxiliary lemmas, starts at y654.115 on the same page. Evidence is clipped at y648 before that heading.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Locate AppendixA through the PDF outline and heading coordinates; inspect only main-text pages1–29, clipping29 before the appendix. Independently enumerate SFBX bold Theorem headings: exactly1–14. Keep weaker-version Theorems1/2 and later general Theorems8/9 separately. Exclude corollaries, lemmas, examples, assumptions, definitions, citations and appendix bodies.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v3 PDF pinned bySHA256; main text only, with page29 clipped before AppendixA.',normalization_policy='Preserve full original theorem wording, printed labels, quantifier order, all branches, integrals, recursion and finite-difference formulas. Normalize wrapping/typesetting only. Keep Theorem6 conditional regret branch, Theorem9 i≥0 notation and Lemma6 reference, and Theorem13 unit-ball scope and original r=0-inclusive domain.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all14 complete main-text Theorems; independent review remains separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
