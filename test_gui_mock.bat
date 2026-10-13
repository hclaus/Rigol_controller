@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: .venv not found. Run "python -m venv .venv" and "pip install -r requirements.txt" first.
    pause
    exit /b 1
)

echo Launching Rigol Controller GUI in MOCK MODE.
echo "Find Power Supplies" will report two fake supplies so you can test
echo the 2nd-panel duplication and the full on/off workflow without any
echo hardware or VISA backend installed.
echo.

set RIGOL_MOCK=1
".venv\Scripts\python.exe" Rigol_Controller.py

echo.
echo ---------------------------------------------
echo GUI closed (exit code %ERRORLEVEL%).
pause
