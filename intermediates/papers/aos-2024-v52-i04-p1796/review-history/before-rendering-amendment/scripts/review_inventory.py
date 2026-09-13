"""Independently check both complete theorem statements against the pinned source."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='bb179114b7bd4773c56a3597c032027326b02bcf2d586bba60fc77375b8eeb12'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==96
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(s in first for s in ['Efficient and Multiply Robust Risk Estimation under General Forms of Dataset Shift','Hongxiang Qiu','Eric Tchetgen Tchetgen','Edgar Dobriban','arXiv:2306.16406v4','8 Jun 2024'])
    assert 'References' in pdf[32].get_text(clip=fitz.Rect(0,620,612,640))
    headings=[];hashes={}
    for n in range(1,34):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,620.7) if n==33 else page.rect
        s=page.get_text(clip=clip);f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==s;hashes[str(n)]=digest(f)
        if n==33:assert 'Medical Research Council).' in s and 'References' not in s
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']);m=re.match(r'^Theorem (\d+)(?:\.| \()',text)
                if m and line['spans'][0]['font']=='CMBX12':headings.append((n,int(m[1])))
    assert headings==[(17,1),(26,2)]
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==2
    assert inv['papers'][0]['source_url']==URL and inv['papers'][0]['main_text_last_pdf_page']==33
    assert not inv['papers'][0]['main_text_boundary']['shared_page_with_appendix']
    assert [c['claim_id'] for c in cs]==[PID+'/T1',PID+'/T2']
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[17,18],[26,27]]
    t1,t2=[c['statement_original'] for c in cs]
    assert all(f'({n})' in t1 for n in range(18,23))
    assert r'\sum_{k=1}^K\mathbb E_{P_*}' in t1 and r'h_v^{k-1}(\bar Z_{k-1})-\widehat\ell_v^k(\bar Z_k)' in t1
    assert r'\Delta:=n^{-1}\sum_{v=1}^V|I_v|\Delta_v' in t1
    assert r'\frac{|I_v|\sum_{a\in\mathcal S\x27_1}\pi_*^a}{n\sum_{a\in\mathcal S\x27_1}\pi_v^a}'.replace(r'\x27',"'") in t1
    assert r'\sum_{k=2}^K B_{k,v}' in t1
    assert 'for all $n,k,v$' in t1 and r'\mathbb E_{P_*}|D_{\mathrm{GSC}}' in t1 and r'|^3<\infty' in t1
    assert r'a_{n,k,v}b_{n,k,v}+a_{n,k,v}+b_{n,k,v}+n^{-1}' in t1
    assert r'a_{n,k,v}b_{n,k,v}+n^{-1/2}(a_{n,k,v}+b_{n,k,v})+n^{-1}' in t1
    assert r'2\Phi\left(-\sqrt n\frac{t-' in t1 and r'\frac{\mathcal C_2}{\sqrt n}' in t1
    assert '1. Efficiency:' in t1 and '2. Multiply robust consistency:' in t1
    assert 'Additionally under Condition DS.0' in t1 and r'$\Delta=0$' in t1
    assert 'Under Condition ST.1' in t1 and 'Under Condition ST.2' in t1
    assert r'D_{\mathrm{GSC}}' in t1 and r'D_{\mathrm{SC}}' in t1 and r'\widehat r-\Delta\xrightarrow{p}r_*' in t1
    foot=cs[0]['source_footnotes'];assert len(foot)==1 and foot[0]['label']=='6'
    assert 'nonzero with probability tending to one exponentially' in foot[0]['statement_original']
    assert r'\max_{v\in[V]}\|\widehat{\mathcal E}^{-v}-\mathcal E_\infty\|_{L^2(P_*)}=o_p(1)' in t2
    assert 'Under Condition DS.1' in t2 and 'Line 5 of Algorithm 1' in t2
    assert r'\frac{\mathbb E_{P_*}[\mathcal E_\infty(X)]-r_*}{\rho_*}(1-A_i-\rho_*)' in t2
    assert r'\frac{\widehat\rho^v-\rho_*}{\widehat\rho^v}' in t2
    assert r'D_{\mathrm{Xcon}}(\widehat\rho^{-v},\widehat{\mathcal E}^{-v},\widehat r_{\mathrm{Xcon}}^v)' in t2
    assert r'\mathcal B' in t2 and r'=o_p(n^{-1/2})' in t2
    assert r'\mathcal E_\infty=\mathcal E_*' in t2 and '(26)' in t2
    for s in [t1,t2,foot[0]['statement_original']]:
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1796-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=headings,method='Independent bold-heading enumeration across all main-text pages and visual comparison of both complete multi-page Theorems; source-specific formula checks, structural validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,17,18,26,27,33],page33_clip_y_max=620.7),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=[
        'Only Theorems 1 and 2 are main-text theorem environments. Propositions, Corollaries, Lemmas and supplemental references are excluded.',
        'Theorem 1 starts on page 17 and ends on page 18 after its final DS.0 statement; its footnote 6 is retained in source_footnotes with independent page evidence.',
        'Theorem 1 preserves the k=1 start in Delta_v versus k=2 in drift sums, the full expansion (19), three finite-sample hypotheses, confidence bound (20), both influence-function expansions (21)/(22) and the consistency branch.',
        'The threshold on t has a+b, while the Gaussian-tail bound uses n^{-1/2}(a+b). The last denominator in (19) prints pi_v^a without a hat; these differences are preserved.',
        'Theorem 1 does not globally assume DS.0: it first treats the bias-corrected estimator r-hat minus Delta, then states Delta=0 additionally under DS.0.',
        'Theorem 2 begins on page 26 and ends with its efficiency specialization (26) on page 27. It allows a common L2 limit E-infinity that need not equal E-star in its initial RAL assertion.',
        'Theorem 2 remainder uses in-fold rho-hat^v in its first term and out-of-fold rho-hat^{-v} in the D_Xcon argument. The Section 4 Algorithm 1 uses in-fold rho-hat^v; the discrepancy is preserved for later source-issue review.',
        'Repeated Algorithm 1 labels refer to different source locations. Theorem 1 references the general Section 3 algorithms; Theorem 2 references the Section 4 algorithm on page 26.',
        'Main text and acknowledgements end on page 33 before References. The bibliography and Supplemental Material are excluded; no supplemental body was read.',
        'Definitions, statistical conditions, estimator construction and full theorem dependency audit remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2306.16406',registered_version_alias='2306.16406v4.pdf',source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract target-risk model, DS.0/DS.0-dagger and DS.1, pseudo-losses/influence functions, general and concept-shift algorithms, drift terms and ST.1/ST.2. Then build and independently validate the full theorem graph.'))
    print('Both main-text Theorems independently source-validated; full census pending.')
if __name__=='__main__':main()
