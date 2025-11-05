#!/usr/bin/env python
import os
import sys
import subprocess

# Get the absolute path to the Ramza directory
script_dir = os.path.dirname(os.path.abspath(__file__))
ramza_dir = os.path.join(script_dir, 'Ramza')

print(f"Script directory: {script_dir}")
print(f"Ramza directory: {ramza_dir}")
print(f"Current working directory: {os.getcwd()}")

# Change to the Ramza directory where start_server.py is located
print(f"Changing directory to: {ramza_dir}")
os.chdir(ramza_dir)

# Execute start_server.py with absolute path
start_server_path = os.path.join(ramza_dir, 'start_server.py')
print(f"Executing: {start_server_path}")
subprocess.run([sys.executable, start_server_path])