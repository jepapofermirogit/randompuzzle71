#!/usr/bin/env python3
"""
Startup script for the All Bitcoin Private Key application
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import requests
        import ecdsa
        import base58
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def main():
    """Main startup function"""
    print("=" * 50)
    print("All Bitcoin Private Key - Python Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\nStarting the application...")
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Start the Flask application with better error handling
        result = subprocess.run([sys.executable, "app.py"], 
                              capture_output=False, 
                              text=True)
        if result.returncode != 0:
            print(f"\nApplication exited with code: {result.returncode}")
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user")
    except OSError as e:
        if hasattr(e, 'winerror') and e.winerror == 10038:
            print("\n" + "="*60)
            print("⚠️  Windows Socket Error Detected")
            print("="*60)
            print("This is a known issue with Flask's development server on Windows.")
            print("\n🔧 Try these solutions:")
            print("1. Run the application again")
            print("2. Change the port in config.py (FLASK_PORT)")
            print("3. Use Flask CLI: python -m flask run")
            print("4. Restart your terminal/command prompt")
            print("="*60)
        else:
            print(f"\nError starting application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
