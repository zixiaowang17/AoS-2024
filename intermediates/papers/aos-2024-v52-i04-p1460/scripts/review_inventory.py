"""Validate the independently enumerated and visually reviewed theorem inventory.

This checker pins a reviewed transcription. Changing the pin requires renewed PDF review.
"""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA
EXPECTED_INVENTORY_SHA='62efa9021de464d0cde9e3b6e338cf286ebfbf4acb546cdedeab877269fc0ba1'

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==74 and 'arXiv:2211.00488v1' in pdf[0].get_text()
    headings=[];text_hashes={}
    for n in range(1,29):
        page=pdf[n-1];text=page.get_text()
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode()==text
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                match=re.match(r'^Theorem (\d+\.\d+)(?:\.| \()',s)
                if match and line['spans'][0]['font']=='SFBX1095':
                    headings.append((n,match[1]))
    assert headings==[(7,'3.1'),(8,'3.2'),(8,'3.3'),(9,'4.1'),(9,'4.2'),(10,'4.3'),(11,'4.4'),(12,'4.5'),(14,'5.1')]
    assert '[ZSF22]' in text and '853' in text and 'APPENDIX' not in text.upper()
    assert 'Appendix A' in pdf[28].get_text(clip=fitz.Rect(0,0,pdf[28].rect.width,94))
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
    for c in inv['claims']:
        s=c['statement_original']
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        assert s.count(r'\[')==s.count(r'\]') and len(re.findall(r'(?<!\\)\$',s))%2==0
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if brace=='{' else -1
                assert depth>=0
            assert depth==0
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert all(f'\n{i}. ' in t['3.1'] for i in [1,2,3])
    assert r'4+\varepsilon' in t['3.1'] and r'\boldsymbol\Omega\ne\boldsymbol I_r' in t['3.1']
    assert r'\tag{7}' in t['3.2'] and r'\tag{8}' in t['3.2']
    assert 'mutually independent' in t['3.2'] and 'independent of $(n,d)$' in t['3.2']
    assert 'Theorem 3.1, claim 3' in t['3.3'] and 'fourth' not in t['3.3']
    assert r'\boldsymbol Q^*(s)' in t['4.1'] and 'countable set' in t['4.1']
    assert 'bounded fourth moment' in t['4.2'] and 'achieved by the null estimators' in t['4.2']
    assert r'\tag{16}' in t['4.3'] and 'limits exist and are equal' in t['4.3']
    assert t['4.4'].count('for all but countably many')==2
    assert r'\lim_{\varepsilon\to0+}\limsup_{n,d\to\infty}' in t['4.4'] and 'independent of everything else' in t['4.4']
    assert all(f'({ch})' in t['4.5'] for ch in ['a','b','c'])
    assert 'global maximum' in t['4.5'] and r'\frac{\gamma^2}{4s}' in t['4.5'] and r'+\mathsf I(\gamma)' in t['4.5']
    assert '(For condition (b)' in t['4.5'] and 'first stationary point' in t['4.5']
    assert r'q_\Theta<q_\Theta^{\mathrm{info}}(k)' in t['5.1'] and r'q_\Theta>q_\Theta^{\mathrm{info}}(k)' in t['5.1']
    assert r'\mathrm{p\text{-}lim}' in t['5.1'] and r'\liminf_{n,d\to\infty}\mathbb E' in t['5.1']
    assert [e['page'] for e in inv['claims'][4]['evidence']]==[9,10]
    assert [e['page'] for e in inv['claims'][-1]['evidence']]==[14,15]
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1460-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
      'The registered source is arXiv:2211.00488v1, 1 November 2022, 74 pages. Main text and references end on page 28; Appendix A starts separately on page 29. Appendix bodies were not read.',
      'Independent bold-heading enumeration confirms nine Theorems: 3.1-3.3, 4.1-4.5 and 5.1. Theorem 4.1 is retained even though its heading attributes the result to [LM19]. Proposition 5.1 is not included.',
      'Complete original bodies were visually compared. Theorem 4.2 continues from page 9 to 10, including its matrix-error bound and the final null-estimator sentence. Theorem 5.1 continues from page 14 to 15; the intervening threshold table is not part of the statement.',
      'The three claims of Theorem 3.1, the two inequalities of Theorem 3.2, both equalities of Theorem 3.3, the nested perturbation limits of Theorem 4.4 and all three alternative conditions of Theorem 4.5 remain complete.',
      'Theorem 4.1 prints Q-star(s) without binding s in the theorem. Theorem 4.5(c) prints global maximum with positive quadratic and mutual-information terms. These source issues must remain separately documented, not silently corrected in the quotations.',
      'Inventory schema validation, math-fragment checks and isolated byte-exact regeneration passed. Definition extraction and full census source review are still pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, schema validation and isolated regeneration.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,7,8,9,10,11,12,14,15,28],boundary_crop='evidence/page-29-appendix-heading.png'),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2211.00488v1.pdf',registered_url_alias='https://export.arxiv.org/pdf/2211.00488',checked_at=now),indent=2)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=9,source_pdf_sha256=SHA,next_action='Extract the fixed-prior matrix models, normalization, estimation losses, Gaussian channel, information and free-energy functionals, assumption clauses and clustering threshold; review conditional and alternative branches independently.'),indent=2)+'\n')
    print('Nine complete original theorem statements independently checked; full census remains pending.')

if __name__=='__main__':main()
