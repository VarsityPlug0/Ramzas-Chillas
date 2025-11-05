#!/usr/bin/env python
"""
Test script to verify static file configuration
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

def test_static_config():
    """Test static file configuration"""
    print("=== Static File Configuration Test ===")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"DEBUG: {settings.DEBUG}")
    
    if hasattr(settings, 'WHITENOISE_STATIC_PREFIX'):
        print(f"WHITENOISE_STATIC_PREFIX: {settings.WHITENOISE_STATIC_PREFIX}")
    
    print("\n=== Checking Static File Finder ===")
    # Test finding a static file
    result = finders.find('images/default-category.jpg')
    print(f"Found default-category.jpg at: {result}")
    
    result = finders.find('images/default-menu-item.jpg')
    print(f"Found default-menu-item.jpg at: {result}")
    
    print("\n=== Checking Static Files Storage ===")
    try:
        url = staticfiles_storage.url('images/default-category.jpg')
        print(f"URL for default-category.jpg: {url}")
    except Exception as e:
        print(f"Error getting URL for default-category.jpg: {e}")
        
    try:
        url = staticfiles_storage.url('images/default-menu-item.jpg')
        print(f"URL for default-menu-item.jpg: {url}")
    except Exception as e:
        print(f"Error getting URL for default-menu-item.jpg: {e}")

if __name__ == '__main__':
    test_static_config()