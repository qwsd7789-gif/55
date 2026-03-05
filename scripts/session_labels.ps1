param(
  [ValidateSet('set','get','remove','list','resolve')]
  [string]$Action,
  [string]$SessionKey,
  [string]$SessionId,
  [string]$Label
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$storeDir = Join-Path $root 'memory'
$storePath = Join-Path $storeDir 'session-labels.json'

if (-not (Test-Path $storeDir)) {
  New-Item -ItemType Directory -Path $storeDir | Out-Null
}

function ConvertTo-HashtableRecursive($obj) {
  if ($null -eq $obj) { return $null }
  if ($obj -is [System.Collections.IDictionary]) {
    $h = @{}
    foreach ($k in $obj.Keys) {
      $h[$k] = ConvertTo-HashtableRecursive $obj[$k]
    }
    return $h
  }
  if ($obj -is [string] -or $obj.GetType().IsValueType) {
    return $obj
  }
  if ($obj -is [System.Collections.IEnumerable]) {
    $arr = @()
    foreach ($item in $obj) {
      $arr += ,(ConvertTo-HashtableRecursive $item)
    }
    return $arr
  }
  if ($obj.PSObject -and $obj.PSObject.Properties.Count -gt 0) {
    $h = @{}
    foreach ($p in $obj.PSObject.Properties) {
      $h[$p.Name] = ConvertTo-HashtableRecursive $p.Value
    }
    return $h
  }
  return $obj
}

function Load-Store {
  if (-not (Test-Path $storePath)) {
    return @{ updatedAt = (Get-Date).ToString('o'); labels = @{} }
  }
  $raw = Get-Content -Raw -Path $storePath
  if ([string]::IsNullOrWhiteSpace($raw)) {
    return @{ updatedAt = (Get-Date).ToString('o'); labels = @{} }
  }
  $obj = $raw | ConvertFrom-Json
  return (ConvertTo-HashtableRecursive $obj)
}

function Save-Store($store) {
  $store.updatedAt = (Get-Date).ToString('o')
  $store | ConvertTo-Json -Depth 8 | Set-Content -Path $storePath -Encoding UTF8
}

function Resolve-Key {
  param([string]$SessionKey,[string]$SessionId)

  if ($SessionKey) { return $SessionKey.ToLowerInvariant() }

  if ($SessionId) {
    $sessions = openclaw sessions --json | ConvertFrom-Json
    $hit = $sessions.sessions | Where-Object { $_.sessionId -eq $SessionId } | Select-Object -First 1
    if (-not $hit) { throw "No session found for sessionId: $SessionId" }
    return $hit.key.ToLowerInvariant()
  }

  throw 'Provide -SessionKey or -SessionId'
}

if (-not $Action) {
  Write-Host "Usage examples:"
  Write-Host "  .\scripts\session_labels.ps1 -Action list"
  Write-Host "  .\scripts\session_labels.ps1 -Action set -SessionKey 'agent:main:main' -Label '主会话'"
  Write-Host "  .\scripts\session_labels.ps1 -Action get -SessionId '<uuid>'"
  Write-Host "  .\scripts\session_labels.ps1 -Action resolve"
  exit 1
}

$store = Load-Store
if (-not $store.Contains('labels')) { $store.labels = @{} }

switch ($Action) {
  'set' {
    if (-not $Label) { throw 'set requires -Label' }
    $key = Resolve-Key -SessionKey $SessionKey -SessionId $SessionId
    $store.labels[$key] = [ordered]@{
      label = $Label
      updatedAt = (Get-Date).ToString('o')
    }
    Save-Store $store
    [pscustomobject]@{ key = $key; label = $Label; store = $storePath } | ConvertTo-Json
  }
  'get' {
    $key = Resolve-Key -SessionKey $SessionKey -SessionId $SessionId
    if ($store.labels.Contains($key)) {
      [pscustomobject]@{ key = $key; label = $store.labels[$key].label; updatedAt = $store.labels[$key].updatedAt } | ConvertTo-Json
    } else {
      [pscustomobject]@{ key = $key; label = $null } | ConvertTo-Json
    }
  }
  'remove' {
    $key = Resolve-Key -SessionKey $SessionKey -SessionId $SessionId
    $ok = $store.labels.Remove($key)
    Save-Store $store
    [pscustomobject]@{ key = $key; removed = [bool]$ok } | ConvertTo-Json
  }
  'list' {
    $rows = @()
    foreach ($k in $store.labels.Keys) {
      $rows += [pscustomobject]@{
        key = $k
        label = $store.labels[$k].label
        updatedAt = $store.labels[$k].updatedAt
      }
    }
    $rows | Sort-Object key | ConvertTo-Json
  }
  'resolve' {
    $sessions = openclaw sessions --json | ConvertFrom-Json
    $rows = @()
    foreach ($s in $sessions.sessions) {
      $k = "$($s.key)".ToLowerInvariant()
      $customLabel = $null
      if ($store.labels.Contains($k)) {
        $customLabel = $store.labels[$k].label
      }
      $rows += [pscustomobject]@{
        key = $k
        sessionId = $s.sessionId
        kind = $s.kind
        updatedAt = $s.updatedAt
        customLabel = $customLabel
      }
    }
    $rows | ConvertTo-Json
  }
}
