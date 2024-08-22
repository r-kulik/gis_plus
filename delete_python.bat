@echo off
setlocal

REM Path to Python installation
set PYTHON_INSTALL_PATH=C:\Python312

REM Uninstall Python
echo Uninstalling Python 3.12.5...
wmic product where "Name like 'Python%%3.12.5%%'" call uninstall /nointeractive

REM Remove Python from PATH
echo Removing Python from PATH...
setx /M PATH "%PATH:C:\Python312\;=%"

REM Delete Python installation directory
echo Deleting Python installation directory...
rmdir /s /q %PYTHON_INSTALL_PATH%

echo Python 3.12.5 has been successfully removed.

endlocal