import json
import os
import re
import subprocess
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple

import requests

APP_TOKEN = "NnhgbjaTlaxqGxsOvaicz73ynJh"
TABLE_TASK = "tblRSk6pIBFi5NLX"
TABLE_HOT = "tblyCdmC2kPn3Gey"
TABLE_SCRIPT = "tbl6iZdUHElUmcEF"
CFG_PATH = Path(r"C:\Users\Administrator\.openclaw\openclaw.json")
SKILL_SCRIPT_DIR = Path(r"C:\Users\Administrator\.agents\skills\video-copy-analyzer\scripts")
WORK_DIR = Path(r"C:\Users\Administrator\.openclaw\workspace\outputs\douyin_pipeline")
COOKIE_FILE = Path(r"C:\Users\Administrator\.openclaw\workspace\config\douyin.cookies.json")
COOKIE_TXT_FILE = Path(r"C:\Users\Administrator\.openclaw\workspace\config\douyin.cookies.txt")
COOKIE_HEADER_FILE = Path(r"C:\Users\Administrator\.openclaw\workspace\config\douyin.cookie.header.txt")
WORK_DIR.mkdir(parents=True, exist_ok=True)


def extract_secret(text: str, key: str) -> str:
    m = re.search(rf'"{re.escape(key)}"\s*:\s*"([^"]+)"', text)
    return m.group(1) if m else ""


def get_tenant_token() -> str:
    raw = CFG_PATH.read_text(encoding="utf-8", errors="ignore")
    app_id = extract_secret(raw, "appId")
    app_secret = extract_secret(raw, "appSecret")
    if not app_id or not app_secret:
        raise RuntimeError("Missing appId/appSecret")
    r = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("code") != 0:
        raise RuntimeError(data)
    return data["tenant_access_token"]


def api_get(headers, url, params=None):
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j


def api_post(headers, url, payload):
    r = requests.post(url, headers=headers, json=payload, timeout=40)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j


def api_put(headers, url, payload):
    r = requests.put(url, headers=headers, json=payload, timeout=40)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j


def list_records(headers, table_id: str):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/records/search"
    data = api_post(headers, url, {"page_size": 500})
    return data["data"]["items"]


def update_record(headers, table_id: str, record_id: str, fields: dict):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/records/{record_id}"
    return api_put(headers, url, {"fields": fields})


def create_record(headers, table_id: str, fields: dict):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/records"
    return api_post(headers, url, {"fields": fields})


def _extract_video_links(text: str) -> List[str]:
    links = []
    for m in re.finditer(r'https?://www\.douyin\.com/video/\d+', text):
        u = m.group(0)
        if u not in links:
            links.append(u)
    return links


def search_douyin_video_links(keyword: str, limit: int = 10):
    # 主路径：搜狗对 douyin 视频页索引更稳定
    q = urllib.parse.quote_plus(f"抖音 {keyword} site:douyin.com/video")
    url = f"https://www.sogou.com/web?query={q}"
    r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    links = _extract_video_links(r.text)

    # 兜底：Bing
    if len(links) < limit:
        q2 = urllib.parse.quote_plus(f"site:douyin.com/video {keyword}")
        u2 = f"https://www.bing.com/search?q={q2}&count=30"
        r2 = requests.get(u2, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if r2.ok:
            for u in _extract_video_links(r2.text):
                if u not in links:
                    links.append(u)
                if len(links) >= limit:
                    break

    return links[:limit]


def _cookie_args() -> List[str]:
    # 优先使用 Netscape cookies 文件
    if COOKIE_TXT_FILE.exists():
        return ["--cookies", str(COOKIE_TXT_FILE)]
    # 其次 header 字符串
    if COOKIE_HEADER_FILE.exists():
        return ["--add-header", f"Cookie: {COOKIE_HEADER_FILE.read_text(encoding='utf-8', errors='ignore').strip()}"]
    if COOKIE_FILE.exists():
        return ["--cookies", str(COOKIE_FILE)]
    return []

def get_video_meta(url: str):
    cmd = ["yt-dlp", *_cookie_args(), "--dump-single-json", "--no-download", url]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout)
    except Exception:
        return None


