import requests, os
from faster_whisper import WhisperModel
video_url='https://sns-video-qc.xhscdn.com/stream/1/110/258/01e9ad8eb42c2c2d010370019ccdf65a7a_258.mp4?sign=32091cb38371770142401f55053e7346&t=69b431d6'
video_path='C:/Users/Administrator/.openclaw/workspace/tmp_xhs_video.mp4'
out_txt='C:/Users/Administrator/.openclaw/workspace/tmp_xhs_transcript.txt'
print('downloading...')
r=requests.get(video_url,timeout=60)
r.raise_for_status()
with open(video_path,'wb') as f:
    f.write(r.content)
print('video bytes',len(r.content))
print('loading model...')
model=WhisperModel('small', device='cpu', compute_type='int8')
print('transcribing...')
segments, info = model.transcribe(video_path, vad_filter=True, language='zh')
lines=[]
for seg in segments:
    lines.append(f"[{seg.start:.2f}-{seg.end:.2f}] {seg.text.strip()}")
text='\n'.join(lines)
with open(out_txt,'w',encoding='utf-8') as f:
    f.write(text)
print('lang',info.language,'prob',info.language_probability)
print('segments',len(lines))
print(text[:180])
