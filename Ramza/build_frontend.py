#!/usr/bin/env python
"""
Build script for frontend assets
"""
import os
import subprocess
import sys
from pathlib import Path

def build_frontend():
    """Build the frontend assets"""
    project_root = Path(__file__).parent.absolute()
    frontend_dir = project_root / "frontend"
    
    print(f"Project root: {project_root}")
    print(f"Frontend directory: {frontend_dir}")
    
    # Check if frontend directory exists
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    print(f"Changed to frontend directory: {os.getcwd()}")
    
    # Install npm dependencies
    print("Installing npm dependencies...")
    try:
        result = subprocess.run(["npm", "install"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ npm install failed: {result.stderr}")
            return False
        print("✅ npm dependencies installed successfully")
    except Exception as e:
        print(f"❌ Error running npm install: {e}")
        return False
    
    # Build frontend
    print("Building frontend...")
    try:
        result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Frontend build failed: {result.stderr}")
            return False
        print("✅ Frontend built successfully")
    except Exception as e:
        print(f"❌ Error running frontend build: {e}")
        return False
    
    # Change back to project root
    os.chdir(project_root)
    print(f"Changed back to project root: {os.getcwd()}")
    
    # Copy built files to static directory
    dist_dir = frontend_dir / "dist"
    static_assets_dir = project_root / "static" / "assets"
    
    if dist_dir.exists():
        print(f"Copying built files from {dist_dir} to {static_assets_dir}")
        # Create static assets directory if it doesn't exist
        static_assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all files from dist to static assets
        import shutil
        for item in dist_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, static_assets_dir / item.name)
                print(f"Copied {item.name}")
            elif item.is_dir():
                dest_dir = static_assets_dir / item.name
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(item, dest_dir)
                print(f"Copied directory {item.name}")
        print("✅ Built files copied to static directory")
    else:
        print("❌ Dist directory not found!")
        return False
    
    return True

if __name__ == "__main__":
    success = build_frontend()
    sys.exit(0 if success else 1)