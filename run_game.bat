@echo off

REM Change to the directory of the batch file (assumes the USB stick is the current drive)
cd /d "%~dp0"

REM Activate the Python environment (adjust the path to the environment if necessary)
call .\env\Scripts\activate.bat

REM Run the Python script
python main.py

REM Deactivate the Python environment after execution
deactivate

REM Pause to keep the command window open after execution
pause