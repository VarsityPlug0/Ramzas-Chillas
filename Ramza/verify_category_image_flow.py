import os
import sys
import django
import requests
import json
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from restaurant.models import Category
from django.conf import settings

def verify_category_image_flow():
    """
    Verify the complete category image flow:
    1. Check if image files exist in the media directory
    2. Check if Category model entries have correct image paths
    3. Test the API endpoint response
    4. Verify frontend can fetch the data correctly
    """
    print("=== Verifying Category Image Flow ===\n")
    
    # 1. Check media directory
    print("1. Checking media directory structure:")
    media_root = settings.MEDIA_ROOT
    categories_dir = os.path.join(media_root, 'categories')
    
    print(f"   Media root: {media_root}")
    print(f"   Categories directory: {categories_dir}")
    print(f"   Categories directory exists: {os.path.exists(categories_dir)}")
    
    if os.path.exists(categories_dir):
        files = os.listdir(categories_dir)
        print(f"   Files in categories directory: {files}")
        for file in files:
            file_path = os.path.join(categories_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"     - {file} ({file_size} bytes)")
    else:
        print("   ERROR: Categories directory does not exist!")
    
    print()
    
    # 2. Check Category model entries
    print("2. Checking Category model entries:")
    categories = Category.objects.all()
    print(f"   Total categories in database: {categories.count()}")
    
    for category in categories:
        print(f"   - {category.name}:")
        print(f"     Description: {category.description}")
        print(f"     Image field: {category.image}")
        if category.image:
            print(f"     Image URL: {category.image.url}")
            print(f"     Image path: {category.image.path}")
            print(f"     File exists: {os.path.exists(category.image.path)}")
        else:
            print("     No image uploaded")
    
    print()
    
    # 3. Test API endpoint
    print("3. Testing API endpoint response:")
    try:
        # Test Django API directly
        from restaurant.views import api_categories
        from django.http import HttpRequest
        
        request = HttpRequest()
        response = api_categories(request)
        
        print(f"   Django API Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            print("   Django API Response:")
            print(json.dumps(data, indent=4))
        
        print()
        
        # 4. Test frontend API request
        print("4. Testing frontend API request:")
        try:
            frontend_response = requests.get('http://localhost:8000/api/v1/categories/')
            print(f"   Frontend Request Status: {frontend_response.status_code}")
            
            if frontend_response.status_code == 200:
                frontend_data = frontend_response.json()
                print("   Frontend Response:")
                print(json.dumps(frontend_data, indent=4))
                
                # Verify structure
                if 'categories' in frontend_data:
                    print("\n   Structure verification:")
                    for i, category in enumerate(frontend_data['categories']):
                        if isinstance(category, dict):
                            has_name = 'name' in category
                            has_image = 'image' in category
                            print(f"   Category {i+1} ({category.get('name', 'Unknown')}): name={has_name}, image={has_image}")
                            if has_image and category['image']:
                                print(f"     Image URL: {category['image']}")
                        else:
                            print(f"   Category {i+1}: Legacy format detected")
                else:
                    print("   WARNING: 'categories' key not found in response")
            else:
                print(f"   ERROR: Frontend request failed with status {frontend_response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("   ERROR: Could not connect to frontend API. Make sure Django server is running.")
        except Exception as e:
            print(f"   ERROR: {e}")
            
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    verify_category_image_flow()