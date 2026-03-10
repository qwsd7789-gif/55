import requests
urls=[
 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/',
 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web',
]
for u in urls:
    try:
        r=requests.get(u,timeout=20,headers={'User-Agent':'Mozilla/5.0'})
        print('URL',u)
        print('STATUS',r.status_code)
        print(r.text[:300])
    except Exception as e:
        print('ERR',u,e)
