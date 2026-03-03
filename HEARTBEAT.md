# 伊朗战争监控 - 每30分钟简报
# 自动获取最新中东/伊朗战争动态

## 任务说明
每30分钟检查一次伊朗战争相关新闻，生成简报发送给用户。

## 执行流程
1. 从 Al Jazeera (半岛电视台) RSS 获取最新中东新闻
2. 从 BBC Middle East RSS 获取英国视角新闻
3. 从 6551 OpenNews API 获取加密/推特聚合新闻
4. 追加“多源检索层”：用 Brave/Search 抓取补充来源（Reuters/AP/FT/CNBC 等）
   - 若 `BRAVE_API_KEY` 未配置或调用失败：自动跳过该层，不报错、不在简报里提示技术错误
5. 筛选 Iran/Israel/Gaza/Khamenei/Hamas/Hezbollah/Oil/tanker 关键词
6. 整合可用信源，整理前10条最重要新闻（不强制四源齐全）
7. **生成简报并主动推送**：直接发给 `agent1-news`，同时抄送飞书群 `oc_fa483d56bb555fbdbff8a5a081ab7719`，不在当前会话直接回复
8. 发送完成

## 简报输出规则
- 简报生成后，通过 `message.send` 主动推送到飞书「新闻简报」群
- 同时更新到 `agent1-news` 的工作记忆
- **不再在当前 webchat 会话中直接回复简报内容**

## 简报模板
```
📊 伊朗战争简报 - [时间]
📡 信源：半岛电视台 + BBC + 6551 OpenNews(推特聚合) + Brave补充检索

🔥 最新动态：
1. [标题] [信源] ([时间])
2. ...

🛢️ 能源/航运动态：
[油轮、石油设施、航运相关]

📈 市场影响：
[油价、股市、加密货币反应]

💡 局势摘要：
[关键变化分析]

🔗 详情链接：
[新闻链接列表]
```

## 数据源
| 信源 | 类型 | URL/API |
|------|------|---------|
| Al Jazeera (半岛电视台) | RSS | https://www.aljazeera.com/xml/rss/all.xml |
| BBC Middle East | RSS | https://feeds.bbci.co.uk/news/world/middle_east/rss.xml |
| 6551 OpenNews | API | https://ai.6551.io/open/news_search |
| Brave Search（补充） | API/搜索 | 通过 web_search 检索 Reuters/AP/FT/CNBC 等 |

## 关键词监控
- 冲突: Iran, Israel, Gaza, war, conflict, Khamenei, Hamas, Hezbollah, Lebanon
- 能源: oil, tanker, ship, vessel, Hormuz, Aramco, refinery, energy, gas
- 航运: Hormuz, Strait of Hormuz, shipping, maritime, port, vessel, cargo
- 地区: Qatar, UAE, Kuwait, Saudi, Cyprus, Lebanon, Middle East
- 市场: oil price, stock, crypto, BTC, ETH

## 6551 OpenNews API 使用
```powershell
$headers = @{ "Authorization" = "Bearer $env:OPENNEWS_TOKEN"; "Content-Type" = "application/json" }
$body = '{"q": "Iran conflict", "limit": 10, "page": 1}'
$response = Invoke-RestMethod -Uri "https://ai.6551.io/open/news_search" -Method Post -Headers $headers -Body $body
```

## 下次执行时间
每30分钟执行一次 (Heartbeat 触发)
