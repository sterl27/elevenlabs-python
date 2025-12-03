# ElevenLabs Studio Launcher for Windows
# Run this script to start the ElevenLabs Studio application

Write-Host "🎤 ElevenLabs Studio Launcher" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment active: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "⚠️  No virtual environment detected. It's recommended to use a venv." -ForegroundColor Yellow
    $response = Read-Host "Continue anyway? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Install requirements
Write-Host "📦 Installing/updating requirements..." -ForegroundColor Blue
try {
    pip install streamlit elevenlabs python-dotenv asyncio websockets pydantic typing-extensions
    Write-Host "✅ Requirements installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install requirements" -ForegroundColor Red
    exit 1
}

# Launch the application
Write-Host "🚀 Starting ElevenLabs Studio..." -ForegroundColor Blue
Write-Host "The app will open in your browser at http://localhost:8501" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

try {
    streamlit run app.py --server.port 8501 --server.headless false
} catch {
    Write-Host "❌ Failed to start the application" -ForegroundColor Red
    Write-Host "Make sure you're in the studio_app directory" -ForegroundColor Yellow
    exit 1
}
