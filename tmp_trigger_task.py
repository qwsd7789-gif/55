import re,requests
APP='NnhgbjaTlaxqGxsOvaicz73ynJh'; TBL='tblRSk6pIBFi5NLX'
raw=open(r'C:\Users\Administrator\.openclaw\openclaw.json','r',encoding='utf-8',errors='ignore').read()
app_id=re.search(r'"appId"\s*:\s*"([^"]+)"',raw).group(1)
app_secret=re.search(r'"appSecret"\s*:\s*"([^"]+)"',raw).group(1)
t=requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',json={'app_id':app_id,'app_secret':app_secret},timeout=20).json()['tenant_access_token']
h={'Authorization':f'Bearer {t}','Content-Type':'application/json; charset=utf-8'}
rs=requests.post(f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records/search',headers=h,json={'page_size':10},timeout=30).json()['data']['items']
rid=rs[0]['record_id']
requests.put(f'https://open.feishu.cn/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records/{rid}',headers=h,json={'fields':{'触发抓取':True,'执行状态':'待抓取'}},timeout=30).raise_for_status()
print(rid)
