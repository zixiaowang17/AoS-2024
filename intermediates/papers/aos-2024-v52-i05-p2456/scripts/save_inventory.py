"""Reproduce all three main-text Theorems from the registered IMS manuscript."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2456'
SHA='0b228ac43be500b5f08a806750371daddeedccc07b2e8fd00d170782cc0d5144'
URL='https://www.e-publications.org/ims/submission/AOS/user/submissionFile/63223?confirm=1e325b16'
NUMBERS=['4.1','4.3','4.4']
STATEMENTS=[r'''Let Assumption A hold. Then, $S_n\Longrightarrow S_\infty$.''',r'''Under Assumption B and $H_0$, in $\mathcal H_K^*$,
\[
\widehat R_n\Longrightarrow R_\infty,
\]
where $R_\infty(a)=\sum_{j=1}^\infty\lambda_j\langle\varphi_j,\Pi a\rangle_{K^\perp}U_j$. Thus, under these conditions $n\widehat Q_K^\perp\xrightarrow{d}\sum_{j=1}^\infty\lambda_jU_j^2$.''',r'''Under Assumption B, $\|\widehat R_n^*\|^2\xrightarrow{d}\|R_\infty\|^2$ a.s.''']
def inventory():
    pages=[11,12,13]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement; manuscript line numbers omitted')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='A Gaussian process approach to model checks',authors=['Juan Carlos Escanciano'],version='IMS manuscript AOS2401-003R2A0.pdf; marked Submitted to the Annals of Statistics',pdf_pages=25,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=20,main_text_boundary=dict(location='The discussion ends on PDF page20 at manuscript line639. APPENDIX: MATHEMATICAL PROOFS starts at y=223.09; main-text evidence is clipped at y=216 on the shared page. Appendix bodies excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate actual small-cap THEOREM environments in main-text pages1–20, clipping the shared final page before the appendix. Three labels4.1,4.3,4.4. Proposition4.2 and Proposition4.5 are excluded from the theorem inventory; references and proof headings are not environments.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified IMS manuscript; appendix bodies excluded.',normalization_policy='Preserve original wording and all mathematical content. Remove manuscript line numbers and normalize wrapping/typesetting only. Preserve lambda_j rather than sqrt(lambda_j) in the source R_infinity formula and the absence of H0 in Theorem4.4. AssumptionB(v), introduced after these theorems, is not retroactively inserted.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all three complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
