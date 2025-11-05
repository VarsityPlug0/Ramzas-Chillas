#!/usr/bin/env python
"""
Deployment readiness check script for Ramza's Chillas application.
This script verifies that all necessary components are in place for deployment to Render.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status."""
    exists = os.path.exists(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_deployment_readiness():
    """Check all deployment readiness requirements."""
    print("=== Ramza's Chillas - Deployment Readiness Check ===\n")
    
    # Check required files
    print("1. Required Files Check:")
    required_files = [
        (project_dir / "render.yaml", "Render configuration file"),
        (project_dir / "requirements.txt", "Python dependencies file"),
        (project_dir / "runtime.txt", "Python runtime version file"),
        (project_dir / "Procfile", "Process file for Render"),
        (project_dir / "manage.py", "Django management script"),
        (project_dir / "start_server.py", "Start server script"),
    ]
    
    all_files_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    print()
    
    # Check required directories
    print("2. Required Directories Check:")
    required_dirs = [
        (project_dir / "fastfood_restaurant", "Main Django project directory"),
        (project_dir / "restaurant", "Restaurant app directory"),
        (project_dir / "custom_admin", "Custom admin app directory"),
        (project_dir / "templates", "Templates directory"),
        (project_dir / "static", "Static files directory"),
    ]
    
    all_dirs_exist = True
    for dirpath, description in required_dirs:
        if not check_directory_exists(dirpath, description):
            all_dirs_exist = False
    
    print()
    
    # Check media directories
    print("3. Media Directories Check:")
    media_root = project_dir / 'media'
    media_dirs = [
        (media_root, "Media root directory"),
        (media_root / 'categories', "Categories media directory"),
        (media_root / 'menu_items', "Menu items media directory"),
        (media_root / 'site', "Site media directory"),
        (media_root / 'content', "Content media directory"),
        (media_root / 'content' / 'backgrounds', "Content backgrounds directory"),
    ]
    
    all_media_dirs_exist = True
    for dirpath, description in media_dirs:
        if not check_directory_exists(dirpath, description):
            all_media_dirs_exist = False
    
    print()
    
    # Django setup and checks
    print("4. Django Configuration Check:")
    try:
        django.setup()
        print("✓ Django setup successful")
        
        # Check database migrations
        from django.core.management import execute_from_command_line
        try:
            # This will show migration status without applying them
            execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
            print("✓ Django migrations check successful")
        except Exception as e:
            print(f"⚠ Django migrations check completed with output: {e}")
            
        # Check if we can import key models
        try:
            from restaurant.models import Category, MenuItem, SiteSettings
            print("✓ Key models imported successfully")
        except Exception as e:
            print(f"✗ Error importing models: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Django setup failed: {e}")
        return False
    
    print()
    
    # Summary
    print("5. Summary:")
    if all_files_exist and all_dirs_exist and all_media_dirs_exist:
        print("✓ All deployment readiness checks passed!")
        print("✓ Application is ready for deployment to Render")
        return True
    else:
        print("✗ Some deployment readiness checks failed!")
        print("✗ Please address the issues above before deploying")
        return False

if __name__ == "__main__":
    success = check_deployment_readiness()
    sys.exit(0 if success else 1)