#!/usr/bin/env bash
# Cross-platform environment setup script
set -euo pipefail

# Find repository root: try git first, then walk up looking for README.md, requirements.txt, or .git
find_repo_root() {
  if command -v git >/dev/null 2>&1; then
    if repo_root=$(git rev-parse --show-toplevel 2>/dev/null); then
      printf '%s' "$repo_root"
      return 0
    fi
  fi

  dir="$PWD"
  while [ "$dir" != "/" ] && [ -n "$dir" ]; do
    if [ -e "$dir/.git" ] || [ -f "$dir/requirements.txt" ] || [ -f "$dir/README.md" ]; then
      printf '%s' "$dir"
      return 0
    fi
    dir=$(dirname "$dir")
  done
  # fallback to current working directory
  printf '%s' "$PWD"
}

REPO_ROOT=$(find_repo_root)
cd "$REPO_ROOT"

echo "Repository root: $REPO_ROOT"

# Choose python executable
PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=python
else
  echo "ERROR: no python or python3 found on PATH" >&2
  return 1
fi

# Determine venv directory name
VENV_DIR=""
if [ -d "$REPO_ROOT/.venv" ]; then
  VENV_DIR="$REPO_ROOT/.venv"
elif [ -d "$REPO_ROOT/venv" ]; then
  VENV_DIR="$REPO_ROOT/venv"
else
  VENV_DIR="$REPO_ROOT/.venv"
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at $VENV_DIR using $PYTHON_CMD"
  "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

# Activation candidates (use forward slashes for Windows Git Bash compatibility)
ACTIVATE_CANDIDATES=(
  "$VENV_DIR/Scripts/activate"
  "$VENV_DIR/bin/activate"
  "$REPO_ROOT/venv/Scripts/activate"
  "$REPO_ROOT/venv/bin/activate"
)

ACTIVATED=0
for candidate in "${ACTIVATE_CANDIDATES[@]}"; do
  # Convert to a form usable by test -e (Bash understands forward slashes)
  if [ -f "$candidate" ]; then
    # Use forward-slash form when sourcing so Git Bash on Windows accepts it
    relpath=$(printf '%s' "$candidate" | sed "s:^$REPO_ROOT/::")
    echo "Sourcing $relpath"
    # shellcheck disable=SC1090
    source "$relpath" >/dev/null 2>&1 || source "$candidate"
    ACTIVATED=1
    break
  fi
done

if [ "$ACTIVATED" -ne 1 ]; then
  echo "WARNING: could not find activation script. You can activate manually:" >&2
  echo "  source $VENV_DIR/bin/activate" >&2
fi

# Install/upgrade packages from requirements.txt if present
REQ_FILE="$REPO_ROOT/requirements.txt"
if [ -f "$REQ_FILE" ]; then
  echo "Upgrading pip and installing requirements from $REQ_FILE"
  if command -v pip >/dev/null 2>&1; then
    pip install --upgrade pip setuptools wheel
    pip install --upgrade -r "$REQ_FILE"
  else
    "$PYTHON_CMD" -m pip install --upgrade pip setuptools wheel
    "$PYTHON_CMD" -m pip install --upgrade -r "$REQ_FILE"
  fi
else
  echo "No requirements.txt found at $REQ_FILE — skipping package install"
fi

# If the script was executed (not sourced), print a note about activation
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  echo "\nNote: to keep the virtual environment activated in your current shell, run:" 
  echo "  source $REPO_ROOT/$(basename "$0")"
fi

echo "Done."
