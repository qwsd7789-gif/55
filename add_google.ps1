$json = Get-Content 'C:\Users\Administrator\.openclaw\openclaw.json' -Raw | ConvertFrom-Json
$json.auth.profiles | Add-Member -NotePropertyName 'google-ai:default' -NotePropertyValue @{provider='google-ai'; mode='api_key'} -PassThru | Out-Null
$json | ConvertTo-Json -Depth 20 | Set-Content 'C:\Users\Administrator\.openclaw\openclaw.json'
