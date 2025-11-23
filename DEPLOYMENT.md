# Deployment Guide

Complete guide to deploy the Chemical Equipment Parameter Visualizer to production.

## 🌐 Deployment Options

### Backend Options
- **Render** (Recommended - Free tier available)
- **Railway** (Easy deployment)
- **Heroku** (Popular choice)
- **PythonAnywhere** (Django-friendly)
- **AWS EC2** (Full control)

### Frontend Options
- **Netlify** (Recommended - Free tier)
- **Vercel** (Fast and easy)
- **GitHub Pages** (Free for static sites)
- **AWS S3 + CloudFront** (Scalable)

## 🚀 Deploy Backend to Render

### Step 1: Prepare Backend

1. **Create `Procfile` in backend directory:**

```
web: gunicorn chemical_equipment_viz.wsgi --log-file -
```

2. **Update `requirements.txt`:**

```txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
pandas==2.1.3
numpy==1.26.2
reportlab==4.0.7
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

3. **Update `settings.py`:**

```python
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ... existing INSTALLED_APPS ...
INSTALLED_APPS = [
    # ... existing apps ...
    'whitenoise.runserver_nostatic',  # Add before staticfiles
    'django.contrib.staticfiles',
]

# ... existing MIDDLEWARE ...
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add after SecurityMiddleware
    # ... rest of middleware ...
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS Settings for production
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000'
).split(',')

# Security Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

4. **Create `build.sh` (for Render):**

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

### Step 2: Deploy to Render

1. **Push to GitHub:**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Create Render Account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: chemical-equipment-api
     - **Environment**: Python 3
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn chemical_equipment_viz.wsgi:application`
     - **Plan**: Free

4. **Set Environment Variables:**
   - SECRET_KEY: `your-secret-key-here`
   - DEBUG: `False`
   - ALLOWED_HOSTS: `your-app.onrender.com`
   - DATABASE_URL: (automatically set by Render if using PostgreSQL)
   - CORS_ALLOWED_ORIGINS: `https://your-frontend.netlify.app`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your API will be at: `https://your-app.onrender.com`

## 🌟 Deploy Frontend to Netlify

### Step 1: Prepare Frontend

1. **Update API URL in `App.jsx`:**

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
```

2. **Create `.env.production` in frontend-web:**

```
REACT_APP_API_URL=https://your-backend.onrender.com/api
```

3. **Create `netlify.toml` in frontend-web:**

```toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

4. **Update `package.json`:**

```json
{
  "name": "chemical-equipment-visualizer-web",
  "version": "1.0.0",
  "private": true,
  "homepage": ".",
  "dependencies": {
    // ... existing dependencies
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

### Step 2: Deploy to Netlify

1. **Build Locally (optional test):**
```bash
cd frontend-web
npm run build
```

2. **Deploy via Netlify CLI:**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend-web
netlify deploy --prod
```

Or:

3. **Deploy via Netlify Dashboard:**
   - Go to [netlify.com](https://www.netlify.com)
   - Sign up with GitHub
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub repository
   - Configure:
     - **Base directory**: frontend-web
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend-web/build`
   - Add Environment Variables:
     - `REACT_APP_API_URL`: `https://your-backend.onrender.com/api`
   - Click "Deploy site"

Your app will be at: `https://your-app.netlify.app`

## 🔒 Security Configuration

### Backend Security Checklist

1. **Generate Strong Secret Key:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

2. **Environment Variables:**
   - Never commit `.env` files
   - Use platform environment variables
   - Rotate keys regularly

3. **Database Security:**
   - Use PostgreSQL in production
   - Enable SSL connections
   - Regular backups

4. **CORS Configuration:**
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.netlify.app",
    "https://www.yourdomain.com",
]

CORS_ALLOW_CREDENTIALS = True
```

5. **Rate Limiting:**
```bash
pip install django-ratelimit
```

```python
# views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h')
def upload_csv(request):
    # ... existing code
```

## 📊 Database Migration

### From SQLite to PostgreSQL

1. **Install PostgreSQL locally:**
   - Download from [postgresql.org](https://www.postgresql.org/download/)

2. **Update settings.py:**
```python
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://user:password@localhost:5432/dbname',
        conn_max_age=600
    )
}
```

3. **Migrate data:**
```bash
# Dump SQLite data
python manage.py dumpdata > data.json

# Switch to PostgreSQL in settings
# Run migrations
python manage.py migrate

# Load data
python manage.py loaddata data.json
```

## 🔧 Custom Domain Setup

### Netlify

1. Go to Site Settings → Domain Management
2. Add custom domain
3. Update DNS records:
   - Add CNAME record: `www` → `your-app.netlify.app`
   - Add A record: `@` → Netlify IP

### Render

1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records as shown

## 📈 Monitoring & Logging

### Backend Monitoring

1. **Sentry for Error Tracking:**
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

2. **Logging Configuration:**
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### Frontend Monitoring

1. **Google Analytics:**
```bash
npm install react-ga4
```

```javascript
// index.js
import ReactGA from 'react-ga4';

ReactGA.initialize('YOUR-GA-ID');
```

## 🚀 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          python manage.py test

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Netlify
        uses: netlify/actions/cli@master
        with:
          args: deploy --prod
        env:
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```

## 📱 Mobile-Friendly Optimization

1. **Add viewport meta tag** in `public/index.html`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

2. **Responsive CSS** (already included in App.css)

3. **PWA Support** (optional):
```bash
npm install --save-dev workbox-webpack-plugin
```

## 🔄 Backup Strategy

### Automated Backups

1. **Database Backup Script:**
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://your-backup-bucket/
```

2. **Schedule with cron:**
```bash
0 2 * * * /path/to/backup.sh
```

## 📊 Performance Optimization

### Backend

1. **Enable caching:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Database indexing:**
```python
class EquipmentDataset(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['user', '-upload_date']),
        ]
```

### Frontend

1. **Code splitting:**
```javascript
const Visualization = React.lazy(() => import('./Visualization'));
```

2. **Image optimization:**
   - Use WebP format
   - Implement lazy loading

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Secret keys generated
- [ ] Debug mode disabled
- [ ] CORS configured
- [ ] Static files collected
- [ ] Database migrated

### Post-Deployment
- [ ] Test all API endpoints
- [ ] Test file upload
- [ ] Test PDF generation
- [ ] Verify authentication
- [ ] Check error logging
- [ ] Monitor performance
- [ ] Test on mobile devices

## 🆘 Troubleshooting Deployment

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --clear --no-input
```

**CORS errors:**
- Check ALLOWED_HOSTS
- Verify CORS_ALLOWED_ORIGINS
- Check frontend API_URL

**Database connection errors:**
- Verify DATABASE_URL
- Check database credentials
- Ensure database is running

**Build failures:**
- Check build logs
- Verify all dependencies installed
- Check Node/Python versions

## 📞 Support

For deployment issues:
- Check platform documentation
- Review deployment logs
- Check environment variables
- Test locally first

---

**Congratulations!** Your app is now deployed and accessible worldwide! 🎉

Update the README.md with your live URLs after deployment.