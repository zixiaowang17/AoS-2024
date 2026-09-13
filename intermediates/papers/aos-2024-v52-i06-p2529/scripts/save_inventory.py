"""Reproduce three full main-text Theorems from the registered arXiv v2 preprint."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2529'
SHA='6e36d59f35a5f480032c8aa11696cceb10caf17a7d2483519f14b3721bfd245a'
URL='https://arxiv.org/pdf/2010.03832v2'
NUMBERS=['5','8','10']
STATEMENTS=[r'''Let $X_l^*$, $l\in\mathbb N$, be independent copies of a regularly varying $[0,\infty)^d$-valued random vector $X^*$ with index $\alpha=1$ satisfying Eq. (3) and with spectral component denoted by $\Theta$. Furthermore, let $u_n\to\infty$ such that $n/a^*(u_n)\to\infty$. Then, for every finite set $K_0\subset\mathbb N_0$ and $\delta\ge0$, the sequence of processes $\bigl(\{G_n(v,s,\beta,p);v\in\partial B_1^+(0),(s,\beta)\in A'_\delta,p\in K_0\}\bigr)_{n\in\mathbb N}$ with
\[
G_n(v,s,\beta,p)=\sqrt{\frac n{a^*(u_n)}}\left[a^*(u_n)\widehat M_{n,u_n}(v,s,\beta,p)-a^*(u_n)\mathbb E[\widehat M_{n,u_n}(v,s,\beta,p)]\right]
\]
(24)
converges weakly in $\ell^\infty(\partial B_1^+(0)\times A'_\delta\times K_0)$ to a tight centered Gaussian process $G$ with covariance
\[
\operatorname{Cov}(G(v,s,\beta,p_1),G(w,t,\gamma,p_2))
=\tau\mathbb E\left[\left(v^\top\frac{(Ys\circ\Theta)^{1/\beta}}{\|(Ys\circ\Theta)^{1/\beta}\|}\right)^{p_1}\left(w^\top\frac{(Yt\circ\Theta)^{1/\gamma}}{\|(Yt\circ\Theta)^{1/\gamma}\|}\right)^{p_2}\mathbf1\{Y(\|s\circ\Theta\|\wedge\|t\circ\Theta\|)>1\}\right].
\]
(25)''',r'''Let $X_l$, $l\in\mathbb N$, be independent copies of a non-standard regularly varying $[0,\infty)^d$-valued random vector $X$. Assume that the vector $X^*=(r_1^{-1}X_1^\alpha,\ldots,r_d^{-1}X_d^\alpha)$ satisfies Eq. (3) and (30). Let $\{k_n\}_{n\in\mathbb N}\subset\mathbb N$ be a sequence such that $k_n\to\infty$, $k_n/n\to0$ and $\sqrt{k_n}A_i^*(n/k_n)\to0$ for all $1\le i\le d$. Then we have
\[
\sqrt{k_n}\left(\widehat\alpha_{n,k_n}^{-1}-\alpha^{-1}\right)\xrightarrow{d}\widetilde H,\qquad n\to\infty,
\]
where $\widetilde H$ is a $d$-dimensional centered Gaussian random vector with covariances
\[
\operatorname{Cov}(\widetilde H_i,\widetilde H_j)=\frac\tau{\alpha_i\alpha_j}\mathbb E[\Theta_i\wedge\Theta_j]=\frac{2-\tau_{ij}}{\alpha_i\alpha_j}.
\]''',r'''Let $X_l$, $l\in\mathbb N$, be independent copies of a non-standard regularly varying $[0,\infty)^d$-valued random vector $X$ satisfying the assumptions of Cor. 6 and Thm. 8 for $a^*(u_n)\sim n/k_n$, some $\delta>0$ and some $K\subset\mathbb N$. Assume that all the partial derivatives
\[
c_{s_i}(v,s,\beta,p)=\frac\partial{\partial s_i}c(v,s,\beta,p),\qquad i\in\{1,\ldots,d\},p\in K,
\]
\[
c_{\beta_i}(v,s,\beta,p)=\frac\partial{\partial\beta_i}c(v,s,\beta,p),\qquad i\in\{1,\ldots,d\},p\in K,
\]
exist and are continuous on $\partial B_1^+(0)\times A'_\delta$. Then, for non-empty $I\subset\{1,\ldots,d\}$, we have
\[
\left\{\sqrt{k}\left(\frac{\widetilde M_{n,k,I}(v_I,p)}{\widetilde P_{n,k,I}}-c(v_I,\mathbf1_I,\mathbf1,p)\right);v\in\partial B_1^+(0),p\in K\right\}
\longrightarrow\left\{\widetilde G(v_I,\mathbf1_I,\mathbf1,p)-\sum_{i\in I}\left(c_{s_i}(v_I,\mathbf1_I,\mathbf1,p)G^0(\mathbf1_{\{i\}})+c_{\beta_i}(v_I,\mathbf1_I,\mathbf1,p)\alpha_i\widetilde H_i\right)\right\}
\]
weakly in $\ell^\infty(\partial B_1^+(0)\times K)$ as $n\to\infty$.''']
def inventory():
    ps=[[7,8],[10],[11]]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — '+('beginning of original statement' if n=='5' and p==7 else 'continuation, process and full covariance' if n=='5' else 'complete original statement')) for p in pages]) for i,(n,s,pages) in enumerate(zip(NUMBERS,STATEMENTS,ps),1)]
    paper=dict(paper_id=PID,title='Estimation of the spectral measure from convex combinations of regularly varying random vectors',authors=['Marco Oesting','Olivier Wintenberger'],version='arXiv:2010.03832v2, marked 3 Jul 2024; preprint dated July 4, 2024',pdf_pages=39,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=25,main_text_boundary=dict(location='Conclusion and acknowledgements end on PDF page25 before References at y=527.295. Evidence is clipped at y=520. The page is shared with references, not an appendix. Appendix A begins on page26; appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Use the PDF outline to locate the appendices; independently enumerate bold Theorem headings in main-text pages1–25, clipping before references. Exactly Theorem5 on pages7–8, Theorem8 on page10 and Theorem10 on page11. Corollary6, propositions, lemmas, remarks, citations and appendix proof headings are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v2 PDF pinned by SHA-256; main-text only, excluding appendices and clipping before references.',normalization_policy='Preserve full original theorem wording, processes, covariance formulas and assumption references. Normalize wrapping/typesetting only. Keep expectation centering in5, the unindexed alpha exponents printed in8, and the k notation and reference to Corollary6 in10. No silent repair of surrounding source definitions.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all three complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
