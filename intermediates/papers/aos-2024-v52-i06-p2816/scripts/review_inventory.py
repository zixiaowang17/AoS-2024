"""Independently enumerate theorem environments and verify the reviewed transcription."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='fa00dae432a2036c3275d4402bb0acb733539a6e1b9971510b08ac7d9a64f6bf'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==53
    first=' '.join(pdf[0].get_text().split())
    for x in ['Noisy recovery from random linear observations: Sharp minimax rates under elliptical constraints','Reese Pathak','Martin J. Wainwright','Lin Xiao','arXiv:2303.12613v1','22 Mar 2023']:assert x in first,x
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert reg['version']=='2303.12613v1.pdf' and reg['source_url']=='https://export.arxiv.org/pdf/2303.12613'
    assert [x for x in pdf.get_toc() if x[1]=='A Proofs from Section 2']==[[1,'A Proofs from Section 2',33]]
    labels=[];hashes={}
    for n in range(1,33):
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==pdf[n-1].get_text();hashes[str(n)]=digest(f)
        for b in pdf[n-1].get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                ss=l['spans']
                if not ss or ss[0]['font']!='SFBX1095':continue
                m=re.match(r'^Theorem (\d+)(?:[ .]|$)',ss[0]['text'])
                if m:labels.append([n,m[1]])
    assert labels==[[8,'1'],[8,'2']],labels
    end=' '.join(pdf[31].get_text().split());assert 'Acknowledgements' in end and 'UC Berkeley AI Research (BAIR) Commons initiative.' in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==2
    for i,c in enumerate(cs,1):assert c['claim_id']==PID+'/T'+str(i) and c['source_order']==i and [e['page'] for e in c['evidence']]==[8]
    assert cs[0]['label']=='Theorem 1 (General minimax upper bound)' and cs[1]['label']=='Theorem 2 (Lower bound)'
    assert cs[0]['statement_original']==r'''The minimax risk is upper bounded as
\[
\mathfrak M(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c)\le\Phi(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c).\tag{6}
\]'''
    assert cs[1]['statement_original']==r'''The minimax risk is lower bounded as
\[
\mathfrak M(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c)\ge\Phi(T,\mathbb P,\Sigma_w,\tfrac\varrho2,K_e,K_c)\ge\frac14\Phi(T,\mathbb P,\Sigma_w,\varrho,K_e,K_c).\tag{7}
\]'''
    v=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2816-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent SFBX1095 theorem heading enumeration across32 main-text pages; visual comparison of complete statements6–7 and the main-text endpoint; source-specific transcription check, structural validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,8,32],main_text_end_page=32),validation=dict(returncode=v.returncode,stdout=v.stdout),notes=['Two complete main-text Theorems on8; proof headings and external Theorem citations are not environments.','Preserve halved radius in the first lower bound and the second1/4 lower bound, not merely the sandwich constant.','Definitions of minimax risk3 and functional5, original conditional-noise conditions and constraints must be retained at extraction.','Main text includes Discussion, simulations and Acknowledgements through32. Appendix A starts33; appendix bodies are excluded.','Full census source review and dependency extraction remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=reg['source_url'],registered_version_alias=reg['version'],checked_at=now))
    p=ROOT/'checkpoint.json'
    if not p.exists() or json.loads(p.read_text()).get('stage')!='complete':write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract random operator, conditional-noise class N1/N2, quadratic norms, ellipse, estimator class, minimax risk and trace functional. Source-review their quantifiers, matrix domains and dependencies before completion.'))
    print('Both original main-text Theorems independently source-validated.')
if __name__=='__main__':main()
