$ErrorActionPreference = 'Stop'

$workspace = "C:\Users\Administrator\.openclaw\workspace"
Set-Location $workspace
$memoryDir = Join-Path $workspace 'memory'
$weeklyDir = Join-Path $memoryDir 'weekly'
New-Item -ItemType Directory -Force -Path $weeklyDir | Out-Null

$now = Get-Date
# 上一周（周一到周日）
$dayOfWeek = [int]$now.DayOfWeek
$daysSinceMonday = if ($dayOfWeek -eq 0) { 6 } else { $dayOfWeek - 1 }
$thisMonday = $now.Date.AddDays(-$daysSinceMonday)
$start = $thisMonday.AddDays(-7)
$end = $thisMonday

$isoWeek = [System.Globalization.ISOWeek]::GetWeekOfYear($start)
$isoYear = [System.Globalization.ISOWeek]::GetYear($start)
$weeklyFile = Join-Path $weeklyDir ("{0}-W{1:00}.md" -f $isoYear, $isoWeek)

$days = @()
for ($d = $start; $d -lt $end; $d = $d.AddDays(1)) {
  $days += $d
}

$lines = @()
$lines += "# Weekly Memory {0}-W{1:00}" -f $isoYear, $isoWeek
$lines += "- Range: {0} ~ {1}" -f $start.ToString('yyyy-MM-dd'), $end.AddDays(-1).ToString('yyyy-MM-dd')
$lines += ""

foreach ($d in $days) {
  $f = Join-Path $memoryDir ($d.ToString('yyyy-MM-dd') + '.md')
  if (Test-Path $f) {
    $lines += "## " + $d.ToString('yyyy-MM-dd')
    $content = Get-Content -Path $f -Encoding UTF8
    $take = $content | Select-Object -First 80
    $lines += $take
    $lines += ""
  }
}

$lines += "## Refined for MEMORY.md"
$lines += "- （在此写入本周提炼后的长期记忆要点，使用项目符号）"
$lines += ""

Set-Content -Path $weeklyFile -Value ($lines -join "`r`n") -Encoding UTF8
Write-Output "Weekly memory generated: $weeklyFile"