@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  start "" "http://127.0.0.1:8000/"
  py -3 server.py
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    start "" "http://127.0.0.1:8000/"
    python server.py
  ) else (
    echo Please install Python 3.10 or later, then run this file again.
    pause
  )
)
