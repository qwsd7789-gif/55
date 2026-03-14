Title: 可用工具

URL Source: http://listenhub.ai/docs/zh/mcp/available-tools

Markdown Content:
可用工具
----

工具清单与关键参数定义。

### [音色查询](http://listenhub.ai/docs/zh/mcp/available-tools#%E9%9F%B3%E8%89%B2%E6%9F%A5%E8%AF%A2)

*   **get_speakers** - 获取可用于播客生成的音色列表。返回音色 ID、姓名、语言、性别和试听音频链接。
    *   `language`：按语言代码筛选（zh/en）（字符串，可选）

### [播客生成](http://listenhub.ai/docs/zh/mcp/available-tools#%E6%92%AD%E5%AE%A2%E7%94%9F%E6%88%90)

*   **create_podcast** - 创建播客，包含完整生成（文本 + 音频）。支持 1-2 位音色。自动轮询直至完成（可能需要几分钟）。
    *   `query`：内容或主题（字符串，可选）
    *   `sources`：文本/URL 来源数组（数组，可选）
    *   `speakerIds`：1-2 个音色 ID 数组（数组，必需）
    *   `language`：语言代码 - zh 或 en（字符串，可选，默认：en）
    *   `mode`：生成模式 - quick、deep 或 debate（字符串，可选，默认：quick）

*   **get_podcast_status** - 查询播客的详细信息。立即返回当前状态，不进行轮询。
    *   `episodeId`：播客 ID（字符串，必需）

*   **create_podcast_text_only** - 创建仅包含文本内容的播客（不含音频）。先审后录流程的第一阶段。
    *   `query`：内容或主题（字符串，可选）
    *   `sources`：文本/URL 来源数组（数组，可选）
    *   `speakerIds`：1-2 个音色 ID 数组（数组，必需）
    *   `language`：语言代码 - zh 或 en（字符串，必需）
    *   `mode`：生成模式 - quick、deep 或 debate（字符串，可选，默认：quick）
    *   `waitForCompletion`：等待生成完成（布尔值，可选，默认：true）

*   **generate_podcast_audio** - 为已有文本内容的播客生成音频。先审后录流程的第二阶段。
    *   `episodeId`：播客 ID（字符串，必需）
    *   `customScripts`：自定义脚本数组（数组，可选）
    *   `waitForCompletion`：等待生成完成（布尔值，可选，默认：true）

### [FlowSpeech 生成](http://listenhub.ai/docs/zh/mcp/available-tools#flowspeech-%E7%94%9F%E6%88%90)

*   **create_flowspeech** - 将文本或 URL 内容转换为语音，创建 FlowSpeech。支持智能模式（AI 增强）和直接模式（不修改）。
    *   `sourceType`：来源类型 - text 或 url（字符串，必需）
    *   `sourceContent`：来源内容（文本或 URL）（字符串，必需）
    *   `speakerId`：用于旁白的音色 ID（字符串，必需）
    *   `language`：语言代码 - zh 或 en（字符串，可选）
    *   `mode`：生成模式 - smart 或 direct（字符串，可选，默认：smart）

*   **get_flowspeech_status** - 查询 FlowSpeech 的详细信息。立即返回当前状态，不进行轮询。
    *   `episodeId`：FlowSpeech ID（字符串，必需）

### [用户账户查询](http://listenhub.ai/docs/zh/mcp/available-tools#%E7%94%A8%E6%88%B7%E8%B4%A6%E6%88%B7%E6%9F%A5%E8%AF%A2)

*   **get_user_subscription** - 获取当前用户的订阅信息，包括订阅状态、积分使用情况、套餐详情和续订状态。

* * *

**感谢使用 ListenHub MCP Server！**

如有任何问题，请随时联系我们：[support@marswave.ai](mailto:support@marswave.ai)
