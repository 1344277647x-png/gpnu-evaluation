@echo off
chcp 65001 >nul 2>&1
title GPnu Evaluation

echo.
echo ========================================
echo    GPnu Course Evaluation System
echo ========================================
echo.

sc query MySQL96 | find "RUNNING" >nul 2>&1
if errorlevel 1 (
    echo [1/3] Starting MySQL...
    net start MySQL96 >nul 2>&1
) else (
    echo [1/3] MySQL already running
)

timeout /t 2 /nobreak >nul

echo [2/3] Starting backend...
taskkill /f /im pythonw.exe >nul 2>&1
start "GPnu-Backend" /MIN D:\gpnu教师评价web\venv\Scripts\pythonw.exe D:\gpnu教师评价web\backend\server.py
timeout /t 2 /nobreak >nul

echo [3/3] Detecting network...
powershell -NoProfile -Command "$ip=(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike '*Loopback*' -and $_.PrefixOrigin -ne 'WellKnown'} | Select-Object -First 1).IPAddress; Write-Host ''; Write-Host '========================================='; Write-Host '  System is READY!'; Write-Host ''; Write-Host '  Local:  http://localhost:5000'; Write-Host '  Share:  http://'$ip':5000'; Write-Host ''; Write-Host '  Admin:  admin / Admin123456'; Write-Host '========================================='; Write-Host ''"

echo Close this window to continue.
echo Run stop.bat to shut down.
echo.
pause
