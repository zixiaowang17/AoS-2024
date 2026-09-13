"""Independently enumerate the registered PDF and check the frozen original inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='51b0517dc6b42a8d072ed29189f2dce2aeaa424f0a496a494e3cf9b7d49bdce7'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==46
    first=' '.join(pdf[0].get_text().split())
    for x in ['DEEP NEURAL NETWORKS FOR NONPARAMETRIC INTERACTION','SOHOM BHATTACHARYA','JIANQING FAN','DEBARGHYA MUKHERJEE','arXiv:2302.05851v1','12 Feb 2023']:assert x in first,x
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2302.05851v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2302.05851'
    assert [x for x in pdf.get_toc() if x[1] in ['References','A Proofs']]==[[1,'References',23],[1,'A Proofs',26]]
    assert any(650<b.y0<651 for b in pdf[22].search_for('REFERENCES'))
    labels=[];hashes={}
    for n in range(1,24):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,645) if n==23 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^THEOREM\s+(\d+\.\d+)\b',text)
                if m:
                    assert all(s['font']=='NimbusRomNo9L-Regu' for s in line['spans']);labels.append([n,m[1]])
    expected=[[9,'2.7'],[11,'2.9'],[12,'2.12'],[14,'3.2'],[16,'3.5'],[18,'3.8'],[19,'3.9']];assert labels==expected,labels
    end=(ROOT/'evidence/page-23.txt').read_text();assert 'This completes the proof.' in end and 'Funding.' in end and 'REFERENCES' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==7
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n
        assert c['label']=='Theorem '+n+(' (Main theorem)' if n=='2.9' else '')
        assert [e['page'] for e in c['evidence']]==([14,15] if n=='3.2' else [page])
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'2.7':[r'N_1L_1=\lfloor n^{1/2(2\beta_1+1)}\rfloor',r'N_2L_2=\lfloor n^{1/2(\beta_2+1)}\rfloor',r'\inf_{\phi_2\in\mathcal F^1_{NN},\phi_2\in\mathcal F^2_{NN}}',r'\|f_0(X)-\phi_1(X)-\phi_2(X)\|^2',r'd(N_1L_1)^{-4\beta_1}+\binom d2(N_2L_2)^{-2\beta_2}','(2.4) and (2.5)',r'independent of $(d,N_1,L_1,N_2,L_2)$'],
'2.9':['Assumption 2.1 - 2.3 and 2.6','equation (2.3)',r'\mid\mathbf S_n',r'\frac{V_n}{n}\log^{3/2}n',r'dN_1^{-4\beta_1}+\binom d2N_2^{-2\beta_2}',r'dN_1^2\log^2N_1\log(dN_1)+\binom d2N_2^2\log^2N_2\log(dN_2)'],
'2.12':[r'\Sigma(\beta,L)','Assumptions 2.1-2.3',r'\mathfrak M(n,d,\mathcal F)',r'\mathbb E_f',r'\ge c',r'n^{-\frac{2\beta_2}{2\beta_2+2}}',r'constant $C$ independent of $(n,d)$'],
'3.2':['Assumption 2.1-2.3 and 3.1','(3.6)','(3.5) satisfes',r'\rho_{n,1}^2+\lambda_{n,1}+\frac{\lambda_{n,1}^2}{2}',r'\rho_{n,2}^2+\lambda_{n,2}+\frac{\lambda_{n,2}^2}{2}','bounded by (3.8)',r'C_3\sqrt{\frac{V_{n,1}\log n}{n}+\frac{2\log d}{n}}',r'C_4\sqrt{\frac{V_{n,2}\log n}{n}+\frac{3\log d}{n}}',r'V_{n,1}=N_1^2\log^3N_1',r'V_{n,2}=N_2^2\log^3N_2'],
'3.5':[r'\widehat\phi','same assumptions as that of Theorem 3.2','Assumption 3.4',r'\|\widehat f-f_0\|_n^2',r's_1(\rho_{n,1}^2+\lambda_{n,1}^2)+s_2(\rho_{n,2}^2+\lambda_{n,2}^2)'],
'3.8':['holds with high probability',r'\{X_1,\ldots,X_n\}','Assumption 3.7','upto log-factors',r'\|\widehat f^{\mathrm{final}}-f_0\|_2^2',r's_1\lambda_{n,1}^2+s_2\lambda_{n,2}^2','same as in Theorem 3.5'],
'3.9':['model (3.1)','Assumptions 2.2, 2.1',r'f\in\mathcal F_{\mathrm{sp}}',r'\|\widehat f-f\|_2^2',r'\vee\frac{\log(d/s_1)}n',r'\vee\frac{\log(d^2/s_2)}n']}
    for n,parts in checks.items():
        for x in parts:assert x in s[n],(n,x)
    assert r'\mathbb E' not in s['3.9'];assert 'Assumption 2.6' not in s['2.7']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2738-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent actual small-cap heading enumeration, visual comparison of every complete theorem, source-specific formula/reference checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[9,11,12,14,15,16,18,19,23],main_text_end_page=23,last_page_clip_y=645),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['All seven Theorems retained; only2.9 has a printed title, Main theorem. No main-result selection.','Theorem3.2 continues onto15 and includes both regularization formulas with the entire sum under each square root.','Original2.7 repeats phi_2 under the infimum, leaves phi_1 unbound there, and uses slash-form exponents. No silent correction.','Theorem2.12 uses c in its bound and C in its final sentence. Theorem3.5 uses phi-hat in prose and f-hat in its conclusion.','Theorem3.8 preserves its unquantified log-factor qualification;3.9 prints no expectation over training data.','Main text includes Section5 proof through23. Appendices starting26 are excluded.','Inventory is validated; definition extraction and independent full census review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=7,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract assumptions, original structured network classes with the Section2.2 architecture revision, sparse model, penalized estimator, restricted strong convexity, sample-split Algorithm1, and their paper-local dependencies. Finalize, reproduce and independently source-review.'))
    print('Seven complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
