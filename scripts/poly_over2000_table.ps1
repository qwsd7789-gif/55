$ErrorActionPreference='Stop'
$minAmount=2000
$tmp = Join-Path $env:TEMP 'poly_trades_latest.json'
& curl.exe "https://data-api.polymarket.com/trades?limit=3000" -o $tmp | Out-Null
$trades = Get-Content $tmp -Raw | ConvertFrom-Json
$marketCache=@{}
function Get-Market($slug){ if(-not $slug){return $null}; if($marketCache.ContainsKey($slug)){return $marketCache[$slug]}; try{$m=Invoke-RestMethod -Uri ("https://gamma-api.polymarket.com/markets?slug="+$slug) -TimeoutSec 30; if($m -and $m.Count -gt 0){$marketCache[$slug]=$m[0]; return $m[0]}}catch{}; $marketCache[$slug]=$null; return $null }
function Get-WalletAgeDays($name){ if($name -and ($name -match '-(\d{13})$')){ $ms=[int64]$Matches[1]; $created=[DateTimeOffset]::FromUnixTimeMilliseconds($ms).UtcDateTime; return [math]::Round((((Get-Date).ToUniversalTime())-$created).TotalDays,2)}; return $null }
$walletFirst=@{}
foreach($t in $trades | Sort-Object timestamp){$w=[string]$t.proxyWallet; if(-not $walletFirst.ContainsKey($w)){$walletFirst[$w]=[int64]$t.timestamp}}
$rows=@(); $utcNow=(Get-Date).ToUniversalTime()
foreach($t in $trades){
 $amount=[math]::Round(([double]$t.size*[double]$t.price),2); if($amount -lt $minAmount){continue}
 $m=Get-Market $t.slug; $tradeUtc=[DateTimeOffset]::FromUnixTimeSeconds([int64]$t.timestamp).UtcDateTime
 $odds = if($m -and $m.lastTradePrice){[double]$m.lastTradePrice}else{[double]$t.price}
 $endUtc = if($m -and $m.endDate){[datetime]$m.endDate}else{$null}
 $impact = if($m -and $m.oneHourPriceChange){[double]$m.oneHourPriceChange}else{0.0}
 $walletAge=Get-WalletAgeDays $t.name
 $score=0; $reasons=@()
 if([math]::Abs($impact)-gt 0.02){$score+=30; $reasons+='+30 价格冲击>2%'}
 if($odds -ge 0.01 -and $odds -le 0.20 -and $amount -ge $minAmount){$score+=12; $reasons+='+12 低赔率区(1%-20%)重仓'}
 if($walletAge -ne $null -and $walletAge -lt 5){$score+=15; $reasons+='+15 新钱包(<5天)'}
 if($walletFirst[[string]$t.proxyWallet] -eq [int64]$t.timestamp){$score+=10; $reasons+='+10 首单即重仓(样本内)'}
 if($endUtc){$mins=($endUtc-$tradeUtc).TotalMinutes; if($mins -ge 0 -and $mins -le 60){$score+=5; $reasons+='+5 临近结束(<60m)'}}
 $rows += [pscustomobject]@{event=$t.title; amountUSD=$amount; orderTime=([DateTimeOffset]$tradeUtc).ToOffset([TimeSpan]::FromHours(8)).ToString('yyyy-MM-dd HH:mm:ss'); odds=[math]::Round($odds,4); endTime=$(if($endUtc){([DateTimeOffset]$endUtc).ToOffset([TimeSpan]::FromHours(8)).ToString('yyyy-MM-dd HH:mm:ss')}else{'-'}); ended=$(if($endUtc -and $endUtc -le $utcNow){'Yes'}else{'No'}); hitReasons=$(if($reasons.Count){$reasons -join '；'}else{'-'}) ; score=$score; link="https://polymarket.com/event/$($t.slug)" }
}
$final=$rows | Sort-Object -Property @{Expression='score';Descending=$true}, @{Expression='amountUSD';Descending=$true} | Select-Object -First 20
$out='C:\Users\Administrator\.openclaw\workspace\reports\polymarket_over2000_'+(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')+'.json'
$final|ConvertTo-Json -Depth 5 | Set-Content -Path $out -Encoding UTF8
Write-Output "OUT=$out"
Write-Output ("COUNT="+$final.Count)
