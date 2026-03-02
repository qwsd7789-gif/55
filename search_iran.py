import os
import json
import urllib.request
from datetime import datetime

token = os.environ.get('OPENNEWS_TOKEN', '')
url = 'https://ai.6551.io/open/news_search'

data = json.dumps({'q': 'Iran', 'limit': 15, 'page': 1}).encode()
req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Authorization', 'Bearer ' + token)
req.add_header('Content-Type', 'application/json')

resp = urllib.request.urlopen(req, timeout=20)
result = json.loads(resp.read().decode())

with open('C:/Users/Administrator/.openclaw/workspace/iran_news_output.txt', 'w', encoding='utf-8') as f:
    f.write('🔥 伊朗 × 数字货币 最新热门新闻\n')
    f.write('=' * 60 + '\n')
    for item in result.get('data', []):
        ai = item.get('aiRating', {})
        score = ai.get('score', 'N/A')
        grade = ai.get('grade', 'N/A')
        ts = item.get('ts', 0)
        date = datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d') if ts else 'Unknown'
        f.write(f'\n📅 {date} | AI评分: {score} | 等级: {grade}\n')
        f.write(f'📰 {item.get("text", "")}\n')
        f.write(f'🔗 {item.get("link", "")}\n')
        f.write('-' * 40 + '\n')

print('Done')
