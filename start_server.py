#!/usr/bin/env python
import os
import sys
import subprocess

# Change to the Ramza directory where the actual start_server.py is located
script_dir = os.path.dirname(os.path.abspath(__file__))
ramza_dir = os.path.join(script_dir, 'Ramza')

print(f"Changing directory to: {ramza_dir}")
os.chdir(ramza_dir)

# Update frontend template with correct hashed filenames before starting
print("Updating frontend template with correct hashed filenames...")
try:
    update_script = os.path.join(ramza_dir, 'update_frontend_template.py')
    if os.path.exists(update_script):
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

# Execute the actual start_server.py
print("Executing Ramza/start_server.py...")
subprocess.run([sys.executable, 'start_server.py'])