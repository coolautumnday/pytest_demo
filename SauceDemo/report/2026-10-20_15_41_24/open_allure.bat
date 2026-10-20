@echo off
    chcp 65001 >nul
    cd /d "%~dp0"
    allure open -h 127.0.0.1 -p 8083 allure-report
    pause
    