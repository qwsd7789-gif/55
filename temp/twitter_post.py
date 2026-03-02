#!/usr/bin/env python3
"""
Twitter 发帖脚本
需要先配置 Twitter API Bearer Token
"""

import os
import sys

# Windows 编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 推文内容（已整理）
tweets = [
    {
        "text": """🔥 中东局势升级 | Iran-Israel Conflict Escalates

📍 最新动态：
• 伊朗报复性袭击进入第3天，卡塔尔/阿联酋/科威特发生爆炸
• 以色列誓言加大对德黑兰打击力度  
• 德黑兰正遭受新一轮空袭
• 真主党向以色列发射火箭弹，以军轰炸贝鲁特

🛢️ 市场影响：原油+6% | 💰 BTC跌破$66K

#Iran #Israel #MiddleEast #Oil #Bitcoin"""
    },
    {
        "text": """📊 冲突对市场的影响 | Market Impact

🛢️ 原油：WTI/Brent飙升6%，供应担忧加剧
🟡 黄金：避险需求上升，关注$2,100突破  
💰 数字货币：BTC跌破$66,000，ETH跟跌
📉 美股期货：早盘下跌，VIX波动率上升

⚠️ 风险提示：若海湾国家卷入战争，油价可能冲击$100

#Oil #Gold #Bitcoin #StockMarket #Trading"""
    },
    {
        "text": """🧵 为什么这次不一样？

1️⃣ 范围扩大：从伊朗-以色列双边冲突扩展至海湾国家
2️⃣ 美国卷入：首批美军士兵死亡，国内政治压力增大
3️⃣ 供应风险：霍尔木兹海峡运输风险上升
4️⃣ 连锁反应：真主党、胡塞武装等多方卷入

📊 民调：仅25%美国人支持对伊朗动武

#Geopolitics #OilPrice #Crypto #Forex"""
    }
]

print("=" * 60)
print("🐦 推文内容预览")
print("=" * 60)

for i, tweet in enumerate(tweets, 1):
    print(f"\n--- 推文 {i} ---")
    print(tweet["text"])
    print(f"\n字数: {len(tweet['text'])} / 280")
    print("-" * 40)

print("\n" + "=" * 60)
print("💡 发推方式选择：")
print("=" * 60)
print("""
方式 1: 使用 inference.sh CLI (推荐)
   安装: curl -fsSL https://cli.inference.sh | sh
   登录: infsh login
   发推: infsh app run x/post-tweet --input '{"text": "推文内容"}'

方式 2: 使用 Twitter API v2
   需要: TWITTER_BEARER_TOKEN
   运行: python twitter_post.py --tweet "推文内容"

方式 3: 使用浏览器自动化
   通过 OpenClaw 浏览器工具登录 twitter.com 手动发布

方式 4: 复制粘贴
   直接复制上方推文内容到 Twitter/X 网页/APP 发布
""")

print("\n📝 建议发布顺序：")
print("   推文 1 (总览) → 推文 2 (市场影响) → 推文 3 (深度分析)")
print("   形成 Thread (推文串)")
