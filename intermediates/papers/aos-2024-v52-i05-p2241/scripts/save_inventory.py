"""Reproduce every complete main-text Theorem in the registered p/e-variable paper."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2241'
SHA='4ab8ada786411ce1154b0662e6821f938f1280465ef3cb5f670cebff8429b8ba'
URL='https://arxiv.org/pdf/2305.16539v4'
NUMBERS=['3.1','3.4','4.2','4.4','4.7','4.9','5.3','5.5','6.1','6.2','6.7']
STATEMENTS=[r'''Suppose that we are testing $\mathcal P=\{P_1,\ldots,P_L\}$ against $\mathcal Q=\{Q\}$ and (JA) holds. The following are equivalent:
(a) there exists an exact (hence pivotal) and nontrivial p-variable;
(b) there exists a pivotal, exact, bounded e-variable that has nontrivial e-power against $Q$;
(c) there exists an exact e-variable that is nontrivial against $Q$;
(d) there exists a random variable $X$ that is pivotal for $\mathcal P$ but has a different distribution under $Q$, where the laws of $X$ under both are atomless;
(e) it holds that $Q\notin\operatorname{Span}(P_1,\ldots,P_L)$.''',r'''Suppose that we are testing $\mathcal P=\{P_1,\ldots,P_L\}$ against $\mathcal Q=\{Q\}$ and (JA) holds. The following are equivalent:
(a) there exists a nontrivial p-variable;
(b) there exists a bounded e-variable that has nontrivial e-power against $Q$;
(c) there exists an e-variable that is nontrivial for $Q$;
(d) it holds that $Q\notin\operatorname{Conv}(P_1,\ldots,P_L)$.''',r'''Assume (JA) and (AC). There exists a maximizer $X$ to (3) of the form $X=(dG/dF)(Y)$, where $F,G\in\Pi(\mathbb R)$, and $Y\in\mathcal T((P_1,\ldots,P_L,Q),(F,\ldots,F,G))$.''',r'''Assuming (N), the following are equivalent.
(a) There exists a unique maximum element $\mu$ in convex order in $\mathcal M_\gamma$, i.e., $\mu\preceq_{\mathrm{cx}}\gamma$ and for each $\nu$ supported on $\mathcal I^+$ with $\nu\preceq_{\mathrm{cx}}\gamma$, it holds that $\nu\preceq_{\mathrm{cx}}\mu$.
(b) The class of measures $\{\mu_x\}_{x\ge0}$ from Proposition 4.3 is monotone (in the usual order), i.e., for all $x\le y$, $\mu_x\le\mu_y$.''',r'''Assume (N), (JA), (AC). Suppose that there exists a convex set $\Gamma\subseteq\mathbb R^2$ such that $\gamma(\partial\Gamma)=1$. Then there exists a unique maximum element $\mu$ in convex order in $\mathcal M_\gamma$. Moreover, $\mu$ is the unique probability measure on the $\mathcal I_2^+$ with $\mu([0,x]^2)=\mu_x(\mathbb R^2)$, where $\mu_x$ was given in Proposition 4.3 applied with $L=2$. In particular, there exist distinct measures $F,G\in\Pi(\mathbb R)$ such that $(dF/dG,dF/dG)|_G=\mu$, attaining the maximum in (7).''',r'''Suppose that $\mathcal X$ is an Euclidean space and $P_1,\ldots,P_L$ are distinct probability measures on $\mathcal X$. If $Q\in\Pi(\mathcal X)$ satisfies $Q\notin\mathcal P=\{P_1,\ldots,P_L\}$, then there exists $k\ge1$ such that $Q^k\notin\operatorname{Span}\mathcal P^k$ (and in particular $Q^k\notin\operatorname{Conv}\mathcal P^k$). Moreover, if we also assume that $Q$ satisfies (AC) and that $P_1,\ldots,P_L$ are linearly independent, then either $Q\notin\operatorname{Span}\mathcal P$ or $Q^2\notin\operatorname{Span}\mathcal P^2$ (or both); in particular, either $Q\notin\operatorname{Conv}\mathcal P$ or $Q^2\notin\operatorname{Conv}\mathcal P^2$ (or both).''',r'''Assume (JA) and (AC). For any $s$, we have $\mu^{(s)}\preceq_{\mathrm{cx}}\mu^{(s+1)}$, and if $\mu^{(s)}\ne\mu^{(s+1)}$, then the inequality is strict, meaning that the above SHINE construction makes progress at each step. Further, assuming (N), it produces a sequence of measures that converges almost surely to a maximal element $\mu$ in convex order in $\mathcal M_\gamma$. In this case, if there exists a maximum element $\mu_0$, then the output of our SHINE construction converges to $\mu_0$.''',r'''Assume the same conditions as in Theorem 5.3. Suppose that there exists $\varepsilon>0$ such that
\[
\mathbb E^Q\left[\left(\frac{dP_j}{dQ}\right)^{2+\varepsilon}\right]<\infty,\quad\text{for some }j,
\]
(14)
and
\[
\mathbb E^Q\left[\left(\frac{dP_{j'}}{dQ}\right)^{-2}\right]<\infty,\quad\text{for some }j'.
\]
(15)
Consider the e-power $\mathrm{EP}_k:=\mathbb E^Q[-\log X_k]$ where $\{X_k\}$ is the SHINE martingale. Then there exist $r\in(0,1)$ and $C>0$ such that
\[
\mathrm{EP}_\infty-\mathrm{EP}_k\le Cr^k,
\]
where $\mathrm{EP}_\infty=\mathbb E[-\log X_\infty]$ and $X_k\to X_\infty$ a.s.''',r'''Assume (JA). Suppose that we are testing $\mathcal P=\{P_1,\ldots,P_L\}$ against $\mathcal Q=\{Q_1,\ldots,Q_M\}$. The following are equivalent:
(a) there exists an exact (hence pivotal) and nontrivial p-variable;
(b) there exists a pivotal, exact, bounded e-variable that has nontrivial e-power against $\mathcal Q$;
(c) there exists an exact e-variable that is nontrivial for $\mathcal Q$;
(d) there exists a random variable $X$ that is pivotal for $\mathcal P$ and satisfies $F\notin\operatorname{Conv}(G_1,\ldots,G_M)$, where $F$ is the law of $X$ under every $P\in\mathcal P$ and $G_j$ is the law of $X$ under $Q_j$ for $1\le j\le M$;
(e) it holds that $\operatorname{Span}(P_1,\ldots,P_L)\cap\operatorname{Conv}(Q_1,\ldots,Q_M)=\varnothing$.
Furthermore, the equivalence of (c) and (e) does not require (JA).''',r'''Assume (JA). Suppose that we are testing $\mathcal P=\{P_1,\ldots,P_L\}$ against $\mathcal Q=\{Q_1,\ldots,Q_M\}$. The following are equivalent:
(a) there exists a nontrivial p-variable;
(b) there exists a bounded e-variable that has nontrivial e-power against $\mathcal Q$;
(c) there exists an e-variable that is nontrivial for $\mathcal Q$;
(d) it holds that $\operatorname{Conv}(P_1,\ldots,P_L)\cap\operatorname{Conv}(Q_1,\ldots,Q_M)=\varnothing$.
Furthermore, the equivalence of (c) and (d) does not require (JA) or finiteness of $\mathcal P$ and $\mathcal Q$.''',r'''Assume that there exists a common reference measure $R\in\Pi(\mathcal X)$ such that $P\ll R$ for $P\in\mathcal P$ and $Q\ll R$ for $Q\in\mathcal Q$. There exists an exact bounded e-variable $X$ for $\mathcal P$ against $\mathcal Q$ satisfying $\inf_{Q\in\mathcal Q}\mathbb E^Q[\log X]>0$ if and only if $0\notin\overline{\overline{\operatorname{Span}}\mathcal P+\overline{\operatorname{Conv}}\mathcal Q}$, where the closure is taken with respect to the total variation distance. If $\mathcal Q$ is tight, then we have the further equivalence to $\overline{\operatorname{Span}}\mathcal P\cap\overline{\operatorname{Conv}}\mathcal Q=\varnothing$.''']
def inventory():
    pages=[[9],[10],[12],[13],[14],[15],[20],[22],[24],[24,25],[25]]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement') for p in pp]) for i,(n,s,pp) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='On the existence of powerful p-values and e-values for composite hypotheses',authors=['Zhenyuan Zhang','Aaditya Ramdas','Ruodu Wang'],version='arXiv:2305.16539v4; 1 Dec 2024',pdf_pages=47,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Section 8 ends on page 28; acknowledgments end on page 29 before REFERENCES at y=131.57. Page-29 evidence clipped at y=126. Appendices start on page 31 and their bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate every small-cap THEOREM heading in all main-text pages; eleven environments. Exclude proofs, citations, Lemmas, Propositions, Corollaries and Conjectures. Preserve every equivalent clause, qualification and displayed formula.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v4; appendix bodies excluded.',normalization_policy='Preserve original theorem wording and mathematical content, including maximal/maximum, exactness/pivotality, JA exceptions, distinct moment indices and nested closure notation. Normalize line wrapping and mathematical typesetting; footnote callouts are not mathematical assumptions.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all eleven complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
