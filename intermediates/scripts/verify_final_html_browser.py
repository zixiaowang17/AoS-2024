#!/usr/bin/env python3
"""Exercise the approved reference and full report in an isolated local Chrome session."""
import json
import signal
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright, expect

def close_test_browser(browser):
    def timeout(signum, frame):
        raise TimeoutError('Chrome shutdown did not acknowledge completion')
    previous=signal.signal(signal.SIGALRM,timeout)
    signal.alarm(15)
    try:
        browser.close()
    except TimeoutError:
        print('Browser checks complete; disposing an unresponsive shutdown through Playwright.',flush=True)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM,previous)


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
BASE = 'http://127.0.0.1:8765/'
OUT = ROOT / 'tooling/renderer-review/final-browser'


def index(path):
    return json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', path.read_text(), re.S).group(1))


def url(path):
    return BASE + str(path.relative_to(REPO))


def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    baseline = json.loads((ROOT / 'tooling/renderer-review/approved-two-paper-baseline.json').read_text())
    targets = {'reference': Path(baseline['reference_report']), 'final': ROOT / 'aggregate/report.html'}
    snapshots = []
    metrics = {}
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless=True)
        version = browser.version
        for width, height in [(1280, 900), (390, 844)]:
            for label, path in targets.items():
                data = index(path)
                context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1)
                page = context.new_page()
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.goto(url(path), wait_until='load')
                expect(page.locator('#results')).to_have_text(f'{len(data["papers"])} of {len(data["papers"])} papers')
                no_overflow(page)
                page.screenshot(path=str(OUT / f'{label}-{width}-catalog.png'))
                snapshots.append(f'{label}-{width}-catalog.png')
                page.locator('#tab-apis').click()
                expect(page.locator('#results')).to_have_text(f'{len(data["interfaces"])} APIs')
                if label == 'final':
                    expect(page.locator('#work-filters')).to_be_visible()
                    expect(page.locator('#work-filters button')).to_have_count(3)
                    for decision, caption in [('use_mathlib','Use mathlib'),('small_adaptation','Small adaptation'),('new_infrastructure','New infrastructure')]:
                        count = sum(x['work_status'] == decision for x in data['interfaces'])
                        page.locator(f'#work-filters button[data-work-status="{decision}"]').click()
                        expect(page.locator(f'#work-filters button[data-work-status="{decision}"]')).to_have_attribute('aria-pressed','true')
                        expect(page.locator('#results')).to_have_text(f'{count} of 2486 APIs')
                        assert page.locator('.api-result .work-status').count() == count
                        assert all(x == caption for x in page.locator('.api-result .work-status').all_text_contents())
                    page.locator('#work-filters button[data-work-status="use_mathlib"]').click()
                    page.reload()
                    expect(page.locator('#work-status')).to_have_value('use_mathlib')
                    page.locator('.api-result').first.click()
                    expect(page.frame_locator('#page').locator('.work-audit .work-status')).to_have_text('Use mathlib')
                    screenshot = f'final-{width}-use-mathlib.png'
                    page.screenshot(path=str(OUT / screenshot)); snapshots.append(screenshot)
                    page.locator('#close').click()
                    expect(page.locator('#work-status')).to_have_value('use_mathlib')
                    page.locator('#tab-paper').click()
                    expect(page.locator('#work-filters')).to_be_hidden()
                    page.locator('#tab-apis').click()
                    expect(page.locator('#work-status')).to_have_value('use_mathlib')
                    page.locator('#work-filters button[data-work-status="use_mathlib"]').click()
                    expect(page.locator('.api-result')).to_have_count(len(data['interfaces']))
                    expect(page.locator('#work-filters [aria-pressed=true]')).to_have_count(0)
                    page.locator('#ranking-note summary').click()
                    for text in ['Green — Use mathlib','Yellow — Small adaptation','Red — New infrastructure','not code length']:
                        assert text in page.locator('#ranking-note').inner_text()
                    screenshot=f'final-{width}-about-ranking.png'
                    page.screenshot(path=str(OUT/screenshot));snapshots.append(screenshot)
                    page.locator('#ranking-note summary').click()
                assert page.evaluate("[...document.querySelectorAll('.api-result')].every(e=>e.querySelector('.rank').getBoundingClientRect().right+8<=e.querySelector('.name').getBoundingClientRect().left)")
                assert page.locator('#ranking-note').get_attribute('open') is None
                page.locator('#search').fill('Cost function')
                api = next(a for a in data['interfaces'] if a['name'] == 'Cost function')
                button = page.locator(f'button[data-route="{api["route"]}"]')
                expect(button.locator('.rank')).to_have_text(str(api['rank']))
                page.locator('#kind').select_option(api['kind'])
                button.click()
                frame = page.frame_locator('#page')
                expect(frame.locator('.original-definition')).to_be_visible()
                if label == 'final':
                    expect(frame.locator('.work-audit .work-status')).to_have_attribute('data-work-status',api['work_status'])
                assert frame.locator('.symbol-highlight').count() > 0
                expect(page.locator('#close')).to_be_focused()
                no_overflow(page)
                assert page.evaluate("[...document.querySelectorAll('.api-result')].every(e=>e.querySelector('.rank').getBoundingClientRect().right+8<=e.querySelector('.name').getBoundingClientRect().left)")
                if width < 800:
                    box = page.locator('#reader').bounding_box()
                    assert box['x'] == 0 and abs(box['width'] - width) < 1
                page.screenshot(path=str(OUT / f'{label}-{width}-reader.png'))
                snapshots.append(f'{label}-{width}-reader.png')
                with context.expect_page() as popup:
                    page.locator('#open-page').click()
                standalone = popup.value
                standalone.wait_for_load_state()
                expect(standalone.locator('h1')).to_have_text('Cost function')
                no_overflow(standalone)
                metrics[f'{label}-{width}'] = standalone.evaluate('''() => {
                    const props = ['fontFamily','fontSize','lineHeight','color','backgroundColor','paddingLeft','borderLeftWidth','borderLeftColor'];
                    const out = {};
                    for (const selector of ['body','.reading','.statement','.original-definition','.theorems-heading']) {
                        const css = getComputedStyle(document.querySelector(selector));
                        out[selector] = Object.fromEntries(props.map(p=>[p,css[p]]));
                    }
                    return out;
                }''')
                standalone.close()
                frame.locator('h1').click()
                page.keyboard.press('Escape')
                expect(page.locator('#reader')).to_be_hidden()
                expect(button).to_be_focused()
                expect(page.locator('#search')).to_have_value('Cost function')
                expect(page.locator('#kind')).to_have_value(api['kind'])
                page.locator('#tab-paper').click()
                page.locator('#search').fill('aos-2024-v52-i04-p1616')
                paper = next(x for x in data['papers'] if x['route'] == 'paper:aos-2024-v52-i04-p1616')
                paper_button = page.locator(f'button[data-route="{paper["route"]}"]')
                paper_button.click()
                frame = page.frame_locator('#page')
                expect(frame.locator('.theorem').first).to_be_visible()
                assert frame.locator('.symbol-highlight').count() == 0
                details = frame.locator('details.requirements').first
                details.locator('summary').click()
                details_id = details.get_attribute('id')
                link = details.locator('a[data-route]').first
                destination = link.get_attribute('data-route')
                link.click()
                expect(page.locator('#back')).to_be_visible()
                expect(page.frame_locator('#page').locator('.original-definition').first).to_be_visible()
                page.locator('#back').click()
                expect(page.frame_locator('#page').locator(f'#{details_id}')).to_have_attribute('open', '')
                page.locator('#close').click()
                expect(page.locator('#search')).to_have_value('aos-2024-v52-i04-p1616')
                expect(paper_button).to_be_focused()
                page.locator('#tab-apis').click()
                expect(page.locator('#search')).to_have_value('Cost function')
                page.locator('#search').fill('no-matches-zzzzzzzzzz')
                expect(page.locator('#results')).to_have_text(f'0 of {len(data["interfaces"])} APIs')
                print(f'PASS {label} {width}: tabs/search/ranks/kind/reader/Escape/focus/standalone/Back', flush=True)
                context.close()
            assert metrics[f'reference-{width}'] == metrics[f'final-{width}'], metrics
        # Standalone mathematical, prose and assumption examples, plus a large shared API.
        path = targets['final']
        data = index(path)
        examples = ['Cost function', 'Dirichlet process', 'Base measure', 'Conditional expectation']
        for width, height in [(1280, 900), (390, 844)]:
            context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1)
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            for n, term in enumerate(examples):
                record = next(a for a in data['interfaces'] if a['name'].startswith(term))
                page.goto(url(path.parent / record['url']), wait_until='load')
                expect(page.locator('.original-definition').first).to_be_visible()
                no_overflow(page)
                assert page.locator('.symbol-highlight').count() > 0
                for block in page.locator('.original-definition').all():
                    assert block.locator('.symbol-highlight').count() > 0
                screenshot = f'final-{width}-example-{n}.png'
                page.screenshot(path=str(OUT / screenshot))
                snapshots.append(screenshot)
                if term == 'Base measure':
                    assert 'Assumption 4.1' in page.locator('.original-definition').first.inner_text()
                if term == 'Conditional expectation':
                    assert page.locator('.paper-group').count() >= 5
            context.close()
        # Verify local-file reading without a network connection.
        context = browser.new_context(offline=True)
        page = context.new_page()
        record = next(a for a in data['interfaces'] if a['name'] == 'Cost function')
        page.goto((path.parent / record['url']).as_uri(), wait_until='load')
        expect(page.locator('.original-definition')).to_be_visible()
        assert page.locator('.symbol-highlight').count() > 0
        page.goto(path.as_uri(), wait_until='load')
        expect(page.locator('#results')).to_have_text('113 of 113 papers')
        page.locator('#tab-apis').click()
        page.locator('#search').fill('Cost function')
        page.locator(f'button[data-route="{record["route"]}"]').click()
        expect(page.frame_locator('#page').locator('.original-definition')).to_be_visible()
        page.locator('#close').click()
        expect(page.locator('#reader')).to_be_hidden()
        context.close()
        close_test_browser(browser)
    assert not errors, errors
    result = {'status': 'passed', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'report_sha256': hashlib.sha256(targets['final'].read_bytes()).hexdigest(),
              'browser': 'Isolated headless Google Chrome via Playwright; in-app browser tool unavailable in this session',
              'browser_version': version, 'viewports': [[1280,900],[390,844]],
              'computed_style_comparison': 'Identical reference/final metrics at both widths',
              'computed_styles': metrics, 'screenshots': snapshots, 'page_errors': errors,
              'checks': ['Tabs, contextual search, no-result state and API-kind filter',
                         'All three status labels and exact filtered counts; toggle buttons, About ranking, reload, reader close and tab switches',
                         'Rank and name never overlap, including four-digit ranks in narrow readers',
                         'Unchanged semantic ranks after filtering', 'Collapsed About ranking',
                         'Reader Close, Escape, focus restoration and mobile full-screen layout',
                         'Open separately and standalone source highlights',
                         'Paper-to-API navigation and Back restoring expanded requirements',
                         'Retained search across reader navigation and tabs',
                         'No horizontal page overflow for representative source types and shared API',
                         'Offline standalone and full index/search/reader files work'],
              'visual_inspection': 'pending'}
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS all browser checks; screenshots ready for visual inspection', flush=True)


if __name__ == '__main__':
    main()
