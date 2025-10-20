@echo off
REM AI Content Studio - Complete Build Script
echo ========================================
echo   AI Content Studio - Full Build
echo ========================================
echo.
echo Bu script 3 farkli dagitim paketi olusturacak:
echo 1. Tek dosya EXE
echo 2. Installer scripti
echo 3. Portable ZIP
echo.
pause

REM Step 1: Build EXE
echo.
echo [1/3] Building standalone EXE...
call build_exe.bat

REM Step 2: Create installer scripts
echo.
echo [2/3] Creating installer scripts...
python build_installer.py

REM Step 3: Create portable version
echo.
echo [3/3] Creating portable version...
call create_portable.bat

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Olusturulan dosyalar:
echo.
echo 1. dist\AI_Content_Studio.exe
echo    - Tek dosya, istediginiz PC'ye kopyalayin
echo.
echo 2. installer.iss
echo    - Inno Setup ile derleyin (profesyonel kurulum)
echo.
echo 3. portable\
echo    - ZIP yapip dagitabilirsiniz (kurulum yok)
echo.
echo.
echo Sonraki adimlar:
echo.
echo KOLAY YOL:
echo   dist\AI_Content_Studio.exe dosyasini kopyalayin
echo.
echo PROFESYONEL:
echo   1. Inno Setup yukleyin
echo   2. installer.iss dosyasini derleyin
echo.
echo PORTABLE:
echo   portable\ klasorunu ZIP yapin
echo.
pause
