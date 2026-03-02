$ErrorActionPreference = 'Stop'

$workspace = "C:\Users\Administrator\.openclaw\workspace"
$memoryDir = Join-Path $workspace 'memory'
$weeklyDir = Join-Path $memoryDir 'weekly'
$mainMemory = Join-Path $workspace 'MEMORY.md'

if (-not (Test-Path $weeklyDir)) { exit 0 }

$latest = Get-ChildItem -Path $weeklyDir -Filter '*.md' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $latest) { exit 0 }

$content = Get-Content -Path $latest.FullName -Encoding UTF8
$startIdx = ($content | Select-String -Pattern '^## Refined for MEMORY.md$' -SimpleMatch).LineNumber
if (-not $startIdx) { exit 0 }

$tail = $content[($startIdx)..($content.Length - 1)]
$bullets = $tail | Where-Object { $_ -match '^- ' -and $_ -notmatch '（在此写入' }
if (-not $bullets -or $bullets.Count -eq 0) { exit 0 }

$tag = "### Weekly Refined: " + [System.IO.Path]::GetFileNameWithoutExtension($latest.Name)
$main = Get-Content -Path $mainMemory -Encoding UTF8
if ($main -contains $tag) { exit 0 }

Add-Content -Path $mainMemory -Value "`r`n$tag`r`n" -Encoding UTF8
foreach ($b in $bullets) {
  Add-Content -Path $mainMemory -Value $b -Encoding UTF8
}
Write-Output "Promoted refined memory from $($latest.Name)"