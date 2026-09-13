"""Validate the independently enumerated and visually reviewed theorem inventory.

This checker pins a reviewed transcription. Changing the pin requires renewed PDF review.
"""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA
EXPECTED_INVENTORY_SHA='de6bc596a31b21a3accee602553198345204f4248bcf610af537780db3746c09'

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==59 and 'arXiv:2308.04916v3' in pdf[0].get_text()
    headings=[];text_hashes={}
    for n in range(1,27):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,156.9671630859375) if n==26 else page.rect
        text=page.get_text(clip=clip)
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<26 else 'page-26-before-appendix.txt')
        assert path.read_bytes().decode()==text
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                match=re.match(r'^THEOREM (\d+)(?:\.| \()',s)
                if match:
                    assert line['spans'][0]['font']=='NimbusRomNo9L-Regu'
                    headings.append((n,match[1]))
    assert headings==[(7,'1'),(9,'2'),(10,'3'),(10,'4'),(11,'5'),(12,'6'),(13,'7'),(14,'8'),(14,'9'),(15,'10')]
    assert 'Acknowledgments.' in text and 'Funding.' in text and 'ANR-23-CE40-0018-01' in text
    assert 'SUPPLEMENTARY' not in text and 'APPENDIX' not in text
    boundary=pdf[25].get_text(clip=fitz.Rect(0,150,pdf[25].rect.width,179))
    assert 'SUPPLEMENTARY MATERIAL' in boundary
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
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
    assert 'truncated priors at $k=n$' in t['1'] and 'truncated' not in t['2']
    assert r'2\beta+2\nu+1' in t['2']
    assert r'\alpha\ge\beta+1/q' in t['3'] and '$q\ge1$' in t['3']
    assert r'$(\sigma_k)$' in t['4'] and r'$r\in[1,2]$' in t['4']
    assert r'w_l=l^{1+\kappa+\varepsilon}' in t['5'] and r'w_l=l^{(1+\kappa+\varepsilon)/2}' in t['5']
    assert '(14)' not in t['5'] and '(19)' not in t['5']
    assert t['6'].count('•')==2 and t['7'].count('•')==2
    assert 'for large enough' not in t['6'] and t['7'].count('for large enough')==2
    assert r'\tag{20}' in t['6'] and r'\tag{21}' in t['6'] and r'\tag{22}' in t['6']
    assert r'\tag{23}' in t['7'] and r'\tag{24}' in t['7'] and r'\log\log n' in t['7']
    assert 'Theorem 7' in t['8'] and 'Theorem 6' in t['9']
    assert r'\|p_f-p_{f_0}\|_{G,1}' in t['9'] and 'M=M(\rho)>0' not in t['9']
    assert '(19)' in t['10'] and '(14)' not in t['10'] and '(6)' not in t['10']
    for n in ['1','2','3','4','10']: assert r'\mathcal L_n' in t[n]
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1433-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
      'The registered source is arXiv:2308.04916v3, 29 May 2024, 59 pages. Main text ends after Funding before the Supplementary Material heading on page 26. Only that upper part of page 26 is retained.',
      'Independent actual-heading enumeration confirms Theorems 1 through 10, with complete original statements on pages 7, 9, 10, 11, 12, 13, 14 and 15. Main-text proof headings and theorem citations are excluded.',
      'All ten complete statements were visually compared against the registered PDF. Both branches of Theorems 6 and 7, all rate exponents, moment orders, smoothness restrictions and truncation clauses are retained.',
      'Theorem 5 has different multiscale weights in its two branches and no moment or tail assumption. Theorem 10 has the tail condition (19), without adding moment condition (14) or a polynomial-scale branch.',
      'Preserve the source notation sigma_k in Theorem 4 and p_f in the G,1 norm in Theorem 9. Theorem 9 refers to Theorem 6, whereas its preceding model paragraph mentions wavelet priors; these source discrepancies require separate extraction notes, not edits to the quotations.',
      'Inventory schema validation, mathematical-fragment checks and isolated exact regeneration passed. Supporting-passage extraction and full census audit remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, schema validation and isolated regeneration.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,7,9,10,11,12,13,14,15,26],boundary_crop='evidence/page-26.png'),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2308.04916v3.pdf',registered_url_alias='https://export.arxiv.org/pdf/2308.04916',checked_at=now),indent=2)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=10,source_pdf_sha256=SHA,next_action='Extract the series priors, scales, separate density conditions, smoothness balls, model conventions, multiscale space and posterior definitions; preserve branch-specific dependencies and source discrepancies.'),indent=2)+'\n')
    print('Ten complete original theorem statements independently checked; full census remains pending.')

if __name__=='__main__':main()
