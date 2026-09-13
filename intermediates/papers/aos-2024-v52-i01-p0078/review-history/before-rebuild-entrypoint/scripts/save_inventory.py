"""Reviewed transcription of the five main-text Theorems in arXiv:2108.09904v2."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')
PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')

RECORDS=[
 ('3.1','CCB with maximum norm difference',7,r'''Suppose $(\log d)^5\Delta_{\infty}=O(1)$, then we have
\[
\sup_{0\le t\le C_0\sqrt{\log d}}\left|\frac{\mathbb{P}(\|U\|_{\infty}>t)}{\mathbb{P}(\|V\|_{\infty}>t)}-1\right|=O\left((\log d)^{5/2}\Delta_{\infty}^{1/2}\right),\tag{3.1}
\]
for some constant $C_0>0$.'''),
 ('3.3','CCB with elementwise ℓ₀-norm difference',8,r'''Assume the Gaussian random vectors $U$ and $V$ have unit variances, i.e., $\sigma^U_{jj}=\sigma^V_{jj}=1,j\in[d]$ and there exists some $\sigma_0<1$ such that $|\sigma^V_{jk}|\le\sigma_0,|\sigma^U_{jk}|\le\sigma_0$ for any $j\ne k$. Suppose there exists a disjoint $\mathfrak{p}$-partition of nodes $\cup_{\ell=1}^{\mathfrak{p}}\mathcal{C}_{\ell}=[d]$ such that $\sigma^U_{jk}=\sigma^V_{jk}=0$ when $j\in\mathcal{C}_{\ell}$ and $k\in\mathcal{C}_{\ell'}$ for some $\ell\ne\ell'$. We have
\[
\sup_{0\le t\le C_0\sqrt{\log d}}\left|\frac{\mathbb{P}(\|U\|_{\infty}>t)}{\mathbb{P}(\|V\|_{\infty}>t)}-1\right|=O\left(\frac{\Delta_0\log d}{\mathfrak{p}}\right),\tag{3.2}
\]
for some constant $C_0>0$.'''),
 ('4.2','FDP/FDR control',11,r'''Under Assumption 4.1 and the scaling condition $\frac{d_2\log d_2+d_0}{d_0d_2\rho}+\frac{s\log^2d_2}{n^{1/2}}+\frac{\log^2d_2}{(n\rho)^{1/5}}=o(1)$, if we implement the StarTrek procedure in Algorithm 2 with $\boldsymbol{\Theta}$ estimated by (4.2) and the quantiles approximated by (4.6), as $(n,d_1,d_2)\rightarrow\infty$, we have
\[
\mathrm{FDP}\le q\frac{d_0}{d_1}+o_{\mathbb{P}}(1)\quad\text{and}\quad\lim_{(n,d_1,d_2)\rightarrow\infty}\mathrm{FDR}\le q\frac{d_0}{d_1}.\tag{4.9}
\]'''),
 ('5.2','FDP/FDR control',13,r'''Under Assumption 5.1, the StarTrek procedure in Algorithm 2 with (5.1) as input and the quantiles approximated by (5.2) satisfies: as $(n,d)\rightarrow\infty$,
\[
\mathrm{FDP}\le q\frac{d_0}{d}+o_{\mathbb{P}}(1)\quad\text{and}\quad\lim_{(n,d)\rightarrow\infty}\mathrm{FDR}\le q\frac{d_0}{d}.\tag{5.6}
\]'''),
 ('6.3',None,15,r'''Under Assumptions 6.1 and 6.2, the StarTrek procedure in Algorithm 2 with the generic estimator $\tilde{\boldsymbol{\Theta}}$ and the approximated quantiles (6.1) satisfies: as $(n,d)\rightarrow\infty$,
\[
\mathrm{FDP}\le qd_0/d+o_{\mathbb{P}}(1)\quad\text{and}\quad\lim_{(n,d)\rightarrow\infty}\mathrm{FDP}\le qd_0/d.
\]''')]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    main_tex=(WORK/'main-only.tex').read_text()
    source_theorems=re.findall(r'\\begin\{theorem\}(.*?)\\end\{theorem\}',main_tex,re.S)
    assert len(source_theorems)==5
    claims=[]
    for order,(number,title,page,body) in enumerate(RECORDS,1):
        claims.append(dict(claim_id=PID+'/T'+number,paper_id=PID,claim_kind='theorem',
            label='Theorem '+number+(' ('+title+')' if title else ''),source_order=order,
            statement_original=body,evidence=[dict(page=page,location='Theorem '+number)]))
    paper=dict(paper_id=PID,title='StarTrek: Combinatorial variable selection with false discovery rate control',
        version='arXiv:2108.09904v2',source_url='https://arxiv.org/pdf/2108.09904v2',
        pdf_pages=87,pdf_sha256=digest(WORK/'source.pdf'),main_text_last_pdf_page=25,
        main_text_boundary=dict(location='Main article and its references end on PDF page 25. The separately headed Supplementary Material begins on PDF page 26.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    for n in ['page-01.png','page-07.png','page-08.png','page-11.png','page-13.png','page-15.png','page-25.png','supplement-boundary.png','main-only.tex','macros.tex']:
        shutil.copy2(WORK/n,ROOT/'evidence'/n)
    write('evidence/enumeration.json',dict(paper_id=PID,method='Enumerated all five uncommented theorem environments before the appendix command in the matching-version source, corroborated by the main-section HTML environments, and checked their complete statements and printed labels against the PDF.',
        source_pdf_sha256=paper['pdf_sha256'],matching_tex_archive_sha256=digest(WORK/'source.tar.gz'),
        main_text_tex_sha256=digest(WORK/'main-only.tex'),theorems=[dict(label=c['label'],evidence=c['evidence'],original_tex=raw) for c,raw in zip(claims,source_theorems)],
        supplement_excluded_from_inventory=True))
    write('inventory-review.json',dict(paper_id=PID,status='complete',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),inventory_sha256=digest(ROOT/'theorem-inventory.json'),
        source_checked=True,validator_status='passed',theorem_count=5,
        notes=['Theorem 6.3 prints FDP in both conclusions. The PDF and matching TeX agree; the second FDP has not been silently changed to FDR.',
               'Assumptions and model definitions outside these five environments remain for the interface-extraction stage; they have not been inserted into original theorem statements.',
               'Theorem titles and equation references were checked against printed numbering, including Algorithm 2 rather than Algorithm 1.',
               'An initial automated boundary probe emitted a short portion of supplementary page 27 after identifying the boundary on page 26. That output was not used in the census; subsequent extraction is limited to the source before the appendix command and HTML Sections 1-8.']))
    checkpoint=json.loads((ROOT/'checkpoint.json').read_text())
    checkpoint.update(inventory_status='validated',inventory_sha256=digest(ROOT/'theorem-inventory.json'),
        remaining_work='Five complete theorem statements checked against the PDF and independently validated. Next extract all relevant main-text definitions, numbered assumptions, procedures and local dependencies, then validate the complete census. Do not inspect the Supplementary Material.')
    write('checkpoint.json',checkpoint)
    print('Saved and validated five Theorems; the paper census remains in progress.')

if __name__=='__main__':
    main()
