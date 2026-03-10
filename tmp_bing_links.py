import requests,re,urllib.parse
kw='AI智能体'
q=urllib.parse.quote_plus(f'site:douyin.com/video {kw}')
u=f'https://www.bing.com/search?q={q}&count=20'
r=requests.get(u,timeout=20,headers={'User-Agent':'Mozilla/5.0'})
print(r.status_code,len(r.text))
links=[]
for m in re.finditer(r'https://www\.douyin\.com/video/\d+',r.text):
    x=m.group(0)
    if x not in links: links.append(x)
print('count',len(links))
print(links[:10])
