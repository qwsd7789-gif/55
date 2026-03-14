Title: 语音合成（TTS)

URL Source: http://listenhub.ai/docs/zh/skills/tts

Markdown Content:
语音合成（TTS)
===============

[![Image 1: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/tts)[中文](http://listenhub.ai/docs/zh/skills/tts)

[![Image 2: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/tts)[中文](http://listenhub.ai/docs/zh/skills/tts)

Search

⌘K

[ListenHub Skills](http://listenhub.ai/docs/zh/skills)[快速开始](http://listenhub.ai/docs/zh/skills/getting-started)[更新 Skills](http://listenhub.ai/docs/zh/skills/updating)[AI 播客](http://listenhub.ai/docs/zh/skills/podcast)[解说视频](http://listenhub.ai/docs/zh/skills/explainer)[语音合成（TTS)](http://listenhub.ai/docs/zh/skills/tts)[语音识别（ASR）](http://listenhub.ai/docs/zh/skills/asr)[图片生成](http://listenhub.ai/docs/zh/skills/image)[内容提取](http://listenhub.ai/docs/zh/skills/content-parser)

进阶指南

[帮助与 FAQ](http://listenhub.ai/docs/zh/skills/help)

[](https://listenhub.ai/welcome)[](https://x.com/listenhub)[](https://discord.gg/9gBPVG6m6x)[](https://github.com/marswaveai/skills)

快捷跳转

[文档站首页](http://listenhub.ai/docs/zh)[Agent Skills 指南](http://listenhub.ai/docs/zh/skills)[OpenAPI 指南](http://listenhub.ai/docs/zh/openapi)[MCP 指南](http://listenhub.ai/docs/zh/mcp)

语音合成（TTS)

语音合成（TTS)
=========

将文本转为自然语音 — 支持单人配音和多角色对话配音。

将文本或 URL 内容转化为自然流畅的语音音频。两种模式：单人配音适合日常朗读和文字转语音，多角色配音适合对话和旁白内容。

**AI Agent 提示**：本页完整内容可通过 `https://listenhub.ai/docs/en/skills/tts.mdx` 以文本形式获取。建议在帮助用户使用此 Skill 前，先用 WebFetch 读取该页内容。

[触发方式](http://listenhub.ai/docs/zh/skills/tts#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)
-----------------------------------------------------------------------------------

输入 `/tts` 命令，或使用以下任意短语触发：

| 短语 | 语言 |
| --- | --- |
| `read aloud` / `read this aloud` | 英文 |
| `TTS` / `text to speech` | 英文 |
| `voice narration` | 英文 |
| `朗读这段` | 中文 |
| `配音` / `语音合成` | 中文 |

使用前请先安装 ListenHub Skills — 参见[快速开始](http://listenhub.ai/docs/zh/skills/getting-started)。

[快速示例](http://listenhub.ai/docs/zh/skills/tts#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)
-----------------------------------------------------------------------------------

`朗读这篇文章：https://en.wikipedia.org/wiki/Podcast`

AI 会获取内容、选择音色，生成自然的语音音频。

[语音合成 vs 配音](http://listenhub.ai/docs/zh/skills/tts#%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90-vs-%E9%85%8D%E9%9F%B3)
---------------------------------------------------------------------------------------------------------------

两个 Skill 都能产出多人语音，但用途不同：

| 场景 | 推荐 Skill |
| --- | --- |
| 基于话题的自然对话讨论 | 播客 |
| 精确控制每句台词和音色 | 语音合成（多角色配音） |
| 朗读文章或文本 | 语音合成（单人配音） |

[两种模式](http://listenhub.ai/docs/zh/skills/tts#%E4%B8%A4%E7%A7%8D%E6%A8%A1%E5%BC%8F)
-----------------------------------------------------------------------------------

单人配音 多角色配音

将文本或 URL 内容转化为单人语音，快速简便（约 1-2 分钟）。

适合文章朗读、日常文字转语音和单人语音合成。

**处理模式：**

| 模式 | 说明 |
| --- | --- |
| `direct` | 原样朗读，不修改（默认） |
| `smart` | 朗读前自动修正语法和标点 |

多角色音频，按段落分配不同音色。速度适中（约 2-3 分钟）。

适合对话配音、多角色旁白和脚本朗读。

**脚本格式：**

```
{
  "scripts": [
    {"content": "大家好，欢迎收听节目。", "speakerId": "cozy-man-chinese"},
    {"content": "谢谢邀请！", "speakerId": "travel-girl-chinese"}
  ]
}
```

每段文字由指定的音色按顺序朗读。

[参数](http://listenhub.ai/docs/zh/skills/tts#%E5%8F%82%E6%95%B0)
---------------------------------------------------------------

| 参数 | 选项 | 默认值 |
| --- | --- | --- |
| 输入 | 文本或 URL | — |
| 语言 | `zh`（中文）、`en`（英文） | 自动检测 |
| 模式 | `direct`（直读）、`smart`（智能）（仅单人配音） | `direct` |
| 路径 | 单人配音、多角色配音 | 单人配音 |

[何时使用哪种模式](http://listenhub.ai/docs/zh/skills/tts#%E4%BD%95%E6%97%B6%E4%BD%BF%E7%94%A8%E5%93%AA%E7%A7%8D%E6%A8%A1%E5%BC%8F)
---------------------------------------------------------------------------------------------------------------------------

| 场景 | 模式 |
| --- | --- |
| 朗读文章或文本 | 单人配音 |
| 日常文字转语音 | 单人配音 |
| 多角色对话配音 | 多角色配音 |
| 精确控制每行的音色 | 多角色配音 |

[多角色配音技巧](http://listenhub.ai/docs/zh/skills/tts#%E5%A4%9A%E8%A7%92%E8%89%B2%E9%85%8D%E9%9F%B3%E6%8A%80%E5%B7%A7)
-----------------------------------------------------------------------------------------------------------------

*   在自然语句边界（句子或段落）处分段
*   交替使用不同音色以营造对话感
*   每个 `speakerId` 必须是 speakers API 返回的有效 ID
*   所有音色应使用相同语言

[限制](http://listenhub.ai/docs/zh/skills/tts#%E9%99%90%E5%88%B6)
---------------------------------------------------------------

*   FlowTTS 文本输入上限：10,000 字符
*   更长的内容请使用 URL 输入 — API 会自动获取并处理

[输出](http://listenhub.ai/docs/zh/skills/tts#%E8%BE%93%E5%87%BA)
---------------------------------------------------------------

生成完成后：

*   **收听链接** — 在 ListenHub 上播放
*   **音频下载** — 对 AI 说"下载音频"即可保存到本地

[API 参考](http://listenhub.ai/docs/zh/skills/tts#api-%E5%8F%82%E8%80%83)
-----------------------------------------------------------------------

技术细节请查看 [语音合成 API 接口文档](http://listenhub.ai/docs/zh/openapi)。

### On this page

[触发方式](http://listenhub.ai/docs/zh/skills/tts#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)[快速示例](http://listenhub.ai/docs/zh/skills/tts#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)[语音合成 vs 配音](http://listenhub.ai/docs/zh/skills/tts#%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90-vs-%E9%85%8D%E9%9F%B3)[两种模式](http://listenhub.ai/docs/zh/skills/tts#%E4%B8%A4%E7%A7%8D%E6%A8%A1%E5%BC%8F)[参数](http://listenhub.ai/docs/zh/skills/tts#%E5%8F%82%E6%95%B0)[何时使用哪种模式](http://listenhub.ai/docs/zh/skills/tts#%E4%BD%95%E6%97%B6%E4%BD%BF%E7%94%A8%E5%93%AA%E7%A7%8D%E6%A8%A1%E5%BC%8F)[多角色配音技巧](http://listenhub.ai/docs/zh/skills/tts#%E5%A4%9A%E8%A7%92%E8%89%B2%E9%85%8D%E9%9F%B3%E6%8A%80%E5%B7%A7)[限制](http://listenhub.ai/docs/zh/skills/tts#%E9%99%90%E5%88%B6)[输出](http://listenhub.ai/docs/zh/skills/tts#%E8%BE%93%E5%87%BA)[API 参考](http://listenhub.ai/docs/zh/skills/tts#api-%E5%8F%82%E8%80%83)
