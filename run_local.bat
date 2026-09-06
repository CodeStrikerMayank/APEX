@echo off
title APEX Student Intelligence Engine
echo ========================================================
echo   Launching APEX Student Hub (Instant Offline Mode)
echo ========================================================
echo   Local Address: http://127.0.0.1:8000
echo   Zero-latency, no cloud spin-down wait.
echo ========================================================

start http://127.0.0.1:8000
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
pause
