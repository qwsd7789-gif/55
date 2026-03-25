# X（Twitter）抓取 SOP
更新时间：2026-03-25
## 目标
在当前 OpenClaw / Windows 工作区中，稳定抓取 X（Twitter）推文正文、线程与可用元数据；优先保证“能读正文并可分析”，其次再提升到“登录态 GraphQL 抓取”。
## 当前已验证可用的主路径
- 主工具：`feedgrab`
- 仓库位置：`C:\Users\Administrator\.openclaw\workspace\tools\feedgrab`
- 已验证：写入 `sessions/x.json` 后，可进入 `twitter_graphql` 抓取链路
---
## 推荐默认执行顺序（当前主会话 agent）
### 路径 1：优先用 `feedgrab` 直接抓
适用：用户发来单条 X 推文链接，先看能否直接抓到正文。
命令：
```powershell
feedgrab "https://x.com/<user>/status/<id>"
```
判定：
- 若能直接返回正文，可先完成“读内容/总结/判断”任务
- 若日志出现 `No valid Twitter cookies found from any source`，说明当前仅走匿名/降级链路，正文通常仍可抓，但完整数据不足
---
### 路径 2：若缺登录态，优先读取 `sessions/x.json`
适用：需要更稳定的 X 抓取、GraphQL、线程、更多元数据。
有效文件：
```text
tools/feedgrab/sessions/x.json
```
格式：
```json
{
  "auth_token": "...",
  "ct0": "..."
}
```
验证命令：
```powershell
feedgrab "https://x.com/<user>/status/<id>"
```
成功标志：
- 日志不再出现 `No valid Twitter cookies found from any source`
- 日志进入 `feedgrab.fetchers.twitter_graphql`
- 看到类似：`Found N tweets by @...`
---
### 路径 3：尝试通过主 Chrome 接管登录态（次优先）
适用：用户不想手动给 cookie，且愿意接管主 Chrome。
前提：
- Chrome 已打开
- 最好开启 remote debugging
- 用户允许接管
当前经验：
- 可以接入 Chrome 页签列表
- 但当前环境下 Chrome 的 remote debugging 服务不稳定，`DevToolsActivePort` 可能存在，但 `http://127.0.0.1:922/json/version` 仍打不开
- 因此路径 **不作为当前默认主路径**，只作为补充尝试
已验证的接管脚本路径：
```text
C:\Users\Administrator\.openclaw\skills\chrome-cdp-skill\skills\chrome-cdp\scripts\cdp.mjs
```
探测命令：
```powershell
node C:\Users\Administrator\.openclaw\skills\chrome-cdp-skill\skills\chrome-cdp\scripts\cdp.mjs list
```
若用户手动确认 Chrome 已允许调试，且 `cdp.mjs list` 能正常列页签，则说明浏览器页面级控制已打通。
但要注意：
- “能列页签” ≠ “一定能成功抽出 X 的 auth_token / ct0”
- 当前这台机器上，CDP 抽 cookie 仍不稳定，不应作为首选依赖
---
### 路径 4：用户手动提供 cookie（当前最稳补救方案）
适用：Chrome 接管失败 / CDP 不稳定 / 需要快速恢复 X 完整抓取能力。
只需要两个值：
- `auth_token`
- `ct0`
写入：
```text
tools/feedgrab/sessions/x.json
```
写入后立即复测：
```powershell
feedgrab "https://x.com/<user>/status/<id>"
```
这是当前 **最稳、最快、最少折腾** 的恢复方案。
---
## 当前抓取方法尝试顺序（固化）
今后处理 X 链接时，默认按以下顺序：
1. **`feedgrab` 直接抓原始 X 链接**
   - 目标：先拿正文
   - 优点：最快
2. **若需要更完整抓取，检查 `tools/feedgrab/sessions/x.json` 是否已有可用 cookie**
   - 有则直接复测
3. **若没有 cookie，尝试主 Chrome 接管（仅在用户同意后）**
   - 检查 Chrome CDP / remote debugging
   - 尝试 `cdp.mjs list`
   - 若失败，不长时间死磕
4. **若主 Chrome 接管不稳定，立即切换为“用户手动提供 `auth_token` + `ct0`”**
   - 这是当前最终兜底且最高成功率路径
5. **抓取成功后，再做正文总结/观点判断/线程分析**
---
## 不再作为当前主路径的方法
### 1. `web_fetch` 直接抓 `x.com`
已验证：当前环境中可能返回
- `Blocked: resolves to private/internal/special-use IP address`
因此不作为 X 主抓取方法。
### 2. `r.jina.ai` 文本化 X 链接
理论上可试，但当前环境同样可能被拦；且即便成功，也通常不如 `feedgrab` 的 X 专用链路稳定。
### 3. Firecrawl
当前环境中 Firecrawl CLI 需要先登录/API key；在未完成认证前，不作为当前主路径。
### 4. `opencli-rs`
已安装，但当前主要定位为通用站点适配 CLI，不作为这台机器上 X 单条推文抓取的首选。
后续可单独评估其在 X 抓取中的位置。
---
## 当前环境结论
### 已安装 / 已验证
- `feedgrab`：已安装并可用
- `opencli-rs`：已安装并可运行
- `feedgrab + sessions/x.json`：已验证可进入 GraphQL 抓取路径
### 当前默认推荐
> 以后抓 X：**优先 feedgrab；优先复用 `sessions/x.json`；Chrome 接管只作补充；接管不稳就直接手动 cookie。**
---
## 最短操作模板
### A. 直接抓
```powershell
cd C:\Users\Administrator\.openclaw\workspace\tools\feedgrab
feedgrab "https://x.com/<user>/status/<id>"
```
### B. 写入 cookie 后再抓
```powershell
# 文件：tools/feedgrab/sessions/x.json
{
  "auth_token": "...",
  "ct0": "..."
}
cd C:\Users\Administrator\.openclaw\workspace\tools\feedgrab
feedgrab "https://x.com/<user>/status/<id>"
```
### C. 检查 Chrome 接管
```powershell
node C:\Users\Administrator\.openclaw\skills\chrome-cdp-skill\skills\chrome-cdp\scripts\cdp.mjs list
```
---
## 本次实战结论（2026-03-25）
- `feedgrab` 匿名链路可抓正文
- Chrome 主浏览器页签接管可部分打通
- Chrome CDP 抽 X cookie 在当前机器上不稳定
- 用户手动提供 `auth_token` + `ct0` 后，成功打通 `feedgrab` 的登录态 GraphQL 抓取路径
