# Active Projects

## 伊朗战争监控简报
**Goal**: 每30分钟输出可靠简报（多信源）
**Status**: 运行中（当前受网络策略影响）
**Blockers**: 外网访问受限（RSS/GitHub/部分API握手失败）
**Next Step**: 网络恢复后立即补发完整简报，并持续按心跳频率执行
**Source**: memory/2026-03-02.md

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
