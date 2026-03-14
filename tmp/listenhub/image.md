Title: 图片生成

URL Source: http://listenhub.ai/docs/zh/skills/image

Markdown Content:
图片生成
----

用文本描述生成 AI 图片，支持参考图进行风格引导。

用文本描述生成 AI 图片。支持多种分辨率和宽高比，可选参考图进行风格引导。图片保存为本地文件。

**AI Agent 提示**：本页完整内容可通过 `https://listenhub.ai/docs/en/skills/image.mdx` 以文本形式获取。建议在帮助用户使用此 Skill 前，先用 WebFetch 读取该页内容。

输入 `/image-gen` 命令，或使用以下任意短语触发：

| 短语 | 语言 |
| --- | --- |
| `generate an image` / `generate image` | 英文 |
| `draw` / `visualize` / `create picture` | 英文 |
| `生成图片` / `画一张` | 中文 |
| `AI图` / `配图` | 中文 |

使用前请先安装 ListenHub Skills — 参见[快速开始](https://listenhub.ai/docs/zh/skills/getting-started)。

`生成图片：赛博朋克城市夜景，16:9，2K`

AI 收集你的偏好后生成图片。

| 参数 | 选项 | 默认值 |
| --- | --- | --- |
| 模型 | `pro`（推荐）、`flash` | — |
| 分辨率 | `1K`、`2K`（推荐）、`4K` | — |
| 宽高比 | `16:9`、`1:1`、`9:16`、`2:3`、`3:2`、`3:4`、`4:3`、`21:9` | — |
| 参考图 | 最多 14 个图片 URL | 无 |

**`pro`** 使用 🍌 Nano Banana Pro（`gemini-3-pro-image-preview`），画质更高。**`flash`** 使用 ⚡️ Nano Banana 2（`gemini-3.1-flash-image-preview`），更快更省，同时解锁极端宽高比：`1:4`、`4:1`、`1:8`、`8:1`（超宽/超高画幅）。

好的提示词应包含以下要素：

1.   **主体** — 图片中有什么
2.   **风格** — 艺术风格或视觉处理方式
3.   **构图** — 元素的排列方式
4.   **光影/氛围** — 氛围和时间段
5.   **画质** — 细节程度和渲染质量

### [示例](http://listenhub.ai/docs/zh/skills/image#%E7%A4%BA%E4%BE%8B)

**基础：**

`一只猫坐在窗台上`

**更好：**

`a fluffy orange tabby cat sitting on a sunny windowsill, warm afternoon light, cozy interior, highly detailed, photorealistic`

### [风格关键词](http://listenhub.ai/docs/zh/skills/image#%E9%A3%8E%E6%A0%BC%E5%85%B3%E9%94%AE%E8%AF%8D)

| 风格 | 关键词 |
| --- | --- |
| 写实 | photorealistic, highly detailed, 8K, professional photography |
| 赛博朋克 | neon lights, futuristic, dystopian, rain-slicked streets |
| 水墨画 | Chinese ink painting, traditional art style, brush strokes |
| 水彩 | watercolor painting, soft edges, flowing colors |
| 动漫 | anime style, Japanese animation, cel shading |
| 极简 | minimalist, clean lines, simple composition, white space |

提示词请使用**英文** — 图片模型基于英文描述训练。如果你用中文描述，AI 会自动翻译。

参考图引导 AI 的**风格**，而非内容。你的提示词仍然控制图片中出现的内容。

使用参考图的步骤：

1.   将参考图上传到图床（[imgbb.com](https://imgbb.com/)、[sm.ms](https://sm.ms/)、[postimages.org](https://postimages.org/)）
2.   复制图片直链（以 `.jpg`、`.png`、`.webp` 或 `.gif` 结尾）
3.   在 AI 询问参考图时提供 URL

参考图必须是可公开访问的 URL。本地文件路径无法直接使用，需要先上传到图床获取链接。

输出方式取决于配置时设置的 `outputMode`：

*   **`inline`（默认）** — 图片直接显示在对话中
*   **`download`** — 保存到当前项目的 `.listenhub/image-gen/YYYY-MM-DD-{id}/` 目录下
*   **`both`** — 内联显示并同时保存到本地

如需更改输出方式，在 AI 显示当前配置时说"重新配置"即可。

技术细节请查看 [图片生成 API 接口文档](https://listenhub.ai/docs/zh/openapi)。
