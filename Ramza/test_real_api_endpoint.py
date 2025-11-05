import requests
import json

def test_real_api_endpoint():
    """
    Test the actual API endpoint to verify it's working correctly
    """
    print("=== Testing Real API Endpoint ===")
    
    try:
        # Make a real HTTP request to the categories API endpoint
        response = requests.get('http://localhost:8000/api/v1/categories/', timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response Data:")
            print(json.dumps(data, indent=2))
            
            # Verify the structure
            if 'categories' in data:
                categories = data['categories']
                print(f"\nFound {len(categories)} categories:")
                
                image_count = 0
                no_image_count = 0
                
                for i, category in enumerate(categories):
                    if isinstance(category, dict):
                        has_image = category.get('image') is not None
                        if has_image:
                            image_count += 1
                            print(f"  {i+1}. {category.get('name', 'N/A')} - HAS IMAGE: {category.get('image')}")
                        else:
                            no_image_count += 1
                            print(f"  {i+1}. {category.get('name', 'N/A')} - NO IMAGE")
                    else:
                        no_image_count += 1
                        print(f"  {i+1}. {category} (legacy format)")
                
                print(f"\nSummary:")
                print(f"  Categories with images: {image_count}")
                print(f"  Categories without images: {no_image_count}")
                
                # Verify that at least one category has an image
                if image_count > 0:
                    print("\n✅ SUCCESS: Category images are being served correctly!")
                else:
                    print("\n⚠️  WARNING: No categories have images. Check if images were uploaded.")
                    
            else:
                print("❌ ERROR: 'categories' key not found in response")
        else:
            print(f"❌ ERROR: Received status code {response.status_code}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the server. Make sure Django is running on port 8000.")
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out. Server might be unresponsive.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_real_api_endpoint()