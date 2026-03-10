import requests,urllib.parse,re
kw='AI智能体'
url='https://www.douyin.com/search/'+urllib.parse.quote(kw)+'?type=video'
r=requests.get(url,timeout=20,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.douyin.com/'})
print(r.status_code,len(r.text))
print(r.text[:500])
ids=re.findall(r'/video/(\d+)',r.text)
print('ids',len(set(ids)),list(dict.fromkeys(ids))[:10])
