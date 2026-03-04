$ErrorActionPreference='Stop'
$utcNow = (Get-Date).ToUniversalTime()
$weekAgo = $utcNow.AddDays(-7)
$minAmount = 2000

$allTrades = @()
$limit = 1000
for($i=0; $i -lt 40; $i++){
  $offset = $i * $limit
  $url = "https://data-api.polymarket.com/trades?limit=$limit&offset=$offset"
  try { $batch = Invoke-RestMethod -Uri $url -TimeoutSec 45 } catch { break }
  if(-not $batch -or $batch.Count -eq 0){ break }
  $allTrades += $batch
  $minTs = ($batch | Measure-Object -Property timestamp -Minimum).Minimum
  if($minTs -le ([DateTimeOffset]$weekAgo).ToUnixTimeSeconds()){ break }
}
if($allTrades.Count -eq 0){ throw 'No trade data returned.' }

$weekStartTs = ([DateTimeOffset]$weekAgo).ToUnixTimeSeconds()
$weekTrades = @()
foreach($t in $allTrades){
  if([int64]$t.timestamp -lt $weekStartTs){ continue }
  $amt = [double]$t.size * [double]$t.price
  if($amt -lt $minAmount){ continue }
  $weekTrades += $t
}

$marketCache = @{}
function Get-Market($slug){
  if(-not $slug){ return $null }
  if($marketCache.ContainsKey($slug)){ return $marketCache[$slug] }
  try{
    $m = Invoke-RestMethod -Uri ("https://gamma-api.polymarket.com/markets?slug=" + $slug) -TimeoutSec 30
    if($m -and $m.Count -gt 0){ $marketCache[$slug] = $m[0]; return $m[0] }
  } catch {}
  $marketCache[$slug] = $null
  return $null
}

$walletFirstTs = @{}
foreach($t in $allTrades | Sort-Object timestamp){
  $w = [string]$t.proxyWallet
  if(-not $walletFirstTs.ContainsKey($w)){ $walletFirstTs[$w] = [int64]$t.timestamp }
}

function Get-WalletAgeDays($name){
  if($name -and ($name -match '-(\d{13})$')){
    $ms = [int64]$Matches[1]
    $created = [DateTimeOffset]::FromUnixTimeMilliseconds($ms).UtcDateTime
    return [math]::Round(($utcNow - $created).TotalDays, 2)
  }
  return $null
}

$rows = @()
foreach($t in $weekTrades){
  $m = Get-Market $t.slug
  if(-not $m -or -not $m.endDate){ continue }
  $endUtc = [datetime]$m.endDate
  if($endUtc -gt $utcNow){ continue }
  if($endUtc -lt $weekAgo){ continue }

  $tradeUtc = [DateTimeOffset]::FromUnixTimeSeconds([int64]$t.timestamp).UtcDateTime
  $amount = [math]::Round(([double]$t.size * [double]$t.price),2)
  $odds = if($m.lastTradePrice){ [double]$m.lastTradePrice } else { [double]$t.price }
  $impact = if($m.oneHourPriceChange){ [double]$m.oneHourPriceChange } else { 0.0 }
  $walletAge = Get-WalletAgeDays $t.name

  $score = 0
  $reasons = @()
  if([math]::Abs($impact) -gt 0.02){ $score += 30; $reasons += '+30 impact>2%' }
  if($odds -ge 0.01 -and $odds -le 0.20 -and $amount -ge $minAmount){ $score += 12; $reasons += '+12 low-odds(1%-20%)+heavy' }
  if($walletAge -ne $null -and $walletAge -lt 5){ $score += 15; $reasons += '+15 new-wallet(<5d)' }
  if($walletFirstTs[[string]$t.proxyWallet] -eq [int64]$t.timestamp -and $amount -ge $minAmount){ $score += 10; $reasons += '+10 first-order-heavy(sampled)' }
  $minsToEnd = ($endUtc - $tradeUtc).TotalMinutes
  if($minsToEnd -ge 0 -and $minsToEnd -le 60){ $score += 5; $reasons += '+5 near-end(<60m)' }

  $rows += [pscustomobject]@{
    event = $t.title
    amountUSD = $amount
    orderTimeCN = ([DateTimeOffset]$tradeUtc).ToOffset([TimeSpan]::FromHours(8)).ToString('yyyy-MM-dd HH:mm:ss')
    odds = [math]::Round($odds,4)
    endTimeCN = ([DateTimeOffset]$endUtc).ToOffset([TimeSpan]::FromHours(8)).ToString('yyyy-MM-dd HH:mm:ss')
    hitReasons = ($(if($reasons.Count -gt 0){$reasons -join '; '} else {'-'}))
    score = $score
    wallet = $t.proxyWallet
    link = "https://polymarket.com/event/$($t.slug)"
  }
}

$final = $rows | Sort-Object -Property @{Expression='score';Descending=$true}, @{Expression='amountUSD';Descending=$true} | Select-Object -First 30

$reportDir = 'C:\Users\Administrator\.openclaw\workspace\reports'
if(!(Test-Path $reportDir)){ New-Item -ItemType Directory -Path $reportDir | Out-Null }
$stamp = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$jsonOut = Join-Path $reportDir ("polymarket_weekly_ended_$stamp.json")
$mdOut = Join-Path $reportDir ("polymarket_weekly_ended_$stamp.md")

$final | ConvertTo-Json -Depth 6 | Set-Content -Path $jsonOut -Encoding UTF8

$md = @()
$md += "# Polymarket Weekly Ended Markets (Amount > $minAmount)"
$md += ("- Generated: " + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))
$md += ("- Trades sampled: " + $allTrades.Count)
$md += ("- Qualified week trades: " + $weekTrades.Count)
$md += ("- Ended-within-week rows: " + $rows.Count)
$md += ""
$md += "| Event | Amount(USD) | Order Time(CN) | Odds | End Time(CN) | Hit Reasons | Score |"
$md += "|---|---:|---|---:|---|---|---:|"
foreach($r in $final){
  $event = ($r.event -replace '\|','/')
  $md += "| $event | $($r.amountUSD) | $($r.orderTimeCN) | $($r.odds) | $($r.endTimeCN) | $($r.hitReasons) | $($r.score) |"
}
$md += ""
$md += "Note: first-order-heavy is first seen in sampled data, not full-chain history."
$md -join "`r`n" | Set-Content -Path $mdOut -Encoding UTF8

Write-Output "JSON=$jsonOut"
Write-Output "MD=$mdOut"
Write-Output ("COUNTS all={0} weekQual={1} endedRows={2} final={3}" -f $allTrades.Count,$weekTrades.Count,$rows.Count,$final.Count)
