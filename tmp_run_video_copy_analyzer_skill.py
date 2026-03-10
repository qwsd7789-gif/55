import os, re, sys, requests
# ensure ffmpeg in PATH for subprocess
winget_links = r'C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Links'
os.environ['PATH'] = winget_links + os.pathsep + os.environ.get('PATH', '')
share_url = 'http://xhslink.com/o/A3kjlQeuy7P'
resolved = requests.get(share_url, allow_redirects=True, timeout=25).url
print('RESOLVED', resolved)
html = requests.get(resolved, timeout=30, headers={'User-Agent': 'Mozilla/5.0'}).text
cands = re.findall(r'https://sns-video[^"\']+\.mp4[^"\']*', html)
if not cands:
    cands = re.findall(r'https://[^"\']+\.mp4[^"\']*', html)
if not cands:
    print('NO_VIDEO_URL')
    sys.exit(2)
video_url = cands[0]
out_dir = r'C:/Users/Administrator/.openclaw/workspace/video-analysis'
os.makedirs(out_dir, exist_ok=True)
video_path = os.path.join(out_dir, 'xhs_69ad8eb400000220fcc.mp4')
srt_path = os.path.join(out_dir, 'xhs_69ad8eb400000220fcc.srt')
print('VIDEO_URL', video_url)
print('DOWNLOADING_VIDEO')
rv = requests.get(video_url, timeout=180)
rv.raise_for_status()
with open(video_path, 'wb') as f:
    f.write(rv.content)
print('VIDEO_SAVED', video_path, len(rv.content))
sys.path.insert(0, r'C:/Users/Administrator/.agents/skills/video-copy-analyzer/scripts')
from extract_subtitle_funasr import extract_with_funasr
print('RUNNING_FUNASR')
ok = extract_with_funasr(video_path, srt_path)
print('FUNASR_OK', ok)
print('SRT_PATH', srt_path)
