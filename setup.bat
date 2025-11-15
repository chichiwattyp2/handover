@echo off
REM WhatsApp Chat Analyzer - Setup Script for Windows
REM This script helps you set up the application quickly

echo ========================================
echo WhatsApp Chat Analyzer - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created
    echo.
    echo IMPORTANT: Please edit .env and add your ANTHROPIC_API_KEY
    echo You can get an API key from: https://console.anthropic.com/
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Run parser test
echo Running parser test...
python test_parser.py

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env and add your ANTHROPIC_API_KEY
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python app.py
echo 4. Open: http://localhost:5000
echo.
pause
