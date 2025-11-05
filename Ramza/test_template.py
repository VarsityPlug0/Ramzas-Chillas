import os
import django
from django.conf import settings
from django.template.loader import get_template

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

def test_template_loading():
    """Test if templates can be loaded without errors"""
    try:
        # Test loading base template
        base_template = get_template('base.html')
        print("Base template loaded successfully")
        
        # Test loading home template
        home_template = get_template('home.html')
        print("Home template loaded successfully")
        
        # Test loading cart template
        cart_template = get_template('cart.html')
        print("Cart template loaded successfully")
        
        # Test loading menu template
        menu_template = get_template('menu.html')
        print("Menu template loaded successfully")
        
        # Test loading checkout template
        checkout_template = get_template('checkout.html')
        print("Checkout template loaded successfully")
        
        print("All templates loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading templates: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_template_loading()