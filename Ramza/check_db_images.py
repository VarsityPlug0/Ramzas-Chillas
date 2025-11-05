#!/usr/bin/env python
"""
Script to check database image references
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

def check_db_images():
    """Check what image references are stored in the database"""
    print("=== Database Image References ===")
    
    # Check Category images
    print("\n--- Categories ---")
    categories = Category.objects.all()
    for category in categories:
        if category.image:
            print(f"Category: {category.name}")
            print(f"  Image field: {category.image}")
            print(f"  Image path: {category.image.path if category.image else 'None'}")
            print(f"  Image URL: {category.image.url if category.image else 'None'}")
            print(f"  File exists: {os.path.exists(category.image.path) if category.image and category.image.path else 'N/A'}")
            print()
        else:
            print(f"Category: {category.name} - No image")
    
    # Check MenuItem images
    print("\n--- Menu Items ---")
    menu_items = MenuItem.objects.all()
    for item in menu_items:
        if item.image:
            print(f"Menu Item: {item.name}")
            print(f"  Image field: {item.image}")
            print(f"  Image path: {item.image.path if item.image else 'None'}")
            print(f"  Image URL: {item.image.url if item.image else 'None'}")
            print(f"  File exists: {os.path.exists(item.image.path) if item.image and item.image.path else 'N/A'}")
            print()
        else:
            print(f"Menu Item: {item.name} - No image")

if __name__ == "__main__":
    check_db_images()