def parse_link_field(link_field) -> str:
    if isinstance(link_field, dict):
        return link_field.get("link") or ""
    if isinstance(link_field, list) and link_field:
        v = link_field[0]
        if isinstance(v, dict):
            return v.get("link") or ""
        return str(v)
    if isinstance(link_field, str):
        return link_field
    return ""


def extract_transcript(video_url: str, out_dir: Path) -> Tuple[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    video_path = out_dir / "video.mp4"
    subprocess.run(["yt-dlp", *_cookie_args(), "-o", str(video_path), video_url], check=True)

    runner = out_dir / "run_funasr.py"
    srt_path = out_dir / "video.srt"
    runner.write_text(
        "import sys\n"
        f"sys.path.insert(0, r'{SKILL_SCRIPT_DIR.as_posix()}')\n"
        "from extract_subtitle_funasr import extract_with_funasr\n"
        f"ok = extract_with_funasr(r'{video_path.as_posix()}', r'{srt_path.as_posix()}')\n"
        "print(ok)\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["Path"] = r"C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Links;" + env.get("Path", "")
    subprocess.run(["python", str(runner)], check=True, env=env)

    txt_lines = []
    for line in srt_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.isdigit() or "-->" in line:
            continue
        txt_lines.append(line)
    return "\n".join(txt_lines), video_path


def extract_keyframes(video_path: Path, out_dir: Path, max_frames: int = 6) -> List[Path]:
    frame_dir = out_dir / "frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    # 每15秒一帧，最多取 max_frames
    out_pattern = str(frame_dir / "frame_%03d.jpg")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_path), "-vf", "fps=1/15", "-q:v", "2", out_pattern
    ], check=True, capture_output=True)
    frames = sorted(frame_dir.glob("frame_*.jpg"))[:max_frames]
    return frames


def upload_file_to_feishu(headers, file_path: Path) -> str:
    with file_path.open("rb") as f:
        files = {"file": (file_path.name, f, "image/jpeg")}
        data = {
            "file_name": file_path.name,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(file_path.stat().st_size),
        }
        r = requests.post(
            "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all",
            headers={"Authorization": headers["Authorization"]},
            data=data,
            files=files,
            timeout=60,
        )
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j["data"]["file_token"]


def rewrite_copy(raw: str, style: str, audience: str):
    raw = (raw or "").strip()
    if not raw:
        return "", ""
    hook = f"给{audience or '普通用户'}的一句话：别再手工刷素材了。"
    rewrite = f"【{style or '口播'}改写】\n{hook}\n\n{raw[:1500]}"
    script = (
        "【拍摄脚本】\n"
        "镜头1（0-3s）：痛点开场，字幕‘手动找选题太慢’\n"
        "镜头2（3-12s）：展示输入关键词自动抓热门视频\n"
        "镜头3（12-25s）：展示提取文案与关键帧\n"
        "镜头4（25-40s）：展示一键改写和脚本生成\n"
        "镜头5（40-50s）：CTA：评论区回复‘模板’领取\n"
    )
    return rewrite, script


