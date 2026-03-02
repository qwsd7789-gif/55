$ErrorActionPreference = 'Stop'
$now = Get-Date
$utcNow = (Get-Date).ToUniversalTime()

# User thresholds
$walletAgeDays = 5
$minOrderUsd = 3000
$impactThreshold = 0.02
$nearEndMinutes = 60

# Fetch active markets (public Gamma API)
$all = @()
for($offset=0; $offset -lt 5000; $offset += 500){
  $url = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=500&offset=$offset"
  $chunk = Invoke-RestMethod -Uri $url -TimeoutSec 40
  if(-not $chunk -or $chunk.Count -eq 0){ break }
  $all += $chunk
  if($chunk.Count -lt 500){ break }
}

$nearEnd = @()
foreach($m in $all){
  if(-not $m.endDate){ continue }
  $minsLeft = ([datetime]$m.endDate - $utcNow).TotalMinutes
  if($minsLeft -gt 0 -and $minsLeft -le $nearEndMinutes){
    $impact1h = [math]::Abs([double]($m.oneHourPriceChange | ForEach-Object { if($_){$_} else {0} }))
    if($impact1h -ge $impactThreshold){
      $nearEnd += [pscustomobject]@{
        id = $m.id
        question = $m.question
        endDate = $m.endDate
        minsLeft = [math]::Round($minsLeft,1)
        lastTradePrice = $m.lastTradePrice
        oneHourPriceChange = $m.oneHourPriceChange
        volume24hr = $m.volume24hr
        liquidity = $m.liquidity
        url = "https://polymarket.com/event/$($m.slug)"
      }
    }
  }
}

$reportDir = "C:\Users\Administrator\.openclaw\workspace\reports"
if(!(Test-Path $reportDir)){ New-Item -ItemType Directory -Path $reportDir | Out-Null }
$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$path = Join-Path $reportDir "polymarket_scan_$stamp.md"

$lines = @()
$lines += "# Polymarket Hourly Scan"
$lines += "- Time: $($now.ToString('yyyy-MM-dd HH:mm:ss zzz'))"
$lines += "- Thresholds: walletAge<$walletAgeDays d; order>$minOrderUsd; priceImpact>2%; nearEnd<$nearEndMinutes min"
$lines += ""
$lines += "## Result"
$lines += "- Active markets scanned: $($all.Count)"
$lines += "- Near-end + >2% 1h price move hits: $($nearEnd.Count)"
$lines += ""
if($nearEnd.Count -gt 0){
  $lines += "## Hits"
  $i=1
  foreach($h in $nearEnd | Select-Object -First 20){
    $lines += "$i. $($h.question)"
    $lines += "   - Mins left: $($h.minsLeft)"
    $lines += "   - 1h change: $($h.oneHourPriceChange)"
    $lines += "   - Last price: $($h.lastTradePrice)"
    $lines += "   - 24h volume: $($h.volume24hr)"
    $lines += "   - Link: $($h.url)"
    $i++
  }
}else{
  $lines += "No hit in this run."
}

$lines += ""
$lines += "## Data-Limit Note"
$lines += "Public endpoint currently does not expose per-wallet age or per-order notional in this script path; wallet-age<5d and order>$3000 checks require wallet/trade stream integration (CLOB authenticated/API indexer)."

$lines -join "`r`n" | Set-Content -Path $path -Encoding UTF8
Write-Output "REPORT=$path"
