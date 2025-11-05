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

from restaurant.views import api_categories
from django.http import HttpRequest

def test_categories_api():
    print("=== Testing Categories API ===")
    # Create a mock request
    request = HttpRequest()
    
    # Call the API function
    response = api_categories(request)
    
    # Print the response
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))

if __name__ == "__main__":
    test_categories_api()