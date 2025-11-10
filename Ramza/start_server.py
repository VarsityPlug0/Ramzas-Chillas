#!/usr/bin/env python
import os
import sys
import django
import shutil
from django.core.management import execute_from_command_line

print("=== START SERVER SCRIPT ===")
print(f"Working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

# Add current directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    print(f"Added {current_dir} to Python path")

# Change to the directory where manage.py is located
os.chdir(current_dir)
print(f"Changed directory to: {os.getcwd()}")

# Update frontend template with correct hashed filenames
print("Updating frontend template with correct hashed filenames...")
try:
    update_script = os.path.join(current_dir, 'update_frontend_template.py')
    if os.path.exists(update_script):
        import subprocess
        result = subprocess.run([sys.executable, update_script], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend template updated successfully!")
        else:
            print(f"⚠️  Warning: Failed to update frontend template: {result.stderr}")
    else:
        print("⚠️  Warning: update_frontend_template.py not found")
except Exception as e:
    print(f"⚠️  Warning: Error updating frontend template: {e}")

# Copy built frontend files to static directory if they don't exist
print("Ensuring frontend assets are in static directory...")
try:
    frontend_dist = os.path.join(current_dir, 'frontend', 'dist')
    static_assets = os.path.join(current_dir, 'static', 'assets')
    
    if os.path.exists(frontend_dist):
        print(f"Found frontend dist directory: {frontend_dist}")
        # Copy files from dist to static
        if not os.path.exists(static_assets):
            os.makedirs(static_assets)
            print(f"Created static assets directory: {static_assets}")
        
        # Copy all files from dist to static
        for item in os.listdir(frontend_dist):
            source = os.path.join(frontend_dist, item)
            destination = os.path.join(static_assets, item)
            if os.path.isfile(source):
                shutil.copy2(source, destination)
                print(f"Copied {item} to static assets")
            elif os.path.isdir(source):
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
                print(f"Copied directory {item} to static assets")
    else:
        print(f"Frontend dist directory not found: {frontend_dist}")
except Exception as e:
    print(f"⚠️  Warning: Error copying frontend assets: {e}")

try:
    print("Setting up Django...")
    django.setup()
    print("Django setup completed successfully")
except Exception as e:
    print(f"Error during Django setup: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Ensure staticfiles directory exists
print("Ensuring staticfiles directory exists...")
static_root = os.path.join(current_dir, 'staticfiles')
if not os.path.exists(static_root):
    os.makedirs(static_root)
    print(f"Created staticfiles directory: {static_root}")
else:
    print(f"Staticfiles directory already exists: {static_root}")

# Collect static files
print("Collecting static files...")
try:
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--verbosity=1', '--clear'])
    print("Static files collected successfully")
except Exception as e:
    print(f"Error collecting static files: {e}")
    import traceback
    traceback.print_exc()
    # Don't exit on static file error as it's not critical for the app to run

# Run migrations
print("Running Django migrations...")
try:
    execute_from_command_line(['manage.py', 'showmigrations'])
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("Migrations completed successfully")
except Exception as e:
    print(f"Error running migrations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create superuser if needed
print("Creating superuser if needed...")
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating new superuser...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f"Error creating superuser: {e}")
    # Don't exit on superuser error as it's not critical for the app to run

# Start Django development server
print("Starting Django development server...")
port = os.environ.get('PORT', '8000')
print(f"Binding to port {port}")

try:
    execute_from_command_line([
        'manage.py', 
        'runserver', 
        f'0.0.0.0:{port}',
        '--noreload'
    ])
except Exception as e:
    print(f"Error starting Django development server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)