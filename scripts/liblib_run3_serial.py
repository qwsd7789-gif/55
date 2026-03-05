import os, time, uuid, hmac, base64, hashlib, mimetypes, json
import requests

AK = "SIwvSSToatJjrspn-iSMXg"
SK = "IEvM9TeJemisc-0pc082P-j1eXlKhAxG"
BASE = "https://openapi.liblibai.cloud"
WORKFLOW_UUID = "13ddb9b3af9f427095f141b65b76e9d6"
TEMPLATE_UUID = "4df2efa0f18d46dc9758803e478eb51c"
IMG_PATH = r"D:\xhs_exports\images\2026-03-05_16-23-09\67a7325c000000002901bce7\01.jpg"
LOAD_IMAGE_NODE = "40"
KSAMPLER_NODE = "27"

PRESETS = {
    "A": {"seed": 123456, "steps": 24, "cfg": 4.0, "denoise": 0.25},
    "B": {"seed": 123456, "steps": 30, "cfg": 5.0, "denoise": 0.45},
    "C": {"seed": -1, "steps": 40, "cfg": 6.5, "denoise": 0.72},
}

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
    ext = name.split(".")[-1].lower()
    s = post("/api/generate/upload/signature", {"name": name[:100], "extension": ext})
    if s.get("code") != 0:
        raise RuntimeError(s)
    d = s["data"]
    fields = {
        "key": d["key"], "policy": d["policy"], "x-oss-date": d["xOssDate"],
        "x-oss-expires": str(d["xOssExpires"]), "x-oss-signature": d["xOssSignature"],
        "x-oss-credential": d["xOssCredential"], "x-oss-signature-version": d["xOssSignatureVersion"],
    }
    ctype = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        up = requests.post(d["postUrl"], data=fields, files={"file": (name, f, ctype)}, timeout=120)
    if up.status_code >= 300:
        raise RuntimeError(f"upload failed {up.status_code}")
    return d["postUrl"].rstrip("/") + "/" + d["key"]

def submit(tag, preset, image_url):
    seed = preset["seed"] if preset["seed"] != -1 else int(time.time() * 1000) % 2147483647
    body = {
        "templateUuid": TEMPLATE_UUID,
        "generateParams": {
            "workflowUuid": WORKFLOW_UUID,
            LOAD_IMAGE_NODE: {"class_type": "LoadImage", "inputs": {"image": image_url}},
            KSAMPLER_NODE: {"class_type": "KSampler", "inputs": {
                "seed": int(seed), "steps": int(preset["steps"]), "cfg": float(preset["cfg"]), "denoise": float(preset["denoise"])
            }},
        },
    }
    for i in range(1, 6):
        s = post('/api/generate/comfyui/app', body)
        if s.get('code') == 0:
            return s['data']['generateUuid']
        if s.get('code') == 429:
            time.sleep(i * 3)
            continue
        raise RuntimeError(s)
    raise RuntimeError(f"{tag} submit retry exhausted")

def wait(gid):
    for _ in range(300):
        st = post('/api/generate/comfy/status', {'generateUuid': gid})
        if st.get('code') != 0:
            time.sleep(3); continue
        d = st.get('data', {})
        gs = d.get('generateStatus')
        if gs == 5:
            return d
        if gs in (6, 7):
            raise RuntimeError(d)
        time.sleep(3)
    raise TimeoutError(gid)

def main():
    print('uploading...', flush=True)
    image_url = upload_image(IMG_PATH)
    print('IMAGE_URL', image_url, flush=True)
    out = {'source': IMG_PATH, 'image_url': image_url, 'runs': {}}
    for tag in ['A', 'B', 'C']:
        p = PRESETS[tag]
        print(f'SUBMIT {tag} {p}', flush=True)
        gid = submit(tag, p, image_url)
        print(f'UUID {tag} {gid}', flush=True)
        d = wait(gid)
        urls = [x.get('imageUrl') for x in (d.get('images') or []) if x.get('imageUrl')]
        out['runs'][tag] = {'generateUuid': gid, 'preset': p, 'imageUrls': urls}
        print(f'DONE {tag} {urls}', flush=True)
    rp = os.path.join(r'C:\Users\Administrator\.openclaw\workspace\reports', f'liblib_run3_serial_{int(time.time())}.json')
    with open(rp, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print('REPORT', rp, flush=True)

if __name__ == '__main__':
    main()
