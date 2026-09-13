"""Rebuild the manually transcribed main-text theorem inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1334'
SHA='ea31f60f810e9e62cb1cea4b540e44a17e40a122a998cb1df72585ec2e818cf4'
claims=[]

def claim(number,page,text):
    claims.append(dict(claim_id=f'{PID}/T{number}',paper_id=PID,claim_kind='theorem',label=f'Theorem {number}',source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location=f'Theorem {number}, complete printed statement')]))

claim('3.3',8,r'''
For any integer $k\ge2$, and any $p\ge q$, we have
\[
\operatorname{Var}(U_k)\le c^k\big[(pq)^k+p\|\mathbf A\|_{4k-4}^{4k-4}+\|\mathbf A\|_{4k-2}^{4k-2}+p^kk^{3k}+k^{6k}\big],
\]
where $c$ is a numerical constant.
''')
claim('4.9',12,r'''
There exists a numerical constant $c>0$ such that the following holds for all positive integers $4\le q\le p$ and for all continuous functions $f:\mathbb R^+\mapsto\mathbb R$. Writing $I_0=[0,0.125(pq)^{1/4}]$ and $k^*=\lceil\log(4\lceil q/2\rceil)\rceil$, we have
\[
\inf_{\widehat T}\sup_{\mathbf A:\|\mathbf A\|_\infty\le0.125(pq)^{1/4}}\mathbb E\big[|\widehat T-f_\sigma(\mathbf A)|\big]\ge c\big[qE_{\mathcal P_{2k^*}^{sym}}[f;I_0]]-q^{1/2}\|f\|_{\infty,I_0}\big]_+,\tag{20}
\]
where we recall that $f_\sigma(\mathbf A)=\sum_{i=1}^q f(\sigma_i(\mathbf A))$.
''')
claim('5.2',14,r'''
Fix any $M>1$ and choose $K=\lfloor c\log(q)\rfloor$ for a suitable numerical constant $M>1$. If $\sigma_1(\mathbf A)\le M(pq)^{1/4}$, then the estimator $\widehat\sigma_i$ defined above satisfies
\[
W(\mu_{\widehat\sigma},\mu_{\sigma(\mathbf A)})\lesssim\frac{M}{\log(q)}(pq)^{1/4}.\tag{25}
\]
In particular, this implies that
\[
\mathbb E\left[\sum_{i=1}^q|\widehat\sigma_i-\sigma_i(\mathbf A)|\right]\lesssim\frac{M}{\log(q)}q(pq)^{1/4}.
\]
''')
claim('6.3',15,r'''
For any positive integer $k\ge1$ and any $p\ge q$, we have
\[
\mathbb E\left[\left(U_k-\|\mathbf A\|_{2k}^{2k}\right)^2\right]\le(c\|E\|_{\psi_2}k)^{c'k}\big[(pq)^k+pq\|\mathbf A\|_\infty^{4k-4}+q\|\mathbf A\|_\infty^{4k-2}\big],\tag{28}
\]
where $c$ and $c'$ are numerical constants.
''')

def main():
    pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Optimal estimation of Schatten norms of a rectangular matrix',authors=['Solène Thépaut','Nicolas Verzelen'],version='arXiv:2111.13551v1, 26 November 2021',source_url='https://arxiv.org/pdf/2111.13551v1',pdf_pages=67,pdf_sha256=SHA,main_text_last_pdf_page=65,main_text_boundary=dict(location='Main text ends on PDF page 65 after the proof of Lemma 9.15. Appendix A: Technical inequalities begins at y=400.551 PDF points on that page. Appendix bodies are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified local arXiv v1 PDF, pages 1-64 and main text above Appendix A on page 65; appendix bodies excluded.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
