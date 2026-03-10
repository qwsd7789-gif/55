import json
import re
import time
from pathlib import Path
import requests

APP_TOKEN = "NnhgbjaTlaxqGxsOvaicz73ynJh"
TABLES = {
    "关键词任务": "tblRSk6pIBFi5NLX",
    "热门视频池": "tblyCdmC2kPn3Gey",
    "改写与脚本": "tbl6iZdUHElUmcEF",
}
REQ_FIELDS = {
    "关键词任务": ["关键词", "抓取数量", "平台", "执行状态", "触发抓取", "最近执行时间", "备注"],
    "热门视频池": ["视频标题", "视频链接", "作者", "点赞数", "评论数", "转发数", "发布时间", "视频时长秒", "提取状态", "触发提取", "原始文案", "清洗文案", "关键帧", "提取日志"],
    "改写与脚本": ["关联视频", "改写风格", "目标人群", "触发改写", "生成状态", "改写文案", "拍摄脚本", "版本号", "生成日志"],
}


def extract_secret(text: str, key: str) -> str:
    m = re.search(rf'"{re.escape(key)}"\s*:\s*"([^"]+)"', text)
    return m.group(1) if m else ""


def get_token() -> str:
    raw = Path(r"C:\Users\Administrator\.openclaw\openclaw.json").read_text(encoding="utf-8", errors="ignore")
    app_id = extract_secret(raw, "appId")
    app_secret = extract_secret(raw, "appSecret")
    r = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=20,
    )
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j["tenant_access_token"]


def api_get(h, url, params=None):
    r = requests.get(url, headers=h, params=params, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j


def api_post(h, url, payload):
    r = requests.post(url, headers=h, json=payload, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j


def api_put(h, url, payload):
    r = requests.put(url, headers=h, json=payload, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j


def api_delete(h, url):
    r = requests.delete(url, headers=h, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("code") != 0:
        raise RuntimeError(j)
    return j


def list_fields(h, table_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/fields"
    return api_get(h, url, {"page_size": 500})["data"]["items"]


def run():
    h = {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json; charset=utf-8"}
    report = {"pass1_schema": {}, "pass2_crud": {}}

    # pass 1: schema
    for tname, tid in TABLES.items():
        fields = [f["field_name"] for f in list_fields(h, tid)]
        missing = [x for x in REQ_FIELDS[tname] if x not in fields]
        report["pass1_schema"][tname] = {
            "ok": len(missing) == 0,
            "missing": missing,
            "field_count": len(fields),
        }

    # pass 2: CRUD
    now_ms = int(time.time() * 1000)

    # 关键词任务
    turl = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLES['关键词任务']}/records"
    tr = api_post(h, turl, {"fields": {"关键词": "验收任务", "抓取数量": 1, "平台": "抖音", "执行状态": "待抓取", "触发抓取": False, "最近执行时间": now_ms, "备注": "schema-check"}})["data"]["record"]
    trid = tr["record_id"]
    api_put(h, f"{turl}/{trid}", {"fields": {"备注": "schema-check-updated"}})
    api_delete(h, f"{turl}/{trid}")
    report["pass2_crud"]["关键词任务"] = {"ok": True}

    # 热门视频池
    hurl = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLES['热门视频池']}/records"
    hr = api_post(h, hurl, {"fields": {"视频标题": "验收视频", "视频链接": {"text": "测试链接", "link": "https://www.douyin.com/video/000"}, "作者": "qa", "点赞数": 0, "评论数": 0, "转发数": 0, "视频时长秒": 1, "提取状态": "待提取", "触发提取": False, "原始文案": "", "清洗文案": "", "提取日志": ""}})["data"]["record"]
    hrid = hr["record_id"]
    api_put(h, f"{hurl}/{hrid}", {"fields": {"提取状态": "完成", "提取日志": "ok"}})
    api_delete(h, f"{hurl}/{hrid}")
    report["pass2_crud"]["热门视频池"] = {"ok": True}

    # 改写与脚本
    surl = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLES['改写与脚本']}/records"
    sr = api_post(h, surl, {"fields": {"改写风格": "口播", "目标人群": "新手", "触发改写": False, "生成状态": "待生成", "改写文案": "", "拍摄脚本": "", "版本号": 1, "生成日志": ""}})["data"]["record"]
    srid = sr["record_id"]
    api_put(h, f"{surl}/{srid}", {"fields": {"生成状态": "完成", "生成日志": "ok"}})
    api_delete(h, f"{surl}/{srid}")
    report["pass2_crud"]["改写与脚本"] = {"ok": True}

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
