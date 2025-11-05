#!/usr/bin/env python
"""
Script to update the frontend template with the correct hashed filenames
"""

import os
import re
from pathlib import Path

def update_template():
    """Update the frontend template with correct hashed filenames"""
    
    # Get project paths
    project_root = Path(__file__).parent.absolute()
    static_dir = project_root / "static" / "assets"  # Look in the assets subdirectory
    template_path = project_root / "templates" / "frontend" / "index.html"
    
    print(f"Project root: {project_root}")
    print(f"Static directory: {static_dir}")
    print(f"Template path: {template_path}")
    
    # Check if static directory exists
    if not static_dir.exists():
        print("❌ Static directory not found!")
        return False
    
    # Find the hashed JS and CSS files (get the most recently modified ones)
    js_files = []
    css_files = []
    
    for file in static_dir.iterdir():
        if file.is_file():
            if file.name.startswith('index-') and file.name.endswith('.js'):
                js_files.append((file.name, file.stat().st_mtime))
            elif file.name.startswith('index-') and file.name.endswith('.css'):
                css_files.append((file.name, file.stat().st_mtime))
    
    if not js_files or not css_files:
        print("❌ Could not find hashed JS or CSS files!")
        return False
    
    # Sort by modification time to get the latest files
    js_files.sort(key=lambda x: x[1], reverse=True)
    css_files.sort(key=lambda x: x[1], reverse=True)
    
    js_file = js_files[0][0]
    css_file = css_files[0][0]
    
    print(f"Found JS file: {js_file}")
    print(f"Found CSS file: {css_file}")
    
    # Read the template
    if not template_path.exists():
        print("❌ Template file not found!")
        return False
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Update the template with correct filenames using the static URL pattern
    # Handle both possible patterns that might be in the template
    updated_content = re.sub(
        r'src="/static/assets/index-[a-f0-9]+\.js"',
        f'src="/static/assets/{js_file}"',
        template_content
    )
    updated_content = re.sub(
        r'href="/static/assets/index-[a-f0-9]+\.css"',
        f'href="/static/assets/{css_file}"',
        updated_content
    )
    
    # Also handle the original paths that might be in the template
    updated_content = re.sub(
        r'src="/assets/index-[a-f0-9]+\.js"',
        f'src="/static/assets/{js_file}"',
        updated_content
    )
    updated_content = re.sub(
        r'href="/assets/index-[a-f0-9]+\.css"',
        f'href="/static/assets/{css_file}"',
        updated_content
    )
    
    # Write the updated template
    with open(template_path, 'w') as f:
        f.write(updated_content)
    
    print("✅ Template updated with correct filenames!")
    print(f"  JS file: {js_file}")
    print(f"  CSS file: {css_file}")
    
    return True

if __name__ == "__main__":
    success = update_template()
    exit(0 if success else 1)