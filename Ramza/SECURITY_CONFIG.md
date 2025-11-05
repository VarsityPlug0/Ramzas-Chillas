# Security Configuration Guide

This document explains how to properly configure secrets and sensitive information for the Ramza's Chillas application.

## Secrets Management

### 1. Environment Variables

All sensitive information should be stored as environment variables, never hardcoded in the source code.

#### Required Environment Variables for Render Deployment:
- `DATABASE_URL`: PostgreSQL database connection string
- `SECRET_KEY`: Django secret key
- `DB_NAME`: PostgreSQL database name (for local development)
- `DB_USER`: PostgreSQL database user (for local development)
- `DB_PASSWORD`: PostgreSQL database password (for local development)
- `DB_HOST`: PostgreSQL database host (for local development)
- `DB_PORT`: PostgreSQL database port (for local development)

### 2. Render Dashboard Configuration

In the Render Dashboard, you should configure these environment variables:

1. Go to your Render Dashboard
2. Select your service
3. Go to "Environment" tab
4. Add the following environment variables:

```
DATABASE_URL=your_postgresql_connection_string_here
SECRET_KEY=your_random_secret_key_here
```

For the DATABASE_URL, you can either:
- Use Render's built-in database service (recommended)
- Use an external PostgreSQL provider

### 3. Local Development Configuration

For local development, create a `.env` file in the project root directory with the following content:

```env
# Database Configuration
DB_NAME=your_local_db_name
DB_USER=your_local_db_user
DB_PASSWORD=your_local_db_password
DB_HOST=localhost
DB_PORT=5432

# Django Secret Key
SECRET_KEY=your_local_secret_key

# Debug Mode (only for development)
DEBUG=True
```

### 4. Secret Key Generation

To generate a new secret key, you can use Django's built-in function:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use this command:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Git Security

The following files should NEVER be committed to version control:
- `.env` files
- Any file containing passwords or secrets
- Local configuration files with sensitive data

The `.gitignore` file should already include patterns to prevent these files from being committed.

### 6. Database Security

#### For Render Deployment:
Use Render's built-in PostgreSQL database service which automatically manages credentials securely.

#### For External PostgreSQL:
Ensure your database connection uses SSL by adding `?sslmode=require` to your DATABASE_URL.

### 7. Best Practices

1. **Never commit secrets to version control**
2. **Use different secret keys for development and production**
3. **Regularly rotate secrets**
4. **Use environment variables for all sensitive configuration**
5. **Enable SSL for database connections**
6. **Use strong, randomly generated passwords**
7. **Limit database user permissions to only what's necessary**

### 8. Troubleshooting

If you encounter authentication errors:

1. Verify all environment variables are correctly set
2. Check that the database URL is properly formatted
3. Ensure the database user has the correct permissions
4. Verify network connectivity to the database server

### 9. Security Checklist

Before deployment, ensure:
- [ ] No hardcoded credentials in source code
- [ ] All secrets are stored as environment variables
- [ ] `.env` files are in `.gitignore`
- [ ] SECRET_KEY is different for development and production
- [ ] Database connections use SSL
- [ ] Database user has minimal required permissions

### 10. Recent Security Improvements

The following security improvements have been implemented:

1. **Removed hardcoded database credentials** from `render.yaml` and `settings.py`
2. **Implemented environment variable-based configuration** for all sensitive data
3. **Updated database connection handling** to use environment variables
4. **Created security documentation** to guide proper configuration
5. **Added .env.example file** to show developers how to set up their local environment