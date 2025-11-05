#!/usr/bin/env python
"""
Test script to verify static file serving
"""
import os
import django
from django.conf import settings
from django.contrib.staticfiles import finders

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

def test_static_files():
    print("=== Static File Serving Test ===")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'Not set')}")
    
    # Check if static directory exists
    static_root = str(settings.STATIC_ROOT)
    if os.path.exists(static_root):
        print(f"Static root directory exists: {static_root}")
        # Count files in static root
        file_count = 0
        for root, dirs, files in os.walk(static_root):
            file_count += len(files)
        print(f"Total files in static root: {file_count}")
    else:
        print(f"Static root directory does not exist: {static_root}")
        
    # Check if our specific static files exist
    default_category_path = finders.find('images/default-category.jpg')
    default_menu_item_path = finders.find('images/default-menu-item.jpg')
    
    print(f"default-category.jpg found at: {default_category_path}")
    print(f"default-menu-item.jpg found at: {default_menu_item_path}")
    
    # Check if files exist in staticfiles directory
    staticfiles_default_category = os.path.join(static_root, 'images', 'default-category.jpg')
    staticfiles_default_menu_item = os.path.join(static_root, 'images', 'default-menu-item.jpg')
    
    print(f"Staticfiles default-category.jpg exists: {os.path.exists(staticfiles_default_category)}")
    print(f"Staticfiles default-menu-item.jpg exists: {os.path.exists(staticfiles_default_menu_item)}")

if __name__ == "__main__":
    test_static_files()