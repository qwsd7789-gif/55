import time, uuid, hmac, base64, hashlib, json
import requests

AK="SIwvSSToatJjrspn-iSMXg"
SK="IEvM9TeJemisc-0pc082P-j1eXlKhAxG"
BASE="https://openapi.liblibai.cloud"
TEMPLATE_UUID="4df2efa0f18d46dc9758803e478eb51c"
IMAGE_URL="https://liblibai-airship-temp.oss-cn-beijing.aliyuncs.com/aliyun-cn-prod/56122ed0ef2d4c8d9217dd7baca36744.jpg"
WORKFLOWS=[
    "24fc40d3b0d94bba9fa70c43da961acb",
    "192b7dc075bb483181c6dff336851f17",
    "b4eb2e484d25424ba75f70b69167d562",
]

def sign_url(uri):
    ts=str(int(time.time()*1000)); nonce=str(uuid.uuid4())
    raw=f"{uri}&{ts}&{nonce}".encode()
    sig=base64.urlsafe_b64encode(hmac.new(SK.encode(),raw,hashlib.sha1).digest()).rstrip(b'=').decode()
    return f"{BASE}{uri}?AccessKey={AK}&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"

def post(uri, body, retry=5):
    last=None
    for i in range(retry):
        try:
            r=requests.post(sign_url(uri),json=body,timeout=90)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last=e; time.sleep(2+i)
    raise last

def run_one(wf):
    body={"templateUuid":TEMPLATE_UUID,"generateParams":{"workflowUuid":wf,"40":{"class_type":"LoadImage","inputs":{"image":IMAGE_URL}}}}
    sub=None
    for i in range(5):
        sub=post('/api/generate/comfyui/app',body)
        if sub.get('code')==0: break
        if sub.get('code')==429: time.sleep(3*(i+1)); continue
        raise RuntimeError(sub)
    gid=sub['data']['generateUuid']
    for _ in range(300):
        st=post('/api/generate/comfy/status',{'generateUuid':gid})
        if st.get('code')!=0: time.sleep(3); continue
        d=st.get('data',{}); gs=d.get('generateStatus')
        if gs==5:
            return {'workflowUuid':wf,'generateUuid':gid,'imageUrls':[x.get('imageUrl') for x in (d.get('images') or []) if x.get('imageUrl')]}
        if gs in (6,7):
            return {'workflowUuid':wf,'generateUuid':gid,'error':d}
        time.sleep(3)
    return {'workflowUuid':wf,'generateUuid':gid,'error':'timeout'}

out=[]
for wf in WORKFLOWS:
    r=run_one(wf)
    out.append(r)
    print(json.dumps(r,ensure_ascii=False))
print('DONE')
