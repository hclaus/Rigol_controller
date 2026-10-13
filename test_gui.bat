@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: .venv not found. Run "python -m venv .venv" and "pip install -r requirements.txt" first.
    pause
    exit /b 1
)

echo Launching Rigol Controller GUI (no power supply needed to test layout/buttons)...
echo Console stays open to show any errors or output.
echo.

".venv\Scripts\python.exe" Rigol_Controller.py

echo.
echo ---------------------------------------------
echo GUI closed (exit code %ERRORLEVEL%).
pause
