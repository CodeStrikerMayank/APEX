@echo off
setlocal enabledelayedexpansion
title APEX - Offline Adaptive Learning Hub
color 0B

echo ===============================================================================
echo            APEX: ADAPTIVE PSYCHOMETRIC EXAM SYSTEM (OFFLINE HUB)
echo ===============================================================================
echo.
echo [*] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python was not found in your system PATH.
    echo     Please install Python 3.10+ from python.org or the Microsoft Store.
    echo.
    pause
    exit /b 1
)

echo [*] Python detected. Checking if APEX server is already running...
powershell -NoProfile -Command "try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 2 -UseBasicParsing; if ($res.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] APEX server is ALREADY running on port 8000!
    echo [*] Opening browser at http://127.0.0.1:8000 ...
    start http://127.0.0.1:8000
    goto :RUNNING_INFO
)

echo [*] Starting APEX offline backend server (FastAPI + SQLite WAL)...
start /b python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > "scratch\server.log" 2>&1

echo [*] Waiting for server to initialize...
set /a attempts=0
:WAIT_LOOP
set /a attempts+=1
if !attempts! gtr 15 (
    echo [!] Warning: Server startup took longer than expected.
    echo     Checking log file 'scratch\server.log' ...
    goto :OPEN_BROWSER
)
timeout /t 1 /nobreak >nul
powershell -NoProfile -Command "try { $res = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 1 -UseBasicParsing; if ($res.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel% neq 0 goto :WAIT_LOOP

:OPEN_BROWSER
echo [*] Server is ONLINE and HEALTHY!
echo [*] Launching your default web browser...
start http://127.0.0.1:8000

:RUNNING_INFO
echo.
echo ===============================================================================
echo   APEX IS RUNNING 100%% OFFLINE!
echo ===============================================================================
echo   Local Web Address : http://127.0.0.1:8000
echo   Alternate Address : http://localhost:8000
echo.
echo   To access from your mobile phone or tablet on the same Wi-Fi:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set "ip=%%a"
    set "ip=!ip: =!"
    echo   Mobile / LAN URL  : http://!ip!:8000
)
echo.
echo   [!] Keep this window open while using APEX.
echo   [!] To stop the server, press Ctrl+C or simply close this window.
echo ===============================================================================
echo.

:: Keep running and wait for user to close
echo Press any key to stop the server and exit...
pause >nul

:: Cleanup background process if started
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [*] APEX server stopped cleanly.
timeout /t 2 >nul
exit /b 0
