Set-Location 'C:\Users\Administrator\.openclaw\workspace'
if(-not (git remote | Select-String -SimpleMatch 'origin')){ git remote add origin 'https://github.com/qwsd7789-gif/55.git' | Out-Null }
git add -A
$changes = git status --porcelain
if ($changes) {
  git commit -m "auto backup $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
  git push origin main
}
