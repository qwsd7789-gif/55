# 伊朗战争监控配置备份
# 备份时间: 2025-03-02 18:55

## 备份文件清单

| 文件名 | 说明 |
|--------|------|
| HEARTBEAT.md | 主监控配置文件，包含执行流程和简报模板 |
| iran-monitor-config.md | 监控任务详细配置 |
| MEMORY.md | 长期记忆，包含技能使用记录 |

## 监控配置摘要

### 信源
- 半岛电视台 (Al Jazeera) RSS
- BBC Middle East RSS
- 6551 OpenNews API (推特聚合)

### 监控关键词
- 冲突: Iran, Israel, Gaza, war, Khamenei, Hamas, Hezbollah
- 能源: oil, tanker, ship, Hormuz, Aramco
- 航运: Hormuz, Strait of Hormuz, shipping, maritime, port
- 地区: Qatar, UAE, Kuwait, Saudi, Cyprus, Lebanon

### 执行频率
每30分钟自动执行 (Heartbeat)

### API配置
- OPENNEWS_TOKEN: 已设置环境变量
- API端点: https://ai.6551.io/open/news_search

## 恢复方法
将备份文件复制回原目录:
```
C:/Users/Administrator/.openclaw/workspace/
```

## 历史备份
查看 backups/ 目录下其他时间戳文件夹
