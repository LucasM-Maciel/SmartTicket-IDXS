@echo off
REM Run pytest from the repository root.
REM Usage and examples: see scripts/retest.md
cd /d "%~dp0.."
python -m pytest %*
exit /b %ERRORLEVEL%
