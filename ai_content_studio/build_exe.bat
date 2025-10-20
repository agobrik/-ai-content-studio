@echo off
REM AI Content Studio - Quick EXE Builder
echo ========================================
echo   AI Content Studio - EXE Builder
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create simple one-file executable
echo Building standalone executable...
echo This may take 5-10 minutes...
echo.

pyinstaller --name="AI_Content_Studio" ^
    --onefile ^
    --windowed ^
    --add-data "config;config" ^
    --hidden-import "PyQt6.QtCore" ^
    --hidden-import "PyQt6.QtGui" ^
    --hidden-import "PyQt6.QtWidgets" ^
    --hidden-import "PyQt6.QtMultimedia" ^
    --hidden-import "gtts" ^
    src\main.py

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Your executable is ready:
echo   dist\AI_Content_Studio.exe
echo.
echo You can copy this single file to any Windows PC and run it!
echo.
echo Note: First run will download AI models (internet required)
echo.
pause
