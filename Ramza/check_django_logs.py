import os
import sys
import django
from pathlib import Path
import logging

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from restaurant.views import api_categories
from django.http import HttpRequest
import json

def check_django_logs():
    """
    Check Django logs for any errors related to category image handling
    """
    print("=== Checking Django Logs for Category Image Issues ===")
    
    # Test the API endpoint directly to see if there are any errors
    print("\n1. Testing API endpoint directly:")
    try:
        request = HttpRequest()
        response = api_categories(request)
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            print("   Response Structure:")
            for i, category in enumerate(data.get('categories', [])):
                if isinstance(category, dict):
                    print(f"     Category {i+1}: {category.get('name', 'Unknown')}")
                    print(f"       Has image: {'image' in category and category['image'] is not None}")
                    if category.get('image'):
                        print(f"       Image URL: {category['image']}")
                else:
                    print(f"     Category {i+1}: {category} (legacy format)")
            
            print("   ✅ API endpoint working correctly")
        else:
            print(f"   ❌ API endpoint failed with status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error testing API endpoint: {e}")
    
    # Check if media files exist
    print("\n2. Checking media files:")
    try:
        from django.conf import settings
        media_root = settings.MEDIA_ROOT
        categories_dir = os.path.join(media_root, 'categories')
        
        print(f"   Media root: {media_root}")
        print(f"   Categories directory exists: {os.path.exists(categories_dir)}")
        
        if os.path.exists(categories_dir):
            files = os.listdir(categories_dir)
            print(f"   Files in categories directory: {files}")
            for file in files:
                file_path = os.path.join(categories_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"     - {file} ({file_size} bytes)")
        else:
            print("   ⚠️  Categories directory does not exist")
            
    except Exception as e:
        print(f"   ❌ Error checking media files: {e}")
    
    # Check database entries
    print("\n3. Checking database entries:")
    try:
        from restaurant.models import Category
        categories = Category.objects.all()
        print(f"   Total categories in database: {categories.count()}")
        
        for category in categories:
            print(f"   - {category.name}:")
            print(f"     Description: {category.description[:50]}{'...' if len(category.description) > 50 else ''}")
            print(f"     Has image: {category.image is not None and bool(category.image)}")
            if category.image:
                print(f"     Image URL: {category.image.url}")
                print(f"     Image path: {category.image.path}")
                print(f"     File exists: {os.path.exists(category.image.path)}")
            else:
                print("     No image uploaded")
                
    except Exception as e:
        print(f"   ❌ Error checking database entries: {e}")
    
    print("\n=== Django Log Check Complete ===")

if __name__ == "__main__":
    check_django_logs()