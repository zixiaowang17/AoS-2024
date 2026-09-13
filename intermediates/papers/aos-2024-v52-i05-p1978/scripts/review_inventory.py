"""Independently check the frozen four-Theorem inventory against the registered source."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='e095eac5b303dead90e1a454a6b97bf1f5ac0e3e6072c5659341ef74f8981364'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==67
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['Debiased Inverse Propensity Score Weighting','Yuhao Wang','Rajen D. Shah','arXiv:2011.08661v3','11 Apr 2024','April 12, 2024']:assert s in first
    appendix_heading=pdf[29].get_text(clip=fitz.Rect(0,220,pdf[29].rect.width,245))
    assert 'Derivations and results relating to Sections' in appendix_heading
    assert 'References' in pdf[26].get_text(clip=fitz.Rect(0,390,pdf[26].rect.width,413))
    labels=[];hashes={}
    for n in range(1,28):
        clip=fitz.Rect(0,0,pdf[n-1].rect.width,380) if n==27 else None
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for s in line['spans']:
                    if s['font']=='CMBX10':
                        m=re.fullmatch(r'Theorem (\d+)\.',s['text'].strip())
                        if m:labels.append((n,m[1]))
    assert labels==[(10,'2'),(11,'3'),(13,'4'),(14,'5')]
    last=(ROOT/'evidence/page-27.txt').read_text()
    assert 'Acknowledgement' in last and 'improved the paper.' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims']
    assert [c['claim_id'] for c in cs]==[PID+'/T'+n for n in ['2','3','4','5']]
    assert [c['source_order'] for c in cs]==[1,2,3,4]
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[10],[11,12],[13,14],[14]]
    t2,t3,t4,t5=[c['statement_original'] for c in cs]
    for s in ['Assumptions 1–5',r'\hat\mu\in\mathbb R^n',r'\sqrt{\sigma_\mu^2+\bar\sigma^2}',r'\sqrt{s\log n}',r'c(p^{-m}+n^{-m})',r'\sigma_\mu^2\|\widehat{\boldsymbol\mu}-\boldsymbol\mu_{\mathrm{ORA}}\|_\infty+\bar\rho^3',r'(\sigma_\mu^2+\bar\sigma^2)^{3/2}']:
        assert s in t2,s
    assert 'Consider the setup of Theorem 2.' in t3 and '(i) of Theorem 2' in t3
    for s in [r'\delta+\sigma_\mu\zeta_1+\sigma\zeta_2',r'\mathbb P(\zeta_1\leq t\mid\mathcal D)',r'\mathbb P(\zeta_2\leq t)',r'\mathbb E(\zeta_1\zeta_2\mid\mathcal D)=0']:
        assert s in t3,s
    assert 'independent' not in t3 and r'\mathbb P(\zeta_2\leq t\mid' not in t3
    for s in ['Assumptions 1–7',r'c_\varepsilon>0',r'\sum_{j=1}^3\mathbb P(\Omega_j^c',r'for all $\alpha\in(0,1]$',r'\widetilde C_{\alpha/3}\mid\mathbf X',r'\frac{\sqrt{b_n\log p\log n}}{n^{1/4}}',r'+b_n+p^{-m}']:
        assert s in t4,s
    for s in ['as in Theorem 4','Assumptions 1–5',r'any sequence $(e_n)_{n=1}^\infty$',r'-2e^{-e_n^2}',r'\frac{e_n}{\sqrt n}\|\tilde\mu(\mathbf X)-\boldsymbol\mu_{\mathrm{ORA}}\|_2',r'\frac{\rho^3}{\sigma^3}']:
        assert s in t5,s
    assert 'Assumptions 1–7' not in t5 and r'\widetilde C' not in t5 and 'Corollary' not in t5
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1978-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=['Theorems 2-5 are the complete main-text inventory; all other numbered main-text results and appendix statements are excluded.','Theorem 3 part (iii) is on page 12; Theorem 4 conclusion is on page 14. Neither continuation is omitted.','Theorem 4 places the all-alpha conditional coverage guarantee on one high-probability event. The entire product b_n*log(p)*log(n) is inside its square root.','Theorem 5 refers to the estimator construction of Theorem 4 but explicitly assumes only 1-5. Its original statement does not restrict the sign of e_n; a later source review must retain that issue rather than rewrite the quantifier.','Source typography distinguishes the scalar mu notation in the opening of Theorem 2 from bold vectors in its norm. Matrix X is bold; the conditioning data D is calligraphic.','The constant-dependence footnote on page 10 is stored separately. This inventory gate does not certify completion of the definition/dependency census.']
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font enumeration, visual comparison of all complete statements, source-specific formula checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,10,11,12,13,14,27],last_page_clip=dict(page=27,y_max=380)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=notes))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2011.08661',registered_version_alias='2011.08661v3.pdf',checked_at=now))
    write('inventory-auxiliary-passages.json',dict(paper_id=PID,passages=[dict(local_id='inventory-footnote-2',statement_original='Here and below, the constants in the conclusions of our results may depend upon quantities introduced as constants in the relevant conditions for these results.',evidence=[dict(page=10,location='Footnote 2 attached to Theorem 2(i)')])]))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract main-text definitions, assumptions, auxiliary-data and cross-fit conventions; independently validate full census before completion.'))
    print('Four complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
