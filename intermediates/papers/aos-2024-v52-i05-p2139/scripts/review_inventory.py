"""Independently enumerate and check the source-pinned two-Theorem inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='1e35d6f0bc3a58a5c680a1c86f8e5366e5b52bcd023f1de570135e283ce2a21e'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==52
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['EFFICIENCY IN LOCAL DIFFERENTIAL PRIVACY','LUKAS STEINBERGER','arXiv:2301.10600v3','7 Mar 2024']:assert s in first,s
    # Inspect only the appendix heading, never its body.
    assert 'APPENDIX A: TECHNICAL LEMMAS AND PROOFS OF SECTION 3' in pdf[28].get_text(clip=fitz.Rect(90,562,540,577))
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=None if n<29 else fitz.Rect(0,0,page.rect.width,550)
        f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];label=''.join(x['text'] for x in ss).strip()
                found=re.fullmatch(r'THEOREM (\d+\.\d+)\.',label)
                if found:
                    assert any(x['text']=='HEOREM' and x['font']=='NimbusRomNo9L-Regu' and 8.7<x['size']<8.9 for x in ss)
                    labels.append((n,found[1]))
    expected=[(11,'3.3'),(12,'3.5'),(14,'4.1'),(15,'4.2'),(15,'4.3'),(21,'4.11'),(22,'4.12')]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-29.txt').read_text()
    assert 'Funding.' in last and 'APPENDIX' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert [c['label'] for c in cs]==['Theorem '+n for _,n in expected]
    assert [c['source_order'] for c in cs]==list(range(1,8)) and [[e['page'] for e in c['evidence']] for c in cs]==[[p] for p,_ in expected]
    statements={n:c['statement_original'] for (_,n),c in zip(expected,cs)}
    a=statements['3.3']
    for t in ['countably generated',r'\frac1n\sum_{i=1}^n I_\theta(Q_{z_{1:i-1}}\mathcal P)',r'\overset{Q^{(n)}P_\theta^n}{\rightsquigarrow}','some random symmetric',r'I_\theta(\mathcal P)\ne0',r'\delta_n=J_p/\sqrt n',r'\frac1{\sqrt n}\sum_{i=1}^n t_{i,\theta}']:assert t in a,t
    assert 'positive definite' not in a
    a=statements['3.5']
    for t in ['every weak accumulation point','almost surely positive definite',r'\forall h\in\mathbb R^p',r'\mathcal N(0,\sigma^{-1})\star L_\theta(\sigma)','possibly depending']:assert t in a,t
    for n in ['4.1','4.2']:
        assert r'\varepsilon\wedge\widehat\theta_n\in K' in statements[n] and 'every compact set' in statements[n]
    assert 'DQM' not in statements['4.1'] and 'private' not in statements['4.1']
    assert 'identifiable' in statements['4.2']
    for t in [r'\Pi_{\tau_n}[g(X_i)]',r'\frac{2\tau_n}{\alpha}W_i',r'W_{ij}\sim\operatorname{Lap}(1)',r'\tau_n^2/n\to0']:assert t in statements['4.3'],t
    for t in [r'p=1','measurable maximizer',r'0\leq\sup',r'I_{\theta_{n_1}}',r'2\varphi(\theta,\widetilde\theta_{n_1})+\varphi(\theta,\theta_{n_1})',r'\theta_{n_1}\to\theta']:assert t in statements['4.11'],t
    for t in ['three times continuously differentiable',r'\theta\mapsto\dddot p_\theta',r'\Theta\to L_1(\mu)',r'n_1/n\to0','converges to',r'\forall h\in\mathbb R']:assert t in statements['4.12'],t
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert 'PROOF' not in s and not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2139-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent small-cap-heading enumeration over all main-text pages, visual comparison of all seven complete statements, source-specific subpart checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[11,12,14,15,21,22,29],appendix_heading_clip=dict(page=29,y_min=562,y_max=577)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Seven printed main-text Theorems are retained, including the cited classical Theorem 4.1.','Theorem 3.3 does not assume positive-definite limit information; Theorem 3.5 explicitly requires positive definiteness of all weak accumulation points.','Theorems 4.1-4.2 only assert probability convergence intersected with each compact K, without a global tightness conclusion.','Theorem 4.11 prints a nonnegative difference involving Fisher information at different parameters; retain it as a source issue instead of silently correcting the theorem.','This gate validates the theorem inventory only; definitions and dependency review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2301.10600',registered_version_alias='2301.10600v3.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=7,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract source definitions and assumptions, then independently validate the complete census.'))
    print('All seven complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
