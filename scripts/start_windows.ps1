$ErrorActionPreference = "Stop"

$RootDir = (Resolve-Path "$PSScriptRoot\..").Path
$RunDir = Join-Path $RootDir ".run"
$PidFile = Join-Path $RunDir "uvicorn.pid"
$LogFile = Join-Path $RunDir "server.log"

if (-not (Test-Path $RunDir)) {
  New-Item -ItemType Directory -Path $RunDir | Out-Null
}

if (-not (Test-Path (Join-Path $RootDir "frontend\node_modules"))) {
  npm --prefix "$RootDir\frontend" install
}

npm --prefix "$RootDir\frontend" run build

$uvExists = $null -ne (Get-Command uv -ErrorAction SilentlyContinue)
if ($uvExists) {
  uv sync --directory $RootDir
  $proc = Start-Process -FilePath "uv" -ArgumentList @("run", "--directory", $RootDir, "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000") -RedirectStandardOutput $LogFile -RedirectStandardError $LogFile -PassThru
} else {
  python -m pip install -e $RootDir
  $proc = Start-Process -FilePath "python" -ArgumentList @("-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000") -RedirectStandardOutput $LogFile -RedirectStandardError $LogFile -PassThru
}

Set-Content -Path $PidFile -Value $proc.Id
Write-Host "Coffee machine server started on http://localhost:8000"
