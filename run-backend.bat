@echo off
cd /d "%~dp0"
rem PORT is read from .env (default 10000) if not set
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe app.py
) else (
    py -3 app.py
)
