import fs from 'node:fs';
import path from 'node:path';

const htmlPath = String.raw`D:\xhs_exports\collected\html\xhs_partial_completed_like100_2026-03-06_23-47-46.html`;
const prompt = '参考这张图片的主题生成一张新的图片。保留核心主体，改变背景和构图，改变光线和色调，增加新的细节，整体视觉效果更高级，避免和原图相似，适合小红书风格，高清。';
const apiKey = process.env.SUXI_API_KEY || process.env.OPENAI_API_KEY;
const baseUrl = (process.env.OPENAI_BASE_URL || 'https://new.suxi.ai/v1').replace(/\/$/, '');
const model = process.env.SUXI_IMAGE_MODEL || 'gemini-2.5-flash-image';
if (!apiKey) throw new Error('Missing SUXI_API_KEY / OPENAI_API_KEY');

const html = fs.readFileSync(htmlPath, 'utf8');
const sections = html.match(/<section[\s\S]*?<\/section>/g) || [];
const wanted = [sections.length - 5, sections.length - 4, sections.length - 3, sections.length - 2, sections.length - 1].filter(i => i >= 0);

function decodeHtml(s='') { return s.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#39;/g, "'").replace(/&quot;/g,'"'); }
function stripTags(s='') { return decodeHtml(s.replace(/<[^>]+>/g,'')); }
function extractDataUrl(str = '') {
  const m = str.match(/data:image\/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=\n\r]+)/i);
  if (!m) return null;
  return { ext: m[1].toLowerCase() === 'jpeg' ? 'jpg' : m[1].toLowerCase(), b64: m[2].replace(/[\r\n]/g, '') };
}
async function callEdit(imagePath) {
  const b64 = fs.readFileSync(imagePath).toString('base64');
  const body = {
    model,
    modalities: ['text', 'image'],
    messages: [{ role: 'user', content: [
      { type: 'text', text: prompt },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${b64}` } }
    ] }]
  };
  const res = await fetch(`${baseUrl}/chat/completions`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const text = await res.text();
  let data; try { data = JSON.parse(text); } catch { data = { raw: text }; }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${JSON.stringify(data).slice(0,800)}`);
  const content = data?.choices?.[0]?.message?.content || '';
  const hit = typeof content === 'string' ? extractDataUrl(content) : null;
  if (!hit) throw new Error(`No inline image: ${JSON.stringify(data).slice(0,800)}`);
  return Buffer.from(hit.b64, 'base64');
}

const runId = `suxi-batch-last5-top1-theme-${Date.now()}`;
const outDir = path.resolve('outputs', runId);
fs.mkdirSync(outDir, { recursive: true });
const manifest = [];

for (const idx of wanted) {
  const sec = sections[idx] || '';
  const title = stripTags((sec.match(/<h3>([\s\S]*?)<\/h3>/) || [,''])[1]).trim();
  const imgs = [...sec.matchAll(/<img src='([^']+)'/g)].map(m => m[1].replace(/\//g, path.sep)).slice(0,1);
  const note = { noteIndex: idx + 1, title, items: [] };
  console.log(`NOTE ${idx+1}: ${title}`);
  for (let i = 0; i < imgs.length; i++) {
    const original = imgs[i];
    console.log(`  RUN ${i+1}: ${original}`);
    try {
      const outBuf = await callEdit(original);
      const outFile = path.join(outDir, `note${idx+1}-img${i+1}.png`);
      fs.writeFileSync(outFile, outBuf);
      note.items.push({ original, generated: outFile, ok: true });
    } catch (e) {
      note.items.push({ original, error: String(e.message || e), ok: false });
    }
  }
  manifest.push(note);
}

const manifestPath = path.join(outDir, 'manifest.json');
fs.writeFileSync(manifestPath, JSON.stringify({ model, prompt, sourceHtml: htmlPath, manifest }, null, 2), 'utf8');

const rows = [];
rows.push(`<!doctype html><html><head><meta charset="utf-8"><title>Suxi Batch Result Last5 Theme</title><style>body{font-family:Arial,Microsoft YaHei;padding:20px}section{border:1px solid #ddd;border-radius:12px;padding:12px;margin:12px 0} .grid{display:grid;grid-template-columns:repeat(2,minmax(320px,1fr));gap:16px;margin-top:12px}.card{border:1px solid #eee;border-radius:10px;padding:10px}.img{max-width:100%;max-height:420px;border:1px solid #ddd;border-radius:8px;background:#fafafa}.meta{font-size:13px;color:#555;word-break:break-all;margin:8px 0}</style></head><body>`);
rows.push(`<h1>Suxi 主题重绘结果（倒数5篇，每篇前1张）</h1><p><b>模型：</b>${model}</p><p><b>提示词：</b>${prompt}</p><p><b>来源：</b>${htmlPath}</p><p><b>输出目录：</b>${outDir}</p>`);
for (const note of manifest) {
  rows.push(`<section><h2>第 ${note.noteIndex} 篇：${note.title}</h2><div class="grid">`);
  note.items.forEach((it, idx) => {
    const orig = it.original.replace(/\\/g,'/');
    const gen = it.generated ? path.resolve(it.generated).replace(/\\/g,'/') : '';
    rows.push(`<div class="card"><h3>第 ${idx+1} 张</h3><div class="meta"><b>原图：</b>${orig}</div><img class="img" src="file:///${orig}" /><div class="meta"><b>生成图：</b>${gen || '失败'}</div>${it.ok ? `<img class="img" src="file:///${gen}" />` : `<pre>${String(it.error||'').replace(/</g,'&lt;')}</pre>`}</div>`);
  });
  rows.push(`</div></section>`);
}
rows.push(`</body></html>`);
const htmlOut = path.join(outDir, 'result.html');
fs.writeFileSync(htmlOut, rows.join('\n'), 'utf8');
console.log(`HTML ${htmlOut}`);
