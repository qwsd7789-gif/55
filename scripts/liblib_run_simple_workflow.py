import os,time,uuid,hmac,base64,hashlib,requests,mimetypes,json,argparse
BASE='https://openapi.liblibai.cloud'

def sign_url(uri,ak,sk):
    ts=str(int(time.time()*1000)); nonce=str(uuid.uuid4())
    raw=f"{uri}&{ts}&{nonce}".encode('utf-8')
    sig=base64.urlsafe_b64encode(hmac.new(sk.encode('utf-8'),raw,hashlib.sha1).digest()).rstrip(b'=').decode('utf-8')
    return f"{BASE}{uri}?AccessKey={ak}&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"

def post_json(uri,body,ak,sk,timeout=60):
    r=requests.post(sign_url(uri,ak,sk),json=body,headers={'Content-Type':'application/json'},timeout=timeout)
    r.raise_for_status()
    return r.json()

def upload(path,ak,sk):
    name=os.path.basename(path); ext=name.split('.')[-1].lower()
    js=post_json('/api/generate/upload/signature',{'name':name[:100],'extension':ext},ak,sk)
    if js.get('code')!=0:
        raise RuntimeError(f"upload signature failed: {js}")
    d=js['data']
    data={
        'key':d['key'],'policy':d['policy'],'x-oss-date':d['xOssDate'],'x-oss-expires':str(d['xOssExpires']),
        'x-oss-signature':d['xOssSignature'],'x-oss-credential':d['xOssCredential'],'x-oss-signature-version':d['xOssSignatureVersion']
    }
    ctype=mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path,'rb') as f:
        up=requests.post(d['postUrl'],data=data,files={'file':(name,f,ctype)},timeout=180)
    if up.status_code>=300:
        raise RuntimeError(f"oss upload failed: {up.status_code} {up.text[:200]}")
    return d['postUrl'].rstrip('/')+'/'+d['key']

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--image-path',required=True)
    ap.add_argument('--workflow-uuid',required=True)
    ap.add_argument('--image-node',required=True)
    ap.add_argument('--ak',required=True)
    ap.add_argument('--sk',required=True)
    args=ap.parse_args()

    image_url=upload(args.image_path,args.ak,args.sk)
    body={
      'templateUuid':'4df2efa0f18d46dc9758803e478eb51c',
      'generateParams':{
        str(args.image_node):{'class_type':'LoadImage','inputs':{'image':image_url}},
        'workflowUuid':args.workflow_uuid
      }
    }
    sub=post_json('/api/generate/comfyui/app',body,args.ak,args.sk)
    if sub.get('code')!=0:
      raise RuntimeError(f"submit failed: {json.dumps(sub,ensure_ascii=False)}")
    gid=sub['data']['generateUuid']

    deadline=time.time()+600
    while time.time()<deadline:
      st=post_json('/api/generate/comfy/status',{'generateUuid':gid},args.ak,args.sk)
      if st.get('code')!=0:
        raise RuntimeError(f"status failed: {json.dumps(st,ensure_ascii=False)}")
      d=st.get('data',{})
      gs=d.get('generateStatus')
      if gs==5:
        print(json.dumps({'uploaded_image_url':image_url,'generate_uuid':gid,'result':d},ensure_ascii=False,indent=2)); return
      if gs in (6,7):
        raise RuntimeError(f"generation failed: {json.dumps(d,ensure_ascii=False)}")
      time.sleep(4)
    raise TimeoutError('poll timeout')

if __name__=='__main__':
    main()
