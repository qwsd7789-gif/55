import time, uuid, hmac, base64, hashlib, json, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

AK='SIwvSSToatJjrspn-iSMXg'
SK='IEvM9TeJemisc-0pc082P-j1eXlKhAxG'
BASE='https://openapi.liblibai.cloud'
TEMPLATE_UUID='4df2efa0f18d46dc9758803e478eb51c'
IMAGE_URL='https://liblibai-airship-temp.oss-cn-beijing.aliyuncs.com/aliyun-cn-prod/56122ed0ef2d4c8d9217dd7baca36744.jpg'
WORKFLOWS=[
 '1b9ab75c0f7b400ab90fd5415e83e278',
 '2fe0d99948cd44d2a656493daf1a82df',
 '24fc40d3b0d94bba9fa70c43da961acb',
 '192b7dc075bb483181c6dff336851f17',
 'b4eb2e484d25424ba75f70b69167d562',
]

sess=requests.Session()
retry=Retry(total=5,connect=5,read=5,backoff_factor=1,status_forcelist=[429,500,502,503,504],allowed_methods=["POST"])
sess.mount('https://',HTTPAdapter(max_retries=retry))

def sign_url(uri):
    ts=str(int(time.time()*1000)); nonce=str(uuid.uuid4())
    raw=f"{uri}&{ts}&{nonce}".encode()
    sig=base64.urlsafe_b64encode(hmac.new(SK.encode(),raw,hashlib.sha1).digest()).rstrip(b'=').decode()
    return f"{BASE}{uri}?AccessKey={AK}&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"

def post(uri,body):
    r=sess.post(sign_url(uri),json=body,timeout=90)
    r.raise_for_status()
    return r.json()

def run_one(wf):
    body={'templateUuid':TEMPLATE_UUID,'generateParams':{'workflowUuid':wf,'40':{'class_type':'LoadImage','inputs':{'image':IMAGE_URL}}}}
    for i in range(1,7):
        s=post('/api/generate/comfyui/app',body)
        if s.get('code')==0:
            gid=s['data']['generateUuid']; break
        if s.get('code')==429:
            time.sleep(i*3); continue
        return {'workflowUuid':wf,'error':'submit','raw':s}
    else:
        return {'workflowUuid':wf,'error':'submit_retry_exhausted'}

    for _ in range(360):
        st=post('/api/generate/comfy/status',{'generateUuid':gid})
        if st.get('code')!=0:
            time.sleep(3); continue
        d=st.get('data',{}); gs=d.get('generateStatus')
        if gs==5:
            return {'workflowUuid':wf,'generateUuid':gid,'imageUrls':[x.get('imageUrl') for x in (d.get('images') or []) if x.get('imageUrl')], 'pointsCost':d.get('pointsCost')}
        if gs in (6,7):
            return {'workflowUuid':wf,'generateUuid':gid,'error':'failed','raw':d}
        time.sleep(3)
    return {'workflowUuid':wf,'generateUuid':gid,'error':'timeout'}

res=[]
for wf in WORKFLOWS:
    try:
        r=run_one(wf)
    except Exception as e:
        r={'workflowUuid':wf,'error':'exception','msg':str(e)}
    res.append(r)
    print(json.dumps(r,ensure_ascii=False), flush=True)

print('FINAL', json.dumps(res,ensure_ascii=False))
