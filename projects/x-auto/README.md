# X Auto Pilot (Hourly)

## Goal
- Monitor non-Chinese X accounts on: Middle East / Crypto / US Stocks / AI
- Every hour: fetch -> dedupe -> score -> rewrite in your voice -> queue 1 post

## Current Status
- ✅ Watchlist prepared: `watchlist.en.json`
- ✅ Persona template prepared: `persona.prompt.md`
- ✅ Pipeline config prepared: `config.sample.json`
- ⚠️ Auto publish pending X connector auth (`infsh` environment not ready yet)

## Hourly Flow
1. Pull headlines from OpenNews + account feeds
2. Remove duplicates and low-score items (<70)
3. Rewrite into your style (fact -> view -> why it matters)
4. Push top 1 into posting queue
5. Publish automatically once X connector is available

## Post Template
- EN Headline
- ZH Insight
- Why it matters (EN)

## Next Step
- Finish X publish connector setup (inference.sh / x integration)
- Switch from queue mode to full auto publish mode
