@echo off
setlocal

:menu
cls
echo.
type banner.txt
echo.
echo ================================
echo.             MENU
echo ================================
echo 1. Launch script
echo 2. Start install requirements file
echo 3. EXIT
echo ================================
set /p choice="Please select an option (1-3): "

if "%choice%"=="1" (
    goto option1
) else if "%choice%"=="2" (
    goto option2
) else if "%choice%"=="3" (
    goto option3
) else (
    echo Invalid choice! Please select a valid option.
    pause
    goto menu
)

:option1
echo Starting script...
python main.py
goto end

:option2
echo Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo An error occurred during the installation.
) else (
    echo Finished installing requirements!
)
pause
goto menu

:option3
goto end

:end
echo EXIT...
endlocal
