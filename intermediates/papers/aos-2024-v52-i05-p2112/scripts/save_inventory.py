"""Reproduce all four original main-text Theorems of the registered arXiv v3 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2112'
SHA='9eadba2195953e9ed76c35785d3f7da46c8c7f739b093d3ebde0f9c3d4227759'
URL='https://arxiv.org/pdf/2209.04962v2'
NUMBERS=['1','2','3','4']
STATEMENTS=[r'''Assume $\frac{np}{\sigma^2}\to\infty$ and $\frac{np}{\log n}\to\infty$. There exists some $\delta=o(1)$ such that with high probability,
\[
\ell(\widehat z,z^*)\leq(1+\delta)\frac{\sigma^2}{2np}.
\]
(7)
As a consequence, when $\sigma=0$ (i.e., there is no additive noise), the spectral method recovers $z^*$ exactly (up to a phase) with high probability as long as $\frac{np}{\log n}\to\infty$.''',r'''Assume $\frac{np}{\sigma^2}\to\infty$, $\frac{np}{\log n}\to\infty$, and $2\leq d=O(1)$. There exists some $\delta=o(1)$ such that with high probability,
\[
\ell^{od}(\widehat Z,Z^*)\leq(1+\delta)\frac{d(d-1)\sigma^2}{2np}.
\]
As a consequence, when $\sigma=0$ (i.e., there is no additive noise), the spectral method recovers $Z^*$ exactly (up to an orthogonal matrix) with high probability as long as $\frac{np}{\log n}\to\infty$.''',r'''There exist constants $C_1,C_2,C_3>0$ such that if $\frac{np}{\log n}>C_1$ and $\frac{np}{\sigma^2}>C_2$, we have
\[
\ell(\widehat z,z^*)\leq\left(1+C_3\left(\left(\frac{\sigma^2}{np}\right)^{1/4}+\sqrt{\frac{\log n}{np}}+\frac1{\log(np)}\right)\right)\frac{\sigma^2}{2np},
\]
with probability at least $1-n^{-9}-\exp\left(-\frac1{32}\left(\frac{np}{\sigma^2}\right)^{1/4}\right)$.''',r'''Assume $2\leq d\leq C_0$ for some constant $C_0>0$. There exist constants $C_1,C_2,C_3$ such that if $\frac{np}{\log n}>C_1$ and $\frac{np}{\sigma^2}>C_2$, we have
\[
\ell^{od}(\widehat Z,Z^*)\leq\left(1+C_3\left(\left(\frac{\sigma^2}{np}\right)^{1/4}+\sqrt{\frac{\log n}{np}}+\frac1{\log(np)}\right)\right)\frac{d(d-1)\sigma^2}{2np}
\]
holds with probability at least $1-n^{-9}-\exp\left(-\frac1{32}\left(\frac{np}{\sigma^2}\right)^{1/4}\right)$.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,[2,5,9,12]),1)]
    paper=dict(paper_id=PID,title='Exact minimax optimality of spectral methods in phase synchronization and orthogonal group synchronization',authors=['Anderson Ye Zhang'],version='arXiv:2209.04962v2; stamp 6 Jan 2024; cover 9 Jan 2024',pdf_pages=41,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='The proof of Lemma 4 in Section 6 ends on PDF page 29. Page-29 evidence is clipped at y=455, above References at y=460.6. Appendix A Proofs of Lemma 3, Proposition 3, and Proposition 4 starts on page 32; no appendix body is used.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate actual bold Theorem environments throughout pages 1-28 and the main-text prefix of page 29; compare all four statements visually. Retain both asymptotic summary theorems and both finite-sample theorems. Include the italic no-noise consequences in Theorems 1 and 2; exclude Lemmas, Propositions, citations and proof headings.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v2 PDF; no replacement source and no appendix body.',normalization_policy='Preserve complete original theorem wording, including both no-noise consequences, exact constants and probability bounds. Normalize PDF line wrapping and mathematical typesetting only.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved all four complete original Theorems; independent source validation is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
