#!/usr/bin/env python
"""
Test script to verify WhiteNoise configuration
"""
import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')
django.setup()

def test_whitenoise_config():
    print("=== WhiteNoise Configuration Test ===")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'Not set')}")
    print(f"WHITENOISE_USE_FINDERS: {getattr(settings, 'WHITENOISE_USE_FINDERS', 'Not set')}")
    print(f"WHITENOISE_AUTOREFRESH: {getattr(settings, 'WHITENOISE_AUTOREFRESH', 'Not set')}")
    print(f"WHITENOISE_MANIFEST_STRICT: {getattr(settings, 'WHITENOISE_MANIFEST_STRICT', 'Not set')}")
    print(f"WHITENOISE_STATIC_PREFIX: {getattr(settings, 'WHITENOISE_STATIC_PREFIX', 'Not set')}")
    
    # Check middleware
    middleware = getattr(settings, 'MIDDLEWARE', [])
    whitenoise_middleware = 'whitenoise.middleware.WhiteNoiseMiddleware'
    if whitenoise_middleware in middleware:
        print(f"WhiteNoise middleware found at position: {middleware.index(whitenoise_middleware)}")
    else:
        print("WhiteNoise middleware NOT found!")
        
    # Check if WhiteNoise is installed
    try:
        import whitenoise
        print(f"WhiteNoise version: {whitenoise.__version__}")
    except ImportError:
        print("WhiteNoise NOT installed!")

if __name__ == "__main__":
    test_whitenoise_config()