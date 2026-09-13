"""Pin and independently validate all four main-text bandit Theorems."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import fitz

ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
WORK=Path('[local path omitted]')/PID
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2341.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
SHA='a4f4af9a32f0d0d733cc8230f9ee11507196c8bb2284e5532ba8f27e9b37c49f'
STATEMENTS=[
 ('1','Upper bound',13,r'''Assume that $\alpha\beta\leq d$. Then the expected regret of the policy $\pi$ given by Algorithm 1 satisfies
\[
\sup_{\Pi(K,\beta,\alpha,\gamma,\kappa)}\mathbb E[R_{n_Q}(\pi)]\leq Cn_Q\left(n_Q+(\kappa n_P)^{\frac{d+2\beta}{d+2\beta+\gamma}}\right)^{-\frac{\beta(1+\alpha)}{d+2\beta}}\tag{11}
\]
where $C>0$ is a constant independent of $n_Q$ and $n_P$.'''),
 ('2','Lower bound',14,r'''Assume that $\alpha\beta\leq d$. Then one has
\[
\inf_{\pi}\sup_{\Pi(K,\beta,\alpha,\gamma,\kappa)}\mathbb E[R_{n_Q}(\pi)]\geq cn_Q\left(n_Q+(\kappa n_P)^{\frac{d+2\beta}{d+2\beta+\gamma}}\right)^{-\frac{\beta(1+\alpha)}{d+2\beta}}\tag{12}
\]
where $c>0$ is a constant independent of $n_Q$ and $n_P$.'''),
 ('3','Upper bound',19,r'''Let $0<\underline\beta<\overline\beta\leq1$ and $\overline\gamma\geq0$. Suppose that $\kappa\asymp1$ and $\alpha\beta\leq d$. Then the policy $\pi^a$ given by Algorithm 2 satisfies that for all $\beta\in[\underline\beta,\overline\beta]$ and $\gamma\in[0,\overline\gamma]$,
\[
\sup_{\Pi(K,\beta,\alpha,\gamma,\kappa,l_0,b)}\mathbb E[R_{n_Q}(\pi^a)]\leq C_1n_Q\left(n_Q+(\kappa n_P)^{\frac{d+2\beta}{d+2\beta+\gamma}}\right)^{-\frac{\beta(1+\alpha)}{d+2\beta}}\log^{C_2}(n_P+n_Q),\tag{19}
\]
for some constants $C_1>0$ and $C_2>0$ independent of $n_Q$ and $n_P$.'''),
 ('4','Lower bound',19,r'''Assume that $\alpha\beta\leq d$. For any constant $\beta\in(0,1]$ and $l_0\geq0$, there exists a constant $b>0$ that only depends on $\beta$, $C_\beta$, $\underline q$, $\overline q$ and $d$ such that
\[
\inf_{\pi}\sup_{\Pi(K,\beta,\alpha,\gamma,\kappa,l_0,b)}\mathbb E[R_{n_Q}(\pi)]\geq cn_Q\left(n_Q+(\kappa n_P)^{\frac{d+2\beta}{d+2\beta+\gamma}}\right)^{-\frac{\beta(1+\alpha)}{d+2\beta}}.\tag{20}
\]
for some constant $c>0$ independent of $n_Q$ and $n_P$.''')]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def main():
    assert digest(PDF)==SHA
    doc=fitz.open(PDF);assert len(doc)==63
    headings=[]
    for i in range(19):
        text=doc[i].get_text()
        (ROOT/'evidence'/f'page-{i+1:02}.txt').write_text(text)
        for match in re.finditer(r'(?m)^Theorem (\d+) \((Upper bound|Lower bound)\)',text):
            headings.append(dict(number=match[1],title=match[2],page=i+1))
    boundary=sorted(doc[19].search_for('Numerical experiments'),key=lambda r:r.y0)[0]
    main20=doc[19].get_text(clip=fitz.Rect(0,0,doc[19].rect.width,boundary.y0-1))
    assert not re.search(r'(?m)^Theorem \d+',main20)
    (ROOT/'evidence'/'page-20-main.txt').write_text(main20)
    assert headings==[dict(number=n,title=t,page=p) for n,t,p,_ in STATEMENTS]
    for n in [13,14,19]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    shutil.copy2(WORK/'boundary-page-20.png',ROOT/'evidence'/'boundary-page-20.png')
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',
        source_order=i,statement_original=body,evidence=[dict(page=p,location='Theorem '+n+' ('+title+')')])
        for i,(n,title,p,body) in enumerate(STATEMENTS,1)]
    paper=dict(paper_id=PID,title='Transfer learning for contextual multi-armed bandits',version='arXiv:2211.12612v2',
        source_url='https://arxiv.org/pdf/2211.12612v2',pdf_pages=63,pdf_sha256=SHA,main_text_last_pdf_page=20,
        main_text_boundary=dict(location='Section 5 Discussion continues onto page 20 and ends above the heading A Numerical experiments (PDF y=510.235). Only the heading was used to confirm the appendix boundary; all appendix content is excluded.',shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    write('evidence/enumeration.json',dict(headings=headings,method='Enumerate actual numbered Theorem headings across pages 1-19 and the main-text prefix of page 20, excluding table-of-contents proof references and appendix content. Visually inspect the complete four statements on pages 13, 14 and 19.',
        source_pdf_metadata=doc.metadata,appendix_heading_pdf_page=20,appendix_heading_y0=boundary.y0))
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',
        reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=4,inventory_sha256=digest(ROOT/'theorem-inventory.json'),notes=[
          'All four original Theorems retain their printed Upper bound or Lower bound titles and equation numbers (11), (12), (19) and (20).',
          'Theorem 3 retains lower and upper beta bounds, an upper gamma bound, kappa asymptotic to one, simultaneous beta/gamma scope, and its logarithmic factor. The alpha*beta<=d condition uses beta without a bar.',
          'Theorem 4 retains existence of b depending only on beta, C_beta, the lower and upper q constants, and d. Its final period after equation (20) and following lower-case for are preserved.',
          'The admissible-policy explanation after Theorem 2 is outside the original theorem body and will be resolved as a separate source definition.',
          'The appendix begins on the same page as the final main-text discussion. The boundary crop includes the heading alone, and no numerical experiment or proof from an appendix was read.']))
    write('checkpoint.json',dict(paper_id=PID,stage='interface_extraction',inventory_status='validated',source_pdf_path=str(PDF),
        source_pdf_sha256=SHA,remaining_work='Extract the bandit model, regret and policy definitions; unpack the general and self-similar parameter spaces and all their assumptions; archive Algorithms 1 and 2 with their referenced procedures and formulas. Preserve which assumptions and algorithms each theorem actually uses, then finalize and source-check the census.'))
    print('Saved and validated four original main-text Theorems; interface extraction remains.')

if __name__=='__main__':main()
