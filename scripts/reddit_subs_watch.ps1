param(
  [int]$TopPerSub = 5,
  [string]$OutDir = "reports/reddit-watch",
  [string]$BaselinePath = "memory/reddit-watch-baseline.json"
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$categories = [ordered]@{
  '财经' = @('economics','finance','investing','SecurityAnalysis','ValueInvesting')
  '股票' = @('stocks','StockMarket','wallstreetbets','options','Bogleheads')
  '伊朗' = @('iran','NewIran','geopolitics','worldnews','CredibleDefense')
}

$subs = @($categories.Values | ForEach-Object { $_ } | Select-Object -Unique)

$headers = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) OpenClaw/1.0' }

$baseline = @{ seen = @{} }
if (Test-Path $BaselinePath) {
  try {
    $raw = Get-Content $BaselinePath -Raw -Encoding UTF8
    if ($raw) {
      $obj = $raw | ConvertFrom-Json -AsHashtable
      if ($obj.ContainsKey('seen')) { $baseline = $obj }
    }
  } catch {}
}

$all = @()
$new = @()
$errors = @()
$perSubTop = @{}

foreach ($sub in $subs) {
  try {
    $url = "https://www.reddit.com/r/$sub/hot.json?limit=$TopPerSub"
    $resp = Invoke-RestMethod -Uri $url -Headers $headers -TimeoutSec 25
    $children = @($resp.data.children)
    if ($children.Count -gt 0) {
      $perSubTop[$sub] = $children[0].data
    }

    foreach ($c in $children) {
      $p = $c.data
      $row = [PSCustomObject]@{
        subreddit   = [string]$p.subreddit
        id          = [string]$p.id
        title       = [string]$p.title
        score       = [int]$p.score
        comments    = [int]$p.num_comments
        created_utc = [double]$p.created_utc
        permalink   = [string]$p.permalink
      }
      $all += $row
      if (-not $baseline.seen.ContainsKey($row.id)) { $new += $row }
      $baseline.seen[$row.id] = $row.created_utc
    }
  } catch {
    $errors += "r/$sub => $($_.Exception.Message)"
  }
}

# Trim baseline
$seenPairs = foreach ($k in $baseline.seen.Keys) {
  [PSCustomObject]@{ id = $k; ts = [double]$baseline.seen[$k] }
}
$seenPairs = $seenPairs | Sort-Object ts -Descending | Select-Object -First 5000
$baseline.seen = @{}
foreach ($x in $seenPairs) { $baseline.seen[$x.id] = $x.ts }

$baseDir = Split-Path -Parent $BaselinePath
if ($baseDir) { New-Item -ItemType Directory -Path $baseDir -Force | Out-Null }
$baseline | ConvertTo-Json -Depth 6 | Set-Content -Path $BaselinePath -Encoding UTF8

$now = Get-Date
$stamp = $now.ToString('yyyyMMdd-HHmm')
New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
$outPath = Join-Path $OutDir "$stamp.md"

$topGlobal = $all | Sort-Object score -Descending | Select-Object -First 20
$newTop = $new | Sort-Object score -Descending | Select-Object -First 30

$lines = @()
$lines += "# Reddit Subreddits Hotspot Monitor"
$lines += ""
$lines += "- Generated at: $($now.ToString('yyyy-MM-dd HH:mm:ss'))"
$lines += "- Subreddits monitored: $($subs.Count)"
$lines += "- Posts scanned: $($all.Count)"
$lines += "- New posts since last run: $($new.Count)"
$lines += "- Errors: $($errors.Count)"
$lines += ""
$lines += "## New hotspots"
if ($newTop.Count -eq 0) {
  $lines += "- None in this run"
} else {
  foreach ($p in $newTop) {
    $u = "https://reddit.com$($p.permalink)"
    $lines += "- [$($p.score)] r/$($p.subreddit) | comments $($p.comments) | $($p.title)"
    $lines += "  - $u"
  }
}
$lines += ""
$lines += "## Global score top 20"
foreach ($p in $topGlobal) {
  $u = "https://reddit.com$($p.permalink)"
  $lines += "- [$($p.score)] r/$($p.subreddit) | comments $($p.comments) | $($p.title)"
  $lines += "  - $u"
}
$lines += ""
$lines += "## Per-category Top 3"
foreach ($cat in $categories.Keys) {
  $lines += ""
  $lines += "### $cat"
  $catSubs = @($categories[$cat])
  $catPosts = $all | Where-Object { $catSubs -contains $_.subreddit } | Sort-Object score -Descending | Select-Object -First 3
  if ($catPosts.Count -eq 0) {
    $lines += "- 暂无数据"
    continue
  }
  foreach ($p in $catPosts) {
    $u = "https://reddit.com$($p.permalink)"
    $lines += "- [$($p.score)] r/$($p.subreddit) | comments $($p.comments) | $($p.title)"
    $lines += "  - $u"
  }
}
$lines += ""
$lines += "## Per-subreddit top 1"
foreach ($sub in $subs) {
  if ($perSubTop.ContainsKey($sub)) {
    $p = $perSubTop[$sub]
    $u = "https://reddit.com$($p.permalink)"
    $lines += "- r/${sub}: [$($p.score)] comments $($p.num_comments) | $($p.title)"
    $lines += "  - $u"
  } else {
    $lines += "- r/${sub}: no data"
  }
}

if ($errors.Count -gt 0) {
  $lines += ""
  $lines += "## Errors"
  foreach ($e in $errors) { $lines += "- $e" }
}

Set-Content -Path $outPath -Value ($lines -join "`r`n") -Encoding UTF8

Write-Output "REPORT=$outPath"
Write-Output "SCANNED=$($all.Count)"
Write-Output "NEW=$($new.Count)"
Write-Output "ERRORS=$($errors.Count)"