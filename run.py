#!/usr/bin/env python3
"""
AI Research Assistant - Multi-Agent System
Main entry point for the application
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import langchain
        import openai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if OpenAI API key is configured"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("Please set your API key:")
        print("export OPENAI_API_KEY=your_api_key_here")
        return False
    print("✅ OpenAI API key is configured")
    return True

def main():
    """Main function to run the application"""
    print("🔬 AI Research Assistant - Multi-Agent System")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    # Run Streamlit app
    print("🚀 Starting the application...")
    try:
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
