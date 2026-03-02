$ErrorActionPreference='Stop'
$tmp = Join-Path $env:TEMP 'poly_trades.json'
& curl.exe "https://data-api.polymarket.com/trades?limit=1000" -o $tmp | Out-Null
$trades = Get-Content $tmp -Raw | ConvertFrom-Json

$markets = @()
for($offset=0; $offset -lt 5000; $offset += 500){
  $url = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=500&offset=$offset"
  $chunk = Invoke-RestMethod -Uri $url -TimeoutSec 40
  if(-not $chunk -or $chunk.Count -eq 0){ break }
  $markets += $chunk
  if($chunk.Count -lt 500){ break }
}

$marketBySlug = @{}
foreach($m in $markets){ if($m.slug){ $marketBySlug[$m.slug] = $m } }

function Get-WalletAgeDays($name){
  if($name -match '-(\d{13})$'){
    $ms=[int64]$Matches[1]
    $created=[DateTimeOffset]::FromUnixTimeMilliseconds($ms).UtcDateTime
    return [math]::Round((((Get-Date).ToUniversalTime()) - $created).TotalDays,2)
  }
  return $null
}

$rows=@()
foreach($t in $trades){
  $amount = [math]::Round(([double]$t.size * [double]$t.price),2)
  $walletAge = Get-WalletAgeDays $t.name
  $m = $null
  if($t.slug -and $marketBySlug.ContainsKey($t.slug)){ $m = $marketBySlug[$t.slug] }

  $odds = $null
  if($m -and $m.lastTradePrice){ $odds = [double]$m.lastTradePrice }
  elseif($t.price){ $odds = [double]$t.price }

  $end = $null
  if($m){ $end = $m.endDate }

  $chg = 0.0
  if($m -and $m.oneHourPriceChange){ $chg = [double]$m.oneHourPriceChange }

  $score = 0
  $reasons = @()
  if([math]::Abs($chg) -gt 0.02){ $score += 30; $reasons += '+30 impact>2%' }
  if($odds -ne $null -and $odds -ge 0.01 -and $odds -le 0.20){ $score += 12; $reasons += '+12 low-odds(1%-20%)' }
  if($walletAge -ne $null -and $walletAge -lt 5){ $score += 15; $reasons += '+15 new-wallet(<5d)' }
  if($amount -gt 3000){ $score += 10; $reasons += '+10 order>$3000' }

  if($score -ge 20){
    $rows += [pscustomobject]@{
      event = $t.title
      amount = $amount
      orderTime = ([DateTimeOffset]::FromUnixTimeSeconds([int64]$t.timestamp).ToOffset([TimeSpan]::FromHours(8)).ToString('yyyy-MM-dd HH:mm:ss'))
      odds = $(if($odds -ne $null){ [math]::Round($odds,4) } else { $null })
      endTime = $end
      hitReasons = ($reasons -join '; ')
      score = $score
      wallet = $t.proxyWallet
      link = $(if($t.slug){ "https://polymarket.com/event/$($t.slug)" } else { '' })
    }
  }
}

$top = $rows | Sort-Object -Property @{Expression='score';Descending=$true}, @{Expression='amount';Descending=$true} | Select-Object -First 15
$reportDir = 'C:\Users\Administrator\.openclaw\workspace\reports'
if(!(Test-Path $reportDir)){ New-Item -ItemType Directory -Path $reportDir | Out-Null }
$out = Join-Path $reportDir ("polymarket_fullscan_{0}.json" -f (Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'))
$top | ConvertTo-Json -Depth 6 | Set-Content -Path $out -Encoding UTF8
Write-Output "OUT=$out"
Write-Output ("COUNT_TOTAL={0} COUNT_TOP={1}" -f $rows.Count, $top.Count)
