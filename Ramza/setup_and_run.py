#!/usr/bin/env python
"""
Setup and run script for Ramza's Chillas restaurant management system.
This script will:
1. Install required dependencies
2. Set up the database
3. Create a superuser
4. Populate default content
5. Start the development server
"""

import os
import sys
import subprocess
import platform

def run_command(command, shell=False):
    """Run a command and return the result"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            check=True, 
            text=True, 
            capture_output=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"Working in directory: {project_dir}")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("Note: Not running in a virtual environment")
        print("Consider creating and activating a virtual environment first:")
        print("  python -m venv venv")
        print("  venv\\Scripts\\activate  (Windows)")
        print("  source venv/bin/activate  (Linux/Mac)")
        print()
    
    # Upgrade pip
    print("Upgrading pip...")
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"]):
        print("Failed to upgrade pip")
        return False
    
    # Install requirements
    print("Installing requirements...")
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]):
        print("Failed to install requirements")
        return False
    
    # Run migrations
    print("Running database migrations...")
    if not run_command([sys.executable, "manage.py", "migrate"]):
        print("Failed to run migrations")
        return False
    
    # Create superuser
    print("Creating superuser...")
    create_superuser_cmd = [
        sys.executable, "manage.py", "shell", "-c",
        "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(is_superuser=True).exists() else print('Superuser already exists')"
    ]
    if not run_command(create_superuser_cmd):
        print("Warning: Could not create superuser")
    
    # Populate default content
    print("Populating default content...")
    if not run_command([sys.executable, "manage.py", "populate_content"]):
        print("Warning: Could not populate default content")
    
    # Collect static files
    print("Collecting static files...")
    if not run_command([sys.executable, "manage.py", "collectstatic", "--noinput"]):
        print("Warning: Could not collect static files")
    
    # Start the development server
    print("\n" + "="*50)
    print("Setup complete! Starting development server...")
    print("Admin: http://127.0.0.1:8000/admin/")
    print("Home: http://127.0.0.1:8000/")
    print("Login with admin / admin123")
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\nServer setup and run completed successfully!")
    else:
        print("\nThere were errors during setup. Please check the output above.")
        sys.exit(1)