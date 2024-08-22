@echo off
setlocal

REM Path to Python installer
set PYTHON_INSTALLER=python-3.12.5-amd64.exe

REM Path to your project directory
set PROJECT_DIR=%CD%

REM Name of the virtual environment
set VENV_NAME=venv

REM Install Python
echo Installing Python...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if %errorlevel% neq 0 (
    echo Failed to install Python. Please check the installer and try again.
    exit /b 1
)
echo Python installed successfully.

REM Add Python to PATH manually
set PATH=%PATH%;C:\Python312\

REM Check if virtual environment folder already exists
if exist %VENV_NAME% (
    echo Virtual environment folder already exists. Deleting it...
    rmdir /s /q %VENV_NAME%
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv %VENV_NAME%
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Please check your Python installation and try again.
    exit /b 1
)

REM Check if virtual environment folder exists
if not exist %VENV_NAME% (
    echo Virtual environment folder not found. Exiting...
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call %VENV_NAME%\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
%VENV_NAME%\Scripts\pip.exe install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Please check requirements.txt and try again.
    exit /b 1
)

REM Flush and migrate database (assuming Django project)
echo Flushing and migrating database...
%VENV_NAME%\Scripts\python.exe manage.py flush --noinput
if %errorlevel% neq 0 (
    echo Failed to flush database. Please check your Django settings and try again.
    exit /b 1
)
%VENV_NAME%\Scripts\python.exe manage.py migrate
if %errorlevel% neq 0 (
    echo Failed to migrate database. Please check your Django settings and try again.
    exit /b 1
)

REM Run server on localhost
echo Running server on localhost...
%VENV_NAME%\Scripts\python.exe manage.py runserver

endlocal