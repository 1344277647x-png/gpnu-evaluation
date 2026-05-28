@echo off
chcp 65001 >nul
title 停止 GPnu 评价系统

echo 正在停止后端服务...
taskkill /f /im pythonw.exe /fi "WINDOWTITLE eq GPnu-Backend*" 2>nul
taskkill /f /fi "WINDOWTITLE eq GPnu-Backend*" 2>nul

echo 后端已停止。
echo MySQL 服务仍在运行（系统服务，不关闭）。
pause
