$ErrorActionPreference = 'Stop'

$workspace = "C:\Users\Administrator\.openclaw\workspace"
$memoryDir = Join-Path $workspace 'memory'
$archiveDir = Join-Path $memoryDir 'archive'
New-Item -ItemType Directory -Force -Path $archiveDir | Out-Null

$cutoff = (Get-Date).AddDays(-60)
$dailyFiles = Get-ChildItem -Path $memoryDir -Filter '20??-??-??.md' -File -ErrorAction SilentlyContinue

foreach ($f in $dailyFiles) {
  if ($f.LastWriteTime -lt $cutoff) {
    Move-Item -Path $f.FullName -Destination (Join-Path $archiveDir $f.Name) -Force
  }
}

Write-Output "Prune done. Older daily memories moved to archive (>60 days)."