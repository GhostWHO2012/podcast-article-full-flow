const { chromium } = require('playwright-core');
const q = process.argv[2] || 'Silicon Valley Girl site:mp.weixin.qq.com';
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const exe = 'C:\\Users\\Administrator\\AppData\\Local\\ms-playwright\\chromium-1234\\chrome-win64\\chrome.exe';
  const browser = await chromium.launch({ executablePath: exe, headless: true, args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' });
  const url = 'https://www.bing.com/search?q=' + encodeURIComponent(q) + '&count=50';
  console.log('OPEN', url);
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto warn:', e.message));
  await page.waitForLoadState('load', { timeout: 30000 }).catch(() => {});
  await sleep(4000);
  const txt = await page.evaluate(() => document.body.innerText || '');
  console.log('BODY_LEN', txt.length, 'CAPTCHA?', /验证码|robot|unusual traffic|verify/.test(txt));
  const links = await page.evaluate(() => {
    const out = [];
    for (const a of document.querySelectorAll('a')) {
      const h = a.getAttribute('href') || '';
      const t = (a.innerText||'').replace(/\s+/g,' ').trim();
      if (h.includes('mp.weixin.qq.com/s/') && t.length > 4) out.push({title:t, href:h});
    }
    return out.slice(0, 30);
  });
  console.log('FOUND', links.length);
  console.log(JSON.stringify(links, null, 2));
  await browser.close();
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
