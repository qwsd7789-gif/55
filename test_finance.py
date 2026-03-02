import sys
sys.path.insert(0, r'C:\Users\Administrator\.openclaw\skills\finance-toolkit')
from finance_toolkit import FinanceToolkit

toolkit = FinanceToolkit()
info = toolkit.get_stock_info('AAPL')
if info:
    print(f"名称: {info['name']}")
    print(f"价格: ${info['current_price']:.2f}")
    print(f"涨跌: {info['change_percent']:.2f}%")
    print(f"市值: ${info['market_cap']:,.0f}")
    print(f"市盈率: {info['pe_ratio']:.2f}")
else:
    print("获取失败")
