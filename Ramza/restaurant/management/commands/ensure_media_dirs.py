import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Ensure media directories exist with proper permissions'

    def handle(self, *args, **options):
        # Ensure media root exists
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            os.makedirs(media_root, exist_ok=True)
            self.stdout.write(f'Created media root directory: {media_root}')
        else:
            self.stdout.write(f'Media root directory exists: {media_root}')
        
        # Ensure categories directory exists
        categories_dir = os.path.join(media_root, 'categories')
        if not os.path.exists(categories_dir):
            os.makedirs(categories_dir, exist_ok=True)
            self.stdout.write(f'Created categories directory: {categories_dir}')
        else:
            self.stdout.write(f'Categories directory exists: {categories_dir}')
        
        # Ensure menu_items directory exists
        menu_items_dir = os.path.join(media_root, 'menu_items')
        if not os.path.exists(menu_items_dir):
            os.makedirs(menu_items_dir, exist_ok=True)
            self.stdout.write(f'Created menu_items directory: {menu_items_dir}')
        else:
            self.stdout.write(f'Menu items directory exists: {menu_items_dir}')
        
        # Ensure site directory exists
        site_dir = os.path.join(media_root, 'site')
        if not os.path.exists(site_dir):
            os.makedirs(site_dir, exist_ok=True)
            self.stdout.write(f'Created site directory: {site_dir}')
        else:
            self.stdout.write(f'Site directory exists: {site_dir}')
        
        # Ensure content directory exists
        content_dir = os.path.join(media_root, 'content')
        if not os.path.exists(content_dir):
            os.makedirs(content_dir, exist_ok=True)
            self.stdout.write(f'Created content directory: {content_dir}')
        else:
            self.stdout.write(f'Content directory exists: {content_dir}')
        
        # Ensure content/backgrounds directory exists
        content_backgrounds_dir = os.path.join(media_root, 'content', 'backgrounds')
        if not os.path.exists(content_backgrounds_dir):
            os.makedirs(content_backgrounds_dir, exist_ok=True)
            self.stdout.write(f'Created content/backgrounds directory: {content_backgrounds_dir}')
        else:
            self.stdout.write(f'Content/backgrounds directory exists: {content_backgrounds_dir}')
        
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully ensured all media directories exist'
            )
        )