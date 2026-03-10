import json
import re
from pathlib import Path
import requests

APP_TOKEN = "NnhgbjaTlaxqGxsOvaicz73ynJh"
OWNER_USER_ID = "ou_7cee3c56e53eac986cee208acd222a03"
CFG_PATH = Path(r"C:\Users\Administrator\.openclaw\openclaw.json")


def extract_secret(text: str, key: str) -> str:
    m = re.search(rf'"{re.escape(key)}"\s*:\s*"([^"]+)"', text)
    return m.group(1) if m else ""


def get_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    r = requests.post(url, json={"app_id": app_id, "app_secret": app_secret}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != 0:
        raise RuntimeError(f"get token failed: {data}")
    return data["tenant_access_token"]


def api_get(headers, url, params=None):
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != 0:
        raise RuntimeError(f"GET failed: {url} -> {data}")
    return data


def api_post(headers, url, payload):
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != 0:
        raise RuntimeError(f"POST failed: {url} -> {data}")
    return data


def list_tables(headers):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    data = api_get(headers, url, {"page_size": 200})
    return data["data"]["items"]


def ensure_table(headers, name: str, cache: list):
    for t in cache:
        if t.get("name") == name:
            return t["table_id"]
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables"
    data = api_post(headers, url, {"table": {"name": name}})
    tid = data["data"]["table_id"]
    cache.append({"name": name, "table_id": tid})
    return tid


def list_fields(headers, table_id: str):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/fields"
    data = api_get(headers, url, {"page_size": 500})
    return data["data"]["items"]


def ensure_field(headers, table_id: str, field_name: str, ftype: int, prop=None):
    for f in list_fields(headers, table_id):
        if f.get("field_name") == field_name:
            return f["field_id"]
    body = {"field_name": field_name, "type": ftype}
    if prop is not None:
        body["property"] = prop
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{table_id}/fields"
    data = api_post(headers, url, body)
    return data["data"]["field"]["field_id"]


def seed_task(headers, task_table_id: str):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{task_table_id}/records"
    body = {
        "fields": {
            "关键词": "AI智能体",
            "抓取数量": 20,
            "平台": "抖音",
            "执行状态": "待抓取",
            "触发抓取": False,
            "备注": "初始化样例"
        }
    }
    data = api_post(headers, url, body)
    return data["data"]["record"]["record_id"]


def try_grant_member(headers):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/permissions/{APP_TOKEN}/members"
    try:
        data = api_post(headers, url, {
            "member_type": "user",
            "member_id": OWNER_USER_ID,
            "perm": "full_access"
        })
        return {"ok": True, "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    raw = CFG_PATH.read_text(encoding="utf-8", errors="ignore")
    app_id = extract_secret(raw, "appId")
    app_secret = extract_secret(raw, "appSecret")
    if not app_id or not app_secret:
        raise RuntimeError("appId/appSecret not found in openclaw.json")

    token = get_token(app_id, app_secret)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}

    tables = list_tables(headers)
    tbl_task = ensure_table(headers, "关键词任务", tables)
    tbl_hot = ensure_table(headers, "热门视频池", tables)
    tbl_script = ensure_table(headers, "改写与脚本", tables)

    # 关键词任务
    ensure_field(headers, tbl_task, "关键词", 1)
    ensure_field(headers, tbl_task, "抓取数量", 2)
    ensure_field(headers, tbl_task, "平台", 3)
    ensure_field(headers, tbl_task, "执行状态", 3)
    ensure_field(headers, tbl_task, "触发抓取", 7)
    ensure_field(headers, tbl_task, "最近执行时间", 5)
    ensure_field(headers, tbl_task, "备注", 1)

    # 热门视频池
    ensure_field(headers, tbl_hot, "关键词任务关联", 18, {"table_id": tbl_task, "multiple": False})
    ensure_field(headers, tbl_hot, "视频标题", 1)
    ensure_field(headers, tbl_hot, "视频链接", 15)
    ensure_field(headers, tbl_hot, "作者", 1)
    ensure_field(headers, tbl_hot, "点赞数", 2)
    ensure_field(headers, tbl_hot, "评论数", 2)
    ensure_field(headers, tbl_hot, "转发数", 2)
    ensure_field(headers, tbl_hot, "发布时间", 5)
    ensure_field(headers, tbl_hot, "视频时长秒", 2)
    ensure_field(headers, tbl_hot, "提取状态", 3)
    ensure_field(headers, tbl_hot, "触发提取", 7)
    ensure_field(headers, tbl_hot, "原始文案", 1)
    ensure_field(headers, tbl_hot, "清洗文案", 1)
    ensure_field(headers, tbl_hot, "关键帧", 17)
    ensure_field(headers, tbl_hot, "提取日志", 1)

    # 改写与脚本
    ensure_field(headers, tbl_script, "关联视频", 18, {"table_id": tbl_hot, "multiple": False})
    ensure_field(headers, tbl_script, "改写风格", 3)
    ensure_field(headers, tbl_script, "目标人群", 1)
    ensure_field(headers, tbl_script, "触发改写", 7)
    ensure_field(headers, tbl_script, "生成状态", 3)
    ensure_field(headers, tbl_script, "改写文案", 1)
    ensure_field(headers, tbl_script, "拍摄脚本", 1)
    ensure_field(headers, tbl_script, "版本号", 2)
    ensure_field(headers, tbl_script, "生成日志", 1)

    seed_id = seed_task(headers, tbl_task)
    perm = try_grant_member(headers)

    print(json.dumps({
        "app_token": APP_TOKEN,
        "url": f"https://pqx6yubp7vo.feishu.cn/base/{APP_TOKEN}",
        "tables": {"task": tbl_task, "hot": tbl_hot, "script": tbl_script},
        "seed_task_record": seed_id,
        "permission": perm
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
