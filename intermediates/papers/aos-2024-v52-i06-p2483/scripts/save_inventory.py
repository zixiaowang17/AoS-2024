"""Reproduce the two main-text Theorems from the registered arXiv v2 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2483'
SHA='0ab1dbbb8e6dfac13438b613e53a1f216dd2dc2973079864f2cb4549c4438b0e'
URL='https://arxiv.org/pdf/2110.11816v2'
NUMBERS=['1','2']
STATEMENTS=[r'''Suppose
\[
n\min\{q,1-q\}\ge n^{-o(1)},\qquad\rho^2>\alpha,\qquad\omega(1)\le K\le\frac{\log n}{16\log\log n\vee2\log\left(\frac1{n\min\{q,1-q\}}\right)},
\]
(7)
where $\alpha\approx0.33833$ is Otter's constant. Then the testing error satisfies
\[
\mathcal Q(f_{\mathcal T}(A,B)\ge\tau)+\mathcal P(f_{\mathcal T}(A,B)\le\tau)=o(1),
\]
(8)
where the threshold is chosen as
\[
\tau=C\mathbb E_{\mathcal P}[f_{\mathcal T}(A,B)]=C\rho^{2K}|\mathcal T|
\]
for any fixed constant $0<C<1$.''',r'''Suppose (7) holds. Then (8) holds with $\widetilde f_{\mathcal T}$ in place of $f_{\mathcal T}$, namely
\[
\mathcal Q(\widetilde f_{\mathcal T}(A,B)\ge\tau)+\mathcal P(\widetilde f_{\mathcal T}(A,B)\le\tau)=o(1).
\]
(9)
Moreover, $\widetilde f_{\mathcal T}(A,B)$ can be computed in $n^{2+o(1)}$ time.''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,[6,7]),1)]
    paper=dict(paper_id=PID,title='Testing network correlation efficiently via counting trees',authors=['Cheng Mao','Yihong Wu','Jiaming Xu','Sophie H. Yu'],version='arXiv:2110.11816v2, marked 2 Apr 2022; cover dated April 5, 2022',pdf_pages=40,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=22,main_text_boundary=dict(location='Numerical results and acknowledgment end on PDF page22 before Appendix A, Preliminary facts about graphs, at y=574.126. Main-text evidence is clipped at y=565 on this shared page. Appendix bodies are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Use the PDF outline to locate appendices and independently enumerate bold Theorem environments on main-text pages1–22, clipping the shared final page. Exactly Theorem1 on page6 and Theorem2 on page7. Citations, proof headings, propositions, lemmas and the computational hardness conjecture are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v2 PDF pinned by SHA-256; inspect main text only and clip shared final page before AppendixA.',normalization_policy='Preserve complete original theorem wording, formulas, reference numbers and all inequalities. Normalize PDF wrapping and typesetting only. Preserve both non-strict testing-error inequalities, the maximum in the K-bound denominator and the threshold inherited by Theorem2.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved both complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
