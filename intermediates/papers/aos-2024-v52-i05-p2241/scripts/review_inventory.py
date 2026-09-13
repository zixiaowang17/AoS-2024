"""Source check of all eleven main-text theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='87b508b19af4bec9ed1d10ffbc2602626b4f40729ab55eec20cbaa4292f949ba'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==47
    first=' '.join(pdf[0].get_text().split())
    for value in ['ON THE EXISTENCE OF POWERFUL P-VALUES','ZHENYUAN ZHANG','AADITYA RAMDAS','RUODU WANG','2305.16539v4','1 Dec 2024']:assert value in first,value
    assert 'REFERENCES' in pdf[28].get_text(clip=fitz.Rect(0,129,pdf[28].rect.width,146))
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=None if n<29 else fitz.Rect(0,0,page.rect.width,126)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];text=''.join(s['text'] for s in ss).strip()
                m=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text)
                if m:
                    assert any(v['text']=='HEOREM' and v['font']=='NimbusRomNo9L-Regu' and 8.7<v['size']<8.9 for v in ss)
                    labels.append([n,m[1]])
    expected=[[9,'3.1'],[10,'3.4'],[12,'4.2'],[13,'4.4'],[14,'4.7'],[15,'4.9'],[20,'5.3'],[22,'5.5'],[24,'6.1'],[24,'6.2'],[25,'6.7']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-29.txt').read_text();assert 'Acknowledgments.' in last and 'REFERENCES' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==11
    assert [c['source_order'] for c in cs]==list(range(1,12))
    for c,(page,num) in zip(cs,expected):
        assert c['label']=='Theorem '+num and c['evidence'][0]['page']==page and c['claim_id']==PID+'/T'+num
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    assert [e['page'] for e in cs[9]['evidence']]==[24,25]
    assert 'under both are atomless' in s['3.1'] and r'\operatorname{Span}' in s['3.1']
    assert 'exact' not in s['3.4'] and r'\operatorname{Conv}' in s['3.4']
    assert r'X=(dG/dF)(Y)' in s['4.2'] and '(3)' in s['4.2']
    assert 'maximum element' in s['4.4'] and 'usual order' in s['4.4']
    assert r'\gamma(\partial\Gamma)=1' in s['4.7'] and 'distinct measures' in s['4.7']
    assert 'there exists $k' in s['4.9'] and '(JA)' not in s['4.9'] and 'linearly independent' in s['4.9']
    assert 'maximal element' in s['5.3'] and 'maximum element' in s['5.3'] and 'almost surely' in s['5.3']
    assert r'2+\varepsilon' in s['5.5'] and r'j\prime' not in s['5.5']
    assert "j'" in s['5.5'] and r'\mathbb E[-\log X_\infty]' in s['5.5']
    assert 'does not require (JA)' in s['6.1'] and 'or finiteness' in s['6.2']
    assert r'\inf_{Q\in\mathcal Q}\mathbb E^Q[\log X]>0' in s['6.7']
    assert r'\overline{\overline{\operatorname{Span}}\mathcal P+\overline{\operatorname{Conv}}\mathcal Q}' in s['6.7']
    assert r'\overline{\operatorname{Span}}\mathcal P\cap\overline{\operatorname{Conv}}\mathcal Q' in s['6.7']
    assert 'total variation distance' in s['6.7'] and 'tight' in s['6.7']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2241-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration, visual comparison of all eleven complete theorem statements, source-specific checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[9,10,12,13,14,15,20,22,24,25,29],main_text_end_clip=dict(page=29,y_max=126)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Eleven complete theorem environments; Theorem 6.2 spans pages 24–25.','Theorem 6.7 has both inner closed-span/closed-convex-hull operators and an outer closure of their sum; the separate closed-set intersection appears only in its tightness conclusion.','Keep JA exceptions, maximal versus maximum, distinct j and j-prime moment indices, and pointwise versus uniform e-power.','This validates the inventory only; source-context extraction remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2305.16539',registered_version_alias='2305.16539v4.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=11,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract p/e-variable definitions, JA and AC, convex-order constructions, SHINE and closed measure-set separation; preserve theorem-specific scope and source issues.'))
    print('All eleven theorem statements independently source-validated.')
if __name__=='__main__':main()
