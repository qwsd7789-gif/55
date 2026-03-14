Title: 错误处理 - ListenHub OpenAPI

URL Source: http://listenhub.ai/docs/zh/openapi/errors

Markdown Content:
错误处理
----

错误码速查与排查建议。

ListenHub API 所有响应都使用 HTTP 200 状态码。通过响应体中的 `code` 字段区分成功与失败：`code = 0` 表示成功，`code ≠ 0` 表示失败。

| 错误码 | 说明 | 处理建议 |
| --- | --- | --- |
| **0** | 请求成功 | — |
| **21007** | API Key 无效 | 检查 `Authorization` 头格式是否为 `Bearer $LISTENHUB_API_KEY`，确认 API Key 已正确复制 |
| **25002** | 资源不存在 | 检查 `episodeId` 是否正确 |
| **25008** | 单集状态不正确 | 仅在「先审后录」流程中出现。需等待文稿生成完成后再提交音频合成，详见[播客 API 文档](https://listenhub.ai/docs/zh/openapi/api-reference/podcast) |
| **26004** | 积分不足 | 调用 `GET /v1/user/subscription` 查询余额，前往[积分购买页面](https://listenhub.ai/zh/pricing/pack?from=pricing)充值 |
| **29003** | 参数错误 | 检查请求参数是否符合 API 文档要求 |
| **29998** | 请求过于频繁 | 已超出 3 RPM 限制，实现退避重试 |
| **91001** | 内容过短 | 增加输入内容长度 |
| **91002** | 内容违规 | 检查内容是否符合平台规范 |
| **91003-91007** | 内容生成错误 | 查看 `message` 字段获取具体错误信息 |

所有错误响应遵循相同的 JSON 格式：

```
{
  "code": 21007,
  "message": "Invalid API key",
  "data": null
}
```

**API Key 问题（21007）**：

1.   确认 `Authorization` 头格式为 `Bearer $LISTENHUB_API_KEY`（注意 Bearer 后有空格）
2.   确认 API Key 完整复制，无多余空格
3.   前往 [API Key 设置页面](https://listenhub.ai/zh/settings/api-keys) 确认 Key 状态

**频率限制（29998）**：

1.   创建请求限制为每分钟 3 次（3 RPM）
2.   查询请求不受此限制
3.   实现指数退避重试策略

*   [认证说明](https://listenhub.ai/docs/zh/openapi/authentication) — API Key 获取和安全建议
*   [积分与定价](https://listenhub.ai/docs/zh/openapi/pricing) — 积分余额不足时的解决方案
*   [技术支持](https://listenhub.ai/docs/zh/openapi/support) — 联系支持团队
