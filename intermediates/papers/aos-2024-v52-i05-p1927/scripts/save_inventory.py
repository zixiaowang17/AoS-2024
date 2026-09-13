# -*- coding: utf-8 -*-
"""Reproduce the two original main-text Theorems from the registered PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p1927'
SHA='36f90f799deee2370dbbf62af76ddfaf3c13ff043d87d528dfb0b84a5b81808a'
URL='https://arxiv.org/pdf/2109.12002v1'
NUMBERS=['1','2'];PAGES=[[10,11],[17,18]]
TITLES=['Non-asymptotic upper bounds','Minimax lower bounds']
STATEMENTS=[r'''There is a universal constant $c_0$ such that:

(a) Slow rate: Under the kernel boundedness condition (13), the bound (17) holds for any solution $\delta=\delta(n,R,\gamma,b)$ to the critical inequality $\operatorname{CI}(bR)$ and any $\lambda_n\geq c_0\delta^2(1-\gamma)$.

(b) Fast rate: Suppose in addition that the kernel eigenfunctions are uniformly bounded (14). Let $\delta_n(\kappa\sigma(\theta^*))$ be the smallest solution to the critical inequality $\operatorname{CI}(\kappa\sigma(\theta^*))$, and suppose that $n$ is large enough to ensure that
\[
R^2\delta_n^2(\kappa\sigma(\theta^*))\leq\frac{\kappa\,\sigma^2(\theta^*)}{200(1-\gamma)\sqrt n}.
\]
(18)
Then the bound (17) holds for any solution $\delta=\delta(n,R,\gamma,\sigma(\theta^*))$ to the critical inequality $\operatorname{CI}(\kappa\sigma(\theta^*))$ and any $\lambda_n\geq c_0\delta^2(1-\gamma)$.''',r'''(a) For any pair $(\bar R,\bar\sigma)$ in Regime A (32a), there is a $(\bar R,\bar\sigma)$-valid family of MRPs such that the lower bound $\operatorname{LB}(\bar R,\bar\sigma,\delta_n)$ holds for any sample size $n$ such that
\[
\bar R^2\delta_n^2\leq\frac{2\kappa\bar\sigma^2}{(1-\gamma)^{3/2}\sqrt n}.
\]
(33a)
(b) Consider any pair $(\bar\sigma,\bar R)$ in Regime B (32b), and suppose that the eigensequence satisfies $\min_{3\leq j\leq d_n}\{\sqrt{\mu_{j-1}}-\sqrt{\mu_j}\}\geq\frac{\delta_n}{2d_n}$. Then there is a $(\bar R,\bar\sigma)$-valid family of MRPs such that the lower bound $\operatorname{LB}(\bar R,\bar\sigma,\delta_n)$ holds for a sample size $n$ large enough such that
\[
\bar R^2\delta_n^2\leq\frac{12\kappa\bar\sigma^2}{(1-\gamma)\sqrt n}\quad\text{and}\quad\bar R\delta_n\leq10\kappa\bar\sigma\left(1-\frac{\mu_2}{\mu_1}\right)\min\left\{\frac{\kappa\bar\sigma/(\sqrt{\mu_1}\bar R)}{(1-\gamma)^2\log n},\frac{\sqrt{\mu_1}}{b}\right\}.
\]
(33b)''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; complete statement including the continuation') for p in pages]) for i,(n,title,s,pages) in enumerate(zip(NUMBERS,TITLES,STATEMENTS,PAGES),1)]
    paper=dict(paper_id=PID,title='Optimal policy evaluation using kernel-based temporal difference methods',authors=['Yaqi Duan','Mengdi Wang','Martin J. Wainwright'],version='arXiv:2109.12002v1; arXiv stamp 24 Sep 2021; title-page date September 27, 2021',pdf_pages=58,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=30,main_text_boundary=dict(location='Section 5 Discussion continues onto PDF page 30 and ends with Acknowledgements at y=286.3. Appendix A, Details of simulations, begins below at y=307.0. Page-30 source evidence is clipped at y=295, above Appendix A.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerated bold Theorem 1 and Theorem 2 environments across all main-text pages, including the proof section. Visually compared both full statements and their next-page continuations. Excluded ordinary-text citations, proof headings, Corollaries, Lemmas and appendices.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v1 PDF. Page 30 is clipped above Appendix A; no appendix body or replacement source is used.',normalization_policy='Preserve original theorem wording, formulas, all branches and numbered references. Normalize line wrapping and mathematical typesetting only. Referenced bounds and standing definitions are saved separately, not inserted into original theorem bodies.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved two complete original Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
