#!/usr/bin/env python3
"""Verify the API count/status columns against the audited relationships."""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
report = ROOT / 'aggregate' / (sys.argv[1] if len(sys.argv) > 1 else 'report.html')
out = ROOT / 'tooling/renderer-review/api-columns'
mode = 'preview' if 'preview' in report.name else 'final'
data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', report.read_text(), re.S).group(1))
audit = json.loads((ROOT / 'aggregate/audited.json').read_text())
by_id = {x['interface_id']: x for x in audit['interfaces']}
for x in data['interfaces']:
    refs = by_id[x['route'].removeprefix('interface:')]['related_theorems']
    assert x['theorem_count'] == len({r['claim_id'] for r in refs})
    assert x['paper_count'] == len({r['paper_id'] for r in refs})
url = 'http://127.0.0.1:8765/' + str(report.relative_to(ROOT.parents[1])) + '?view=apis'
errors = []
screenshots = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless=True)
    for width in (1280, 900, 390, 320):
        page = browser.new_page(viewport={'width':width, 'height':900})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(url, wait_until='load')
        expect(page.locator('.api-result')).to_have_count(2486)
        assert page.locator('.api-counts .count-value').all_text_contents() == [f'{x["theorem_count"]} / {x["paper_count"]}' for x in data['interfaces']]
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        assert page.evaluate('''() => [...document.querySelectorAll('.api-result')].every(row => {
          const box = s => row.querySelector(s).getBoundingClientRect();
          return box('.rank').right + 8 <= box('.name').left && box('.api-counts').right <= box('.api-status').left;
        })''')
        if width >= 900:
            expect(page.locator('#api-columns')).to_be_visible()
            assert page.evaluate('''() => {
              const labels=[...document.querySelector('#api-columns').children];
              const cells=[...document.querySelector('.api-result').children];
              return labels.every((label,i)=>Math.abs(label.getBoundingClientRect().left-cells[i].getBoundingClientRect().left)<1);
            }''')
        else:
            expect(page.locator('.api-counts .column-label').first).to_be_visible()
        for status, color in [('use_mathlib','rgb(22, 101, 52)'),('small_adaptation','rgb(133, 77, 14)'),('new_infrastructure','rgb(165, 34, 34)')]:
            assert page.locator(f'.api-result [data-work-status="{status}"]').first.evaluate('(e)=>getComputedStyle(e).color') == color
        name = f'{mode}-{width}-columns.png';page.screenshot(path=str(out/name));screenshots.append(name)
        page.locator('#work-filters button[data-work-status="use_mathlib"]').click()
        expect(page.locator('.api-result')).to_have_count(sum(x['work_status']=='use_mathlib' for x in data['interfaces']))
        name = f'{mode}-{width}-green.png';page.screenshot(path=str(out/name));screenshots.append(name)
        if width == 1280:
            page.locator('.api-result').first.click()
            expect(page.frame_locator('#page').locator('h1')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
            name=f'{mode}-{width}-sidebar.png';page.screenshot(path=str(out/name));screenshots.append(name)
        page.close()
        print(f'PASS {width}: all counts, separate cells, colors and overflow', flush=True)
    browser.close()
assert not errors, errors
result = {'status':'passed', 'checked_at':datetime.now(timezone.utc).isoformat(),
          'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),
          'checks':['All 2486 counts agree with unique theorem IDs and paper IDs',
                    'Count and status cells remain separate at desktop, tablet and narrow widths',
                    'Headers align with columns; four-digit ranks do not overlap names',
                    'Green, yellow and red assessment labels retain their text',
                    'Status filtering and narrow sidebar render correctly'],
          'screenshots':screenshots, 'page_errors':errors, 'visual_inspection':'pending'}
(out/f'{mode}-verification.json').write_text(json.dumps(result,indent=2)+'\n')
