# Local Setup Instructions for Ramza's Chillas

## Prerequisites
- Python 3.13.x installed
- Git (optional, for version control)

## Setup Process

### 1. Create Virtual Environment
```bash
cd c:\Users\money\Bevan The IT GUY\absa
python -m venv ramzas_env
```

### 2. Activate Virtual Environment
```bash
# Windows
ramzas_env\Scripts\activate
```

### 3. Install Dependencies
```bash
cd ramzas-chillas
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Populate Default Content
```bash
python manage.py populate_content
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Start Development Server
```bash
python manage.py runserver
```

## Alternative Method (Windows)
Simply double-click the `start_local.bat` file to automatically:
1. Activate the virtual environment
2. Start the development server

## Accessing the Application
- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Default Admin Credentials**: 
  - Username: admin
  - Password: admin123

## Stopping the Server
Press `Ctrl+C` in the terminal to stop the development server.

## Troubleshooting
1. If you encounter import errors, make sure the virtual environment is activated
2. If static files are not loading, ensure you ran `collectstatic`
3. If database errors occur, make sure you ran `migrate`