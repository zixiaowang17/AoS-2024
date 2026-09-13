"""Reproduce the eight original main-text Theorems of the registered p2791 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2791'
SHA='f513008a3eea20d3a7e2818b1e1fc38d354cf7b023de1c2f95ff5d36e38b9423'
URL='https://arxiv.org/pdf/2006.02044v2'
NUMBERS=['3.1','3.3','3.4','3.5','3.6','4.1','4.5','4.11']
PAGES=[10,11,11,12,12,13,17,20]
STATEMENTS=[r'''Fix $d\ge5$ and let $\Omega$ be a convex body satisfying (3). The following inequality holds when $\mathcal F$ is either $\mathcal C_L^B(\Omega)$ for $B\ge L$, or $\mathcal C_L(\Omega)$:
\[
\sup_{f\in\mathcal F}\mathbb E_f\ell_{\mathbb P}^2(\hat f_n(\mathcal F),f)\ge c_d\sigma L n^{-2/d}(\log n)^{-4(d+1)/d}\tag{19}
\]
provided $n\ge N_{d,\sigma/L}$. Additionally when $\Omega$ is a polytope whose number of facets is bounded by a constant depending on $d$ alone, the same inequality holds for $\mathcal F=\mathcal C^B(\Omega)$ i.e.,
\[
\sup_{f\in\mathcal C^B(\Omega)}\mathbb E_f\ell_{\mathbb P}^2(\hat f_n(\mathcal C^B(\Omega)),f)\ge c_d\sigma B n^{-2/d}(\log n)^{-4(d+1)/d}\tag{20}
\]
for $n\ge N_{d,\sigma/B}$.''',r'''For every $\mathfrak L>0$ and $\sigma>0$, there exist constants $C_d$ (depending on $d$ alone) and $N_{d,\sigma/\mathfrak L}$ (depending only on $d$ and $\sigma/\mathfrak L$) such that
\[
\sup_{f\in\mathcal F^{\mathfrak L}(\Omega)}\mathbb E_f\ell_{\mathbb P_n}^2(\hat f_n(\mathcal C(\Omega)),f)\le
\begin{cases}
C_d\mathfrak L^{\frac{2d}{4+d}}\left(\frac{\sigma^2}{n}(\log n)^F\right)^{\frac4{d+4}}&\text{for }d\le3\\
C_4\frac{\sigma\mathfrak L}{\sqrt n}(\log n)^{1+\frac F2}&\text{for }d=4\\
C_d\sigma\mathfrak L\left(\frac{(\log n)^F}{n}\right)^{\frac2d}&\text{for }d\ge5
\end{cases}\tag{21}
\]
for $n\ge N_{d,\sigma/\mathfrak L}$.''',r'''Fix $d\ge5$, $L>0$ and $\sigma>0$. There exist constants $c_d$ and $C_{d,\sigma/L}$ such that
\[
\sup_{f\in\mathcal C_L^L(\Omega)}\mathbb E_f\ell_{\mathbb P_n}^2(\hat f_n(\mathcal C(\Omega)),f)\ge c_d\sigma L n^{-\frac2d}(\log n)^{-\frac{4(d+1)}d}\tag{22}
\]
for $n\ge C_{d,\sigma/L}$.''',r'''For every $k\ge1$ and $h\ge1$, we have
\[
\sup_{f\in\mathcal C_{k,h}(\Omega)}\mathbb E_f\ell_{\mathbb P_n}^2(\hat f_n(\mathcal C(\Omega)),f)\le
\begin{cases}
C_d\sigma^2\left(\frac kn\right)(\log n)^h&\text{for }d=1,2,3\\
C_d\sigma^2\left(\frac kn\right)(\log n)^{h+2}&\text{for }d=4\\
C_d\sigma^2\left(\frac{k(\log n)^h}{n}\right)^{4/d}&\text{for }d\ge5
\end{cases}\tag{23}
\]
for a constant $C_d$ depending on $d$ alone.''',r'''Fix $d\ge5$. There exist positive constants $c_d$ and $N_d$ such that for $n\ge N_d$ and
\[
1\le k\le\min\left(\sqrt n\sigma^{-d/4},c_dn\right),\tag{24}
\]
we have
\[
\mathbb E_{\tilde f_k}\ell_{\mathbb P_n}^2(\hat f_n(\mathcal C(\Omega)),\tilde f_k)\ge c_d\sigma^2\left[\frac kn\right]^{4/d}(\log n)^{-4(d+1)/d}\tag{25}
\]
where $\tilde f_k$ is the function from Lemma 3.2.''',r'''Consider data generated according to the model:
\[
Y_i=f(X_i)+\xi_i\qquad\text{for }i=1,\ldots,n
\]
where $X_1,\ldots,X_n$ are fixed deterministic design points in a convex body $\mathcal X\subseteq\mathbb R^d$, $f$ belongs to a convex class of functions $\mathcal F$ and $\xi_1,\ldots,\xi_n\overset{\mathrm{i.i.d}}\sim N(0,\sigma^2)$. Consider the LSE $\hat f_n(\mathcal F)$ defined in (2). Define
\[
t_f(\mathcal F):=\operatorname*{argmax}_{t\ge0}H_f(t,\mathcal F)
\]
where
\[
H_f(t,\mathcal F):=\mathbb E\sup_{g\in\mathcal F:\ell_{\mathbb P_n}(f,g)\le t}\frac1n\sum_{i=1}^n\xi_i(g(X_i)-f(X_i))-\frac{t^2}2.
\]
Then $H_f(\cdot,\mathcal F)$ is a concave function on $[0,\infty)$, $t_f(\mathcal F)$ is unique and the following pair of inequalities hold for positive constants $c$ and $C$:
\[
\mathbb P\left\{0.5t_f^2(\mathcal F)\le\ell_{\mathbb P_n}^2(\hat f_n(\mathcal F),f)\le2t_f^2(\mathcal F)\right\}\ge1-6\exp\left(-\frac{cnt_f^2(\mathcal F)}{\sigma^2}\right)\tag{26}
\]
and
\[
0.5t_f^2(\mathcal F)-\frac{C\sigma^2}n\le\mathbb E\ell_{\mathbb P_n}^2(\hat f_n(\mathcal F),f)\le2t_f^2(\mathcal F)+\frac{C\sigma^2}n.\tag{27}
\]
Upper bounds for $t_f(\mathcal F)$ can be obtained via:
\[
t_f(\mathcal F)\le\inf\{t>0:H_f(t,\mathcal F)\le0\}\tag{28}
\]
and lower bounds for $t_f(\mathcal F)$ can be obtained via:
\[
t_f(\mathcal F)\ge t_1\qquad\text{if }0\le t_1<t_0\text{ are such that }H_f(t_1,\mathcal F)\le H_f(t_0,\mathcal F).\tag{29}
\]''',r'''Suppose $\Omega$ is a convex body contained in the unit ball. Let $\tilde f$ be a convex function on $\Omega$ that is bounded by $\Gamma$. For a fixed $1\le p<\infty$ and $t>0$, let
\[
B_p^\Gamma(\tilde f,t,\Omega)=\left\{f\in\mathcal C^\Gamma(\Omega):\int_\Omega|f(x)-\tilde f(x)|^pdx\le t^p\right\}.\tag{42}
\]
Suppose $\Delta_1,\ldots,\Delta_k\subseteq\Omega$ are $d$-simplices with disjoint interiors such that $\tilde f$ is affine on each $\Delta_i$. Then for every $0<\epsilon<\Gamma$ and $t>0$, we have
\[
\log N_{[\,]}(\varepsilon,B_p^\Gamma(\tilde f,t,\Omega),\|\cdot\|_{p,\cup_{i=1}^k\Delta_i})\le C_{d,p}k\left[\log\frac\Gamma\epsilon\right]^{d+1}\left[\frac t\epsilon\right]^{d/2}\tag{43}
\]
for a constant $C_{d,p}$ that depends on $p$ and $d$ alone. The left hand side above denotes bracketing entropy with respect to $L_p$ metric on $\Delta_1\cup\cdots\cup\Delta_k$.''',r'''Suppose $\Omega$ is of the form (14) and satisfies (3). There exists $c_{d,p}$ depending only on $d$ and $p$ such that for every $\epsilon>0$ and $t>0$,
\[
\log N(\epsilon,\{f\in\mathcal C(\Omega):\ell_{\mathcal S}(f,\Omega,p)\le t\},\ell_{\mathcal S}(\cdot,\Omega,p))\le[c_{d,p}\log(1/\delta)]^F\left[\frac t\epsilon\right]^{d/2}.\tag{52}
\]''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' (Chatterjee)' if n=='4.1' else ''),source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,p,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Convex regression in multidimensions: Suboptimality of least squares estimators',authors=['Gil Kur','Fuchang Gao','Adityanand Guntuboyina','Bodhisattva Sen'],version='arXiv:2006.02044v2, stamped 3 Sep 2024',pdf_pages=67,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=24,main_text_boundary=dict(location='Section5.6, Acknowledgments and Funding end on PDF page24, with NSF Grant DMS-1712822. The outline places Appendix A (Proofs of Minimax Rates for Convex Regression) on25. Appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Independent CMBX10 theorem-heading enumeration over all24 main-text pages; visual comparison of eight complete theorem statements. Include Theorems4.1,4.5,4.11 in the proof-sketch section, exclude Lemmas/Propositions, citations and prose references.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v2 PDF, pinned by SHA256; main text through24; appendices excluded.',normalization_policy='Preserve original wording, displayed cases, quantifiers, constants and equation labels. Normalize line wrapping and mathematical typesetting only. Distinguish fraktur L in3.3 from Lipschitz L; retain3.1 branches,3.6 k restriction, all4.1 equations26–29 and both epsilon glyphs in4.5.'),papers=[paper],claims=cs)
def main():
    p=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved eight original main-text Theorems; independent inventory review remains separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);a=parser.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
