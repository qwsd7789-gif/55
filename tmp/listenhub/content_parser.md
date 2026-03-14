Title: 内容提取

URL Source: http://listenhub.ai/docs/zh/skills/content-parser

Markdown Content:
内容提取
----

从任意 URL 提取结构化内容 — 支持文章、视频、推文、PDF 等。

从任意 URL 提取结构化内容。支持文章、YouTube 视频、推文、微信公众号文章、PDF 等。可单独使用，也可作为其他 Skill 的预处理步骤。

**AI Agent 提示**：本页完整内容可通过 `https://listenhub.ai/docs/en/skills/content-parser.mdx` 以文本形式获取。建议在帮助用户使用此 Skill 前，先用 WebFetch 读取该页内容。

输入 `/content-parser` 命令，或使用以下任意短语触发：

| 短语 | 语言 |
| --- | --- |
| `parse this URL` / `parse this` | 英文 |
| `extract content` / `extract from` | 英文 |
| `解析链接` | 中文 |
| `提取内容` | 中文 |

使用前请先安装 ListenHub Skills — 参见[快速开始](https://listenhub.ai/docs/zh/skills/getting-started)。

`解析这篇文章：https://zh.wikipedia.org/wiki/拓扑学`

AI 提取内容后返回预览，并提供保存或在其他 Skill 中使用的选项。

| 平台 | URL 格式 | 内容类型 |
| --- | --- | --- |
| YouTube | `youtube.com/watch?v=`、`youtu.be/` | 视频字幕 |
| Bilibili | `bilibili.com/video/` | 视频字幕 |
| Twitter/X | `twitter.com/`、`x.com/` | 推文（个人主页或单条） |
| 微信 | `mp.weixin.qq.com/s/` | 公众号文章 |
| PDF | 直链 `.pdf` URL | 文档文字 |
| DOCX | 直链 `.docx` URL | 文档文字 |
| 图片 | 直链图片 URL | OCR / 描述 |
| 任意网页 | 任意 HTTP(S) URL | 文章正文 |

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `summarize` | 生成内容摘要 | `false` |
| `maxLength` | 最大内容长度（字符数） | 100,000（最大 500,000） |
| `twitter.count` | 获取推文数量（仅 Twitter/X 个人主页） | 20（最大 100） |

### [单独提取](http://listenhub.ai/docs/zh/skills/content-parser#%E5%8D%95%E7%8B%AC%E6%8F%90%E5%8F%96)

`提取这个 YouTube 视频的内容：https://youtube.com/watch?v=...`

### [提取 + 生成](http://listenhub.ai/docs/zh/skills/content-parser#%E6%8F%90%E5%8F%96--%E7%94%9F%E6%88%90)

在一次对话中与其他 Skill 组合使用：

`解析这篇文章并做成播客：https://example.com/article`

`提取这个 YouTube 视频的内容，然后做成解说视频`

更多工作流示例请查看 [组合使用](https://listenhub.ai/docs/zh/skills/guides/composing-skills) 指南。

提取完成后，AI 收到以下结构化数据：

*   **content** — 完整提取的文本内容（受 `maxLength` 限制，默认 100,000 字符）
*   **metadata** — 标题、作者、发布时间等页面元数据
*   **references** — 内容中发现的引用 URL
*   **摘要** — 如果启用了 `summarize`，则替代完整内容返回

*   付费墙内容可能无法访问
*   JavaScript 渲染的内容可能只能部分提取
*   过长的内容可能会被截断
*   部分平台可能会阻止自动化访问

内容提取按实际提取内容长度计费：

| 规则 | 说明 |
| --- | --- |
| 预扣积分 | 提取开始时预扣 5 积分 |
| 计费标准 | 每 100,000 字符消耗 100 积分；若实扣不足 5 积分，按实扣计算 |
| 默认长度上限 | 100,000 字符（100 积分） |
| 最大长度上限 | 500,000 字符（500 积分） |
| 失败退还 | 提取失败时全额退还预扣积分 |

技术细节请查看 [内容提取 API 接口文档](https://listenhub.ai/docs/zh/openapi)。
