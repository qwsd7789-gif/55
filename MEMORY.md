# MEMORY.md - 长期记忆

## 🧠 记忆系统（Three-Tier）
- **L1 长期记忆**: `MEMORY.md`（核心原则/用户偏好/长期目标）
- **L2 每日记忆**: `memory/YYYY-MM-DD.md`（事件、决策、上下文）
- **L3 项目记忆**: `PROJECTS.md`（目标、状态、阻塞、下一步）
- **检索优先级**: MEMORY.md > 今日日志 > 昨日日志 > PROJECTS.md > 更早日志

## 🧠 用例模板记忆

### Polymarket Scanner（已学习，待能力接入）
- **目标**: 夜间每15分钟扫描预测市场，跟踪仓位与价格异动，晨报输出 P&L + 建议动作。
- **标准流程**:
  1) 拉取跟踪市场价格
  2) 计算仓位 P&L
  3) 检测 >10% 价格异动并告警
  4) 记录日志与机会点
  5) 早晨汇总健康报告
- **当前状态**: 本机 skills 列表未发现 `polymarket`（待安装/接入后可自动化执行）。

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

### 2026-03-16
- 用户新增偏好：Reddit 定时简报默认翻译成中文输出。
- 展示格式偏好：按“各板块 Top3 + 中文标题 + 原帖链接”呈现，优先手机端可读。
### 2026-03-19
- 用户将 Reddit 每日热点抓取/推送板块调整为：地缘政治、石油、股票、数字货币。

### 2026-03-20
- 用户将 Reddit 抓取方向进一步调整为：财经、股票、伊朗。
- 用户开始尝试 ClawChain 挖矿，已完成本机矿工初始化与首轮成功提交。

### 2026-03-24
- 用户再次调整 Reddit 抓取/推送板块，今后默认仅抓取：财经、股票、数字货币、政治、战争。

### 2026-03-10
- 用户确认将 `video-copy-analyzer` 作为共享全局 skill，供所有 agent 默认复用。
- 新增全局规则：当链接或文件中包含视频，且用户需求是“提取视频文案 / 提取字幕 / 获取口播内容 / 理解视频内容”时，默认优先使用 `video-copy-analyzer`。
- 适用平台包括但不限于：小红书、抖音、B站、YouTube 等视频链接。
### 2026-03-06
- 用户新增工作偏好：收到任务后，先判断能否使用已有技能/经验路径。
- 若建议使用某个技能执行，必须先征求用户确认（“我建议用 XXX 技能来做，可以吗？”），得到同意后再执行。
- 当用户要“找某个 skill”时，优先试用/调用 `find-skills` 技能。
- 今后凡是用户询问任何 skill，也优先使用 `find-skills` 技能检索；回答时先给出候选 skill 的安装量与具体功能，再给建议。
- 用户新增默认安装/配置策略：除非用户特别说明，后续安装 skill 时默认按“全局安装、尽量让所有 agent 可见/可用”执行；若 skill 需要 API / key / cookie / token 等配置，也默认优先采用可被其他 agent 复用的全局配置路径，而不是仅配在当前 agent/会话里。
- 但存在显式例外：X/Twitter 凭据不全局共享，仅限 `x-chuangzuo` 与 `video-stream` 两个 agent 使用。
- 用户新增全局执行偏好：以后凡是找数据、打开网站、调用某类功能时，先优先检查并使用已经安装的 skill；只有在现有 skill 不合适、不可用或不存在时，才再去外部源/外部方案。
- 用户新增网页抓取偏好：在与用户对话时，如需打开网页、读取网页内容、抓取页面数据，默认优先尝试使用 `opencli`；仅当 `opencli` 不适合、不可用或目标不支持时，再退回其他网页抓取方案。
- 用户说“整理一下/整理把”时，默认理解为：把当前会话里值得保留的规则、项目状态、成功路径沉淀进记忆/项目文件，帮助减轻上下文负载。
- 在执行任何任务前，先进行“是否可用已有 skill 完成”的快速检查，再确定执行路径。
- 用户确认将“r.jina.ai 网页文本化前缀”作为常用经验纳入长期记忆。
- 新增强规则：今后遇到链接打不开，默认优先尝试 `https://r.jina.ai/http://原始链接`（或 `https://r.jina.ai/https://原始链接`）进行文本化访问，再考虑其他抓取方案。

### 2026-03-07
- 用户确认将“链接失败时先 r.jina.ai 重试”升级为强制执行规则。
- 规则落地为：自动重试（不先询问）→ r.jina.ai 失败后立即找合适 agent/自动化抓取 → 再失败才给人工替代方案。
- 已加注防偏移要求：不得跳过该步骤；若失败需明确告知每一步已尝试情况。

### 2025-03-02
- 设置伊朗战争监控系统
- 整合 6551 OpenNews 作为推特/新闻源
