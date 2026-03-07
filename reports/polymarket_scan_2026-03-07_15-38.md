# Polymarket Hourly Scan
- Time: 2026-03-07 15:38:03 +08:00
- Thresholds: walletAge<5 d; order>3000; priceImpact>2%; nearEnd<60 min

## Result
- Active markets scanned: 5000
- Near-end + >2% 1h price move hits: 3

## Hits
1. Will St. Johnâs win the 2025-2026 Big East Menâs Basketball regular season championship?
   - Mins left: 21.9
   - 1h change: -0.025
   - Last price: 0.999
   - 24h volume: 52411.778632000016
   - Link: https://polymarket.com/event/will-st-johns-win-the-2025-2026-big-east-mens-basketball-regular-season-championship
2. Will UConn win the 2025-2026 Big East Menâs Basketball regular season championship?
   - Mins left: 21.9
   - 1h change: -0.06
   - Last price: 0.013
   - 24h volume: 14544.283657000004
   - Link: https://polymarket.com/event/will-uconn-win-the-2025-2026-big-east-mens-basketball-regular-season-championship
3. Will another team win the 2025-2026 Big East Menâs Basketball regular season championship?
   - Mins left: 21.9
   - 1h change: -0.091
   - Last price: 0.001
   - 24h volume: 1139.92
   - Link: https://polymarket.com/event/will-another-team-win-the-2025-2026-big-east-mens-basketball-regular-season-championship

## Data-Limit Note
Public endpoint currently does not expose per-wallet age or per-order notional in this script path; wallet-age<5d and order> checks require wallet/trade stream integration (CLOB authenticated/API indexer).
