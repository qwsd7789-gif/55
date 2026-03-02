import urllib.request
import json
import os
from datetime import datetime

url = 'https://ai.6551.io/open/news_search'
token = os.environ.get('OPENNEWS_TOKEN', '')

data = json.dumps({'q': 'Iran cryptocurrency', 'limit': 15, 'page': 1}).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Authorization', f'Bearer {token}')
req.add_header('Content-Type', 'application/json')

try:
    resp = urllib.request.urlopen(req, timeout=20)
    result = json.loads(resp.read().decode('utf-8'))
    
    print('🔥 伊朗 × 数字货币 最新热门新闻')
    print('=' * 60)
    
    for item in result.get('data', []):
        ai = item.get('aiRating', {})
        score = ai.get('score', 'N/A')
        grade = ai.get('grade', 'N/A')
        signal = ai.get('signal', 'N/A')
        ts = item.get('ts', 0)
        date = datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M') if ts else 'Unknown'
        
        print(f'\n📅 {date}')
        print(f'🎯 AI评分: {score}/100 | 等级: {grade} | 信号: {signal}')
        print(f'📰 {item.get("text", "")}')
        print(f'🔗 {item.get("link", "")}')
        print(f'📡 来源: {item.get("newsType", "")}')
        coins = item.get('coins', [])
        if coins:
            print(f'💰 相关币种: {", ".join([c.get("symbol", "") for c in coins])}')
        print('-' * 60)
except Exception as e:
    print(f'Error: {e}')
