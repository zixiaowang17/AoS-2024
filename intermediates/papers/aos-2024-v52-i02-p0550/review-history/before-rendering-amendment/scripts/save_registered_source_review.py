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
    assert len(pdf) == entry['pdf_pages'] == 86
    assert 'arXiv:2208.10158v3' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['Anne van Delft', 'Holger Dette'])
    headings = []
    for n in range(1, 31):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    if span['font'] == 'Utopia-Bold':
                        match = re.fullmatch(r'Theorem (\d+\.\d+)\.', span['text'].strip())
                        if match:
                            headings.append((n, match[1]))
    assert headings == [(16,'3.1'),(18,'3.2'),(20,'3.3'),(20,'3.4'),(21,'3.5'),(21,'3.6'),(22,'4.1'),(22,'4.2'),(24,'4.3'),(24,'4.4'),(25,'4.5')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 30
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'Zhang, D' in pdf[29].get_text()
    heading = pdf[30].get_text(clip=fitz.Rect(0, 0, pdf[30].rect.width, 90))
    assert 'Appendix A:' in heading and 'Preliminaries and inequalities' in heading
    base = {'D5','D6','D7','D10','D11','D14','D16','D17','D9','D2','D12','D13','D15','D18'}
    pivotal = {'D19','D20','D21','D22','D23'}
    direct = {
        'T3.1': base,
        'T3.2': base | pivotal,
        'T3.3': base | {'D3','D25'},
        'T3.4': base | {'D26','D27'},
        'T3.5': base | {'D28','D29'},
        'T3.6': base | {'D32'},
        'T4.1': base | pivotal | {'D24','D33'},
        'T4.2': base | pivotal | {'D34','D37'},
        'T4.3': base | pivotal | {'D35','D36','D40'},
        'T4.4': base | pivotal | {'D35','D36','D40'},
        'T4.5': base | pivotal | {'D35','D36','D41'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 41
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 250
    assert sum(len(c['depends_on']) for c in census['claims']) == 204
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    all_theorems = set(direct)
    assert reach('D1') == reach('D2') == reach('D4') == all_theorems
    pivotal_theorems = {'T3.2','T4.1','T4.2','T4.3','T4.4','T4.5'}
    for lid in ['D19','D20','D21','D22','D23']:
        assert reach(lid) == pivotal_theorems
    for lid, expected in {
        'D25': {'T3.3'}, 'D26': {'T3.4'}, 'D27': {'T3.4'},
        'D28': {'T3.5'}, 'D29': {'T3.5'},
        'D30': {'T3.6'}, 'D31': {'T3.6'}, 'D32': {'T3.6'},
        'D24': {'T4.1','T4.2'},
        'D35': {'T4.3','T4.4','T4.5'}, 'D36': {'T4.3','T4.4','T4.5'},
        'D40': {'T4.3','T4.4'}, 'D41': {'T4.5'},
    }.items():
        assert reach(lid) == expected, lid
    assert members['D18']['source_kind'] == 'theorem_excerpt'
    for lid in ['D5','D6','D7','D10','D11','D14']:
        assert members[lid]['source_kind'] == 'assumption'
    assert members['D40']['depends_on'] == ['D39','D38']
    assert members['D41']['depends_on'] == ['D38','D35']
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
    pages = [1] + list(range(3,26)) + [30]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=31, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 11 Theorems, 41 source entries, 250 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
