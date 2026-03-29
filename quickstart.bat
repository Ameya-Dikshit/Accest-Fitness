@echo off
REM Quick Start Script for ACEest Fitness API (Windows)

echo.
echo 🚀 ACEest Fitness API - Quick Start
echo ====================================
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version
echo.

REM Create virtual environment
echo ✓ Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo   Virtual environment created
) else (
    echo   Virtual environment already exists
)
echo.

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat
echo   Virtual environment activated
echo.

REM Install dependencies
echo ✓ Installing dependencies...
python -m pip install --upgrade pip > nul 2>&1
pip install -r requirements.txt > nul 2>&1
echo   Dependencies installed
echo.

REM Initialize database
echo ✓ Initializing database...
python -c "from app import init_db; init_db()" 2>nul
echo   Database initialized
echo.

REM Display startup instructions
echo ====================================
echo ✅ Setup Complete!
echo ====================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate.bat
echo   set FLASK_DEBUG=True
echo   flask run
echo.
echo Or run in production mode:
echo   gunicorn --bind 0.0.0.0:5000 app:app
echo.
echo API will be available at: http://localhost:5000
echo.
echo Run tests with:
echo   pytest tests/ -v
echo.

pause
