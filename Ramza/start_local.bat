@echo off
cls
echo =====================================================
echo    Ramza's Chillas - Restaurant Management System    
echo =====================================================
echo.

REM Change to the project directory
cd /d "c:\Users\money\Bevan The IT GUY\absa\ramzas-chillas"

REM Activate the virtual environment
echo Activating virtual environment...
call "..\ramzas_env\Scripts\activate.bat"
echo.

REM Verify Django is available
echo Checking Django installation...
python -c "import django; print('Django version:', django.get_version())"
echo.

REM Start the development server
echo =====================================================
echo Server starting at http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
echo.
echo Login with admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo =====================================================
echo.

python manage.py runserver

pause