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
EVIDENCE_ROOT=ROOT/'evidence'
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
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


EXPECTED_SOURCE='50dc1b6cd36db1bc1b015e6722efb096eca9f3b5658405e7e9edc4604b1ae923'
EXPECTED_MAIN_TEX='54ef40b29f8143e50553d197954150f14b720b97cb34812c2999d539551844a7'

def main():
    # The literal statements and frozen main-text TeX are previously reviewed
    # extraction inputs. A rebuild does not emit a new source-review record.
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==EXPECTED_SOURCE
    assert digest(EVIDENCE_ROOT/'main-only.tex')==EXPECTED_MAIN_TEX
    source_theorems=re.findall(r'\\begin\{theorem\}(.*?)\\end\{theorem\}',(EVIDENCE_ROOT/'main-only.tex').read_text(),re.S)
    assert len(source_theorems)==5
    claims=[]
    for order,(number,title,page,body) in enumerate(RECORDS,1):
        claims.append(dict(claim_id=PID+'/T'+number,paper_id=PID,claim_kind='theorem',
            label='Theorem '+number+(' ('+title+')' if title else ''),source_order=order,
            statement_original=body,evidence=[dict(page=page,location='Theorem '+number)]))
    paper=dict(paper_id=PID,title='StarTrek: Combinatorial variable selection with false discovery rate control',
        version='arXiv:2108.09904v2',source_url='https://arxiv.org/pdf/2108.09904v2',
        pdf_pages=87,pdf_sha256=digest(source),main_text_last_pdf_page=25,
        main_text_boundary=dict(location='Main article and its references end on PDF page 25. The separately headed Supplementary Material begins on PDF page 26.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    print('Reproduced the five reviewed main-text Theorems from retained inputs.')
if __name__=='__main__':main()
