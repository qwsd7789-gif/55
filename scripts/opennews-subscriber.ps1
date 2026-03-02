#!/usr/bin/env pwsh
# OpenNews Real-time News Subscriber

$token = $env:OPENNEWS_TOKEN
$logFile = "$PSScriptRoot/../memory/opennews-stream.log"

echo "[$(Get-Date)] Starting OpenNews WebSocket subscriber..." | Tee-Object -Append $logFile

# Subscribe to all news
echo '{"action":"subscribe","filters":{}}' | wscat -c "wss://ai.6551.io/open/ws/news" -H "Authorization: Bearer $token" 2>&1 | ForEach-Object {
    $line = $_
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timestamp] $line" | Tee-Object -Append $logFile
}
