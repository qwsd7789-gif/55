# Polymarket Hourly Scan
- Time: 2026-03-08 15:38:06 +08:00
- Thresholds: walletAge<5 d; order>3000; priceImpact>2%; nearEnd<60 min

## Result
- Active markets scanned: 5000
- Near-end + >2% 1h price move hits: 2

## Hits
1. Will CDU win the most seats in the 2026 Baden-WÃ¼rttemberg parliamentary elections?
   - Mins left: 21.9
   - 1h change: -0.032
   - Last price: 0.51
   - 24h volume: 108804.87624599999
   - Link: https://polymarket.com/event/will-cdu-win-the-most-seats-in-the-2026-baden-wrttemberg-parliamentary-elections
2. Will The Greens win the most seats in the 2026 Baden-WÃ¼rttemberg parliamentary elections?
   - Mins left: 21.9
   - 1h change: 0.029
   - Last price: 0.489
   - 24h volume: 82183.39157599995
   - Link: https://polymarket.com/event/will-the-greens-win-the-most-seats-in-the-2026-baden-wrttemberg-parliamentary-elections

## Data-Limit Note
Public endpoint currently does not expose per-wallet age or per-order notional in this script path; wallet-age<5d and order> checks require wallet/trade stream integration (CLOB authenticated/API indexer).
