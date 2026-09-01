const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { chromium } = require('playwright-core');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const OUT_DIR = 'C:/Users/Administrator/WorkBuddy/2026-08-24-15-20-36/outputs/svg_articles';
const IMG_DIR = path.join(OUT_DIR, 'images');

const URLS = [
  'https://mp.weixin.qq.com/s/f9kqycryKQE6Ff7S5-pkLQ',
  'https://mp.weixin.qq.com/s/u31XEfHqRouxJ1zLWlNQAg',
  'https://mp.weixin.qq.com/s/0Ln2bwX0sGb93D0ZhS7dFw',
  'https://mp.weixin.qq.com/s/cKAKXe0aJ6kNFPBDqc8COQ',
  'https://mp.weixin.qq.com/s/YjAcINxD3-AOE8ltGIgKBg',
  'https://mp.weixin.qq.com/s/LE76dre_QALg-3oiPmdpKQ',
  'https://mp.weixin.qq.com/s/Y-O367LgrM2pcamYglwTiw',
  'https://mp.weixin.qq.com/s/EppqydP6sOy28vk9Rfmy9w',
  'https://mp.weixin.qq.com/s/0tEHXXpg2-pw3b3nI2_V6A',
];

function downloadImage(url, dest, referer) {
  return new Promise((resolve) => {
    if (!url || !/^https?:\/\//.test(url)) return resolve(null);
    const lib = url.startsWith('https') ? https : http;
    const req = lib.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Referer': referer,
      },
      timeout: 30000,
    }, (res) => {
      if (res.statusCode !== 200) { res.resume(); return resolve(null); }
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        try { fs.writeFileSync(dest, Buffer.concat(chunks)); resolve(true); }
        catch (e) { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
  });
}

function sanitize(s) { return (s || '').replace(/[\\/:*?"<>|\n\r]/g, '_').slice(0, 60); }
function tsToDate(ts) {
  const n = parseInt(ts, 10);
  if (!n) return '';
  const d = new Date(n * 1000);
  if (isNaN(d)) return '';
  return d.toISOString().slice(0, 10);
}
function slugify(s, i) { return (i + 1) + '_' + sanitize(s).slice(0, 40); }

(async () => {
  fs.mkdirSync(IMG_DIR, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const results = [];

  for (let i = 0; i < URLS.length; i++) {
    const url = URLS[i];
    const page = await browser.newPage({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' });
    let info = { index: i + 1, url, title: '', author: '', date: '', text: '', images: [], error: '' };
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForSelector('#js_content', { timeout: 20000 }).catch(() => {});
      await page.waitForTimeout(2500);

      const meta = await page.evaluate(() => {
        const og = (n) => { const e = document.querySelector('meta[property="og:' + n + '"]'); return e ? e.getAttribute('content') : ''; };
        const title = og('title') || (document.querySelector('#activity-name') ? document.querySelector('#activity-name').innerText : '') || document.title;
        const nickname = (document.querySelector('#js_name') && document.querySelector('#js_name').innerText) || '';
        const ctMatch = document.documentElement.innerHTML.match(/var\s+ct\s*=\s*["']?(\d+)["']?/);
        const ct = ctMatch ? ctMatch[1] : '';
        const content = document.querySelector('#js_content');
        const text = content ? content.innerText : '';
        const imgs = Array.from(document.querySelectorAll('#js_content img')).map(im => im.getAttribute('data-src') || im.getAttribute('src')).filter(Boolean);
        return { title: title.trim(), nickname: nickname.trim(), ct, text: text.trim(), imgs };
      });

      info.title = meta.title;
      info.author = meta.nickname;
      info.date = tsToDate(meta.ct);
      info.text = meta.text;
      info.images = meta.imgs;

      // download images
      const slug = slugify(meta.title, i);
      const imgLocal = [];
      for (let j = 0; j < meta.imgs.length; j++) {
        const u = meta.imgs[j];
        const ext = (u.split('?')[0].split('.').pop() || 'jpg').replace(/[^a-z0-9]/gi, '').slice(0, 4) || 'jpg';
        const fname = `${slug}_img${j + 1}.${ext}`;
        const dest = path.join(IMG_DIR, fname);
        const ok = await downloadImage(u, dest, url);
        if (ok) imgLocal.push({ fname, orig: u });
      }
      info.imgLocal = imgLocal;

      // write per-article markdown
      const md = [];
      md.push(`# ${meta.title}\n`);
      md.push(`- **作者/公众号**：${meta.nickname || 'Silicon Valley Girl'}`);
      md.push(`- **发布时间**：${info.date || '未知'}`);
      md.push(`- **原文**：[${url}](${url})\n`);
      md.push(`---\n`);
      md.push(meta.text);
      md.push(`\n---\n`);
      if (imgLocal.length) {
        md.push(`## 配图\n`);
        for (const im of imgLocal) md.push(`![${im.fname}](images/${im.fname})\n`);
      }
      fs.writeFileSync(path.join(OUT_DIR, slug + '.md'), md.join('\n'), 'utf8');
      info.slug = slug;
      console.log(`[${i + 1}/9] OK  "${meta.title}"  text=${meta.text.length}chars imgs=${imgLocal.length}/${meta.imgs.length}`);
    } catch (e) {
      info.error = String(e && e.message || e);
      console.log(`[${i + 1}/9] FAIL ${url} -> ${info.error}`);
    } finally {
      await page.close().catch(() => {});
    }
    results.push(info);
  }

  await browser.close();
  fs.writeFileSync(path.join(OUT_DIR, '_results.json'), JSON.stringify(results, null, 2), 'utf8');
  console.log('DONE. files in', OUT_DIR);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
