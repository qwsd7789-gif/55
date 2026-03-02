$ErrorActionPreference = 'Stop'

$workspace = "C:\Users\Administrator\.openclaw\workspace"
Set-Location $workspace

$day = (Get-Date).AddDays(-1)
$dateStr = $day.ToString('yyyy-MM-dd')
$memoryDir = Join-Path $workspace 'memory'
New-Item -ItemType Directory -Force -Path $memoryDir | Out-Null
$dailyFile = Join-Path $memoryDir ("$dateStr.md")

if (-not (Test-Path $dailyFile)) {
  "# $dateStr`r`n" | Out-File -FilePath $dailyFile -Encoding UTF8
}

$start = Get-Date -Year $day.Year -Month $day.Month -Day $day.Day -Hour 0 -Minute 0 -Second 0
$end = $start.AddDays(1)
$since = $start.ToString('s')
$until = $end.ToString('s')

$commits = git log --since="$since" --until="$until" --pretty="- %h %s" 2>$null
$files = git log --since="$since" --until="$until" --name-only --pretty="" 2>$null | Where-Object { $_ -and $_.Trim() -ne '' } | Sort-Object -Unique

$stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
$block = @()
$block += "## 自动午夜总结 ($stamp)"
if ($commits) {
  $block += "### Git 提交"
  $block += $commits
} else {
  $block += "- 当天无 Git 提交记录"
}

if ($files) {
  $block += "### 变更文件"
  $block += ($files | ForEach-Object { "- $_" })
}
$block += ""

Add-Content -Path $dailyFile -Value ($block -join "`r`n") -Encoding UTF8
Write-Output "Daily memory updated: $dailyFile"