"""Rebuild manually transcribed main-text theorems from the pinned local source."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1277'
SHA='f6029bf56e0c7d9e0ddb7fd6c856e2d364833f16d7530ff9ce81e6eb5f53e25c'
claims=[]

def claim(number,page,text):
    claims.append(dict(claim_id=f'{PID}/T{number}',paper_id=PID,claim_kind='theorem',label=f'Theorem {number}',source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location=f'Theorem {number}, complete printed statement')]))

claim(2,6,r'''
The rate
\[
v_n(H)=\max\big(n^{-1/(4H+2)},\delta^{1/2}\big)
\]
is a lower rate of convergence for estimating $H$ in $\mathcal E^n$. Moreover,
\[
w_n(H)=\max\big(n^{-1/(4H+2)}\log n,\delta^{1/2}\big)
\]
is a lower rate of convergence for estimating $\eta$ over $\mathcal D$ in $\mathcal E^n$ (with obvious modifications in the definition).
''')
claim(3,8,r'''
The rate $v_n(H)=\max(n^{-1/(4H+2)},\delta^{1/2})$ is achievable for estimating $H$ over $\mathcal D$. More precisely, for $\nu_0<\inf_{(H,\eta)\in\mathcal D}\eta^2\kappa_0(H)2^{2H}$ with $\kappa_0(H)=4-2^{2H}$, the family of random variables
\[
\big(v_n^{-1}(\widehat H_n-H)\big)_{n\ge1}
\]
is tight in $\mathbb P_{H,\eta}$-probability, uniformly over $\mathcal D$.
''')
claim(4,9,r'''
The rates $v_n(H)=n^{-1/(4H+2)}$ and $w_n(H)=n^{-1/(4H+2)}\log n$ are lower rates of convergence for estimating $H$ and $\eta$ respectively over $\mathcal D$.
''')
claim(11,12,r'''
The rates $v_n(H)=n^{-1/(4H+2)}$ and $w_n(H)=n^{-1/(4H+2)}\log n$ are achievable for estimating $H$ and $\eta$ respectively over the parameter set $\mathcal D$.

More precisely, if $m_{opt}$ satisfies $m_{opt}>m>1/(4H)-2H-1$ for any $H_-<H<H_+$, then the sequences of random variables
\[
\big(v_n(H)^{-1}(\widehat H_n^{(m_{opt})}-H)\big)_{n\ge1}
\]
and
\[
\big(w_n(H)^{-1}(\widehat\eta_n^{(m_{opt})}-\eta)\big)_{n\ge1}
\]
are bounded in $\mathbb P_{H,\eta}$ probability, uniformly over $\mathcal D$.
''')

def main():
    pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Statistical inference for rough volatility: Minimax theory',authors=['Carsten H. Chong','Marc Hoffmann','Yanghui Liu','Mathieu Rosenbaum','Grégoire Szymansky'],version='arXiv:2210.01214v2, 15 February 2024',source_url='https://arxiv.org/pdf/2210.01214v2',pdf_pages=61,pdf_sha256=SHA,main_text_last_pdf_page=56,main_text_boundary=dict(location='References [56]-[58] finish at the top of PDF page 56. Appendix A starts below them at y=146.769 PDF points. Only the material above that heading belongs to the admitted main text; appendices A-C are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified local arXiv v2 PDF, pages 1-55 and the references above the Appendix A heading on page 56; appendix bodies excluded.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
