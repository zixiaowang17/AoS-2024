import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from registered_source_gate import REVIEW_CHECKS, check_registered_source, digest

class SourceGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'paper.pdf').write_bytes(b'%PDF-pinned source')
        self.audit = {'paper_id': 'paper', 'status': 'complete',
                      'source': {'pdf_sha256': digest(self.root/'paper.pdf')}}
        self.entry = {'pdf_path': 'paper.pdf', 'sha256': self.audit['source']['pdf_sha256'],
                      'pdf_pages': 3, 'status': 'verified_local'}
        for name in ('paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json'):
            (self.root/name).write_text('{}')

    def check(self):
        return check_registered_source(self.root, self.audit, self.entry, self.root)['status']

    def save_review(self):
        self.review = {'paper_id': 'paper', 'status': 'complete',
            'registered_pdf_sha256': self.entry['sha256'], 'registered_pdf_pages': 3,
            'method': 'source_content_revalidation',
            'checks': {key: True for key in REVIEW_CHECKS},
            'findings': ['Specific source correspondence checked'], 'evidence': [{'page': 1}],
            'reviewed_artifacts': {name: digest(self.root/name) for name in
                ('paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json')}}
        (self.root/'registered-source-review.json').write_text(json.dumps(self.review))

    def test_old_complete_flag_is_insufficient(self):
        self.assertEqual(self.check(), 'source_revalidation_pending')

    def test_changed_registered_version_requires_source_review(self):
        self.save_review()
        (self.root/'paper.pdf').write_bytes(b'%PDF-new version')
        self.entry['sha256'] = digest(self.root/'paper.pdf')
        self.assertEqual(self.check(), 'source_version_review_required')

    def test_tampered_source_is_not_counted(self):
        self.save_review()
        (self.root/'paper.pdf').write_bytes(b'%PDF-corrupted')
        self.assertEqual(self.check(), 'registered_source_changed')

    def test_artifact_edits_invalidate_prior_review(self):
        self.save_review()
        self.assertEqual(self.check(), 'complete')
        (self.root/'ranked-interfaces.json').write_text('{"changed":true}')
        self.assertEqual(self.check(), 'source_revalidation_pending')

    def test_hash_only_review_cannot_claim_content_review(self):
        self.save_review()
        self.review['method'] = 'hash_only'
        (self.root/'registered-source-review.json').write_text(json.dumps(self.review))
        self.assertEqual(self.check(), 'source_revalidation_pending')

if __name__ == '__main__':
    unittest.main()
