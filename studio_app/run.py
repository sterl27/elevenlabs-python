#!/usr/bin/env python3
"""
Launch script for ElevenLabs Studio App
"""

import os
import subprocess
import sys
from pathlib import Path


def install_requirements():
    """Install required packages"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        print("Installing requirements...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
    else:
        print("Requirements file not found. Installing basic packages...")
        packages = [
            "streamlit>=1.28.0",
            "elevenlabs",
            "python-dotenv"
        ]
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """Main function to launch the app"""
    # Change to app directory
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    # Install requirements if needed
    try:
        import streamlit

        import elevenlabs
    except ImportError:
        print("Missing dependencies. Installing...")
        install_requirements()
    
    # Launch Streamlit app
    print("Starting ElevenLabs Studio...")
    print("App will open in your default browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\nShutting down ElevenLabs Studio...")
    except Exception as e:
        print(f"Error launching app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
