#!/usr/bin/env python
"""
Script to build the React frontend and integrate it with Django
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_frontend():
    """Build the React frontend and copy assets to Django static directory"""
    
    # Get project paths
    project_root = Path(__file__).parent.absolute()
    frontend_dir = project_root / "frontend"
    static_dir = project_root / "static"
    build_dir = frontend_dir / "dist"
    
    print(f"Project root: {project_root}")
    print(f"Frontend directory: {frontend_dir}")
    print(f"Static directory: {static_dir}")
    print(f"Build directory: {build_dir}")
    
    # Check if frontend directory exists
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Check if build directory exists
    if not build_dir.exists():
        print("❌ Build directory not found! Building frontend...")
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Install npm dependencies if node_modules doesn't exist
        node_modules_dir = frontend_dir / "node_modules"
        if not node_modules_dir.exists():
            print("📦 Installing npm dependencies...")
            try:
                subprocess.run(["npm", "install"], check=True)
                print("✅ npm dependencies installed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install npm dependencies: {e}")
                return False
        
        # Build the React app
        print("🔨 Building React frontend...")
        try:
            subprocess.run(["npm", "run", "build"], check=True)
            print("✅ React frontend built successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build React frontend: {e}")
            return False
    
    # Check if build was successful
    if not build_dir.exists():
        print("❌ Build directory not found!")
        return False
    
    # Create static directory if it doesn't exist
    static_dir.mkdir(exist_ok=True)
    
    # Copy built assets to static directory
    print("📂 Copying built assets to Django static directory...")
    
    # Copy all files from build directory to static
    for item in build_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, static_dir / item.name)
            print(f"  📄 Copied {item.name}")
        elif item.is_dir():
            target_dir = static_dir / item.name
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(item, target_dir)
            print(f"  📁 Copied directory {item.name}")
    
    print("✅ Frontend assets copied to static directory!")
    
    # Create a simple index.html template for Django
    templates_dir = project_root / "templates" / "frontend"
    templates_dir.mkdir(exist_ok=True, parents=True)
    
    index_html_content = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="{% static 'favicon.ico' %}" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ramza's Chillas - Chill Vibes & Hot Food</title>
    <script type="module" crossorigin src="{% static 'index.js' %}"></script>
    <link rel="stylesheet" href="{% static 'index.css' %}">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>"""
    
    index_html_path = templates_dir / "index.html"
    with open(index_html_path, 'w') as f:
        f.write(index_html_content)
    
    print("✅ Django template created!")
    print("🎉 Frontend build and integration completed successfully!")
    return True

if __name__ == "__main__":
    success = build_frontend()
    sys.exit(0 if success else 1)