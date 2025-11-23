# Quick Start Guide

Get the Chemical Equipment Parameter Visualizer up and running in 10 minutes!

## ⚡ Prerequisites Check

Run these commands to verify installations:

```bash
# Check Python (need 3.8+)
python --version

# Check Node.js (need 14+)
node --version

# Check npm
npm --version

# Check Git
git --version
```

If any are missing, install from:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Git: https://git-scm.com/

## 🚀 Super Quick Setup (Copy & Paste)

### Windows (PowerShell)

```powershell
# 1. Create project structure
mkdir chemical-equipment-visualizer
cd chemical-equipment-visualizer

# 2. Clone or download the files (or create structure manually)
# If you have the GitHub repo:
git clone <your-repo-url> .

# 3. Backend Setup
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install Django djangorestframework django-cors-headers pandas reportlab
django-admin startproject chemical_equipment_viz .
django-admin startapp api
python manage.py migrate
python manage.py createsuperuser
# Enter: admin / admin@example.com / admin123
python manage.py runserver

# Keep this running and open NEW terminal for frontend
```

### macOS/Linux (Bash)

```bash
# 1. Create project structure
mkdir chemical-equipment-visualizer
cd chemical-equipment-visualizer

# 2. Clone or download the files
git clone <your-repo-url> .

# 3. Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install Django djangorestframework django-cors-headers pandas reportlab
django-admin startproject chemical_equipment_viz .
django-admin startapp api
python manage.py migrate
python manage.py createsuperuser
# Enter: admin / admin@example.com / admin123
python manage.py runserver

# Keep this running and open NEW terminal for frontend
```

### Frontend Setup (All Platforms)

```bash
# In NEW terminal
cd frontend-web

# If using create-react-app (first time)
npx create-react-app .

# Install dependencies
npm install axios chart.js react-chartjs-2

# Start frontend
npm start
```

### Desktop App (Optional)

```bash
# In ANOTHER NEW terminal
cd desktop-app

# Windows:
python -m venv venv
venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# All platforms:
pip install PyQt5 matplotlib pandas requests
python main.py
```

## 🎯 First Time Usage

### Step 1: Register Account

1. Open web app: http://localhost:3000
2. Click "Register"
3. Enter:
   - Username: `testuser`
   - Email: `test@example.com` (optional)
   - Password: `testpass123`
4. Click "Register"

### Step 2: Upload Sample Data

1. Download `sample_equipment_data.csv` from project root
2. Click "Upload CSV" tab
3. Click "Browse" and select the CSV file
4. Click "Upload & Analyze"

### Step 3: View Results

You'll automatically see:
- ✅ Summary statistics cards
- 📊 Equipment type pie chart
- 📈 Parameter line chart
- 📋 Data table with all equipment
- 📄 PDF download button

## 🎨 What You Should See

### Web Application (http://localhost:3000)

```
┌─────────────────────────────────────┐
│  Chemical Equipment Visualizer      │
│  Welcome, testuser     [Logout]     │
├─────────────────────────────────────┤
│  [Upload CSV] [Visualization] [History] │
├─────────────────────────────────────┤
│  Summary Cards:                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ │
│  │ 20   │ │175.5 │ │66.5  │ │197.6 │ │
│  │Equip.│ │Flow  │ │Press │ │Temp  │ │
│  └──────┘ └──────┘ └──────┘ └──────┘ │
│                                       │
│  Charts:                             │
│  [Pie Chart] [Line Chart]            │
│                                       │
│  Data Table:                         │
│  Equipment | Type | Flow | Press...  │
│  ─────────────────────────────────   │
│  Pump-101  | Pump | 150.5| 45.2...  │
└─────────────────────────────────────┘
```

### Desktop Application

```
┌─────────────────────────────────────┐
│ Chemical Equipment Visualizer       │
│ Welcome, testuser    [Logout]       │
├─────────────────────────────────────┤
│ Tabs: [Upload] [Visualization] [History] │
├─────────────────────────────────────┤
│                                      │
│  Charts displayed here with         │
│  matplotlib visualization           │
│                                      │
│  Data table below charts            │
│                                      │
└─────────────────────────────────────┘
```

## 🐛 Quick Troubleshooting

### Backend Won't Start

**Error**: "Port 8000 is already in use"

```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <number> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Then restart:
python manage.py runserver
```

**Error**: "No module named 'rest_framework'"

```bash
pip install djangorestframework django-cors-headers
```

### Frontend Won't Start

**Error**: "npm ERR! Missing script: start"

```bash
# You're not in a React app directory
# Make sure you ran: npx create-react-app . first
cd frontend-web
npx create-react-app .
npm install axios chart.js react-chartjs-2
npm start
```

**Error**: "Module not found: Can't resolve 'axios'"

```bash
npm install axios chart.js react-chartjs-2
```

### Desktop App Won't Start

**Error**: "No module named 'PyQt5'"

```bash
# Try conda if pip fails:
conda install pyqt

# Or system package manager:
# Ubuntu/Debian:
sudo apt-get install python3-pyqt5

# macOS:
brew install pyqt5
```

### Can't Login

**Error**: "Invalid credentials"

1. Did you create a user? Try registering first.
2. Check backend is running on port 8000
3. Check browser console for CORS errors

## 📝 Testing the App

### Test Checklist

1. ✅ **Registration**
   - Can create new account
   - Get redirected after registration

2. ✅ **Login**
   - Can login with credentials
   - See welcome message

3. ✅ **CSV Upload**
   - Can select file
   - Upload succeeds
   - See success message

4. ✅ **Visualization**
   - See summary cards
   - See pie chart (type distribution)
   - See line chart (parameters)
   - See data table

5. ✅ **PDF Generation**
   - Click download button
   - PDF downloads successfully
   - PDF contains data

6. ✅ **History**
   - See uploaded datasets
   - Can view previous datasets
   - Limited to 5 entries

## 🎓 Next Steps

### Add More Data

Create your own CSV files with this format:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
My-Pump-1,Pump,100.0,50.0,80.0
My-Reactor-1,Reactor,200.0,100.0,400.0
```

### Customize the App

1. **Change colors** in `App.css`
2. **Add new charts** in visualization section
3. **Modify statistics** in backend views
4. **Add new equipment types**

### Deploy to Production

See `DEPLOYMENT.md` for full deployment guide.

Quick deploy options:
- **Backend**: Render (free tier)
- **Frontend**: Netlify (free tier)

## 📞 Need Help?

### Resources

- **Full README**: See `README.md` for detailed docs
- **VS Code Guide**: See `VSCODE_SETUP.md` for IDE setup
- **Deployment**: See `DEPLOYMENT.md` for production

### Common Questions

**Q: Can I use a different database?**
A: Yes! Update `DATABASES` in `settings.py` for PostgreSQL/MySQL

**Q: How do I add more fields to the CSV?**
A: Update the model in `models.py` and the serializer in `serializers.py`

**Q: Can I deploy this for free?**
A: Yes! Use Render (backend) + Netlify (frontend) free tiers

**Q: Is the desktop app required?**
A: No, it's optional. Web app works standalone.

## 🎉 Success!

If you see:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Can register and login
- ✅ Can upload CSV
- ✅ See charts and data

**Congratulations!** You're ready to develop! 🚀

---

**Time spent**: ~10 minutes
**Next**: Explore features, customize, or deploy!

For detailed information, see the complete `README.md`.
