@echo off
cd /d "%~dp0"
echo Installing Flask and dependencies...

if exist .venv\Scripts\pip.exe (
    .venv\Scripts\pip.exe install -r requirements.txt
    echo Done. Run the backend with: run-backend.bat
) else (
    echo Creating venv and installing...
    py -3 -m venv .venv
    .venv\Scripts\pip.exe install -r requirements.txt
    echo Done. Run the backend with: run-backend.bat
)
pause
