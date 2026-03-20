# Active Projects

## 伊朗战争监控简报
**Goal**: 每30分钟输出可靠简报（多信源）
**Status**: 已停止
**Blockers**: 无
**Next Step**: 如用户重新开启，再恢复监控与推送
**Source**: memory/2026-03-02.md

## Polymarket 伊朗停战盘口监控
**Goal**: 每天 08:00 / 20:00 监控伊朗停战相关盘口，推送停战概率及较上次变化
**Status**: 脚本已创建并跑通，待接入 cron
**Scope**: `us-x-iran-ceasefire-by-march-31`、`us-x-iran-ceasefire-by-april-15-182`、`us-x-iran-ceasefire-by-april-30-194`、`trump-announces-end-of-military-operations-against-iran-by-march-31st`
**Output**: `reports/poly_iran_ceasefire/*.md` + `memory/poly_iran_ceasefire_state.json`
**Source**: 2026-03-19 本会话

## Workspace 自动备份（GitHub）
**Goal**: 每12小时自动备份 workspace 到 GitHub
**Status**: 已启用并完成首次推送
**Blockers**: 无
**Next Step**: 定期检查计划任务与推送结果
**Source**: memory/2026-03-02.md

## Skill 能力扩展
**Goal**: 持续补齐高频可用 skills
**Status**: find-skills 已安装（ready）
**Blockers**: 某些来源受网络/SSL限制
**Next Step**: 用 find-skills 筛选并安装“memory management / context”相关技能
**Source**: 本会话安装结果

## Suxi / Gemini 图片重绘工作流
**Goal**: 基于本地 XHS HTML/图片批量调用 Suxi 的 `gemini-2.5-flash-image` 做重绘，并自动输出原图/生成图 HTML 对照页
**Status**: 已跑通，可批量执行
**关键路径**:
- API Base URL: `OPENAI_BASE_URL=https://new.suxi.ai/v1`
- 认证: `SUXI_API_KEY`（或兼容 `OPENAI_API_KEY`）
- 默认模型: `gemini-2.5-flash-image`
- 入口脚本: `workspace/suxi_image.mjs`
- 已存在多份批处理脚本，支持不同篇数/图序号/提示词模板
**已验证经验**:
- API 路线优先于网页自动化，适合批量处理
- 若接口返回 `No inline image`，常见原因是模型回了文字说明而非图片数据
- 提示词中加入“不要输出任何解释文字，只返回最终生成的图片结果”后，成功率明显提高
- `fetch failed` 更像链路抖动，重试常可恢复
- `model_not_found` / “无可用渠道” 说明 Suxi 上游分发临时不可用，稍后重试可能恢复
**Next Step**: 将现有批处理脚本收敛为一个可参数化通用脚本（支持篇数范围、倒数选择、图片序号、提示词模板）
**Source**: 2026-03-09 会话批量执行结果

---

## Migration Rules
- Daily log -> MEMORY.md：当偏好/原则被重复验证
- Daily log -> PROJECTS.md：当一次性任务演变为持续项目
- PROJECTS.md -> MEMORY.md：项目完结后沉淀长期经验
- Daily logs >30天：归档为月度摘要

## Success Metrics
- 核心上下文加载控制在 3 个文件内（MEMORY + 今日/昨日 + PROJECTS）
- 历史决策可在 30 秒内定位
- 显著减少“重复确认已讨论事项”
