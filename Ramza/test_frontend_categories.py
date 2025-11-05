import requests
import json

def test_frontend_categories_api():
    """
    Test the frontend categories API endpoint to verify it's receiving
    the updated data with the image field
    """
    print("=== Testing Frontend Categories API Request ===")
    
    try:
        # Make a request to the Django API endpoint for categories
        response = requests.get('http://localhost:8000/api/v1/categories/')
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response Data:")
            print(json.dumps(data, indent=2))
            
            # Check if the response contains the expected structure
            if 'categories' in data:
                categories = data['categories']
                print(f"\nFound {len(categories)} categories:")
                for i, category in enumerate(categories):
                    if isinstance(category, dict):
                        print(f"  {i+1}. Name: {category.get('name', 'N/A')}")
                        print(f"     Description: {category.get('description', 'N/A')}")
                        print(f"     Image: {category.get('image', 'N/A')}")
                    else:
                        print(f"  {i+1}. {category} (legacy format)")
            else:
                print("Warning: 'categories' key not found in response")
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Django is running on port 8000.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_frontend_categories_api()