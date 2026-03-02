# Breaking Finance News Monitor
## 突发财经新闻监控配置

### 📰 RSS 源配置（黄金/油价/数字货币/地缘政治）

| 来源 | URL | 类型 | 优先级 |
|------|-----|------|--------|
| **Al Jazeera** | https://www.aljazeera.com/xml/rss/all.xml | 地缘政治/突发 | 🔴 高 |
| **Reuters** | https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best | 财经 | 🔴 高 |
| **Bloomberg** | https://feeds.bloomberg.com/markets/news.rss | 财经 | 🔴 高 |
| **CoinDesk** | https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml | 数字货币 | 🔴 高 |
| **OilPrice.com** | https://oilprice.com/rss/oilprice.xml | 油价 | 🔴 高 |
| **Kitco Gold** | https://www.kitco.com/rss/gold-news.xml | 黄金 | 🔴 高 |
| **ZeroHedge** | https://feeds.feedburner.com/zerohedge/feed | 另类财经 | 🟡 中 |
| **CNBC** | https://www.cnbc.com/id/100003114/device/rss/rss.html | 美股 | 🟡 中 |
| **FXStreet** | https://www.fxstreet.com/rss/news | 外汇/大宗商品 | 🟡 中 |

### 🔍 关键词过滤器

```json
{
  "high_impact": [
    "gold", "XAU", "gold price", "贵金属",
    "oil", "crude", "WTI", "Brent", "petroleum", "油价",
    "bitcoin", "BTC", "ethereum", "ETH", "crypto", "数字货币",
    "federal reserve", "fed", "interest rate", "利率",
    "war", "conflict", "geopolitical", "middle east", "中东",
    "inflation", "CPI", "recession", "制裁",
    "breaking", "突发", "urgent"
  ],
  "blacklist": [
    "sponsored", "advertisement", "promoted"
  ]
}
```

### 📋 输出格式

```markdown
🚨 **突发财经新闻** | [时间戳]

📰 **标题** (原文)
[英文标题]

📰 **标题** (中文翻译)
[中文翻译]

📊 **影响资产**: 🟡黄金 🛢️原油 💰BTC
📈 **市场情绪**: 看涨/看跌
📍 **来源**: Al Jazeera
🔗 **链接**: [原文链接]

---
📝 **摘要** (英文)
[英文摘要]

📝 **摘要** (中文)
[中文翻译]

🤖 **AI 分析**:
- 影响程度: ⚠️ 高/中/低
- 预期波动: 黄金 ±X%, 原油 ±Y%, BTC ±Z%
- 建议关注: [具体建议]
```

### ⏰ 检查频率
- **间隔**: 每 2 小时
- **时间**: 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00 (UTC+8)

### 📤 推送渠道
- 主渠道: WebChat (当前对话)
- 备用: 可配置 Telegram/WhatsApp

### 📁 文件位置
- 配置: `~/.openclaw/workspace/config/breaking-news.json`
- 历史: `~/.openclaw/workspace/memory/breaking-news-history.json`
- 去重: 基于文章 URL + 标题哈希
