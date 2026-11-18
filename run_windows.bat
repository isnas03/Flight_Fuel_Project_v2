@echo off
setlocal
cd /d "%~dp0"
if not exist ".runtime\python.exe" (
  echo Complete setup_windows.bat first. See README.md.
  pause
  exit /b 1
)
set "PYTHONHOME="
set "PYTHONPATH="
set "TCL_LIBRARY="
set "TK_LIBRARY="
rem Include Conda DLL directories and use the exact project Python executable.
set "PATH=%CD%\.runtime;%CD%\.runtime\Library\mingw-w64\bin;%CD%\.runtime\Library\usr\bin;%CD%\.runtime\Library\bin;%CD%\.runtime\Scripts;%PATH%"
"%CD%\.runtime\python.exe" -E -s "%CD%\fuel_calculator.py"
if errorlevel 1 pause
