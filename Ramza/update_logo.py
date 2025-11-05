import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

# Import after Django setup
from restaurant.models import SiteSettings
from django.core.files import File

def update_logo():
    try:
        # Get the first (and only) SiteSettings instance
        site_settings = SiteSettings.objects.first()  # type: ignore
        if site_settings:
            # Update the logo field
            logo_path = os.path.join(settings.MEDIA_ROOT, 'site', 'logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    site_settings.logo.save('logo.png', File(f), save=True)
                print("Logo updated successfully")
            else:
                print(f"Logo file not found at {logo_path}")
        else:
            print("No site settings found")
    except Exception as e:
        print(f"Error updating logo: {e}")

if __name__ == "__main__":
    update_logo()