#!/bin/bash
# Quick Start Script for ACEest Fitness API

set -e

echo "🚀 ACEest Fitness API - Quick Start"
echo "===================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "  Found Python: $python_version"

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  Virtual environment activated"

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "  Dependencies installed"

# Initialize database
echo ""
echo "✓ Initializing database..."
python -c "from app import init_db; init_db()" 2>/dev/null || true
echo "  Database initialized"

# Display startup instructions
echo ""
echo "===================================="
echo "✅ Setup Complete!"
echo "===================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  export FLASK_DEBUG=True"
echo "  flask run"
echo ""
echo "Or run in production mode:"
echo "  gunicorn --bind 0.0.0.0:5000 app:app"
echo ""
echo "API will be available at: http://localhost:5000"
echo ""
echo "Run tests with:"
echo "  pytest tests/ -v"
echo ""
