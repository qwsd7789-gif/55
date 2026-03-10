import requests, urllib.parse
kw=urllib.parse.quote('AI智能体')
urls=[
 f'https://www.iesdouyin.com/web/api/v2/search/item/?keyword={kw}&count=10&offset=0&search_source=switch_tab&type=1',
 f'https://www.iesdouyin.com/web/api/v2/search/sug/?keyword={kw}',
 f'https://www.iesdouyin.com/web/api/v2/general/search/single/?keyword={kw}',
]
for u in urls:
    try:
        r=requests.get(u,timeout=20,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.douyin.com/search/'+kw})
        print('\nURL',u,'\n',r.status_code,'len',len(r.text))
        print(r.text[:300])
    except Exception as e:
        print('ERR',u,e)
