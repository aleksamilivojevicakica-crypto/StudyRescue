"""Browser tests via HTML injection; CI blocks navigation to local URLs."""
from pathlib import Path
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
css=(r/'assets/styles.css').read_text()
js=(r/'assets/app.js').read_text()
trans=(r/'assets/translations.js').read_text()

def load(browser, lang, pg, width=1280, height=850):
    page=browser.new_page(viewport={'width':width,'height':height},accept_downloads=True)
    page.set_content((r/lang/(pg+'.html')).read_text())
    page.add_style_tag(content=css)
    page.add_script_tag(content=trans)
    page.add_script_tag(content=js)
    return page

with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    # Test every localized view + newly added chat and export calendar.
    for lang in ('en','de','fr'):
        for pg in ('overview','tasks','planner','coach','insights','settings'):
            page=load(b,lang,pg)
            assert page.locator('#pageContent').inner_text().strip(),(lang,pg)
            if pg=='coach':
                assert page.locator('#chatForm').count()==1
                assert page.locator('#chatInput').get_attribute('maxlength')=='600'
            if pg=='settings':
                assert page.locator('#icsBtn').count()==1
            page.close()
    page=load(b,'en','overview')
    page.locator('#newTaskHeader').click()
    page.locator('#inputTitle').fill('Read chemistry chapter 7')
    page.locator('#inputMinutes').fill('90')
    page.locator('#inputSubject').select_option('science')
    page.locator('#taskForm button[type=submit]').click()
    assert page.locator('.stat-value').first.inner_text()=='1'
    page.screenshot(path=r/'preview_studyrescue4.png',full_page=True)
    page.close()
    page=load(b,'en','settings')
    # Click .ics even if there are zero events: it must still output valid VCALENDAR.
    with page.expect_download(timeout=2000) as info:
        page.locator('#icsBtn').click()
    download=info.value
    assert download.suggested_filename=='studyrescue-study-plan.ics'
    path=r/'tests'/'tmp.ics';download.save_as(path)
    cal=path.read_text();path.unlink()
    assert 'BEGIN:VCALENDAR' in cal and 'END:VCALENDAR' in cal
    page.close()
    page=load(b,'en','coach')
    page.screenshot(path=r/'preview_ai_coach4.png',full_page=True)
    page.close()
    page=load(b,'fr','overview',width=390,height=844)
    assert page.locator('#mobileMenu').is_visible()
    page.locator('#mobileMenu').click()
    assert page.locator('#sidebar').evaluate('(node)=>node.classList.contains("open")')
    page.close()
    b.close()
print('PASS: new coach chat + ICS button for EN/DE/FR, task creation, file export and mobile menu in Chromium')
