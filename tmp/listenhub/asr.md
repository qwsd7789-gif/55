Title: 语音识别（ASR）

URL Source: http://listenhub.ai/docs/zh/skills/asr

Markdown Content:
语音识别（ASR）
===============

[![Image 1: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/asr)[中文](http://listenhub.ai/docs/zh/skills/asr)

[![Image 2: ListenHub](http://listenhub.ai/favicon.svg)Skills](http://listenhub.ai/docs/zh/skills)

[EN](http://listenhub.ai/docs/en/skills/asr)[中文](http://listenhub.ai/docs/zh/skills/asr)

Search

⌘K

[ListenHub Skills](http://listenhub.ai/docs/zh/skills)[快速开始](http://listenhub.ai/docs/zh/skills/getting-started)[更新 Skills](http://listenhub.ai/docs/zh/skills/updating)[AI 播客](http://listenhub.ai/docs/zh/skills/podcast)[解说视频](http://listenhub.ai/docs/zh/skills/explainer)[语音合成（TTS)](http://listenhub.ai/docs/zh/skills/tts)[语音识别（ASR）](http://listenhub.ai/docs/zh/skills/asr)[图片生成](http://listenhub.ai/docs/zh/skills/image)[内容提取](http://listenhub.ai/docs/zh/skills/content-parser)

进阶指南

[帮助与 FAQ](http://listenhub.ai/docs/zh/skills/help)

[](https://listenhub.ai/welcome)[](https://x.com/listenhub)[](https://discord.gg/9gBPVG6m6x)[](https://github.com/marswaveai/skills)

快捷跳转

[文档站首页](http://listenhub.ai/docs/zh)[Agent Skills 指南](http://listenhub.ai/docs/zh/skills)[OpenAPI 指南](http://listenhub.ai/docs/zh/openapi)[MCP 指南](http://listenhub.ai/docs/zh/mcp)

语音识别（ASR）前置依赖

语音识别（ASR）
=========

使用本地语音识别将音频文件转录为文字 — 无需 API Key。

使用 `coli asr` 将音频文件转录为文字，完全在本地离线运行。安装完成后无需 API Key 或网络连接。

**无需 ListenHub API Key。** 此 Skill 完全在本机运行。需要安装 `coli` 命令行工具 — 详见下方前置依赖说明。

**AI Agent 提示**：本页完整内容可通过 `https://listenhub.ai/docs/en/skills/asr.mdx` 以文本形式获取。建议在帮助用户使用此 Skill 前，先用 WebFetch 读取该页内容。

[前置依赖](http://listenhub.ai/docs/zh/skills/asr#%E5%89%8D%E7%BD%AE%E4%BE%9D%E8%B5%96)
-----------------------------------------------------------------------------------

使用此 Skill 前，请先安装 `coli` 命令行工具：

`npm install -g @marswave/coli`

**可选但推荐：** 安装 `ffmpeg` 以支持更多音频格式（MP4、M4A、AAC 等）：

```
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

WAV 格式无需 `ffmpeg`，其他格式需要。

首次转录时，`coli` 会自动下载所需的语音模型（约 60 MB）到 `~/.coli/models/`。

[触发方式](http://listenhub.ai/docs/zh/skills/asr#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)
-----------------------------------------------------------------------------------

使用 `/asr` 调用此 Skill，或使用以下任意短语：

| 短语 | 语言 |
| --- | --- |
| `transcribe` / `transcribe this` | 英文 |
| `ASR` | 英文 |
| `转录` / `识别音频` | 中文 |
| `语音转文字` | 中文 |
| `把这段音频转成文字` | 中文 |

[快速示例](http://listenhub.ai/docs/zh/skills/asr#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)
-----------------------------------------------------------------------------------

`帮我转录这个文件 meeting.m4a`

AI 会检查前置依赖、读取配置、确认参数后在本地运行转录。结果直接显示在对话中。

[模型](http://listenhub.ai/docs/zh/skills/asr#%E6%A8%A1%E5%9E%8B)
---------------------------------------------------------------

| 模型 | 支持语言 | 说明 |
| --- | --- | --- |
| `sensevoice`（默认） | 中文、英文、日语、韩语、粤语 | 同时检测语言、情绪和音频事件 |
| `whisper-tiny.en` | 仅英文 | 轻量模型，仅支持英文 |

多语言内容或语言未知时，推荐使用 `sensevoice`。

[选项](http://listenhub.ai/docs/zh/skills/asr#%E9%80%89%E9%A1%B9)
---------------------------------------------------------------

### [AI 润色](http://listenhub.ai/docs/zh/skills/asr#ai-%E6%B6%A6%E8%89%B2)

启用润色（默认开启）时，AI 会对原始转录进行后处理：修正标点、去除语气词、提升可读性，但不改变原意，也不进行摘要。

原始转录文本随时可按需查看。

[输出](http://listenhub.ai/docs/zh/skills/asr#%E8%BE%93%E5%87%BA)
---------------------------------------------------------------

转录结果直接显示在对话中。查看后，AI 会询问是否保存为 Markdown 文件到当前目录：

`{音频文件名}-transcript.md`

Markdown 文件包含 front-matter 头部，记录源文件、日期、模型、时长和检测到的语言。

[组合使用](http://listenhub.ai/docs/zh/skills/asr#%E7%BB%84%E5%90%88%E4%BD%BF%E7%94%A8)
-----------------------------------------------------------------------------------

此 Skill 输出的文字可直接传递给其他 Skill：

*   转录采访录音 → 作为参考材料传入 `/podcast`
*   转录语音备忘 → 作为 `/explainer` 的输入内容

[API 参考](http://listenhub.ai/docs/zh/skills/asr#api-%E5%8F%82%E8%80%83)
-----------------------------------------------------------------------

无 API 调用。此 Skill 仅使用本地 `coli asr` 命令。

[语音合成（TTS) 将文本转为自然语音 — 支持单人配音和多角色对话配音。](http://listenhub.ai/docs/zh/skills/tts)[图片生成 用文本描述生成 AI 图片，支持参考图进行风格引导。](http://listenhub.ai/docs/zh/skills/image)

### On this page

[前置依赖](http://listenhub.ai/docs/zh/skills/asr#%E5%89%8D%E7%BD%AE%E4%BE%9D%E8%B5%96)[触发方式](http://listenhub.ai/docs/zh/skills/asr#%E8%A7%A6%E5%8F%91%E6%96%B9%E5%BC%8F)[快速示例](http://listenhub.ai/docs/zh/skills/asr#%E5%BF%AB%E9%80%9F%E7%A4%BA%E4%BE%8B)[模型](http://listenhub.ai/docs/zh/skills/asr#%E6%A8%A1%E5%9E%8B)[选项](http://listenhub.ai/docs/zh/skills/asr#%E9%80%89%E9%A1%B9)[AI 润色](http://listenhub.ai/docs/zh/skills/asr#ai-%E6%B6%A6%E8%89%B2)[输出](http://listenhub.ai/docs/zh/skills/asr#%E8%BE%93%E5%87%BA)[组合使用](http://listenhub.ai/docs/zh/skills/asr#%E7%BB%84%E5%90%88%E4%BD%BF%E7%94%A8)[API 参考](http://listenhub.ai/docs/zh/skills/asr#api-%E5%8F%82%E8%80%83)
