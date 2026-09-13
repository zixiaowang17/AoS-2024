"""Check completion against the fixed source register and a pinned source review.

This gate verifies review provenance, not mathematical correctness. The review
must be written only after actually inspecting the source and census contents.
"""
import hashlib
import json
from pathlib import Path

REVIEW_CHECKS = ('theorem_inventory', 'original_statements', 'source_passages',
                 'dependencies', 'names_and_highlights')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_registered_source(folder, audit, registered, repository):
    pdf = repository / registered['pdf_path']
    result = {'registered_pdf_path': str(pdf),
              'registered_pdf_sha256': registered.get('sha256'),
              'prior_source_review_status': audit.get('status')}
    if registered.get('status') != 'verified_local' or not pdf.is_file():
        return {**result, 'status': 'registered_source_unavailable'}
    if digest(pdf) != registered.get('sha256'):
        return {**result, 'status': 'registered_source_changed'}
    if audit['source']['pdf_sha256'] != registered['sha256']:
        return {**result, 'status': 'source_version_review_required'}
    review_path = folder / 'registered-source-review.json'
    if not review_path.is_file():
        return {**result, 'status': 'source_revalidation_pending'}
    review = json.loads(review_path.read_text())
    valid = (review.get('status') == 'complete'
             and review.get('paper_id') == audit['paper_id']
             and review.get('registered_pdf_sha256') == registered['sha256']
             and review.get('registered_pdf_pages') == registered['pdf_pages']
             and review.get('method') == 'source_content_revalidation'
             and all(review.get('checks', {}).get(k) is True for k in REVIEW_CHECKS)
             and bool(review.get('findings'))
             and bool(review.get('evidence')))
    for name in ('paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json'):
        valid = valid and review.get('reviewed_artifacts', {}).get(name) == digest(folder / name)
    if not valid:
        return {**result, 'status': 'source_revalidation_pending'}
    return {**result, 'status': 'complete', 'registered_source_review_sha256': digest(review_path)}
