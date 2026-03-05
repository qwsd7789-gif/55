param(
  [Parameter(Mandatory = $true)]
  [string]$Keyword,
  [int]$Top = 20,
  [int]$Retry = 2,
  [double]$MinDelaySec = 0.8,
  [double]$MaxDelaySec = 1.8,
  [string]$Host = "127.0.0.1",
  [int]$Port = 9222,
  [switch]$ReuseExistingTab
)

$ErrorActionPreference = 'Stop'

$workspace = "C:\Users\Administrator\.openclaw\workspace"
$cdpScript = "C:\Users\Administrator\.openclaw\skills\XiaohongshuSkills\scripts\cdp_publish.py"

if (-not (Test-Path $cdpScript)) {
  throw "cdp_publish.py not found: $cdpScript"
}

if ($Top -lt 1) { throw "Top must be >= 1" }
if ($Retry -lt 1) { throw "Retry must be >= 1" }
if ($MinDelaySec -gt $MaxDelaySec) { throw "MinDelaySec must be <= MaxDelaySec" }

function Invoke-Xhs {
  param([string[]]$Args)
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = "python"
  $psi.Arguments = ($Args -join ' ')
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.UseShellExecute = $false
  $psi.CreateNoWindow = $true

  $p = New-Object System.Diagnostics.Process
  $p.StartInfo = $psi
  [void]$p.Start()
  $stdout = $p.StandardOutput.ReadToEnd()
  $stderr = $p.StandardError.ReadToEnd()
  $p.WaitForExit()

  return [pscustomobject]@{
    ExitCode = $p.ExitCode
    StdOut = $stdout
    StdErr = $stderr
  }
}

function Extract-JsonAfterMarker {
  param(
    [string]$Text,
    [string]$Marker
  )
  $idx = $Text.IndexOf($Marker)
  if ($idx -lt 0) { return $null }
  $jsonText = $Text.Substring($idx + $Marker.Length).Trim()
  if ([string]::IsNullOrWhiteSpace($jsonText)) { return $null }
  try {
    return $jsonText | ConvertFrom-Json
  } catch {
    return $null
  }
}

function Get-FeedId {
  param($Feed)
  foreach ($k in @('id','note_id','noteId','feed_id','noteIdStr')) {
    if ($Feed.PSObject.Properties.Name -contains $k -and $Feed.$k) { return [string]$Feed.$k }
  }
  return $null
}

function Get-XsecToken {
  param($Feed)
  foreach ($k in @('xsec_token','xsecToken','xsec_token_v2')) {
    if ($Feed.PSObject.Properties.Name -contains $k -and $Feed.$k) { return [string]$Feed.$k }
  }
  return $null
}

$commonArgs = @('"' + $cdpScript + '"', '--host', $Host, '--port', "$Port")
if ($ReuseExistingTab) { $commonArgs += '--reuse-existing-tab' }

Write-Host "[xhs] Step1: search links by keyword='$Keyword'"
$searchArgs = @($commonArgs + @('search-feeds', '--keyword', '"' + $Keyword.Replace('"','\"') + '"'))
$searchResult = Invoke-Xhs -Args $searchArgs

if ($searchResult.ExitCode -ne 0) {
  throw "search-feeds failed.`nSTDOUT:`n$($searchResult.StdOut)`nSTDERR:`n$($searchResult.StdErr)"
}

$searchPayload = Extract-JsonAfterMarker -Text $searchResult.StdOut -Marker 'SEARCH_FEEDS_RESULT:'
if (-not $searchPayload) {
  throw "Cannot parse SEARCH_FEEDS_RESULT JSON. Raw output:`n$($searchResult.StdOut)"
}

$feeds = @($searchPayload.feeds)
if (-not $feeds -or $feeds.Count -eq 0) {
  Write-Host "[xhs] No feeds found."
  exit 0
}

$selected = $feeds | Select-Object -First $Top
Write-Host "[xhs] Step2: extract details from $($selected.Count) links"

$details = @()
$errors = @()
$success = 0
$failed = 0

foreach ($feed in $selected) {
  $feedId = Get-FeedId -Feed $feed
  $xsec = Get-XsecToken -Feed $feed

  if (-not $feedId -or -not $xsec) {
    $failed++
    $errors += [pscustomobject]@{
      feed_id = $feedId
      xsec_token = $xsec
      reason = 'missing_feed_id_or_xsec_token'
    }
    continue
  }

  $ok = $false
  $lastErr = $null

  for ($i = 1; $i -le $Retry; $i++) {
    $detailArgs = @($commonArgs + @(
      'get-feed-detail',
      '--feed-id', $feedId,
      '--xsec-token', $xsec
    ))

    $res = Invoke-Xhs -Args $detailArgs
    if ($res.ExitCode -eq 0) {
      $payload = Extract-JsonAfterMarker -Text $res.StdOut -Marker 'GET_FEED_DETAIL_RESULT:'
      if ($payload) {
        $details += [pscustomobject]@{
          feed_id = $feedId
          xsec_token = $xsec
          attempt = $i
          detail = $payload.detail
        }
        $success++
        $ok = $true
        break
      }
      $lastErr = "JSON parse failed"
    } else {
      $lastErr = $res.StdErr
    }

    $sleep = Get-Random -Minimum $MinDelaySec -Maximum $MaxDelaySec
    Start-Sleep -Milliseconds ([int]($sleep * 1000))
  }

  if (-not $ok) {
    $failed++
    $errors += [pscustomobject]@{
      feed_id = $feedId
      xsec_token = $xsec
      reason = ($lastErr | Out-String).Trim()
    }
  }

  $gap = Get-Random -Minimum $MinDelaySec -Maximum $MaxDelaySec
  Start-Sleep -Milliseconds ([int]($gap * 1000))
}

$ts = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$outDir = Join-Path $workspace 'reports'
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
$outPath = Join-Path $outDir ("xhs_collect_" + $ts + ".json")

$result = [pscustomobject]@{
  keyword = $Keyword
  top = $Top
  selected_count = $selected.Count
  success = $success
  failed = $failed
  recommended_keywords = $searchPayload.recommended_keywords
  details = $details
  errors = $errors
  generated_at = (Get-Date).ToString('o')
}

$result | ConvertTo-Json -Depth 12 | Set-Content -Path $outPath -Encoding UTF8

Write-Host "[xhs] Done. success=$success failed=$failed"
Write-Host "[xhs] Report: $outPath"
