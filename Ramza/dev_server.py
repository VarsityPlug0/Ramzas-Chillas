#!/usr/bin/env python
"""
Script to run both Django backend and React frontend in development mode
"""

import os
import sys
import subprocess
import threading
from pathlib import Path

def run_django_server():
    """Run Django development server"""
    try:
        subprocess.run([
            "python", "manage.py", "runserver"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Django server error: {e}")
    except KeyboardInterrupt:
        print(" Django server stopped")

def run_react_dev_server():
    """Run React development server"""
    try:
        # Change to frontend directory
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        subprocess.run([
            "npm", "run", "dev"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ React dev server error: {e}")
    except KeyboardInterrupt:
        print(" React dev server stopped")

def main():
    """Main function to run both servers"""
    print("🚀 Starting Ramza's Chillas Development Servers")
    print("=" * 50)
    
    # Start Django server in a separate thread
    django_thread = threading.Thread(target=run_django_server)
    django_thread.daemon = True
    django_thread.start()
    
    print("🔧 Django server started on http://127.0.0.1:8000")
    
    # Run React dev server in main thread
    print("🔧 Starting React development server...")
    run_react_dev_server()
    
    print("\n🛑 Development servers stopped")

if __name__ == "__main__":
    main()