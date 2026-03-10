param(
  [string]$AppToken = "NnhgbjaTlaxqGxsOvaicz73ynJh",
  [string]$OwnerUserId = "ou_7cee3c56e53eac986cee208acd222a03"
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$cfgPath = 'C:\Users\Administrator\.openclaw\openclaw.json'
$cfgRaw = Get-Content -Raw -Path $cfgPath -Encoding UTF8
$appId = ([regex]::Match($cfgRaw, '"appId"\s*:\s*"([^"]+)"')).Groups[1].Value
$appSecret = ([regex]::Match($cfgRaw, '"appSecret"\s*:\s*"([^"]+)"')).Groups[1].Value
if ([string]::IsNullOrWhiteSpace($appId) -or [string]::IsNullOrWhiteSpace($appSecret)) {
  throw 'Cannot parse Feishu appId/appSecret from openclaw.json'
}

function Get-TenantToken {
  $body = @{ app_id = $appId; app_secret = $appSecret } | ConvertTo-Json
  $resp = Invoke-RestMethod -Method Post -Uri 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' -ContentType 'application/json; charset=utf-8' -Body $body
  if ($resp.code -ne 0) { throw "Get token failed: $($resp.msg)" }
  return $resp.tenant_access_token
}

$token = Get-TenantToken
$headers = @{ Authorization = "Bearer $token"; 'Content-Type' = 'application/json; charset=utf-8' }

function Api-Get([string]$url) {
  $r = Invoke-RestMethod -Method Get -Uri $url -Headers $headers
  if ($r.code -ne 0) { throw "GET $url failed: $($r.msg)" }
  return $r
}

function Api-Post([string]$url, $obj) {
  $r = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body ($obj | ConvertTo-Json -Depth 12)
  if ($r.code -ne 0) { throw "POST $url failed: $($r.msg)" }
  return $r
}

$tablesResp = Api-Get "https://open.feishu.cn/open-apis/bitable/v1/apps/$AppToken/tables?page_size=200"
$tables = @($tablesResp.data.items)

function Ensure-Table([string]$name) {
  $hit = $tables | Where-Object { $_.name -eq $name } | Select-Object -First 1
  if ($hit) { return $hit.table_id }
  $created = Api-Post "https://open.feishu.cn/open-apis/bitable/v1/apps/$AppToken/tables" @{ table = @{ name = $name } }
  $id = $created.data.table_id
  $script:tables += @(@{ name = $name; table_id = $id })
  return $id
}

function Get-Fields([string]$tableId) {
  $r = Api-Get "https://open.feishu.cn/open-apis/bitable/v1/apps/$AppToken/tables/$tableId/fields?page_size=500"
  return @($r.data.items)
}

function Ensure-Field([string]$tableId, [string]$fieldName, [int]$type, $property = $null) {
  $fields = Get-Fields $tableId
  $hit = $fields | Where-Object { $_.field_name -eq $fieldName } | Select-Object -First 1
  if ($hit) { return $hit.field_id }

  $body = @{ field_name = $fieldName; type = $type }
  if ($null -ne $property) { $body.property = $property }

  $created = Api-Post "https://open.feishu.cn/open-apis/bitable/v1/apps/$AppToken/tables/$tableId/fields" $body
  return $created.data.field.field_id
}

# 3 tables
$tblTask   = Ensure-Table '关键词任务'
$tblHot    = Ensure-Table '热门视频池'
$tblScript = Ensure-Table '改写与脚本'

# Table 1: 关键词任务
Ensure-Field $tblTask '关键词' 1 | Out-Null
Ensure-Field $tblTask '抓取数量' 2 | Out-Null
Ensure-Field $tblTask '平台' 3 | Out-Null
Ensure-Field $tblTask '执行状态' 3 | Out-Null
Ensure-Field $tblTask '触发抓取' 7 | Out-Null
Ensure-Field $tblTask '最近执行时间' 5 | Out-Null
Ensure-Field $tblTask '备注' 1 | Out-Null

# Table 2: 热门视频池
Ensure-Field $tblHot '关键词任务关联' 18 @{ table_id = $tblTask; multiple = $false } | Out-Null
Ensure-Field $tblHot '视频标题' 1 | Out-Null
Ensure-Field $tblHot '视频链接' 15 | Out-Null
Ensure-Field $tblHot '作者' 1 | Out-Null
Ensure-Field $tblHot '点赞数' 2 | Out-Null
Ensure-Field $tblHot '评论数' 2 | Out-Null
Ensure-Field $tblHot '转发数' 2 | Out-Null
Ensure-Field $tblHot '发布时间' 5 | Out-Null
Ensure-Field $tblHot '视频时长秒' 2 | Out-Null
Ensure-Field $tblHot '提取状态' 3 | Out-Null
Ensure-Field $tblHot '触发提取' 7 | Out-Null
Ensure-Field $tblHot '原始文案' 1 | Out-Null
Ensure-Field $tblHot '清洗文案' 1 | Out-Null
Ensure-Field $tblHot '关键帧' 17 | Out-Null
Ensure-Field $tblHot '提取日志' 1 | Out-Null

# Table 3: 改写与脚本
Ensure-Field $tblScript '关联视频' 18 @{ table_id = $tblHot; multiple = $false } | Out-Null
Ensure-Field $tblScript '改写风格' 3 | Out-Null
Ensure-Field $tblScript '目标人群' 1 | Out-Null
Ensure-Field $tblScript '触发改写' 7 | Out-Null
Ensure-Field $tblScript '生成状态' 3 | Out-Null
Ensure-Field $tblScript '改写文案' 1 | Out-Null
Ensure-Field $tblScript '拍摄脚本' 1 | Out-Null
Ensure-Field $tblScript '版本号' 2 | Out-Null
Ensure-Field $tblScript '生成日志' 1 | Out-Null

# Seed one task row
$seed = Api-Post "https://open.feishu.cn/open-apis/bitable/v1/apps/$AppToken/tables/$tblTask/records" @{
  fields = @{
    '关键词' = 'AI智能体'
    '抓取数量' = 20
    '平台' = '抖音'
    '执行状态' = '待抓取'
    '触发抓取' = $false
    '备注' = '初始化样例'
  }
}

# try grant owner permission
$permMsg = 'skip'
try {
  $perm = Api-Post "https://open.feishu.cn/open-apis/bitable/v1/permissions/$AppToken/members" @{ member_type='user'; member_id=$OwnerUserId; perm='full_access' }
  $permMsg = "ok:$($perm.msg)"
} catch {
  $permMsg = "warn:$($_.Exception.Message)"
}

[pscustomobject]@{
  app_token = $AppToken
  app_url = "https://pqx6yubp7vo.feishu.cn/base/$AppToken"
  table_ids = @{ task = $tblTask; hot = $tblHot; script = $tblScript }
  seeded_task_record_id = $seed.data.record.record_id
  permission = $permMsg
} | ConvertTo-Json -Depth 8
