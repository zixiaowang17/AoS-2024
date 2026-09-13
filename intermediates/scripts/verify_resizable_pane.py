#!/usr/bin/env python3
"""Exercise dragging across the iframe, persistence, keyboard and mobile limits."""
import signal
import hashlib
import json
import sys
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


root = Path(__file__).resolve().parents[1]
report = root / 'aggregate' / (sys.argv[1] if len(sys.argv)>1 else 'report.html')
out = root / 'tooling/renderer-review/resizable-pane'
mode = 'preview' if 'preview' in report.name else 'final'
url = 'http://127.0.0.1:8765/' + str(report.relative_to(root.parents[1])) + '?view=apis'
errors=[]
shots=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
    context=browser.new_context(viewport={'width':1280,'height':900})
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url);page.locator('.api-result').first.click()
    divider=page.locator('#pane-divider')
    expect(divider).to_be_visible()
    expect(page.frame_locator('#page').locator('h1')).to_be_visible()
    frame_url=page.locator('#page').get_attribute('src')
    navigations=[];page.on('framenavigated',lambda f:navigations.append(f.url))
    def left():return page.locator('#reader').bounding_box()['x']
    def drag(target):
        box=divider.bounding_box();page.mouse.move(box['x']+box['width']/2,120)
        page.mouse.down();page.mouse.move(target,120,steps=12);page.mouse.up()
        assert not page.locator('body').evaluate("e=>e.classList.contains('resizing')")
    drag(710);assert abs(left()-710)<2
    assert not navigations and page.locator('#page').get_attribute('src')==frame_url
    name=f'{mode}-wide-list.png';page.screenshot(path=str(out/name));shots.append(name)
    page.locator('#close').click();page.locator('.api-result').first.click();assert abs(left()-710)<2
    page.reload();expect(divider).to_be_visible();assert abs(left()-710)<2
    divider.focus();page.keyboard.press('ArrowLeft');assert abs(left()-686)<2
    page.keyboard.press('Shift+ArrowRight');assert abs(left()-750)<2
    page.keyboard.press('Home');assert abs(left()-310)<2
    page.keyboard.press('End');assert abs(left()-920)<2
    drag(50);assert abs(left()-310)<2
    name=f'{mode}-wide-reader.png';page.screenshot(path=str(out/name));shots.append(name)
    drag(1250);assert abs(left()-920)<2
    divider.dblclick();assert abs(left()-1280*.38)<2
    # Loss of capture/cancel cannot leave the iframe shield enabled.
    box=divider.bounding_box();page.mouse.move(box['x']+6,100);page.mouse.down()
    divider.dispatch_event('pointercancel');page.mouse.up()
    assert not page.locator('body').evaluate("e=>e.classList.contains('resizing')")
    drag(640)
    for width in (900,801):
        page.set_viewport_size({'width':width,'height':900})
        assert 309<=left()<=width-359
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    page.set_viewport_size({'width':390,'height':844})
    expect(divider).to_be_hidden();assert left()==0
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    name=f'{mode}-mobile.png';page.screenshot(path=str(out/name));shots.append(name)
    page.set_viewport_size({'width':1280,'height':900});assert abs(left()-640)<2
    assert int(divider.get_attribute('aria-valuenow'))==50
    # Storage denial must preserve dragging and reading.
    denied=browser.new_context(viewport={'width':1280,'height':900})
    denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage denied')}})")
    other=denied.new_page();other.on('pageerror',lambda e:errors.append(str(e)))
    other.goto(url);other.locator('.api-result').first.click();other.locator('#pane-divider').focus();other.keyboard.press('ArrowRight')
    expect(other.frame_locator('#page').locator('h1')).to_be_visible();denied.close()
    # File reports support the same control without a server.
    local=browser.new_context(offline=True,viewport={'width':1280,'height':900})
    other=local.new_page();other.on('pageerror',lambda e:errors.append(str(e)))
    other.goto(report.as_uri()+'?view=apis');other.locator('.api-result').first.click()
    other.locator('#pane-divider').focus();other.keyboard.press('ArrowRight')
    expect(other.frame_locator('#page').locator('h1')).to_be_visible()
    saved_left=other.locator('#reader').bounding_box()['x'];other.reload()
    expect(other.frame_locator('#page').locator('h1')).to_be_visible()
    assert abs(other.locator('#reader').bounding_box()['x']-saved_left)<2
    local.close()
    close_test_browser(browser)
assert not errors,errors
result={'status':'passed','checked_at':datetime.now(timezone.utc).isoformat(),
        'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),
        'checks':['Dragging across the iframe without reloading it','Persistence after close/reopen and reload',
                  'Keyboard arrows, Shift, Home/End and double-click reset','Minimum pane widths and viewport resizing',
                  'Pointer cancellation clears drag state','Mobile full-screen reader hides divider',
                  'Blocked storage and offline file reading remain usable'],
        'screenshots':shots,'page_errors':errors,'visual_inspection':'pending'}
(out/f'{mode}-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS all resizable-pane checks',flush=True)
