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
WORK = Path('[local path omitted]')
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
    tex = (WORK/'main-only.tex').read_text()
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
        pdf_pages=67, pdf_sha256=digest(WORK/'source.pdf'), main_text_last_pdf_page=25,
        main_text_boundary=dict(location='The main text ends with Discussion and Acknowledgments on PDF page 25, above the Supplementary Material heading. Extraction stops at that heading; the supplement is excluded.', shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json', dict(schema_version='statistical-theorem-inventory-v1',
          scope=dict(theorem_scope='main_text_only'), papers=[paper], claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    for name in ['main-only.tex','page-16.png','page-20.png','page-25.png']:
        shutil.copy2(WORK/name,ROOT/'evidence'/name)
    write('evidence/enumeration.json',dict(paper_id=PID,source_pdf_sha256=paper['pdf_sha256'],
        matching_tex_archive_sha256=digest(WORK/'source.tar.gz'),
        method='Enumerated all three uncommented mythm environments in main.tex before the supplementary-material environment; scanned PDF pages 1-25 up to the boundary and visually checked both theorem pages and the boundary crop.',
        theorems=[dict(label=c['label'],evidence=c['evidence'],original_tex=raw) for c,raw in zip(claims,envs)],
        supplementary_material_read=False))
    write('inventory-review.json',dict(paper_id=PID,status='complete',
        reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        inventory_sha256=digest(ROOT/'theorem-inventory.json'), source_checked=True,
        validator_status='passed',theorem_count=3,notes=[
          'Theorems 1 and 2 print 0 <= t <= p in their time-index sets. Both PDF and TeX agree; this has not been silently changed to a bound on tau.',
          'Theorem 3 has four subparts; all four and the three allowed background-knowledge pairs are preserved.',
          'Older review material covers a different scope and is not used as evidence of completion.']))
    write('checkpoint.json',dict(paper_id=PID,stage='interface_extraction',inventory_status='validated',
        source_pdf_path=str(WORK/'source.pdf'),source_pdf_sha256=paper['pdf_sha256'],
        remaining_work='Extract relevant main-text definitions and local statement dependencies, check source correspondence and highlight selectors, then finalize and independently validate the census.'))

if __name__ == '__main__':
    main()
