import os, time, uuid, hmac, base64, hashlib, mimetypes, json
import requests

AK = "SIwvSSToatJjrspn-iSMXg"
SK = "IEvM9TeJemisc-0pc082P-j1eXlKhAxG"
BASE = "https://openapi.liblibai.cloud"
WORKFLOW_UUID = "13ddb9b3af9f427095f141b65b76e9d6"
TEMPLATE_UUID = "4df2efa0f18d46dc9758803e478eb51c"
IMG_PATH = r"C:\Users\Administrator\Desktop\ScreenShot_2026-03-05_162834_848.png"

LOAD_IMAGE_NODE = "40"
KSAMPLER_NODE = "27"

PRESETS = {
    "A": {"seed": 123456, "steps": 24, "cfg": 4.0, "denoise": 0.25},
    "B": {"seed": 123456, "steps": 28, "cfg": 4.8, "denoise": 0.38},
    "C": {"seed": -1, "steps": 34, "cfg": 5.8, "denoise": 0.58},
    "D": {"seed": -1, "steps": 42, "cfg": 6.8, "denoise": 0.75},
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
    ctype = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        files = {"file": (name, f, ctype)}
        up = requests.post(d["postUrl"], data=fields, files=files, timeout=120)
    if up.status_code >= 300:
        raise RuntimeError(f"upload failed: {up.status_code} {up.text[:300]}")
    return d["postUrl"].rstrip("/") + "/" + d["key"]


def submit_variant(image_url: str, preset: dict) -> str:
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
    s = post("/api/generate/comfyui/app", body)
    if s.get("code") != 0:
        raise RuntimeError(s)
    return s["data"]["generateUuid"]


def wait_done(gid: str, timeout=900):
    end = time.time() + timeout
    while time.time() < end:
        st = post("/api/generate/comfy/status", {"generateUuid": gid})
        if st.get("code") != 0:
            raise RuntimeError(st)
        d = st.get("data", {})
        gs = d.get("generateStatus")
        if gs == 5:
            return d
        if gs in (6, 7):
            raise RuntimeError(d)
        time.sleep(4)
    raise TimeoutError(gid)


def main():
    image_url = upload_image(IMG_PATH)
    print("image_url", image_url)
    out = {"image_url": image_url, "runs": {}}
    for tag, preset in PRESETS.items():
        print(f"run {tag} ...")
        gid = submit_variant(image_url, preset)
        d = wait_done(gid)
        imgs = d.get("images") or []
        out["runs"][tag] = {
            "preset": preset,
            "generateUuid": gid,
            "pointsCost": d.get("pointsCost"),
            "accountBalance": d.get("accountBalance"),
            "imageUrls": [x.get("imageUrl") for x in imgs if x.get("imageUrl")],
        }
        print(tag, out["runs"][tag]["imageUrls"])

    p = os.path.join(r"C:\Users\Administrator\.openclaw\workspace\reports", f"liblib_abcd_{int(time.time())}.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("report", p)


if __name__ == "__main__":
    main()
