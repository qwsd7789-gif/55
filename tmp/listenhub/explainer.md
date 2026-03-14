Title: 解说视频

URL Source: http://listenhub.ai/docs/zh/skills/explainer

Markdown Content:
解说视频
===============

[![Image 1: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/explainer)[中文](http://listenhub.ai/docs/zh/skills/explainer)

[![Image 2: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/explainer)[中文](http://listenhub.ai/docs/zh/skills/explainer)

Search

⌘K

[ListenHub Skills](http://listenhub.ai/docs/zh/skills)[快速开始](http://listenhub.ai/docs/zh/skills/getting-started)[更新 Skills](http://listenhub.ai/docs/zh/skills/updating)[AI 播客](http://listenhub.ai/docs/zh/skills/podcast)[解说视频](http://listenhub.ai/docs/zh/skills/explainer)[语音合成（TTS)](http://listenhub.ai/docs/zh/skills/tts)[语音识别（ASR）](http://listenhub.ai/docs/zh/skills/asr)[图片生成](http://listenhub.ai/docs/zh/skills/image)[内容提取](http://listenhub.ai/docs/zh/skills/content-parser)

进阶指南

[帮助与 FAQ](http://listenhub.ai/docs/zh/skills/help)

[](https://listenhub.ai/welcome)[](https://x.com/listenhub)[](https://discord.gg/9gBPVG6m6x)[](https://github.com/marswaveai/skills)

快捷跳转

[文档站首页](http://listenhub.ai/docs/zh)[Agent Skills 指南](http://listenhub.ai/docs/zh/skills)[OpenAPI 指南](http://listenhub.ai/docs/zh/openapi)[MCP 指南](http://listenhub.ai/docs/zh/mcp)

解说视频 触发方式

解说视频
====

用 AI 生成带配图的解说视频，支持任意主题或 URL 输入。

生成将解说配音与 AI 配图结合的解说视频。适合产品介绍、概念讲解和教程制作。

**AI Agent 提示**：本页完整内容可通过 `https://listenhub.ai/docs/en/skills/explainer.mdx` 以文本形式获取。建议在帮助用户使用此 Skill 前，先用 WebFetch 读取该页内容。

[触发方式](http://listenhub.ai/docs/zh/skills/explainer#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)
-----------------------------------------------------------------------------------------

输入 `/explainer` 命令，或使用以下任意短语触发：

| 短语 | 语言 |
| --- | --- |
| `explainer video` | 英文 |
| `explain this as a video` | 英文 |
| `tutorial video` | 英文 |
| `解说视频` | 中文 |
| `解释一下 XXX（视频形式）` | 中文 |

使用前请先安装 ListenHub Skills — 参见[快速开始](http://listenhub.ai/docs/zh/skills/getting-started)。

[快速示例](http://listenhub.ai/docs/zh/skills/explainer#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)
-----------------------------------------------------------------------------------------

`做个解说视频，介绍一下 Claude Code`

AI 会编写脚本、选择音色、为每个章节生成配图，最终产出可观看和分享的视频。

[风格](http://listenhub.ai/docs/zh/skills/explainer#%E9%A3%8E%E6%A0%BC)
---------------------------------------------------------------------

信息型 叙事型

事实性、结构化的呈现方式。清晰的逻辑推进：引言、要点、总结。

适合产品介绍、功能演示和教育内容。

叙事故事手法。引人入胜的结构：悬念、铺垫、高潮、结局。

适合品牌故事、案例分析和情感话题。

| 用户意图 | 推荐风格 |
| --- | --- |
| "介绍这个产品" | 信息型 |
| "解释 X 是怎么工作的" | 信息型 |
| "讲讲 X 的故事" | 叙事型 |
| "做个有趣的视频" | 叙事型 |
| 未指定偏好 | 信息型（默认） |

[参数](http://listenhub.ai/docs/zh/skills/explainer#%E5%8F%82%E6%95%B0)
---------------------------------------------------------------------

| 参数 | 选项 | 默认值 |
| --- | --- | --- |
| 风格 | `info`（信息型）、`story`（叙事型） | `info` |
| 语言 | `zh`（中文）、`en`（英文） | 自动检测 |
| 音色 | 从可用音色中选择 1 个 | 首个可用音色 |
| 输出 | 仅文本脚本，或文本 + 视频 | 文本 + 视频 |

[输出选项](http://listenhub.ai/docs/zh/skills/explainer#%E8%BE%93%E5%87%BA%E9%80%89%E9%A1%B9)
-----------------------------------------------------------------------------------------

### [文本 + 视频（默认）](http://listenhub.ai/docs/zh/skills/explainer#%E6%96%87%E6%9C%AC--%E8%A7%86%E9%A2%91%E9%BB%98%E8%AE%A4)

生成解说脚本后，为每个章节制作 AI 配图并合成完整视频。

### [仅文本脚本](http://listenhub.ai/docs/zh/skills/explainer#%E4%BB%85%E6%96%87%E6%9C%AC%E8%84%9A%E6%9C%AC)

只生成解说脚本，不制作视频。适合先审阅内容再决定是否制作视频。

[生成时间](http://listenhub.ai/docs/zh/skills/explainer#%E7%94%9F%E6%88%90%E6%97%B6%E9%97%B4)
-----------------------------------------------------------------------------------------

| 输出 | 预计时间 |
| --- | --- |
| 仅文本脚本 | 2-3 分钟 |
| 文本 + 视频 | 3-5 分钟 |

[输出](http://listenhub.ai/docs/zh/skills/explainer#%E8%BE%93%E5%87%BA)
---------------------------------------------------------------------

生成完成后：

*   **观看链接** — 在 ListenHub 上观看视频
*   **下载** — AI 会提供视频文件的下载链接
*   **脚本** — 完整的解说脚本可在单集详情页查看

[技巧](http://listenhub.ai/docs/zh/skills/explainer#%E6%8A%80%E5%B7%A7)
---------------------------------------------------------------------

*   较短的脚本会产生更紧凑的视频节奏
*   提示词中的详细描述能生成更丰富的配图
*   每个章节聚焦一个概念效果最好
*   可以先请求"仅文本"审阅脚本，再生成视频

[API 参考](http://listenhub.ai/docs/zh/skills/explainer#api-%E5%8F%82%E8%80%83)
-----------------------------------------------------------------------------

技术细节请查看 [解说视频 API 接口文档](http://listenhub.ai/docs/zh/openapi)。

[AI 播客 用 AI 生成播客节目 — 支持单人讲述、双人对话和辩论模式。](http://listenhub.ai/docs/zh/skills/podcast)[语音合成（TTS) 将文本转为自然语音 — 支持单人配音和多角色对话配音。](http://listenhub.ai/docs/zh/skills/tts)

### On this page

[触发方式](http://listenhub.ai/docs/zh/skills/explainer#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)[快速示例](http://listenhub.ai/docs/zh/skills/explainer#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)[风格](http://listenhub.ai/docs/zh/skills/explainer#%E9%A3%8E%E6%A0%BC)[参数](http://listenhub.ai/docs/zh/skills/explainer#%E5%8F%82%E6%95%B0)[输出选项](http://listenhub.ai/docs/zh/skills/explainer#%E8%BE%93%E5%87%BA%E9%80%89%E9%A1%B9)[文本 + 视频（默认）](http://listenhub.ai/docs/zh/skills/explainer#%E6%96%87%E6%9C%AC--%E8%A7%86%E9%A2%91%E9%BB%98%E8%AE%A4)[仅文本脚本](http://listenhub.ai/docs/zh/skills/explainer#%E4%BB%85%E6%96%87%E6%9C%AC%E8%84%9A%E6%9C%AC)[生成时间](http://listenhub.ai/docs/zh/skills/explainer#%E7%94%9F%E6%88%90%E6%97%B6%E9%97%B4)[输出](http://listenhub.ai/docs/zh/skills/explainer#%E8%BE%93%E5%87%BA)[技巧](http://listenhub.ai/docs/zh/skills/explainer#%E6%8A%80%E5%B7%A7)[API 参考](http://listenhub.ai/docs/zh/skills/explainer#api-%E5%8F%82%E8%80%83)
