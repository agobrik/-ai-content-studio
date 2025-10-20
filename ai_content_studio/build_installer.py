"""
AI Content Studio - Standalone Installer Builder
Creates a Windows executable installer using PyInstaller
"""

import os
import sys
import shutil
from pathlib import Path

def create_spec_file():
    """Create PyInstaller spec file"""

    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('assets', 'assets'),
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('beniokumalisin.md', '.'),
        ('ORNEK_PROMPTLAR.md', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtMultimedia',
        'torch',
        'torchvision',
        'diffusers',
        'transformers',
        'trimesh',
        'gtts',
        'PIL',
        'numpy',
        'scipy',
        'matplotlib',
        'cv2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AIContentStudio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI app, no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AIContentStudio',
)
"""

    with open('AIContentStudio.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("✓ Spec file created: AIContentStudio.spec")


def create_nsis_installer():
    """Create NSIS installer script"""

    nsis_content = """
; AI Content Studio Installer
; NSIS Installer Script

!include "MUI2.nsh"

Name "AI Content Studio"
OutFile "AI_Content_Studio_Setup.exe"
InstallDir "$PROGRAMFILES\\AI Content Studio"
InstallDirRegKey HKLM "Software\\AIContentStudio" "Install_Dir"
RequestExecutionLevel admin

!define MUI_ABORTWARNING
!define MUI_ICON "assets\\icon.ico"
!define MUI_UNICON "assets\\icon.ico"

!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Turkish"
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"

  ; Copy all files
  File /r "dist\\AIContentStudio\\*.*"

  ; Create shortcuts
  CreateDirectory "$SMPROGRAMS\\AI Content Studio"
  CreateShortcut "$SMPROGRAMS\\AI Content Studio\\AI Content Studio.lnk" "$INSTDIR\\AIContentStudio.exe"
  CreateShortcut "$DESKTOP\\AI Content Studio.lnk" "$INSTDIR\\AIContentStudio.exe"

  ; Write uninstaller
  WriteUninstaller "$INSTDIR\\Uninstall.exe"

  ; Registry keys
  WriteRegStr HKLM "Software\\AIContentStudio" "Install_Dir" "$INSTDIR"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AIContentStudio" "DisplayName" "AI Content Studio"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AIContentStudio" "UninstallString" '"$INSTDIR\\Uninstall.exe"'

  MessageBox MB_OK "AI Content Studio başarıyla kuruldu!$\\n$\\nMasaüstünde kısayol oluşturuldu."
SectionEnd

Section "Uninstall"
  ; Remove files
  Delete "$INSTDIR\\*.*"
  RMDir /r "$INSTDIR"

  ; Remove shortcuts
  Delete "$SMPROGRAMS\\AI Content Studio\\*.*"
  RMDir "$SMPROGRAMS\\AI Content Studio"
  Delete "$DESKTOP\\AI Content Studio.lnk"

  ; Remove registry keys
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AIContentStudio"
  DeleteRegKey HKLM "Software\\AIContentStudio"
SectionEnd
"""

    with open('installer.nsi', 'w', encoding='utf-8') as f:
        f.write(nsis_content)

    print("✓ NSIS script created: installer.nsi")


def create_inno_setup_script():
    """Create Inno Setup installer script (alternative to NSIS)"""

    inno_content = """
; AI Content Studio - Inno Setup Script

[Setup]
AppName=AI Content Studio
AppVersion=1.0.0
AppPublisher=AI Content Studio
DefaultDirName={autopf}\\AI Content Studio
DefaultGroupName=AI Content Studio
OutputDir=.
OutputBaseFilename=AI_Content_Studio_Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
WizardStyle=modern

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\\Turkish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\\AIContentStudio\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\\AI Content Studio"; Filename: "{app}\\AIContentStudio.exe"
Name: "{autodesktop}\\AI Content Studio"; Filename: "{app}\\AIContentStudio.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\AIContentStudio.exe"; Description: "{cm:LaunchProgram,AI Content Studio}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('AI Content Studio başarıyla kuruldu!' + #13#10 + #13#10 +
           'İlk kullanımda AI modelleri indirilecektir.' + #13#10 +
           'İnternet bağlantısı gereklidir.', mbInformation, MB_OK);
  end;
end;
"""

    with open('installer.iss', 'w', encoding='utf-8') as f:
        f.write(inno_content)

    print("✓ Inno Setup script created: installer.iss")


def create_portable_version():
    """Create portable ZIP version"""

    script_content = """@echo off
echo ========================================
echo   AI Content Studio - Portable Versiyon
echo ========================================
echo.
echo Portable kurulum olusturuluyor...
echo.

REM Create portable directory
mkdir portable 2>nul

REM Copy application files
echo 1. Dosyalar kopyalaniyor...
xcopy /E /I /Y dist\\AIContentStudio portable\\AIContentStudio

REM Create launcher
echo 2. Baslatici olusturuluyor...
(
echo @echo off
echo cd /d "%%~dp0AIContentStudio"
echo start AIContentStudio.exe
) > portable\\AI_Content_Studio.bat

REM Create readme
echo 3. README olusturuluyor...
(
echo # AI Content Studio - Portable Versiyon
echo.
echo ## Kullanim:
echo.
echo 1. AI_Content_Studio.bat dosyasina cift tiklayin
echo 2. Uygulama acilacak
echo 3. Kurulum gerektirmez, direkt calisir
echo.
echo ## Notlar:
echo.
echo - Ilk kullanimda modeller indirilecek
echo - Internet baglantisi gerekli
echo - Windows 10/11 uyumlu
echo.
echo Iyi kullanimlar!
) > portable\\README.txt

echo.
echo ✓ Portable versiyon hazir: portable/
echo.
echo Portable klasorunu istediginiz yere kopyalayabilirsiniz.
echo.
pause
"""

    with open('create_portable.bat', 'w', encoding='utf-8') as f:
        f.write(script_content)

    print("✓ Portable creator created: create_portable.bat")


def main():
    """Main build process"""
    print("=" * 60)
    print("  AI Content Studio - Installer Builder")
    print("=" * 60)
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        os.system("pip install pyinstaller")

    # Create necessary files
    print("\n1. Creating build scripts...")
    create_spec_file()
    create_nsis_installer()
    create_inno_setup_script()
    create_portable_version()

    print("\n" + "=" * 60)
    print("  Build scripts created successfully!")
    print("=" * 60)

    print("""
Next steps:

METHOD 1: PyInstaller (Standalone EXE)
--------------------------------------
1. Run: pyinstaller AIContentStudio.spec
2. Output: dist/AIContentStudio/AIContentStudio.exe
3. Distribute the entire 'dist/AIContentStudio' folder

METHOD 2: NSIS Installer
------------------------
1. Install NSIS: https://nsis.sourceforge.io/
2. Build with PyInstaller first (method 1)
3. Right-click installer.nsi → "Compile NSIS Script"
4. Output: AI_Content_Studio_Setup.exe

METHOD 3: Inno Setup Installer (Recommended)
--------------------------------------------
1. Install Inno Setup: https://jrsoftware.org/isinfo.php
2. Build with PyInstaller first (method 1)
3. Open installer.iss in Inno Setup
4. Click "Compile"
5. Output: AI_Content_Studio_Setup.exe

METHOD 4: Portable ZIP
----------------------
1. Build with PyInstaller first (method 1)
2. Run: create_portable.bat
3. Zip the 'portable' folder
4. Distribute the ZIP file

Recommended: Use METHOD 3 (Inno Setup) for best results!
""")

if __name__ == "__main__":
    main()
