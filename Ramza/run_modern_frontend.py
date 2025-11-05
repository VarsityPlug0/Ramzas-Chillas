#!/usr/bin/env python
"""
Script to demonstrate how to run the modern React frontend
"""

import os
import sys
import subprocess
from pathlib import Path

def show_instructions():
    """Show instructions for running the modern frontend"""
    
    instructions = """
🚀 Ramza's Chillas - Modern Frontend Instructions
================================================

📁 Project Structure:
The modern React frontend is located in the 'frontend' directory.

📋 Setup Instructions:

1. Install Node.js dependencies:
   cd frontend
   npm install

2. Run the development server:
   npm run dev
   # This will start the React app on http://localhost:3000

3. The React app will proxy API requests to Django backend at http://localhost:8000

🔧 Alternative: Build and integrate with Django:

1. Build the React app:
   cd frontend
   npm run build

2. Integrate with Django:
   cd ..
   python build_frontend.py

3. Run Django server:
   python manage.py runserver

📱 Access Points:
- React Dev Server: http://localhost:3000
- Django Server: http://localhost:8000
- API Endpoints: http://localhost:8000/api/

📦 Key Features:
- Modern React 18 with Hooks
- Tailwind CSS for styling
- Framer Motion for animations
- React Router for navigation
- Context API for state management
- Responsive design for all devices
- Toast notifications for user feedback

⚡ Performance Benefits:
- Fast refresh development experience
- Code splitting and lazy loading
- Optimized bundle size
- Efficient state management
- Modern build tooling with Vite

For more details, check the README_MODERN.md file.
"""
    
    print(instructions)

def main():
    """Main function"""
    show_instructions()
    
    # Ask user if they want to run the setup
    response = input("\n❓ Would you like to install frontend dependencies now? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        frontend_dir = Path(__file__).parent / "frontend"
        
        if not frontend_dir.exists():
            print("❌ Frontend directory not found!")
            return
        
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        print("📦 Installing npm dependencies...")
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✅ Dependencies installed successfully!")
            print("\n🚀 To start the development server, run:")
            print("   npm run dev")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
    else:
        print("\n💡 To get started later:")
        print("   cd frontend")
        print("   npm install")
        print("   npm run dev")

if __name__ == "__main__":
    main()