#!/usr/bin/env python
"""
Complete setup script for Ramza's Chillas restaurant management system.
This script will:
1. Check if virtual environment exists, create if not
2. Install required dependencies
3. Set up the database
4. Create a superuser
5. Populate default content
6. Collect static files
7. Provide instructions for running the server
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(command, shell=False, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {' '.join(command) if isinstance(command, list) else command}")
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            check=True, 
            text=True, 
            capture_output=True,
            cwd=cwd
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def main():
    # Get project paths
    project_dir = Path(__file__).parent.absolute()
    parent_dir = project_dir.parent
    venv_dir = parent_dir / "ramzas_env"
    
    print(f"Project directory: {project_dir}")
    print(f"Virtual environment directory: {venv_dir}")
    print()
    
    # Check if virtual environment exists, create if not
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        print("Virtual environment created successfully!")
        print()
    else:
        print("Virtual environment already exists.")
        print()
    
    # Determine the Python executable in the virtual environment
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
    
    if not python_exe.exists():
        print(f"Error: Python executable not found at {python_exe}")
        return False
    
    # Upgrade pip
    print("Upgrading pip...")
    if not run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"]):
        print("Failed to upgrade pip")
        return False
    print()
    
    # Install requirements
    print("Installing requirements...")
    requirements_file = project_dir / "requirements.txt"
    if not run_command([str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)]):
        print("Failed to install requirements")
        return False
    print()
    
    # Run migrations
    print("Running database migrations...")
    if not run_command([str(python_exe), "manage.py", "migrate"], cwd=project_dir):
        print("Failed to run migrations")
        return False
    print()
    
    # Create superuser
    print("Creating superuser...")
    create_superuser_cmd = [
        str(python_exe), "manage.py", "shell", "-c",
        "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(is_superuser=True).exists() else print('Superuser already exists')"
    ]
    if not run_command(create_superuser_cmd, cwd=project_dir):
        print("Warning: Could not create superuser")
    print()
    
    # Populate default content
    print("Populating default content...")
    if not run_command([str(python_exe), "manage.py", "populate_content"], cwd=project_dir):
        print("Warning: Could not populate default content")
    print()
    
    # Collect static files
    print("Collecting static files...")
    if not run_command([str(python_exe), "manage.py", "collectstatic", "--noinput"], cwd=project_dir):
        print("Warning: Could not collect static files")
    print()
    
    # Provide instructions
    print("="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print()
    print("To run the development server, you can either:")
    print()
    print("1. Double-click the 'start_local.bat' file")
    print()
    print("2. Or run these commands manually:")
    print(f"   cd {project_dir}")
    if sys.platform == "win32":
        print(f"   ..\\ramzas_env\\Scripts\\activate.bat")
    else:
        print(f"   source ../ramzas_env/bin/activate")
    print("   python manage.py runserver")
    print()
    print("Then open your browser to:")
    print("  Home: http://127.0.0.1:8000/")
    print("  Admin: http://127.0.0.1:8000/admin/")
    print()
    print("Login with admin / admin123")
    print()
    print("Press Enter to exit...")
    input()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nSetup failed. Please check the output above.")
        input("Press Enter to exit...")
        sys.exit(1)