"""PDF-reviewed main-text theorem inventory for arXiv:2112.08417v2."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
EVIDENCE_ROOT = ROOT/'evidence'
PID = ROOT.name
SKILL = Path('skills/statistical-paper-census/scripts')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')

STATEMENTS = [
 r'''Let $\mathcal{M}$ be a DMAG with time series structure and time index set $\mathbf{T}=\{t-\tau\mid 0\leq t\leq p\}$. Then $\mathcal{M}$ is a ts-DMAG, i.e., there is a ts-DAG $\mathcal{D}$ such that $\mathcal{M}=\mathcal{M}^{p}(\mathcal{D})$ if and only if the MAG latent projection $\mathcal{M}^{p}(\mathcal{D}_c(\mathcal{M}))$ of the canonical ts-DAG $\mathcal{D}_c(\mathcal{M})$ of $\mathcal{M}$ equals $\mathcal{M}$, i.e., if and only if $\mathcal{M}=\mathcal{M}^{p}(\mathcal{D}_c(\mathcal{M}))$.''',
 r'''Let $\mathcal{G}$ be a directed mixed graph with time series structure and time index set $\mathbf{T}=\{t-\tau\mid 0\leq t\leq p\}$. Then $\mathcal{G}$ is a ts-DMAG, i.e., there is a ts-DAG $\mathcal{D}$ such that $\mathcal{G}=\mathcal{M}^{p}(\mathcal{D})$ if and only if $\mathcal{G}$ is acyclic and $\mathcal{G}=\mathcal{M}^{p}(\mathcal{D}_c(\mathcal{G}))$.''',
 r'''Let $\mathcal{D}$ be a ts-DAG and let $(\mathcal{A},\mathcal{A}^{stat})$ either be $(\mathcal{A}_{to},\mathcal{A}_{to})$ or $(\mathcal{A}_{ta},\mathcal{A}_{ta})$ or $(\mathcal{A}_{\mathcal{D}},\mathcal{A}^{stat}_{\mathcal{D}})$. Then:

1. Every non-circle mark (head or tail) in $\mathcal{P}(\mathcal{M}^{p}_{st}(\mathcal{D}),\mathcal{A}^{stat})$ is also in $stat(\mathcal{P}(\mathcal{M}^{p}(\mathcal{D}),\mathcal{A}))$.
2. Every non-circle mark in $\mathcal{P}(\mathcal{M}^{p}_{st}(\mathcal{D}),\mathcal{A}^{stat})$ is also in $\mathcal{P}(\mathcal{M}^{p}(\mathcal{D}),\mathcal{A})$.
3. There are cases in which a non-circle mark that is in $stat(\mathcal{P}(\mathcal{M}^{p}(\mathcal{D}),\mathcal{A}))$ is not also in $\mathcal{P}(\mathcal{M}^{p}_{st}(\mathcal{D}),\mathcal{A}^{stat})$.
4. There are cases in which a non-circle mark that is in $\mathcal{P}(\mathcal{M}^{p}(\mathcal{D}),\mathcal{A})$ is not also in $\mathcal{P}(\mathcal{M}^{p}_{st}(\mathcal{D}),\mathcal{A}^{stat})$, even regarding adjacencies that are shared by both graphs.'''
]

def main():
    source = Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source) == 'd455852177d78183664ed5a1b6f93701cfbe5d650be1a03569bac2d5cf913a1f'
    assert digest(EVIDENCE_ROOT/'main-only.tex') == 'f2f1184435c08f734b0133e99257aef6be36d2069f89fb4c03b8c1550349d0ed'
    tex = (EVIDENCE_ROOT/'main-only.tex').read_text()
    tex = re.sub(r'(?m)(?<!\\)%.*$', '', tex)
    envs = re.findall(r'\\begin\{mythm\}(.*?)\\end\{mythm\}', tex, re.S)
    assert len(envs) == 3
    claims = [dict(claim_id=PID+'/T'+str(i), paper_id=PID, claim_kind='theorem',
                   label='Theorem '+str(i), source_order=i, statement_original=body,
                   evidence=[dict(page=page, location='Theorem '+str(i))])
              for i,(body,page) in enumerate(zip(STATEMENTS,[16,16,20]),1)]
    paper = dict(paper_id=PID,
        title='Characterization of causal ancestral graphs for time series with latent confounders',
        version='arXiv:2112.08417v2', source_url='https://arxiv.org/pdf/2112.08417v2',
        pdf_pages=67, pdf_sha256=digest(source), main_text_last_pdf_page=25,
        main_text_boundary=dict(location='The main text ends with Discussion and Acknowledgments on PDF page 25, above the Supplementary Material heading. Extraction stops at that heading; the supplement is excluded.', shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json', dict(schema_version='statistical-theorem-inventory-v1',
          scope=dict(theorem_scope='main_text_only'), papers=[paper], claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)

if __name__ == '__main__':
    main()
