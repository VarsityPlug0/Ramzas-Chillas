import os
from pathlib import Path

# Get the project base directory
BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / 'media'

print(f"Base directory: {BASE_DIR}")
print(f"Media root: {MEDIA_ROOT}")
print(f"Media root exists: {MEDIA_ROOT.exists()}")

if MEDIA_ROOT.exists():
    print("Contents of media directory:")
    for item in MEDIA_ROOT.iterdir():
        print(f"  {item.name} ({'dir' if item.is_dir() else 'file'})")
        if item.is_dir():
            try:
                sub_items = list(item.iterdir())
                print(f"    Contains {len(sub_items)} items")
                for sub_item in sub_items[:5]:  # Show first 5 items
                    print(f"      {sub_item.name}")
                if len(sub_items) > 5:
                    print(f"      ... and {len(sub_items) - 5} more")
            except PermissionError:
                print("      Permission denied")
else:
    print("Creating media directory...")
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    print("Created media directory")

# Ensure categories directory exists
CATEGORIES_DIR = MEDIA_ROOT / 'categories'
if not CATEGORIES_DIR.exists():
    print("Creating categories directory...")
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    print("Created categories directory")
else:
    print("Categories directory exists")