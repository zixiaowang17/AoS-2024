"""Reproduce all eight complete main-text Theorems from the registered Gaussian approximation PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2293'
SHA='504e0a5bbb366e23bc01b4264674f851a547786f4601c4101495940434e53293'
URL='https://arxiv.org/pdf/2408.02913v2'
NUMBERS=['2.1','2.2','2.3','2.4','2.5','3.1','3.2','4.1']
STATEMENTS=[r'''Let $(X_i)_{1\le i\le n}$ be independent but possibly not identically distributed random variables with $\mathbb E(X_i)=0$ and for a $p>2$, $\max_{1\le i\le n}\|X_i\|_p=O(1)$, and there exists $\gamma\ge2$ such that
\[
\sum_{i=1}^n\mathbb E[\min\{|X_i|^\gamma/n^{\gamma/p},|X_i|^2/n^{2/p}\}]=o(1).
\]
(2.1)
Then, there exists a Brownian motion $\mathbb B(\cdot)$, such that the following holds
\[
\max_{1\le i\le n}|S_i-\mathbb B(\mathbb E(S_i^2))|=o_{\mathbb P}(n^{1/p}).
\]
(2.2)''',r'''Let $p>2$. For the process $(X_t)_t$, assume Conditions 2.2, 2.3, and 2.1 with
\[
A>A_0:=\max\left\{\frac{p^2-p-2+(p-2)\sqrt{p^2+10p+1}}{4p},1\right\}.
\]
(2.7)
Then there exists a Gaussian process $Y_t$ with $\operatorname{Cov}(X_s,X_t)=\operatorname{Cov}(Y_s,Y_t)$, such that
\[
\max_{1\le i\le n}\left|S_i-\sum_{j=1}^iY_j\right|=o_{\mathbb P}(n^{1/p}\sqrt{\log n}).
\]
(2.8)
In fact, there also exists a Gaussian process $Y_t^\oplus$, with $\operatorname{Cov}(Y_s^\oplus,Y_t^\oplus)=\operatorname{Cov}(X_s^\oplus,X_t^\oplus)$, such that
\[
\max_{1\le i\le n}\left|S_i-\sum_{j=1}^iY_j^\oplus\right|=o_{\mathbb P}(n^{1/p}).
\]
(2.9)''',r'''Assume the process $(X_t)_{t\ge1}$ satisfies Conditions 2.2, 2.4 and 2.1 with
\[
A>A'_0:=\max\left\{\frac{p^2-4+(p-2)\sqrt{p^2+20p+4}}{8p},1\right\}.
\]
(2.10)
Then, there exists a Gaussian process $(Y_t)$ with $\operatorname{Cov}(Y_s,Y_t):=\operatorname{Cov}(X_s,X_t)$, such that
\[
\max_{1\le i\le n}\left|S_i-\sum_{j=1}^iY_j\right|=o_{\mathbb P}(n^{1/p}).
\]
(2.11)''',r'''For the process $(X_t)_{t\ge1}$, assume Conditions 2.2 and 2.1 with $A>A_0$; see (2.7). Then there exists a Brownian motion $\mathbb B(\cdot)$, such that
\[
\max_{1\le j\le n}|S_j-\mathbb B(\mathbb E(S_j^{\oplus2}))|=o_{\mathbb P}(n^{1/p}).
\]
(2.12)
Further, it holds that
\[
\max_{1\le j\le n}|S_j-\mathbb B(\mathbb E(S_j^2))|=o_{\mathbb P}(n^{1/p}\sqrt{\log n}).
\]
(2.13)''',r'''Under conditions of Theorem 2.3, there exists a Brownian motion $\mathbb B(\cdot)$ such that
\[
\max_{1\le j\le n}|S_j-\mathbb B(\mathbb E(S_j^2))|=o_{\mathbb P}(n^{1/p}).
\]
(2.14)''',r'''Let $p>2$. Assume Condition 2.1 holds for $\Theta_{i,p}$. Let $Q_n=\sum_{1\le s\le t\le n}a_{s,t}X_sX_t$, with $a_{s,t}=0$ if $|s-t|>D_n$ for some $D_n\le n$, and $\sup|a_{s,t}|\le1$. Denote
\[
R_k=\sum_{j=1}^k(V_j-\mathbb E(V_j)),\quad\text{where}\quad V_k=\sum_{t=(k-1)D_n+1}^{(kD_n)\wedge n}\sum_{1\le s\le t}a_{s,t}X_sX_t,\quad\text{for }1\le k\le\lceil n/D_n\rceil.
\]
(3.3)
Then there exists constants $C_p$, depending only on $p$, such that for all $x>0$,
\[
\mathbb P\left(\max_{1\le k\le\lceil n/D_n\rceil}|R_k|\ge x\right)\le\begin{cases}
C_px^{-p/2}nD_n^{p/4}\mu_{p,A}^p,&2<p\le4,\\
C_px^{-p/2}nD_n^{p/2-1}\mu_{p,A}^p+C_p\exp\left(-\frac{C_px^2}{nD_n\mu_{4,A}^4}\right),&p>4.
\end{cases}
\]
(3.4)''',r'''Let $p>2$. Assume that the decay Condition 2.1 holds with $A>1$. Further grant the truncated uniform integrability Condition 2.2. Then there exists a Brownian motion $\mathbb B(\cdot)$ such that
\[
\max_{1\le j\le n}|S_j-\mathbb B(\mathbb E(S_j^2))|=o_{\mathbb P}(n^{(1-A\zeta_1)/2}\sqrt{\log n}).
\]
(3.11)''',r'''Assume $\mu,f\in C^3[0,1]$ and, for some constants $C_1,C_2>0$, $C_1\le f(t)\le C_2$ for all $t\in[0,1]$. Then under the assumptions of Theorem 2.4 for $Z_i$, there exists Brownian motion $\mathbb B(\cdot)$ such that with $Q_{h_n}(t)=\sum_{i=1}^nw_{h_n}(t,i)Y_i$, where $Y_i=\mathbb B(\mathbb E(S_i^2))-\mathbb B(\mathbb E(S_{i-1}^2))$, the following is true:
\[
\sup_{t\in[\omega h_n,1-\omega h_n]}|\widehat\mu_{h_n}(t)-\mu(t)-h_n^2\beta\mu''(t)-Q_{h_n}(t)|=o_{\mathbb P}(h_n^{-1}n^{1/p-1}\sqrt{\log n}),
\]
(4.10)
for any $h_n\to0$ satisfying $h_n^4=O(n^{1/p-1})$ and $nh_n\to\infty$ with $\beta=\int u^2K(u)\,du/2$.''']
def inventory():
    pages=[5,7,7,8,8,11,13,15]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='Gaussian approximation for nonstationary time series with optimal rate and explicit construction',authors=['Soham Bonnerjee','Sayar Karmakar','Wei Biao Wu'],version='arXiv:2408.02913v2; 7 Aug 2024',pdf_pages=60,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=21,main_text_boundary=dict(location='Section 7 and Acknowledgments end on PDF page 21 before SUPPLEMENTARY MATERIAL at y=422.68. Page-21 evidence clipped at y=416; supplementary and appendix bodies excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate every actual small-cap THEOREM heading in all main-text pages; eight environments including the independent-variable result T2.1. Exclude proof headings, citations, Propositions, Remarks and Conditions.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v2; appendix bodies excluded.',normalization_policy='Preserve original wording, assumptions, full formulas, both truncation branches and both moment ranges. Normalize line wrapping and mathematical typesetting. T2.2 second branch still compares the original S_i, not S_i^oplus.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all eight complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
