"""
URL configuration for fastfood_restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from restaurant import views
from frontend.views import serve_react_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('custom_admin.urls')),
    path('api/menu/', views.menu, name='api_menu'),
    path('api/cart/', views.cart, name='api_cart'),
    path('api/checkout/', views.checkout, name='api_checkout'),
    # New API endpoints for React frontend
    path('api/v1/menu-items/', views.api_menu_items, name='api_menu_items'),
    path('api/v1/categories/', views.api_categories, name='api_categories'),
    path('api/v1/featured-items/', views.api_featured_items, name='api_featured_items'),
    path('api/v1/site-settings/', views.api_site_settings, name='api_site_settings'),
    path('api/v1/content-sections/', views.api_content_sections, name='api_content_sections'),
    path('api/v1/site-images/', views.api_site_images, name='api_site_images'),
    path('api/v1/testimonials/', views.api_testimonials, name='api_testimonials'),
    # Orders API
    path('api/v1/orders/', include('orders.urls')),
    # Order tracking page
    path('track-order/', TemplateView.as_view(template_name='order_tracking.html'), name='track_order'),
    # Serve the React frontend for all other routes
    re_path(r'^(?!api|admin|dashboard|track-order|media|static).*$', serve_react_app, name='frontend'),
]

# Serve media files in development and on Render (for simplicity)
# In production, you should use a CDN or cloud storage
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development (production uses WhiteNoise)
# NOTE: In production, WhiteNoise serves static files automatically
# We only need this for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Static files are served automatically by WhiteNoise middleware

# Additional media file serving for production environments
# This ensures media files are served even when DEBUG=False
if not settings.DEBUG:
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]