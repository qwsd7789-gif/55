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
        "key": d["key"],
        "policy": d["policy"],
        "x-oss-date": d["xOssDate"],
        "x-oss-expires": str(d["xOssExpires"]),
        "x-oss-signature": d["xOssSignature"],
        "x-oss-credential": d["xOssCredential"],
        "x-oss-signature-version": d["xOssSignatureVersion"],
    }
    ctype = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        files = {"file": (name, f, ctype)}
        up = requests.post(d["postUrl"], data=fields, files=files, timeout=120)
    if up.status_code >= 300:
        raise RuntimeError(f"upload failed: {up.status_code} {up.text[:200]}")
    return d["postUrl"].rstrip("/") + "/" + d["key"]


def submit_with_retry(body: dict, max_retry=4):
    for i in range(1, max_retry + 1):
        s = post("/api/generate/comfyui/app", body)
        if s.get("code") == 0:
            return s["data"]["generateUuid"]
        if s.get("code") == 429 and i < max_retry:
            time.sleep(4 * i)
            continue
        raise RuntimeError(s)
    raise RuntimeError("submit retry exhausted")


def run_one(tag: str, preset: dict, image_url: str):
    seed = preset["seed"] if preset["seed"] != -1 else int(time.time() * 1000) % 2147483647
    body = {
        "templateUuid": TEMPLATE_UUID,
        "generateParams": {
            "workflowUuid": WORKFLOW_UUID,
            LOAD_IMAGE_NODE: {
                "class_type": "LoadImage",
                "inputs": {"image": image_url},
            },
            KSAMPLER_NODE: {
                "class_type": "KSampler",
                "inputs": {
                    "seed": int(seed),
                    "steps": int(preset["steps"]),
                    "cfg": float(preset["cfg"]),
                    "denoise": float(preset["denoise"]),
                },
            },
        },
    }
    gid = submit_with_retry(body)

    end = time.time() + 1200
    while time.time() < end:
        st = post("/api/generate/comfy/status", {"generateUuid": gid})
        if st.get("code") != 0:
            raise RuntimeError({"tag": tag, "status": st})
        d = st.get("data", {})
        gs = d.get("generateStatus")
        if gs == 5:
            imgs = [x.get("imageUrl") for x in (d.get("images") or []) if x.get("imageUrl")]
            return {
                "tag": tag,
                "preset": preset,
                "generateUuid": gid,
                "pointsCost": d.get("pointsCost"),
                "accountBalance": d.get("accountBalance"),
                "imageUrls": imgs,
            }
        if gs in (6, 7):
            raise RuntimeError({"tag": tag, "failed": d})
        time.sleep(3)
    raise TimeoutError(f"{tag} timeout")


def main():
    image_url = upload_image(IMG_PATH)
    out = {"source": IMG_PATH, "image_url": image_url, "runs": {}}

    for tag, preset in PRESETS.items():
        r = run_one(tag, preset, image_url)
        out["runs"][tag] = r
        print(tag, r["imageUrls"])
        time.sleep(2)

    report = os.path.join(r"C:\Users\Administrator\.openclaw\workspace\reports", f"liblib_run3_{int(time.time())}.json")
    with open(report, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("REPORT", report)


if __name__ == "__main__":
    main()
