$ErrorActionPreference = 'Continue'

$workspace = "C:\Users\Administrator\.openclaw\workspace"
$memoryDir = Join-Path $workspace 'memory'
$logDir = Join-Path $memoryDir 'logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir 'qmd-index.log'

$stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
if (Get-Command qmd -ErrorAction SilentlyContinue) {
  try {
    qmd index "$memoryDir" *>> $logFile
    Add-Content -Path $logFile -Value "[$stamp] qmd index done" -Encoding UTF8
  } catch {
    Add-Content -Path $logFile -Value "[$stamp] qmd index failed: $($_.Exception.Message)" -Encoding UTF8
  }
} else {
  Add-Content -Path $logFile -Value "[$stamp] qmd not found, skipped" -Encoding UTF8
}
