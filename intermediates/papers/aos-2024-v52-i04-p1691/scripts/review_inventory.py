"""Independently enumerate and validate the eight source-reviewed main-text Theorems."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
EXPECTED='486cab005e49ca17c132e9b3a0436ee6e49062627f3c616269d4a0330b5a08c2'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source);assert len(pdf)==67
    assert 'arXiv:2309.15300v1' in pdf[0].get_text() and '26 Sep 2023' in pdf[0].get_text()
    assert '834175' in pdf[28].get_text()
    assert 'SUPPLEMENTARY MATERIAL' in pdf[29].get_text(clip=fitz.Rect(0,0,pdf[29].rect.width,115))
    headings=[];hashes={}
    for n in range(1,30):
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode()==pdf[n-1].get_text()
        hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in pdf[n-1].get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);m=re.match(r'^THEOREM (\d+\.\d+)\.',s)
                if m:headings.append((n,m[1]))
    expected=[(10,'3.1'),(13,'4.1'),(15,'4.2'),(16,'4.3'),(17,'4.4'),(18,'4.5'),(20,'5.1'),(21,'5.2')]
    assert headings==expected
    path=ROOT/'theorem-inventory.json';assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED
    inv=json.loads(path.read_text());assert len(inv['claims'])==8
    assert [c['claim_id'] for c in inv['claims']]==[PID+':theorem-'+n for _,n in expected]
    assert [[e['page'] for e in c['evidence']] for c in inv['claims']]==[[p] for p,_ in expected]
    old=json.loads((ROOT/'prior-review/theorem-inventory.json').read_text())
    assert [c['statement_original'] for c in old['claims']]==[c['statement_original'] for c in inv['claims']]
    t={c['label']:c['statement_original'] for c in inv['claims']}
    assert '(3.5)' in t['Theorem 3.1'] and '(3.6)' in t['Theorem 3.1']
    assert 'Assumption 3.2' in t['Theorem 3.1'] and 'If, in addition' in t['Theorem 3.1']
    assert r'\beta|I_{h}^{\ast}(\mathsf{v})|\leq 1' in t['Theorem 3.1']
    assert r'M_{4+\delta}(\mu_{Y})' in t['Theorem 4.1'] and r'\tilde{\epsilon}_{n}^{-2}' in t['Theorem 4.1']
    assert 'for every' in t['Theorem 4.1'] and r'\alpha+(\beta d\vee 1)' in t['Theorem 4.1']
    assert '(4.1)' in t['Theorem 4.2'] and '(4.1)' in t['Theorem 4.4']
    assert r'\iota>1' in t['Theorem 4.3'] and r'\varpi>1' in t['Theorem 4.3']
    assert 'Assumptions 4.3–4.5' in t['Theorem 4.4']
    assert 'Granted the assumptions of Theorem 4.4' in t['Theorem 4.5']
    assert r'\underline{\lim}' in t['Theorem 5.1'] and 'for any estimator' in t['Theorem 5.1']
    assert r'(2\beta d\vee 1)+1' in t['Theorem 5.1']
    assert r'\tilde{\mu}_{1n}' in t['Theorem 5.2'] and 'large enough' in t['Theorem 5.2']
    for s in t.values():
        assert s.count('$')%2==0
        # An aligned row separator such as \\[-3pt] is not a display opener.
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        assert not any(ord(c)<32 and c!='\n' for c in s)
        for a,b in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1691-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,d):(ROOT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,
        theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,
        method='Independent enumeration of actual small-cap Theorem headings across main-text pages 1–29, followed by visual comparison of all eight full statements, mathematical-fragment checks, structural validation and exact reproduction.',
        evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,10,13,15,16,17,18,20,21,29]),
        validation=dict(returncode=result.returncode,stdout=result.stdout),
        notes=['Eight existing stable theorem IDs and all original statement strings retained after PDF comparison.',
               'Theorems 3.1 and 4.1 include both their initial and additional-regularity branches.',
               'Theorem 4.1 uses a moment sieve for the observation law mu_Y, not a substituted signal-law sieve.',
               'Theorems 4.2 and 4.4 also assert that (4.1) holds. Theorem 4.5 inherits the assumptions of 4.4 and strengthens iota and varpi.',
               'Theorem 5.1 has a liminf risk bound for every estimator, with the printed exponent and strict inequality. Theorem 5.2 uses the probability-valued approximate minimizer, not the raw signed kernel estimator.',
               'All eight statements end on their starting pages. No appendix or supplementary body was read; source issue and full dependency reviews are separate remaining stages.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',updated_at=now,theorem_count=8,source_pdf_sha256=SHA,
        next_action='Correct existing passage scope and graph, preserve auxiliary definitions, rebuild reproducibly, and independently review all source interfaces before completion.'))
    print('Eight main-text Theorems independently source-validated; full census revalidation remains pending.')
if __name__=='__main__':main()
