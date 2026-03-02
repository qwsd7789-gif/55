import fs from 'node:fs';
import path from 'node:path';

const apiKey = process.env.GOOGLE_API_KEY;
if (!apiKey) {
  console.error('Missing GOOGLE_API_KEY');
  process.exit(1);
}

const prompt = process.argv.slice(2).join(' ') || 'A cinematic night city skyline in rain, neon reflections, ultra detailed';
const outDir = path.resolve('./outputs');
fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, `gemini-${Date.now()}.png`);

const model = 'gemini-2.0-flash-exp-image-generation';
const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

const body = {
  contents: [
    {
      parts: [{ text: prompt }]
    }
  ],
  generationConfig: {
    responseModalities: ['TEXT', 'IMAGE']
  }
};

const res = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body)
});

if (!res.ok) {
  const text = await res.text();
  console.error(`Request failed: ${res.status} ${res.statusText}`);
  console.error(text);
  process.exit(1);
}

const data = await res.json();
const parts = data?.candidates?.[0]?.content?.parts || [];
const imagePart = parts.find(p => p.inlineData?.mimeType?.startsWith('image/'));

if (!imagePart?.inlineData?.data) {
  console.error('No image returned. Full response:');
  console.error(JSON.stringify(data, null, 2));
  process.exit(1);
}

const buffer = Buffer.from(imagePart.inlineData.data, 'base64');
fs.writeFileSync(outPath, buffer);

const textPart = parts.find(p => typeof p.text === 'string');
if (textPart?.text) {
  console.log('Model text:', textPart.text);
}
console.log('Image saved to:', outPath);
