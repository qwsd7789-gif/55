import feedparser

print('=== CoinDesk 最新 ===')
feed = feedparser.parse('https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml')
for i, entry in enumerate(feed.entries[:5], 1):
    title = entry.get('title', '')
    link = entry.get('link', '')
    print(f'{i}. {title}')
    print(f'   {link}\n')

print('\n=== Reuters 最新 ===')
feed = feedparser.parse('https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best')
for i, entry in enumerate(feed.entries[:5], 1):
    title = entry.get('title', '')
    link = entry.get('link', '')
    print(f'{i}. {title}')
    print(f'   {link}\n')
