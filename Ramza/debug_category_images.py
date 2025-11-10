#!/usr/bin/env python
"""
Script to debug category images and identify issues
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

# Add current directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    django.setup()
    print("Django setup completed successfully")
except Exception as e:
    print(f"Error during Django setup: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import models
from restaurant.models import Category

def debug_category_images():
    """Debug category images and identify issues"""
    
    print("Checking category images...")
    
    # Get all categories
    categories = Category.objects.all()
    print(f"Found {len(categories)} categories")
    
    for category in categories:
        print(f"\nCategory: {category.name}")
        print(f"  Description: {category.description}")
        print(f"  Is active: {category.is_active}")
        
        if category.image:
            print(f"  Image field: {category.image}")
            try:
                print(f"  Image URL: {category.image.url}")
                print(f"  Image path: {category.image.path}")
                file_exists = os.path.exists(category.image.path)
                print(f"  File exists: {file_exists}")
                
                if file_exists:
                    file_size = os.path.getsize(category.image.path)
                    print(f"  File size: {file_size} bytes")
                    
                    # Check if file is corrupted (0 bytes or too small)
                    if file_size == 0:
                        print(f"  ⚠️  WARNING: Image file is empty!")
                    elif file_size < 100:  # Less than 100 bytes is suspicious
                        print(f"  ⚠️  WARNING: Image file is unusually small!")
                else:
                    print(f"  ❌ ERROR: Image file does not exist!")
                    
            except Exception as e:
                print(f"  ❌ ERROR accessing image: {e}")
        else:
            print(f"  ℹ️  No image assigned")

if __name__ == "__main__":
    debug_category_images()