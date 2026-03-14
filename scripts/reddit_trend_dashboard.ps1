param(
  [int]$TopN = 25,
  [string]$OutDir = "reports/reddit-trends"
)

$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

if (-not (Get-Command rdt -ErrorAction SilentlyContinue)) {
  throw "rdt command not found. Install with: uv tool install rdt-cli"
}

$raw = rdt popular --json --compact
$obj = $raw | ConvertFrom-Json

if (-not $obj.ok) {
  throw "rdt popular returned failure"
}

$posts = @($obj.data) | Select-Object -First $TopN
if ($posts.Count -eq 0) {
  throw "No posts returned from rdt popular"
}

$stop = @(
  'the','and','for','with','that','this','from','have','been','were','what','when','where','into','just','your','they','them','will','over','about','after','before','their','there','than','then','says','said','saying','only','more','most','some','such','very','much','many','like','dont','doesnt','cant','wont','im','youre','its','how','why','who','are','is','was','has','had','his','her','she','him','our','out','all','new','now'
)

$subAgg = $posts | Group-Object subreddit | Sort-Object Count -Descending
$topScore = $posts | Sort-Object score -Descending | Select-Object -First 10
$topComment = $posts | Sort-Object num_comments -Descending | Select-Object -First 10

$tokens = foreach ($p in $posts) {
  $t = [string]$p.title
  foreach ($m in [regex]::Matches($t.ToLower(), "[a-zA-Z][a-zA-Z0-9']{2,}")) {
    $w = $m.Value.Trim("'")
    if ($w.Length -ge 4 -and -not $stop.Contains($w)) { $w }
  }
}
$topKeywords = $tokens | Group-Object | Sort-Object Count -Descending | Select-Object -First 15

$now = Get-Date
$stamp = $now.ToString('yyyyMMdd-HHmm')
$outPath = Join-Path $OutDir "$stamp.md"
New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

$lines = @()
$lines += "# Reddit Trend Dashboard"
$lines += ""
$lines += "- Generated at: $($now.ToString('yyyy-MM-dd HH:mm:ss'))"
$lines += "- Sample size: $($posts.Count)"
$lines += "- Source: rdt popular --json --compact"
$lines += ""
$lines += "## 1) Subreddit distribution"
foreach ($g in $subAgg | Select-Object -First 15) {
  $lines += "- r/$($g.Name): $($g.Count)"
}
$lines += ""
$lines += "## 2) Score Top 10"
foreach ($p in $topScore) {
  $url = "https://reddit.com$($p.permalink)"
  $lines += "- [$($p.score)] r/$($p.subreddit) | comments $($p.num_comments) | $($p.title)"
  $lines += "  - $url"
}
$lines += ""
$lines += "## 3) Comments Top 10"
foreach ($p in $topComment) {
  $url = "https://reddit.com$($p.permalink)"
  $lines += "- [comments $($p.num_comments)] r/$($p.subreddit) | score $($p.score) | $($p.title)"
  $lines += "  - $url"
}
$lines += ""
$lines += "## 4) Keyword clusters (title frequency)"
foreach ($k in $topKeywords) {
  $lines += "- $($k.Name): $($k.Count)"
}

Set-Content -Path $outPath -Value ($lines -join "`r`n") -Encoding UTF8

Write-Output "REPORT=$outPath"
Write-Output "POSTS=$($posts.Count)"
Write-Output "TOP1=$($topScore[0].title)"