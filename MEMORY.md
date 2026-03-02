# MEMORY.md - 长期记忆

## 🧠 重要技能记忆

### OpenNews 6551 Skill
- **用途**: 通过 API 获取加密新闻和实时更新
- **API**: `https://ai.6551.io/open/news_search`
- **认证**: Bearer Token ($OPENNEWS_TOKEN)
- **功能**:
  - 关键词搜索新闻
  - AI评分和信号分析
  - 实时市场动态
- **使用场景**: 伊朗战争监控、油价动态、地缘政治
- **已配置**: ✅ 环境变量 OPENNEWS_TOKEN 已设置

**示例命令**:
```powershell
$headers = @{ "Authorization" = "Bearer $env:OPENNEWS_TOKEN"; "Content-Type" = "application/json" }
$body = '{"q": "Iran conflict", "limit": 10, "page": 1}'
$response = Invoke-RestMethod -Uri "https://ai.6551.io/open/news_search" -Method Post -Headers $headers -Body $body
```

### Twitter-Automation Skill
- **用途**: 通过 inference.sh 自动发推
- **状态**: ❌ infsh CLI 在 Windows 上安装困难
- **替代方案**: 使用 OpenNews 6551 获取推特相关新闻

### 伊朗战争监控任务
- **频率**: 每30分钟
- **信源**: 
  - 半岛电视台 RSS
  - BBC Middle East RSS
  - 6551 OpenNews API (推特+新闻聚合)
- **监控关键词**: Iran, Israel, Gaza, war, oil, tanker, Khamenei

---

## 📅 时间线

### 2025-03-02
- 设置伊朗战争监控系统
- 整合 6551 OpenNews 作为推特/新闻源
