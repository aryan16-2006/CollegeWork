#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python is not installed. Please install Python 3." >&2
  exit 1
fi
$PY -m pip install -r "$SCRIPT_DIR/requirements.txt"
exec $PY "$SCRIPT_DIR/main.py"