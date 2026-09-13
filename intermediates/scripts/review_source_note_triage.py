#!/usr/bin/env python3
"""Validate retained-note triage coverage and provenance, not mathematical resolution."""
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def item_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    aggregate = root / 'aggregate'
    path = aggregate / 'source-note-triage.json'
    before = path.read_bytes()
    triage = json.loads(before)
    followups = aggregate / 'working/source-followups.json'
    assert triage['source_followups_sha256'] == file_digest(followups)
    items = json.loads(followups.read_text())['items']
    paper_ids = [p['paper_id'] for p in json.loads((root / 'corpus.json').read_text())['papers']]
    seen = set()
    for decision in triage['decisions']:
        index = decision['item_index']
        assert isinstance(index, int) and 0 <= index < len(items) and index not in seen
        seen.add(index)
        item = items[index]
        assert decision['item_sha256'] == item_digest(item)
        assert all(decision[key] == item[key] for key in ('paper_id', 'source', 'field'))
        assert decision['status'] == 'triaged' and decision['reason'].strip()
        source = json.loads((root / item['source']).read_text())
        for field in item['field']:
            source = source[field]
        assert source == item['value'], (index, 'Retained note differs from current audit')
        if 'duplicate_of' in decision:
            original = items[decision['duplicate_of']]
            assert original['paper_id'] == item['paper_id'] and original['value'] == item['value']
    pending = triage['pending_item_indices']
    assert len(set(pending)) == len(pending)
    assert not seen.intersection(pending) and seen.union(pending) == set(range(len(items)))
    pending_papers = {items[index]['paper_id'] for index in pending}
    complete = [pid for pid in paper_ids if pid not in pending_papers]
    assert triage['completed_papers'] == complete
    assert triage['next_paper'] == next((pid for pid in paper_ids if pid in pending_papers), None)
    counts = dict(total_items=len(items), triaged_items=len(seen), pending_items=len(pending),
                  fully_triaged_papers=len(complete))
    assert triage['counts'] == counts
    validation = json.loads((aggregate / 'working/independent-validation.json').read_text())
    assert validation['status'] == 'passed'
    assert validation['census_sha256'] == file_digest(aggregate / 'working/ranked-interfaces.json')
    assert validation['grouping_review_sha256'] == file_digest(aggregate / 'grouping-review.json')
    assert path.read_bytes() == before, 'Triage changed while checking; rerun against current bytes'
    result = dict(
        status='passed', release_complete=False, checked_at=datetime.now(timezone.utc).isoformat(),
        scope='Checkpoint integrity and exact note provenance only; not proof of semantic resolution or final release completion.',
        triage_sha256=hashlib.sha256(before).hexdigest(),
        source_followups_sha256=file_digest(followups), counts=counts,
        checks=['Exact retained-note item hashes', 'Current audit fields match retained notes',
                'Duplicate records have identical values within the same paper',
                'Disjoint complete reviewed/pending partition',
                'All note items accounted for in each fully triaged paper',
                'Current aggregate and grouping checkpoint hashes'])
    destination = aggregate / 'source-note-triage-validation.json'
    fd, temporary = tempfile.mkstemp(prefix='.triage-validation-', dir=aggregate)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
        os.replace(temporary, destination)
    finally:
        Path(temporary).unlink(missing_ok=True)
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
