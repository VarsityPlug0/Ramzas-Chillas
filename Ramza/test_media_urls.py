#!/usr/bin/env python
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

# Test the media URLs
from restaurant.models import MenuItem
from django.conf import settings

print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"BASE_DIR: {settings.BASE_DIR}")

# Get all menu items and check their URLs
menu_items = MenuItem.objects.all()
print(f"\nFound {len(menu_items)} menu items")

for item in menu_items:
    if item.image:
        print(f"{item.name}:")
        print(f"  Image field: {item.image}")
        print(f"  Image URL: {item.image.url}")
        print(f"  Image path: {item.image.path}")
        print(f"  File exists: {os.path.exists(item.image.path)}")
        print()