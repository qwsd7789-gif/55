# TOOLS.md - Local Notes
Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.
## What Goes Here
Things like:
- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific
## Examples
```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered
### SSH
- home-server → 192.168.1.100, user: admin
### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```
## Why Separate?
Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.
---
## 新闻与推文
- **首选工具**: `opennews` skill
- **用途**: 获取新闻源和推特推文
- **替代方案**: 当 opennews 不可用时，使用 web_search 或 browser
---
## 视频文案提取
- **全局默认技能**: `video-copy-analyzer`
- **默认触发**: 用户给出视频链接/视频文件，并要求提取文案、字幕、口播内容，或要求理解视频内容
- **适用平台**: 小红书、抖音、B站、YouTube 等
- **当前状态**: 已可用；2026-03-10 已修复阶段2所需 ffmpeg 环境
## 即梦 / Dreamina CLI
- **共享全局技能**: `seedance-cli`
- **安装位置**: `C:\Users\Administrator\.openclaw\skills\seedance-cli`
- **本机二进制**: `C:\Users\Administrator\dreamina-bin\dreamina.exe`
- **默认用途**: 当用户明确要求“直接提交即梦任务/查 submit_id/查余额/查结果”时，优先走本地官方 CLI，而不是只写提示词
- **默认视频模型**: `seedance2.0fast`
- **常见能力**: `text2video`、`image2video`、`multiframe2video`、`multimodal2video`、`query_result`、`list_task`、`user_credit`
- **当前状态**: 2026-04-03 已验证可直接提交任务，账户余额可用

## ASR 转写默认路径
- **默认工具**: `coli asr`（本地离线）
- **安装状态**: ✅ `@marswave/coli` 已安装
- **备用工具**: `openai-whisper`（需要时用于可调模型/批处理）
---
## 小红书 (Xiaohongshu)
- **发布模式**: 直接发布（不再询问确认）
- **默认账号**: default
- **浏览器模式**: headed（有窗口）
- **稳定抓取脚本（两阶段，v2）**: `scripts/xhs_collect_notes.ps1`
  - 流程: 先 `search-feeds` 抓链接，再逐条 `get-feed-detail` 提取
  - 增强: 失败分类统计 + 自动补抓（`-BackfillPasses`）
  - 示例: `./scripts/xhs_collect_notes.ps1 -Keyword "留学申请" -Top 20 -Retry 2 -BackfillPasses 1 -ReuseExistingTab`
---
## 网页打开与抓取
- **默认优先工具**: `opencli`
- **适用场景**: 与用户对话时，需要打开网页、读取网页内容、抓取页面数据
- **执行顺序**: 先尝试 `opencli` → 若不适用/不支持/失败，再改用其他抓取方案
---
## 飞书命令默认路径
- **默认优先工具**: `lark-cli`（`@larksuite/cli`）
- **适用场景**: 以后凡是涉及飞书 / Lark 开放平台命令、消息、日历、文档、云盘、多维表格、邮箱、通讯录、知识库、会议等操作，默认优先尝试 `lark-cli`
- **执行顺序**: 先检查 `lark-cli` 是否已安装并可用 → 优先使用快捷命令（如 `im +messages-send`、`calendar +agenda`）→ 再使用 `schema` 自省 → 若快捷命令不覆盖，再退到 API 命令或 `lark-cli api` 通用调用
- **安全规则**:
  - 写操作优先 `--dry-run`（如支持）
  - 遇到不熟悉的 API，先跑 `lark-cli schema <api>`
  - 不在回复中泄露 token / secret / app credential
- **当前状态**: 2026-03-28 已完成 `lark-cli` 安装、飞书应用配置、用户登录和 doctor 健康检查；当前可直接用于飞书消息/文件发送
- **身份经验**:
  - `im +messages-send` 发消息时，默认显式带 `--as bot`
  - 用户接收方优先使用 `lark-cli auth status` 返回的当前 app 下 `userOpenId`，避免 `open_id cross app`
- **本地文件发送 SOP**:
  - 图片：若源文件不在当前工作目录，先复制到 workspace 下临时目录，再用相对路径发送（`--image ./file.jpg`）
  - 视频：先复制到 workspace 下临时目录，再生成封面图后发送（`--video ./video.mp4 --video-cover ./cover.jpg`）
  - `lark-cli` 对本地媒体路径要求较严格，优先使用“切到目标目录 + 相对路径”方式
---
## Session Labels（会话持久标签）
- 脚本: `scripts/session_labels.ps1`
- 存储: `memory/session-labels.json`
- 用途: 给 `sessionKey` 绑定自定义名称，重启后仍可恢复（UI 原生 Label 可能丢失）
示例：
- 设置：`./scripts/session_labels.ps1 -Action set -SessionKey 'agent:main:main' -Label '主会话'`
- 查看：`./scripts/session_labels.ps1 -Action list`
- 按当前 sessions 解析：`./scripts/session_labels.ps1 -Action resolve`
Add whatever helps you do your job. This is your cheat sheet.
