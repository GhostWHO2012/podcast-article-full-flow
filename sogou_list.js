const { chromium } = require('playwright-core');

const query = process.argv[2] || 'Silicon Valley Girl';
const outJson = process.argv[3] || 'C:\\Users\\Administrator\\WorkBuddy\\2026-08-24-15-20-36\\sogou_articles.json';

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const exe = 'C:\\Users\\Administrator\\AppData\\Local\\ms-playwright\\chromium-1234\\chrome-win64\\chrome.exe';
  const browser = await chromium.launch({ executablePath: exe, headless: true, args: ['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1100, height: 900 }, userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' });

  // 1) 账号搜索页
  const gzhUrl = 'https://weixin.sogou.com/weixin?type=gzh&query=' + encodeURIComponent(query);
  console.log('OPEN', gzhUrl);
  await page.goto(gzhUrl, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto warn:', e.message));
  await page.waitForLoadState('load', { timeout: 30000 }).catch(() => {});
  await sleep(5000);

  const bodyText = await page.evaluate(() => document.body.innerText || '');
  console.log('CAPTCHA?', /验证码|antispider|访问过于频繁|请输入/.test(bodyText));
  console.log('BODY_LEN', bodyText.length);

  // 提取账号卡片里的文章列表链接（type=2&...&account=）
  const accountLink = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a'));
    for (const a of links) {
      const h = a.getAttribute('href') || '';
      if (h.includes('type=2') && h.includes('account=')) return h;
      if (h.includes('weixin?type=2') && /gzh|account/.test(h)) return h;
    }
    return null;
  });
  console.log('ACCOUNT_LINK', accountLink);

  let articles = [];
  if (accountLink) {
    const abs = accountLink.startsWith('http') ? accountLink : 'https://weixin.sogou.com' + accountLink;
    console.log('OPEN articles', abs);
    await page.goto(abs, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto2 warn:', e.message));
    await page.waitForLoadState('load', { timeout: 30000 }).catch(() => {});
    await sleep(5000);
    articles = await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('a'));
      const res = [];
      for (const a of cards) {
        const h = a.getAttribute('href') || '';
        const t = (a.innerText || '').replace(/\s+/g, ' ').trim();
        if ((h.includes('link?url') || h.includes('mp.weixin.qq.com/s/')) && t.length > 4) {
          res.push({ title: t, href: h.startsWith('http') ? h : 'https://weixin.sogou.com' + h });
        }
      }
      return res.slice(0, 20);
    });
  }
  console.log('ARTICLES_FOUND', articles.length);
  console.log(JSON.stringify(articles, null, 2));

  require('fs').writeFileSync(outJson, JSON.stringify(articles, null, 2));
  await browser.close();
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
