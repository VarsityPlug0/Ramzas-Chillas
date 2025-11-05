#!/usr/bin/env python
"""
Script to clear image cache and check for database inconsistencies
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from django.core.cache import cache
from restaurant.models import Category, MenuItem

def clear_image_cache():
    """Clear any cached image references"""
    print("=== Clearing Image Cache ===")
    
    # Clear Django cache
    try:
        cache.clear()
        print("Django cache cleared successfully")
    except Exception as e:
        print(f"Could not clear Django cache: {e}")
    
    # Check for any categories or menu items with missing images
    print("\n=== Checking for Database Inconsistencies ===")
    
    # Check categories
    categories = Category.objects.all()
    inconsistent_categories = []
    
    for category in categories:
        if category.image:
            image_path = category.image.path
            if not os.path.exists(image_path):
                print(f"Category '{category.name}' has reference to missing image: {category.image}")
                inconsistent_categories.append(category)
    
    # Check menu items
    menu_items = MenuItem.objects.all()
    inconsistent_items = []
    
    for item in menu_items:
        if item.image:
            image_path = item.image.path
            if not os.path.exists(image_path):
                print(f"Menu Item '{item.name}' has reference to missing image: {item.image}")
                inconsistent_items.append(item)
    
    # Report findings
    print(f"\nFound {len(inconsistent_categories)} categories with missing images")
    print(f"Found {len(inconsistent_items)} menu items with missing images")
    
    if inconsistent_categories or inconsistent_items:
        print("\nRecommendation: Run the fix_media_references.py script to clear these references")
    else:
        print("\nNo database inconsistencies found")
    
    # Show current image references
    print("\n=== Current Image References ===")
    print("Categories:")
    for category in categories:
        if category.image:
            print(f"  {category.name}: {category.image.url}")
        else:
            print(f"  {category.name}: No image")
    
    print("\nMenu Items:")
    for item in menu_items:
        if item.image:
            print(f"  {item.name}: {item.image.url}")
        else:
            print(f"  {item.name}: No image")

if __name__ == "__main__":
    clear_image_cache()