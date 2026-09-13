"""Record the completed source review and promote the checked published census.

Run only after the visual and dependency review recorded in this transition.
The completion record pins the exact artifacts; it is not a correctness oracle.
"""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parents[1]
REPO = PAPER.parents[3]
PID = PAPER.name
HISTORY = PAPER / 'source-history/arxiv-2107.01305v2'
SKILL = Path('skills/statistical-paper-census/scripts')
ARTIFACTS = ['theorem-inventory.json', 'inventory-review.json', 'ranked-interfaces.json',
             'unfinalized-census.json', 'source-passages.json', 'ambient-conventions.json',
             'interface-draft.json']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    pdf = Path(subprocess.check_output(['python3', str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    inv = json.loads((ROOT / 'theorem-inventory.json').read_text())
    census = json.loads((ROOT / 'ranked-interfaces.json').read_text())
    meta = inv['papers'][0]
    assert digest(pdf) == meta['pdf_sha256']
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(SKILL / 'validate_census.py'), str(ROOT / name)],
                                text=True, capture_output=True, check=True)
        results.append({'artifact': name, 'returncode': result.returncode, 'stdout': result.stdout})
    for it in census['interfaces']:
        for m in it['members']:
            selectors = m['highlight_symbols'] + m['highlight_phrases']
            source = m['statement_original'] + '\n' + m['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in source for s in selectors), m['local_id']
            assert all(any(s in t for t in [source] + related) for s in selectors), m['local_id']
    # A byte-preserved snapshot keeps the prior successful source and census
    # distinct from the replacement; it is never counted as another paper.
    if not HISTORY.exists():
        old_audit = json.loads((PAPER / 'paper-audit.json').read_text())
        assert old_audit['source']['pdf_sha256'] == '8a21eebddf49f561327788c21c73fee3528e235684aa9342be9d8bd50c8a86fc'
        old_pdf = Path(old_audit['source']['pdf_path'])
        assert digest(old_pdf) == old_audit['source']['pdf_sha256']
        stable_old_pdf = REPO / 'local-pdfs/aos/2024/versions' / PID / 'arxiv-2107.01305v2.pdf'
        stable_old_pdf.parent.mkdir(parents=True, exist_ok=True)
        if stable_old_pdf.exists():
            assert digest(stable_old_pdf) == digest(old_pdf)
        else:
            shutil.copy2(old_pdf, stable_old_pdf)
        assert digest(stable_old_pdf) == digest(old_pdf)
        originals = [p for p in PAPER.iterdir() if p.name not in
                     {'source-transition', 'source-history', 'source-version-transition.json'}]
        hashes = {str(f.relative_to(PAPER)): digest(f)
                  for p in originals for f in (p.rglob('*') if p.is_dir() else [p]) if f.is_file()}
        HISTORY.mkdir(parents=True)
        for p in originals:
            shutil.move(str(p), str(HISTORY / p.name))
        assert all(digest(HISTORY / name) == sha for name, sha in hashes.items())
        save(HISTORY / 'archive-record.json', {
            'paper_id': PID, 'version': old_audit['source']['version'],
            'stable_pdf_path': str(stable_old_pdf), 'pdf_sha256': digest(stable_old_pdf),
            'original_files': hashes,
            'note': 'Original files preserved byte-for-byte; the old audit retains its original cache path. Use stable_pdf_path for its preserved PDF version.'})
    old_audit = json.loads((HISTORY / 'paper-audit.json').read_text())
    for name in ARTIFACTS:
        shutil.copy2(ROOT / name, PAPER / name)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    counts = {'theorems': len(census['claims']), 'interfaces': len(census['interfaces']),
              'source_members': sum(len(i['members']) for i in census['interfaces']),
              'direct_theorem_uses': sum(len(i['central_claim_uses']) for i in census['interfaces']),
              'related_theorem_connections': sum(len(i['related_theorems']) for i in census['interfaces'])}
    findings = [
        'The registered source is the 26-page published article (printed pages 52–77). All twelve actual Theorem environments were enumerated and their full statements visually checked, including every continuation. Conclusion ends on PDF page 24; references extend to page 26; appendices are separate and were not read.',
        'Published 4.8 corresponds to arXiv 4.9 (unprojected cryo-EM discrepancy formulas), and published 4.9 corresponds to arXiv 4.10 (projected transcendence degrees). Original statement bodies have the same mathematical hypotheses and conclusions; labels and copy-editing differ. Every direct-use ID and derived theorem path was rebuilt using the published identity mapping.',
        'Reviewed all 37 local source members against published PDF pages 5–12 and 14–20. Updated their evidence pages, source wording, dot notation for projected observations, and equation references (D.S11), (D.S31), (D.S57). The latter remain unresolved main-text references to excluded appendices.',
        'Reviewed the 12 direct-dependency sets and every local prerequisite edge. Rebuilt all 76 direct uses and 116 related connections with source-specific explanations; retained projected and unprojected paths separately, ambient conventions separately, and inline theorem binders as binders.',
        'Reviewed source keywords, naming passages and selectors for every interface. Published terminology is Continuous multireference alignment and Nondegenerate up to orbit. Corrected literal double-escaped TeX in naming contexts. All 37 members have an exact meaningful source selector match; every supplied selector matches its passage/label or a related same-paper theorem.',
        'In Section 3 the first white-noise display is printed f_g(t) + sigma dW(t), without dt after the signal. The later Gaussian-process integral includes dt. The archived original retains the first display as printed; it is not silently repaired.',
        'Definition 2.12 and the generic-gradient-span condition in Remark 2.9 remain distinct from a theorem conclusion. Spherical and radially indexed cryo-EM coefficient vectors remain distinct, sharing only the explicitly named Clebsch–Gordan convention.',
        'Theorem 2.11(b) restricts its landscape conclusion to the stated ball, while 2.13(b) imposes the ball restriction on the converse. The explicit radial bounds in 4.6, 4.8 and 4.9 are respectively 2, 1 and 4. These distinctions were checked in the source.'
    ]
    source = {key: meta[key] for key in ['source_url', 'version', 'pdf_sha256', 'pdf_pages', 'main_text_last_pdf_page']}
    source['pdf_path'] = str(pdf)
    audit = {
        'schema_version': 'statistical-paper-audit-v1', 'paper_id': PID, 'status': 'complete',
        'audit_kind': 'source_review', 'completed_at': now, 'source': source,
        'enumeration': {'theorem_ids': meta['intake_review']['theorem_ids'],
                        'method': 'Independent printed-heading enumeration followed by visual comparison of complete statements and all continuation pages; see inventory-review.json.',
                        'excluded_result_types': ['Lemma', 'Proposition', 'Corollary', 'Fact'], 'appendices_read': False},
        'validation': {'status': 'passed', 'validator': str(SKILL / 'validate_census.py'),
                       'checks': findings, 'independent_process_results': results},
        'counts': counts, 'source_notes': findings,
        'unresolved_source_references': [
            {**item, 'source': item['source'].replace('(D.11)', '(D.S11)').replace('(D.31)', '(D.S31)').replace('(D.57)', '(D.S57)')}
            for item in old_audit['unresolved_source_references']],
        'artifacts': {name: {'path': name, 'sha256': digest(PAPER / name)} for name in ARTIFACTS},
        'evidence': {p.name: {'path': str(p.relative_to(PAPER)), 'sha256': digest(p)}
                     for p in sorted((ROOT / 'evidence').iterdir()) if p.is_file()},
        'review_limits': ['Source fidelity and statement dependencies reviewed; theorem proofs and library availability are outside this audit.',
                         'Separate appendices excluded. Source-referenced basis and phase conventions remain unresolved as recorded.'],
        'previous_source_archive': 'source-history/arxiv-2107.01305v2/archive-record.json'
    }
    save(PAPER / 'paper-audit.json', audit)
    save(PAPER / 'registered-source-review.json', {
        'paper_id': PID, 'status': 'complete', 'method': 'source_content_revalidation', 'reviewed_at': now,
        'registered_pdf_sha256': source['pdf_sha256'], 'registered_pdf_pages': source['pdf_pages'],
        'checks': {key: True for key in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
        'findings': findings, 'evidence': list(audit['evidence'].values()),
        'reviewed_artifacts': {name: digest(PAPER / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']}
    })
    save(PAPER / 'checkpoint.json', {'paper_id': PID, 'stage': 'complete', 'status': 'complete',
         'updated_at': now, 'source': source, 'counts': counts,
         'current_review': 'registered-source-review.json', 'next_action': 'Proceed to the next queued paper.'})
    transition_path = PAPER / 'source-version-transition.json'
    transition = json.loads(transition_path.read_text())
    transition.update(status='complete', stage='published_census_validated_and_promoted', updated_at=now,
                      next_action='Continue with the next paper; the preserved arXiv census is historical.',
                      previous_source_archive=audit['previous_source_archive'],
                      current_census_sha256=digest(PAPER / 'ranked-interfaces.json'), observed_differences=findings)
    save(transition_path, transition)
    (PAPER / 'scripts').mkdir(exist_ok=True)
    (PAPER / 'scripts/README.md').write_text(
        '# Published-source census\n\nCurrent reproducible scripts are in `../source-transition/published/`: '
        '`save_inventory.py`, `build_census.py`, and `complete_review.py`. '
        'They use the preserved old extraction as a transcription scaffold and the separately reviewed published PDF as source authority. '
        'The old scripts and their original artifacts are archived under `../source-history/arxiv-2107.01305v2/`.\n')
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        subprocess.run([sys.executable, '-B', str(SKILL / 'validate_census.py'), str(PAPER / name)], check=True)
    # Verify evidence and all promoted artifact bytes, not only schema acceptance.
    for entry in list(audit['artifacts'].values()) + list(audit['evidence'].values()):
        assert digest(PAPER / entry['path']) == entry['sha256']
    print(json.dumps({'paper_id': PID, 'status': 'complete', 'counts': counts}))


if __name__ == '__main__':
    main()
