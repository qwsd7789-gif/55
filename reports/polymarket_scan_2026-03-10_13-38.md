# Polymarket Hourly Scan
- Time: 2026-03-10 13:38:02 +08:00
- Thresholds: walletAge<5 d; order>3000; priceImpact>2%; nearEnd<60 min

## Result
- Active markets scanned: 5000
- Near-end + >2% 1h price move hits: 0

No hit in this run.

## Data-Limit Note
Public endpoint currently does not expose per-wallet age or per-order notional in this script path; wallet-age<5d and order> checks require wallet/trade stream integration (CLOB authenticated/API indexer).
