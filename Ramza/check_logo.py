import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

from restaurant.models import SiteSettings

def check_logo():
    try:
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.logo:
            print(f"Logo found: {site_settings.logo.url}")
            print(f"Logo path: {site_settings.logo.path}")
        else:
            print("No logo found in database")
    except Exception as e:
        print(f"Error checking logo: {e}")

if __name__ == "__main__":
    check_logo()