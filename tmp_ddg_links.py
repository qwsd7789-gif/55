import urllib.parse,re,requests
kw='AI智能体'
q=urllib.parse.quote_plus(f'site:douyin.com/video {kw}')
u=f'https://duckgo.com/html/?q={q}'
h={'User-Agent':'Mozilla/5.0'}
t=requests.get(u,headers=h,timeout=20).text
ls=[]
for m in re.finditer(r'href="//duckgo.com/l/\?uddg=([^"]+)"',t):
    x=urllib.parse.unquote(m.group(1))
    if 'douyin.com/video/' in x:
        x=x.split('&')[0]
        if x not in ls: ls.append(x)
print('count',len(ls))
print(ls[:10])
