"""Reproduce both original main-text Theorems of the registered arXiv v3 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2059'
SHA='dcfc8fb8000dbbaf89536ce13c4ce35739ef253fa73e5aed1baef4bd6cc5dcbf'
URL='https://arxiv.org/pdf/2309.05482v3'
NUMBERS=['3.3','4.4']
STATEMENTS=[r'''Let $\pi_1,\ldots,\pi_B$ be $B$ uniformly random permutations of $[n]$, and $T(.,.;x,Z,\varepsilon)$ be a bi-variate function satisfying condition 3.1. Under the null hypothesis $H_0$, construct paired statistics $(T_{0b},T_{b0})$ as
\[
T_{0b}=T(\pi_0,\pi_b;x,Z,\varepsilon),\qquad T_{b0}=T(\pi_b,\pi_0;x,Z,\varepsilon).
\]
Substituting these into Algorithm 1, we obtain $\mathbb P_{H_0}[p_{val}\leq\alpha]<2\alpha$ for all $\alpha>0$, where the probability is marginalized over both noise and permutation randomness.''',r'''The confidence interval constructed by Algorithm 2 corresponds to the $\mathrm{CI}_\alpha$ defined in Lemma 4.1, and guarantees a worst-case coverage of $(1-2\alpha)$ for a specified mis-coverage level $\alpha$.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,[9,12]),1)]
    paper=dict(paper_id=PID,title='A conformal test of linear models via permutation-augmented regressions',authors=['Leying Guan'],version='arXiv:2309.05482v3; 27 Dec 2023',pdf_pages=36,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=28,main_text_boundary=dict(location='Section 8 Discussions continues onto PDF page 28, followed by Acknowledgment and Funding. Page-28 evidence is clipped at y=478, above References at y=485.5. Appendix A Proofs starts on page 31; no appendix material is used in the census.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate actual bold Theorem environments on pages 1-27 and the main-text prefix of page 28; visually compare both complete statements. Corollary 4.1, Lemma 4.3, Propositions, Remarks and proof headings are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v3 PDF; no replacement source and no appendix material.',normalization_policy='Preserve complete original statements, including the printed Lemma 4.1 reference in Theorem 4.4. Normalize PDF line wrapping and mathematical typesetting only.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved both complete original Theorems; independent source validation is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
