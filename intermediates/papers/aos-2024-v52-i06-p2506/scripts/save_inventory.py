"""Reproduce four complete main-text Theorems from the registered arXiv v4 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2506'
SHA='500239b27bec9a744424a489d3c785ccdf3d463606c209d50e010d8ce2add2b6'
URL='https://arxiv.org/pdf/2206.13668v4'
NUMBERS=['5.3','5.5','5.10','5.14']
STATEMENTS=[r'''Let $T\in S^r(\mathbb R^d)$ for $r\ge3$ be a diagonal tensor satisfying
\[
T_{i\cdots i}\ne0\qquad\text{for at least }d-1\text{ different values of }i=1,\ldots,d.
\]
(13)
Then $Q\bullet T\in\mathcal V^{\mathrm{diag}}$ if and only if $Q\in\operatorname{SP}(d)$, i.e. $\mathcal G_T(\mathcal V^{\mathrm{diag}})=\operatorname{SP}(d)$. If $r=2$, the same conclusion holds under a stronger condition that $T_{jj}\ne T_{kk}$ for $j\ne k$.''',r'''Consider the model (1) with $\mathbb E\varepsilon=0$, $\operatorname{var}(\varepsilon)=I_d$ and suppose that for some $r\ge3$ the tensor $h_r(\varepsilon)$ is diagonal with at most one zero on the diagonal. Then $A$ in (1) is identifiable up to permuting and swapping signs of its rows.''',r'''Suppose that $T\in S^r(\mathbb R^d)$ for an even $r$ is a reflectionally invariant tensor. Let $l=(r-2)/2$ and suppose, in addition, that $T$ satisfies
\[
\sum_{i_1,\ldots,i_l}T_{i_1i_1\cdots i_li_ljj}\ne\sum_{i_1,\ldots,i_l}T_{i_1i_1\cdots i_li_lkk}\qquad\text{for all }j\ne k.
\]
(14)
Then $Q\bullet T\in\mathcal V^{\mathrm{refl}}$ if and only if $Q\in\operatorname{SP}(d)$, i.e. $\mathcal G_T(\mathcal V^{\mathrm{refl}})=\operatorname{SP}(d)$.''',r'''Consider the model (1) with $\mathbb E\varepsilon=0$, $\operatorname{var}(\varepsilon)=I_d$ and suppose that for some even $r$ the tensor $h_r(\varepsilon)$ is reflectionally invariant and it satisfies the genericity condition (14). Then $A$ is identifiable up to permuting and swapping signs of its rows.''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,[9,9,11,12]),1)]
    paper=dict(paper_id=PID,title='Non-independent components analysis',authors=['Geert Mesters','Piotr Zwiernik'],version='arXiv:2206.13668v4, marked 19 Mar 2024',pdf_pages=53,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=21,main_text_boundary=dict(location='Discussion and acknowledgements end on PDF page21 before REFERENCES at y=580.205. Main-text evidence is clipped at y=572. This page is shared with references, not an appendix; appendix and supplementary bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Independently enumerate actual small-cap THEOREM environments on pages1–21, clipping the final page before references. Exactly5.3,5.5,5.10,5.14 in source order. Main-text Corollary5.15 and propositions, lemmas, remarks, citations and proof headings are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v4 PDF pinned by SHA-256; main-text only, ending before references and excluding appendices/supplementary bodies.',normalization_policy='Preserve original complete theorem bodies and all branches. Normalize wrapping and typesetting only. Keep the r=2 branch in5.3, the even-r and repeated-index sums in5.10, and both original sign/permutation identification conclusions. Preserve the source title components (plural), though the corpus title uses component.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all four complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
