"""Validate the independently enumerated and visually compared theorem inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
EXPECTED_INVENTORY_SHA='11eb2a11a9d614fc5e5cc529e152c6603e82877fe61100369c047497a0f0924a'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==86 and 'arXiv:2109.13601v2' in pdf[0].get_text()
    headings=[];hashes={}
    for n in range(1,34):
        p=pdf[n-1];text=p.get_text()
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode()==text
        hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in p.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                m=re.match(r'^Theorem (\d+)(?:\.| \()',s)
                if m and line['spans'][0]['font']=='CMBX10':
                    headings.append((n,m[1]))
    assert headings==[(10,'1'),(11,'2'),(12,'3'),(15,'4'),(16,'5'),(17,'6'),(22,'7'),(23,'8'),(24,'9')]
    assert '[48]' in text and '393' in text and '424' in text
    header=pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,155))
    assert 'This supplementary material' in header and 'S-1.' in header
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert len(inv['claims'])==9 and inv['papers'][0]['main_text_last_pdf_page']==33
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert all(r'\overline\Phi(b)' in t[n] for n in ['1','2','3','7'])
    assert r'b=b_n\to-\infty' in t['1'] and r'b=b_n\to-\infty' not in t['2']
    assert all(r'\underline{\lim}_n B_n>1' in t[n] for n in ['3','6'])
    assert r'\mathcal S_B(\Theta_b)' in t['3']
    assert [e['page'] for e in inv['claims'][3]['evidence']]==[15,16]
    assert 'Assumption 1A' in t['4'] and 'Assumption 1B' in t['4']
    assert r'2\Lambda_n(\boldsymbol a)-1+o(1)' in t['4']
    assert r'\mathbf 1\{|X_i|>a_n^*\}' in t['4']
    assert 'Finally, if we instead grant Assumption 1B' in t['5']
    assert r'\alpha_n+\exp\left(-(1-\Lambda_n(\boldsymbol a))^2s_n/32\right)' in t['5']
    assert 'conclusions of Theorem 4 hold' in t['6'] and r'\overline F_0(a_n^*-\delta_n)' in t['6']
    assert r"\Theta'_b" in t['7'] and r'E_\theta\mathrm L_{\mathrm C}' in t['7']
    assert r'\varphi^{\widehat\ell}' in t['7'] and r'\varphi^{BH}' in t['7']
    assert [e['page'] for e in inv['claims'][7]['evidence']]==[23,24]
    assert r'(0,r/2^\zeta)' in t['8'] and r'\kappa^{1/\zeta})^\zeta-\kappa=\beta' in t['8']
    assert r'n^{-\kappa}/(\log n)^{1-1/\zeta}' in t['8']
    assert all(f'({s})' in t['9'] for s in ['i','ii','iii','iv'])
    assert 'polynomial in $n$' in t['9'] and r'\kappa(r,\beta,2)<1-\beta' in t['9']
    for s in t.values():
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(c)<32 and c!='\n' for c in s)
        for d,i in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for c in re.findall(r'(?<!\\)[{}]',d+i):
                depth+=1 if c=='{' else -1
                assert depth>=0
            assert depth==0
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1564-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,d):(ROOT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent bold-heading enumeration across the main paper and visual comparison of every complete statement, with schema, mathematical-fragment and byte-exact reproduction checks.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,10,11,12,15,16,17,22,23,24,33],boundary_crop='evidence/supplement-boundary.png'),notes=[
      'The inventory contains nine main-text Theorems, with Theorem 4 continuing to page 16 and Theorem 8 continuing to page 24. Theorem 7 ends on page 22 and Theorem 9 ends on page 24.',
      'The source uses upper-tail Phi-bar, Fraktur R for the combined risk, bold italic a for the strength vector, calligraphic S for procedure classes, and underlined lim for liminf in Theorems 3 and 6.',
      'Theorem 5 includes its uniform bound, explicit error expression and Assumption 1B replacement clause. Theorem 6 incorporates both branches of Theorem 4 with a restricted class and FNR loss.',
      'Theorem 9 is itself a summary theorem. All four points and the polynomial-loss sentence are preserved; precise supplementary statements are not substituted.',
      'The main paper ends after reference [48] on page 33. Supplementary theorem labels encountered during initial heading location are excluded; no supplementary theorem body is used as census content.',
      'BH and empirical Bayes procedure references S-18 and S-29 require scope-aware resolution using the available main-text description. Full supporting-passage and dependency review remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2109.13601v2.pdf',registered_url_alias='https://export.arxiv.org/pdf/2109.13601',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=9,source_pdf_sha256=SHA,next_action='Extract the sparse model and risks, Gaussian/Subbotin cases, parameter classes, Assumption 1A/1B, sparsity-preserving procedures, main-text BH/empirical Bayes descriptions and large-signal adaptation context. Preserve unresolved supplement-only details.'))
    print('Nine complete main-text theorem statements independently validated; full census remains pending.')
if __name__=='__main__':main()
