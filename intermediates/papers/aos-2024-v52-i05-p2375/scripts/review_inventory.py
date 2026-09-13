"""Independently check four main-text theorem environments before interface extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='dff4787c8790d5f041dedcd200c1f00377f29e1c861f24173b96bb41a86df169'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==66
    first=' '.join(pdf[0].get_text().split())
    for v in ['2110.14067v2','25 Feb 2023','Yunyi Zhang','Efstathios Paparoditis','Dimitris N. Politis']:assert v in first,v
    assert pdf[28].get_text().lstrip().startswith('References')
    labels=[];hashes={}
    for n in range(1,29):
        page=pdf[n-1];clip=None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        rows={}
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    if span['font']=='CMBX10':rows.setdefault(round(span['bbox'][1],1),[]).append(span)
        for y,spans in sorted(rows.items()):
            bold=' '.join(s['text'] for s in sorted(spans,key=lambda s:s['bbox'][0]))
            match=re.match(r'^Theorem\s+(\d+)$',bold)
            if match:labels.append([n,match[1]])
    expected=[[10,'1'],[14,'2'],[18,'3'],[23,'4']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-28.txt').read_text();assert 'Acknowledgement' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==4
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label'].startswith('Theorem '+n) and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==({'1':[10,11],'2':[14,15],'3':[18],'4':[23]}[n])
    s={str(i):c['statement_original'] for i,c in enumerate(cs,1)}
    checks={
'1':[r'p_1=O(T^{\alpha_{p_1}})',r'\sum_{j=0}^da_{kj}(X_iX_{i-j}-EX_iX_{i-j})',r'\frac{12\alpha_{p_1}}m+12\alpha B+\alpha_l<1',r'8\alpha B+\alpha_s<\alpha_l',r'EZ_{i_1,k_1}Z_{i_2,k_2}'],
'2':[r'\frac{12\beta_X}m+12\alpha_X\beta_X+\alpha_l<1','(i)','(ii)',r'E(X_{i_1}X_{i_1-j}-\sigma_j)(X_{i_2}X_{i_2-j}-\sigma_j)',r'\sigma_0>c',r'EZ_{i_1,j_1}Z_{i_2,j_2}'],
'3':['weakly stationary','smallest eigenvalue',r'p=O(1)','Definition 3',r'\left\|\frac1{\sqrt T}\sum_{i=1}^TZ_{i,j}\right\|_2>C'],
'4':['conditions of Lemma 4','as in Lemma 3','(i)','(ii)','(iii)',r'8\beta_X/m+7\alpha_X\beta_X-1/2',r'^{1/6}',r'H_\sigma(x)',r'H_\rho(x)',r'H_a(x)',r'k_T\times T^{-1/2}=o(1)']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert 'weakly stationary' not in s['1']
    assert 'X_{i_1-j_1}' not in s['2']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2375-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font heading enumeration, visual comparison of all four full statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[11,14,15,18,23,28],main_text_end_page=28),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['All four main-text Theorem environments; appendix bodies excluded.','Preserve all five growth inequalities, both T2 branches, T3 covariance and all three bootstrap branches with their distinct rates.','Inventory validation only; source-context extraction remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2110.14067',registered_version_alias='2110.14067v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract independent-input dependence definitions, autocovariance/correlation estimators, AR Yule-Walker objects, kernel and bootstrap definitions; independently review every branch and source issue.'))
    print('All four theorem statements independently source-validated.')
if __name__=='__main__':main()
