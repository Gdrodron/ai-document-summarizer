@echo off
echo.
echo ===== Railway Auto Deploy =====
echo.

git add .

set /p msg=Commit message: 

git commit -m "%msg%"

if errorlevel 1 (
    echo.
    echo Commit failed.
    pause
    exit /b
)

git push origin main

echo.
echo ===============================
echo Push successful!
echo Railway will now deploy automatically.
echo ===============================

pause