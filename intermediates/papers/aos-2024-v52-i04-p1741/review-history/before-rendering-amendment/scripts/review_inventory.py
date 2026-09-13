"""Record and verify the independent main-text theorem inventory comparison."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='b9936be921578f5e6b5597a6fea0065ebac237a120fc17b6a30a237d415d2460'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==33
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(s in first for s in ['2024, Vol. 52, No. 4, 1741–1773','10.1214/24-AOS2415','EUN RYUNG LEE','SEYOUNG PARK','ENNO MAMMEN','BYEONG U. PARK'])
    assert 'APPENDIX: PROOFS OF MAIN THEOREMS' in pdf[24].get_text(clip=fitz.Rect(0,200,486,220))
    headings=[];hashes={}
    for n in range(1,26):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,204.59) if n==25 else page.rect
        s=page.get_text(clip=clip);f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==s;hashes[str(n)]=digest(f)
        if n==25:assert 'a promising avenue for future research.' in s and 'APPENDIX:' not in s
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']);m=re.match(r'^THEOREM (\d+)\.',text)
                if m:headings.append((n,int(m[1])))
    assert headings==[(8,1),(11,2),(16,3),(16,4),(17,5),(18,6),(18,7)]
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==7
    assert inv['papers'][0]['source_url']==URL and inv['papers'][0]['main_text_last_pdf_page']==25
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix']
    assert [c['claim_id'] for c in cs]==[PID+f'/T{i}' for _,i in headings]
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[p] for p,_ in headings]
    t=[c['statement_original'] for c in cs]
    assert r'$R<\infty$' in t[0] and r'$q_0>0$' in t[0]
    assert r'\int_0^1\eta_j(x_j)\widehat p_j(x_j)dx_j=0' in t[0]
    assert r'\frac{2R^2(1+q_0)^2}{r}' in t[0] and r'\frac1{2R^2(1+q_0)^2}-1' in t[0]
    assert 'for all $r\\geq1$' in t[0]
    assert '(A1)–(A6)' in t[1] and r'$\phi>0$ for all $d$' in t[1]
    assert r'\frac{|S|}{\phi\wedge1}' in t[1] and r'\frac{\phi^2\wedge1}{|S|^2}' in t[1]
    assert r'\lambda\geq2C_1' in t[1] and r'\log(|S|\vee n)' in t[1]
    assert '(A1)–(A7)' in t[2] and 'bounded away from zero' in t[2]
    assert '(2.20)' in t[2] and '(2.21)' in t[2] and r'(1+s_1)' in t[2]
    assert all('conditions of Theorem 3' in s and '(2.20)' in s and '(2.21)' in s for s in t[3:5])
    assert r'\frac{n^{-1/5}}{|S|^{2/5}(1+s_1)^{2/5}}' in t[3]
    assert 'for each fixed $x_j\\in(0,1)$' in t[3] and r'\sqrt{nh_j}' in t[3]
    assert r'$(1+s_1^2)nh^3\to0$' in t[4] and r'\sup_{x_j\in[0,1]}' in t[4]
    assert '(A1), (A2), (A4), (A5) and (A7)' in t[5]
    assert 'additional assumption' in t[5] and 'additional constraint' in t[5] and '(3.7)' in t[5]
    assert r'\Theta_{jk}\x27\x27' not in t[5] # literal primes, not encoded replacement text
    assert r'(\gamma s_1)^{3/4}' in t[5] and r's_q(\gamma s_1)^{3(1-q)/4}' in t[5]
    assert r'$q\in[0,1]$' in t[5] and r'$q\in(0,1]$' in t[6]
    assert 'some permutation' in t[6] and r'\|(p_{jk}-p_jp_k)/p_j\|_\infty' in t[6]
    assert r's_q\vee s_q^*\leq\beta' in t[6]
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
    with tempfile.TemporaryDirectory(prefix='p1741-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=headings,
        method='Independent small-cap heading enumeration throughout admitted main text; visual comparison of all seven complete theorem statements, source-specific branch and formula checks, structural validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,8,11,16,17,18,25],page25_clip_y_max=204.59),validation=dict(returncode=result.returncode,stdout=result.stdout),
        notes=['All seven statements end on their starting pages. Propositions, unnumbered normal-limit consequences and citations are not inventoried.',
               'The conclusion extends to page 25; appendix material begins below the clipped main-text endpoint and was not read.',
               'Theorem 1 retains its exact nonasymptotic max expression, including the minus one outside the fraction.',
               'Theorem 2 has a sum of component errors, whereas Theorem 3 has a maximum; their compatibility hypotheses differ.',
               'Theorem 4 is pointwise on the open interval; Theorem 5 is uniform on the closed interval and adds a distinct bandwidth condition.',
               'Theorem 6 has an initial operator bound and a second branch with additional true-kernel regularity and an additional optimization constraint. Its q range includes zero.',
               'Theorem 7 uses q in (0,1], a relabeling of coordinates and a population density-ratio bound; no unstated A assumptions were inserted.',
               'Source definitions, operator conventions, dependency paths and full census review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=7,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract source definitions, A1–A7, operator conventions and algorithm dependencies; validate the full census independently before completion.'))
    print('Seven main-text Theorems independently source-validated; full census pending.')
if __name__=='__main__':main()
