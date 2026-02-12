#!/usr/bin/env bash
set -euo pipefail

# Simple build script for this project.
# Usage:
#   bash build.sh           -> creates .venv, installs deps, compiles .py to .pyc
#   bash build.sh --bundle  -> additionally bundles scripts with PyInstaller

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

CREATOR_PYTHON=$(command -v python3 || command -v python || true)
if [ -z "$CREATOR_PYTHON" ]; then
  echo "Error: python3 or python not found in PATH. Install Python first." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment .venv using $CREATOR_PYTHON"
  "$CREATOR_PYTHON" -m venv .venv
fi

# Activate the venv for the script session
if [ -f ".venv/bin/activate" ]; then
  # POSIX / WSL / macOS
  # shellcheck disable=SC1091
  source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
  # Git Bash / MSYS / Cygwin may have Scripts/activate
  # shellcheck disable=SC1091
  source .venv/Scripts/activate
else
  echo "Error: could not find the virtualenv activate script." >&2
  exit 1
fi

echo "Upgrading pip and installing requirements (if present)"
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi

echo "Compiling Python files to bytecode"
python -m compileall -f .

if [ "${1:-}" = "--bundle" ]; then
  if ! command -v pyinstaller >/dev/null 2>&1; then
    echo "PyInstaller not found in venv; installing it now"
    pip install pyinstaller
  fi

  mkdir -p dist_build
  mkdir -p build_tmp
  echo "Bundling top-level .py scripts with PyInstaller into dist_build/"
  for file in *.py; do
    # Skip this build script and common non-entry files
    case "$file" in
      build.sh|requirements.txt)
        continue
        ;;
      *)
        echo "Packaging $file"
        pyinstaller --onefile --distpath dist_build --workpath build_tmp --specpath build_tmp "$file"
        ;;
    esac
  done
  echo "Bundles are in: $ROOT_DIR/dist_build"
fi

echo "Build finished."