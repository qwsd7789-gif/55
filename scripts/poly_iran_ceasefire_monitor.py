#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "https://gamma-api.polymarket.com"
TZ8 = timezone(timedelta(hours=8))
ROOT = Path(r"C:\Users\Administrator\.openclaw\workspace")
STATE_PATH = ROOT / "memory" / "poly_iran_ceasefire_state.json"
REPORT_DIR = ROOT / "reports" / "poly_iran_ceasefire"

TARGETS = [
    {
        "slug": "us-x-iran-ceasefire-by-march-31",
        "label": "US x Iran ceasefire by March 31?",
        "deadline_hint": "2026-03-31 23:59 ET",
    },
    {
        "slug": "us-x-iran-ceasefire-by-april-15-182",
        "label": "US x Iran ceasefire by April 15?",
        "deadline_hint": "2026-04-15",
    },
    {
        "slug": "us-x-iran-ceasefire-by-april-30-194",
        "label": "US x Iran ceasefire by April 30?",
        "deadline_hint": "2026-04-30 23:59 ET",
    },
    {
        "slug": "trump-announces-end-of-military-operations-against-iran-by-march-31st",
        "label": "Trump announces end of military operations against Iran by March 31st?",
        "deadline_hint": "2026-03-31 23:55 UTC",
    },
]


def fetch_market(slug: str):
    url = BASE + "/markets?" + urllib.parse.urlencode({"slug": slug})
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; poly-iran-monitor/1.0)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data[0] if data else None


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"history": {}}
    return {"history": {}}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def pct(value):
    return None if value is None else round(float(value) * 100, 2)


def main():
    now = datetime.now(TZ8)
    state = load_state()
    history = state.setdefault("history", {})
    rows = []

    for target in TARGETS:
        market = fetch_market(target["slug"])
        if not market:
            continue

        try:
            prices = json.loads(market.get("outcomePrices", "[]"))
        except Exception:
            prices = []

        yes = float(prices[0]) if len(prices) > 0 else None
        no = float(prices[1]) if len(prices) > 1 else None
        liq = float(market.get("liquidityNum") or 0)
        vol = float(market.get("volumeNum") or 0)
        vol24 = float(market.get("volume24hr") or 0)

        prev = history.get(target["slug"], {})
        prev_yes = prev.get("yes_prob")
        delta_pp = None if prev_yes is None or yes is None else round((yes - prev_yes) * 100, 2)

        row = {
            "slug": target["slug"],
            "label": target["label"],
            "question": market.get("question") or target["label"],
            "yes_prob": yes,
            "no_prob": no,
            "yes_pct": pct(yes),
            "no_pct": pct(no),
            "delta_pp_vs_last": delta_pp,
            "liquidity": round(liq, 2),
            "volume": round(vol, 2),
            "volume24h": round(vol24, 2),
            "endDate": market.get("endDate"),
            "deadline_hint": target["deadline_hint"],
            "url": f"https://polymarket.com/event/{target['slug']}",
        }
        rows.append(row)

        history[target["slug"]] = {
            "ts": now.isoformat(),
            "yes_prob": yes,
            "no_prob": no,
            "liquidity": liq,
            "volume": vol,
            "volume24h": vol24,
        }

    rows.sort(key=lambda x: x["liquidity"], reverse=True)
    save_state(state)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y%m%d-%H%M")
    out = REPORT_DIR / f"{stamp}.md"

    lines = []
    lines.append("# 伊朗停战盘口监控")
    lines.append("")
    lines.append(f"- 时间: {now.strftime('%Y-%m-%d %H:%M:%S %z')}")
    lines.append(f"- 监控盘口数: {len(rows)}")
    lines.append("")
    lines.append("## 概率变化（按 TVL 排序）")

    for i, row in enumerate(rows, 1):
        if row["delta_pp_vs_last"] is None:
            delta = "首次记录"
        else:
            delta = f"{row['delta_pp_vs_last']:+.2f}pp"
        deadline = row["endDate"] or row["deadline_hint"] or "-"
        yes_pct = row["yes_pct"] if row["yes_pct"] is not None else 0.0
        lines.append(f"{i}. {row['question']}")
        lines.append(f"   - 停战/事件概率(Yes): {yes_pct:.2f}%")
        lines.append(f"   - 较上次变化: {delta}")
        lines.append(f"   - TVL/Liquidity: ${row['liquidity']:,.2f}")
        lines.append(f"   - 累计成交额: ${row['volume']:,.2f}")
        lines.append(f"   - 24h 成交额: ${row['volume24h']:,.2f}")
        lines.append(f"   - 到期/判定时间: {deadline}")
        lines.append(f"   - 链接: {row['url']}")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "report": str(out),
                "generated_at": now.isoformat(),
                "items": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
