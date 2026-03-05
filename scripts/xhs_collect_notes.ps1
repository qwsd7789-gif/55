param(
  [Parameter(Mandatory = $true)]
  [string]$Keyword,
  [int]$Top = 20,
  [int]$Retry = 2,
  [int]$BackfillPasses = 1,
  [double]$MinDelaySec = 0.8,
  [double]$MaxDelaySec = 1.8,
  [string]$Host = "127.0.0.1",
  [int]$Port = 9222,
  [switch]$ReuseExistingTab
)

$ErrorActionPreference = 'Stop'

$workspace = "C:\Users\Administrator\.openclaw\workspace"
$cdpScript = "C:\Users\Administrator\.openclaw\skills\XiaohongshuSkills\scripts\cdp_publish.py"

if (-not (Test-Path $cdpScript)) { throw "cdp_publish.py not found: $cdpScript" }
if ($Top -lt 1) { throw "Top must be >= 1" }
if ($Retry -lt 1) { throw "Retry must be >= 1" }
if ($BackfillPasses -lt 0) { throw "BackfillPasses must be >= 0" }
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

  [pscustomobject]@{ ExitCode = $p.ExitCode; StdOut = $stdout; StdErr = $stderr }
}

function Extract-JsonAfterMarker {
  param([string]$Text,[string]$Marker)
  $idx = $Text.IndexOf($Marker)
  if ($idx -lt 0) { return $null }
  $jsonText = $Text.Substring($idx + $Marker.Length).Trim()
  if ([string]::IsNullOrWhiteSpace($jsonText)) { return $null }
  try { return $jsonText | ConvertFrom-Json } catch { return $null }
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

function Classify-Error {
  param([string]$Reason)
  $r = ($Reason | Out-String).ToLowerInvariant()
  if ($r -match 'not_logged_in|login|qr') { return 'login' }
  if ($r -match 'timeout|timed out|waiting for') { return 'timeout' }
  if ($r -match 'json|decode|parse') { return 'parse' }
  if ($r -match '429|forbidden|risk|captcha|blocked|inaccessible') { return 'risk_control' }
  if ($r -match 'connection|cannot reach chrome|cdp|websocket') { return 'browser_connection' }
  if ($r -match 'missing_feed_id_or_xsec_token') { return 'missing_key' }
  return 'unknown'
}

function Sleep-Random {
  param([double]$Min,[double]$Max)
  $ms = [int]((Get-Random -Minimum $Min -Maximum $Max) * 1000)
  Start-Sleep -Milliseconds $ms
}

function Fetch-Detail {
  param(
    [string]$FeedId,
    [string]$Xsec,
    [int]$RetryCount,
    [string[]]$CommonArgs,
    [double]$Min,
    [double]$Max
  )

  for ($i = 1; $i -le $RetryCount; $i++) {
    $detailArgs = @($CommonArgs + @('get-feed-detail','--feed-id',$FeedId,'--xsec-token',$Xsec))
    $res = Invoke-Xhs -Args $detailArgs

    if ($res.ExitCode -eq 0) {
      $payload = Extract-JsonAfterMarker -Text $res.StdOut -Marker 'GET_FEED_DETAIL_RESULT:'
      if ($payload) {
        return [pscustomobject]@{
          ok = $true
          feed_id = $FeedId
          xsec_token = $Xsec
          attempt = $i
          detail = $payload.detail
          reason = $null
          error_type = $null
        }
      }
      $reason = 'JSON parse failed'
    } else {
      $reason = (($res.StdErr + "`n" + $res.StdOut) | Out-String).Trim()
    }

    if ($i -lt $RetryCount) { Sleep-Random -Min $Min -Max $Max }
  }

  [pscustomobject]@{
    ok = $false
    feed_id = $FeedId
    xsec_token = $Xsec
    attempt = $RetryCount
    detail = $null
    reason = $reason
    error_type = (Classify-Error -Reason $reason)
  }
}

$commonArgs = @('"' + $cdpScript + '"', '--host', $Host, '--port', "$Port")
if ($ReuseExistingTab) { $commonArgs += '--reuse-existing-tab' }

Write-Host "[xhs-v2] Step1: search links by keyword='$Keyword'"
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
  Write-Host "[xhs-v2] No feeds found."
  exit 0
}

$selected = @($feeds | Select-Object -First $Top)
Write-Host "[xhs-v2] Step2: extract details from $($selected.Count) links"

$details = @()
$errors = @()
$errorBreakdown = @{}

