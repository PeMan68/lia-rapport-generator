@echo off
REM Byggscript för LIA Rapportgenerator
REM Bygger exe-fil med PyInstaller med korrekt konfiguration

echo ================================================
echo   LIA Rapportgenerator - Byggscript
echo ================================================
echo.

REM Kontrollera att PyInstaller är installerat
echo [0/3] Kontrollerar PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo       PyInstaller saknas - installerar nu...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo.
        echo ================================================
        echo   FEL: Kunde inte installera PyInstaller!
        echo ================================================
        echo   Forsok manuellt: pip install pyinstaller
        echo ================================================
        pause
        exit /b 1
    )
    echo       OK! PyInstaller installerat.
) else (
    echo       OK! PyInstaller ar redan installerat.
)
echo.

REM Ta bort gamla build-filer
echo [1/3] Rensar gamla build-filer...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo       OK!
echo.

REM Bygg exe-fil med spec-filen
echo [2/3] Bygger exe-fil...
echo       Detta kan ta nagra minuter...
python -m PyInstaller LIA_Rapportgenerator.spec
if errorlevel 1 (
    echo.
    echo ================================================
    echo   FEL: PyInstaller misslyckades!
    echo ================================================
    pause
    exit /b 1
)
echo       OK!
echo.

REM Kontrollera att bygget lyckades
if exist "dist\LIA_Rapportgenerator.exe" (
    echo [3/3] Bygget klart!
    echo.
    echo ================================================
    echo   LYCKAT!
    echo ================================================
    echo   Exe-fil skapad: dist\LIA_Rapportgenerator.exe
    echo.
    echo   Du kan nu kopiera filen och dela den.
    echo   Testa: dist\LIA_Rapportgenerator.exe
    echo ================================================
) else (
    echo [3/3] FEL!
    echo.
    echo ================================================
    echo   BYGGET MISSLYCKADES
    echo ================================================
    echo   Kontrollera felmeddelanden ovan.
    echo ================================================
)

echo.
pause
