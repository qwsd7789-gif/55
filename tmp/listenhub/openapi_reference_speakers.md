Title: 音色列表 - ListenHub OpenAPI

URL Source: http://listenhub.ai/docs/zh/openapi/api-reference/speakers

Markdown Content:
[获取音色列表](http://listenhub.ai/docs/zh/openapi/api-reference/speakers#%E8%8E%B7%E5%8F%96%E9%9F%B3%E8%89%B2%E5%88%97%E8%A1%A8)
---------------------------------------------------------------------------------------------------------------------------

`GET /v1/speakers/list`

获取所有可用的音色（包含克隆音色），用于后续创建内容时选择音色。

**请求示例**：

```
# 获取所有中文音色
curl -X GET "https://api.marswave.ai/openapi/v1/speakers/list?language=zh" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY"

# 获取所有英文音色
curl -X GET "https://api.marswave.ai/openapi/v1/speakers/list?language=en" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY"
```

```
const response = await fetch('https://api.marswave.ai/openapi/v1/speakers/list?language=zh', {
  headers: {
    'Authorization': `Bearer ${process.env.LISTENHUB_API_KEY}`,
  },
});
const data = await response.json();
console.log(data);
```

```
import os
import requests

response = requests.get(
    'https://api.marswave.ai/openapi/v1/speakers/list',
    headers={'Authorization': f'Bearer {os.environ["LISTENHUB_API_KEY"]}'},
    params={'language': 'zh'}
)
data = response.json()
print(data)
```

**响应示例**：

```
{
  "code": 0,
  "message": "",
  "data": {
    "items": [
      {
        "name": "原野",
        "speakerId": "CN-Man-Beijing-V2",
        "demoAudioUrl": "https://example.com/demo-male.mp3",
        "gender": "male",
        "language": "zh"
      },
      {
        "name": "晓曼",
        "speakerId": "chat-girl-105-cn",
        "demoAudioUrl": "https://example.com/demo-female.mp3",
        "gender": "female",
        "language": "zh"
      }
    ]
  }
}
```

* * *
