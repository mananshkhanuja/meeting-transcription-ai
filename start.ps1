# PowerShell Execution Stub for Windows Meeting Transcription

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $ProjectRoot

Write-Host "Initializing Python 3.11 Virtual Environment Stack..." -ForegroundColor Cyan

$VenvPython = Join-Path -Path $ProjectRoot -ChildPath ".venv\Scripts\python.exe"

if (-not (Test-Path -Path $VenvPython)) {
    Write-Host "Virtual environment not found! Please ensure it is correctly installed." -ForegroundColor Red
    exit 1
}

& $VenvPython src\main.py
