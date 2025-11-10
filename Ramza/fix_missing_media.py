#!/usr/bin/env python
"""
Script to fix missing media files by copying them from the static directory
"""

import os
import sys
import django
import shutil
from pathlib import Path

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
from restaurant.models import MenuItem

def fix_missing_media():
    """Fix missing media files by copying from static directory"""
    
    # Get project paths
    base_dir = Path(__file__).resolve().parent
    static_images_dir = base_dir / "static" / "images"
    media_menu_items_dir = base_dir / "media" / "menu_items"
    
    print(f"Static images directory: {static_images_dir}")
    print(f"Media menu items directory: {media_menu_items_dir}")
    print(f"Media menu items directory exists: {media_menu_items_dir.exists()}")
    
    # Create media directory if it doesn't exist
    if not media_menu_items_dir.exists():
        media_menu_items_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created media menu items directory: {media_menu_items_dir}")
    else:
        print(f"Media menu items directory already exists")
    
    # List files in media directory
    if media_menu_items_dir.exists():
        media_files = list(media_menu_items_dir.iterdir())
        print(f"Files in media directory: {len(media_files)}")
        for file in media_files:
            print(f"  - {file.name}")
    
    # Get all menu items
    menu_items = MenuItem.objects.all()
    print(f"\nFound {len(menu_items)} menu items")
    
    fixed_count = 0
    
    for item in menu_items:
        if item.image:
            # Get the filename from the image field
            filename = os.path.basename(item.image.name)
            print(f"\nChecking {item.name}: {filename}")
            
            # Check if file exists in media directory
            media_file_path = media_menu_items_dir / filename
            print(f"  Media file path: {media_file_path}")
            print(f"  Media file exists: {media_file_path.exists()}")
            
            if not media_file_path.exists():
                # Look for the file in static directory
                static_file_path = static_images_dir / filename
                print(f"  Static file path: {static_file_path}")
                print(f"  Static file exists: {static_file_path.exists()}")
                
                # Handle filename variations (spaces, special characters)
                if not static_file_path.exists():
                    print("  Looking for similar filenames...")
                    # Try to find similar filenames
                    for static_file in static_images_dir.iterdir():
                        if static_file.is_file():
                            # Try to match by removing spaces and special characters
                            static_name_clean = static_file.name.replace(' ', '_').replace('@', '_').replace('(', '_').replace(')', '_')
                            filename_clean = filename.replace(' ', '_').replace('@', '_').replace('(', '_').replace(')', '_')
                            
                            if static_name_clean == filename_clean:
                                static_file_path = static_file
                                print(f"  Found similar file: {static_file_path}")
                                break
                
                if static_file_path.exists():
                    # Copy file from static to media directory
                    try:
                        print(f"  Copying {static_file_path} to {media_file_path}")
                        shutil.copy2(static_file_path, media_file_path)
                        print(f"  ✅ Copied {filename} from static to media directory")
                        fixed_count += 1
                    except Exception as e:
                        print(f"  ❌ Error copying {filename}: {e}")
                else:
                    print(f"  ⚠️  File not found in static directory: {filename}")
            else:
                print(f"  ✅ File already exists in media directory: {filename}")
    
    # List files in media directory after processing
    print(f"\nAfter processing:")
    if media_menu_items_dir.exists():
        media_files = list(media_menu_items_dir.iterdir())
        print(f"Files in media directory: {len(media_files)}")
        for file in media_files:
            print(f"  - {file.name}")
    
    print(f"\nFixed {fixed_count} missing media files")
    return fixed_count

if __name__ == "__main__":
    fix_missing_media()