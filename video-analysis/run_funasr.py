import sys
sys.path.insert(0, r'C:\Users\Administrator\.agents\skills\video-copy-analyzer\scripts')
from extract_subtitle_funasr import extract_with_funasr
video = r'C:\Users\Administrator\.openclaw\workspace\video-analysis\69ad8eb40000000022020fcc.mp4'
out = r'C:\Users\Administrator\.openclaw\workspace\video-analysis\69ad8eb40000000022020fcc.srt'
ok = extract_with_funasr(video, out)
print('SUCCESS=', ok)
