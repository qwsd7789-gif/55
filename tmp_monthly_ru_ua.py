import pandas as pd
import yfinance as yf
from urllib.request import urlopen
import io

def to_series(df):
    if isinstance(df, pd.Series):
        return df
    if 'Adj Close' in df.columns:
        s = df['Adj Close']
    else:
        s = df['Close']
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:,0]
    return s
start = '2022-02-01'
end = '2024-03-01'
sp = to_series(yf.download('^GSPC', start=start, end=end, auto_adjust=False, progress=False))
oil = to_series(yf.download('CL=F', start=start, end=end, auto_adjust=False, progress=False))
sp.index = pd.to_datetime(sp.index)
oil.index = pd.to_datetime(oil.index)
raw = urlopen('https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL').read().decode('utf-8', errors='ignore')
cpi = pd.read_csv(io.StringIO(raw))
date_col = 'DATE' if 'DATE' in cpi.columns else 'observation_date'
cpi[date_col] = pd.to_datetime(cpi[date_col])
cpi['CPIAUCSL'] = pd.to_numeric(cpi['CPIAUCSL'], errors='coerce')
cpi = cpi.set_index(date_col)['CPIAUCSL']
cpi_yoy = cpi.pct_change(12) * 100
months = pd.period_range('2022-03', '2024-02', freq='M')
rows = []
for m in months:
    month_end = m.to_timestamp(how='end').normalize()
    oil_val = float(oil[:month_end].dropna().iloc[-1])
    sp_val = float(sp[:month_end].dropna().iloc[-1])
    cpi_month = pd.Timestamp(f'{m.year}-{m.month:02d}-01')
    cpi_val = float(cpi_yoy[:cpi_month].dropna().iloc[-1])
    rows.append({
        '月份': str(m),
        'WTI原油(美元/桶)': round(oil_val, 2),
        '美国CPI同比(%)': round(cpi_val, 1),
        '标普500': round(sp_val, 0),
    })

df = pd.DataFrame(rows)
print(df.to_csv(index=False))
