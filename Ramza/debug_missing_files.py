#!/usr/bin/env python
"""
Script to debug specific missing files
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

def debug_missing_files():
    """Debug specific missing files"""
    print("=== Debugging Specific Missing Files ===")
    
    # Check for specific problematic filenames
    problematic_files = [
        'crack_burgers_-.jpeg',
        'Crispy_Fried_Samosa_Triangles.jpeg'
    ]
    
    print("\n--- Checking for problematic filenames in database ---")
    for filename in problematic_files:
        print(f"Looking for: {filename}")
        
        # Check in categories
        categories = Category.objects.all()
        found_in_categories = []
        for category in categories:
            if category.image and filename in str(category.image):
                found_in_categories.append(category)
                print(f"  Found in Category: {category.name} (ID: {category.id})")
                print(f"    Image field: {category.image}")
                print(f"    Image path: {category.image.path if category.image else 'None'}")
                print(f"    File exists: {os.path.exists(category.image.path) if category.image and category.image.path else 'N/A'}")
                
        # Check in menu items
        menu_items = MenuItem.objects.all()
        found_in_items = []
        for item in menu_items:
            if item.image and filename in str(item.image):
                found_in_items.append(item)
                print(f"  Found in Menu Item: {item.name} (ID: {item.id})")
                print(f"    Image field: {item.image}")
                print(f"    Image path: {item.image.path if item.image else 'None'}")
                print(f"    File exists: {os.path.exists(item.image.path) if item.image and item.image.path else 'N/A'}")
        
        if not found_in_categories and not found_in_items:
            print(f"  Not found in database")
    
    # Check what files actually exist in media directories
    print("\n--- Actual files in media directories ---")
    media_dirs = ['media/categories', 'media/menu_items']
    for media_dir in media_dirs:
        if os.path.exists(media_dir):
            print(f"Directory: {media_dir}")
            files = os.listdir(media_dir)
            for file in files:
                print(f"  {file}")
        else:
            print(f"Directory does not exist: {media_dir}")

if __name__ == "__main__":
    debug_missing_files()