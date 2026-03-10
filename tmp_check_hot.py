import re,requests,json
APP='NnhgbjaTlaxqGxsOvaicz73ynJh'; TBL='tblyCdmC2kPn3Gey'
raw=open(r'C:\Users\Administrator\.openclaw\openclaw.json','r',encoding='utf-8',errors='ignore').read()
app_id=re.search(r'"appId"\s*:\s*"([^"]+)"',raw).group(1)
app_secret=re.search(r'"appSecret"\s*:\s*"([^"]+)"',raw).group(1)
t=requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',json={'app_id':app_id,'app_secret':app_secret},timeout=20).json()['tenant_access_token']
h={'Authorization':f'Bearer {t}','Content-Type':'application/json; charset=utf-8'}
rs=requests.post(f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records/search',headers=h,json={'page_size':5},timeout=30).json()['data']['items']
print(len(rs))
for r in rs[:3]:
    f=r['fields']
    print(r['record_id'], f.get('视频标题','')[:40], f.get('提取状态'))
