#!/usr/bin/env python
"""
Test script to verify media file serving configuration
"""
import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

def test_media_configuration():
    print("=== Media Configuration Test ===")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    
    # Check if media directory exists
    media_root = str(settings.MEDIA_ROOT)  # Convert Path to string
    if os.path.exists(media_root):
        print(f"Media directory exists: {media_root}")
        # List files in media directory
        for root, dirs, files in os.walk(media_root):
            level = root.replace(media_root, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    else:
        print(f"Media directory does not exist: {media_root}")
        
    # Check if static directory exists
    static_root = str(settings.STATIC_ROOT)  # Convert Path to string
    if os.path.exists(static_root):
        print(f"Static directory exists: {static_root}")
    else:
        print(f"Static directory does not exist: {static_root}")

if __name__ == "__main__":
    test_media_configuration()