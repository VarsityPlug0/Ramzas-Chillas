#!/usr/bin/env python
"""
Test database connection and migrations
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_restaurant.settings')

# Setup Django
django.setup()

def test_database_connection():
    """Test if we can connect to the database"""
    try:
        from django.db import connection
        print("Testing database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"Database connection successful: {result}")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tables_exist():
    """Test if required tables exist"""
    try:
        from django.db import connection
        tables = connection.introspection.table_names()
        print(f"Existing tables: {tables}")
        
        required_tables = [
            'restaurant_sitesettings',
            'restaurant_contentsection', 
            'restaurant_siteimage'
        ]
        
        missing_tables = []
        for table in required_tables:
            if table not in tables:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"Missing tables: {missing_tables}")
            return False
        else:
            print("All required tables exist")
            return True
    except Exception as e:
        print(f"Error checking tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_migrations():
    """Show migration status"""
    try:
        from django.core.management import execute_from_command_line
        print("Current migration status:")
        execute_from_command_line(['manage.py', 'showmigrations'])
        return True
    except Exception as e:
        print(f"Error showing migrations: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== Database Connection Test ===")
    
    # Test database connection
    if not test_database_connection():
        sys.exit(1)
    
    # Show migrations
    if not show_migrations():
        sys.exit(1)
        
    # Test if tables exist
    if not test_tables_exist():
        print("Some tables are missing. You may need to run migrations.")
        sys.exit(1)
    
    print("All tests passed!")