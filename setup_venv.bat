@echo off
setlocal

rem Creates .venv next to this script, with the same package versions as the Mac setup.
rem Uses Python 3.14 because PyYAML has no Windows wheel for 3.15 yet. uv downloads it,
rem so Python does not need to be installed first.

cd /d "%~dp0"

where uv >nul 2>nul
if not errorlevel 1 goto :have_uv

echo uv not found, installing it...
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
if errorlevel 1 goto :fail
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

:have_uv
echo Creating .venv with Python 3.14.7...
rem --clear replaces any existing .venv, so this script is safe to re-run.
uv venv .venv --python 3.14.7 --clear
if errorlevel 1 goto :fail

echo Installing packages...
uv pip install --python .venv\Scripts\python.exe astropy==8.0.2 numpy==2.5.4 matplotlib==3.11.2
if errorlevel 1 goto :fail

.venv\Scripts\python.exe -c "import astropy, numpy, matplotlib; print('All packages import OK')"
if errorlevel 1 goto :fail

echo.
echo Done. To use it, run:  .venv\Scripts\activate
echo.
pause
exit /b 0

:fail
echo.
echo Setup failed. See the error above.
echo.
pause
exit /b 1
