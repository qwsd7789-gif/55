import requests,time,uuid,hmac,base64,hashlib
ak='SIwvSSToatJjrspn-iSMXg'; sk='IEvM9TeJemisc-0pc082P-j1eXlKhAxG'; BASE='https://openapi.liblibai.cloud'

def sign(uri):
    ts=str(int(time.time()*1000)); n=str(uuid.uuid4()); raw=f'{uri}&{ts}&{n}'.encode(); sig=base64.urlsafe_b64encode(hmac.new(sk.encode(),raw,hashlib.sha1).digest()).rstrip(b'=').decode(); return f'{BASE}{uri}?AccessKey={ak}&Signature={sig}&Timestamp={ts}&SignatureNonce={n}'
img='https://liblibai-airship-temp.oss-cn-beijing.aliyuncs.com/aliyun-cn-prod/3efb7888815e40bfbb54b8f1f92f5c8a.png'
cands=[
 {'extraModelJson':[{'modelId':'597c767a1c924eee8c993a539c2cfd2c','versionUuid':'c939f39f740942e4ad6ed173a3f38f3a'}]},
 {'extraModelJson':'[{"modelId":"597c767a1c924eee8c993a539c2cfd2c","versionUuid":"c939f39f740942e4ad6ed173a3f38f3a"}]'},
 {'extraModelJson':{'checkpoints':[{'modelUuid':'597c767a1c924eee8c993a539c2cfd2c','versionUuid':'c939f39f740942e4ad6ed173a3f38f3a'}]}},
]
for i,em in enumerate(cands,1):
    gp={'workflowUuid':'c939f39f740942e4ad6ed173a3f38f3a','40':{'class_type':'LoadImage','inputs':{'image':img}},'3':{'class_type':'KSampler','inputs':{'denoise':0.5}},'extraModelJson':em}
    b={'templateUuid':'4df2efa0f18d46dc9758803e478eb51c','generateParams':gp}
    r=requests.post(sign('/api/generate/comfyui/app'),json=b,timeout=60)
    try:j=r.json()
    except Exception: print(i,'nonjson',r.status_code,r.text[:120]); continue
    print(i,j.get('code'),j.get('msg'))
    time.sleep(1)
