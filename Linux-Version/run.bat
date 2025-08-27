@echo off
echo Starting Bubbles PyInstaller Forge (Linux Version)...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists in parent directory
if exist "..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\venv\Scripts\activate.bat"
) else if exist "..\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\.venv\Scripts\activate.bat"
) else (
    echo No virtual environment found, using system Python
)

REM Install requirements if needed
if exist "..\requirements.txt" (
    echo Updating pip...
    python -m pip install --upgrade pip --quiet
    echo Installing/updating requirements...
    pip install -r "..\requirements.txt" --quiet
)

REM Run the application
echo Launching Bubbles PyInstaller Forge...
echo.
python "BubblesPyInstallerForge-Linux.py"

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)
