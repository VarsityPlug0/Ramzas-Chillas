#!/usr/bin/env python
"""
Test script to verify media file serving fix
"""
import os
import django
from django.conf import settings
from django.urls import reverse

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

def test_media_serving():
    print("=== Media Serving Fix Test ===")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Check if media directory exists
    media_root = str(settings.MEDIA_ROOT)
    if os.path.exists(media_root):
        print(f"Media directory exists: {media_root}")
        # Count media files
        file_count = 0
        for root, dirs, files in os.walk(media_root):
            file_count += len(files)
        print(f"Total media files: {file_count}")
        
        # List some example files
        print("Sample media files:")
        for root, dirs, files in os.walk(media_root):
            for file in files[:5]:  # Show first 5 files
                print(f"  {os.path.join(root, file)}")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more files")
            break
    else:
        print(f"Media directory does not exist: {media_root}")
        print("Creating media directory...")
        os.makedirs(media_root, exist_ok=True)
        print("Media directory created")
    
    # Test URL patterns
    try:
        from fastfood_restaurant.urls import urlpatterns
        print(f"Total URL patterns: {len(urlpatterns)}")
        
        # Check if media URL pattern exists
        media_pattern_found = False
        for pattern in urlpatterns:
            if hasattr(pattern, 'pattern') and 'media' in str(pattern.pattern):
                media_pattern_found = True
                print(f"Media URL pattern found: {pattern.pattern}")
                break
        
        if not media_pattern_found:
            print("WARNING: No media URL pattern found!")
            
    except Exception as e:
        print(f"Error checking URL patterns: {e}")

if __name__ == "__main__":
    test_media_serving()