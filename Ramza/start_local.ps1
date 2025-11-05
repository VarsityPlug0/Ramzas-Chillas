# PowerShell script to start Ramza's Chillas locally
Write-Host "Starting Ramza's Chillas Restaurant Management System" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

# Get the current directory
$currentDir = Get-Location
Write-Host "Current directory: $currentDir"

# Go to the parent directory
Set-Location ".."

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\ramzas_env\Scripts\Activate.ps1"

# Go back to the project directory
Set-Location "ramzas-chillas"

# Verify Django is available
Write-Host "Checking Django installation..." -ForegroundColor Yellow
python -c "import django; print('Django version:', django.get_version())"

# Start the development server
Write-Host "Starting development server..." -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Server starting at http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin panel: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "Login with admin / admin123" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

python manage.py runserver