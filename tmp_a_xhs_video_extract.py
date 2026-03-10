import re, requests, json, html

url='https://www.xiaohongshu.com/discovery/item/69ad8eb40000000022020fcc?app_platform=ios&app_version=9.19.4&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CBfmdn91HH8Ui5xFmwvafpRcLjkjgom3bVoo1Yx8B8pHw=&author_share=1&xhsshare=CopyLink&shareRedId=ODtEQ0Y3PUs2NzUyOTgwNjY8OTpJOEs-&apptime=1773113624&share_id=4c3ee1a2b78b43278321bdfc2fc7b86e'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Referer':'https://www.xiaohongshu.com/'
}
resp=requests.get(url,headers=headers,timeout=30)
resp.raise_for_status()
text=resp.text

cands=[]
# generic full urls
for pat in [r'https://[^"\']+\.mp4[^"\']*', r'https://sns-video-bd\.xhscdn\.com/[^"\']+', r'https://[^"\']+video[^"\']+']:
    cands += re.findall(pat,text)

# json escaped urls
for m in re.findall(r'"(https?:\\/\\/[^"\\]+(?:mp4|m3u8)[^"\\]*)"', text):
    u=m.replace('\\/','/')
    cands.append(u)

# keys then read nearby url-like strings
for k in ['masterUrl','originVideoKey','video_info_v2','h264','h265','stream','media']:
    idx=text.find(k)
    if idx!=-1:
        seg=text[max(0,idx-4000):idx+12000]
        cands += re.findall(r'https://[^"\']+', seg)
        cands += [x.replace('\\/','/') for x in re.findall(r'https?:\\/\\/[^"\']+', seg)]

# normalize
def clean(u):
    return html.unescape(u).replace('\\u002F','/').replace('\\/','/').strip()
uniq=[]
for u in cands:
    u=clean(u)
    if u.startswith('http') and u not in uniq:
        uniq.append(u)

# prioritize likely media
ranked=[u for u in uniq if any(x in u.lower() for x in ['mp4','m3u8','video','sns-video','xhscdn'])]
print('TOTAL_URLS',len(uniq))
print('MEDIA_LIKE',len(ranked))
for u in ranked[:80]:
    print(u)
