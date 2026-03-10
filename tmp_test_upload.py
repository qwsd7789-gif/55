import re, requests
raw=open(r'C:\Users\Administrator\.openclaw\openclaw.json','r',encoding='utf-8',errors='ignore').read()
app_id=re.search(r'"appId"\s*:\s*"([^"]+)"',raw).group(1)
app_secret=re.search(r'"appSecret"\s*:\s*"([^"]+)"',raw).group(1)

t=requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',json={'app_id':app_id,'app_secret':app_secret},timeout=20).json()['tenant_access_token']
headers={'Authorization':f'Bearer {t}'}
files={'file':('a.txt',b'hello','text/plain')}
data={'file_name':'a.txt','parent_type':'bitable_file','parent_node':'NnhgbjaTlaxqGxsOvaicz73ynJh','size':'5'}
r=requests.post('https://open.feishu.cn/open-apis/drive/v1/medias/upload_all',headers=headers,data=data,files=files,timeout=30)
print(r.status_code)
print(r.text)
