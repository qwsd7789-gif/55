# 突发财经新闻监控系统 - 配置指南

## ✅ 已完成配置

### 1. 安装的技能
- ✅ `finance-news` - 基础财经新闻
- ✅ `twitter-automation` - 推特发布（之前安装的）

### 2. 配置文件
- 📄 `~/.openclaw/workspace/config/breaking-news-monitor.md` - 监控配置说明
- 📄 `~/.openclaw/workspace/config/breaking-news-cron.yaml` - Cron 任务配置
- 🐍 `~/.openclaw/workspace/scripts/breaking-news-monitor.py` - 检测脚本
- 📋 `~/.openclaw/workspace/HEARTBEAT.md` - 心跳检测任务

### 3. 监控的 RSS 源
| 来源 | 类型 | 优先级 |
|------|------|--------|
| Al Jazeera | 地缘政治/中东新闻 | 🔴 高 |
| Reuters Markets | 全球财经 | 🔴 高 |
| CoinDesk | 数字货币 | 🔴 高 |
| OilPrice.com | 原油/能源 | 🔴 高 |
| Kitco | 黄金/贵金属 | 🔴 高 |

### 4. 监控的资产
- 🟡 **黄金** (Gold, XAU, XAUUSD)
- 🛢️ **原油** (Oil, WTI, Brent, Crude)
- 💰 **数字货币** (Bitcoin, BTC, Ethereum, ETH)

### 5. 高影响力关键词
`breaking`, `突发`, `urgent`, `fed`, `interest rate`, `war`, `conflict`, `middle east`, `inflation`, `sanctions`, `战争`, `制裁`

---

## 🚀 启动监控

### 方式一：OpenClaw Cron（推荐）
运行以下命令配置每 2 小时执行：

```bash
# 添加 cron 任务
openclaw cron add --schedule "0 */2 * * *" \
  --timezone "Asia/Shanghai" \
  --command "python3 ~/.openclaw/workspace/scripts/breaking-news-monitor.py"
```

### 方式二：手动测试
先手动运行测试：

```bash
python3 ~/.openclaw/workspace/scripts/breaking-news-monitor.py
```

### 方式三：心跳检测（已配置）
心跳检测会自动读取 `HEARTBEAT.md` 并执行检查任务。

---

## 📤 推送设置

当前配置推送到 **WebChat**（即当前对话）。

如需改为其他渠道：
- **Telegram**: 修改脚本中的推送逻辑
- **WhatsApp**: 使用 `message` 工具
- **飞书/钉钉**: 配置 Webhook

---

## 📝 输出格式示例

```markdown
🔴 **突发财经新闻** | 2026-03-02 16:00

📰 **标题** (原文)
BREAKING: Federal Reserve signals potential rate cuts in March

📊 **影响资产**: 🟡黄金 🛢️原油 💰数字货币
📍 **来源**: Reuters (Global)
🔗 **链接**: https://reuters.com/...

---
📝 **摘要** (原文)
The Federal Reserve indicated in its latest meeting that...

🤖 **AI 分析**:
- 影响程度: ⚠️ 高
- 涉及资产: 黄金, 原油, 数字货币
- 建议关注: 利率决策可能引发市场波动，请关注后续声明
```

---

## ⚙️ 自定义配置

### 添加新的 RSS 源
编辑 `~/.openclaw/workspace/scripts/breaking-news-monitor.py`：

```python
RSS_SOURCES = {
    # ... 现有源
    "BBC": {
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "priority": "medium",
        "region": "Global"
    }
}
```

### 修改关键词
在脚本中编辑 `ASSET_KEYWORDS` 或 `HIGH_IMPACT_KEYWORDS`。

### 调整检查频率
修改 `HEARTBEAT.md` 或 cron 配置的 schedule 表达式。

---

## 🔔 提醒

1. **首次运行**: 建议先手动测试脚本是否正常工作
2. **去重机制**: 48 小时内相同新闻不会重复推送
3. **AI 翻译**: 当前版本为预留接口，如需完整双语翻译，需接入 Gemini/Kimi API
4. **RSS 稳定性**: 部分 RSS 源可能需要翻墙访问

---

## 📞 需要帮助？

如需调整配置或添加新的新闻源，随时告诉我！
