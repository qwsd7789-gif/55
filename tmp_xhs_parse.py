import re, requests
u='https://www.xiaohongshu.com/discovery/item/69ad8eb40000000022020fcc?app_platform=ios&app_version=9.19.4&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CBfmdn91HH8Ui5xFmwvafpRcLjkjgom3bVoo1Yx8B8pHw=&author_share=1&xhsshare=CopyLink&shareRedId=ODtEQ0Y3PUs2NzUyOTgwNjY8OTpJOEs-&apptime=1773113624&share_id=4c3ee1a2b78b43278321bdfc2fc7b86e'
t=requests.get(u,timeout=30).text
print('len',len(t))
for k in ['小龙虾','自动批量创作笔记','noteId','title','desc','video','transcript','subtitle','creator']:
    print(k, t.find(k))
print('og:title', re.findall(r'<meta property="og:title" content="(.*?)"',t)[:1])
print('og:desc', re.findall(r'<meta property="og:description" content="(.*?)"',t)[:1])
state = re.findall(r'__INITIAL_STATE__\s*=\s*(\{.*?\})\s*</script>', t, re.S)
print('state matches', len(state))
if state:
    print('state head', state[0][:300])
