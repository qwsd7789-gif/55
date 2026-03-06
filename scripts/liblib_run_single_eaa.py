import os, time, uuid, hmac, base64, hashlib, requests, json, mimetypes, argparse

BASE='https://openapi.liblibai.cloud'


def sign_url(uri, ak, sk):
    ts=str(int(time.time()*1000))
    nonce=str(uuid.uuid4())
    raw=f"{uri}&{ts}&{nonce}".encode('utf-8')
    sig=base64.urlsafe_b64encode(hmac.new(sk.encode('utf-8'), raw, hashlib.sha1).digest()).rstrip(b'=').decode('utf-8')
    return f"{BASE}{uri}?AccessKey={ak}&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"


def post_json(uri, body, ak, sk, timeout=60):
    r=requests.post(sign_url(uri, ak, sk), json=body, headers={'Content-Type':'application/json'}, timeout=timeout)
    r.raise_for_status()
    return r.json()


def upload_local_image(path, ak, sk):
    name=os.path.basename(path)
    ext=(name.split('.')[-1] if '.' in name else 'png').lower()
    js=post_json('/api/generate/upload/signature', {'name': name[:100], 'extension': ext}, ak, sk)
    if js.get('code')!=0:
        raise RuntimeError(f"upload signature failed: {js}")
    d=js['data']
    post_url=d['postUrl']
    key=d['key']

    data={
        'key': key,
        'policy': d['policy'],
        'x-oss-date': d['xOssDate'],
        'x-oss-expires': str(d['xOssExpires']),
        'x-oss-signature': d['xOssSignature'],
        'x-oss-credential': d['xOssCredential'],
        'x-oss-signature-version': d['xOssSignatureVersion'],
    }
    ctype=mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path,'rb') as f:
        files={'file': (name, f, ctype)}
        up=requests.post(post_url, data=data, files=files, timeout=180)
    if up.status_code >= 300:
        raise RuntimeError(f"OSS upload failed: {up.status_code} {up.text[:300]}")
    return post_url.rstrip('/') + '/' + key


def submit_and_poll(image_url, ak, sk, v204=1480, v205=0.5, v206=1):
    body={
        'templateUuid':'4df2efa0f18d46dc9758803e478eb51c',
        'generateParams':{
            '203': {'class_type':'LoadImage','inputs': {'image': image_url}},
            '204': {'class_type':'easy int','inputs': {'value': int(v204)}},
            '205': {'class_type':'easy float','inputs': {'value': float(v205)}},
            '206': {'class_type':'easy int','inputs': {'value': int(v206)}},
            'workflowUuid':'eaa51cebd2124d6bb165b8aaef93342b'
        }
    }
    sub=post_json('/api/generate/comfyui/app', body, ak, sk)
    if sub.get('code')!=0:
        raise RuntimeError(f"submit failed: {json.dumps(sub, ensure_ascii=False)}")
    gid=sub['data']['generateUuid']

    deadline=time.time()+900
    while time.time()<deadline:
        st=post_json('/api/generate/comfy/status', {'generateUuid': gid}, ak, sk)
        if st.get('code')!=0:
            raise RuntimeError(f"status failed: {json.dumps(st, ensure_ascii=False)}")
        d=st.get('data',{})
        gs=d.get('generateStatus')
        if gs==5:
            return gid, d
        if gs in (6,7):
            raise RuntimeError(f"generation failed: {json.dumps(d, ensure_ascii=False)}")
        time.sleep(4)
    raise TimeoutError('poll timeout')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--image-path', required=True)
    ap.add_argument('--ak', default=os.environ.get('LIBLIB_AK'))
    ap.add_argument('--sk', default=os.environ.get('LIBLIB_SK'))
    ap.add_argument('--v204', type=int, default=1480)
    ap.add_argument('--v205', type=float, default=0.5)
    ap.add_argument('--v206', type=int, default=1)
    args=ap.parse_args()

    if not args.ak or not args.sk:
        raise SystemExit('Missing AK/SK. Provide --ak/--sk or LIBLIB_AK/LIBLIB_SK env.')
    if not os.path.exists(args.image_path):
        raise SystemExit(f'Image not found: {args.image_path}')

    image_url=upload_local_image(args.image_path, args.ak, args.sk)
    gid, result=submit_and_poll(image_url, args.ak, args.sk, args.v204, args.v205, args.v206)
    out={
        'input_image_path': args.image_path,
        'uploaded_image_url': image_url,
        'params': {'v204': args.v204, 'v205': args.v205, 'v206': args.v206},
        'generate_uuid': gid,
        'result': result,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__=='__main__':
    main()
