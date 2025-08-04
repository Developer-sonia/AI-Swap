#!/bin/bash

# Manual VPS Setup Script for AI-Swap
# Run this script step by step for manual control

echo "🔧 Manual VPS Setup for AI-Swap"
echo "=================================="

# Step 1: Install Python 3.10
echo "Step 1: Installing Python 3.10..."
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Step 2: Install system dependencies
echo "Step 2: Installing system dependencies for OpenCV..."
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

# Step 3: Create application directory
echo "Step 3: Creating application directory..."
sudo mkdir -p /opt/ai-swap
sudo chown $USER:$USER /opt/ai-swap

# Step 4: Copy application files
echo "Step 4: Copying application files..."
# Assuming you're running this from the project root
cp -r backend /opt/ai-swap/
cp -r frontend /opt/ai-swap/

# Step 5: Create virtual environment
echo "Step 5: Creating Python virtual environment..."
cd /opt/ai-swap
python3.10 -m venv venv

# Step 6: Activate virtual environment and install dependencies
echo "Step 6: Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Step 7: Create necessary directories
echo "Step 7: Creating necessary directories..."
mkdir -p backend/uploads backend/results backend/logs
chmod 755 backend/uploads backend/results backend/logs

# Step 8: Setup environment file
echo "Step 8: Setting up environment configuration..."
if [ ! -f backend/.env ]; then
    cp backend/env.example backend/.env
    echo "📝 Environment file created. Please edit backend/.env with your configuration"
fi

echo ""
echo "✅ Manual setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your configuration"
echo "2. Test the application: cd /opt/ai-swap && source venv/bin/activate && python backend/wsgi.py"
echo "3. For production, consider setting up gunicorn and nginx"
echo ""
echo "🔧 To activate the virtual environment manually:"
echo "   cd /opt/ai-swap && source venv/bin/activate"
echo ""
echo "🚀 To run the application:"
echo "   cd /opt/ai-swap"
echo "   source venv/bin/activate"
echo "   python backend/wsgi.py" 