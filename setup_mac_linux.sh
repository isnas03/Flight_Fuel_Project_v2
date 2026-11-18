#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
if ! command -v conda >/dev/null 2>&1; then
  echo 'Conda was not found. Complete Step 1 in README.md, then reopen your terminal.'
  exit 1
fi
if [ -d .runtime/conda-meta ]; then
  echo 'Updating the existing project environment.'
  conda install --prefix "$PWD/.runtime" --override-channels -c conda-forge python=3.12 'tk>=8.6,<9' 'matplotlib>=3.8,<4' -y
else
  conda create --prefix "$PWD/.runtime" --override-channels -c conda-forge python=3.12 'tk>=8.6,<9' 'matplotlib>=3.8,<4' -y
fi
echo 'Setup complete. Run: bash run_mac_linux.sh'
