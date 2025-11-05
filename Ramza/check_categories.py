import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from restaurant.models import Category

def check_categories():
    print("=== Category Images Check ===")
    categories = Category.objects.all()
    
    if not categories:
        print("No categories found in database")
        return
    
    print(f"Found {categories.count()} categories:")
    for i, category in enumerate(categories):
        print(f"\n{i+1}. {category.name}")
        print(f"   Description: {category.description}")
        print(f"   Image field: {category.image}")
        if category.image:
            print(f"   Image URL: {category.image.url}")
            print(f"   Image path: {category.image.path}")
            print(f"   File exists: {os.path.exists(category.image.path)}")
        else:
            print("   No image uploaded")
    
    print("\n=== Media Directory Check ===")
    media_root = project_dir / 'media'
    categories_dir = media_root / 'categories'
    
    print(f"Media root: {media_root}")
    print(f"Media root exists: {media_root.exists()}")
    
    if media_root.exists():
        print(f"Categories directory: {categories_dir}")
        print(f"Categories directory exists: {categories_dir.exists()}")
        
        if categories_dir.exists():
            files = list(categories_dir.iterdir())
            print(f"Files in categories directory: {len(files)}")
            for file in files:
                print(f"  - {file.name}")

if __name__ == "__main__":
    check_categories()