const { chromium } = require('playwright-core');

const url = process.argv[2] || 'https://mp.weixin.qq.com/s/ndUoKBXMZU2agqB0tOK7bg';
const out = process.argv[3] || 'C:\\Users\\Administrator\\WorkBuddy\\2026-08-24-15-20-36\\outputs\\wx_article_full2.png';

(async () => {
  const exe = 'C:\\Users\\Administrator\\AppData\\Local\\ms-playwright\\chromium-1234\\chrome-win64\\chrome.exe';
  const browser = await chromium.launch({
    executablePath: exe,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage({
    viewport: { width: 420, height: 800 },
    deviceScaleFactor: 2,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
  });

  // 不依赖 networkidle（部分文章有持续轮询），用 domcontentloaded + 固定等待
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto warn:', e.message));
  await page.waitForLoadState('load', { timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(3000);

  // 滚动到底部，触发所有懒加载图片（带重试，避免重定向瞬间 context 销毁）
  for (let i = 0; i < 3; i++) {
    try {
      await page.evaluate(async () => {
        await new Promise(res => {
          let y = 0;
          const step = 300;
          const t = setInterval(() => {
            window.scrollBy(0, step);
            y += step;
            if (y >= document.body.scrollHeight) { clearInterval(t); res(); }
          }, 80);
        });
        window.scrollTo(0, 0);
      });
      break;
    } catch (e) {
      console.log('scroll retry', i, e.message);
      await page.waitForTimeout(1500);
    }
  }
  await page.waitForTimeout(4000);

  await page.screenshot({ path: out, fullPage: true });
  console.log('SAVED:', out);

  await browser.close();
})().catch(e => { console.error('FATAL:', e); process.exit(1); });
