import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

# Now we can import and use Django models
from restaurant.models import Testimonial

try:
    # Try to query testimonials
    testimonials = Testimonial.objects.filter(is_active=True)
    print(f"Found {testimonials.count()} testimonials")
    for testimonial in testimonials:
        print(f"- {testimonial.customer_name}: {testimonial.review[:50]}...")
except Exception as e:
    print(f"Error querying testimonials: {e}")
    import traceback
    traceback.print_exc()