#!/usr/bin/env python
import os
import sys
import subprocess

# Change to the Ramza directory where the actual start_server.py is located
script_dir = os.path.dirname(os.path.abspath(__file__))
ramza_dir = os.path.join(script_dir, 'Ramza')

print(f"Changing directory to: {ramza_dir}")
os.chdir(ramza_dir)

# Execute the actual start_server.py
print("Executing Ramza/start_server.py...")
subprocess.run([sys.executable, 'start_server.py'])