const fs = require('fs');
const path = require('path');
const ROOT = 'C:/Users/Administrator/WorkBuddy/2026-08-24-15-20-36/outputs/svg_articles';
const IMG_DIR = path.join(ROOT, 'images');
const OUT = path.join(ROOT, 'by_article');
fs.mkdirSync(OUT, { recursive: true });

function sanitize(s) { return (s || '').replace(/[\\/:*?"<>|\n\r]/g, '_').slice(0, 50); }

const mdFiles = fs.readdirSync(ROOT).filter(f => /^\d+_.*\.md$/.test(f)).sort();
let count = 0;

for (const mf of mdFiles) {
  const idx = mf.split('_')[0];
  const title = mf.replace(/^\d+_/, '').replace(/\.md$/, '');
  const folder = path.join(OUT, `${idx}_${sanitize(title)}`);
  const imgFolder = path.join(folder, 'images');
  fs.mkdirSync(imgFolder, { recursive: true });

  let md = fs.readFileSync(path.join(ROOT, mf), 'utf8');
  const imgRefs = [...md.matchAll(/\(images\/([^)]+)\)/g)].map(m => m[1]);
  for (const ref of imgRefs) {
    const src = path.join(IMG_DIR, ref);
    const dst = path.join(imgFolder, ref);
    if (fs.existsSync(src)) fs.copyFileSync(src, dst);
  }
  fs.writeFileSync(path.join(folder, 'article.md'), md, 'utf8');
  count++;
  console.log(`[${idx}] ${title}  ->  ${path.basename(folder)}  (images: ${imgRefs.length})`);
}

console.log('Created', count, 'self-contained article folders in', OUT);
