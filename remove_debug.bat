@echo off
REM --- Batch File to Delete Specific Debug Files ---
:: Optional: Set the directory to operate in (current directory if not specified)
:: If you need a specific path, uncomment and modify the line below:
:: cd /d "C:\Path\To\Your\Folder"
echo Deleting files matching debug_*.json...
del "debug_*.json" /S /Q
echo Deleting files matching debug_*.png...
del "debug_*.png" /S /Q
REM --- Remove directories (silent) ---
echo Removing temporary directories...
for /d /r . %%i in (__pycache__) do @if exist "%%i" rd /s /q "%%i" 2>nul
for /d /r . %%i in (.pytest_cache) do @if exist "%%i" rd /s /q "%%i" 2>nul
for /d /r . %%i in (66-1-k2) do @if exist "%%i" rd /s /q "%%i" 2>nul
for /d /r . %%i in (66-3-k3) do @if exist "%%i" rd /s /q "%%i" 2>nul
for /d /r . %%i in (66-6-k3) do @if exist "%%i" rd /s /q "%%i" 2>nul
for /d /r . %%i in (190-46-k2) do @if exist "%%i" rd /s /q "%%i" 2>nul
for /d /r . %%i in (190-47-k3) do @if exist "%%i" rd /s /q "%%i" 2>nul
for /d /r . %%i in (*results) do @if exist "%%i" rd /s /q "%%i" 2>nul
REM --- Remove files (silent) ---
echo Removing temporary files...
for /r . %%i in (*.pyc) do @if exist "%%i" del /q "%%i" 2>nul
for /r . %%i in (*.tmp) do @if exist "%%i" del /q "%%i" 2>nul
for /r . %%i in (*.bak) do @if exist "%%i" del /q "%%i" 2>nul
for /r . %%i in (*.log) do @if exist "%%i" del /q "%%i" 2>nul
for /r . %%i in (*.sqlite) do @if exist "%%i" del /q "%%i" 2>nul
for /r . %%i in (*.xml) do @if exist "%%i" del /q "%%i" 2>nul
for /r . %%i in (log.html) do @if exist "%%i" del /q "%%i" 2>nul
for /r . %%i in (*report.html) do @if exist "%%i" del /q "%%i" 2>nul
echo.
echo Cleanup complete.
