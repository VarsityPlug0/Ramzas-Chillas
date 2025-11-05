# Deployment Checklist for Render

This checklist ensures that all necessary steps are completed before deploying to Render.

## Pre-deployment Checks

### 1. Code and Configuration
- [x] All code changes are committed and pushed to GitHub
- [x] `render.yaml` is properly configured with correct database URL
- [x] `requirements.txt` includes all necessary dependencies
- [x] `runtime.txt` specifies the correct Python version
- [x] `Procfile` correctly defines the start command
- [x] Static files configuration is correct in `settings.py`
- [x] Media files configuration is correct in `settings.py`
- [x] Database configuration uses environment variables
- [x] Security settings are appropriate for production (DEBUG=False)
- [x] Allowed hosts include Render domain names

### 2. Database
- [x] Database migrations are created and committed
- [x] Database URL is properly configured in Render environment
- [x] PostgreSQL database service is configured in `render.yaml`

### 3. Media and Static Files
- [x] Media directories are created with proper permissions
- [x] Static files can be collected successfully
- [x] WhiteNoise is configured for serving static files
- [x] Media files serving is configured for production

### 4. Environment Variables
- [x] SECRET_KEY is set as a secret environment variable in Render
- [x] DATABASE_URL is set in Render environment
- [x] All other required environment variables are configured

## Deployment Process

### 1. Render Dashboard Setup
1. Go to Render Dashboard
2. Connect your GitHub repository
3. Select the branch to deploy (usually master/main)
4. Review and confirm the `render.yaml` configuration
5. Click "Apply" to start deployment

### 2. Post-deployment Verification
- [ ] Application starts without errors
- [ ] Database migrations run successfully
- [ ] Static files are served correctly
- [ ] Media files are accessible
- [ ] Admin interface is accessible
- [ ] Custom admin dashboard works
- [ ] Menu items display correctly
- [ ] Category images display correctly
- [ ] All pages load without errors

## Troubleshooting

### Common Issues
1. **Application fails to start**: Check logs in Render dashboard
2. **Database connection errors**: Verify DATABASE_URL environment variable
3. **Static files not found**: Ensure `collectstatic` runs during deployment
4. **Media files not accessible**: Check media directory permissions and configuration
5. **Permission denied errors**: Ensure proper directory permissions

### Useful Commands for Debugging
```bash
# Check application logs
render logs -a <app-name>

# Run management commands
render run -a <app-name> python manage.py <command>

# Check database connection
render run -a <app-name> python manage.py dbshell
```

## Maintenance

### Regular Tasks
- [ ] Monitor application logs for errors
- [ ] Check disk space usage for media files
- [ ] Backup database regularly
- [ ] Update dependencies periodically
- [ ] Review and rotate secret keys

### Scaling Considerations
- Monitor resource usage (CPU, memory, disk)
- Consider using a CDN for media files
- Optimize database queries
- Implement caching where appropriate