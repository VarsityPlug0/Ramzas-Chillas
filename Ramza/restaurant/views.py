from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views import View
import random
import os
from django.conf import settings
from .models import Category, MenuItem, SiteSettings, ContentSection, SiteImage

# Fallback food images
FOOD_IMAGES = [
    'images/Pork Rib Kota.jpeg',
    'images/download (1).jpeg',
    'images/download (2).jpeg', 
    'images/download (3).jpeg',
    'images/download.jpeg',
    'images/f7e6fd36-3419-4899-9bae-5bb98585a7aa.jpg',
    'images/image.jpg',
    'images/insta _ @gorgeous_thato_ (1).jpeg',
    'images/insta _ @gorgeous_thato_.jpeg'
]

def get_random_background():
    """Get a random background image from the background folder"""
    try:
        background_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'background')
        if os.path.exists(background_path):
            background_files = [f for f in os.listdir(background_path) 
                              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
            if background_files:
                return f'images/background/{random.choice(background_files)}'
    except Exception:
        pass
    
    # Fallback to a food image if no background images found
    return random.choice(FOOD_IMAGES)

def home(request):
    try:
        # Get data from database
        categories = Category.objects.filter(is_active=True)[:4]
        featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:3]
        
        # If no featured items, get some random available items
        if not featured_items:
            featured_items = MenuItem.objects.filter(is_available=True)[:3]
            
        # Convert to list and add fallback images
        categories_list = []
        for i, cat in enumerate(categories):
            categories_list.append({
                'name': cat.name,
                'description': cat.description,
                'image': cat.image.url if cat.image else None
            })
            
        # Ensure we have at least 4 categories for the template
        while len(categories_list) < 4:
            default_categories = [
                {'name': 'Burgers', 'description': 'Juicy burgers', 'image': None},
                {'name': 'Pizzas', 'description': 'Wood-fired pizzas', 'image': None},
                {'name': 'Drinks', 'description': 'Refreshing beverages', 'image': None},
                {'name': 'Sides', 'description': 'Perfect sides', 'image': None},
            ]
            if len(categories_list) < len(default_categories):
                categories_list.append(default_categories[len(categories_list)])
            else:
                break
                
        featured_list = []
        for item in featured_items:
            featured_list.append({
                'id': item.id,
                'name': item.name,
                'price': float(item.price),
                'description': item.description,
                'image': item.image.url if item.image else None
            })
            
        # Ensure we have at least 3 featured items
        while len(featured_list) < 3:
            default_featured = [
                {'id': 1, 'name': 'Chill Burger', 'price': 12.99, 'description': 'Laid-back beef patty with fresh chilled ingredients', 'image': None},
                {'id': 2, 'name': 'Chilla Margherita', 'price': 18.99, 'description': 'Classic pizza with our signature chill twist', 'image': None},
                {'id': 3, 'name': 'Ramza Fries', 'price': 4.99, 'description': 'Golden fries with our special chill seasoning', 'image': None},
            ]
            if len(featured_list) < len(default_featured):
                featured_list.append(default_featured[len(featured_list)])
            else:
                break
            
    except Exception as e:
        # Fallback data if database has issues
        categories_list = [
            {'name': 'Burgers', 'description': 'Juicy burgers', 'image': None},
            {'name': 'Pizzas', 'description': 'Wood-fired pizzas', 'image': None},
            {'name': 'Drinks', 'description': 'Refreshing beverages', 'image': None},
            {'name': 'Sides', 'description': 'Perfect sides', 'image': None},
        ]
        featured_list = [
            {'id': 1, 'name': 'Chill Burger', 'price': 12.99, 'description': 'Laid-back beef patty with fresh chilled ingredients', 'image': None},
            {'id': 2, 'name': 'Chilla Margherita', 'price': 18.99, 'description': 'Classic pizza with our signature chill twist', 'image': None},
            {'id': 3, 'name': 'Ramza Fries', 'price': 4.99, 'description': 'Golden fries with our special chill seasoning', 'image': None},
        ]
    
    context = {
        'featured_items': featured_list,
        'categories': categories_list,
    }
    return render(request, 'home.html', context)

