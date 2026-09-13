"""Independently verify the six-theorem inventory and retain source-review evidence."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='4e84e039b6f8f6c7f0a7857f5c659e943541f53f180202ed2a005b49c4bc4d76'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==51
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(s in first for s in ['Learning Gaussian Mixtures Using the Wasserstein-Fisher-Rao Gradient Flow','Yuling Yan','Kaizheng Wang','Philippe Rigollet','January 5, 2023','arXiv:2301.01766v1','4 Jan 2023'])
    assert 'Preliminaries' in pdf[14].get_text(clip=fitz.Rect(0,520,612,540))
    headings=[];hashes={}
    for n in range(1,16):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,520.1) if n==15 else page.rect
        s=page.get_text(clip=clip);f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==s;hashes[str(n)]=digest(f)
        if n==15:assert 'Figure 5:' in s and '3.8 ≤x ≤4.1.' in s and 'Preliminaries' not in s
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']);m=re.match(r'^Theorem (\d+)(?:\.| \()',text)
                if m and line['spans'][0]['font']=='SFBX1000':headings.append((n,int(m[1])))
    assert headings==[(3,1),(6,2),(6,3),(8,4),(8,5),(9,6)]
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==6
    assert inv['papers'][0]['source_url']==URL and inv['papers'][0]['main_text_last_pdf_page']==15
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix']
    assert [c['claim_id'] for c in cs]==[PID+f'/T{i}' for _,i in headings]
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[3],[6],[6,7],[8],[8],[9]]
    t=[c['statement_original'] for c in cs]
    assert '1. (Existence)' in t[0] and '2. (Optimality condition)' in t[0]
    assert 'if and only if (i)' in t[0] and '(ii)' in t[0] and r'$\widehat\rho$-a.e.' in t[0]
    assert all(r'\operatorname{supp}(\rho_0)=\mathbb R^d' in t[i] and r'\rho_n\xrightarrow{\mathrm w}\widehat\rho' in t[i] for i in [1,3])
    assert 'There exists $\\eta_0>0$' in t[1] and 'There exists $\\eta_0$' in t[3]
    assert '(3.7)' in t[1] and '(3.12)' in t[3]
    assert t[2].count(r'\sum_{l=1}^m\omega_t^{(j)}\phi')==2
    assert t[5].count(r'\sum_{l=1}^m\omega_t^{(j)}\phi')==1
    assert r'\sum_{l=1}^m\omega_t^{(l)}\phi' in t[4]
    assert all('has unique solution on any time interval $[0,T]$' in t[i] for i in [2,4,5])
    assert all('distributional solution' in t[i] for i in [2,4,5])
    assert '(3.6)' in t[2] and '(3.11)' in t[4] and '(3.18)' in t[5]
    assert r'\rho_t:=\frac1m\sum_{l=1}^m\delta_{\mu_t^{(l)}}' in t[5]
    assert 'Uniform' in t[2] and 'Uniform' in t[5] and 'Uniform' not in t[4]
    assert r'\omega_0=[\omega_0^{(j)}]_{1\leq j\leq m}\in\Delta^{m-1}' in t[2] and r'\in\Delta^{m-1}' in t[4]
    for s in t:
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1774-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=headings,method='Independent bold-heading enumeration throughout admitted main text and visual comparison of the six complete original theorem statements, including the page-7 ending of Theorem 3. Source-specific checks, structural validation and byte-exact reproduction passed.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,3,6,7,8,9,15],page15_clip_y_max=520.1),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=[
        'The registered file is arXiv v1, not the published journal text. Its title-page date is January 5, 2023 and the arXiv stamp is 4 Jan 2023. The version-specific URL identifies the inspected source.',
        'Only Theorems 1–6 occur in the main text. Citations to Theorems 7 and 8 are not theorem environments; appendix headings were inspected solely to locate the boundary, without reading appendix bodies.',
        'Theorem 1 has existence and both optimality conditions; the adjacent remark does not replace the original statement.',
        'Theorems 2 and 4 require weak convergence to a limit before identifying it as an NPMLE. They do not establish that convergence occurs.',
        'Theorem 4 uses eta and eta0, while its referenced iteration (3.12) uses gamma. It also omits the explicit positivity assertion on eta0 printed in Theorem 2. Both differences are preserved.',
        'Theorems 3 and 6 print omega_t^(j) inside a sum over l in their denominators. Theorem 5 instead prints omega_t^(l). These source indices were visually checked and not corrected.',
        'Theorem 6 uses equal weights 1/m in its measure formula but contains omega_t^(j) in its ODE without defining its dynamics in that theorem. This remains a source issue.',
        'Theorem 3 continues to the first sentence on page 7 before Algorithm 1. Theorems 5 and 6 end on their starting pages.',
        'Main-text Figure 5 ends on page 15 before Appendix A. The saved clip excludes the appendix heading and body.',
        'Definitions, auxiliary conventions and theorem dependency audit remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2301.01766',registered_version_alias='2301.01766v1.pdf',source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=6,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract main-text probability-measure conventions, NPMLE and first variation, gradient updates/PDEs, and source issues; build and independently validate their theorem dependencies.'))
    print('Six main-text Theorems independently source-validated; full census pending.')
if __name__=='__main__':main()
