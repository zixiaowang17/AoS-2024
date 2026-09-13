"""Record source checks and independent validation for the completed paper census."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import fitz

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2348.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
    assert digest(PDF)==paper['pdf_sha256']
    assert digest(ROOT/'theorem-inventory.json')==json.loads((ROOT/'inventory-review.json').read_text())['inventory_sha256']
    pdf=fitz.open(PDF)
    labels=[]
    for i in range(30):
        for b in pdf[i].get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    match=re.search(r'Theorem\s+(\d+\.\d+)',span['text'])
                    if match and 'BX' in span['font']:
                        labels.append((i+1,match.group(1)))
    assert labels==[(6,'3.1'),(20,'6.5')],labels
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
    counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
    assert counts==dict(theorems=2,interfaces=13,source_members=13,direct_theorem_uses=7,related_theorem_connections=13,unranked_auxiliary_passages=6)
    related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
    assert all(related['D'+str(i)]=={'3.1'} for i in range(1,11))
    assert all(related['D'+str(i)]=={'6.5'} for i in range(11,14))
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    assert set(claims['3.1']['depends_on'])=={'D1','D4','D9','D10'}
    assert set(claims['6.5']['depends_on'])=={'D11','D12','D13'}
    members=[m for x in data['interfaces'] for m in x['members']]
    by_id={m['local_id']:m for m in members}
    assert by_id['D5']['depends_on']==[]
    assert by_id['D6']['depends_on']==['D5']
    assert by_id['D11']['depends_on']==[]
    assert by_id['D12']['depends_on']==by_id['D13']['depends_on']==['D11']
    assert r'X_{n,r}\mathbf1' in claims['6.5']['statement_original']
    assert r'X_{n,r}^2\mathbf1' not in claims['6.5']['statement_original']
    assert r'$\delta_n(m)$ is replaced by $\bar\delta_n(m)$' in claims['3.1']['statement_original']
    for item in data['claims']+members+ambient['auxiliary_passages']:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced mathematical braces',item)
            assert depth==0,('unbalanced mathematical braces',item)
    for name in [f'page-{i:02}.png' for i in [1,2,3,4,5,6,20,29,30]]+['appendix-heading.png','process-crop.png']:
        shutil.copy2(WORK/name,ROOT/'evidence'/name)
    artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=51,main_text_last_pdf_page=30,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Search all 30 main-document pages for Theorem occurrences, distinguish printed environments from citations and proof headings, and corroborate with bold-font label enumeration. Visually inspect the complete statements on pages 6 and 20. Main body and acknowledgements end on page 29, references on page 30, and the supplement begins on page 31.',bold_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary'],supplementary_material_used=False),
        counts=counts,
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'Both full original theorem statements match the independently validated inventory, whose source-review hash still matches.',
            'PDF version, page count and SHA-256 match the source provenance and the external cached document.',
            'Both text enumeration and printed bold labels identify precisely Theorem 3.1 and Theorem 6.5. The latter remains included despite being reproduced from Hall and Heyde in a proof section.',
            'All 13 source interfaces and six auxiliary passages were checked against the main-text PDF, with separate records for source discrepancies.',
            'The finalizer derives seven direct uses and 13 related-theorem connections. A separate validator process accepts the census, source inventory, local graph, names, highlights, explanations and derived counts.',
            'The ten sampling/copula/statistic interfaces reach only Theorem 3.1; the three array-condition interfaces reach only Theorem 6.5. No proof-only connection is promoted to a statement dependency.',
            'The centered process depends on pseudo-observations; no hypothesis of mutual independence is required merely to define that process. The null mean and variance separately depend on H_k.',
            'Lindeberg and Lyapunov conditions use the generic martingale array, with no edge treating the sufficient Lyapunov condition as an additional hypothesis for the first theorem implication.',
            'Every member has a source-backed visible selector and all selectors match its own passage/label or a same-paper related theorem. Mathematical fragments in claims, members and auxiliary passages have balanced braces.']),
        source_notes=[
            'The cached source is arXiv:2204.01803v1, stamped 4 April 2022; its manuscript date is April 6, 2022. The title and authors match the corpus entry, but this audit does not assert equality with the later journal version.',
            'Theorem 3.1 uses H5 for its scalar limit and H_(4m-3) with d=o(n^(1/(m-1))) for its joint limit. Neither is weakened to the hypothesis the resulting test is designed to target.',
            'Max-ranks use weak inequalities and pseudo-observations divide by n+1. The selected process uses the finite-grid cdf U_n for centering and retains all pairs, including diagonal terms, in S^M.',
            'The finite-sample scale bar-delta and the asymptotic scale delta retain their different definitions. The theorem\'s final replacement sentence is preserved literally.',
            'Equation (6.24) visibly contains a first power of X_n,r. This possible source error is not corrected or used to certify the truth of the theorem.',
            'The displayed H_k equality, contradictory prose/inclusion direction, moment-index typo, array initial-value convention and cross-row dimension issue remain explicit source-review notes.',
            'No appendix body was read. Only a crop of the supplement title/abstract and Appendix A heading was used to confirm the endpoint.'],
        unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
        review_limits=['Source fidelity and statement dependency audit, not a certification of proofs or a repair of mathematical errors.','All findings are specific to the pinned preprint; supplementary appendices are excluded.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print(json.dumps(counts))

if __name__=='__main__':main()
