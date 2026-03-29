$ErrorActionPreference = "Stop"

$RootDir = (Resolve-Path "$PSScriptRoot\..").Path
$PidFile = Join-Path $RootDir ".run\uvicorn.pid"

if (-not (Test-Path $PidFile)) {
  Write-Host "No running server found."
  exit 0
}

$PidValue = Get-Content $PidFile
try {
  Stop-Process -Id $PidValue -Force
  Write-Host "Coffee machine server stopped."
} catch {
  Write-Host "Server process was not running."
}

Remove-Item $PidFile -ErrorAction SilentlyContinue
