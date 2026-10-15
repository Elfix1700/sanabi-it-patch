#!/usr/bin/env bash
# Avvia la patch italiana per SANABI su Linux / macOS / Steam Deck.
# Uso:  ./run_linux.sh --apply
#       ./run_linux.sh --check
#       ./run_linux.sh --restore
set -euo pipefail
cd "$(dirname "$0")"

PY=python3
command -v "$PY" >/dev/null 2>&1 || { echo "ERRORE: serve Python 3." >&2; exit 1; }

# controlla UnityPy, installala se manca
if ! "$PY" -c "import UnityPy" >/dev/null 2>&1; then
  echo "UnityPy non trovato. Installazione in corso..."
  "$PY" -m pip install --user UnityPy || {
    echo "ERRORE: installa UnityPy a mano:  pip install UnityPy" >&2
    exit 1
  }
fi

exec "$PY" patcher/patch_sanabi_it.py "$@"
