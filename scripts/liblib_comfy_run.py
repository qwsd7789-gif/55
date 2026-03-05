import argparse
import base64
import hashlib
import hmac
import json
import time
import uuid
from typing import Dict, Any

import requests

BASE_URL = "https://openapi.liblibai.cloud"
DEFAULT_TEMPLATE_UUID = "4df2efa0f18d46dc9758803e478eb51c"


def make_signature(uri: str, secret_key: str, timestamp: str, nonce: str) -> str:
    raw = f"{uri}&{timestamp}&{nonce}".encode("utf-8")
    digest = hmac.new(secret_key.encode("utf-8"), raw, hashlib.sha1).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")


def signed_url(uri: str, access_key: str, secret_key: str) -> str:
    ts = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    sig = make_signature(uri, secret_key, ts, nonce)
    return (
        f"{BASE_URL}{uri}?AccessKey={access_key}"
        f"&Signature={sig}&Timestamp={ts}&SignatureNonce={nonce}"
    )


def post_json(uri: str, body: Dict[str, Any], access_key: str, secret_key: str) -> Dict[str, Any]:
    url = signed_url(uri, access_key, secret_key)
    resp = requests.post(url, json=body, headers={"Content-Type": "application/json"}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def submit_comfy(
    access_key: str,
    secret_key: str,
    workflow_uuid: str,
    image_url: str,
    width: int | None,
    height: int | None,
) -> str:
    # 你的工作流来自链接：comfyOrid=13ddb9b3af9f427095f141b65b76e9d6
    # 下面节点ID基于你提供的本地工作流JSON：LoadImage(40)
    generate_params: Dict[str, Any] = {
        "workflowUuid": workflow_uuid,
        "40": {
            "class_type": "LoadImage",
            "inputs": {
                "image": image_url
            }
        },
    }

    # 如果你确认线上API参数里有对应缩放节点，可启用这段（需与线上节点ID一致）
    if width and height:
        generate_params["54"] = {
            "class_type": "LayerUtility: ImageScaleByAspectRatio V2",
            "inputs": {
                "scale_to_length": max(width, height)
            }
        }

    body = {
        "templateUuid": DEFAULT_TEMPLATE_UUID,
        "generateParams": generate_params,
    }

    data = post_json("/api/generate/comfyui/app", body, access_key, secret_key)
    if data.get("code") != 0:
        raise RuntimeError(f"submit failed: {data}")
    return data["data"]["generateUuid"]


def poll_status(access_key: str, secret_key: str, generate_uuid: str, interval: int = 4, timeout: int = 600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = post_json("/api/generate/comfy/status", {"generateUuid": generate_uuid}, access_key, secret_key)
        if data.get("code") != 0:
            raise RuntimeError(f"status failed: {data}")
        d = data.get("data", {})
        status = d.get("generateStatus")
        if status == 5:
            return d
        if status in (6, 7):
            raise RuntimeError(f"generate failed: {d}")
        time.sleep(interval)
    raise TimeoutError("poll timeout")


def main():
    ap = argparse.ArgumentParser(description="Run Liblib Comfy workflow")
    ap.add_argument("--access-key", required=True)
    ap.add_argument("--secret-key", required=True)
    ap.add_argument("--workflow-uuid", default="13ddb9b3af9f427095f141b65b76e9d6")
    ap.add_argument("--image-url", required=True, help="公网可访问图片URL")
    ap.add_argument("--width", type=int, default=None)
    ap.add_argument("--height", type=int, default=None)
    args = ap.parse_args()

    gen_uuid = submit_comfy(
        access_key=args.access_key,
        secret_key=args.secret_key,
        workflow_uuid=args.workflow_uuid,
        image_url=args.image_url,
        width=args.width,
        height=args.height,
    )
    print(f"generateUuid={gen_uuid}")

    result = poll_status(args.access_key, args.secret_key, gen_uuid)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
