#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
if [ ! -x "$PWD/.runtime/bin/python" ]; then
  echo 'Complete setup first: bash setup_mac_linux.sh'
  exit 1
fi
# An explicit interpreter bypasses pyenv shims and shell aliases.
# Discard inherited Python/Tk overrides that could select a different runtime.
unset PYTHONHOME PYTHONPATH TCL_LIBRARY TK_LIBRARY
exec "$PWD/.runtime/bin/python" -E -s "$PWD/fuel_calculator.py"
