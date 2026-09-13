"""Independent source enumeration, transcription regression and inventory validation."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='2628fafa6307fcfc73e6e2f59efbed65dc1fb1ba069593ccde343b1eec0c1688'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==50
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['LEAVE-ONE-OUT SINGULAR SUBSPACE PERTURBATION ANALYSIS','ANDERSON Y. ZHANG','HARRISON Y. ZHOU','arXiv:2205.14855v2','14 Jan 2024']:assert s in first,s
    assert [x for x in pdf.get_toc() if x[1]=='A Proof of Theorem 2.3']==[[1,'A Proof of Theorem 2.3',31]]
    assert 'SUPPLEMENTARY MATERIAL' in pdf[27].get_text(clip=fitz.Rect(0,418,pdf[27].rect.width,435))
    labels=[];hashes={}
    for n in range(1,29):
        clip=fitz.Rect(0,0,pdf[n-1].rect.width,414) if n==28 else None
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];s=''.join(x['text'] for x in ss).strip()
                m=re.fullmatch(r'THEOREM (\d+\.\d+)\.',s)
                if m:
                    assert any(x['text']=='HEOREM' and x['font']=='NimbusRomNo9L-Regu' for x in ss)
                    labels.append((n,m[1]))
    assert labels==[(4,'2.1'),(7,'2.2'),(7,'2.3'),(11,'3.1'),(14,'3.2'),(14,'3.3'),(16,'3.4'),(17,'3.5'),(20,'5.1')],labels
    last=(ROOT/'evidence/page-28.txt').read_text();assert 'Acknowledgements.' in last and 'suggestions.' in last and 'SUPPLEMENTARY' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims']
    assert [c['label'] for c in cs]==['Theorem '+n for p,n in labels]
    assert [c['source_order'] for c in cs]==list(range(1,10))
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[4,5],[7],[7],[11],[14],[14],[16],[17],[20]]
    t={c['label']:c['statement_original'] for c in cs}
    checks={
      'Theorem 2.1':[r'\rho:=\frac{\sigma_r-\sigma_{r+1}}{\|(I-U_rU_r^T)y_n\|}>2',r'\frac{4\sqrt2}{\rho}',r'\sqrt{\sum_{i=1}^r\left(\frac{u_i^Ty_n}{\sigma_i}\right)^2}'],
      'Theorem 2.2':[r'\beta n/k^2\geq10',r'\frac{\lambda_\kappa}{\|E\|}>16',r'\sqrt{\frac{k\kappa}{\beta n}}',r'For any $i\in[n]$'],
      'Theorem 2.3':['there exists some',r'\sqrt{\frac{k^2}{\beta n}}\lambda_{r+1}',r'\frac{\sqrt{kr}}{\sqrt{\beta n}}',r'\lambda_r}\right)'],
      'Theorem 3.1':[r'$r=\kappa$',r'\beta n/k^2\geq10',r'\psi_1^{-1}+\rho_1^{-2}',r'\beta^{-0.5}k\left(1+\sqrt{\frac pn}\right)',r'\exp\left(-\frac n2\right)'],
      'Theorem 3.2':[r'\beta n/k^4\geq400',r'C_1\leq\rho_2\leq\psi_2/C_2',r'\rho_2\psi_2^{-1}+\rho_2^{-1}',r'\psi_2,\rho_2\to\infty',r'\rho_2/\psi_2=o(1)'],
      'Theorem 3.3':[r'$r=k$',r'\overset{\mathrm{iid}}',r'\beta n/k^4\geq100',r'k^{3.5}\beta^{-0.5}\left(1+\frac pn\right)',r'^{-0.25}',r'+2e^{-0.08n}'],
      'Theorem 3.4':[r'\operatorname{Var}(\xi)=\bar\sigma^2',r'\sigma\leq C\bar\sigma',r'\beta n>40',r'\psi_3\geq C',r"(1-C''\psi_3^{-1})^2",r'(1+C^{\prime\prime\prime}\psi_3^{-1})^2',r'-\exp(-C^{\prime\prime\prime}\sqrt p)'],
      'Theorem 3.5':['all the assumptions needed in Theorem 3.4 and Lemma 3.4','minimax rate (31)','if and only if',r'\mathcal N(0,\bar\sigma^2)'],
      'Theorem 5.1':[r'\sigma_r^2-\sigma_{r+1}^2-\|(I-U_rU_r^T)y_n\|^2>0',r'2\sqrt2\sigma_r',r'\sqrt{\sum_{i=1}^r\left(\frac{u_i^Ty_n}{\sigma_i}\right)^2}']}
    for label,ss in checks.items():
        for s in ss:assert s in t[label],(label,s)
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0
        assert 'PROOF' not in s and not any(ord(ch)<32 and ch!='\n' for ch in s)
        assert s.count(r'\[')==s.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2004-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent printed-environment enumeration, visual comparison of all nine statements, source-specific formula checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[4,5,7,11,14,16,17,20,28],last_page_clip=dict(page=28,y_max=414)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Theorem 5.1 is in the main-text proof section and is included.','Theorem 2.1 continues onto page 5; Theorem 3.2 contains both finite-sample and asymptotic conclusions.','Lemma 3.4 is not an inventoried claim; its assumptions and rate (31) are explicit statement dependencies of Theorem 3.5.','This gate validates the theorem inventory, not completion of the definition/dependency census.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2205.14855',registered_version_alias='2205.14855v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=9,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract and independently review the source definitions and theorem-local relationships. Preserve source discrepancies.'))
    print('Nine complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