def menu(request):
    try:
        # Get all available menu items from database
        menu_items = MenuItem.objects.filter(is_available=True).select_related('category')
        categories = ['All'] + list(Category.objects.filter(is_active=True).values_list('name', flat=True))
        
        # Convert queryset to list with proper image handling
        menu_items_list = []
        for item in menu_items:
            menu_items_list.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),  # Convert to float for JSON serialization
                'category': item.category.name,
                'image': item.image.url if item.image else None
            })
        
        # If no items exist, create fallback data
        if not menu_items_list:
            # Create categories first
            burger_cat, _ = Category.objects.get_or_create(name='Burgers', defaults={'sort_order': 1})
            pizza_cat, _ = Category.objects.get_or_create(name='Pizzas', defaults={'sort_order': 2})
            drinks_cat, _ = Category.objects.get_or_create(name='Drinks', defaults={'sort_order': 3})
            sides_cat, _ = Category.objects.get_or_create(name='Sides', defaults={'sort_order': 4})
            
            # Create sample menu items
            MenuItem.objects.get_or_create(
                name='Chill Burger',
                defaults={
                    'description': 'Laid-back beef patty with fresh chilled ingredients',
                    'price': 12.99,
                    'category': burger_cat,
                    'is_featured': True
                }
            )
            MenuItem.objects.get_or_create(
                name='Ramza Special',
                defaults={
                    'description': 'Signature chicken with avocado and cool ranch',
                    'price': 14.99,
                    'category': burger_cat
                }
            )
            MenuItem.objects.get_or_create(
                name='Chilla Margherita',
                defaults={
                    'description': 'Classic pizza with our signature chill twist',
                    'price': 18.99,
                    'category': pizza_cat,
                    'is_featured': True
                }
            )
            MenuItem.objects.get_or_create(
                name='Fire Pepperoni',
                defaults={
                    'description': 'Hot pepperoni with cool mozzarella balance',
                    'price': 22.99,
                    'category': pizza_cat
                }
            )
            MenuItem.objects.get_or_create(
                name='Chill Cola',
                defaults={
                    'description': 'Ice-cold refreshing cola to keep you cool',
                    'price': 2.99,
                    'category': drinks_cat
                }
            )
            MenuItem.objects.get_or_create(
                name='Ramza Fries',
                defaults={
                    'description': 'Golden fries with our special chill seasoning',
                    'price': 4.99,
                    'category': sides_cat,
                    'is_featured': True
                }
            )
            
            # Reload data
            menu_items = MenuItem.objects.filter(is_available=True).select_related('category')
            categories = ['All'] + list(Category.objects.filter(is_active=True).values_list('name', flat=True))
            
            # Convert queryset to list with proper image handling
            menu_items_list = []
            for item in menu_items:
                menu_items_list.append({
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': float(item.price),  # Convert to float for JSON serialization
                    'category': item.category.name,
                    'image': item.image.url if item.image else None
                })
        
    except Exception as e:
        # Fallback data
        menu_items_list = [
            {'id': 1, 'name': 'Chill Burger', 'description': 'Laid-back beef patty with fresh chilled ingredients', 'price': 12.99, 'category': 'Burgers', 'image': random.choice(FOOD_IMAGES)},
            {'id': 2, 'name': 'Ramza Special', 'description': 'Signature chicken with avocado and cool ranch', 'price': 14.99, 'category': 'Burgers', 'image': random.choice(FOOD_IMAGES)},
            {'id': 3, 'name': 'Chilla Margherita', 'description': 'Classic pizza with our signature chill twist', 'price': 18.99, 'category': 'Pizzas', 'image': random.choice(FOOD_IMAGES)},
            {'id': 4, 'name': 'Fire Pepperoni', 'description': 'Hot pepperoni with cool mozzarella balance', 'price': 22.99, 'category': 'Pizzas', 'image': random.choice(FOOD_IMAGES)},
            {'id': 5, 'name': 'Chill Cola', 'description': 'Ice-cold refreshing cola to keep you cool', 'price': 2.99, 'category': 'Drinks', 'image': random.choice(FOOD_IMAGES)},
            {'id': 6, 'name': 'Ramza Fries', 'description': 'Golden fries with our special chill seasoning', 'price': 4.99, 'category': 'Sides', 'image': random.choice(FOOD_IMAGES)},
        ]
        categories = ['All', 'Burgers', 'Pizzas', 'Drinks', 'Sides']
    
    context = {
        'menu_items': menu_items_list,
        'categories': categories,
    }
    return render(request, 'menu.html', context)

