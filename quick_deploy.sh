#!/bin/bash

# Quick Deploy Script for AI-Swap
# This script provides the fastest way to get your app running on a VPS

echo "🚀 Quick Deploy for AI-Swap"
echo "============================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root. Use a regular user with sudo access."
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
echo "🐍 Installing Python 3.10..."
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Install OpenCV dependencies
echo "🔧 Installing OpenCV dependencies..."
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

# Create app directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/ai-swap
sudo chown $USER:$USER /opt/ai-swap

# Copy files (assuming we're in the project root)
echo "📋 Copying application files..."
cp -r backend /opt/ai-swap/
cp -r frontend /opt/ai-swap/

# Create virtual environment
echo "🔧 Creating virtual environment..."
cd /opt/ai-swap
python3.10 -m venv venv

# Install dependencies
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p backend/uploads backend/results backend/logs
chmod 755 backend/uploads backend/results backend/logs

# Setup environment
if [ ! -f backend/.env ]; then
    echo "⚙️ Creating environment file..."
    cp backend/env.example backend/.env
    echo "📝 Please edit backend/.env with your configuration"
fi

echo ""
echo "✅ Quick deployment complete!"
echo ""
echo "🔧 To run the application:"
echo "   cd /opt/ai-swap"
echo "   source venv/bin/activate"
echo "   python backend/wsgi.py"
echo ""
echo "🌐 The app will be available at: http://your-server-ip:8000"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env with your configuration"
echo "2. Test the application"
echo "3. For production, consider running with gunicorn"
echo "4. Set up nginx for better performance" 