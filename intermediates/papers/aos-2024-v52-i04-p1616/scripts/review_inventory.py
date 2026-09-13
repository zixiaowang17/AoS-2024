"""Record the independent main-text theorem inventory review."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
EXPECTED='268ff5b29670f04643defc849238116786a741498cc19ee784fbe29afa31e991'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==47 and 'arXiv:2212.12848v3' in pdf[0].get_text()
    assert any('Appendix A.' in title and n==29 for _,title,n in pdf.get_toc())
    headings=[];hashes={}
    for n in range(1,29):
        page=pdf[n-1];path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode()==page.get_text()
        hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                s=''.join(x['text'] for x in l['spans'])
                m=re.match(r'^Theorem (\d+) \(',s)
                if m and l['spans'][0]['font']=='TeXGyreTermesX-Bold':headings.append((n,m[1]))
    assert headings==[(9,'1'),(9,'2'),(11,'3')]
    assert '[ZMGS22]' in pdf[27].get_text() and '7257' in pdf[27].get_text()
    assert 'Appendix A. Proof of Proposition 1' in pdf[28].get_text(clip=fitz.Rect(0,0,pdf[28].rect.width,100))
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED
    inv=json.loads(path.read_text())
    assert len(inv['claims'])==3
    assert [c['claim_id'] for c in inv['claims']]==[PID+':theorem-'+str(i) for i in range(1,4)]
    t=[c['statement_original'] for c in inv['claims']]
    assert r'\mathsf{S}^{2}_{\varepsilon}' in t[0] and 'infimum is achieved' in t[0]
    assert r'9\left\lceil\frac{d_{x}}{2}\right\rceil+11' in t[1]
    assert r'9\left\lceil\frac{d_{x}\vee d_{y}}{2}\right\rceil+11' in t[1]
    assert 'without the square' in t[2] and 'Furthermore' in t[2]
    assert t[2].count(r'\sup_')==2 and r'(d_{x}\wedge d_{y})\vee 4' in t[2]
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1616-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,
        inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in inv['claims']],
        method='Independent bold-heading enumeration, PDF visual comparison of all three complete theorem statements, schema validation and exact reproduction.',
        evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,9,11,28]),
        notes=['Exactly three main-text Theorems. Regular-font theorem citations, Propositions, Corollary 1 and main-text Lemmas are excluded.',
               'Theorem 2 exponents are nine times the indicated ceiling plus eleven, not nine times the sum with eleven; the original transcription agrees with the PDF.',
               'Theorem 3 includes both upper bounds, the separated unsquared-distance clause and both lower bounds on the same page.',
               'Theorem 1 concerns the decomposition component S_epsilon^2; its superscript is a component label rather than a square. The preceding centering convention requires separate extraction.',
               'Existing theorem IDs and original statement bodies are retained after fresh source comparison. Full census revalidation remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',updated_at=now,theorem_count=3,source_pdf_sha256=SHA,prior_artifacts='prior-review',next_action='Complete centering and decomposition dependency context, reproduce source passages and independently validate the full census.'))
    print('Three original Theorems independently source-validated; full census review pending.')
if __name__=='__main__':main()
