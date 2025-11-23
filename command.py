# Complete Commands Reference

#All commands needed to setup, run, and deploy the Chemical Equipment Parameter Visualizer.

## 📋 Table of Contents
- [Initial Setup](#initial-setup)
- [Backend Commands](#backend-commands)
- [Frontend Commands](#frontend-commands)
- [Desktop App Commands](#desktop-app-commands)
- [Git Commands](#git-commands)
- [Deployment Commands](#deployment-commands)
- [Troubleshooting Commands](#troubleshooting-commands)

---

## Initial Setup

### Create Project Structure

```bash
# Create main directory
mkdir chemical-equipment-visualizer
cd chemical-equipment-visualizer

# Create subdirectories
mkdir -p backend/chemical_equipment_viz
mkdir -p backend/api
mkdir -p frontend-web/src
mkdir -p frontend-web/public
mkdir -p desktop-app
```

### Initialize Git

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

---

## Backend Commands

### Setup Virtual Environment

**Windows:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

# Or install individually:
pip install Django==4.2.7
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install pandas==2.1.3
pip install numpy==1.26.2
pip install reportlab==4.0.7
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0
```

### Django Project Setup

```bash
# Create Django project (first time only)
django-admin startproject chemical_equipment_viz .
django-admin startapp api

# Create migrations
python manage.py makemigrations
python manage.py makemigrations api

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

# Collect static files (for production)
python manage.py collectstatic --no-input
```

### Run Development Server

```bash
# Default (port 8000)
python manage.py runserver

# Custom port
python manage.py runserver 8001

# Listen on all interfaces
python manage.py runserver 0.0.0.0:8000
```

### Database Commands

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Reverse migration
python manage.py migrate api 0001

# Reset database (CAUTION: Deletes all data)
rm db.sqlite3
python manage.py migrate

# Dump data
python manage.py dumpdata > data.json

# Load data
python manage.py loaddata data.json
```

### Django Shell

```bash
# Open Django shell
python manage.py shell

# In shell:
from django.contrib.auth.models import User
from api.models import EquipmentDataset

# List all users
User.objects.all()

# List all datasets
EquipmentDataset.objects.all()

# Create test user
User.objects.create_user('testuser', 'test@example.com', 'testpass123')
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test api

# Run with verbosity
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

---

## Frontend Commands

### Setup

```bash
cd frontend-web

# Create React app (first time only)
npx create-react-app .

# Or with specific template
npx create-react-app . --template minimal
```

### Install Dependencies

```bash
# Install all dependencies
npm install

# Install specific packages
npm install axios
npm install chart.js react-chartjs-2

# Install dev dependencies
npm install --save-dev eslint prettier
```

### Development

```bash
# Start development server
npm start

# Start on different port
PORT=3001 npm start

# Build for production
npm run build

# Test the build locally
npm install -g serve
serve -s build
```

### Package Management

```bash
# Update all packages
npm update

# Check for outdated packages
npm outdated

# Install specific version
npm install axios@1.6.2

# Remove package
npm uninstall chart.js

# Clear cache
npm cache clean --force

# Reinstall all
rm -rf node_modules package-lock.json
npm install
```

### Linting & Formatting

```bash
# Run ESLint
npm run lint

# Fix ESLint issues
npm run lint -- --fix

# Format with Prettier
npx prettier --write "src/**/*.{js,jsx,json,css}"
```

---

## Desktop App Commands

### Setup

**Windows:**
```powershell
cd desktop-app
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
cd desktop-app
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r desktop_requirements.txt

# Or install individually:
pip install PyQt5==5.15.10
pip install matplotlib==3.8.2
pip install pandas==2.1.3
pip install requests==2.31.0
pip install numpy==1.26.2
```

### Run Desktop App

```bash
# Run application
python main.py

# Run with Python 3 explicitly
python3 main.py
```

### Build Executable (Optional)

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py

# Executable will be in dist/
```

---

## Git Commands

### Basic Operations

```bash
# Check status
git status

# Add files
git add .
git add backend/api/views.py

# Commit
git commit -m "Add CSV upload feature"

# Push
git push origin main

# Pull
git pull origin main

# View history
git log --oneline
```

### Branching

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# List branches
git branch

# Delete branch
git branch -d feature/old-feature

# Merge branch
git checkout main
git merge feature/new-feature
```

### Stashing

```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply stash
git stash apply

# Pop stash
git stash pop
```

### Undoing Changes

```bash
# Discard changes in file
git checkout -- filename

# Unstage file
git reset HEAD filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## Deployment Commands

### Render (Backend)

```bash
# Install deployment dependencies
pip install gunicorn dj-database-url psycopg2-binary

# Create Procfile
echo "web: gunicorn chemical_equipment_viz.wsgi" > Procfile

# Collect static files
python manage.py collectstatic --no-input

# Test gunicorn locally
gunicorn chemical_equipment_viz.wsgi:application
```

### Netlify (Frontend)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize site
netlify init

# Deploy to production
netlify deploy --prod

# Or deploy specific directory
cd frontend-web
netlify deploy --prod --dir=build
```

### Heroku (Alternative)

```bash
# Install Heroku CLI
# Windows: Download from heroku.com
# Mac: brew install heroku/brew/heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create chemical-equipment-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail
```

### Docker (Optional)

```bash
# Build image
docker build -t chemical-equipment-visualizer .

# Run container
docker run -p 8000:8000 chemical-equipment-visualizer

# Docker Compose
docker-compose up
docker-compose down
```

---

## Troubleshooting Commands

### Port Issues

**Windows:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
lsof -ti:8000 | xargs kill -9

# Or with specific port
sudo lsof -i :8000
kill -9 <PID>
```

### Python Issues

```bash
# Check Python version
python --version
python3 --version

# Check installed packages
pip list
pip freeze

# Check specific package
pip show django

# Reinstall package
pip uninstall django
pip install django

# Clear pip cache
pip cache purge
```

### Node/npm Issues

```bash
# Check versions
node --version
npm --version

# Clear npm cache
npm cache clean --force

# Rebuild node modules
rm -rf node_modules package-lock.json
npm install

# Update npm
npm install -g npm@latest

# Fix permissions (Linux/Mac)
sudo chown -R $USER:$USER node_modules
```

### Database Issues

```bash
# Reset SQLite database
cd backend
rm db.sqlite3
rm -rf api/migrations/0*.py
python manage.py makemigrations
python manage.py migrate

# Check database
python manage.py dbshell

# In dbshell:
.tables
.schema api_equipmentdataset
.quit
```

### Django Issues

```bash
# Check Django installation
python -m django --version

# Check project structure
python manage.py check

# Show settings
python manage.py diffsettings

# Clear sessions
python manage.py clearsessions

# Flush database (CAUTION)
python manage.py flush
```

### Permission Issues

**macOS/Linux:**
```bash
# Make script executable
chmod +x setup.sh
chmod +x build.sh

# Fix ownership
sudo chown -R $USER:$USER .

# Fix Python permissions
sudo chmod -R 755 venv
```

**Windows:**
```powershell
# Run as Administrator
# Right-click PowerShell -> Run as Administrator

# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Quick Reference

### Start Everything

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend-web
npm start
```

**Terminal 3 - Desktop (Optional):**
```bash
cd desktop-app
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python main.py
```

### Stop Everything

```bash
# Press Ctrl+C in each terminal
# Or close terminal windows
```

### Clean Everything

```bash
# Clean Python
rm -rf backend/venv
rm -rf backend/__pycache__
rm -rf backend/*/__pycache__
rm backend/db.sqlite3

# Clean Node
rm -rf frontend-web/node_modules
rm frontend-web/package-lock.json

# Clean Desktop
rm -rf desktop-app/venv
```

### Full Reset

```bash
# CAUTION: This deletes everything and starts fresh
rm -rf backend/venv backend/db.sqlite3 backend/__pycache__
rm -rf frontend-web/node_modules frontend-web/package-lock.json
rm -rf desktop-app/venv

# Then run setup again
./setup.sh  # or follow manual setup steps
```

---

## Environment Variables

### Backend (.env)

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```bash
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
```

### Load Environment Variables

**Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
```

**Node.js:**
```javascript
// Automatically loaded by create-react-app
const API_URL = process.env.REACT_APP_API_URL;
```

---

## Useful Aliases (Optional)

Add to `.bashrc` or `.zshrc`:

```bash
# Project shortcuts
alias chem-backend='cd ~/chemical-equipment-visualizer/backend && source venv/bin/activate'
alias chem-frontend='cd ~/chemical-equipment-visualizer/frontend-web'
alias chem-desktop='cd ~/chemical-equipment-visualizer/desktop-app && source venv/bin/activate'

# Django shortcuts
alias dj-run='python manage.py runserver'
alias dj-migrate='python manage.py migrate'
alias dj-shell='python manage.py shell'

# npm shortcuts
alias nr='npm run'
alias ni='npm install'
alias ns='npm start'
```

---

## Testing Commands

### Test API with curl

```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Upload CSV (replace TOKEN)
curl -X POST http://localhost:8000/api/datasets/upload_csv/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "file=@sample_equipment_data.csv"

# Get datasets
curl http://localhost:8000/api/datasets/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---