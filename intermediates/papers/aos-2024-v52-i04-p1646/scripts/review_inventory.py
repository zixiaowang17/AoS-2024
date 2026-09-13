"""Independently verify the source-complete three-theorem inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
EXPECTED='7bb5e5c39662bfcbf7d74fcc3ea9091df02f65c107bf368016a7557b1e6dfa51'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==45 and 'arXiv:2112.13479v1' in pdf[0].get_text()
    headings=[];hashes={}
    for n in range(1,32):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,321.86700439453125) if n==31 else page.rect
        txt=page.get_text(clip=clip)
        name=f'page-{n:02}.txt' if n<31 else 'page-31-before-appendix.txt'
        path=ROOT/'evidence'/name
        assert path.read_bytes().decode()==txt
        hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);m=re.match(r'^Theorem (\d+)\.',s)
                if m and line['spans'][0]['font']=='LMRoman10-Bold':headings.append((n,m[1]))
    assert headings==[(11,'1'),(12,'2'),(13,'3')]
    assert 'in press..' in txt and 'Further assumptions' not in txt
    assert 'Further assumptions' in pdf[30].get_text(clip=fitz.Rect(0,322,pdf[30].rect.width,339))
    path=ROOT/'theorem-inventory.json';assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED
    inv=json.loads(path.read_text());assert len(inv['claims'])==3
    assert [[e['page'] for e in c['evidence']] for c in inv['claims']]==[[11],[12,13],[13,14]]
    t=[c['statement_original'] for c in inv['claims']]
    assert all('B1-B4' in s for s in t)
    assert 'C1-C2' in t[0] and 'C1-C2' in t[1] and 'C1' not in t[2]
    assert all(f'({i})' in t[0] and f'({i})' in t[1] for i in ['i','ii','iii'])
    assert r'=1,\tag{3.28}' in t[1] and r'=\exp(-\exp(-v)),\tag{3.23}' in t[0]
    assert 'C3' not in t[1]
    assert t[1].count('under (3.7) it holds that')==2
    assert r'\tag{3.29}' in t[1] and r'\tag{3.30}' in t[1]
    assert r'\tag{3.33}' in t[2] and r'\tag{3.34}' in t[2]
    assert r'\min(p_1,m)\to\infty' in t[2] and r'\min(p_1,p_2,m)\to\infty' in t[2]
    for s in t:
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1646-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,d):(ROOT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,
        inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in inv['claims']],
        method='Independent bold-heading enumeration over admitted main text, visual comparison of all original statements including continuations, schema and math-fragment validation, and byte-exact reproduction.',
        evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,11,12,13,14,31]),
        notes=['The three Theorems contain three null partial-sum regimes, three alternative partial-sum regimes, and null/alternative maximum-statistic limits, respectively.',
               'Theorem 2 continues onto page 13 and Theorem 3 onto page 14. Their final almost-all-realizations clauses are included.',
               'Equations (3.23) and (3.28) print equalities rather than explicit probability limits; these are preserved under their asymptotic introduction.',
               'Theorem 2 names C1-C2 but not the immediately preceding C3. Its parts (ii) and (iii) explicitly specify (3.7) despite the broader opening reference.',
               'Theorem 3 names C2 without C1, and its alternative rate condition has a different minimum-of-dimensions limit from its distribution statements.',
               'B1-B4 are referred to the excluded supplement in the main text; their bodies remain unresolved. Appendix heading location does not authorize reading them.',
               'Reference entries continue above Appendix A on shared page 31; evidence is clipped above y=321.86700439453125.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',updated_at=now,theorem_count=3,source_pdf_sha256=SHA,
        next_action='Extract main-text model, alternatives, projected eigenvalues, transformations, conditional law, monitoring statistics and C assumptions. Keep B1-B4 unresolved and preserve printed equality, assumption-list and rate conventions.'))
    print('Three complete main-text Theorems independently validated; full census pending.')
if __name__=='__main__':main()
