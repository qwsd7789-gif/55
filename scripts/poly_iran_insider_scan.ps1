$ErrorActionPreference='Stop'
$keywords = @('iran','israel','gaza','hamas','hezbollah','khamenei','hormuz','middle east','tehran','lebanon','idf','iranian','israeli','tanker','oil')
$minAmount = 2000

$all = @()
for($i=0; $i -lt 12; $i++){
  $offset = $i * 1000
  $url = "https://data-api.polymarket.com/trades?limit=1000&offset=$offset"
  try { $batch = Invoke-RestMethod -Uri $url -TimeoutSec 45 } catch { break }
  if(-not $batch -or $batch.Count -eq 0){ break }
  $all += $batch
}

$marketCache = @{}
function Get-Market($slug){
  if(-not $slug){ return $null }
  if($marketCache.ContainsKey($slug)){ return $marketCache[$slug] }
  try {
    $m = Invoke-RestMethod -Uri ("https://gamma-api.polymarket.com/markets?slug=" + $slug) -TimeoutSec 30
    if($m -and $m.Count -gt 0){ $marketCache[$slug] = $m[0]; return $m[0] }
  } catch {}
  $marketCache[$slug] = $null
  return $null
}

function WalletAgeDays($name){
  if($name -and ($name -match '-(\d{13})$')){
    $ms=[int64]$Matches[1]
    $created=[DateTimeOffset]::FromUnixTimeMilliseconds($ms).UtcDateTime
    return [math]::Round((((Get-Date).ToUniversalTime())-$created).TotalDays,2)
  }
  return $null
}

$walletFirst = @{}
foreach($t in $all | Sort-Object timestamp){
  $w=[string]$t.proxyWallet
  if(-not $walletFirst.ContainsKey($w)){ $walletFirst[$w]=[int64]$t.timestamp }
}

$rows=@()
foreach($t in $all){
  $title = [string]$t.title
  $titleLower = $title.ToLower()
  $match = $false
  foreach($k in $keywords){ if($titleLower.Contains($k)){ $match = $true; break } }
  if(-not $match){ continue }

  $amount = [math]::Round(([double]$t.size * [double]$t.price),2)
  if($amount -lt $minAmount){ continue }

  $m = Get-Market $t.slug
  $odds = if($m -and $m.lastTradePrice){ [double]$m.lastTradePrice } else { [double]$t.price }
  $impact = if($m -and $m.oneHourPriceChange){ [double]$m.oneHourPriceChange } else { 0.0 }
  $endUtc = if($m -and $m.endDate){ [datetime]$m.endDate } else { $null }
  $tradeUtc = [DateTimeOffset]::FromUnixTimeSeconds([int64]$t.timestamp).UtcDateTime

  $score=0; $reasons=@()
  if([math]::Abs($impact) -gt 0.02){ $score += 30; $reasons += '+30 impact>2%' }
  if($odds -ge 0.01 -and $odds -le 0.20){ $score += 12; $reasons += '+12 low-odds(1%-20%)+heavy' }
  $age = WalletAgeDays $t.name
  if($age -ne $null -and $age -lt 5){ $score += 15; $reasons += '+15 new-wallet(<5d)' }
  if($walletFirst[[string]$t.proxyWallet] -eq [int64]$t.timestamp){ $score += 10; $reasons += '+10 first-order-heavy(sampled)' }
  if($endUtc){ $mins=($endUtc-$tradeUtc).TotalMinutes; if($mins -ge 0 -and $mins -le 60){ $score += 5; $reasons += '+5 near-end(<60m)' } }

  $rows += [pscustomobject]@{
    event = $title
    amountUSD = $amount
    orderTimeCN = ([DateTimeOffset]$tradeUtc).ToOffset([TimeSpan]::FromHours(8)).ToString('yyyy-MM-dd HH:mm:ss')
    odds = [math]::Round($odds,4)
    endTimeCN = $(if($endUtc){ ([DateTimeOffset]$endUtc).ToOffset([TimeSpan]::FromHours(8)).ToString('yyyy-MM-dd HH:mm:ss') } else { '-' })
    wallet = $t.proxyWallet
    hitReasons = $(if($reasons.Count){$reasons -join '; '} else {'-'})
    score = $score
    link = "https://polymarket.com/event/$($t.slug)"
  }
}

$final = $rows | Sort-Object -Property @{Expression='score';Descending=$true}, @{Expression='amountUSD';Descending=$true} | Select-Object -First 20
$out = "C:\Users\Administrator\.openclaw\workspace\reports\poly_iran_insider_" + (Get-Date -Format 'yyyy-MM-dd_HH-mm-ss') + ".json"
$final | ConvertTo-Json -Depth 6 | Set-Content -Path $out -Encoding UTF8
Write-Output "OUT=$out"
Write-Output ("ALL_TRADES=" + $all.Count)
Write-Output ("MATCHES=" + $final.Count)
