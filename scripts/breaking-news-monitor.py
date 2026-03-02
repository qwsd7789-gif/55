#!/usr/bin/env python3
"""
突发财经新闻检测脚本
- 抓取多个 RSS 源
- 过滤黄金/油价/数字货币相关新闻
- AI 分析和翻译
- 推送到用户
"""

import feedparser
import json
import hashlib
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests

# Windows 编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# RSS 源配置
RSS_SOURCES = {
    "Al Jazeera": {
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "priority": "high",
        "region": "MENA"
    },
    "Reuters": {
        "url": "https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best", 
        "priority": "high",
        "region": "Global"
    },
    "CoinDesk": {
        "url": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml",
        "priority": "high",
        "region": "Crypto"
    },
    "OilPrice": {
        "url": "https://oilprice.com/rss/oilprice.xml",
        "priority": "high", 
        "region": "Energy"
    },
    "Kitco": {
        "url": "https://www.kitco.com/rss/gold-news.xml",
        "priority": "high",
        "region": "Metals"
    }
}

# 关键词映射
ASSET_KEYWORDS = {
    "黄金": ["gold", "XAU", "XAUUSD", "precious metal", "贵金属"],
    "原油": ["oil", "crude", "WTI", "Brent", "petroleum", "油价", "原油"],
    "数字货币": ["bitcoin", "BTC", "ethereum", "ETH", "crypto", "cryptocurrency", "数字货币", "加密货币"]
}

HIGH_IMPACT_KEYWORDS = [
    "breaking", "突发", "urgent", "紧急",
    "federal reserve", "fed", "interest rate", "利率",
    "war", "conflict", "geopolitical", "middle east", "中东",
    "inflation", "CPI", "recession", "制裁", "sanctions",
    "attack", "轰炸", "explosion", "爆炸"
]

class BreakingNewsMonitor:
    def __init__(self):
        self.workspace = os.path.expanduser("~/.openclaw/workspace")
        self.history_file = os.path.join(self.workspace, "memory", "breaking-news-history.json")
        self._load_history()
    
    def _load_history(self):
        """加载已发送新闻历史"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = {}
    
    def _save_history(self):
        """保存新闻历史"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def _get_article_id(self, title: str, link: str) -> str:
        """生成文章唯一 ID"""
        content = f"{title}|{link}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _is_duplicate(self, article_id: str) -> bool:
        """检查是否已发送过"""
        if article_id in self.history:
            sent_time = datetime.fromisoformat(self.history[article_id])
            # 48 小时内不重复发送
            if datetime.now() - sent_time < timedelta(hours=48):
                return True
        return False
    
    def _detect_assets(self, title: str, summary: str) -> List[str]:
        """检测涉及哪些资产"""
        text = f"{title} {summary}".lower()
        assets = []
        for asset, keywords in ASSET_KEYWORDS.items():
            if any(kw.lower() in text for kw in keywords):
                assets.append(asset)
        return assets
    
    def _is_high_impact(self, title: str, summary: str) -> bool:
        """判断是否高影响力新闻"""
        text = f"{title} {summary}".lower()
        return any(kw.lower() in text for kw in HIGH_IMPACT_KEYWORDS)
    
    def _translate_with_ai(self, text: str) -> str:
        """使用 AI 翻译（简化版，实际使用时可调用外部 API）"""
        # 这里预留 AI 翻译接口
        # 实际实现可以调用 Gemini / Kimi / OpenAI
        return f"[AI翻译] {text}"
    
    def fetch_rss(self, source_name: str, source_config: dict) -> List[Dict]:
        """抓取单个 RSS 源"""
        try:
            feed = feedparser.parse(source_config["url"])
            articles = []
            for entry in feed.entries[:10]:  # 只取最新的 10 条
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "published": entry.get("published", ""),
                    "source": source_name,
                    "priority": source_config["priority"],
                    "region": source_config.get("region", "Global")
                })
            return articles
        except Exception as e:
            print(f"Error fetching {source_name}: {e}")
            return []
    
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """处理并过滤文章"""
        results = []
        for article in articles:
            article_id = self._get_article_id(article["title"], article["link"])
            
            # 检查重复
            if self._is_duplicate(article_id):
                continue
            
            # 检测资产类型
            assets = self._detect_assets(article["title"], article["summary"])
            
            # 判断影响力
            is_high_impact = self._is_high_impact(article["title"], article["summary"])
            
            # 只保留涉及目标资产或高影响力的新闻
            if assets or is_high_impact:
                article["id"] = article_id
                article["assets"] = assets
                article["is_high_impact"] = is_high_impact
                article["detected_at"] = datetime.now().isoformat()
                results.append(article)
                
                # 记录到历史
                self.history[article_id] = datetime.now().isoformat()
        
        return results
    
    def format_output(self, article: Dict) -> str:
        """格式化输出"""
        asset_emojis = {
            "黄金": "🟡",
            "原油": "🛢️", 
            "数字货币": "💰"
        }
        
        asset_str = " ".join([f"{asset_emojis.get(a, '📊')}{a}" for a in article["assets"]])
        
        priority_emoji = "🔴" if article["priority"] == "high" else "🟡"
        
        output = f"""
{priority_emoji} **突发财经新闻** | {article['detected_at'][:16]}

📰 **标题** (原文)
{article['title']}

📊 **影响资产**: {asset_str if asset_str else '📊 综合市场'}
📍 **来源**: {article['source']} ({article['region']})
🔗 **链接**: {article['link']}

---
📝 **摘要** (原文)
{article['summary'][:300]}...

🤖 **AI 分析**:
- 影响程度: {"⚠️ 高" if article['is_high_impact'] else "📌 中/低"}
- 涉及资产: {', '.join(article['assets']) if article['assets'] else '市场整体'}
- 建议关注: 请结合市场走势谨慎决策
"""
        return output
    
    def run(self):
        """主运行函数"""
        all_articles = []
        
        print(f"🔄 开始检查突发新闻... {datetime.now()}")
        
        # 抓取所有 RSS 源
        for source_name, config in RSS_SOURCES.items():
            print(f"📡 正在抓取: {source_name}...")
            articles = self.fetch_rss(source_name, config)
            all_articles.extend(articles)
        
        # 处理和过滤
        filtered = self.process_articles(all_articles)
        
        # 保存历史
        self._save_history()
        
        # 输出结果
        if filtered:
            print(f"\n🚨 发现 {len(filtered)} 条高影响力新闻:\n")
            for article in filtered:
                output = self.format_output(article)
                print(output)
                print("\n" + "="*60 + "\n")
        else:
            print("✅ 暂无新的高影响力财经新闻")
        
        return filtered


if __name__ == "__main__":
    monitor = BreakingNewsMonitor()
    monitor.run()
