Title: AI 播客

URL Source: http://listenhub.ai/docs/zh/skills/podcast

Markdown Content:
AI 播客
===============

[![Image 1: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/podcast)[中文](http://listenhub.ai/docs/zh/skills/podcast)

[![Image 2: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/podcast)[中文](http://listenhub.ai/docs/zh/skills/podcast)

Search

⌘K

[ListenHub Skills](http://listenhub.ai/docs/zh/skills)[快速开始](http://listenhub.ai/docs/zh/skills/getting-started)[更新 Skills](http://listenhub.ai/docs/zh/skills/updating)[AI 播客](http://listenhub.ai/docs/zh/skills/podcast)[解说视频](http://listenhub.ai/docs/zh/skills/explainer)[语音合成（TTS)](http://listenhub.ai/docs/zh/skills/tts)[语音识别（ASR）](http://listenhub.ai/docs/zh/skills/asr)[图片生成](http://listenhub.ai/docs/zh/skills/image)[内容提取](http://listenhub.ai/docs/zh/skills/content-parser)

进阶指南

[帮助与 FAQ](http://listenhub.ai/docs/zh/skills/help)

[](https://listenhub.ai/welcome)[](https://x.com/listenhub)[](https://discord.gg/9gBPVG6m6x)[](https://github.com/marswaveai/skills)

快捷跳转

[文档站首页](http://listenhub.ai/docs/zh)[Agent Skills 指南](http://listenhub.ai/docs/zh/skills)[OpenAPI 指南](http://listenhub.ai/docs/zh/openapi)[MCP 指南](http://listenhub.ai/docs/zh/mcp)

AI 播客 触发方式

AI 播客
=====

用 AI 生成播客节目 — 支持单人讲述、双人对话和辩论模式。

从任意主题、URL 或文本生成播客节目。支持快速概述、深度分析和辩论等多种模式，可选 1-2 位 AI 主播。

**AI Agent 提示**：本页完整内容可通过 `https://listenhub.ai/docs/en/skills/podcast.mdx` 以文本形式获取。建议在帮助用户使用此 Skill 前，先用 WebFetch 读取该页内容。

[触发方式](http://listenhub.ai/docs/zh/skills/podcast#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)
---------------------------------------------------------------------------------------

输入 `/podcast` 命令，或使用以下任意短语触发：

| 短语 | 语言 |
| --- | --- |
| `make a podcast about...` | 英文 |
| `podcast` | 英文 |
| `discuss` / `debate` / `dialogue` | 英文 |
| `做播客` | 中文 |
| `播客` / `录一期节目` | 中文 |

使用前请先安装 ListenHub Skills — 参见[快速开始](http://listenhub.ai/docs/zh/skills/getting-started)。

[快速示例](http://listenhub.ai/docs/zh/skills/podcast#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)
---------------------------------------------------------------------------------------

`做个关于最新 AI 发展的播客，用中文，要有深度`

AI 会自动处理选题研究、写稿、选声和音频生成。完成后你会收到收听和下载链接。

[模式](http://listenhub.ai/docs/zh/skills/podcast#%E6%A8%A1%E5%BC%8F)
-------------------------------------------------------------------

快速 深度 辩论

简短精练的话题概述，约 5 分钟。

适合新闻摘要、简要介绍和快速点评。

深入分析和详细讨论，约 10-15 分钟。

适合主题深挖、教育内容和深度解析。

两位主播持不同观点进行讨论，约 10-15 分钟。需要 2 位主播。

适合争议话题、利弊分析和观点碰撞。

| 用户意图 | 推荐模式 |
| --- | --- |
| "快速了解一下 X" | 快速 |
| "深入学习 X" | 深度 |
| "X 的优缺点是什么" | 辩论 |
| 未指定偏好 | 快速（默认） |

[参数](http://listenhub.ai/docs/zh/skills/podcast#%E5%8F%82%E6%95%B0)
-------------------------------------------------------------------

| 参数 | 选项 | 默认值 |
| --- | --- | --- |
| 模式 | `quick`（快速）、`deep`（深度）、`debate`（辩论） | `quick` |
| 语言 | `zh`（中文）、`en`（英文） | 自动检测 |
| 主播数量 | 1（单人）或 2（对话） | 1 |
| 参考材料 | URL 或文本 | 无 |

主播列表从 API 动态获取 — AI 会展示对应语言的可用音色供你选择。可以问"有哪些音色？"来浏览完整列表和试听。

[生成方式](http://listenhub.ai/docs/zh/skills/podcast#%E7%94%9F%E6%88%90%E6%96%B9%E5%BC%8F)
---------------------------------------------------------------------------------------

### [一步生成（推荐）](http://listenhub.ai/docs/zh/skills/podcast#%E4%B8%80%E6%AD%A5%E7%94%9F%E6%88%90%E6%8E%A8%E8%8D%90)

文本和音频一次性生成，更快更简单。

`"做个关于量子计算的播客"`

### [两步生成（先审稿）](http://listenhub.ai/docs/zh/skills/podcast#%E4%B8%A4%E6%AD%A5%E7%94%9F%E6%88%90%E5%85%88%E5%AE%A1%E7%A8%BF)

先生成文本脚本，允许你审阅和编辑后再生成音频。

`"做个关于量子计算的播客，让我先看看稿子"`

两步生成流程：

1.   生成文本脚本并保存为 markdown 文件
2.   暂停等待审阅 — 你可以编辑内容、调整长度或重新组织结构
3.   确认后从最终脚本生成音频

适合需要精简长稿、调整语气或确保准确性的场景。

[支持的输入](http://listenhub.ai/docs/zh/skills/podcast#%E6%94%AF%E6%8C%81%E7%9A%84%E8%BE%93%E5%85%A5)
-------------------------------------------------------------------------------------------------

| 输入类型 | 示例 |
| --- | --- |
| 主题描述 | "可再生能源的未来" |
| URL | YouTube 视频、文章或博客链接 |
| 纯文本 | 直接粘贴或输入内容 |

[输出](http://listenhub.ai/docs/zh/skills/podcast#%E8%BE%93%E5%87%BA)
-------------------------------------------------------------------

生成完成后，你会收到：

*   **收听链接** — 在 ListenHub 上直接播放
*   **音频下载** — 对 AI 说"下载音频"即可保存到本地
*   **文稿** — 在单集详情页中查看

[API 参考](http://listenhub.ai/docs/zh/skills/podcast#api-%E5%8F%82%E8%80%83)
---------------------------------------------------------------------------

技术细节请查看 [播客 API 接口文档](http://listenhub.ai/docs/zh/openapi)。

[更新 Skills 保持 ListenHub Skills 最新状态。用户和 AI Agent 的更新说明。](http://listenhub.ai/docs/zh/skills/updating)[解说视频 用 AI 生成带配图的解说视频，支持任意主题或 URL 输入。](http://listenhub.ai/docs/zh/skills/explainer)

### On this page

[触发方式](http://listenhub.ai/docs/zh/skills/podcast#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)[快速示例](http://listenhub.ai/docs/zh/skills/podcast#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)[模式](http://listenhub.ai/docs/zh/skills/podcast#%E6%A8%A1%E5%BC%8F)[参数](http://listenhub.ai/docs/zh/skills/podcast#%E5%8F%82%E6%95%B0)[生成方式](http://listenhub.ai/docs/zh/skills/podcast#%E7%94%9F%E6%88%90%E6%96%B9%E5%BC%8F)[一步生成（推荐）](http://listenhub.ai/docs/zh/skills/podcast#%E4%B8%80%E6%AD%A5%E7%94%9F%E6%88%90%E6%8E%A8%E8%8D%90)[两步生成（先审稿）](http://listenhub.ai/docs/zh/skills/podcast#%E4%B8%A4%E6%AD%A5%E7%94%9F%E6%88%90%E5%85%88%E5%AE%A1%E7%A8%BF)[支持的输入](http://listenhub.ai/docs/zh/skills/podcast#%E6%94%AF%E6%8C%81%E7%9A%84%E8%BE%93%E5%85%A5)[输出](http://listenhub.ai/docs/zh/skills/podcast#%E8%BE%93%E5%87%BA)[API 参考](http://listenhub.ai/docs/zh/skills/podcast#api-%E5%8F%82%E8%80%83)
