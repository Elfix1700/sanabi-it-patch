@echo off
rem Avvia la patch italiana per SANABI su Windows.
rem Uso:  run_windows.bat --apply
rem       run_windows.bat --check
rem       run_windows.bat --restore
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo ERRORE: installa Python 3 da https://www.python.org/downloads/
    echo e durante l'installazione spunta "Add Python to PATH".
    pause
    exit /b 1
)

python -c "import UnityPy" >nul 2>&1
if errorlevel 1 (
    echo UnityPy non trovato. Installazione in corso...
    python -m pip install UnityPy
    if errorlevel 1 (
        echo ERRORE: installa UnityPy a mano con:  pip install UnityPy
        pause
        exit /b 1
    )
)

python patcher\patch_sanabi_it.py %*
pause
