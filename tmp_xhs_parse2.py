import re, json, requests
u='https://www.xiaohongshu.com/discovery/item/69ad8eb40000000022020fcc?app_platform=ios&app_version=9.19.4&share_from_user_hidden=true&xsec_source=app_share&type=video&xsec_token=CBfmdn91HH8Ui5xFmwvafpRcLjkjgom3bVoo1Yx8B8pHw=&author_share=1&xhsshare=CopyLink&shareRedId=ODtEQ0Y3PUs2NzUyOTgwNjY8OTpJOEs-&apptime=1773113624&share_id=4c3ee1a2b78b43278321bdfc2fc7b86e'
t=requests.get(u,timeout=30).text
state = re.findall(r'__INITIAL_STATE__\s*=\s*(\{.*?\})\s*</script>', t, re.S)[0]
obj=json.loads(state)
# print top keys
print('top keys:', list(obj.keys())[:20])
# recursively find likely note payload keys
candidates=[]
def walk(x,path=''):
    if isinstance(x,dict):
        for k,v in x.items():
            p=f'{path}.{k}' if path else k
            lk=k.lower()
            if any(s in lk for s in ['note','video','title','desc','user','author','content']):
                candidates.append(p)
            walk(v,p)
    elif isinstance(x,list):
        for i,v in enumerate(x[:5]):
            walk(v,f'{path}[{i}]')
walk(obj)
# dedup and show focused paths
seen=[]
for p in candidates:
    if p not in seen:
        seen.append(p)
print('candidate paths sample:', seen[:120])
# try locate note detail map common path
for path in ['note','notePageData','noteDetailMap','noteDetail','currentNoteId','noteId','feeds']:
    print(path, 'in json string?', path in state)
# quick regexs for title/desc around chinese snippet
for kw in ['小龙虾','自动批量创作笔记']:
    i=state.find(kw)
    print('kw',kw,'idx',i)
    if i!=-1:
        print(state[max(0,i-120):i+180])
