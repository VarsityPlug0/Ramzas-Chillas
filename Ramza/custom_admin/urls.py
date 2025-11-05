from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Menu Items
    path('menu-items/', views.menu_items, name='menu_items'),
    path('menu-items/add/', views.edit_menu_item, name='add_menu_item'),
    path('menu-items/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu-items/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('menu-items/upload-image/', views.upload_menu_item_image, name='upload_menu_item_image'),
    
    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.edit_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/upload-image/', views.upload_category_image, name='upload_category_image'),
    
    # Orders
    path('orders/', views.orders, name='orders'),
    path('orders/update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    
    # Site Settings
    path('settings/', views.site_settings, name='site_settings'),
    
    # Content Sections
    path('content-sections/', views.content_sections, name='content_sections'),
    path('content-sections/add/', views.edit_content_section, name='add_content_section'),
    path('content-sections/edit/<int:section_id>/', views.edit_content_section, name='edit_content_section'),
    path('content-sections/delete/<int:section_id>/', views.delete_content_section, name='delete_content_section'),
    
    # Site Images
    path('site-images/', views.site_images, name='site_images'),
    path('site-images/add/', views.edit_site_image, name='add_site_image'),
    path('site-images/edit/<int:image_id>/', views.edit_site_image, name='edit_site_image'),
    path('site-images/delete/<int:image_id>/', views.delete_site_image, name='delete_site_image'),
    
    # Testimonials
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/add/', views.edit_testimonial, name='add_testimonial'),
    path('testimonials/edit/<int:testimonial_id>/', views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/delete/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
    
    # Global Images
    path('all-images/', views.all_images, name='all_images'),
    path('all-images/edit/<str:model_type>/<int:object_id>/', views.edit_global_image, name='edit_global_image'),
    path('all-images/upload/', views.upload_global_image, name='upload_global_image'),
]