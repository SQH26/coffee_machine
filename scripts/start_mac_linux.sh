#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT_DIR/.run"
PID_FILE="$RUN_DIR/uvicorn.pid"
LOG_FILE="$RUN_DIR/server.log"

mkdir -p "$RUN_DIR"

if [ ! -d "$ROOT_DIR/frontend/node_modules" ]; then
  npm --prefix "$ROOT_DIR/frontend" install
fi

npm --prefix "$ROOT_DIR/frontend" run build

if command -v uv >/dev/null 2>&1; then
  uv sync --directory "$ROOT_DIR"
  uv run --directory "$ROOT_DIR" uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > "$LOG_FILE" 2>&1 &
else
  python3 -m pip install -e "$ROOT_DIR"
  python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > "$LOG_FILE" 2>&1 &
fi

echo $! > "$PID_FILE"
echo "Coffee machine server started on http://localhost:8000"
