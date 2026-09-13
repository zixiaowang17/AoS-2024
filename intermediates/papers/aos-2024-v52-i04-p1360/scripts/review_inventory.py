"""Record the independently checked inventory, pinned to the reviewed transcription.

A changed inventory requires renewed source comparison, not just a new expected hash.
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA

EXPECTED_INVENTORY_SHA='716c67c5f78193d83b1598aa8ac0db7d0a1a85df1b9da1ae85378af2e0700eb7'


def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==46 and 'arXiv:2111.06859v1' in pdf[0].get_text()
    headings=[]
    text_hashes={}
    for n,page in enumerate(list(pdf)[:21],1):
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode('utf8')==page.get_text()
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        assert not re.search(r'^APPENDIX\b',page.get_text(),re.M)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                m=re.match(r'^Theorem (\d+) \(',text)
                if m: assert line['spans'][0]['font']=='CMBX10'
                if m: headings.append((n,m[1]))
    assert headings==[(6,'1'),(7,'2'),(9,'3'),(10,'4'),(11,'5'),(12,'6'),(14,'7')]
    boundary=pdf[21].get_text(clip=fitz.Rect(0,0,pdf[21].rect.width,201.90811157226562))
    assert '56(2):254' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-22-before-appendix.txt').read_bytes().decode()==boundary
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
    assert [e['page'] for e in inv['claims'][1]['evidence']]==[7,8]
    assert [e['page'] for e in inv['claims'][3]['evidence']]==[10,11]
    for c in inv['claims']:
        s=c['statement_original']
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        assert s.count(r'\[')==s.count(r'\]') and len(re.findall(r'(?<!\\)\$',s))%2==0
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if brace=='{' else -1
                assert depth>=0
            assert depth==0
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert 'holds uniformly' in t['1'] and 'even polynomial when $j$ is odd' in t['1']
    assert r'K\ge r+3' in t['2'] and r'K\ge4' in t['2']
    assert 'The same result holds' in t['2'] and r'$r+1$ times differentiable' in t['2']
    assert r'as $n\to0$' in t['3'] and r'$r$ times differentiable' in t['3']
    assert 'symmetric' not in t['3'] and r'P(-q' not in t['3']
    assert t['4'].count(r'\begin{cases}')==2 and t['4'].count(r'\end{cases}')==2
    assert all(s in t['4'] for s in ['(i)','(ii)','(iii)','(iv)',r'E_{P,\lambda}\tau^{r+1}',r'\bar{\bar c}'])
    assert 'The same result holds' in t['4'] and r'K\ge4' in t['4']
    assert r'Q_1' in t['5'] and r'E[T_2-T_1]>0' in t['5'] and 'The same result holds' in t['5']
    assert 'conditions of Theorem 2 hold with $r=2$' in t['6'] and 'Algorithm 1' in t['6']
    assert r'Fix $n$ and let $K\to\infty$' in t['7']
    assert t['7'].count(r'\sqrt{nE(\psi(\widehat P_1)-\psi)^2}/\sigma')==2
    assert r'W_{SB}' not in t['7'] and 'differantiable' in t['7']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1360-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
        'The pinned source is the 46-page arXiv:2111.06859v1 PDF dated 12 November 2021. The register filename and unversioned export URL identify the same verified bytes; the precise versioned URL is retained.',
        'Independent bold-heading enumeration of all admitted main-text pages confirms exactly seven Theorems, numbered 1 through 7, on pages 6,7,9,10,11,12,14. Citations, Propositions and proofs are excluded.',
        'All seven original statements were compared visually, including the continuations of Theorem 2 on page 8 and Theorem 4 on page 11. Printed titles, hypotheses, every bullet and each replacement-of-method clause are retained.',
        'Theorem 1 assumes a uniform Edgeworth expansion with alternating polynomial parity. Theorem 2 instead supplies finite moments, nonsingular covariance, Cramer condition and smoothness, with separate K thresholds for the two conclusions.',
        'Theorem 3 retains the printed n-to-zero limit and r-times differentiability. It has no symmetric-coverage conclusion; this is not borrowed from Theorem 4.',
        'Theorem 4 includes the complete minorization and split-process construction, both transition cases, centered cycle sum and all four conditions. Its r+3 and r+1 moment requirements under different initial laws remain distinct.',
        'Theorem 5 uses the regenerative-cycle pairs and requires a positive expected cycle length. Theorem 6 inherits Theorem 2 with r=2 and refers to the original Algorithm 1 and expansion (6).',
        'Theorem 7 fixes n and sends K to infinity, unlike earlier fixed-K expansions. A high-resolution formula crop confirms that division by sigma is outside each square root. The source spelling differantiable is retained, and no SB conclusion is added.',
        'The main text and references end above Appendix A on PDF page 22 at y=202.908. The earlier line beginning Appendix E on page 6 is a proof reference, not an appendix boundary. No appendix body was opened.',
        'Inventory schema validation and isolated exact regeneration passed. Supporting source passages, algorithm transcription, relationship extraction and complete source audit remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, typography check, schema validation and isolated rebuild.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,6,7,8,9,10,11,12,14],boundary_crop='evidence/page-22-boundary.png',before_appendix_text_sha256=hashlib.sha256((ROOT/'evidence/page-22-before-appendix.txt').read_bytes()).hexdigest()),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2111.06859v1.pdf',registered_url_alias='https://export.arxiv.org/pdf/2111.06859',checked_at=now),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=7,source_pdf_sha256=SHA,next_action='Extract the four batching statistics and CI constructions, independent versus gapped versus regenerative sampling, the original mixing and Harris definitions, full Algorithm 1 and its source coefficients, and theorem-local conditions; then finalize and independently review all relationships.'),indent=2)+'\n')
    print('Seven complete theorem statements independently checked; full census remains in progress.')

if __name__=='__main__':main()
