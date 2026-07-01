@echo off
cd /d "%~dp0"

echo Entrando na pasta do jogo...

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3 -m pip install --user -r requirements.txt
    py -3 main.py
) else (
    python -m pip install --user -r requirements.txt
    python main.py
)
