#!/usr/bin/env python
import feedparser

# 抓取 Al Jazeera 最新 RSS
feed = feedparser.parse('https://www.aljazeera.com/xml/rss/all.xml')

print('Al Jazeera 最新新闻 (Top 10)')
print('=' * 70)

iran_news = []
for i, entry in enumerate(feed.entries[:10], 1):
    title = entry.get('title', '')
    link = entry.get('link', '')
    summary = entry.get('summary', '')[:200]
    
    # 检查是否与伊朗相关
    keywords = ['iran', 'iranian', 'tehran', 'khamenei', 'israel', 'war', 'gaza', 'beirut', 'hezbollah']
    if any(kw in title.lower() or kw in summary.lower() for kw in keywords):
        iran_news.append({
            'title': title,
            'link': link,
            'summary': summary + '...' if len(summary) >= 200 else summary
        })
    
    print(f'{i}. {title}')
    print(f'   链接: {link}\n')

print('\n' + '=' * 70)
print(f'找到 {len(iran_news)} 条伊朗/中东相关新闻')
print()

for news in iran_news:
    print(f'** {news["title"]} **')
    print(f'   {news["summary"]}')
    print(f'   -> {news["link"]}')
    print()
