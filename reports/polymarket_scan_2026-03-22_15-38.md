# Polymarket Hourly Scan
- Time: 2026-03-22 15:38:01 +08:00
- Thresholds: walletAge<5 d; order>3000; priceImpact>2%; nearEnd<60 min

## Result
- Active markets scanned: 5000
- Near-end + >2% 1h price move hits: 1

## Hits
1. Will SPD win the most seats in the 2026 Rhineland-Palatinate parliamentary elections?
   - Mins left: 22
   - 1h change: -0.02
   - Last price: 0.37
   - 24h volume: 20449.613314000002
   - Link: https://polymarket.com/event/will-spd-win-the-most-seats-in-the-2026-rhineland-palatinate-parliamentary-elections

## Data-Limit Note
Public endpoint currently does not expose per-wallet age or per-order notional in this script path; wallet-age<5d and order> checks require wallet/trade stream integration (CLOB authenticated/API indexer).
