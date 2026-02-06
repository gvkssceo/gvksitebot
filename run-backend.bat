@echo off
cd /d "%~dp0"
set PORT=5001
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe app.py
) else (
    py -3 app.py
)
