Title: 核心概念 - ListenHub OpenAPI

URL Source: http://listenhub.ai/docs/zh/openapi/concepts

Markdown Content:
核心概念
----

Episode、Speaker、生成模式与数据流说明。

*   **Episode（单集）** — ListenHub 的基本内容单元。每个单集有唯一的 `episodeId`，包含音频、文本脚本和元数据。
*   **Speaker（音色）** — 定义音频的声学特征。通过 `speakerId` 标识，包含语言和性别等属性。调用 `GET /v1/speakers/list` 获取可用音色列表，或浏览[语音角色文档](https://listenhub.ai/docs/zh/openapi/api-reference/speakers)。

| 模式 | 子模式 | 说明 | 生成时间 | API 端点 |
| --- | --- | --- | --- | --- |
| [**Podcast**](https://listenhub.ai/docs/zh/openapi/api-reference/podcast) | **quick** | 快速生成，效率优先，适合新闻快报等时效性内容 | 1-2 分钟 | `/v1/podcast/episodes` |
|  | **debate** | 双主持人辩论形式，适合观点讨论和多角度分析 | 2-4 分钟 |  |
|  | **deep** | 深度分析，内容质量高，适合专业知识分享和深度解读 | 2-4 分钟 |  |
| [**Text to Speech**](https://listenhub.ai/docs/zh/openapi/api-reference/flowspeech) | **smart** | AI 智能优化内容后再合成，适合修复不通顺语句和错别字 | 1-2 分钟 | `/v1/flow-speech/episodes` |
|  | **direct** | 文本直接转换语音，适合已完善的文本和播报 | 1-2 分钟 |  |
| [**Content Extract**](https://listenhub.ai/docs/zh/openapi/api-reference/content-extract) | — | 异步 URL 内容提取，适合文章解析、调研和内容分析 | 10-30 秒 | `/v1/content/extract` |

Podcast 模式支持选择 1-2 个 Speaker（单人或双人播客）。debate 模式必须使用 2 个 Speaker。

每个 Episode 生成后可获取两类数据：脚本文本和音频文件。

### [脚本](http://listenhub.ai/docs/zh/openapi/concepts#%E8%84%9A%E6%9C%AC)

音频生成期间，可通过 SSE 提前获取大纲和脚本文本，无需等待音频完成：

*   **Podcast**：创建后 20-60 秒开始推送
*   **Text to Speech**：创建后约 3 秒开始推送

### [音频文件](http://listenhub.ai/docs/zh/openapi/concepts#%E9%9F%B3%E9%A2%91%E6%96%87%E4%BB%B6)

音频生成完成后，响应中包含以下字段：

| 字段 | 格式 | 说明 |
| --- | --- | --- |
| `audioStreamUrl` | M3U8 | 流式播放，适合实时场景 |
| `audioUrl` | MP3 | 完整文件，适合下载和离线使用 |

ListenHub 提供在线 Playground，无需编写代码即可体验多音色语音合成。

**访问地址**：[Multi-speaker TTS Playground](https://assets.listenhub.ai/listenhub-public-prod/static/playgroud-tts.html)

*   多角色对话——一次生成包含多个音色的对话音频
*   灵活分配——为每段台词独立指定音色
*   即时试听——在线编辑脚本，实时预览效果

适用于有声书/广播剧制作、对话式内容生成和产品演示快速制作。

*   [快速开始](https://listenhub.ai/docs/zh/openapi/quick-start) — 5 分钟完成第一次 API 调用
*   [认证说明](https://listenhub.ai/docs/zh/openapi/authentication) — Base URL、API Key 和请求限制
*   [播客生成 API](https://listenhub.ai/docs/zh/openapi/api-reference/podcast) — 完整参数和响应说明
