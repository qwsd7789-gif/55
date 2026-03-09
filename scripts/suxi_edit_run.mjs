import fs from 'node:fs';
import path from 'node:path';

const imgPath = String.raw`D:\xhs_exports\collected\images\2026-03-06_18-29-51\6733254c000000003c01a99e\01.jpg`;
const apiKey = process.env.SUXI_API_KEY || process.env.OPENAI_API_KEY;
const baseUrl = (process.env.OPENAI_BASE_URL || 'https://new.suxi.ai/v1').replace(/\/$/, '');
const model = process.env.SUXI_IMAGE_MODEL || 'gemini-2.5-flash-image';
const prompt = '请参考原图，提取爆款视觉元素进行重绘。保持手串主体大小、画面主体位置和核心构图关系不变，不要把手串画大或画小。整体风格为简约、艺术化、自然元素融合风格，画面更高级、更干净、更适合小红书爆款审美。保留饰品质感与细节，背景可做适度美化，但不要喧宾夺主。';

if (!apiKey) {
  console.error('Missing SUXI_API_KEY / OPENAI_API_KEY');
  process.exit(1);
}

const b64 = fs.readFileSync(imgPath).toString('base64');
const mime = 'image/jpeg';
const outDir = path.resolve('outputs');
fs.mkdirSync(outDir, { recursive: true });
const outBase = path.join(outDir, `suxi-edit-${Date.now()}`);

function extractDataUrl(str = '') {
  const m = str.match(/data:image\/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=\n\r]+)/i);
  if (!m) return null;
  return { ext: m[1].toLowerCase() === 'jpeg' ? 'jpg' : m[1].toLowerCase(), b64: m[2].replace(/[\r\n]/g, '') };
}

const body = {
  model,
  modalities: ['text', 'image'],
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: prompt },
        { type: 'image_url', image_url: { url: `data:${mime};base64,${b64}` } }
      ]
    }
  ]
};

const res = await fetch(`${baseUrl}/chat/completions`, {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(body)
});

const text = await res.text();
let data;
try { data = JSON.parse(text); } catch { data = { raw: text }; }

if (!res.ok) {
  console.error('HTTP_FAIL');
  console.error(res.status, res.statusText);
  console.error(JSON.stringify(data, null, 2));
  process.exit(1);
}

const content = data?.choices?.[0]?.message?.content || '';
const hit = typeof content === 'string' ? extractDataUrl(content) : null;
if (hit) {
  const fp = `${outBase}.${hit.ext}`;
  fs.writeFileSync(fp, Buffer.from(hit.b64, 'base64'));
  console.log(`OK_IMAGE ${fp}`);
  process.exit(0);
}

console.log('NO_INLINE_IMAGE');
console.log(JSON.stringify(data, null, 2).slice(0, 6000));
process.exit(2);
