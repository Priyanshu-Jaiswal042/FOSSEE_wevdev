#!/bin/bash

echo "🚀 Installing All Dependencies"
echo "=============================="
echo ""

# Backend
echo "📦 Backend Dependencies..."
cd backend
if [ -d "venv" ]; then
    echo "Virtual environment exists, activating..."
else
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed successfully"
else
    echo "❌ Backend installation failed"
    exit 1
fi

deactivate
cd ..

# Frontend
echo ""
echo "📦 Frontend Dependencies..."
cd frontend-web

if [ -d "node_modules" ]; then
    echo "node_modules exists, updating..."
    npm update
else
    echo "Installing npm packages..."
    npm install
fi

if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed successfully"
else
    echo "❌ Frontend installation failed"
    exit 1
fi

cd ..

# Desktop
echo ""
echo "📦 Desktop App Dependencies..."
cd desktop-app

if [ -d "venv" ]; then
    echo "Virtual environment exists, activating..."
else
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r desktop_requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Desktop app dependencies installed successfully"
else
    echo "❌ Desktop app installation failed"
    exit 1
fi

deactivate
cd ..

echo ""
echo "=============================="
echo "🎉 All Dependencies Installed!"
echo "=============================="
echo ""
echo "Next steps:"
echo "1. cd backend && source venv/bin/activate && python manage.py migrate"
echo "2. cd frontend-web && npm start"
echo "3. cd desktop-app && source venv/bin/activate && python main.py"