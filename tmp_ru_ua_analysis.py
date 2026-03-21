import pandas as pd
import yfinance as yf
from urllib.request import urlopen
import io
war_start = pd.Timestamp('202-02-24')
start = '202-02-01'
end = '2024-03-31'
sp = yf.download('^GSPC', start=start, end=end, auto_adjust=False, progress=False)
oil = yf.download('CL=F', start=start, end=end, auto_adjust=False, progress=False)
sp = sp['Adj Close'] if 'Adj Close' in sp else sp['Close']
oil = oil['Adj Close'] if 'Adj Close' in oil else oil['Close']
raw = urlopen('https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL').read().decode('utf-8', errors='ignore')
cpi = pd.read_csv(io.StringIO(raw))
date_col = 'DATE' if 'DATE' in cpi.columns else 'observation_date'
val_col = 'CPIAUCSL'
cpi[date_col]=pd.to_datetime(cpi[date_col])
cpi[val_col]=pd.to_numeric(cpi[val_col], errors='coerce')
cpi=cpi.set_index(date_col)[val_col]
cpi_yoy = cpi.pct_change(12)*100
points = [
    ('开战时', pd.Timestamp('202-02-24')),
    ('202Q1', pd.Timestamp('202-03-31')),
    ('202Q2', pd.Timestamp('202-06-30')),
    ('202Q3', pd.Timestamp('202-09-30')),
    ('202Q4', pd.Timestamp('202-12-30')),
    ('2023Q1', pd.Timestamp('2023-03-31')),
    ('2023Q2', pd.Timestamp('2023-06-30')),
    ('2023Q3', pd.Timestamp('2023-09-29')),
    ('2023Q4', pd.Timestamp('2023-12-29')),
    ('两年后附近', pd.Timestamp('2024-02-29')),
]
base_oil = float(oil[:war_start].dropna().iloc[-1])
base_sp = float(sp[:war_start].dropna().iloc[-1])
base_cpi = float(cpi_yoy[:war_start].dropna().iloc[-1])
rows=[]
for label, d in points:
    o = float(oil[:d].dropna().iloc[-1])
    s = float(sp[:d].dropna().iloc[-1])
    cy = float(cpi_yoy[:d].dropna().iloc[-1])
    rows.append({
        '阶段': label,
        '日期': str(d.date()),
        'WTI原油(美元/桶)': round(o,2),
        '油价较开战变动%': round((o/base_oil-1)*100,1),
        '美国CPI同比%': round(cy,1),
        'CPI较开战变化pp': round(cy-base_cpi,1),
        '标普500': round(s,0),
        '标普较开战变动%': round((s/base_sp-1)*100,1),
    })

df = pd.DataFrame(rows)
print('BASE')
print(f'oil={base_oil:.2f}, cpi_yoy={base_cpi:.1f}, spx={base_sp:.0f}')
print('TABLE_CSV')
print(df.to_csv(index=False))
