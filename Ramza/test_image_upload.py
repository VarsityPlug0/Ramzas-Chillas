#!/usr/bin/env python
"""
Test script to verify image upload functionality
"""
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from restaurant.models import Category, MenuItem
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

def test_image_upload():
    """Test image upload functionality"""
    print("Testing image upload functionality...")
    
    # Create a simple test image
    test_image = SimpleUploadedFile(
        name='test_image.jpg',
        content=b'test image content',
        content_type='image/jpeg'
    )
    
    # Test category image upload
    print("Testing category image upload...")
    try:
        category = Category.objects.create(
            name='Test Category',
            description='Test category for image upload',
            image=test_image
        )
        print(f"Category image URL: {category.image.url}")
        print(f"Category image path: {category.image.path}")
        print("Category image upload successful!")
        
        # Test updating the image
        print("Testing category image update...")
        new_test_image = SimpleUploadedFile(
            name='new_test_image.jpg',
            content=b'new test image content',
            content_type='image/jpeg'
        )
        old_image_path = category.image.path
        category.image = new_test_image
        category.save()
        
        # Check if old image was deleted
        if os.path.exists(old_image_path):
            print("Warning: Old image file still exists")
        else:
            print("Old image file successfully deleted")
            
        print(f"New category image URL: {category.image.url}")
        print("Category image update successful!")
        
        # Clean up
        category.delete()
        print("Category cleanup successful!")
        
    except Exception as e:
        print(f"Error during category image test: {e}")
        return False
    
    print("All tests passed!")
    return True

if __name__ == '__main__':
    test_image_upload()