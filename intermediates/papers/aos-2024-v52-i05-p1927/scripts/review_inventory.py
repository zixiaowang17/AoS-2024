# -*- coding: utf-8 -*-
"""Retain the independent review of two complete original Theorems."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='a255b3cca274041f929eb12feb8884d9c2dad1164c4ed2e4663c554483f0fa69'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==58
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['Optimal policy evaluation using kernel-based temporal difference methods','Yaqi Duan','Mengdi Wang','Martin J. Wainwright','arXiv:2109.12002v1','24 Sep 2021']:assert s in first,s
    assert 'Details of simulations' in pdf[29].get_text(clip=fitz.Rect(0,300,pdf[29].rect.width,327))
    labels=[];hashes={}
    for n in range(1,31):
        clip=fitz.Rect(0,0,pdf[n-1].rect.width,295) if n==30 else None
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for s in line['spans']:
                    m=re.fullmatch(r'Theorem (\d+)',s['text'].strip())
                    if m and s['font']=='CMBX10':labels.append((n,m[1]))
    assert labels==[(10,'1'),(17,'2')]
    end=(ROOT/'evidence/page-30.txt').read_text()
    assert 'Acknowledgements' in end and 'N00014-21-1-2842' in end and 'Details of simulations' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    d=json.loads(f.read_text());cs=d['claims']
    assert [c['claim_id'] for c in cs]==[PID+'/T1',PID+'/T2']
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[10,11],[17,18]]
    assert [c['source_order'] for c in cs]==[1,2]
    t1,t2=[c['statement_original'] for c in cs]
    for s in ['(a) Slow rate','(b) Fast rate','(13)','(14)','(17)',r'\operatorname{CI}(bR)',r'200(1-\gamma)\sqrt n']:
        assert s in t1,s
    assert t1.count('any solution')==2 and t1.count(r'\lambda_n\geq c_0\delta^2(1-\gamma)')==2
    for s in ['(32a)','(32b)',r'$(\bar\sigma,\bar R)$',r'(1-\gamma)^{3/2}\sqrt n',r'\min_{3\leq j\leq d_n}',r'\sqrt{\mu_{j-1}}-\sqrt{\mu_j}',r'\frac{\delta_n}{2d_n}',r'12\kappa\bar\sigma^2',r'1-\frac{\mu_2}{\mu_1}',r'\frac{\kappa\bar\sigma/(\sqrt{\mu_1}\bar R)}{(1-\gamma)^2\log n}',r'\frac{\sqrt{\mu_1}}{b}','(33a)','(33b)']:assert s in t2,s
    check=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1927-inventory-',dir='/private/tmp') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=['Both bold theorem environments and their next-page continuations were visually compared. Proof citations, proof headings and Lemmas are excluded.',
      'Theorem 1 retains slow and fast branches, the smallest critical solution in (18), and arbitrary critical solutions in the conclusion. The bound (17) and its probability statement are separate source context.',
      'Theorem 2 retains both regimes, reversed pair order in part (b), the 3/2 horizon exponent in (33a), the eigengap and all of (33b). The preceding LB display and family conditions require separate extraction.',
      'Main text ends on shared page 30 after Acknowledgements. Evidence is clipped at y=295, above Appendix A at y=307. Full context and dependency review remains a separate gate.']
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font enumeration, visual comparison of full statements, source-specific formula checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,10,11,17,18,30],shared_page_clip=dict(page=30,y_max=295,before_main_text_end=True)),validation=dict(returncode=check.returncode,stdout=check.stdout),notes=notes))
    write('evidence/source-provenance.json',dict(d['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2109.12002',registered_version_alias='2109.12002v1.pdf',checked_at=now))
    f=ROOT/'checkpoint.json'
    if not f.exists() or json.loads(f.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract definitions and referenced bounds; resolve projected target, iid stationary sampling, critical radii and lower-bound family conventions; independently validate before completion.'))
    print('Two complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
