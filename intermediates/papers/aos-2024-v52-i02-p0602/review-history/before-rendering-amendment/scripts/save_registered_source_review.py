"""Pin the manual PDF review; machine checks establish provenance and consistency."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import fitz

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
PID = ROOT.name


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = Path(subprocess.check_output([sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    register = json.loads((REPO / 'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry = next(p for p in register['papers'] if p['paper_id'] == PID)
    audit = json.loads((ROOT / 'paper-audit.json').read_text())
    inv = json.loads((ROOT / 'theorem-inventory.json').read_text())
    census = json.loads((ROOT / 'ranked-interfaces.json').read_text())
    assert digest(source) == entry['sha256'] == audit['source']['pdf_sha256']
    pdf = fitz.open(source)
    assert len(pdf) == entry['pdf_pages'] == 111
    assert 'arXiv:2208.13074v2' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['Jiaqi Li', 'Likai Chen', 'Weining Wang', 'Wei Biao Wu'])
    headings = []
    for n in range(1, 38):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    if span['font'] == 'CMBX10':
                        match = re.fullmatch(r'Theorem (\d+)', span['text'].strip())
                        if match:
                            headings.append((n, match[1]))
    assert headings == [(10,'1'),(15,'2'),(21,'3'),(30,'4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 37
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'Detecting simultaneous changepoints in multiple' in pdf[36].get_text()
    heading = pdf[37].get_text(clip=fitz.Rect(0, 65, pdf[37].rect.width, 90))
    assert heading.strip() == 'Appendix A\nSimulation and Application'
    direct = {
        'T1': {'D2','D8','D9','D10','D11','D12'},
        'T2': {'D1','D5','D7','D10','D11','D12','D13','D14','D15','D16'},
        'T3': {'D10','D11','D12','D17','D19','D20','D22','D23'},
        'T4': {'D25','D26','D27','D28','D29','D35','D36','D37','D38','D40'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 39
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 59
    assert sum(len(c['depends_on']) for c in census['claims']) == 34
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    for lid in ['D1','D3','D4','D5','D6','D7','D10','D11','D12']:
        assert reach(lid) == {'T1','T2','T3'}
    assert reach('D2') == {'T1'}
    assert reach('D8') == {'T1','T2'}
    assert reach('D9') == {'T1','T3'}
    for n in range(13,17): assert reach('D'+str(n)) == {'T2'}
    for n in range(17,24): assert reach('D'+str(n)) == {'T3'}
    for n in range(25,41): assert reach('D'+str(n)) == {'T4'}
    assert 'D24' not in members
    for lid in ['D10','D11','D12','D16','D20','D28','D29','D36','D37','D38']:
        assert members[lid]['source_kind'] == 'assumption'
    assert members['D39']['source_kind'] == 'source_passage'
    assert members['D5']['statement_original'].startswith('Then the long-run variance matrix')
    assert by_local['D5']['source_keywords'][0]['source_text'] == 'long-run variance matrix'
    assert members['D32']['statement_original'].find('long-run covariance matrix') >= 0
    historical = ROOT / 'review-history/before-local-source-rebuild'
    assert (historical / 'theorem-inventory.json').read_bytes() == (ROOT / 'theorem-inventory.json').read_bytes()
    assert digest(historical / 'paper-audit.json') == audit['registered_source_correction']['previous_audit_sha256']
    def check_strings(value):
        if isinstance(value, dict):
            for v in value.values(): check_strings(v)
        elif isinstance(value, list):
            for v in value: check_strings(v)
        elif isinstance(value, str):
            assert not any(ord(c)<32 and c not in '\n\t' for c in value), repr(value)
    check_strings(census)
    for it in census['interfaces']:
        for member in it['members']:
            selectors = member.get('highlight_symbols', []) + member.get('highlight_phrases', [])
            original = member['statement_original'] + '\n' + member['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), member['local_id']
            assert all(any(s in t for t in [original] + related) for s in selectors), member['local_id']
    for item in audit['artifacts'].values():
        assert digest(ROOT / item['path']) == item['sha256']
    rebuild = json.loads((ROOT / 'evidence/revalidation/rebuild-check.json').read_text())
    assert len(rebuild['comparisons']) == 6
    for item in rebuild['comparisons']:
        assert item['matches_saved_bytes'] is True
        assert item['saved_sha256'] == item['regenerated_sha256'] == digest(ROOT / item['artifact'])
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)], text=True, capture_output=True, check=True)
        results.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    findings = json.loads((ROOT / 'evidence/revalidation/manual-findings.json').read_text())
    pages = [1,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,25,26,27,28,29,30,37]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=38, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 4 Theorems, 39 source entries, 59 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
