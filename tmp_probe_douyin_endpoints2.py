import requests
u='https://www.douyin.com/aweme/v1/web/hot/search/video/list/?device_platform=webapp&aid=6383&channel=channel_pc_web'
r=requests.get(u,timeout=20,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.douyin.com/hot'})
print(r.status_code, len(r.content))
print(r.headers.get('content-type'))
print(r.text[:500])
