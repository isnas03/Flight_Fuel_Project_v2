@echo off
setlocal
cd /d "%~dp0"
where conda >nul 2>nul
if errorlevel 1 (
  echo Conda not found. Open Miniforge Prompt and follow README.md.
  pause
  exit /b 1
)
if exist ".runtime\conda-meta" (
  call conda install --prefix "%CD%\.runtime" --override-channels -c conda-forge python=3.12 "tk>=8.6,<9" "matplotlib>=3.8,<4" -y
) else (
  call conda create --prefix "%CD%\.runtime" --override-channels -c conda-forge python=3.12 "tk>=8.6,<9" "matplotlib>=3.8,<4" -y
)
if errorlevel 1 (
  echo Setup failed. Read the error above and troubleshooting in README.md.
  pause
  exit /b 1
)
echo Setup complete. You can now open run_windows.bat.
pause
