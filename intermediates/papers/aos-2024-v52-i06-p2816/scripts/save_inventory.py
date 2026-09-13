"""Reproduce both original main-text Theorems from the registered p2816 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2816'
SHA='5a2d2dd02ebd28b8db0afa09bcca352dc259d4281354abf8ac16f68111291cd2'
URL='https://arxiv.org/pdf/2303.12613v1'
NUMBERS=['1','2']
LABELS=['Theorem 1 (General minimax upper bound)','Theorem 2 (Lower bound)']
STATEMENTS=[r'''The minimax risk is upper bounded as
\[
\mathfrak M(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c)\le\Phi(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c).\tag{6}
\]''',r'''The minimax risk is lower bounded as
\[
\mathfrak M(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c)\ge\Phi(T,\mathbb P,\Sigma_w,\tfrac\varrho2,K_e,K_c)\ge\frac14\Phi(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c).\tag{7}
\]''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label=l,source_order=i,statement_original=s,evidence=[dict(page=8,location=l+' — complete original statement')]) for i,(n,l,s) in enumerate(zip(NUMBERS,LABELS,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Noisy recovery from random linear observations: Sharp minimax rates under elliptical constraints',authors=['Reese Pathak','Martin J. Wainwright','Lin Xiao'],version='arXiv:2303.12613v1, stamped 22 Mar 2023',pdf_pages=53,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=32,main_text_boundary=dict(location='Section5.1.2 and Figure2 conclude on PDF page32, followed by Acknowledgements ending with the UC Berkeley AI Research (BAIR) Commons initiative. The outline places Appendix A (Proofs from Section2) on33; all appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Independently enumerate actual bold SFBX1095 theorem headings over all32 main-text pages; visually compare both full statements on8. Citations, proof headings, Propositions, Corollaries and Lemmas are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv2303.12613v1 PDF pinned by SHA256. Main text through32; appendix bodies excluded.',normalization_policy='Original complete theorem wording, argument order, radius halving and constant1/4 preserved. Normalize line wrapping and mathematical typesetting only; keep source assumptions and definitions separately.'),papers=[paper],claims=cs)
def main():
    p=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved both complete main-text Theorems; independent review remains separate.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path);a=ap.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
