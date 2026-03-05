import os, time, uuid, hmac, base64, hashlib, requests, json, mimetypes
AK='SIwvSSToatJjrspn-iSMXg'
SK='IEvM9TeJemisc-0pc082P-j1eXlKhAxG'
BASE='https://openapi.liblibai.cloud'
img=r'C:\Users\Administrator\Desktop\ScreenShot_2026-03-05_162834_848.png'

def sign(uri):
    ts=str(int(time.time()*1000)); nonce=str(uuid.uuid4())
    raw=f"{uri}&{ts}&{nonce}".encode()
    sig=base64.urlsafe_b64encode(hmac.new(SK.encode(),raw,hashlib.sha1).digest()).rstrip(b'=').decode()
    return f"{BASE}{uri}?AccessKey={AK}&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"

uri='/api/generate/upload/signature'
name=os.path.basename(img)
ext=name.split('.')[-1].lower()
resp=requests.post(sign(uri),json={'name':name[:100],'extension':ext},timeout=60)
print('upload-sign status',resp.status_code)
print(resp.text[:500])
resp.raise_for_status(); js=resp.json(); assert js.get('code')==0, js
u=js['data']
post_url=u['postUrl']; key=u['key']

data={
 'key':key,
 'policy':u['policy'],
 'x-oss-date':u['xOssDate'],
 'x-oss-expires':str(u['xOssExpires']),
 'x-oss-signature':u['xOssSignature'],
 'x-oss-credential':u['xOssCredential'],
 'x-oss-signature-version':u['xOssSignatureVersion'],
}
ctype=mimetypes.guess_type(img)[0] or 'image/png'
with open(img,'rb') as f:
    files={'file':(os.path.basename(img),f,ctype)}
    up=requests.post(post_url,data=data,files=files,timeout=120)
print('oss upload status',up.status_code)
print(up.text[:300])
if up.status_code>=300:
    raise SystemExit('upload failed')
image_url=post_url.rstrip('/')+'/'+key
print('image_url',image_url)

uri='/api/generate/comfyui/app'
body={
 'templateUuid':'4df2efa0f18d46dc9758803e478eb51c',
 'generateParams':{
   'workflowUuid':'13ddb9b3af9f427095f141b65b76e9d6',
   '40':{'class_type':'LoadImage','inputs':{'image':image_url}}
 }
}
sub=requests.post(sign(uri),json=body,timeout=60)
print('submit status',sub.status_code)
print(sub.text[:1200])
sub.raise_for_status(); sj=sub.json();
print('submit json code',sj.get('code'))
if sj.get('code')!=0:
    raise SystemExit('submit failed')
gid=sj['data']['generateUuid']
print('generateUuid',gid)

uri='/api/generate/comfy/status'
for i in range(60):
    st=requests.post(sign(uri),json={'generateUuid':gid},timeout=60)
    js=st.json()
    d=js.get('data',{})
    print('poll',i,'code',js.get('code'),'status',d.get('generateStatus'))
    if js.get('code')!=0:
        print(js); break
    if d.get('generateStatus')==5:
        print(json.dumps(d,ensure_ascii=False)[:4000]); break
    if d.get('generateStatus') in (6,7):
        print(json.dumps(d,ensure_ascii=False)[:4000]); break
    time.sleep(4)
