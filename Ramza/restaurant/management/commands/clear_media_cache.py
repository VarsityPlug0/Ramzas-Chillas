from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Clear media cache and reset any cached image references'

    def handle(self, *args, **options):
        # Clear Django cache
        try:
            cache.clear()
            self.stdout.write(
                self.style.SUCCESS('Successfully cleared Django cache')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to clear Django cache: {e}')
            )

        # Clear media directory cache files if any
        media_dirs = [
            os.path.join(settings.MEDIA_ROOT, 'categories'),
            os.path.join(settings.MEDIA_ROOT, 'menu_items'),
        ]
        
        cleared_count = 0
        for media_dir in media_dirs:
            if os.path.exists(media_dir):
                # Look for any cache files (files that might be temporary or cache files)
                for filename in os.listdir(media_dir):
                    if filename.startswith('.') or '.tmp' in filename or '.cache' in filename:
                        file_path = os.path.join(media_dir, filename)
                        try:
                            os.remove(file_path)
                            self.stdout.write(
                                self.style.SUCCESS(f'Removed cache file: {file_path}')
                            )
                            cleared_count += 1
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f'Failed to remove {file_path}: {e}')
                            )
        
        if cleared_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Cleared {cleared_count} cache files')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No cache files found in media directories')
            )

        self.stdout.write(
            self.style.SUCCESS('Media cache clearing completed')
        )