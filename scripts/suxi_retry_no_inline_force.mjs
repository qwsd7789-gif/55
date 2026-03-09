import fs from 'node:fs';
import path from 'node:path';

const jobs = [
  {
    noteIndex: 2,
    title: '2. 水晶店主的理货Plog17 | 美到谁了我不说✨',
    imagePath: String.raw`D:\xhs_exports\collected\images\2026-03-06_18-29-51\6733254c000000003c01a99e\01.jpg`
  },
  {
    noteIndex: 4,
    title: '4. 喜金💰人的本命手串',
    imagePath: String.raw`D:\xhs_exports\collected\images\2026-03-06_18-29-51\676cea79000000001300c3ce\01.jpg`
  }
];

const prompt = '参考这张图片的主题，重新生成一张新的图片。要求：保留核心元素，改变背景、光线，不要和原图一样。重要：不要输出任何解释文字、不要输出说明、不要输出markdown，只返回最终生成的图片结果。';
const apiKey = process.env.SUXI_API_KEY || process.env.OPENAI_API_KEY;
const baseUrl = (process.env.OPENAI_BASE_URL || 'https://new.suxi.ai/v1').replace(/\/$/, '');
const model = process.env.SUXI_IMAGE_MODEL || 'gemini-2.5-flash-image';
if (!apiKey) throw new Error('Missing SUXI_API_KEY / OPENAI_API_KEY');

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
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${JSON.stringify(data).slice(0,1000)}`);
  const content = data?.choices?.[0]?.message?.content || '';
  const hit = typeof content === 'string' ? extractDataUrl(content) : null;
  if (!hit) throw new Error(`No inline image: ${JSON.stringify(data).slice(0,1000)}`);
  return Buffer.from(hit.b64, 'base64');
}

const runId = `suxi-retry-force-image-${Date.now()}`;
const outDir = path.resolve('outputs', runId);
fs.mkdirSync(outDir, { recursive: true });
const manifest = [];
for (const job of jobs) {
  try {
    const outBuf = await callEdit(job.imagePath);
    const outFile = path.join(outDir, `note${job.noteIndex}-img1.png`);
    fs.writeFileSync(outFile, outBuf);
    manifest.push({ ...job, generated: outFile, ok: true });
  } catch (e) {
    manifest.push({ ...job, error: String(e.message || e), ok: false });
  }
}
fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({ model, prompt, manifest }, null, 2), 'utf8');
console.log(`OUT ${outDir}`);
