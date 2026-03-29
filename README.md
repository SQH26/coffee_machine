# Coffee Machine

Simple coffee machine app with a Next.js frontend and FastAPI backend.

## Requirements
- Python 3.11+
- Node.js 20+
- Optional: `uv` for Python dependency management

## Local Run (macOS/Linux)
```bash
./scripts/start_mac_linux.sh
```

Stop:
```bash
./scripts/stop_mac_linux.sh
```

## Local Run (Windows PowerShell)
```powershell
.\scripts\start_windows.ps1
```

Stop:
```powershell
.\scripts\stop_windows.ps1
```

## Docker
Build:
```bash
docker build -t coffee-machine .
```

Run:
```bash
docker run --rm -p 8000:8000 --env-file .env coffee-machine
```

Open [http://localhost:8000](http://localhost:8000).

## Test
```bash
uv sync
uv run pytest
```
