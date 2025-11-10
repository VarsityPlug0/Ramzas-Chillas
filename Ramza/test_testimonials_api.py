#!/usr/bin/env python
"""
Script to test the testimonials API endpoint
"""

import os
import sys
import django
import json

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

# Import views and request
from restaurant.views import api_testimonials
from django.http import HttpRequest

def test_testimonials_api():
    """Test the testimonials API endpoint"""
    
    print("Testing testimonials API endpoint...")
    
    # Create a mock request
    request = HttpRequest()
    request.META['REQUEST_METHOD'] = 'GET'
    
    try:
        # Get the API response
        response = api_testimonials(request)
        
        # Print the response data
        print("API Response Status Code:", response.status_code)
        print("API Response Content:")
        print(response.content.decode('utf-8'))
        
        # Try to parse JSON to check if it's valid
        try:
            data = json.loads(response.content.decode('utf-8'))
            print("\n✅ JSON is valid")
            print(f"Testimonials count: {len(data.get('testimonials', []))}")
            
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON is invalid: {e}")
            
    except Exception as e:
        print(f"❌ Error calling API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_testimonials_api()