import requests
cands=[
 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/aweme/',
 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/video/',
 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/',
 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/',
 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web',
 'https://www.douyin.com/aweme/v1/web/hot/search/video/list/?device_platform=webapp&aid=6383&channel=channel_pc_web',
 'https://www.douyin.com/aweme/v1/web/hot/search/aweme/list/?device_platform=webapp&aid=6383&channel=channel_pc_web',
]
for u in cands:
    try:
        r=requests.get(u,timeout=20,headers={'User-Agent':'Mozilla/5.0'})
        print('\n',u,'\n',r.status_code, r.text[:220])
    except Exception as e:
        print('ERR',u,e)
