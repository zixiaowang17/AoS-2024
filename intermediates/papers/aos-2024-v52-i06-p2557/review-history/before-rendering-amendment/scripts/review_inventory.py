"""Independently enumerate and verify every main-text Theorem before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='51f4f2517fa5f133cc41fa353e85ee5b78d07fdf9605bdb9691f6f77ebfef651'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==55
    first=' '.join(pdf[0].get_text().split())
    for v in ['Statistical Complexity and Optimal Algorithms','Non-linear Ridge Bandits','Nived Rajaraman','Yanjun Han','Jiantao Jiao','Kannan Ramchandran','January 11, 2024','arXiv:2302.06025v3','10 Jan 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2302.06025v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2302.06025'
    boundary=pdf[28].search_for('Auxiliary lemmas');assert len(boundary)==1 and 654<boundary[0].y0<655
    assert [x for x in pdf.get_toc() if x[1]=='A Auxiliary lemmas']==[[1,'A Auxiliary lemmas',29]]
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,648) if n==29 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(span['text'] for span in line['spans'] if 'SFBX' in span['font']).strip()
                match=re.fullmatch(r'Theorem\s+(\d+)\.',text)
                if match:labels.append([n,match[1]])
    expected=[[6,'1'],[7,'2'],[8,'3'],[10,'4'],[11,'5'],[11,'6'],[12,'7'],[15,'8'],[22,'9'],[24,'10'],[27,'11'],[28,'12'],[28,'13'],[29,'14']]
    assert labels==expected,labels
    end=(ROOT/'evidence/page-29.txt').read_text();assert 'More general class of reward functions.' in end and 'Auxiliary lemmas' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==14
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page]
        assert c['label'].startswith('Theorem '+n)
    assert cs[0]['label']=='Theorem 1 (Weaker version of Theorem 9)' and cs[1]['label']=='Theorem 2 (Weaker version of Theorem 8)'
    assert cs[-1]['evidence'][0]['before_main_text_end'] is True
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'1':['Assumption 1',r'\kappa\in(0,1/4)',r'\lesssim d^2\cdot\int_{1/\sqrt d}^{1/2}',r'\max_{1/\sqrt d\le y\le x}\min_{z\in[(1-\kappa)y,(1+\kappa)y]}[f\prime(z)]^2','Algorithm 1 in Section 3.1'],
'2':['even or odd',r'\le T',r'\gtrsim d\cdot\int_{\sqrt{c\log(T)/d}}^{1/2}',r'(f(x))^2','independent of $(f,d)$'],
'3':[r'\varepsilon\in[c_1/\sqrt d,1/2]',r'\int_{1/\sqrt d}^{\varepsilon}','In addition assume',r'\varepsilon\in[\sqrt{c_2\log(T)/d},1/2]',r'\int_{\sqrt{c_2\log(T)/d}}^{\varepsilon}'],
'4':['For every Lipschitz','there exists a tie-breaking rule','(El-UCB)',r'T^\star_{\mathrm{UCB}}\le T',r'\frac d{g(\sqrt{c\log(T)/d})^2}',r'g(x):=\max\{|f(x)|,|f(-x)|\}'],
'5':['there exists improper online regression oracles satisfying (5) or proper offline regression oracles satisfying (6)','for any algorithm under the oracle model',r'T^\star_{\mathrm{RO}}\le T',r'\frac d{g(\sqrt{c\log(T)/d})^2}'],
'6':['Assumption 2',r'\ge1-3\gamma/4',r'\varepsilon<\gamma',r'\mathbb E[\langle\widehat\theta_T,\theta^\star\rangle]\ge1-\varepsilon',r'\frac{d^2}{c_f^2\varepsilon}','If in addition $f$ satisfies Assumption 1',r'\frac{C_f}{c_f}d\sqrt T,T'],
'7':['Assumptions 2 and 3',r'\varepsilon<1/2',r'\ge\frac{cd^2}{\varepsilon}',r'\ge c\min\{d\sqrt T,T\}',r'(\gamma,c_f,L)'],
'8':[r'\varepsilon_1=\sqrt{\frac{c\log(1/\delta)}d}',r'\varepsilon_{t+1}^2=\varepsilon_t^2+\frac cd g(\varepsilon_t)^2','uniform distributed',r'\mathbb S^{d-1}',r'\bigcap_{s\le t}\{|\langle\theta^\star,a_s\rangle|\le\varepsilon_s\}',r'\ge1-t\delta'],
'9':[r'\kappa_1\in(0,(x_0^{-1}-1)/2)',r'\kappa_2\in(0,1/4)',r'\left\lceil\frac{(2\kappa_1+4)^2\kappa_2(2-\kappa_2)}{\kappa_1^2(1-\kappa_2)^2}\right\rceil+1',r'1+\frac{\kappa_1}4,1+\frac{\kappa_1}2,1-x_0^2,\frac{1-x_0}2','Lemma 6',r'\{\varepsilon_i\}_{i\ge0}',r'\frac12\min_{z\in[1/\sqrt d,(1+\kappa_1/2)/\sqrt d]}',r'\frac12\max_{c_2/\sqrt d\le y\le(1-\kappa_2)\sqrt{(i-1)/d}}',r'\text{if }d_0+1\le i\le m',r'c_1=\kappa_1\sqrt{1-(1-\kappa_2)^2}/4',r'c_2=(2\kappa_1+4)\sqrt{1-(1-\kappa_2)^2}/\kappa_1',r'm=\lceil x_0^2d\rceil','If $f$ is monotone',r'\log^2\left(\frac d\delta\right)\sum_{i=1}^m\frac1{\varepsilon_i^2}'],
'10':['same setting of Theorem 9','continuous and strictly increasing','without the knowledge of $f$',r'\log^3\left(\frac d\delta\right)\sum_{i=1}^m\frac1{\varepsilon_i^2}'],
'11':[r'\operatorname{Unif}(\mathbb S^{d-1})','any nonadaptive learner',r'\mathbb E[\langle\theta^\star,\widehat\theta_T\rangle]>1/2',r'\max_{K\ge1}\frac{cd}{g(\sqrt{(\log K)/d})^2+K^{-1}}'],
'12':[r'K=\exp(o(d))','there exists a finite action set',r'\inf_{\theta^\star\in\mathbb S^{d-1}}\mathbb E_{\theta^\star}',r'\ge4/5',r'\frac c{g(\sqrt{(c\prime\log K)/d})^2+K^{-1}}'],
'13':['monotonicity condition in Assumption 1',r'f\prime(x)/f\prime(y)\le C',r'1/c\le x/y\le c',r'\theta^\star\in\mathbb B^d',r'\frac{f(r)}{r^4}d^2',r'\frac{f(r)}{r^2}d',r'\max\{f(x)^2,f(-x)^2\}',r'\max_{r\in[0,1]}',r'+d\sqrt T,Tf(r)',r'(c,C,\kappa)'],
'14':[r'f(x)=\operatorname{id}(x)=x',r'T^\star_{\mathrm{burn\text{-}in}}(\operatorname{id},d)\gtrsim d^2']}
    for n,parts in checks.items():
        for v in parts:assert v.replace(r'\prime',"'") in s[n],(n,v)
    assert s['3'].count('•')==2 and s['9'].count(r'\text{if }')==2
    assert 'Assumption 1' not in s['7'] and 'Assumption 1' not in s['9']
    assert 'Lipschitz' not in s['8'] and 'even or odd' not in s['8']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2557-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    pages=[1,6,7,8,10,11,12,15,22,24,27,28,29]
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent SFBX-font theorem heading enumeration, visual comparison of all fourteen full statements, source-specific branch and formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=pages,main_text_end_page=29,last_page_clip_y=648),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Exactly Theorems1–14, all retained even when1/2 are labeled weaker versions of9/8. No lemma, corollary, example or appendix theorem is counted.','Preserve Theorem3’s two branches, Theorem4’s existential tie-breaking rule, Theorem5’s distinct proper/offline and improper/online oracle alternatives, and Theorem6’s additional Assumption1 only for its regret branch.','Theorem8 is a Bayes path bound for a uniform sphere prior; Theorem11 is nonadaptive and Bayes, while Theorem12 is a finite-action minimax existence result. Their quantifiers are not interchangeable.','Theorem9 includes all constants, both finite-difference cases and its Lemma6 reference. Theorem10 imports its setting but does not assume knowledge of f. Theorem13 is over the unit ball and only references the monotonicity part of Assumption1.','Inventory validation only. Definitions1–4, Assumptions1–3, observation/oracle models, algorithms, constants and dependencies remain to be extracted and independently reviewed.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=14,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original ridge-bandit observation model, learner policies, sample complexity/regret/burn-in/trajectory definitions, Assumptions1–3, Eluder-UCB and regression oracle models, Algorithms1–4; preserve the unresolved appendix-only Lemma6 constant reference. Resolve all theorem-local assumption branches and distinct Bayes/minimax/nonadaptive/finite-action/unit-ball scopes; then finalize, reproduce and independently review the census.'))
    print('All14 complete main-text theorem statements independently source-validated.')
if __name__=='__main__':main()
