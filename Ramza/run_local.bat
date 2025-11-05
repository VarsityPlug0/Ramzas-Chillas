@echo off
echo Ramza's Chillas - Local Setup and Run Script
echo =============================================

echo.
echo Changing to project directory...
cd /d "c:\Users\money\Bevan The IT GUY\absa\ramzas-chillas"

echo.
echo Setting up Python virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Error creating virtual environment
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Error activating virtual environment
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo Error upgrading pip
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Installing required packages...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error installing requirements
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Running database migrations...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo Error running migrations
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Creating superuser (admin/admin123)...
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(is_superuser=True).exists() else None | python manage.py shell
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Could not create superuser
)

echo.
echo Populating default content...
python manage.py populate_content
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Could not populate default content
)

echo.
echo Collecting static files...
python manage.py collectstatic --noinput
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Could not collect static files
)

echo.
echo Starting development server...
echo.
echo =============================================
echo Setup complete! Opening browser and starting server...
echo.
echo Admin: http://127.0.0.1:8000/admin/
echo Home: http://127.0.0.1:8000/
echo.
echo Login with admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo =============================================
echo.

python manage.py runserver
if %ERRORLEVEL% NEQ 0 (
    echo Error starting server
    pause
    exit /b %ERRORLEVEL%
)

pause