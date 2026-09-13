"""Independently enumerate and source-validate the three original theorem statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='187436ed57566fc3ee411e46a91cccb8ae22303cf6627a611dad6711930f3d5c'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==54
    first=' '.join(pdf[0].get_text().split())
    for v in ['SKEWED BERNSTEIN–VON MISES THEOREM','DANIELE DURANTE','FRANCESCO POZZA','BOTOND SZABO','arXiv:2301.03038v3','8 Apr 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2301.03038v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2301.03038'
    assert [x for x in pdf.get_toc() if x[1] in ['References','Proofs of Lemmas, Theorems and Corollaries']]==[[1,'References',29],[1,'Proofs of Lemmas, Theorems and Corollaries',32]]
    assert any(248<b.y0<249 for b in pdf[28].search_for('REFERENCES'))
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,242) if n==29 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']).strip();match=re.match(r'^THEOREM\s+(\d+\.\d+)\b',text)
                if match:
                    assert all(x['font']=='NimbusRomNo9L-Regu' for x in line['spans'])
                    labels.append([n,match[1]])
    expected=[[11,'2.1'],[22,'4.1'],[25,'4.5']];assert labels==expected,labels
    end=(ROOT/'evidence/page-29.txt').read_text();assert 'approximation still within the SKS class.' in end and 'REFERENCES' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==3
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'2.1':[r'h=\delta_n^{-1}(\theta-\theta_*)',r'M_n=\sqrt{c_0\log\delta_n^{-1}}','Assumptions 1–4','inner point',r'O_{P_0^n}(M_n^{c_3}\delta_n^2)',r'\xi=\Delta_{\theta_*}^n+\delta_n(V_{\theta_*}^n)^{-1}\log\pi^{(1)}',r'\Omega^{-1}=[v_{st}^n-\delta_na_{\theta_*,stl}^{(3),n}\xi_l]',r'(\delta_n/12\eta)',r'(h-\xi)_s(h-\xi)_t(h-\xi)_l+3(h-\xi)_s\xi_t\xi_l',r'F(-x)=1-F(x)',r'F(x)=1/2+\eta x+O(x^2)',r'\eta\in\mathbb R'],
'4.1':[r'\widehat h=\sqrt n(\theta-\widehat\theta)',r'M_n=\sqrt{c_0\log n}','Assumptions 1, 7–8, and 9–10',r'O_{P_0^n}\left(M_n^{c_8}/n\right)','defined as in (22)',r'|G(\widehat h)|\lesssim\|\widehat h\|^r',r'\pi(\widehat\theta+\widehat h/\sqrt n)',r'\int G(\widehat h)|\pi_n(\widehat h)-\widehat p_{\mathrm{SKS}}^n(\widehat h)|',r'O_{P_0^n}(M_n^{c_8+r}/n)'],
'4.5':[r'\Pi_{n,C}(S)=\int_S\pi_{n,C}(\widehat h_C)\,\mathrm d\widehat h_C',r'S\subset\mathbb R^{d_C}','under the assumptions of Theorem 4.1',r'O_{P_0^n}\left(M_n^{c_9}/n\right)',r'\widehat P_{\mathrm{SKS},C}^n(S)=\int_S\widehat p_{\mathrm{SKS},C}^n(\widehat h_C)', 'defined as in (31)']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert r'\int |G' not in s['4.1'] and 'Assumptions 5' not in s['4.1']
    assert 'Theorem C.1' not in ''.join(s.values()) and r'\eta>0' not in s['2.1']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2714-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent actual small-cap heading enumeration, visual comparison of all three complete statements, source-specific formula/reference checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,11,22,25,29],main_text_end_page=29,last_page_clip_y=242),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Exactly three original Theorems; the numbering jumps to4.5 because intervening numbered items are remarks. Lemmas and corollaries are excluded.','Theta_* has a subscript star. Theorem2.1 retains general delta_n scaling, Einstein-index contractions, eta in R and both symmetry/local expansion requirements for F.','Theorem4.1 includes both total variation and the signed-G weighted absolute density-difference integral. Do not replace the integrand by |G|, drop its prior moment condition, or import Assumptions5–6.','Theorem4.5 imports Theorem4.1 assumptions and targets the marginal approximation(31). Supplementary Theorems C.1/C.6 are not inventoried.','Main text continues onto29, before references at y248.679; clipped242. Supplementary bodies starting32 are not read.','Inventory validated; original definitions, assumptions, marginal coefficients, local dependencies and full census review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=3,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original SKS density, posterior setup and pseudo-true parameter, Assumptions1–4 and7–10, MAP/skew-modal approximation(22), and marginal construction(27)–(31). Preserve distinct general versus regular/MAP conditions and all index conventions. Finalize, reproduce and independently source-review.'))
    print('Three complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
