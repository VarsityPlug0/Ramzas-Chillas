#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

def test_templates():
    """Test that templates load without errors"""
    templates_to_test = [
        'base.html',
        'home.html',
        'menu.html',
        'cart.html',
        'checkout.html'
    ]
    
    print("Testing template loading...")
    
    for template_name in templates_to_test:
        try:
            template = get_template(template_name)
            print(f"✓ {template_name} loaded successfully")
        except Exception as e:
            print(f"✗ {template_name} failed to load: {e}")
            return False
    
    print("All templates loaded successfully!")
    return True

if __name__ == '__main__':
    test_templates()