"""Check independent source enumeration and the visually reviewed theorem transcription."""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA
EXPECTED='8349a57759e496871c0e348cd64e1b05b021fa06a712235eaae9a9f54b540495'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source);assert len(pdf)==41
    assert 'arXiv:2209.04419v2' in pdf[0].get_text() and '4 Jun 2024' in pdf[0].get_text()
    assert 'Appendix' in pdf[28].get_text(clip=fitz.Rect(0,0,pdf[28].rect.width,95))
    assert '1004–1018' in pdf[27].get_text()
    headings=[];hashes={}
    for n in range(1,29):
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode()==pdf[n-1].get_text()
        hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for block in pdf[n-1].get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);m=re.match(r'^Theorem (\d+)',s)
                if m and line['spans'][0]['font']=='CMBX10':headings.append((n,m[1]))
    assert headings==[(12,'1'),(12,'2'),(15,'3'),(17,'4')]
    path=ROOT/'theorem-inventory.json';assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED
    inv=json.loads(path.read_text());t=[c['statement_original'] for c in inv['claims']]
    assert len(t)==4 and [[e['page'] for e in c['evidence']] for c in inv['claims']]==[[12],[12],[15],[17,18]]
    assert r'\widetilde s\ge\overline s' in t[1] and r'f_l(\boldsymbol Q_l^r,\overline Q_l)' in t[1]
    assert 'with respect to the randomness in the algorithm' in t[1]
    assert r'\lambda_N\ge C_1' in t[2] and r'\gamma_1>0' in t[2]
    assert r'\mathbb P(\boldsymbol\theta^*,C)' in t[2]
    assert r'\lambda_N=C_3' in t[3] and r'\max_{1\le j\le m}\lambda_j' in t[3]
    assert 'with probability tending to 1.' in t[3]
    assert r'\max_{l\in S^c}' in t[3] and r'|\boldsymbol\omega_{-l}|_1' in t[3]
    assert r'\boldsymbol\Sigma=\mathbb E\boldsymbol X\boldsymbol X^{\mathrm T}' in t[3]
    for s in t:
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        for a,b in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for c in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if c=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1671-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,
        theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,
        method='Independent bold-heading enumeration of pages 1–28; visual comparison of all four full statements and Theorem 4 continuation; source-specific formula checks, schema validation and exact reproduction.',
        evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,12,15,17,18,28]),
        validation=dict(returncode=result.returncode,stdout=result.stdout),
        notes=['Theorem 1 is a privacy property; Theorem 2 compares with the non-private majority vector and uses its support size, not the population support size.',
               'Theorems 3 and 4 are separate model-specific statements. Theorem 4 includes part (c) and the limiting conclusion on page 18.',
               'Theorem 3 prints the family as blackboard P despite calligraphic P in (10), includes an unused gamma_1, and gives only a lower bound for lambda_N. These are preserved.',
               'Theorem 4 preserves the random maximum of local lambda_j, the probability qualifier, the uncentered second-moment formula called covariance, and the printed omega_-l and Delta_0 notation.',
               'Lemma titles quoting external Theorems and other in-text theorem citations are not theorem environments. No appendix body was inspected.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',updated_at=now,theorem_count=4,source_pdf_sha256=SHA,
        next_action='Complete algorithm and distribution-family source extraction, local dependency graph and independent full source review.'))
    print('Four complete main-text Theorems independently validated.')
if __name__=='__main__':main()