$queue = @()
foreach ($feed in $selected) {
  $feedId = Get-FeedId -Feed $feed
  $xsec = Get-XsecToken -Feed $feed
  if (-not $feedId -or -not $xsec) {
    $errType = 'missing_key'
    if (-not $errorBreakdown.ContainsKey($errType)) { $errorBreakdown[$errType] = 0 }
    $errorBreakdown[$errType]++
    $errors += [pscustomobject]@{ feed_id = $feedId; xsec_token = $xsec; reason = 'missing_feed_id_or_xsec_token'; error_type = $errType; pass = 0 }
    continue
  }
  $queue += [pscustomobject]@{ feed_id = $feedId; xsec_token = $xsec }
}

# Pass 0: normal extraction
$failedQueue = @()
foreach ($item in $queue) {
  $r = Fetch-Detail -FeedId $item.feed_id -Xsec $item.xsec_token -RetryCount $Retry -CommonArgs $commonArgs -Min $MinDelaySec -Max $MaxDelaySec
  if ($r.ok) {
    $details += [pscustomobject]@{ feed_id = $r.feed_id; xsec_token = $r.xsec_token; attempt = $r.attempt; pass = 0; detail = $r.detail }
  } else {
    $failedQueue += $item
    $etype = $r.error_type
    if (-not $errorBreakdown.ContainsKey($etype)) { $errorBreakdown[$etype] = 0 }
    $errorBreakdown[$etype]++
    $errors += [pscustomobject]@{ feed_id = $r.feed_id; xsec_token = $r.xsec_token; reason = $r.reason; error_type = $etype; pass = 0 }
  }
  Sleep-Random -Min $MinDelaySec -Max $MaxDelaySec
}

# Backfill passes for failed queue
for ($p = 1; $p -le $BackfillPasses; $p++) {
  if (-not $failedQueue -or $failedQueue.Count -eq 0) { break }
  Write-Host "[xhs-v2] Backfill pass $p for $($failedQueue.Count) failed items"

  $nextFailed = @()
  foreach ($item in $failedQueue) {
    $r = Fetch-Detail -FeedId $item.feed_id -Xsec $item.xsec_token -RetryCount $Retry -CommonArgs $commonArgs -Min $MinDelaySec -Max $MaxDelaySec
    if ($r.ok) {
      $details += [pscustomobject]@{ feed_id = $r.feed_id; xsec_token = $r.xsec_token; attempt = $r.attempt; pass = $p; detail = $r.detail }
      # remove old pass0 error rows for this item when recovered
      $errors = @($errors | Where-Object { -not (($_.feed_id -eq $r.feed_id) -and ($_.xsec_token -eq $r.xsec_token)) })
    } else {
      $nextFailed += $item
      $etype = $r.error_type
      if (-not $errorBreakdown.ContainsKey($etype)) { $errorBreakdown[$etype] = 0 }
      $errorBreakdown[$etype]++
      $errors += [pscustomobject]@{ feed_id = $r.feed_id; xsec_token = $r.xsec_token; reason = $r.reason; error_type = $etype; pass = $p }
    }
    Sleep-Random -Min $MinDelaySec -Max $MaxDelaySec
  }
  $failedQueue = $nextFailed
}

# de-dup detail by feed_id (keep first success)
$detailMap = @{}
foreach ($d in $details) {
  if (-not $detailMap.ContainsKey($d.feed_id)) { $detailMap[$d.feed_id] = $d }
}
$finalDetails = @($detailMap.Values)

# de-dup errors by feed_id keep latest pass
$errorMap = @{}
foreach ($e in $errors) { $errorMap[$e.feed_id] = $e }
$finalErrors = @($errorMap.Values)

$success = $finalDetails.Count
$failed = $finalErrors.Count
$selectedCount = $selected.Count
$successRate = if ($selectedCount -gt 0) { [Math]::Round(($success / $selectedCount) * 100, 2) } else { 0 }

$ts = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$outDir = Join-Path $workspace 'reports'
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
$outPath = Join-Path $outDir ("xhs_collect_v2_" + $ts + ".json")

$result = [pscustomobject]@{
  keyword = $Keyword
  top = $Top
  retry = $Retry
  backfill_passes = $BackfillPasses
  selected_count = $selectedCount
  success = $success
  failed = $failed
  success_rate = $successRate
  recommended_keywords = $searchPayload.recommended_keywords
  error_breakdown = $errorBreakdown
  details = $finalDetails
  errors = $finalErrors
  generated_at = (Get-Date).ToString('o')
}

$result | ConvertTo-Json -Depth 16 | Set-Content -Path $outPath -Encoding UTF8

Write-Host "[xhs-v2] Done. success=$success failed=$failed success_rate=$successRate%"
Write-Host "[xhs-v2] Report: $outPath"
