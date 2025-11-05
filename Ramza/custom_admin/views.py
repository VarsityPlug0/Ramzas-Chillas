from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from restaurant.models import MenuItem, Category, SiteSettings, ContentSection, SiteImage, Testimonial
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
from pathlib import Path

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_required(view_func):
    """Decorator to require admin authentication for all admin views"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('custom_admin:login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Admin Login View
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions')
    
    return render(request, 'custom_admin/login.html')

# Admin Logout
def admin_logout(request):
    logout(request)
    return redirect('custom_admin:login')

# Dashboard
@admin_required
def dashboard(request):
    # Get statistics
    total_items = MenuItem.objects.count()
    total_categories = Category.objects.filter(is_active=True).count()
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True).count()
    low_stock_items = MenuItem.objects.filter(stock_quantity__lte=5, is_available=True).count()
    
    # New content statistics
    total_content_sections = ContentSection.objects.count()
    total_site_images = SiteImage.objects.count()
    total_testimonials = Testimonial.objects.count()
    inactive_content_sections = ContentSection.objects.filter(is_active=False).count()
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Get website images for image gallery
    website_images = get_website_images()
    
    # Get background images
    background_images = get_background_images()
    
    context = {
        'total_items': total_items,
        'total_categories': total_categories,
        'featured_items': featured_items,
        'low_stock_items': low_stock_items,
        'total_content_sections': total_content_sections,
        'total_site_images': total_site_images,
        'total_testimonials': total_testimonials,
        'inactive_content_sections': inactive_content_sections,
        'recent_orders': recent_orders,
        'website_images': website_images,
        'background_images': background_images,
    }
    return render(request, 'custom_admin/dashboard.html', context)

def get_website_images():
    """Get all images currently used on the website"""
    images = {
        'menu_items': [],
        'categories': [],
        'site_settings': [],
        'static_images': [],
    }
    
    try:
        # Menu item images
        menu_items_with_images = MenuItem.objects.filter(image__isnull=False).exclude(image='')
        for item in menu_items_with_images:
            if item.image:
                images['menu_items'].append({
                    'name': item.name,
                    'image_url': item.image.url,
                    'type': 'Menu Item',
                    'status': 'Active' if item.is_available else 'Inactive',
                    'featured': item.is_featured,
                    'category': item.category.name if item.category else 'No Category'
                })
        
        # Category images
        categories_with_images = Category.objects.filter(image__isnull=False).exclude(image='')
        for category in categories_with_images:
            if category.image:
                images['categories'].append({
                    'name': category.name,
                    'image_url': category.image.url,
                    'type': 'Category',
                    'status': 'Active' if category.is_active else 'Inactive',
                    'sort_order': category.sort_order
                })
        
        # Site settings images
        try:
            site_settings = SiteSettings.objects.first()
            if site_settings:
                if site_settings.logo:
                    images['site_settings'].append({
                        'name': 'Restaurant Logo',
                        'image_url': site_settings.logo.url,
                        'type': 'Site Logo',
                        'status': 'Active'
                    })
                if site_settings.hero_image:
                    images['site_settings'].append({
                        'name': 'Hero Image',
                        'image_url': site_settings.hero_image.url,
                        'type': 'Hero Image',
                        'status': 'Active'
                    })
        except:
            pass
        
        # Static images from food folder
        static_folder = os.path.join(settings.BASE_DIR, 'static', 'images')
        if os.path.exists(static_folder):
            for filename in os.listdir(static_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    images['static_images'].append({
                        'name': filename,
                        'image_url': f'/static/images/{filename}',
                        'type': 'Static Image',
                        'status': 'Available'
                    })
    
    except Exception as e:
        # If there's any error, return empty structure
        pass
    
    return images

def get_background_images():
    """Get all background images available for the website"""
    background_images = {
        'images': [],
        'total_count': 0,
        'folder_path': '/static/images/background/',
        'status': 'active'
    }
    
    try:
        background_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'background')
        
        if os.path.exists(background_path):
            background_files = []
            
            for filename in os.listdir(background_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    file_path = os.path.join(background_path, filename)
                    file_size = os.path.getsize(file_path)
                    
                    background_files.append({
                        'name': filename,
                        'display_name': filename.replace('-', ' ').replace('_', ' ').title(),
                        'image_url': f'/static/images/background/{filename}',
                        'file_size': round(file_size / 1024, 1),  # Size in KB
                        'type': 'Background Image',
                        'status': 'Active',
                        'extension': filename.split('.')[-1].upper(),
                        'added_date': 'Unknown'  # Could be enhanced with file modification time
                    })
            
            background_images['images'] = sorted(background_files, key=lambda x: x['name'])
            background_images['total_count'] = len(background_files)
            
            if len(background_files) == 0:
                background_images['status'] = 'empty'
        else:
            background_images['status'] = 'folder_missing'
    
    except Exception as e:
        background_images['status'] = 'error'
        background_images['error_message'] = str(e)
    
    return background_images

# Menu Items Management
@admin_required
def menu_items(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    items = MenuItem.objects.all()
    
    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    if category_filter:
        items = items.filter(category_id=category_filter)
    
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'custom_admin/menu_items.html', context)

# Add/Edit Menu Item
@user_passes_test(is_admin)
def edit_menu_item(request, item_id=None):
    item = get_object_or_404(MenuItem, id=item_id) if item_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity', 0)
        is_available = request.POST.get('is_available') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        
        if item:
            item.name = name
            item.description = description
            item.price = price
            item.category_id = category_id
            item.stock_quantity = stock_quantity
            item.is_available = is_available
            item.is_featured = is_featured
            # Only update image if a new one was uploaded via AJAX
            if request.FILES.get('image'):
                item.image = request.FILES['image']
            item.save()
            messages.success(request, 'Menu item updated successfully!')
        else:
            item = MenuItem.objects.create(
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                stock_quantity=stock_quantity,
                is_available=is_available,
                is_featured=is_featured,
                image=request.FILES.get('image')
            )
            messages.success(request, 'Menu item created successfully!')
        
        return redirect('custom_admin:menu_items')
    
    categories = Category.objects.filter(is_active=True)
    context = {
        'item': item,
        'categories': categories,
    }
    return render(request, 'custom_admin/edit_menu_item.html', context)

# Delete Menu Item
@user_passes_test(is_admin)
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('custom_admin:menu_items')

# Categories Management
@user_passes_test(is_admin)
def categories(request):
    categories = Category.objects.all().order_by('sort_order', 'name')
    context = {'categories': categories}
    return render(request, 'custom_admin/categories.html', context)

# Add/Edit Category
@user_passes_test(is_admin)
def edit_category(request, category_id=None):
    category = get_object_or_404(Category, id=category_id) if category_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        sort_order = request.POST.get('sort_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # Ensure media directories exist
        media_root = settings.MEDIA_ROOT
        categories_dir = os.path.join(media_root, 'categories')
        if not os.path.exists(categories_dir):
            os.makedirs(categories_dir, exist_ok=True)
        
        if category:
            category.name = name
            category.description = description
            category.sort_order = sort_order
            category.is_active = is_active
            # Only update image if a new one was uploaded via AJAX
            if request.FILES.get('image'):
                # Delete old image if it exists
                if category.image:
                    old_image_path = category.image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                category.image = request.FILES['image']
            category.save()
            messages.success(request, 'Category updated successfully!')
        else:
            category = Category.objects.create(
                name=name,
                description=description,
                sort_order=sort_order,
                is_active=is_active,
                image=request.FILES.get('image')
            )
            messages.success(request, 'Category created successfully!')
        
        return redirect('custom_admin:categories')
    
    context = {'category': category}
    return render(request, 'custom_admin/edit_category.html', context)

# Orders Management
@user_passes_test(is_admin)
def orders(request):
    status_filter = request.GET.get('status', '')
    
    orders = Order.objects.all().order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'custom_admin/orders.html', context)

# Update Order Status
@csrf_exempt
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'success': False})

# Site Settings
@user_passes_test(is_admin)
def site_settings(request):
    settings, created = SiteSettings.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        settings.site_name = request.POST.get('site_name', '')
        settings.site_description = request.POST.get('site_description', '')
        settings.phone_number = request.POST.get('phone_number', '')
        settings.email = request.POST.get('email', '')
        settings.address = request.POST.get('address', '')
        settings.delivery_fee = request.POST.get('delivery_fee', 0)
        
        if request.FILES.get('logo'):
            settings.logo = request.FILES['logo']
        if request.FILES.get('hero_image'):
            settings.hero_image = request.FILES['hero_image']
        
        settings.save()
        messages.success(request, 'Site settings updated successfully!')
        return redirect('custom_admin:site_settings')
    
    context = {'settings': settings}
    return render(request, 'custom_admin/site_settings.html', context)

# Content Sections Management
@user_passes_test(is_admin)
def content_sections(request):
    search_query = request.GET.get('search', '')
    
    sections = ContentSection.objects.all()
    
    if search_query:
        sections = sections.filter(Q(title__icontains=search_query) | Q(section__icontains=search_query))
    
    paginator = Paginator(sections, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'custom_admin/content_sections.html', context)

# Add/Edit Content Section
@user_passes_test(is_admin)
def edit_content_section(request, section_id=None):
    section = get_object_or_404(ContentSection, id=section_id) if section_id else None
    
    if request.method == 'POST':
        section_type = request.POST.get('section')
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        description = request.POST.get('description')
        button_text = request.POST.get('button_text')
        button_url = request.POST.get('button_url')
        extra_text_1 = request.POST.get('extra_text_1')
        extra_text_2 = request.POST.get('extra_text_2')
        extra_text_3 = request.POST.get('extra_text_3')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        is_active = request.POST.get('is_active') == 'on'
        
        if section:
            # Check if section type is being changed and if it already exists
            if section.section != section_type and ContentSection.objects.filter(section=section_type).exists():
                messages.error(request, f'A content section of type "{section_type}" already exists!')
                context = {
                    'section': section,
                }
                return render(request, 'custom_admin/edit_content_section.html', context)
            
            section.section = section_type
            section.title = title
            section.subtitle = subtitle
            section.description = description
            section.button_text = button_text
            section.button_url = button_url
            section.extra_text_1 = extra_text_1
            section.extra_text_2 = extra_text_2
            section.extra_text_3 = extra_text_3
            section.meta_title = meta_title
            section.meta_description = meta_description
            section.is_active = is_active
            
            if request.FILES.get('image'):
                section.image = request.FILES['image']
            if request.FILES.get('background_image'):
                section.background_image = request.FILES['background_image']
                
            section.save()
            messages.success(request, 'Content section updated successfully!')
        else:
            # Check if section type already exists
            if ContentSection.objects.filter(section=section_type).exists():
                messages.error(request, f'A content section of type "{section_type}" already exists!')
                context = {
                    'section': None,
                }
                return render(request, 'custom_admin/edit_content_section.html', context)
                
            section = ContentSection.objects.create(
                section=section_type,
                title=title,
                subtitle=subtitle,
                description=description,
                button_text=button_text,
                button_url=button_url,
                extra_text_1=extra_text_1,
                extra_text_2=extra_text_2,
                extra_text_3=extra_text_3,
                meta_title=meta_title,
                meta_description=meta_description,
                is_active=is_active,
                image=request.FILES.get('image'),
                background_image=request.FILES.get('background_image')
            )
            messages.success(request, 'Content section created successfully!')
        
        return redirect('custom_admin:content_sections')
    
    context = {
        'section': section,
    }
    return render(request, 'custom_admin/edit_content_section.html', context)

# Delete Content Section
@user_passes_test(is_admin)
def delete_content_section(request, section_id):
    section = get_object_or_404(ContentSection, id=section_id)
    section.delete()
    messages.success(request, 'Content section deleted successfully!')
    return redirect('custom_admin:content_sections')

# Site Images Management
@user_passes_test(is_admin)
def site_images(request):
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    
    images = SiteImage.objects.all()
    
    if search_query:
        images = images.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    if type_filter:
        images = images.filter(image_type=type_filter)
    
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get image type choices for filter
    image_types = SiteImage.IMAGE_TYPES
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'type_filter': type_filter,
        'image_types': image_types,
    }
    return render(request, 'custom_admin/site_images.html', context)

# Add/Edit Site Image
@user_passes_test(is_admin)
def edit_site_image(request, image_id=None):
    image = get_object_or_404(SiteImage, id=image_id) if image_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        image_type = request.POST.get('image_type')
        alt_text = request.POST.get('alt_text')
        description = request.POST.get('description')
        sort_order = request.POST.get('sort_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        if image:
            image.name = name
            image.image_type = image_type
            image.alt_text = alt_text
            image.description = description
            image.sort_order = sort_order
            image.is_active = is_active
            
            if request.FILES.get('image'):
                image.image = request.FILES['image']
                
            image.save()
            messages.success(request, 'Site image updated successfully!')
        else:
            if not request.FILES.get('image'):
                messages.error(request, 'Please select an image to upload!')
                context = {
                    'image': None,
                }
                return render(request, 'custom_admin/edit_site_image.html', context)
                
            image = SiteImage.objects.create(
                name=name,
                image_type=image_type,
                alt_text=alt_text,
                description=description,
                sort_order=sort_order,
                is_active=is_active,
                image=request.FILES['image']
            )
            messages.success(request, 'Site image created successfully!')
        
        return redirect('custom_admin:site_images')
    
    context = {
        'image': image,
    }
    return render(request, 'custom_admin/edit_site_image.html', context)

# Delete Site Image
@user_passes_test(is_admin)
def delete_site_image(request, image_id):
    image = get_object_or_404(SiteImage, id=image_id)
    image.delete()
    messages.success(request, 'Site image deleted successfully!')
    return redirect('custom_admin:site_images')

# Testimonials Management
@user_passes_test(is_admin)
def testimonials(request):
    search_query = request.GET.get('search', '')
    
    testimonials = Testimonial.objects.all()
    
    if search_query:
        testimonials = testimonials.filter(Q(customer_name__icontains=search_query) | Q(review__icontains=search_query))
    
    paginator = Paginator(testimonials, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'custom_admin/testimonials.html', context)

# Add/Edit Testimonial
@user_passes_test(is_admin)
def edit_testimonial(request, testimonial_id=None):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id) if testimonial_id else None
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_title = request.POST.get('customer_title')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        sort_order = request.POST.get('sort_order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        if testimonial:
            testimonial.customer_name = customer_name
            testimonial.customer_title = customer_title
            testimonial.review = review
            testimonial.rating = rating
            testimonial.sort_order = sort_order
            testimonial.is_active = is_active
            
            if request.FILES.get('image'):
                testimonial.image = request.FILES['image']
                
            testimonial.save()
            messages.success(request, 'Testimonial updated successfully!')
        else:
            testimonial = Testimonial.objects.create(
                customer_name=customer_name,
                customer_title=customer_title,
                review=review,
                rating=rating,
                sort_order=sort_order,
                is_active=is_active,
                image=request.FILES.get('image')
            )
            messages.success(request, 'Testimonial created successfully!')
        
        return redirect('custom_admin:testimonials')
    
    context = {
        'testimonial': testimonial,
    }
    return render(request, 'custom_admin/edit_testimonial.html', context)

# Delete Testimonial
@user_passes_test(is_admin)
def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully!')
    return redirect('custom_admin:testimonials')

# AJAX Image Upload for Menu Items
@csrf_exempt
@user_passes_test(is_admin)
def upload_menu_item_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            
            # Generate a unique filename
            import uuid
            from django.utils.text import slugify
            filename = f"{uuid.uuid4().hex}_{slugify(image.name)}"
            
            # Save the image directly to the menu_items directory
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            
            path = os.path.join('menu_items', filename)
            file_path = default_storage.save(path, ContentFile(image.read()))
            image_url = default_storage.url(file_path)
            
            return JsonResponse({
                'success': True,
                'image_url': image_url
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'No image provided'
    })

# AJAX Image Upload for Categories
@csrf_exempt
@user_passes_test(is_admin)
def upload_category_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            
            # Generate a unique filename
            import uuid
            from django.utils.text import slugify
            filename = f"{uuid.uuid4().hex}_{slugify(image.name)}"
            
            # Save the image directly to the categories directory
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            
            path = os.path.join('categories', filename)
            file_path = default_storage.save(path, ContentFile(image.read()))
            image_url = default_storage.url(file_path)
            
            return JsonResponse({
                'success': True,
                'image_url': image_url
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'No image provided'
    })

# Global Images View
@admin_required
def all_images(request):
    """Display all images used throughout the site"""
    # Get all images from different models
    images = []
    
    # Menu item images
    menu_items = MenuItem.objects.filter(image__isnull=False).exclude(image='')
    for item in menu_items:
        images.append({
            'id': item.id,
            'name': item.name,
            'image_url': item.image.url if item.image else '',
            'type': 'Menu Item',
            'model_type': 'menuitem',
            'featured': item.is_featured,
            'available': item.is_available,
            'category': item.category.name if item.category else 'No Category'
        })
    
    # Category images
    categories = Category.objects.filter(image__isnull=False).exclude(image='')
    for category in categories:
        images.append({
            'id': category.id,
            'name': category.name,
            'image_url': category.image.url if category.image else '',
            'type': 'Category',
            'model_type': 'category',
            'active': category.is_active,
            'sort_order': category.sort_order
        })
    
    # Content section images
    content_sections = ContentSection.objects.filter(
        Q(image__isnull=False) | Q(background_image__isnull=False)
    ).exclude(image='', background_image='')
    
    for section in content_sections:
        if section.image:
            images.append({
                'id': section.id,
                'name': f"{section.get_section_display()} - Main Image",
                'image_url': section.image.url if section.image else '',
                'type': 'Content Section',
                'model_type': 'contentsection',
                'section': section.get_section_display(),
                'field': 'image'
            })
        if section.background_image:
            images.append({
                'id': section.id,
                'name': f"{section.get_section_display()} - Background",
                'image_url': section.background_image.url if section.background_image else '',
                'type': 'Content Section',
                'model_type': 'contentsection',
                'section': section.get_section_display(),
                'field': 'background_image'
            })
    
    # Site settings images
    try:
        site_settings = SiteSettings.objects.first()
        if site_settings:
            if site_settings.logo:
                images.append({
                    'id': site_settings.id,
                    'name': 'Restaurant Logo',
                    'image_url': site_settings.logo.url if site_settings.logo else '',
                    'type': 'Site Settings',
                    'model_type': 'sitesettings',
                    'field': 'logo'
                })
            if site_settings.favicon:
                images.append({
                    'id': site_settings.id,
                    'name': 'Favicon',
                    'image_url': site_settings.favicon.url if site_settings.favicon else '',
                    'type': 'Site Settings',
                    'model_type': 'sitesettings',
                    'field': 'favicon'
                })
    except:
        pass
    
    # Site images
    site_images = SiteImage.objects.filter(image__isnull=False).exclude(image='')
    for site_image in site_images:
        images.append({
            'id': site_image.id,
            'name': site_image.name,
            'image_url': site_image.image.url if site_image.image else '',
            'type': f'Site Image ({site_image.get_image_type_display()})',
            'model_type': 'siteimage',
            'active': site_image.is_active,
            'image_type': site_image.get_image_type_display()
        })
    
    # Testimonial images
    testimonials = Testimonial.objects.filter(image__isnull=False).exclude(image='')
    for testimonial in testimonials:
        images.append({
            'id': testimonial.id,
            'name': f"{testimonial.customer_name} - Testimonial",
            'image_url': testimonial.image.url if testimonial.image else '',
            'type': 'Testimonial',
            'model_type': 'testimonial',
            'active': testimonial.is_active,
            'rating': testimonial.rating
        })
    
    # Paginate results
    paginator = Paginator(images, 24)  # Show 24 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_images': len(images)
    }
    return render(request, 'custom_admin/all_images.html', context)

# Edit Global Image
@user_passes_test(is_admin)
def edit_global_image(request, model_type, object_id):
    """Edit a specific image from any model"""
    if request.method == 'POST':
        try:
            # Get the model and object
            model_map = {
                'menuitem': MenuItem,
                'category': Category,
                'contentsection': ContentSection,
                'sitesettings': SiteSettings,
                'siteimage': SiteImage,
                'testimonial': Testimonial
            }
            
            if model_type not in model_map:
                messages.error(request, 'Invalid model type')
                return redirect('custom_admin:all_images')
            
            model = model_map[model_type]
            
            # Special handling for SiteSettings (only one instance)
            if model_type == 'sitesettings':
                obj = model.objects.first()
                if not obj:
                    obj = model.objects.create()
            else:
                obj = get_object_or_404(model, id=object_id)
            
            # Handle featured toggle for menu items
            if model_type == 'menuitem' and 'is_featured' in request.POST:
                obj.is_featured = request.POST.get('is_featured') == 'on'
            
            # Handle active toggle for categories and site images
            if model_type == 'category' and 'is_active' in request.POST:
                obj.is_active = request.POST.get('is_active') == 'on'
            
            if model_type == 'siteimage' and 'is_active' in request.POST:
                obj.is_active = request.POST.get('is_active') == 'on'
            
            if model_type == 'testimonial' and 'is_active' in request.POST:
                obj.is_active = request.POST.get('is_active') == 'on'
            
            # Handle image upload from AJAX
            new_image_url = request.POST.get('new_image_url')
            if new_image_url:
                # Image was already uploaded via AJAX, show success message
                # The model field was already updated in the AJAX upload, so we just need to save any other changes
                obj.save()
                messages.success(request, 'Image updated successfully!')
            elif request.FILES.get('image'):
                # Handle direct file upload (fallback)
                # Delete old image if it exists
                field_name = request.POST.get('field_name', 'image')
                if hasattr(obj, field_name) and getattr(obj, field_name):
                    old_image = getattr(obj, field_name)
                    if old_image and hasattr(old_image, 'path') and os.path.exists(old_image.path):
                        os.remove(old_image.path)
                
                # Set new image
                setattr(obj, field_name, request.FILES['image'])
                obj.save()
                messages.success(request, 'Image updated successfully!')
            else:
                # Just save the toggles if no image was uploaded
                obj.save()
                messages.success(request, 'Settings updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating image: {str(e)}')
        
        return redirect('custom_admin:all_images')
    
    # GET request - show edit form
    try:
        model_map = {
            'menuitem': MenuItem,
            'category': Category,
            'contentsection': ContentSection,
            'sitesettings': SiteSettings,
            'siteimage': SiteImage,
            'testimonial': Testimonial
        }
        
        if model_type not in model_map:
            messages.error(request, 'Invalid model type')
            return redirect('custom_admin:all_images')
        
        model = model_map[model_type]
        
        # Special handling for SiteSettings (only one instance)
        if model_type == 'sitesettings':
            obj = model.objects.first()
            if not obj:
                obj = model.objects.create()
        else:
            obj = get_object_or_404(model, id=object_id)
        
        context = {
            'object': obj,
            'model_type': model_type,
            'object_id': object_id
        }
        return render(request, 'custom_admin/edit_global_image.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading image: {str(e)}')
        return redirect('custom_admin:all_images')

# AJAX Global Image Upload
@csrf_exempt
@user_passes_test(is_admin)
def upload_global_image(request):
    """Handle AJAX image uploads for any model"""
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            model_type = request.POST.get('model_type', 'menuitem')
            field_name = request.POST.get('field_name', 'image')
            
            # Generate a unique filename
            import uuid
            from django.utils.text import slugify
            filename = f"{uuid.uuid4().hex}_{slugify(image.name)}"
            
            # Determine upload path based on model type
            upload_paths = {
                'menuitem': 'menu_items',
                'category': 'categories',
                'contentsection': 'content',
                'sitesettings': 'site',
                'siteimage': 'site_images',
                'testimonial': 'testimonials'
            }
            
            upload_dir = upload_paths.get(model_type, 'uploads')
            if model_type == 'contentsection' and field_name == 'background_image':
                upload_dir = 'content/backgrounds'
            
            # Save the image
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            
            path = os.path.join(upload_dir, filename)
            file_path = default_storage.save(path, ContentFile(image.read()))
            image_url = default_storage.url(file_path)
            
            # Also save to the actual model field if object_id is provided
            object_id = request.POST.get('object_id')
            
            if object_id:
                try:
                    model_map = {
                        'menuitem': MenuItem,
                        'category': Category,
                        'contentsection': ContentSection,
                        'sitesettings': SiteSettings,
                        'siteimage': SiteImage,
                        'testimonial': Testimonial
                    }
                    
                    if model_type in model_map:
                        model = model_map[model_type]
                        # Special handling for SiteSettings (only one instance)
                        if model_type == 'sitesettings':
                            obj = model.objects.first()
                            if not obj:
                                obj = model.objects.create()
                        else:
                            obj = get_object_or_404(model, id=object_id)
                        
                        # Delete old image if it exists
                        if hasattr(obj, field_name) and getattr(obj, field_name):
                            old_image = getattr(obj, field_name)
                            if old_image and hasattr(old_image, 'path') and os.path.exists(old_image.path):
                                os.remove(old_image.path)
                        
                        # Save the image properly to the model field
                        from django.core.files.base import ContentFile
                        import os
                        
                        # Generate a unique filename
                        import uuid
                        from django.utils.text import slugify
                        filename = f"{uuid.uuid4().hex}_{slugify(image.name)}"
                        
                        # Determine upload path based on model type
                        upload_paths = {
                            'menuitem': 'menu_items',
                            'category': 'categories',
                            'contentsection': 'content',
                            'sitesettings': 'site',
                            'siteimage': 'site_images',
                            'testimonial': 'testimonials'
                        }
                        
                        upload_dir = upload_paths.get(model_type, 'uploads')
                        if model_type == 'contentsection' and field_name == 'background_image':
                            upload_dir = 'content/backgrounds'
                        
                        path = os.path.join(upload_dir, filename)
                        
                        # Save the image to the model field
                        getattr(obj, field_name).save(filename, ContentFile(image.read()), save=True)
                except Exception as e:
                    pass  # If we can't update the model, at least return the image URL
            
            return JsonResponse({
                'success': True,
                'image_url': image_url
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'No image provided'
    })