def cart(request):
    # The cart is managed client-side with localStorage
    # This view just renders the cart template
    return render(request, 'cart.html')

def checkout(request):
    # The checkout process
    # This view just renders the checkout template
    return render(request, 'checkout.html')

# API Endpoints for React Frontend
def api_menu_items(request):
    """API endpoint to get all menu items"""
    try:
        menu_items = MenuItem.objects.filter(is_available=True).select_related('category')
        menu_items_list = []
        for item in menu_items:
            # Safely handle image URL generation
            image_url = None
            try:
                if item.image:
                    image_url = item.image.url
            except Exception as e:
                print(f"Warning: Could not generate URL for menu item image {item.name}: {e}")
                image_url = None
                
            menu_items_list.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'category': item.category.name,
                'image': image_url
            })
        return JsonResponse({'menu_items': menu_items_list})
    except Exception as e:
        print(f"Error in api_menu_items: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def api_categories(request):
    """API endpoint to get all categories with image data"""
    try:
        categories = Category.objects.filter(is_active=True)
        categories_list = []
        for cat in categories:
            # Safely handle image URL generation
            image_url = None
            try:
                if cat.image:
                    image_url = cat.image.url
            except Exception as e:
                print(f"Warning: Could not generate URL for category image {cat.name}: {e}")
                image_url = None
                
            categories_list.append({
                'name': cat.name,
                'description': cat.description,
                'image': image_url
            })
        return JsonResponse({'categories': categories_list})
    except Exception as e:
        print(f"Error in api_categories: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def api_featured_items(request):
    """API endpoint to get featured items"""
    try:
        featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:3]
        featured_list = []
        for item in featured_items:
            # Safely handle image URL generation
            image_url = None
            try:
                if item.image:
                    image_url = item.image.url
            except Exception as e:
                print(f"Warning: Could not generate URL for featured item image {item.name}: {e}")
                image_url = None
                
            featured_list.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'image': image_url
            })
        return JsonResponse({'featured_items': featured_list})
    except Exception as e:
        print(f"Error in api_featured_items: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def api_site_settings(request):
    """API endpoint to get site settings"""
    try:
        site_settings = SiteSettings.objects.first()
        if site_settings:
            # Safely handle logo URL
            logo_url = None
            try:
                if site_settings.logo:
                    logo_url = site_settings.logo.url
            except Exception as e:
                print(f"Warning: Could not generate URL for site logo: {e}")
                logo_url = None
                
            # Safely handle favicon URL
            favicon_url = None
            try:
                if site_settings.favicon:
                    favicon_url = site_settings.favicon.url
            except Exception as e:
                print(f"Warning: Could not generate URL for site favicon: {e}")
                favicon_url = None
                
            settings_data = {
                'site_name': site_settings.site_name,
                'site_description': site_settings.site_description,
                'phone_number': site_settings.phone_number,
                'email': site_settings.email,
                'address': site_settings.address,
                'facebook_url': site_settings.facebook_url,
                'instagram_url': site_settings.instagram_url,
                'twitter_url': site_settings.twitter_url,
                'opening_time': site_settings.opening_time.strftime('%H:%M') if site_settings.opening_time else '09:00',
                'closing_time': site_settings.closing_time.strftime('%H:%M') if site_settings.closing_time else '22:00',
                'business_hours_text': site_settings.business_hours_text,
                'delivery_fee': float(site_settings.delivery_fee),
                'free_delivery_minimum': float(site_settings.free_delivery_minimum),
                'delivery_radius': site_settings.delivery_radius,
                'delivery_time_text': site_settings.delivery_time_text,
                'tax_rate': float(site_settings.tax_rate),
                'nav_home_text': site_settings.nav_home_text,
                'nav_menu_text': site_settings.nav_menu_text,
                'nav_about_text': site_settings.nav_about_text,
                'nav_contact_text': site_settings.nav_contact_text,
                'nav_cart_text': site_settings.nav_cart_text,
                'footer_copyright': site_settings.footer_copyright,
                'footer_description': site_settings.footer_description,
                'logo': logo_url,
                'favicon': favicon_url,
            }
            return JsonResponse({'site_settings': settings_data})
        else:
            # Return default settings if none exist
            default_settings = {
                'site_name': "Ramza's Chillas",
                'site_description': "Chill Vibes • Hot Food",
                'phone_number': "(555) 123-CHILL",
                'email': "hello@ramzaschillas.com",
                'address': "123 Chill Street, Island City",
                'facebook_url': "",
                'instagram_url': "",
                'twitter_url': "",
                'opening_time': '09:00',
                'closing_time': '22:00',
                'business_hours_text': "Mon-Thu: 11:00 AM - 10:00 PM\nFri-Sat: 11:00 AM - 11:00 PM\nSunday: 12:00 PM - 9:00 PM",
                'delivery_fee': 3.99,
                'free_delivery_minimum': 25.00,
                'delivery_radius': 5,
                'delivery_time_text': "25-30 minutes",
                'tax_rate': 0.0825,
                'nav_home_text': "Home",
                'nav_menu_text': "Menu",
                'nav_about_text': "About",
                'nav_contact_text': "Contact",
                'nav_cart_text': "Cart",
                'footer_copyright': "© 2024 Ramza's Chillas. All rights reserved.",
                'footer_description': "Serving the finest food with fresh ingredients and chill vibes since 2024. Your go-to spot for quality meals in a relaxed atmosphere.",
                'logo': None,
                'favicon': None,
            }
            return JsonResponse({'site_settings': default_settings})
    except Exception as e:
        print(f"Error in api_site_settings: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def api_content_sections(request):
    """API endpoint to get all content sections"""
    try:
        content_sections = ContentSection.objects.filter(is_active=True)
        sections_data = {}
        for section in content_sections:
            # Safely handle image URLs
            image_url = None
            try:
                if section.image:
                    image_url = section.image.url
            except Exception as e:
                print(f"Warning: Could not generate URL for content section image {section.section}: {e}")
                image_url = None
                
            background_image_url = None
            try:
                if section.background_image:
                    background_image_url = section.background_image.url
            except Exception as e:
                print(f"Warning: Could not generate URL for content section background image {section.section}: {e}")
                background_image_url = None
                
            sections_data[section.section] = {
                'title': section.title,
                'subtitle': section.subtitle,
                'description': section.description,
                'button_text': section.button_text,
                'button_url': section.button_url,
                'extra_text_1': section.extra_text_1,
                'extra_text_2': section.extra_text_2,
                'extra_text_3': section.extra_text_3,
                'image': image_url,
                'background_image': background_image_url,
                'meta_title': section.meta_title,
                'meta_description': section.meta_description,
            }
        return JsonResponse({'content_sections': sections_data})
    except Exception as e:
        print(f"Error in api_content_sections: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def api_site_images(request):
    """API endpoint to get all site images"""
    try:
        site_images = SiteImage.objects.filter(is_active=True)
        images_data = {}
        for image in site_images:
            # Safely handle image URL
            image_url = None
            try:
                if image.image:
                    image_url = image.image.url
            except Exception as e:
                print(f"Warning: Could not generate URL for site image {image.name}: {e}")
                image_url = None
                
            images_data[image.name] = {
                'url': image_url,
                'alt_text': image.alt_text,
                'description': image.description,
                'image_type': image.image_type,
            }
        return JsonResponse({'site_images': images_data})
    except Exception as e:
        print(f"Error in api_site_images: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def api_testimonials(request):
    """API endpoint to get all active testimonials"""
    try:
        testimonials = Testimonial.objects.filter(is_active=True)
        testimonials_data = []
        for testimonial in testimonials:
            # Safely handle image URL
            image_url = None
            try:
                if testimonial.image:
                    image_url = testimonial.image.url
            except Exception as e:
                print(f"Warning: Could not generate URL for testimonial image {testimonial.customer_name}: {e}")
                image_url = None
                
            testimonials_data.append({
                'id': testimonial.id,
                'customer_name': testimonial.customer_name,
                'customer_title': testimonial.customer_title,
                'review': testimonial.review,
                'rating': testimonial.rating,
                'image': image_url,
            })
        return JsonResponse({'testimonials': testimonials_data})
    except Exception as e:
        print(f"Error in api_testimonials: {e}")
        return JsonResponse({'error': str(e)}, status=500)
