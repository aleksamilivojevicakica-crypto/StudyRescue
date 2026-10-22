"""Browser smoke-test all language/page combinations without outside network access.
The CI environment blocks top-level browser navigation; we inject real HTML + assets
into an isolated Chromium document. No AI API is called.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
translations=(root/'assets/translations.js').read_text()
app=(root/'assets/app.js').read_text()
css=(root/'assets/styles.css').read_text()
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for lang in ['en','de','fr']:
        for page_name in ['overview','tasks','planner','coach','insights','settings']:
            page=browser.new_page(viewport={'width':1280,'height':850})
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.set_content((root/lang/(page_name+'.html')).read_text())
            page.add_style_tag(content=css)
            page.add_script_tag(content=translations)
            page.add_script_tag(content=app)
            assert page.locator('h1').count()>0,(lang,page_name,'missing heading')
            assert page.locator('#mainNav .nav-link').count()==6,(lang,page_name,'missing sidebar')
            assert page.locator('#languageSwitch a').count()==3,(lang,page_name,'missing language buttons')
            assert page.locator('#pageContent').inner_text().strip(),(lang,page_name,'empty page')
            if page_name == 'overview' and lang == 'en':
                page.locator('#newTaskHeader').click()
                assert page.locator('#taskDialog').evaluate('(el)=>el.open')
                page.locator('#inputTitle').fill('Test integration')
                page.locator('#taskForm button[type=submit]').click()
                assert page.locator('.stat-value').first.inner_text()=='1','saving task did not update dashboard'
                assert 'Test integration' in page.locator('#pageContent').inner_text()
            page.close()
    browser.close()
assert not errors,errors
print('PASS: all 18 pages rendered in Chromium; navigation, translations and add-task interaction work.')
