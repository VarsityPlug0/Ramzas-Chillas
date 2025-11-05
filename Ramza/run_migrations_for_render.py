#!/usr/bin/env python
"""
Script to run migrations for Render deployment.
This ensures all database tables are created properly.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

# Setup Django
django.setup()

if __name__ == '__main__':
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Also collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])