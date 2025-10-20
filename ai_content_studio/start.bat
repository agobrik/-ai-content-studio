@echo off
REM AI Content Studio - Windows Launcher

echo =====================================
echo   AI Content Studio
echo =====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run setup.bat first or create venv manually.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Launch application
echo Launching AI Content Studio...
echo.
python src\main.py

REM Deactivate virtual environment on exit
deactivate

pause
