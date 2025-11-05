#!/usr/bin/env python
"""
Script to fix media file references in the database.
This script will:
1. Check all Category and MenuItem records for missing image files
2. Clear references to missing files
3. Optionally replace with default images
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from restaurant.models import Category, MenuItem

def fix_media_references():
    """Fix references to missing media files"""
    print("Checking for missing media files...")
    
    # Check Category images
    categories = Category.objects.all()
    fixed_categories = 0
    
    for category in categories:
        if category.image:
            image_path = category.image.path
            if not os.path.exists(image_path):
                print(f"Category '{category.name}' references missing image: {category.image}")
                # Clear the reference to the missing image
                category.image = None
                category.save()
                fixed_categories += 1
                print(f"  -> Cleared reference to missing image")
    
    print(f"Fixed {fixed_categories} categories with missing images")
    
    # Check MenuItem images
    menu_items = MenuItem.objects.all()
    fixed_items = 0
    
    for item in menu_items:
        if item.image:
            image_path = item.image.path
            if not os.path.exists(image_path):
                print(f"Menu Item '{item.name}' references missing image: {item.image}")
                # Clear the reference to the missing image
                item.image = None
                item.save()
                fixed_items += 1
                print(f"  -> Cleared reference to missing image")
    
    print(f"Fixed {fixed_items} menu items with missing images")
    print(f"Total fixed records: {fixed_categories + fixed_items}")

if __name__ == "__main__":
    fix_media_references()