def process_tasks(headers):
    items = list_records(headers, TABLE_TASK)
    for it in items:
        rid = it["record_id"]
        f = it.get("fields", {})
        if not f.get("触发抓取"):
            continue
        keyword = str(f.get("关键词") or "").strip()
        limit = int(f.get("抓取数量") or 10)
        if not keyword:
            update_record(headers, TABLE_TASK, rid, {"执行状态": "失败", "备注": "关键词为空", "触发抓取": False})
            continue

        update_record(headers, TABLE_TASK, rid, {"执行状态": "抓取中"})
        links = search_douyin_video_links(keyword, limit)

        created = 0
        for u in links:
            meta = get_video_meta(u) or {}
            fields = {
                "视频标题": meta.get("title") or "",
                "视频链接": {"text": "打开视频", "link": u},
                "作者": (meta.get("uploader") or ""),
                "点赞数": int(meta.get("like_count") or 0),
                "评论数": int(meta.get("comment_count") or 0),
                "转发数": int(meta.get("repost_count") or 0),
                "视频时长秒": int(meta.get("duration") or 0),
                "提取状态": "待提取",
                "触发提取": False,
                "提取日志": "",
            }
            create_record(headers, TABLE_HOT, fields)
            created += 1

        update_record(headers, TABLE_TASK, rid, {
            "执行状态": "已完成" if created else "失败",
            "备注": f"抓取完成，新增{created}条",
            "触发抓取": False,
            "最近执行时间": int(datetime.now().timestamp() * 1000),
        })


def process_extract(headers):
    items = list_records(headers, TABLE_HOT)
    for it in items:
        rid = it["record_id"]
        f = it.get("fields", {})
        if not f.get("触发提取"):
            continue
        url = parse_link_field(f.get("视频链接"))
        if not url:
            update_record(headers, TABLE_HOT, rid, {"提取状态": "失败", "提取日志": "缺少视频链接", "触发提取": False})
            continue

        update_record(headers, TABLE_HOT, rid, {"提取状态": "提取中"})
        try:
            out_dir = WORK_DIR / rid
            text, video_path = extract_transcript(url, out_dir)
            frames = extract_keyframes(video_path, out_dir, max_frames=6)
            tokens = []
            for p in frames:
                try:
                    tokens.append({"file_token": upload_file_to_feishu(headers, p)})
                except Exception:
                    pass

            update_fields = {
                "原始文案": text[:20000],
                "清洗文案": text[:20000],
                "提取状态": "完成",
                "提取日志": f"文案提取完成，关键帧{len(tokens)}张",
                "触发提取": False,
            }
            if tokens:
                update_fields["关键帧"] = tokens
            update_record(headers, TABLE_HOT, rid, update_fields)
        except Exception as e:
            update_record(headers, TABLE_HOT, rid, {
                "提取状态": "失败",
                "提取日志": str(e)[:1000],
                "触发提取": False,
            })


def process_rewrite(headers):
    hot_records = {i["record_id"]: i for i in list_records(headers, TABLE_HOT)}
    items = list_records(headers, TABLE_SCRIPT)
    for it in items:
        rid = it["record_id"]
        f = it.get("fields", {})
        if not f.get("触发改写"):
            continue

        rel = f.get("关联视频") or []
        hot_id: Optional[str] = None
        if isinstance(rel, list) and rel:
            hot_id = rel[0] if isinstance(rel[0], str) else rel[0].get("record_ids", [None])[0]
        if not hot_id:
            update_record(headers, TABLE_SCRIPT, rid, {"生成状态": "失败", "生成日志": "未关联视频", "触发改写": False})
            continue

        hot = hot_records.get(hot_id, {})
        raw = (hot.get("fields", {}).get("清洗文案") or hot.get("fields", {}).get("原始文案") or "")
        style = str(f.get("改写风格") or "口播")
        audience = str(f.get("目标人群") or "")

        rewrite, script = rewrite_copy(raw, style, audience)
        if not rewrite:
            update_record(headers, TABLE_SCRIPT, rid, {"生成状态": "失败", "生成日志": "源文案为空", "触发改写": False})
            continue

        update_record(headers, TABLE_SCRIPT, rid, {
            "改写文案": rewrite[:20000],
            "拍摄脚本": script[:20000],
            "生成状态": "完成",
            "生成日志": "已生成",
            "触发改写": False,
            "版本号": int((f.get("版本号") or 0)) + 1,
        })


def main():
    token = get_tenant_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    process_tasks(headers)
    process_extract(headers)
    process_rewrite(headers)
    print("OK")


if __name__ == "__main__":
    main()
