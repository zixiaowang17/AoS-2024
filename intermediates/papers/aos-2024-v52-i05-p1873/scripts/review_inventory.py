"""Validate the frozen inventory after a separate visual source comparison.

Source review and proof certification are distinct; this script does not prove results.
"""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='269b267b5c612714f0d1d938a7f1d86ded73b77a27f714f3b2bd48ed738af055'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==103
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for x in ['Spectral Statistics of Sample Block Correlation Matrices','Zhigang Bao','Jiang Hu','Xiaocong Xu','Xiaozhuo Zhang','arXiv:2207.06107v2','8 Sep 2022']:assert x in first,x
    # Inspect the appendix heading only, not its body.
    assert 'APPENDIX A.' in pdf[33].get_text(clip=fitz.Rect(0,188.4,pdf[33].rect.width,201))
    headings=[];hashes={}
    for n in range(1,35):
        p=pdf[n-1];clip=fitz.Rect(0,0,p.rect.width,188.4) if n==34 else p.rect
        s=p.get_text(clip=clip);f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==s;hashes[str(n)]=digest(f)
        if n==34:assert '(110)' in s and 'APPENDIX' not in s
        for block in p.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    m=re.fullmatch(r'Theorem (\d+\.\d+)\.?',span['text'].strip())
                    if m and span['font']=='URWPalladioL-Bold':headings.append((n,m[1]))
    expected=[(5,'1.9'),(7,'1.11'),(9,'1.17'),(9,'1.18'),(10,'1.20'),(29,'5.3')]
    assert headings==expected,headings
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==6
    assert [c['claim_id'] for c in cs]==[PID+'/T'+n for _,n in expected]
    assert [c['source_order'] for c in cs]==list(range(1,7))
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[5,6],[7],[9],[9],[10],[29]]
    paper=inv['papers'][0];assert paper['source_url']==URL and paper['main_text_last_pdf_page']==34
    assert paper['main_text_boundary']['shared_page_with_appendix'] is True
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    assert all(x in t['1.9'] for x in ['fixed integer','Case 1','Case 2',r'p_t\leq N^{1-\epsilon}',r'\operatorname{Ber}(\hat y_t)',r'{2x}',r'(1-\hat y)_+\delta_0','converge weakly','Section 1.5'])
    assert r'\pi' not in t['1.9']
    assert all(x in t['1.11'] for x in ['(19)','(20)','(21)',r'\sigma_f^2>c',r'\frac1{4\pi i}',r'\frac{(k-1)m_\boxplus',r'\hat y\in(0,\infty)'])
    assert all(x in t['1.17'] for x in [r'p_{\max}\leq N^{1/2-\epsilon}',r'\mu_{\mathrm{mp},y}',r'\frac{Ny_t^2}{1-y_t}',r'+y\frac{(m_y\'(z))^2' .replace('\\\'',"'"),r'-\frac{ym_y',r'\sigma_f^2>c'])
    assert all(x in t['1.18'] for x in [r'\hat H:=',r'p_t/(N-1)',r'(N-1)\int',r'-\frac1z',r'\tilde\sigma_f^2>c','Proposition 1.5','Corollaries 1.14 and 1.15','simultaneously'])
    assert t['1.20']=='Theorems 1.11, 1.17, 1.18 and Corollaries 1.14, 1.15 still hold under Assumptions 1.19 and 1.7.'
    assert all(x in t['5.3'] for x in ['(88)','(89)','(90)',r'\alpha_t(z)=\mathbb E^\chi',r'\beta_t(z)=\frac1{1-y_t}',r'\operatorname{Tr}f(H)-\oint_{\bar\gamma_1^0}',r'\partial_{z_2}\frac',r'\operatorname{tr}Q_tG(z_1)P_tG(z_2)',r'\hat y\in(0,\infty)'])
    assert 'some small constant' not in t['5.3'] and 'Proof' not in t['5.3']
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1873-inventory-',dir='/private/tmp') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
      'Six actual main-text Theorems: 1.9, 1.11, 1.17, 1.18, 1.20 and 5.3. Theorem 5.3 is inside Section 5, not an appendix. Main text ends after equation (110) above Appendix A on page 34.',
      'Theorem 1.9 contains a general moment statement and two weak-convergence cases. Its Marchenko-Pastur density denominator is printed as 2x, without pi; this apparent source error is retained.',
      'Theorem 1.11 preserves both contour regimes, positive variance qualification and every term of (20)-(21), including the order dz2 dz1.',
      'Theorem 1.17 uses finite y rather than limiting hat-y. The y in the second mean term multiplies the entire fraction, including both numerator terms; visual inspection resolves misleading plain-text extraction. Its pmax threshold is N^(1/2-epsilon).',
      'Theorem 1.18 retains the unknown-mean matrix, N-1 normalization, tilde Bernoulli laws, -1/z mean correction, Proposition 1.5 subordination reference and the simultaneous B/N substitutions for both Corollaries.',
      'Theorem 1.20 is a whole inherited conclusion under replacement Assumption 1.19 and dimensional Assumption 1.7. Corollaries 1.14 and 1.15 require auxiliary source preservation, not additional Theorem records.',
      'Theorem 5.3 defines alpha, beta and K inline and uses the truncated expectation and clipped contours from main text. Its printed centering contour integral has no Cauchy prefactor; the proof below uses -1/(2 pi i), but the statement is not repaired. Unlike earlier CLTs it prints no positive-variance qualification.',
      'Definition extraction, inherited-conclusion resolution and complete graph/source review remain pending; inventory validation does not complete the paper.'
    ]
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=headings,method='Independent actual-heading enumeration across all main-text pages and visual comparison of all six statements; frozen transcription checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,5,6,7,9,10,29,34],page34_clip_y_max=188.4),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=notes))
    write('evidence/source-provenance.json',dict(paper,cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2207.06107',registered_version_alias='2207.06107v2.pdf',source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=6,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract main-text matrix and spectral definitions, separate the moment assumptions and both contour regimes, resolve inherited Corollaries; independently review the resulting full local graph.'))
    print('Six main-text Theorems source-validated; definition census remains pending.')
if __name__=='__main__':main()
