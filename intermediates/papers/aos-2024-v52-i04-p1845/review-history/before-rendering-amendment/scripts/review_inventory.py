"""Independently check the frozen nine-Theorem inventory against registered arXiv v2.

Checks record a completed manual source comparison; execution does not certify proofs.
"""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='7b51e9d16626fd9f259a0c02ebc30483d6f553431fc736d6e8ba46bf787435ca'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==79
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for x in ['How do noise tails impact on deep ReLU networks?','Jianqing Fan','Yihong Gu','Wen-Xin Zhou','arXiv:2203.10418v2','30 Dec 2022']:assert x in first,x
    assert 'References' in pdf[26].get_text(clip=fitz.Rect(0,207.5,pdf[26].rect.width,230))
    headings=[];hashes={}
    for n in range(1,28):
        p=pdf[n-1];clip=fitz.Rect(0,0,p.rect.width,207.5) if n==27 else p.rect
        s=p.get_text(clip=clip);f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==s;hashes[str(n)]=digest(f)
        if n==27:assert 'regularized' in s and 'References' not in s
        for block in p.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    # Real theorem labels use the medium/bold font; diagram labels and citations do not.
                    m=re.fullmatch(r'Theorem (\d+\.\d+)\.?',span['text'].strip())
                    if m and span['font']=='NimbusRomNo9L-Medi':headings.append((n,m[1]))
    expected_headings=[(11,'3.3'),(14,'3.5'),(15,'3.6'),(15,'3.7'),(18,'4.1'),(19,'4.2'),(20,'4.3'),(23,'4.5'),(24,'4.6')]
    assert headings==expected_headings,headings
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==9
    assert [c['claim_id'] for c in cs]==[PID+'/T'+n for _,n in expected_headings]
    assert [c['source_order'] for c in cs]==list(range(1,10))
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[11,12],[14],[15],[15,16],[18],[19],[20],[23,24],[24,25]]
    paper=inv['papers'][0];assert paper['source_url']==URL and paper['main_text_last_pdf_page']==27
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    assert 'Conditions 1 and 2' in t['3.3'] and r'$p\geq2$' in t['3.3']
    assert r'\delta_b\vee\delta_a\vee\delta_s' in t['3.3']
    assert r'\omega v_p^{1/p}V_n^{-1/p}' in t['3.3'] and r'+\delta^2' in t['3.3']
    assert all(s in t['3.3'] for s in [r'\delta_{\mathrm{opt}}>0',r'e^{-nV_nD^2/c_2}',r'e^{-nV_n/c_2}+\omega^{1-p}D^{-2p}',r'\tau\leq\omega D^2(v_p/V_n)^{1/p}',r'\tau>\omega D^2(v_p/V_n)^{1/p}'])
    assert r'v_p^{1/((2p-1)p)}' in t['3.5'] and 'Assume Conditions 1 holds' in t['3.5']
    assert all(s in t['3.5'] for s in [r'\nu^*=1-\frac1{2p-1}',r'\bar L=c_3\lceil L\log L\rceil',r'\bar N=c_4\lceil N\log N\rceil',r'v_p^{\frac1{2p-1}}',r'v_p^{\frac2{2p-1}}',r'\frac{8\gamma^*-2\nu^*}{2\gamma^*+\nu^*}'])
    assert r'\nu^\dagger=1-1/p' in t['3.6'] and r'\delta_{n,\mathrm{LS}}^2' in t['3.6']
    assert r'\mathcal S_{n,\infty}(\delta_{n,\mathrm{LS}})' in t['3.6'] and r'\leq c_7D^{-2p}' in t['3.6']
    assert 'Conditions 1 and 3' in t['3.7'] and r'c_1\leq\tau\lesssim1' in t['3.7']
    assert r'\mathcal H(l,d,\mathcal P)' in t['3.7'] and r'\mathcal S(\delta_{n,\mathrm H})' in t['3.7']
    assert t['3.7'].endswith('independent of $n,D$.')
    assert r'$0\in\mathcal F_0$' in t['4.1']
    assert all(s in t['4.1'] for s in [r'\mathbb E[|\varepsilon|^p\mid X]\leq1',r'\widehat{\mathcal R}_\tau(f_{0,\tau})',r'c_9\delta^2',r'\text{or }',r'n^{-100}',r'\sqrt n\log n',r'\tau^{p-1}\log^2(n)',r'\alpha(3\nu^*+4)'])
    for num in ['4.1','4.2']:
        assert '(1)' in t[num] and '(2)' in t[num]
        assert t[num].count(r'\exists\widehat f_n')==2
        assert r'\liminf_{n\to\infty}\inf_' in t[num] and r'\geq1-\frac{c_{10}}{\log n}' in t[num]
    assert 'be as in Theorem 4.1' in t['4.2']
    assert r'\mathcal S^{\mathrm{HN}}_{n,\infty}' in t['4.2'] and r'7\alpha\nu^\dagger' in t['4.2']
    assert r'\sup_{f_0\in\mathcal F_0}\inf_{f\in\mathcal F_n}' in t['4.3']
    assert r'\log^5(\bar N\bar L)' in t['4.3'] and 'uniform distribution' in t['4.3']
    assert all(s in t['4.5'] for s in [r'\lfloor N^{1/d}\rfloor^2\lfloor L^{1/d}\rfloor^2',r'\mathbf1_{\{\alpha_i<K\}}\Delta',r'(5L+7)(\lceil\log_2(1/\epsilon)\rceil+2)',r'(4N+3)d\vee(8N+10)',r'$9L+12$',r'(8N+6)(\lceil\log_2(1/\epsilon)\rceil+1)',r'\sum_{i=0}^r2^{-i}\theta_i',r'(\theta_1,\ldots,\theta_r)',r'\lceil\log_2(1/\epsilon)\rceil+1)'])
    assert r'$\Delta_2>0$' in t['4.6'] and r'$y_i\in\{-1,1\}$' in t['4.6']
    assert r'with depth $c_{24}L$, $c_{25}N\log_2(1/\Delta_2)$' in t['4.6']
    assert r'\|x-x_\alpha\|_\infty\geq\Delta_2' in t['4.6'] and t['4.6'].count('s=1,2')==2
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
    with tempfile.TemporaryDirectory(prefix='p1845-inventory-',dir='/private/tmp') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
        'Nine actual Theorems: 3.3, 3.5, 3.6, 3.7, 4.1, 4.2, 4.3, 4.5 and 4.6. Figure 2 labels on page 17 and prose references are not extra theorem environments. Results 3.4 and 4.4 are Propositions, not missing Theorems.',
        'Theorem 3.3 continues on page 12; its two concentration branches have different exponents. Its approximate-minimizer set uses squared tolerance delta^2, while the error bound uses delta_opt unsquared.',
        'Theorem 3.5 preserves the printed moment factor v_p^[1/((2p-1)p)], both network scalings, robustification parameter and rate factors, as well as its uniform probability bound and constant dependence.',
        'Theorem 3.6 preserves the squared optimization error, tau=infinity estimator set, polynomial tail and moment-dependent rate. Theorem 3.7 continues through its constant qualification on page 16; its H(l,d,P) and unqualified S(delta) are retained rather than silently corrected.',
        'Theorems 4.1 and 4.2 assert existence of an approximate estimator with large error, not a lower bound on every member of that estimator set. Both subparts and their liminf-inf-sup order are preserved. The set S_HN includes a min condition or a separate n^-100 approximation condition.',
        'Theorem 4.1 defines a data-generating family using F, then specializes it to F0 in the suprema. Its lower bound has approximation, capped stochastic and Huberization terms; the square root applies to n alone in sqrt(n)*log(n). Theorem 4.2 explicitly inherits F0, U and S_HN from Theorem 4.1.',
        'Theorem 4.3 is an L2 approximation lower bound under the uniform design, not the nearby L-infinity bound from prior literature.',
        'Theorem 4.5 continues after Figure 4 on page 24. Both network architectures, approximation guarantee and exact binary-expansion branch are retained. The source sum begins at i=0 but its binary vector begins at theta_1; it also contains a dangling parenthesis in the reduction term and uses +2 versus +1 in different architecture formulas. These are not repaired.',
        'Theorem 4.6 continues on page 25. It writes y_i in the hypothesis but y_alpha in the conclusion, omits the word width before c25*N*log2(1/Delta2), and permits all Delta2>0 despite logarithmic size expressions. Preserve these source issues rather than inserting additional restrictions.',
        'Definition extraction and full theorem-interface graph review are still pending; the independently validated inventory alone does not complete this paper.']
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=headings,method='Independent bold-heading enumeration across all main-text pages, visual comparison of every complete original statement and source-specific formula checks; structural validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,11,12,14,15,16,18,19,20,23,24,25,27],page27_clip_y_max=207.5),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=notes))
    write('evidence/source-provenance.json',dict(paper,cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2203.10418',registered_version_alias='2203.10418v2.pdf',source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=9,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract main-text regression, Huber/network classes, smoothness and composition definitions, moment/symmetry conditions, estimator sets and approximation regions; then independently review the full local dependency graph.'))
    print('Nine main-text Theorems independently source-validated; definition census remains pending.')
if __name__=='__main__':main()
