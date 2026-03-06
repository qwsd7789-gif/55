import os,time,uuid,hmac,base64,hashlib,requests,json,mimetypes,argparse
BASE='https://openapi.liblibai.cloud'

def sign_url(uri,ak,sk):
    ts=str(int(time.time()*1000)); nonce=str(uuid.uuid4())
    raw=f"{uri}&{ts}&{nonce}".encode('utf-8')
    sig=base64.urlsafe_b64encode(hmac.new(sk.encode('utf-8'),raw,hashlib.sha1).digest()).rstrip(b'=').decode('utf-8')
    return f"{BASE}{uri}?AccessKey={ak}&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"

def post_json(uri,body,ak,sk,timeout=60):
    r=requests.post(sign_url(uri,ak,sk),json=body,headers={'Content-Type':'application/json'},timeout=timeout)
    r.raise_for_status(); return r.json()

def upload(path,ak,sk):
    name=os.path.basename(path); ext=name.split('.')[-1].lower()
    js=post_json('/api/generate/upload/signature',{'name':name[:100],'extension':ext},ak,sk)
    if js.get('code')!=0: raise RuntimeError(js)
    d=js['data']; post_url=d['postUrl']; key=d['key']
    data={'key':key,'policy':d['policy'],'x-oss-date':d['xOssDate'],'x-oss-expires':str(d['xOssExpires']),'x-oss-signature':d['xOssSignature'],'x-oss-credential':d['xOssCredential'],'x-oss-signature-version':d['xOssSignatureVersion']}
    ctype=mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path,'rb') as f:
        up=requests.post(post_url,data=data,files={'file':(name,f,ctype)},timeout=180)
    if up.status_code>=300: raise RuntimeError(up.text[:300])
    return post_url.rstrip('/')+'/'+key

def run_once(image_url,ak,sk,strength):
    gp={
      'workflowUuid':'c939f39f740942e4ad6ed173a3f38f3a',
      '40':{'class_type':'LoadImage','inputs':{'image':image_url}},
      '3':{'class_type':'KSampler','inputs':{'denoise':float(strength)}}
    }
    body={'templateUuid':'4df2efa0f18d46dc9758803e478eb51c','generateParams':gp}
    sub=post_json('/api/generate/comfyui/app',body,ak,sk)
    if sub.get('code')!=0: raise RuntimeError(json.dumps(sub,ensure_ascii=False))
    gid=sub['data']['generateUuid']
    for _ in range(180):
        st=post_json('/api/generate/comfy/status',{'generateUuid':gid},ak,sk)
        if st.get('code')!=0: raise RuntimeError(json.dumps(st,ensure_ascii=False))
        d=st.get('data',{}); gs=d.get('generateStatus')
        if gs==5: return gid,d
        if gs in (6,7): raise RuntimeError(json.dumps(d,ensure_ascii=False))
        time.sleep(4)
    raise TimeoutError('timeout')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--image-path',required=True); ap.add_argument('--ak',required=True); ap.add_argument('--sk',required=True); ap.add_argument('--strength',type=float,required=True)
    args=ap.parse_args()
    p=args.image_path
    if p.lower().endswith('.webp'):
        from PIL import Image
        png=os.path.join(os.path.dirname(p),'__tmp_liblib_input.png')
        Image.open(p).convert('RGB').save(png,'PNG'); p=png
    u=upload(p,args.ak,args.sk)
    gid,res=run_once(u,args.ak,args.sk,args.strength)
    print(json.dumps({'uploaded_image_url':u,'strength':args.strength,'generate_uuid':gid,'result':res},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
