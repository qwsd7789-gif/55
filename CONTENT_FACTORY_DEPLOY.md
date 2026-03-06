# OpenClaw + Obsidian 内容工厂部署记录

部署时间：2026-03-06

## 已完成

1. 创建中央内容库（Vault）
- 路径：`C:\Users\Administrator\Documents\bgggcontent`
- 目录结构：
  - `01-灵感与素材库/1-日常灵感剪报`
  - `01-灵感与素材库/2-爆款素材片段`
  - `02-选题池/待写选题库`
  - `03-内容工厂/1-大纲挑选区`
  - `03-内容工厂/2-初稿打磨区`
  - `03-内容工厂/3-终稿确认区`
  - `04-已发布归档/公众号已发布`

2. 为多 Agent 工作区创建共享链接 `bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-agent1-news\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-agent2-polymarket\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-agent3-xhs\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-agent4-xhs\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-builder\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-image-stream\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-orchestrator\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-reviewer\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-video-stream\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-work\bgggcontent`
- `C:\Users\Administrator\.openclaw\workspace-x-chuangzuo\bgggcontent`

3. 规则已全局生效
- 链接打不开时优先 `r.jina.ai` 前缀
- 任务执行前优先检查是否可用现有 skill
- 需要调用特定 skill 时先征求用户确认

## 说明

- 已安装 `npm i -g obsidian-cli`，但当前系统命令对应的是第三方同名 CLI（`obsidian`），并非我们预期的笔记操作工具。
- 因此当前阶段采用「共享 Vault + 目录规范 + Agent 规则」先落地，保证可用与安全。

## 下一步（建议）

1. 你在 Obsidian Desktop 中直接打开：`C:\Users\Administrator\Documents\bgggcontent`
2. 我为你生成 `SOP_GZH.md` + 文档 YAML 模板（可直接开写）
3. 再确认并接入可用的 Obsidian 文件操作链路（避免同名 CLI 混淆）
