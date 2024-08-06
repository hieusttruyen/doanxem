@echo off 
echo Run.....

@echo off
:: Kiểm tra xem file có đang chạy với quyền admin hay không
openfiles >nul 2>&1
if %errorlevel% NEQ 0 (
    :: Nếu không, yêu cầu quyền admin và chạy lại chính file này
    echo Requesting administrative privileges...
    powershell start-process "%~f0" -verb runas
    exit /b
)


:: Đổi tên cửa sổ CMD
title cmd_rokauto
:: Nếu có quyền admin, thiết lập kích thước cửa sổ CMD
@REM mode con: cols=30 lines=40

:: Chuyển đến thư mục chứa file batch
cd /d "%~dp0"

:: Chạy file main.py với Python
python main.py

pause
