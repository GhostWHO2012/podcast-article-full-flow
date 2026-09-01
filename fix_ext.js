const fs = require('fs');
const path = require('path');
const IMG_DIR = 'C:/Users/Administrator/WorkBuddy/2026-08-24-15-20-36/outputs/svg_articles/images';
const OUT_DIR = 'C:/Users/Administrator/WorkBuddy/2026-08-24-15-20-36/outputs/svg_articles';

function extOf(buf) {
  if (buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47) return 'png';
  if (buf[0] === 0xff && buf[1] === 0xd8 && buf[2] === 0xff) return 'jpg';
  if (buf[0] === 0x52 && buf[1] === 0x49 && buf[2] === 0x46 && buf[3] === 0x46) return 'webp';
  if (buf[0] === 0x47 && buf[1] === 0x49 && buf[2] === 0x46) return 'gif';
  return null;
}

const files = fs.readdirSync(IMG_DIR).filter(f => /\.(cnsz|cnmm|jpg|jpeg|png|webp|gif)$/i.test(f));
let fixed = 0;
const renameMap = {};
for (const f of files) {
  const buf = fs.readFileSync(path.join(IMG_DIR, f));
  const ext = extOf(buf);
  if (!ext) continue;
  const curExt = f.split('.').pop().toLowerCase();
  if (curExt === ext) continue;
  const newName = f.replace(/\.[^.]+$/, '.' + ext);
  if (fs.existsSync(path.join(IMG_DIR, newName))) continue;
  fs.renameSync(path.join(IMG_DIR, f), path.join(IMG_DIR, newName));
  renameMap[f] = newName;
  fixed++;
}

// update references in all .md files
if (Object.keys(renameMap).length) {
  const mds = fs.readdirSync(OUT_DIR).filter(f => f.endsWith('.md'));
  for (const m of mds) {
    const p = path.join(OUT_DIR, m);
    let txt = fs.readFileSync(p, 'utf8');
    let changed = false;
    for (const [oldN, newN] of Object.entries(renameMap)) {
      if (txt.includes(oldN)) { txt = txt.split(oldN).join(newN); changed = true; }
    }
    if (changed) fs.writeFileSync(p, txt, 'utf8');
  }
}
console.log('Renamed', fixed, 'images:', JSON.stringify(renameMap, null, 2));
console.log('Remaining non-standard ext:', fs.readdirSync(IMG_DIR).filter(f => !/\.(png|jpg|jpeg|webp|gif)$/i.test(f)));
