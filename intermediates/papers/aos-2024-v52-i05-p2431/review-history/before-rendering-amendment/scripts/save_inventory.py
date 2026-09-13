"""Reproduce all five main-text Theorems from the registered multi-layer SBM PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2431'
SHA='729249562a67503fcb0c40a36bb63f3f77cf9224ca014d3b04b04e24ffcd5ae8'
URL='https://arxiv.org/pdf/2311.07773v1'
NUMBERS=['2.2','3.1','3.3','4.1','4.2']
STATEMENTS=[r'''Let $T_n=n^a$, $\rho_n=n^{-b}$ for some $a>0$, $b\in(0,2)$. Then
- without computational constraints, the MLSBM is recoverable if $1+a-b>0$; and is not recoverable by any algorithm if $1+a-b<0$.
- assuming the low-degree polynomial conjecture, the MLSBM is recoverable using a polynomial-time algorithm if $1+a/2-b>0$, and not recoverable by any polynomial-time algorithm if $1+a/2-b<0$.
The above results also hold for detection.''',r'''If $nT_n^{1/2}\rho_n\ge C\sqrt{\log(n)}$ for some absolute constant $C>0$, then MLSBM sequence $(P_{1,n}:n\ge1)$ specified in Definition 1 is asymptotically recoverable by a polynomial-time algorithm.''',r'''Assuming the low-degree polynomial conjecture Conjecture 3.2, the MLSBM sequences $(P_{1,n},P_{0,n})$ specified in Definition 1 with $\rho_n$ satisfying Assumption 1 are not distinguishable by any polynomial-time algorithm if $nT_n^{1/2}\rho_n\le(1/2)(\log n)^{-1.4}$ for all $n$ large enough.''',r'''When $nT_n\rho_n\to0$, we have
\[
d_{\chi^2}(P_{1,\tau,n},P_{0,n})=\sum_A P_{1,\tau,n}^2(A)/P_{0,n}(A)-1=o(1),\qquad\forall\tau\in\mathcal S_{T_n}.
\]
As a result,
\[
d_{\chi^2}(P_{1,n},P_{0,n})=o(1)
\]
and $P_{1,n},P_{0,n}$ are indistinguishable.''',r'''Let $P_{1,n}$ be the sequence of MLSBM defined in Definition 1 with $(T_n,\rho_n)$ satisfying Assumption 1. If $nT_n\rho_n\to\infty$, then for any $\epsilon>0$
\[
\lim_{n\to\infty}P_{1,n}(\ell_n(\widehat\sigma_{\mathrm{mle}},\sigma)\ge\epsilon)=0,
\]
where $\ell_n(\cdot,\cdot)$ is the Hamming loss function defined in Definition 2. In other words, $P_{1,n}$ is asymptotically recoverable and hence distinguishable from $P_{0,n}$.''']
def inventory():
    pages=[6,7,8,10,11]
    titles=['Simplified main result','Computational upper bound [28]','Computational lower bound','Detection lower bound in MLSBM',None]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' ('+title+')' if title else ''),source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,s,p,title) in enumerate(zip(NUMBERS,STATEMENTS,pages,titles),1)]
    paper=dict(paper_id=PID,title='Computational and statistical thresholds in multi-layer stochastic block models',authors=['Jing Lei','Anru R. Zhang','Zihan Zhu'],version='arXiv:2311.07773v1; 13 Nov 2023; cover dated 15 Nov 2023',pdf_pages=31,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=12,main_text_boundary=dict(location='Discussion and Acknowledgement end on PDF page12. Appendix A, Proofs for Section2, begins at y=466.815. Main-text evidence is clipped at y=458 on the shared page; appendix bodies excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate bold Theorem headings in main-text pages1–12, clipping the shared last page before AppendixA. Five labels2.2,3.1,3.3,4.1,4.2; include the simplified and credited results. Conjecture3.2 is not a Theorem. Preserve both T2.2 bullets and all T4.1 conclusions.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v1; appendix bodies excluded.',normalization_policy='Preserve original wording and formulas, including conditional computational claims, exact log exponents and joint/marginal notation. Normalize wrapping and typesetting only; record source ambiguities separately.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all five complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
