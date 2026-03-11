param(
  [string]$Prompt = 'A cute shiba inu, cinematic lighting, high detail',
  [string]$OutFile = 'C:/Users/Administrator/.openclaw/workspace/output/newapi_gemini_image.png',
  [string]$ApiKey = $env:NEWAPI_API_KEY,
  [string]$BaseUrl = 'https://api.newapi.ai',
  [string]$Model = 'gemini-2.5-flash-image'
)

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
  throw 'Missing API key. Set NEWAPI_API_KEY or pass -ApiKey.'
}

$uri = "$BaseUrl/v1beta/models/$Model`:generateContent/"
$payload = @{
  contents = @(
    @{
      role = 'user'
      parts = @(
        @{ text = $Prompt }
      )
    }
  )
  generationConfig = @{
    responseModalities = @('TEXT','IMAGE')
    imageConfig = @{
      aspectRatio = '1:1'
      imageSize   = '1K'
    }
  }
}

$body = $payload | ConvertTo-Json -Depth 20

$resp = Invoke-RestMethod -Method Post -Uri $uri -Headers @{
  Authorization = "Bearer $ApiKey"
  'Content-Type' = 'application/json'
} -Body $body

$b64 = $null
if ($resp.candidates) {
  foreach ($c in $resp.candidates) {
    if ($c.content -and $c.content.parts) {
      foreach ($p in $c.content.parts) {
        if ($p.inlineData -and $p.inlineData.data) {
          $b64 = $p.inlineData.data
          break
        }
      }
    }
    if ($b64) { break }
  }
}

if (-not $b64) {
  $resp | ConvertTo-Json -Depth 50
  throw 'No image base64 found at candidates[].content.parts[].inlineData.data'
}

$dir = Split-Path -Parent $OutFile
if ($dir -and -not (Test-Path $dir)) {
  New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

[System.IO.File]::WriteAllBytes($OutFile, [Convert]::FromBase64String($b64))
Write-Output "OK: $OutFile"
