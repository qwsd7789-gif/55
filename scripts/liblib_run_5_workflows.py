import os, time, uuid, hmac, base64, hashlib, mimetypes, json
import requests

AK = "SIwvSSToatJjrspn-iSMXg"
SK = "IEvM9TeJemisc-0pc082P-j1eXlKhAxG"
BASE = "https://openapi.liblibai.cloud"
TEMPLATE_UUID = "4df2efa0f18d46dc9758803e478eb51c"
IMG_PATH = r"D:\xhs_exports\images\2026-03-05_16-23-09\67a7325c000000002901bce7\01.jpg"

WORKFLOWS = [
    "1b9ab75c0f7b400ab90fd5415e83e278",
    "2fe0d99948cd44d2a656493daf1a82df",
    "24fc40d3b0d94bba9fa70c43da961acb",
    "192b7dc075bb483181c6dff336851f17",
    "b4eb2e484d25424ba75f70b69167d562",
]

def sign_url(uri: str) -> str:
    ts = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    raw = f"{uri}&{ts}&{nonce}".encode()
    sig = base64.urlsafe_b64encode(hmac.new(SK.encode(), raw, hashlib.sha1).digest()).rstrip(b"=").decode()
    return f"{BASE}{uri}?AccessKey={AK}&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"

def post(uri: str, body: dict) -> dict:
    r = requests.post(sign_url(uri), json=body, timeout=90)
    r.raise_for_status()
    return r.json()

def upload_image(path: str) -> str:
    name = os.path.basename(path)
    ext = name.split('.')[-1].lower()
    s = post('/api/generate/upload/signature', {'name': name[:100], 'extension': ext})
    if s.get('code') != 0:
        raise RuntimeError(s)
    d = s['data']
    fields = {
        'key': d['key'], 'policy': d['policy'], 'x-oss-date': d['xOssDate'],
        'x-oss-expires': str(d['xOssExpires']), 'x-oss-signature': d['xOssSignature'],
        'x-oss-credential': d['xOssCredential'], 'x-oss-signature-version': d['xOssSignatureVersion'],
    }
    ctype = mimetypes.guess_type(path)[0] or 'image/jpeg'
    with open(path, 'rb') as f:
        up = requests.post(d['postUrl'], data=fields, files={'file': (name, f, ctype)}, timeout=120)
    if up.status_code >= 300:
        raise RuntimeError(f"upload failed {up.status_code}")
    return d['postUrl'].rstrip('/') + '/' + d['key']

def run_one(workflow_uuid: str, image_url: str):
    body = {
        'templateUuid': TEMPLATE_UUID,
        'generateParams': {
            'workflowUuid': workflow_uuid,
            '40': {'class_type': 'LoadImage', 'inputs': {'image': image_url}},
        },
    }
    # submit retry for 429
    sub = None
    for i in range(1, 6):
        sub = post('/api/generate/comfyui/app', body)
        if sub.get('code') == 0:
            break
        if sub.get('code') == 429 and i < 5:
            time.sleep(i * 3)
            continue
        raise RuntimeError({'workflowUuid': workflow_uuid, 'submit': sub})
    gid = sub['data']['generateUuid']

    for _ in range(300):
        st = post('/api/generate/comfy/status', {'generateUuid': gid})
        if st.get('code') != 0:
            time.sleep(3)
            continue
        d = st.get('data', {})
        gs = d.get('generateStatus')
        if gs == 5:
            imgs = [x.get('imageUrl') for x in (d.get('images') or []) if x.get('imageUrl')]
            return {'workflowUuid': workflow_uuid, 'generateUuid': gid, 'imageUrls': imgs, 'pointsCost': d.get('pointsCost')}
        if gs in (6, 7):
            return {'workflowUuid': workflow_uuid, 'generateUuid': gid, 'error': d}
        time.sleep(3)
    return {'workflowUuid': workflow_uuid, 'generateUuid': gid, 'error': 'timeout'}

def main():
    image_url = upload_image(IMG_PATH)
    out = {'source': IMG_PATH, 'uploaded_image_url': image_url, 'results': []}
    print('uploaded_image_url', image_url, flush=True)

    for w in WORKFLOWS:
        print('running', w, flush=True)
        r = run_one(w, image_url)
        out['results'].append(r)
        print('done', w, r.get('imageUrls'), flush=True)

    report = os.path.join(r'C:\Users\Administrator\.openclaw\workspace\reports', f'liblib_5wf_{int(time.time())}.json')
    with open(report, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print('REPORT', report, flush=True)

if __name__ == '__main__':
    main()
