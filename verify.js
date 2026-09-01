const { chromium } = require('playwright-core');
const url = process.argv[2] || 'https://mp.weixin.qq.com/s/ndUoKBXMZU2agqB0tOK7bg';

(async () => {
  const exe = 'C:\\Users\\Administrator\\AppData\\Local\\ms-playwright\\chromium-1234\\chrome-win64\\chrome.exe';
  const browser = await chromium.launch({ executablePath: exe, headless: true, args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 420, height: 800 }, userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto warn:', e.message));
  await page.waitForLoadState('load', { timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(4000);
  const info = await page.evaluate(() => {
    const title = document.title;
    const content = document.querySelector('#js_content');
    const text = (content ? content.innerText : document.body.innerText || '').replace(/\s+/g, ' ').trim();
    return { title, textLen: text.length, snippet: text.slice(0, 200), hasVerify: /环境异常|验证|请点击|verify/i.test(document.body.innerText||'') };
  });
  console.log('TITLE:', info.title);
  console.log('TEXT_LEN:', info.textLen);
  console.log('HAS_VERIFY_PAGE:', info.hasVerify);
  console.log('SNIPPET:', info.snippet);
  await browser.close();
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
