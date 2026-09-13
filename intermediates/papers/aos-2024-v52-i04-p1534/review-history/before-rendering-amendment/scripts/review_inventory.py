"""Independently validate the six visually reviewed main-text theorem statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
EXPECTED_INVENTORY_SHA='ea3fb55fb768adf3498c8c01a28a37f03037f5f3eca062122653c125a9bb7f54'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source);assert len(pdf)==83 and 'arXiv:2303.16711v3' in pdf[0].get_text()
    headings=[];hashes={}
    for n in range(1,31):
        p=pdf[n-1];clip=fitz.Rect(0,0,p.rect.width,637.9385986328125) if n==30 else p.rect;t=p.get_text(clip=clip)
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<30 else 'page-30-before-appendix.txt');assert path.read_bytes().decode()==t;hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in p.get_text('dict',clip=clip)['blocks']:
            for l in b.get('lines',[]):
                s=''.join(x['text'] for x in l['spans']);m=re.match(r'^Theorem (\d+) \(',s)
                if m:
                    assert l['spans'][0]['font']=='CMBX10';headings.append((n,m[1]))
    assert headings==[(6,'1'),(14,'2'),(15,'3'),(15,'4'),(16,'5'),(19,'6')]
    assert 'Zheng, W.' in t and '459' in t and 'Appendices' not in t
    assert 'Appendices' in pdf[29].get_text(clip=fitz.Rect(0,638,pdf[29].rect.width,658))
    path=ROOT/'theorem-inventory.json';assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text());assert len(inv['claims'])==6
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert all(part in t['1'] for part in ['(i)','(ii)','Both of the following implications'])
    assert r'\mathcal R_n^j=o_p(n^{-1/2})' in t['2'] and r'\mathcal D_n^j=o_P(n^{-1/2})' in t['2']
    assert '(4) holds' in t['2'] and 'is regular' in t['2'] and r'\mathbb H' in t['2']
    assert all(part in t['3'] for part in ['(i)','(ii)','asymptotically conservative','for all $\\delta>0$'])
    assert 'Theorem 2' in t['4'] and r'\max_{j\in\{1,2\}}' in t['4']
    assert [e['page'] for e in inv['claims'][4]['evidence']]==[16,17]
    assert '(25) holds' in t['5'] and 'Moreover' in t['5'] and r'\mathcal B_n^{j,\beta_n}' in t['5']
    assert r'\beta\in\ell^2\cap(0,1]^{\mathbb N}' in t['6'] and r'\|\dot\nu_0(s)\|_{\mathcal H}>0' in t['6']
    assert r'\Pr\left\{\|\mathbb H^\beta+\dot\nu_0^\beta(s)\|_{\mathcal H}^2>\zeta_{1-\alpha}\right\}>\alpha' in t['6']
    assert 'Also,' in t['6'] and r'\|h_n-h_0\|_{\mathcal H}=O(n^{-1/2})' in t['6']
    for s in t.values():
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not any(ord(c)<32 and c!='\n' for c in s)
        for d,i in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for c in re.findall(r'(?<!\\)[{}]',d+i):
                depth+=1 if c=='{' else -1
                assert depth>=0
            assert depth==0
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1534-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True);assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,d):(ROOT/name).write_text(json.dumps(d,indent=2)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent bold-heading enumeration and visual comparison of every theorem, including its full continued statement; schema, mathematical-fragment and exact rebuild checks.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,6,14,15,16,17,19,30],boundary_crop='evidence/page-30.png'),notes=['Six Theorems occur in the main text. A prose reference beginning Theorem 5 on page 21 is not a theorem environment.','Theorem 5 continues onto page 17; Theorem 4 is entirely on page 15, with only its proof discussion continuing on page 16.','Theorems 2 and 5 incorporate equations (4) and (25), respectively, which must be saved separately during source extraction.','Preserve the original lowercase o_p and uppercase o_P in Theorem 2, the two different confidence-set guarantees in Theorem 3, and the fixed positive-entry beta and local-power inequality in Theorem 6.','The arXiv stamp is dated 27 September 2023 while the title page says 28 September 2023; both are recorded. Full supporting-passage review remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2303.16711v3.pdf',registered_url_alias='https://export.arxiv.org/pdf/2303.16711',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=6,source_pdf_sha256=SHA,next_action='Extract pathwise differentiability, EIF and RKHS conventions, cross-fitted estimators, remainders and drifts, confidence sets and bootstrap thresholds, regularization and local alternatives; retain source issues and theorem-reference scope.'))
    print('Six complete original theorems independently validated; full census remains pending.')
if __name__=='__main__':main()
