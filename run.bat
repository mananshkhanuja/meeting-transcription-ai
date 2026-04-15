@echo off
echo Initializing Python 3.11 Virtual Environment Stack...

SET VENV_PYTHON="%~dp0.venv\Scripts\python.exe"

IF NOT EXIST %VENV_PYTHON% (
    echo Virtual environment not found! Please assure it is installed.
    pause
    exit /b 1
)

%VENV_PYTHON% "%~dp0src\main.py"
pause
