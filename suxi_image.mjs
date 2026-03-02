import fs from 'node:fs';
import path from 'node:path';

const apiKey = process.env.SUXI_API_KEY || process.env.OPENAI_API_KEY;
const baseUrl = (process.env.OPENAI_BASE_URL || 'https://new.suxi.ai/v1').replace(/\/$/, '');
const model = process.env.SUXI_IMAGE_MODEL || 'gemini-3-pro-image-preview';

if (!apiKey) {
  console.error('Missing SUXI_API_KEY (or OPENAI_API_KEY)');
  process.exit(1);
}

const prompt = process.argv.slice(2).join(' ') || 'A simple red apple on white background';
const outDir = path.resolve('./outputs');
fs.mkdirSync(outDir, { recursive: true });
const ts = Date.now();
const outPath = path.join(outDir, `suxi-${ts}.jpg`);

async function postJson(url, body) {
  const res = await fetch(url, {
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
    throw new Error(`${res.status} ${res.statusText}\n${JSON.stringify(data, null, 2)}`);
  }
  return data;
}

function extractDataUrl(str = '') {
  // Supports markdown image: ![](data:image/jpeg;base64,xxxx)
  const m = str.match(/data:image\/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=\n\r]+)/i);
  if (!m) return null;
  return { mime: m[1].toLowerCase(), b64: m[2].replace(/[\r\n]/g, '') };
}

try {
  const data = await postJson(`${baseUrl}/chat/completions`, {
    model,
    modalities: ['text', 'image'],
    messages: [
      { role: 'user', content: prompt }
    ]
  });

  const content = data?.choices?.[0]?.message?.content || '';
  const hit = extractDataUrl(content);

  if (!hit) {
    console.log('No inline image found. Raw response snippet:');
    console.log(String(content).slice(0, 800));
    process.exit(2);
  }

  const ext = hit.mime === 'jpeg' ? 'jpg' : hit.mime;
  const finalPath = outPath.replace(/\.jpg$/, `.${ext}`);
  fs.writeFileSync(finalPath, Buffer.from(hit.b64, 'base64'));

  console.log('Model:', model);
  console.log('Image saved to:', finalPath);
  process.exit(0);
} catch (err) {
  console.error('Image generation failed:');
  console.error(String(err.message || err));
  process.exit(1);
}
