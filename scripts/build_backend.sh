#!/usr/bin/env bash
set -euo pipefail

# Build the sidecar Tauri packages on macOS Apple Silicon. Run from repo root.
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Python virtual environment not found at $PYTHON_BIN" >&2
  exit 1
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" -m PyInstaller --noconfirm --clean EDWINBackend.spec
mkdir -p desktop/src-tauri/binaries
cp dist/EDWINBackend desktop/src-tauri/binaries/EDWINBackend-aarch64-apple-darwin
echo "Built desktop/src-tauri/binaries/EDWINBackend-aarch64-apple-darwin"
