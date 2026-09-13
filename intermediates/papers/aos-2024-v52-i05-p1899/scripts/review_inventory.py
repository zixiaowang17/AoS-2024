# -*- coding: utf-8 -*-
"""Independently validate the frozen twenty-Theorem source transcription.

Records a completed visual source comparison, not a proof-correctness verdict.
"""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
EXPECTED='d24637d6390d7921fa7b2596828a44ad809d69ae75bcad012a0bec72cfa94dd2'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==80
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for x in ['JOINT SEQUENTIAL DETECTION AND ISOLATION FOR DEPENDENT DATA STREAMS','ANAMITRA CHAUDHURI','GEORGIOS FELLOURIS']:
        assert x in first,x
    for x in ['arXiv:2207.00120v1','30 Jun 2022']:assert x in first,x
    assert 'APPENDIX A: PROOFS REGARDING ERROR CONTROL' in pdf[25].get_text(clip=fitz.Rect(0,65,pdf[25].rect.width,81))
    assert 'Funding.' in pdf[24].get_text() and 'DMS-1737962' in pdf[24].get_text()
    headings=[];hashes={}
    for n in range(1,26):
        p=pdf[n-1];s=p.get_text();f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==s;hashes[str(n)]=digest(f)
        for block in p.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                # The printed label uses separate full-height T and reduced-height HE OREM spans.
                text=''.join(span['text'] for span in line['spans'])
                m=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text.strip())
                if m:headings.append((n,m[1]))
    expected=[(8,'3.1'),(9,'3.2'),(11,'4.1'),(11,'4.2'),(12,'4.3'),(12,'4.4'),(13,'4.5'),(14,'4.6'),(15,'5.1'),(15,'5.2'),(16,'5.3'),(17,'5.4'),(18,'5.5'),(18,'5.6'),(20,'6.1'),(20,'6.2'),(21,'6.3'),(21,'6.4'),(22,'6.5'),(22,'6.6')]
    assert headings==expected,headings
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==20
    assert [c['claim_id'] for c in cs]==[PID+'/T'+n for _,n in expected]
    assert [c['source_order'] for c in cs]==list(range(1,21))
    assert [[e['page'] for e in c['evidence']] for c in cs]==[[8],[9],[11],[11],[12],[12],[13],[14],[15],[15,16],[16],[17],[18],[18],[20],[20,21],[21],[21],[22],[22]]
    paper=inv['papers'][0];assert paper['source_url']==URL and paper['main_text_last_pdf_page']==25
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
    '3.1':[r'\emptyset\notin\Psi',r'a_e|\mathcal K|/\delta',r'b_e|\mathcal K|/\gamma',r'\Psi_{m,m}',r'/(\gamma\wedge\delta)'],
    '3.2':[r'C_e\geq c_e/\beta',r'D_e\geq d_e|\mathcal K|/\alpha',r'(a_e\vee c_e)(|\mathcal K|+1)/\delta',r'(b_e\vee d_e)|\mathcal K|/\gamma',r's_e=s\'_e=e'.replace('\\\'',"'"),'as in Theorem 3.1'],
    '4.1':['(12) holds',r'\emptyset\notin\Psi',r'\mathbb E_P[T^*]\lesssim',r'\mathcal H_{\Psi,e};s\'_e'.replace('\\\'',"'"),r'\mathcal G_{\Psi,e};s\'_e'.replace('\\\'',"'")],
    '4.2':['(i)','(ii)',r'P\in\mathcal H_0',r'P\notin\mathcal H_0',r'\text{as }\beta\to0',r'\text{as }\delta\to0',r'\text{as }\alpha\to0',r'\text{as }\gamma,\delta\to0',r'\text{as }\alpha,\gamma,\delta\to0'],
    '4.3':['(15)','(16)',r'\Psi_{m,m}',r'\mathcal P_\Psi\setminus\{P\}',r'|\log(\gamma\wedge\delta)|'],
    '4.4':['(17)',r'\min_{e\in\mathcal K}',r'\mathcal D_\Psi(\alpha,\beta)',r'\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)',r'\mathcal E_\Psi(\gamma,\delta)','either fixed or go to'],
    '4.5':['(18)',r'\max_{e\in\mathcal A(P)}','for some $e','(15) holds',r'|\log\alpha|\gg|\log\gamma|\vee|\log\delta|',r'|\log\gamma|\gg|\log\delta|',r'\mathcal I(P,\mathcal H_0)\wedge\mathcal I(P,\mathcal H_{\Psi,e})'],
    '4.6':['(18) holds','(15) - (16)',r'\mathcal I(P,\mathcal H_0)\wedge\mathcal I(P,\mathcal H_{\Psi,e})',r'\frac{|\log\alpha|}{\mathcal I(P,\mathcal H_0)}\bigvee'],
    '5.1':['Suppose that either',r'l\vee p(T)\wedge u',r'T\in\{T^*,T^*_{\mathrm{fwer}}\}',r'l=p(T)=0',r'D_{\mathrm{iso}}(T)=\emptyset'],
    '5.2':[r'$l\geq1$',r'$\ell=u<K$',r'T_1\wedge T_2\wedge T_4\wedge T_5\wedge T_6',r'T_1\wedge T_2\wedge T_3',r'T_6&:=',r'\min\{1/A,\Lambda_{(l)}(n)/B\}',r'\max\{B,A\Lambda_{(u+1)}(n)\}'],
    '5.3':['Subsection 3.2.2',r'\prod_{i=1}^{p(n)\wedge u}',r'T_1\wedge T_3\wedge T_4\wedge T_5',r'T_1\wedge T_2',r'T_5&=',r'\prod_{i=1}^u',r'\prod_{i=1}^{p(n)}'],
    '5.4':['asymptotically optimal','(i)','(ii)',r'T_0\wedge T_1\wedge T_2\wedge T_3\wedge T_4',r'T_4&=',r'\Lambda_{(1)}(n)\leq1/A',r'\Lambda_{(1)}(n)\geq B'],
    '5.5':[r'\min_{\{k\}\in\mathcal A(P)}\mathcal I(P,\mathcal H_{\Psi,k})',r'\min_{\{k\}\in\mathcal A(P)}\mathcal I(P^k,\mathcal H^k)',r'|\mathcal A(P)|>1',r'|\mathcal A(P)|<u',r'\Psi_{0,u}'],
    '5.6':['exactly one signal',r'\Psi_{1,1}\subseteq\Psi','either fixed or go to',r'\frac{\mathcal I(P,\mathcal H_0)}{\mathcal I(P^k,\mathcal H^k)}'],
    '6.1':['(23) holds',r'\Psi_{\mathrm{dis}}',r'B\subseteq\{i_1(n),\ldots,i_{p(n)}(n)\}',r'\prod_{e\in B}\Lambda_e(n)','Subsection 3.2.2'],
    '6.2':[r's\'_e\supseteq v_l\supseteq e'.replace('\\\'',"'"),r'|\mathcal A(P)|>1',r'L(P)>1','powerset of',r'\mathcal I(P^e,\mathcal H^e)'],
    '6.3':[r'v_l\cup v_{l\'}'.replace('\\\'',"'"),r'e\cup v_l',r'e\setminus v_0\in v_l',r'v_0\supseteq e',r'\mathcal I(P^e,\mathcal G^e)','powerset of'],
    '6.4':[r's_e\supseteq v_1\cup\ldots\cup v_{L(P)}','exactly one dependent pair',r'|\mathcal A(P)|=1'],
    '6.5':['either fixed or go to',r'\Psi_{1,1}\subseteq\Psi','e.g., when (23) holds',r'\mathcal I(P^e,\mathcal G^e)'],
    '6.6':[r'\Psi_{\mathrm{dis}}',r's_e=s\'_e=e'.replace('\\\'',"'"),r'\min_{e\notin\mathcal A(P)}','asymptotically optimal as',r'\chi^*_{\mathrm{fwer}}']}
    for n,parts in checks.items():
        for s in parts:assert s in t[n],(n,s)
    assert t['5.2'].count('&:=')==6 and t['5.3'].count('&=')==5 and t['5.4'].count('&=')==5
    assert t['6.2'].count('•')==2 and t['6.3'].count(r'\text{if }')==4
    for c in cs:
        s=c['statement_original'];assert 'PROOF.' not in s and 'The proof can be found' not in s
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1899-inventory-',dir='/private/tmp') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
      'Twenty actual small-cap Theorem environments in source order. Theorems 5.2 and 6.2 continue onto pages 16 and 21 respectively. Mixed-case citations, Corollaries 5.1 and 6.1 and appendix results are excluded.',
      'Theorems 3.1 and 3.2 retain all threshold inequalities, including |K|+1 only in the appropriate denominator-side threshold coefficient, and the combined gamma-wedge-delta branch. Theorem 3.2(iii) references only the threshold choices from Theorem 3.1; its pure-isolation precondition must not be imported wholesale.',
      'Theorems 4.1 and 4.2 explicitly require (12). Theorem 4.2 has five bounds with different limits: beta, delta, alpha, gamma/delta, and alpha/gamma/delta. Detection uses a minimum over signals and isolation a maximum, with distinct se and se-prime.',
      'Theorems 4.3–4.6 inherit (11)–(12) from the beginning of Section 4.4. The equations (15)–(18) have different min/max and signal/non-signal roles; each is retained. Theorem 4.3 preserves the special fixed-cardinality denominator I(P,P_Psi minus {P}).',
      'Theorems 4.4 and 5.6(ii)/6.5 allow gamma and delta to remain fixed. They are not rewritten to require all four tolerances to vanish. Theorems 4.5 and 4.6 retain both detection and familywise formulations and their different rate requirements.',
      'Theorem 5.1 keeps the clipped-count index l vee p(T) wedge u and the empty-selection convention. Theorem 5.2 uses ell in its first branch and l elsewhere, as printed.',
      'Theorem 5.2 preserves all six stopping-time definitions and both u<K/u=K branches. Theorem 5.3 preserves the capped product for detection and all five joint stopping times, including p(n)-versus-u product ranges. Theorem 5.4 preserves its local/global isolation split and all five stopping times.',
      'Theorems 5.5 and 5.6 concern dependent sources, despite the independence assumptions in the preceding subsection. Their ARE bounds retain separate global and marginal information quantities and the additional sufficient independence conditions for equality.',
      'Theorem 6.1 maximizes a product only over subsets B of currently positive local-statistic units satisfying B in Psi. It is not an unrestricted product or a maximum over individual pairs.',
      'Theorem 6.2 has two alternative sets of sufficient conditions, the second continued on page 21. Theorem 6.3 has four subsystem-containment branches; its source writes e minus v0 in v_l, with membership rather than subset notation. This apparent source inconsistency is retained.',
      'Theorems 6.4–6.6 retain exact dependent-pair and independent-pair quantifiers. Theorem 6.6 is a familywise test optimality result, not an ARE statement for the joint test.',
      'Main text ends after Conclusion and Funding on page 25; the following page begins Appendix A. No appendix body was used. Complete definition extraction, standing-scope resolution and full graph validation are still pending.'
    ]
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=headings,method='Independent small-cap environment enumeration, visual comparison of every full statement, source-specific formula and branch checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,8,9,11,12,13,14,15,16,17,18,20,21,22,25]),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=notes))
    write('evidence/source-provenance.json',dict(paper,cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2207.00120',registered_version_alias='2207.00120v1.pdf',source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=20,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract original main-text data/filtration, hypothesis/prior families, four error-control classes, likelihood statistics, stopping rules, threshold conditions, information assumptions, ARE and dependence-partition definitions. Resolve section-specific scope and validate all twenty theorem dependency closures before completing this paper.'))
    print('Twenty complete main-text Theorems independently source-validated; definition census remains pending.')
if __name__=='__main__':main()
