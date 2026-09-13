"""Source check of all ten main-text theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='44f8c040d6ef81a8a6cd3799fbb29f2f397f6b9e5678cd4bb73eec7eb3e0358b'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==106
    first=' '.join(pdf[0].get_text().split())
    for s in ['Quantile processes and their applications in finite','Anurag Dey','Probal Chaudhuri','2407.21238v2','29 Nov 2024']:assert s in first,s
    assert 'Appendix' in pdf[28].get_text(clip=fitz.Rect(0,528,pdf[28].rect.width,550))
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=None if n<29 else fitz.Rect(0,0,page.rect.width,527)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];text=''.join(s['text'] for s in ss).strip()
                m=re.match(r'Theorem (\d+\.\d+)\.',text)
                if m:
                    assert ss[0]['font']=='CMBX12'
                    labels.append([n,m[1]])
    expected=[[10,'3.1'],[12,'3.2'],[16,'4.1'],[19,'5.1'],[20,'5.2'],[21,'5.3'],[22,'5.4'],[23,'6.1'],[23,'6.2'],[26,'6.3']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-29.txt').read_text();assert 'sample size increases.' in last and 'Appendix' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==10
    assert [c['source_order'] for c in cs]==list(range(1,11))
    for c,(page,num) in zip(cs,expected):
        assert c['label']=='Theorem '+num and c['evidence'][0]['page']==page and c['claim_id']==PID+'/T'+num
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    assert [e['page'] for e in cs[8]['evidence']]==[23,24]
    assert 'sup norm metric' in s['3.1'] and 'Table 1' in s['3.1']
    assert 'conclusion of Theorem 3.1' in s['3.2'] and 'Assumptions 1 and 3–5' in s['3.2']
    assert 'Assumptions 1 and 6–8' in s['4.1'] and 'Assumptions 1 and 8–11' in s['4.1']
    assert 'conclusion of Theorem 3.1' in s['5.1'] and 'assumptions of Theorem 3.2' in s['5.1']
    assert 'Assumptions 1 and 8–11' in s['5.2'] and 'continuous' in s['5.2']
    assert '(12)' in s['5.3'] and '(13)' in s['5.3'] and '(14)' in s['5.3']
    assert '(16)' in s['5.4'] and 'assumptions of Theorem 4.1' in s['5.4']
    for n in ['6.1','6.2']:
        assert 'Assumptions 4 and 5' in s[n] and '(6)' in s[n] and 'if and only if' in s[n]
        assert 'Assumption 3' not in s[n]
    assert 'respectively.' in s['6.3'] and '1/4' in s['6.3']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2194-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration, visual comparison of all ten complete theorem statements, source-specific checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[10,12,16,19,20,21,22,23,24,26,29],main_text_end_clip=dict(page=29,y_max=527)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Ten theorem environments; Theorem 6.2 crosses pages 23–24.','Retain references to earlier conclusions separately from references to earlier assumptions.','Fixed-H and growing-H alternatives stay separate.','Preserve the expectation-parenthesis placement in (8) and slash division in (23)–(24); interpretation issues belong in separate notes.','No appendix body inspected. This validates the inventory only.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2407.21238',registered_version_alias='2407.21238v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=10,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract main-text definitions and assumptions with branch-specific relationships; preserve supplement-only references as unresolved.'))
    print('All ten theorem statements independently source-validated.')
if __name__=='__main__':main()
