Title: 积分与定价 - ListenHub OpenAPI

URL Source: http://listenhub.ai/docs/zh/openapi/pricing

Markdown Content:
积分与定价 - ListenHub OpenAPI
===============

[![Image 1: ListenHub](http://listenhub.ai/favicon.svg)OpenAPI](http://listenhub.ai/docs/zh/openapi)

[EN](http://listenhub.ai/docs/en/openapi/pricing)[中文](http://listenhub.ai/docs/zh/openapi/pricing)

[![Image 2: ListenHub](http://listenhub.ai/favicon.svg)OpenAPI](http://listenhub.ai/docs/zh/openapi)

[EN](http://listenhub.ai/docs/en/openapi/pricing)[中文](http://listenhub.ai/docs/zh/openapi/pricing)

Search

⌘K

[ListenHub OpenAPI](http://listenhub.ai/docs/zh/openapi)[快速开始](http://listenhub.ai/docs/zh/openapi/quick-start)

OpenClaw 🦞

[核心概念](http://listenhub.ai/docs/zh/openapi/concepts)[认证与安全](http://listenhub.ai/docs/zh/openapi/authentication)

API 参考

[错误处理](http://listenhub.ai/docs/zh/openapi/errors)[积分与定价](http://listenhub.ai/docs/zh/openapi/pricing)[技术支持](http://listenhub.ai/docs/zh/openapi/support)

[](https://listenhub.ai/welcome)[](https://x.com/listenhub)[](https://discord.gg/9gBPVG6m6x)

快捷跳转

[文档站首页](http://listenhub.ai/docs/zh)[Agent Skills 指南](http://listenhub.ai/docs/zh/skills)[OpenAPI 指南](http://listenhub.ai/docs/zh/openapi)[MCP 指南](http://listenhub.ai/docs/zh/mcp)

积分与定价

积分与定价
=====

积分类型、消耗参考与请求限制。

[积分概述](http://listenhub.ai/docs/zh/openapi/pricing#%E7%A7%AF%E5%88%86%E6%A6%82%E8%BF%B0)
----------------------------------------------------------------------------------------

ListenHub 使用积分系统计费。积分可用于生成 AI 播客、文本转语音、内容提取等所有 API 功能。新用户注册即获 100 积分，可以直接体验 API。

[积分类型](http://listenhub.ai/docs/zh/openapi/pricing#%E7%A7%AF%E5%88%86%E7%B1%BB%E5%9E%8B)
----------------------------------------------------------------------------------------

| 类型 | 有效期 | 获取方式 |
| --- | --- | --- |
| **月度积分** | 当前订阅周期内有效，周期结束后清零 | 订阅自动发放 |
| **永久积分** | 永不过期 | 购买积分包、邀请奖励、分享奖励 |
| **限时积分** | 发放时注明有效期，逾期失效 | 每日签到、官方活动 |

扣除顺序：**限时积分 → 月度积分 → 永久积分**。

[订阅计划](http://listenhub.ai/docs/zh/openapi/pricing#%E8%AE%A2%E9%98%85%E8%AE%A1%E5%88%92)
----------------------------------------------------------------------------------------

| 计划 | 月度积分 |
| --- | --- |
| Basic | 1,300 积分/月 |
| Pro | 2,700 积分/月 |
| Max | 30,000 积分/月 |

除订阅外，还可以[购买积分包](https://listenhub.ai/zh/pricing/pack?from=pricing)获取永久积分。

[积分消耗参考](http://listenhub.ai/docs/zh/openapi/pricing#%E7%A7%AF%E5%88%86%E6%B6%88%E8%80%97%E5%8F%82%E8%80%83)
------------------------------------------------------------------------------------------------------------

| 内容类型 | 参考消耗 |
| --- | --- |
| 5 分钟 AI 播客 | ~24 积分 |
| 10 分钟文字转语音 | ~40 积分 |
| 内容提取 | 最低 5 积分；每 100,000 字符消耗 100 积分（最高 500 积分） |

以上积分消耗数据仅供参考，实际消耗以系统实时计算为准。调用 `GET /v1/user/subscription` 可随时查询积分余额。

### [内容提取积分策略](http://listenhub.ai/docs/zh/openapi/pricing#%E5%86%85%E5%AE%B9%E6%8F%90%E5%8F%96%E7%A7%AF%E5%88%86%E7%AD%96%E7%95%A5)

内容提取采用预扣积分模式：

| 规则 | 说明 |
| --- | --- |
| **预扣积分** | 任务开始时预扣 5 积分 |
| **实际扣除** | 每 100,000 字符消耗 100 积分；若实扣不足 5 积分，按实扣计算 |
| **失败退还** | 提取失败时全额退还预扣积分 |
| **默认长度上限** | 每次请求 100,000 字符（100 积分） |
| **最大长度上限** | 每次请求 500,000 字符（500 积分） |

积分按实际提取内容长度计算。3,000 字符的文章实扣 3 积分；100,000 字符的文章消耗 100 积分；250,000 字符的文章消耗 250 积分。

[请求限制](http://listenhub.ai/docs/zh/openapi/pricing#%E8%AF%B7%E6%B1%82%E9%99%90%E5%88%B6)
----------------------------------------------------------------------------------------

| 限制项 | 值 | 说明 |
| --- | --- | --- |
| 创建请求频率 | 3 RPM | 每分钟最多 3 次创建请求 |
| 超出限制错误码 | `29998` | 实现退避重试策略 |

**推荐策略**：

*   实现请求队列，避免突发请求
*   使用指数退避算法进行重试
*   监控请求频率，预防触发限制

[查询积分余额](http://listenhub.ai/docs/zh/openapi/pricing#%E6%9F%A5%E8%AF%A2%E7%A7%AF%E5%88%86%E4%BD%99%E9%A2%9D)
------------------------------------------------------------------------------------------------------------

通过 API 查询当前积分详情：

cURL JavaScript Python

```
curl -X GET "https://api.marswave.ai/openapi/v1/user/subscription" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY"
```

```
const response = await fetch('https://api.marswave.ai/openapi/v1/user/subscription', {
  headers: {
    'Authorization': `Bearer ${process.env.LISTENHUB_API_KEY}`,
  },
});
const data = await response.json();
console.log('Available credits:', data.data.totalAvailableCredits);
```

```
import os
import requests

response = requests.get(
    'https://api.marswave.ai/openapi/v1/user/subscription',
    headers={'Authorization': f'Bearer {os.environ["LISTENHUB_API_KEY"]}'}
)
data = response.json()
print('Available credits:', data['data']['totalAvailableCredits'])
```

返回结果包含月度积分、永久积分、限时积分和总可用积分。详见 [订阅查询 API](http://listenhub.ai/docs/zh/openapi/api-reference/subscription)。

[下一步](http://listenhub.ai/docs/zh/openapi/pricing#%E4%B8%8B%E4%B8%80%E6%AD%A5)
------------------------------------------------------------------------------

*   [错误处理](http://listenhub.ai/docs/zh/openapi/errors) — 积分不足（26004）等错误码的处理
*   [技术支持](http://listenhub.ai/docs/zh/openapi/support) — 企业方案和定制需求
*   [订阅查询 API](http://listenhub.ai/docs/zh/openapi/api-reference/subscription) — 完整的积分查询接口说明

### On this page

[积分概述](http://listenhub.ai/docs/zh/openapi/pricing#%E7%A7%AF%E5%88%86%E6%A6%82%E8%BF%B0)[积分类型](http://listenhub.ai/docs/zh/openapi/pricing#%E7%A7%AF%E5%88%86%E7%B1%BB%E5%9E%8B)[订阅计划](http://listenhub.ai/docs/zh/openapi/pricing#%E8%AE%A2%E9%98%85%E8%AE%A1%E5%88%92)[积分消耗参考](http://listenhub.ai/docs/zh/openapi/pricing#%E7%A7%AF%E5%88%86%E6%B6%88%E8%80%97%E5%8F%82%E8%80%83)[内容提取积分策略](http://listenhub.ai/docs/zh/openapi/pricing#%E5%86%85%E5%AE%B9%E6%8F%90%E5%8F%96%E7%A7%AF%E5%88%86%E7%AD%96%E7%95%A5)[请求限制](http://listenhub.ai/docs/zh/openapi/pricing#%E8%AF%B7%E6%B1%82%E9%99%90%E5%88%B6)[查询积分余额](http://listenhub.ai/docs/zh/openapi/pricing#%E6%9F%A5%E8%AF%A2%E7%A7%AF%E5%88%86%E4%BD%99%E9%A2%9D)[下一步](http://listenhub.ai/docs/zh/openapi/pricing#%E4%B8%8B%E4%B8%80%E6%AD%A5)
