"""Independently enumerate the two bold Theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='4e31d37e8b2ae54d7401aaf7cc18f5f86bab1923c11cc0a4ff51f701f27c6bea'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==40
    first=' '.join(pdf[0].get_text().split())
    for v in ['Testing network correlation','Cheng Mao, Yihong Wu, Jiaming Xu, and Sophie H. Yu','April 5, 2022','arXiv:2110.11816v2','2 Apr 2022']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2110.11816v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2110.11816'
    lastpage=pdf[21];assert 'Preliminary facts about graphs' in lastpage.get_text(clip=fitz.Rect(0,570,lastpage.rect.width,594))
    assert [x for x in pdf.get_toc() if x[1].startswith('A Preliminary')]==[[1,'A Preliminary facts about graphs',22]]
    labels=[];hashes={}
    for n in range(1,23):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,565) if n==22 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(span['text'] for span in line['spans'] if 'CMBX' in span['font']).strip()
                match=re.match(r'^Theorem\s+(\d+)\.$',text)
                if match:labels.append([n,match[1]])
    expected=[[6,'1'],[7,'2']];assert labels==expected,labels
    last=(ROOT/'evidence/page-22.txt').read_text();assert 'Acknowledgment' in last and 'Preliminary facts about graphs' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==2
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label']=='Theorem '+n and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    for v in [r'n\min\{q,1-q\}\ge n^{-o(1)}',r'\rho^2>\alpha',r'\omega(1)\le K',r'16\log\log n\vee2\log',r'\frac1{n\min\{q,1-q\}}',r'\mathcal Q(f_{\mathcal T}(A,B)\ge\tau)+\mathcal P(f_{\mathcal T}(A,B)\le\tau)=o(1)',r'\tau=C\mathbb E_{\mathcal P}[f_{\mathcal T}(A,B)]=C\rho^{2K}|\mathcal T|','any fixed constant $0<C<1$']:assert v in s['1'],v
    for v in ['Suppose (7) holds. Then (8) holds',r'\widetilde f_{\mathcal T}',r'\mathcal Q(\widetilde f_{\mathcal T}(A,B)\ge\tau)+\mathcal P(\widetilde f_{\mathcal T}(A,B)\le\tau)=o(1)',r'n^{2+o(1)}']:assert v in s['2'],v
    assert '(7)' in s['1'] and '(8)' in s['1'] and '(9)' in s['2']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2483-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font heading enumeration, visual comparison of both complete statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,6,7,22],main_text_end_page=22,last_page_clip_y=565),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Two actual main-text Theorem environments,1 and2; propositions, lemmas and the computational hardness conjecture are excluded.','Preserve the max in the tree-size bound, strict rho-squared threshold, diverging K and both non-strict testing-error inequalities.','Theorem2 reuses condition(7) and the threshold in(8); its approximation and algorithm are defined in the main text. The forward reference to appendix equation(54) does not authorize reading appendix bodies.','Inventory validation only; full source-context extraction and independent dependency review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract the correlated and independent graph laws, signed tree statistic and threshold, tree-size condition(7), Otter constant, and color-coding approximation including its randomness and computation. Resolve main-text definitions without reading appendix equation(54). Complete independent source review and byte-exact reproduction.'))
    print('Both theorem statements independently source-validated.')
if __name__=='__main__':main()
