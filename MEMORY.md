# MEMORY.md - 长期记忆

## 核心偏好
- 用户习惯直接下达任务，希望先动手排查和修复。
- 执行任务前先检查是否已有可用 skill；若建议用某个 skill 执行，先征求用户确认。
- 链接抓取失败时，默认先尝试 `r.jina.ai` 文本化回退。
- 网页打开/抓取默认优先尝试 `opencli`；不适用再换其他方案。
- 视频口播/字幕/文案提取默认优先 `video-copy-analyzer`。
- 回测默认引擎：vectorbt。
- 年化收益默认口径：CAGR。

## 当前长期事项
- 已安装并可复用 `seedance-cli`，用于即梦官方 CLI 提交/查任务。
- X/Twitter 抓取默认优先 `feedgrab`，优先复用 `tools/feedgrab/sessions/x.json`。
- 飞书本地文件发送默认优先 `lark-cli`。
