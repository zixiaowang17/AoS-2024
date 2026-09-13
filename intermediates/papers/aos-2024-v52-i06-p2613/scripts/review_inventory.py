"""Independently enumerate and validate the six original theorem statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='88f8ab025c051e462d1261eb7ea3d206d4b1b0142d492ba641c8df5a28ff9f8d'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==69
    first=' '.join(pdf[0].get_text().split())
    for v in ['Time-uniform central limit theory','and asymptotic confidence sequences','Ian Waudby-Smith','David Arbour','Ritwik Sinha','Edward H. Kennedy','Aaditya Ramdas','arXiv:2103.06476v9','14 Mar 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2103.06476v9.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2103.06476'
    boundary=pdf[27].search_for('References');assert len(boundary)==1 and 638<boundary[0].y0<639
    assert [x for x in pdf.get_toc() if x[1]=='Proofs of the main results']==[[1,'Proofs of the main results',33]]
    labels=[];hashes={}
    for n in range(1,29):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,632) if n==28 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(span['text'] for span in line['spans'] if span['font']=='SFBX1000').strip()
                match=re.match(r'^Theorem\s+(\d+\.\d+)\b',text)
                if match:labels.append([n,match[1]])
    expected=[[8,'2.2'],[10,'2.4'],[13,'2.8'],[18,'3.1'],[19,'3.2'],[21,'3.3']];assert labels==expected,labels
    end=(ROOT/'evidence/page-28.txt').read_text();assert 'Acknowledgements' in end and 'References' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==6
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page] and c['label'].startswith('Theorem '+n+' (')
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'2.2':['infinite sequence of i.i.d. observations','finite variance',r'\widehat\mu_t:=\frac1t\sum_{i=1}^tY_i',r'\widehat\sigma_t^2:=\frac1t\sum_{i=1}^tY_i^2-(\widehat\mu_t)^2','prespecified constant',r'\overline C_t^{\mathcal G}',r'\overline{\mathfrak B}_t^{\mathcal G}',r'\widehat\sigma_t\sqrt{\frac{2(t\rho^2+1)}{t^2\rho^2}',r'\frac{\sqrt{t\rho^2+1}}\alpha'],
'2.4':['totally ordered infinite set','minimal element','Conditions G-1–G-4',r'[\widehat\theta_t-L_t,\widehat\theta_t+U_t]','potentially enriched probability space',r'\forall t\in\mathcal T',r'\ge1-\alpha',r'L_t^*/L_t\xrightarrow{\mathrm{a.s.}}1',r'U_t^*/U_t\xrightarrow{\mathrm{a.s.}}1'],
'2.8':['same setup as Proposition 2.5','Conditions L-1, L-2, and L-3-$\eta$',r'(\widetilde C_t(m))_{t=m}^\infty','given in (18)','sharp asymptotic',r'\widetilde\mu_t:=\frac1t\sum_{i=1}^t\mu_i',r'\lim_{m\to\infty}',r'\forall t\ge m',r'=1-\alpha'],
'3.1':['cross-fit AIPW estimator as in (25)',r'\|\widehat\mu_t^a(X)-\overline\mu^a(X)\|_{L_2(\mathbb P)}=o(1)','but need not be',r'\|\widehat f_t-\overline f\|_{L_2(\mathbb P)}=o(1)',r'\pi(X)\in[\delta,1-\delta]','almost surely',r'\mathbb E|\overline f(Z)|^{2+\varepsilon}<\infty',r'\sqrt{\widehat{\operatorname{var}}_t(\widehat f)}\cdot\sqrt{\frac{2(t\rho^2+1)}{t^2\rho^2}'],
'3.2':['same setup as Theorem 3.1','no longer known','consistently estimated',r'\|\widehat\pi_t-\pi\|_{L_2(\mathbb P)}\sum_{a=0}^1\|\widehat\mu_t^a-\mu^a\|_{L_2(\mathbb P)}=o\left(\sqrt{\log t/t}\right)',r'\|\widehat f_t-f\|_{L_2(\mathbb P)}=o(1)','efficient influence function (24)',r'\mathbb E|f(Z)|^{2+\varepsilon}<\infty',r'\sqrt{\widehat{\operatorname{var}}_t(\widehat f)}'],
'3.3':['independent triples',r'Z_t:=(X_t,A_t,Y_t)',r'\widetilde{\mathrm{ATE}}','conditions of Corollary 2.6','replaced by the influence functions',r'(\overline f(Z_t))_{t=1}^\infty',r'\frac{2(t\rho^2\widehat{\operatorname{var}}_t(\overline f)+1)}{t^2\rho^2}',r'\frac{\sqrt{t\rho^2\widehat{\operatorname{var}}_t(\overline f)+1}}\alpha',r'\widetilde\psi_t:=\frac1t\sum_{i=1}^t\psi_i']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert 'identically' not in s['3.3']
    assert r'\widehat{\operatorname{var}}_t(\widehat f)' not in s['3.3']
    assert r'\widehat{\operatorname{var}}_t(\overline f)' not in s['3.1']+s['3.2']
    assert 'Proposition 2.5' in (ROOT/'evidence/page-11.txt').read_text()
    assert 'Corollary 2.6' in (ROOT/'evidence/page-12.txt').read_text()
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2613-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    pages=[1,8,10,11,13,18,19,21,28]
    crops=[dict(path='evidence/page-'+str(n).zfill(2)+'-theorem-crop.jpg',page=n) for n in [8,18,21]]
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font theorem-heading enumeration, visual comparison of all six complete statements, source-specific formula and reference checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=pages,visually_reviewed_crops=crops,main_text_end_page=28,last_page_clip_y=632),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Exactly six actual main-text Theorems2.2,2.4,2.8,3.1,3.2,3.3. Proposition2.5 and Corollary2.6 are retained only if needed to interpret explicit references; stale appendix outline theorem labels do not change the inventory.','Theorem2.2 uses barred C and Fraktur B, sample variance with denominator t, and any prespecified rho>0. Theorem2.8 asserts equality1-alpha in the limiting all-future coverage probability, not merely a lower bound.','Theorem3.1 permits a misspecified regression limit under known propensity; Theorem3.2 instead requires consistent nuisance estimates and an efficient influence function. Theorem3.3 allows independent non-identically distributed triples and prints a variance estimate of the limiting bar-f, not fitted hat-f.','Inventory only. Conditions G1–G4,L1/L2/L3eta, Corollary2.6 assumptions, AsympCS/coverage definitions, cross-fitting and influence-function/variance formulas remain to be extracted and source-reviewed. Appendix bodies are excluded.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=6,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract all original AsympCS/coverage definitions, explicit G/L/ATE conditions and Corollary2.6 imports, causal estimands and identification assumptions, sequential cross-fitting and fitted/limit influence and variance definitions. Resolve source discrepancies without appendix bodies; finalize, rebuild and independently source-review the census.'))
    print('Six complete main-text Theorem statements independently source-validated.')
if __name__=='__main__':main()
