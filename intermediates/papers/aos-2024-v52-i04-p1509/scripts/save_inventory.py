"""Regenerate the complete main-text theorem inventory from the saved transcription."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1509'
SHA='41ad2b881f250cc5e8ef27156d744623d49c3461ab82e6a8733ab84734e1a476'
claims=[dict(claim_id=PID+'/T1',paper_id=PID,claim_kind='theorem',label='Theorem 1',source_order=1,statement_original=r'''Suppose Assumptions A, B, and C are satisfied. Then (2) and (7) hold, and
\[
\sup_{t\in\mathbb R}\left|\mathbb P_n^*\left[\widetilde\theta_n^*(\mathsf x)-\widehat\theta_n(\mathsf x)\le t\right]-\mathbb P\left[\widehat\theta_n(\mathsf x)-\theta_0(\mathsf x)\le t\right]\right|=o_{\mathbb P}(1).\tag{8}
\]''',evidence=[dict(page=9,location='Theorem 1, complete original body ending at equation (8)')])]
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Bootstrap-assisted inference for generalized Grenander-type estimators',authors=['Matias D. Cattaneo','Michael Jansson','Kenichi Nagasawa'],version='arXiv:2303.13598v3, 4 July 2024',source_url='https://arxiv.org/pdf/2303.13598v3',pdf_pages=66,pdf_sha256=SHA,main_text_last_pdf_page=20,main_text_boundary=dict(location='Main text ends with the simulation discussion on PDF page 20, before APPENDIX A: TECHNICAL RESULTS AND OMITTED DETAILS at y=671.2371826171875 PDF points. The appendix and following supplement are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[PID+'/T1'],zero_theorems_confirmed=False))
    data=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified registered arXiv v3 PDF; pages 1-19 and page 20 above Appendix A only.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
