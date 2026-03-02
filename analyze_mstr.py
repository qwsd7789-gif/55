import sys
sys.path.insert(0, r'C:\Users\Administrator\.openclaw\skills\finance-toolkit')
from finance_toolkit import FinanceToolkit

toolkit = FinanceToolkit()

print("=" * 60)
print("MSTR (MicroStrategy) 股票分析报告")
print("=" * 60)

# 1. 获取基本信息
print("\n📊 基本信息")
print("-" * 40)
info = toolkit.get_stock_info('MSTR')
if info:
    print(f"公司名称: {info['name']}")
    print(f"当前价格: ${info['current_price']:.2f}")
    print(f"涨跌: {info['change_percent']:.2f}%")
    print(f"市值: ${info['market_cap']:,.0f}")
    print(f"市盈率: {info['pe_ratio']:.2f}")
    print(f"行业: {info['industry']}")
    print(f"货币: {info['currency']}")

# 2. 综合分析
print("\n📈 综合分析")
print("-" * 40)
analysis = toolkit.analyze_stock('MSTR', period='3mo')
if analysis and 'error' not in analysis:
    basic = analysis['basic_info']
    price = analysis['price_analysis']
    technical = analysis['technical_analysis']
    risk = analysis['risk_analysis']
    recommendation = analysis['recommendation']
    
    print(f"\n💰 价格分析:")
    print(f"  当前价格: ${price['current_price']:.2f}")
    print(f"  价格变动: {price['price_change_percent']:.2f}%")
    print(f"  52周最高: ${price['high_52w']:.2f}")
    print(f"  52周最低: ${price['low_52w']:.2f}")
    print(f"  当前距高点: {price['current_vs_high']:.1f}%")
    print(f"  当前距低点: {price['current_vs_low']:.1f}%")
    print(f"  成交量趋势: {price['volume_trend']}")
    
    print(f"\n📉 技术分析:")
    print(f"  趋势: {technical['trend']}")
    print(f"  RSI: {technical['rsi']:.2f} ({technical['rsi_signal']})")
    print(f"  MACD信号: {technical['macd_signal']}")
    print(f"  布林带: {technical['bb_signal']}")
    ma_pos = technical['ma_position']
    print(f"  均线位置: 高于MA5={ma_pos['above_ma5']}, 高于MA20={ma_pos['above_ma20']}, 高于MA60={ma_pos['above_ma60']}")
    
    print(f"\n⚠️ 风险分析:")
    print(f"  风险等级: {risk['risk_level']}")
    print(f"  年化波动率: {risk['annual_volatility']:.2%}")
    print(f"  最大回撤: {risk['max_drawdown']:.2%}")
    print(f"  夏普比率: {risk['sharpe_ratio']:.2f}")
    
    print(f"\n🎯 投资建议:")
    print(f"  操作建议: 【{recommendation['action']}】")
    print(f"  信心指数: {recommendation['confidence']:.2f}/1.0")
    print(f"  建议期限: {recommendation['time_horizon']}")
    print(f"\n  详细建议:")
    for detail in recommendation['details']:
        print(f"    • {detail}")

# 3. MSTR 特殊说明
print("\n" + "=" * 60)
print("💡 MSTR (MicroStrategy) 特别提示")
print("=" * 60)
print("""
MSTR 是一家特殊的公司:
• 主营业务: 企业软件 + 比特币投资
• 持仓: 持有超过 20 万枚 BTC（全球最大企业持仓）
• 股价特性: 与比特币价格高度相关
• 波动性: 通常比 BTC 波动更大（杠杆效应）

分析 MSTR 时需同时关注:
1. 比特币价格走势
2. 公司基本面（软件业务）
3. 监管政策对加密货币的影响
""")

print("\n" + "=" * 60)
print("报告生成完成")
print("=" * 60)
