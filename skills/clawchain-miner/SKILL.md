# ClawChain 自动挖矿 Skill

ClawChain 通过 AI challenge 挖矿，脚本目录见 `scripts/`。

## 常用命令
- 首次初始化：`python scripts/setup.py --non-interactive`
- 开始挖矿：`python scripts/mine.py`
- 查看状态：`python scripts/status.py --chain`

## 说明
- 优先使用本地 solver；复杂题型会自动尝试 `OPENAI_API_KEY` / `GEMINI_API_KEY` / `ANTHROPIC_API_KEY`
- 默认 RPC 配置在 `scripts/config.json`
- 日志输出到 `data/mining_log.json`
