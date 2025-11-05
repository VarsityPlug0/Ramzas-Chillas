#!/usr/bin/env python
"""
Script to debug image URLs and check for specific problematic filenames
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

def debug_image_urls():
    """Debug image URLs and check for specific filenames"""
    print("=== Debugging Image URLs ===")
    
    # Check for specific problematic filenames
    problematic_files = [
        'Crispy_Fried_Samosa_Triangles.jpeg',
        'crack_burgers_-.jpeg'
    ]
    
    print("\n--- Checking for problematic filenames ---")
    for filename in problematic_files:
        print(f"Looking for: {filename}")
        
        # Check in categories
        categories = Category.objects.all()
        for category in categories:
            if category.image and filename in str(category.image):
                print(f"  Found in Category: {category.name}")
                
        # Check in menu items
        menu_items = MenuItem.objects.all()
        for item in menu_items:
            if item.image and filename in str(item.image):
                print(f"  Found in Menu Item: {item.name}")
    
    # Check what the actual URLs should be
    print("\n--- Actual Database References ---")
    categories = Category.objects.all()
    for i, category in enumerate(categories):
        print(f"Category {i+1}: {category.name}")
        if category.image:
            print(f"  Image field: {category.image}")
            print(f"  Image URL: {category.image.url}")
        else:
            print(f"  No image")
        print()
    
    # Check if media files exist
    print("\n--- Media Directory Contents ---")
    media_dirs = ['media/categories', 'media/menu_items']
    for media_dir in media_dirs:
        if os.path.exists(media_dir):
            print(f"Directory: {media_dir}")
            files = os.listdir(media_dir)
            for file in files:
                print(f"  {file}")
        else:
            print(f"Directory does not exist: {media_dir}")
        print()

if __name__ == "__main__":
    debug_image_urls()