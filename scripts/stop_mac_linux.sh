#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$ROOT_DIR/.run/uvicorn.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "No running server found."
  exit 0
fi

PID="$(cat "$PID_FILE")"
if kill "$PID" >/dev/null 2>&1; then
  rm -f "$PID_FILE"
  echo "Coffee machine server stopped."
else
  rm -f "$PID_FILE"
  echo "Server process was not running."
fi
