Title: 认证与安全 - ListenHub OpenAPI

URL Source: http://listenhub.ai/docs/zh/openapi/authentication

Markdown Content:
认证与安全
-----

Base URL、API Key 使用方式和请求限制。

所有 API 请求发送到：

`https://api.marswave.ai/openapi`

### [获取 API Key](http://listenhub.ai/docs/zh/openapi/authentication#%E8%8E%B7%E5%8F%96-api-key)

1.   访问 [API Key 设置页面](https://listenhub.ai/zh/settings/api-keys)
2.   点击「创建 API Key」
3.   复制并保存

### [使用方式](http://listenhub.ai/docs/zh/openapi/authentication#%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F)

在每个请求的 `Authorization` 头中携带 API Key：

### [设置环境变量](http://listenhub.ai/docs/zh/openapi/authentication#%E8%AE%BE%E7%BD%AE%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)

将 API Key 存为 `LISTENHUB_API_KEY` 环境变量，本文档所有代码示例均使用此变量名：

```
# 添加到 ~/.zshrc 或 ~/.bashrc
export LISTENHUB_API_KEY="your_api_key_here"
```

也可在项目根目录创建 `.env` 文件（需搭配 `dotenv` 等库加载）：

```
# .env
LISTENHUB_API_KEY=your_api_key_here
```

### [安全建议](http://listenhub.ai/docs/zh/openapi/authentication#%E5%AE%89%E5%85%A8%E5%BB%BA%E8%AE%AE)

API Key 等同于你的账户凭证，泄露可能导致积分被消耗。

*   始终使用 HTTPS
*   不要在前端代码中暴露 API Key
*   不要将 API Key 或 `.env` 文件提交到 Git 仓库
*   使用环境变量存储 API Key

| 限制项 | 值 | 说明 |
| --- | --- | --- |
| 创建请求频率 | 3 RPM | 每分钟最多 3 次创建请求 |
| 超出限制错误码 | `29998` | 实现退避重试策略 |

查询类请求（如查询单集状态、获取音色列表）不受此限制。

*   [快速开始](https://listenhub.ai/docs/zh/openapi/quick-start) — 5 分钟完成第一次调用
*   [核心概念](https://listenhub.ai/docs/zh/openapi/concepts) — 了解生成模式和数据流
*   [错误处理](https://listenhub.ai/docs/zh/openapi/errors) — 错误码速查和排查建议
