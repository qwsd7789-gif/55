# 伊朗战争监控简报任务
# 每30分钟检查一次最新动态

## 执行步骤：
1. 从 Al Jazeera RSS 获取中东新闻
2. 筛选 Iran/Israel/Gaza/war/conflict 相关新闻
3. 生成简报并发送给用户

## 简报格式：
- 📅 时间：[当前时间]
- 🔥 最新动态：
  1. [新闻标题] - [时间]
  2. ...
- 📊 局势评估：[AI分析]
- 📎 相关链接

## 信息源：
- Al Jazeera English (半岛电视台): https://www.aljazeera.com/xml/rss/all.xml
- BBC Middle East: https://feeds.bbci.co.uk/news/world/middle_east/rss.xml
- Twitter 监控 (待配置)

## 执行命令：
# 获取最新新闻
Invoke-WebRequest -Uri "https://www.aljazeera.com/xml/rss/all.xml" -UseBasicParsing | 
  [xml]$xml = $_; 
  $xml.rss.channel.item | Where-Object { $_.title -match "Iran|Israel|Gaza|war|conflict|Khamenei|Hamas|Hezbollah" } | 
  Select-Object -First 5
