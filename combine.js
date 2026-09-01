const fs = require('fs');
const path = require('path');
const OUT_DIR = 'C:/Users/Administrator/WorkBuddy/2026-08-24-15-20-36/outputs/svg_articles';

const results = JSON.parse(fs.readFileSync(path.join(OUT_DIR, '_results.json'), 'utf8'));

// order files by index prefix
const files = fs.readdirSync(OUT_DIR).filter(f => /^\d+_.*\.md$/.test(f)).sort();

const toc = ['# Silicon Valley Girl 公众号文章合集（9 篇）', ''];
toc.push(`> 抓取时间：2026-08-26 ｜ 来源：晚点再听 LaterCast（公众号 Silicon Valley Girl）`);
toc.push(`> 共 ${results.length} 篇，配图 ${results.reduce((a, r) => a + (r.imgLocal ? r.imgLocal.length : 0), 0)} 张\n`);
toc.push('## 目录\n');
results.forEach((r, i) => {
  const f = files[i];
  const wc = (r.text || '').length;
  toc.push(`${i + 1}. [${r.title}](#${String(i + 1).padStart(2, '0')}-${r.title.replace(/[^\w一-龥]/g, '').slice(0, 20)})  —  ${r.date || '?'} ｜ ${wc} 字 ｜ 配图 ${(r.imgLocal || []).length} 张`);
});
toc.push('\n---\n');

let combined = toc.join('\n');

files.forEach((f, i) => {
  const body = fs.readFileSync(path.join(OUT_DIR, f), 'utf8');
  // add anchor id via a level-1 marker we can't do in plain md; use a comment + heading
  combined += `\n\n<!-- anchor ${i + 1} -->\n` + body + '\n\n---\n';
});

fs.writeFileSync(path.join(OUT_DIR, 'Silicon_Valley_Girl_合集.md'), combined, 'utf8');
console.log('Combined written:', combined.length, 'bytes;', files.length, 'articles merged.');
